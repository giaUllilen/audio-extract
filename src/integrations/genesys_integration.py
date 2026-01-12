import os
from src.utils.logger import logger
import PureCloudPlatformClientV2 as genesys_sdk
from PureCloudPlatformClientV2.rest import ApiException
import src.utils.environment as env
from src.repository.models.job_model import JobModel
from src.repository.models.batch_model import BatchModel
from src.repository.batch_repository import BatchRepository
from src.repository.audio_repository import AudioRepository
from src.repository.models.audio_model import AudioModel
from PureCloudPlatformClientV2.models import BatchDownloadRequest, BatchDownloadJobSubmission
from typing import List
import time
from datetime import datetime

class GenesysIntegration:
    
    def __init__(self):
        self.client_id = env.GENESYS_CLOUD_CLIENT_ID
        self.client_secret = env.GENESYS_CLOUD_CLIENT_SECRET 
        self.conversation_api = None
        self.recording_api = None
        self.analytics_api = None
        self.batch_db = BatchRepository()
        self.audio_db = AudioRepository()

    def authenticate(self):
        api_client = genesys_sdk.ApiClient()

        try:
            api_client.get_client_credentials_token(self.client_id, self.client_secret)
            self.conversation_api = genesys_sdk.ConversationsApi(api_client)
            self.recording_api = genesys_sdk.RecordingApi(api_client)
            self.analytics_api = genesys_sdk.AnalyticsApi(api_client)
            
            logger.info(f"[Genesys integration] Autenticacion exitosa con genesys")
            
        except ApiException as e:
            logger.error(f"[Genesys integration] Error en autenticacion: {e}")

    def get_recording_metadata(self, conversation_id):
        try:
            response = self.recording_api.get_conversation_recordings(conversation_id)

            return response
        except ApiException as e:
            logger.error(f"[Genesys integration] Error al obtener metadatos de grabaciones: {e}")
            return None
        
    def init_batch_download(self, conversations: List[AudioModel], job: JobModel, start_date: str) -> None:
        batch_size = env.BATCH_SIZE

        if not conversations:
            logger.debug(f"[Genesys integration] La lista de conversaciones esta vacia")
            return
        
        logger.info(f"[Genesys integration]Se encontraron {len(conversations)} conversaciones") 

        for i in range(0, len(conversations), batch_size):
            batch = conversations[i: i + batch_size]
            logger.info(f"[Genesys integration] Procesando batch con {len(batch)} grabaciones")

            final_batch_submission = BatchDownloadJobSubmission()
            final_batch_submission.batch_download_request_list = []

            for conversation in batch:
                # Extraer conversation_id del objeto AudioModel
                conversation_id = conversation.id_conversation
                batch_submission = self.add_conversation_to_batch(conversation_id)
                
                if batch_submission and batch_submission.batch_download_request_list:                 
                    first_recording = batch_submission.batch_download_request_list[0]
                    final_batch_submission.batch_download_request_list.append(first_recording)

            if not final_batch_submission.batch_download_request_list:
                logger.warning("[Genesys integration] No hay conversaciones validas en este batch")
                continue

            batch_process_result = self.recording_api.post_recording_batchrequests(final_batch_submission)

            if not batch_process_result:
                return

            logger.info(f"[Genesys integration] Inicia insercion a base de datos")
            
            process_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
            
            new_batch = BatchModel(
                genesys_batch_id=batch_process_result.id,
                audios_count=len(batch),
                start_date=time.asctime(time.localtime()),
                process_date=process_date,
                status='PENDING GENESYS',
                job_id=job.id
            )
            
            result = self.batch_db.insert(new_batch)

            for conversation in batch:
                conversation.batch_id = result.genesys_batch_id
                self.audio_db.insert(conversation)
            
            if result:
                logger.debug(f"[Genesys integration] Se inserto el batch correctamente")
                
    def add_conversation_to_batch(self, conversation_id: str) -> BatchDownloadJobSubmission:
        batch_list: List[BatchDownloadRequest] = []
        try:
            batch_submission = BatchDownloadJobSubmission()
            recordings_data = self.recording_api.get_conversation_recordingmetadata(conversation_id)

            if recordings_data:
                for recording in recordings_data:
                    batch_req = BatchDownloadRequest()
                    batch_req.conversation_id = recording.conversation_id
                    batch_req.recording_id = recording.id
                    batch_list.append(batch_req) 
                    logger.debug(f"[Genesys integration] Conversacion agregada al batch: {recording.conversation_id}")

                batch_submission.batch_download_request_list = batch_list
            else:
                logger.debug(f"[Genesys integration] No se encontraron grabaciones para la conversacion: {conversation_id}")
                raise ValueError(f"No se encontraron grabaciones para la conversacion: {conversation_id}")

        except ApiException as e:
            logger.error(f"[Genesys integration] Error al obtener metadata de grabaciones: {e}")
            raise
        
        return batch_submission

    def get_call_duration(self, recording) -> int:
        try:
            # Buscar en todos los participantes
            for participant in recording.participants:
                if participant.purpose == "agent":  # Solo buscar en participantes de tipo agente
                    for session in participant.sessions:
                        if hasattr(session, 'metrics') and session.metrics:
                            for metric in session.metrics:
                                if metric.name == "tHandle":
                                    # Son milisegundos
                                    duration_minutes = metric.value 
                                    logger.debug(f"[Audio transcript] tHandle encontrado: {metric.value}ms")
                                    return duration_minutes
            
            logger.warning(f"[Audio transcript] No se encontró tHandle para {recording.conversation_id}")
            return 0
            
        except Exception as e:
            logger.error(f"[Audio transcript] Error extrayendo duración: {e}")
            return 0    