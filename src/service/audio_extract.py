from datetime import datetime
import time
import pytz
import requests
import os
import io
from typing import List, Tuple, Dict
from src.integrations.genesys_integration import GenesysIntegration
from src.integrations.email_integration import EmailIntegration
from PureCloudPlatformClientV2.models import ConversationQuery
from PureCloudPlatformClientV2.rest import ApiException
from src.repository.models.batch_model import BatchModel
from src.repository.batch_repository import BatchRepository
from src.repository.models.job_model import JobModel
from src.repository.job_repository import JobRepository
from src.repository.models.audio_model import AudioModel
from src.repository.audio_repository import AudioRepository
from datetime import datetime, timedelta
from src.utils.logger import logger
import src.utils.environment as env

class AudioExtractService:
    
    def __init__(self) -> None:
        self.genesys = GenesysIntegration()
        self.genesys.authenticate()
        self.batch_db = BatchRepository()
        self.job_db = JobRepository()
        self.audio_db = AudioRepository()
        self.email_integration = EmailIntegration()

    def execute(self) -> None:
        #Se considera zona horaria Lima
        lima_time_zone = pytz.timezone("America/Lima")

        #Se toma todo el dia anterior
        yesterday = datetime.now(lima_time_zone) - timedelta(days=1)

        # Si yesterday es domingo (weekday() == 6), ajustar a sabado
        if yesterday.weekday() == 6:
            yesterday -= timedelta(days=1)

        start_date = yesterday.strftime("%Y-%m-%dT00:00:00")
        end_date = yesterday.strftime("%Y-%m-%dT23:59:59")
        
        conversations, job = self.get_audios_ids_by_date_range(start_date, end_date)
        if len(conversations) == 0:
            # No hay conversaciones, actualizar job a SUCCESS y enviar notificación
            self.job_db.update_status(job.id, "SUCCESS")
            logger.info(f"[Audio extract] No se encontraron conversaciones para procesar. Job {job.id} marcado como SUCCESS")
            self.email_integration.send_email()
            
        else:
            logger.info(f"[Audio extract] Se encontraron {len(conversations)} conversaciones para procesar")
            self.genesys.init_batch_download(conversations, job, start_date)

    
    def get_audios_ids_by_date_range(self, start_date: str, end_date: str) -> Tuple[List[str], JobModel]:
        interval = f"{start_date}/{end_date}"
        page_number = 1
        page_size = env.BATCH_SIZE

        #Se considera zona horaria Lima y fecha actual
        lima_time_zone = pytz.timezone("America/Lima")
        today = datetime.now(lima_time_zone)
        
        job = JobModel(
            creation_date=today,
            status='PROCESSING'
        )
        job = self.job_db.insert(job)
        filtered_conversations = []            
        while True:
            query = ConversationQuery()
            query.interval = interval
            query.paging = {"pageNumber": page_number, "pageSize": page_size}
            query.order = "asc"
            query.order_by = "conversationStart"
            query.segment_filters = [{
                "type": "and",
                "predicates": [
                    {
                        "type": "dimension",
                        "dimension": "queueId",
                        "operator": "matches",
                        "value": env.GENESYS_QUEUE_ID
                    }
                ]
            }]

            try:
                response = self.genesys.analytics_api.post_analytics_conversations_details_query(query)
                if not response.conversations:
                    break
                #Si quieres revisar que campos vienen de genesys, descomenta el siguiente bloque
                '''
                for resp in response.conversations:
                    with open('conversation_response_test.txt', 'a') as f:
                        f.write(f"\n\nConversation ID: {resp.conversation_id}\n")
                        f.write(str(resp))
                        f.write("\n" + "="*50 + "\n")
                '''
                # Filtrar conversaciones que tengan al menos un participante "agent" 
                for conv in response.conversations:
                    has_agent = False
                    if conv.participants:
                        for participant in conv.participants:
                            if participant.purpose == "agent":
                                has_agent = True
                                break
                    
                    if has_agent:
                        #Atributos que se extraen de Genesys
                        duration_milliseconds = self.genesys.get_call_duration(conv)
                        call_date = getattr(conv, 'conversation_start', None)

                        audio = AudioModel(
                            id_conversation=conv.conversation_id,
                            status='PENDING',
                            creation_date=datetime.now(),
                            call_date=call_date,
                            call_duration=duration_milliseconds
                        )
                        filtered_conversations.append(audio)
                        
                        
                        logger.info(f"[Audio extract] Conversacion {conv.conversation_id} incluida (tiene Agent)")
                    else:
                        logger.info(f"[Audio extract] Conversacion {conv.conversation_id} excluida (no tiene Agent)")     
                
                logger.info(f"[Audio extract] Pagina {page_number}: {len(filtered_conversations)} conversaciones con Agent de {len(response.conversations)} totales")
                
                if len(response.conversations) < page_size:
                    break
                
                page_number += 1  

            except ApiException as e:
                logger.error(f"[Audio extract] Error al obtener IDs de conversaciones: {e}")
                return [], job

        logger.info(f"[Audio extract] Total de conversaciones con 'agent' obtenidas: {len(filtered_conversations)}")
        return filtered_conversations, job

    