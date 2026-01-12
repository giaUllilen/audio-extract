from src.utils.logger import logger
import src.utils.environment as env
import requests
from datetime import datetime, timedelta
import pytz
from src.repository.models.job_model import JobModel
from src.repository.audio_repository import AudioRepository

class EmailIntegration:

    def __init__(self):
        self.audio_db = AudioRepository()

    def milliseconds_to_hms(self, milliseconds: int) -> str:
        """Convierte milisegundos a formato HH:MM:SS"""
        if milliseconds == 0:
            return "00:00:00"
        
        # Convertir milisegundos a segundos totales
        total_seconds = int(milliseconds / 1000)
        
        # Calcular horas, minutos y segundos
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def send_email(self):
        #Fecha de proceso
        lima_time_zone = pytz.timezone("America/Lima")

        #Se toma todo el dia anterior
        yesterday = datetime.now(lima_time_zone) - timedelta(days=1)

        # Si yesterday es domingo (weekday() == 6), ajustar a sabado
        if yesterday.weekday() == 6:
            yesterday -= timedelta(days=1)

        date_process = yesterday.strftime("%d/%m/%Y")

        emails = (env.EMAILS).split(",")
        emails_list = [{"name": "", "email": email.strip()} for email in emails if email.strip()]

        email_data = {
            "title": "Transcripcion y Analisis de AUDIOS-SAC " + f"{date_process}", 
            "subject": "Transcripcion y Analisis de AUDIOS-SAC " + f"{date_process}",
            "priority": "sendinblue",
            "htmlContent": env.EMAIL_MESSAGE + f" {date_process}.",
            "to": emails_list,
            
        }
        
        try:
            response = requests.post(
                env.NOTIFY_URL,
                json=email_data
            )
            
            response.raise_for_status()
            logger.info("Email enviado exitosamente")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al enviar el correo: {str(e)}")
            raise
    