"""
Pruebas unitarias para AudioExtractService
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import pytz
from src.service.audio_extract import AudioExtractService
from src.repository.models.audio_model import AudioModel
from src.repository.models.job_model import JobModel
from PureCloudPlatformClientV2.rest import ApiException


class TestAudioExtractService:
    """Pruebas para AudioExtractService"""
    
    @patch('src.service.audio_extract.EmailIntegration')
    @patch('src.service.audio_extract.AudioRepository')
    @patch('src.service.audio_extract.JobRepository')
    @patch('src.service.audio_extract.BatchRepository')
    @patch('src.service.audio_extract.GenesysIntegration')
    def test_init(self, mock_genesys, mock_batch_repo, mock_job_repo, 
                  mock_audio_repo, mock_email):
        """Verifica la inicialización del servicio"""
        # Arrange
        mock_genesys_instance = Mock()
        mock_genesys.return_value = mock_genesys_instance
        
        # Act
        service = AudioExtractService()
        
        # Assert
        assert service.genesys is not None
        assert service.batch_db is not None
        assert service.job_db is not None
        assert service.audio_db is not None
        assert service.email_integration is not None
        mock_genesys_instance.authenticate.assert_called_once()
    
    @patch('src.service.audio_extract.EmailIntegration')
    @patch('src.service.audio_extract.AudioRepository')
    @patch('src.service.audio_extract.JobRepository')
    @patch('src.service.audio_extract.BatchRepository')
    @patch('src.service.audio_extract.GenesysIntegration')
    def test_execute_no_conversations(self, mock_genesys, mock_batch_repo, 
                                     mock_job_repo, mock_audio_repo, mock_email):
        """Verifica la ejecución cuando no hay conversaciones"""
        # Arrange
        mock_genesys_instance = Mock()
        mock_genesys.return_value = mock_genesys_instance
        
        mock_job_repo_instance = Mock()
        mock_job_repo.return_value = mock_job_repo_instance
        
        mock_email_instance = Mock()
        mock_email.return_value = mock_email_instance
        
        service = AudioExtractService()
        
        job = JobModel(id=1, creation_date=datetime.now(), status="PROCESSING")
        service.get_audios_ids_by_date_range = Mock(return_value=([], job))
        
        # Act
        service.execute()
        
        # Assert
        mock_job_repo_instance.update_status.assert_called_once_with(1, "SUCCESS")
        mock_email_instance.send_email.assert_called_once()
    
    @patch('src.service.audio_extract.EmailIntegration')
    @patch('src.service.audio_extract.AudioRepository')
    @patch('src.service.audio_extract.JobRepository')
    @patch('src.service.audio_extract.BatchRepository')
    @patch('src.service.audio_extract.GenesysIntegration')
    def test_execute_with_conversations(self, mock_genesys, mock_batch_repo,
                                       mock_job_repo, mock_audio_repo, mock_email):
        """Verifica la ejecución con conversaciones disponibles"""
        # Arrange
        mock_genesys_instance = Mock()
        mock_genesys.return_value = mock_genesys_instance
        
        service = AudioExtractService()
        
        job = JobModel(id=1, creation_date=datetime.now(), status="PROCESSING")
        conversations = [
            AudioModel(id_conversation="conv-1", status="PENDING",
                      creation_date=datetime.now(), call_date=datetime.now(), 
                      call_duration=60000)
        ]
        
        service.get_audios_ids_by_date_range = Mock(return_value=(conversations, job))
        
        # Act
        service.execute()
        
        # Assert
        mock_genesys_instance.init_batch_download.assert_called_once()
    
    @patch('src.service.audio_extract.env')
    @patch('src.service.audio_extract.EmailIntegration')
    @patch('src.service.audio_extract.AudioRepository')
    @patch('src.service.audio_extract.JobRepository')
    @patch('src.service.audio_extract.BatchRepository')
    @patch('src.service.audio_extract.GenesysIntegration')
    def test_get_audios_ids_by_date_range_success(self, mock_genesys, mock_batch_repo,
                                                   mock_job_repo, mock_audio_repo, 
                                                   mock_email, mock_env,
                                                   sample_conversation_response):
        """Verifica la obtención de IDs de audios por rango de fechas"""
        # Arrange
        mock_env.BATCH_SIZE = 10
        mock_env.GENESYS_QUEUE_ID = "test-queue-id"
        
        mock_genesys_instance = Mock()
        mock_genesys.return_value = mock_genesys_instance
        
        mock_analytics_api = Mock()
        mock_analytics_api.post_analytics_conversations_details_query.return_value = sample_conversation_response
        mock_genesys_instance.analytics_api = mock_analytics_api
        mock_genesys_instance.get_call_duration.return_value = 120000
        
        mock_job_repo_instance = Mock()
        mock_job_repo.return_value = mock_job_repo_instance
        
        job = JobModel(id=1, creation_date=datetime.now(), status="PROCESSING")
        mock_job_repo_instance.insert.return_value = job
        
        service = AudioExtractService()
        
        # Act
        conversations, returned_job = service.get_audios_ids_by_date_range(
            "2024-01-01T00:00:00",
            "2024-01-01T23:59:59"
        )
        
        # Assert
        assert len(conversations) > 0
        assert returned_job.id == 1
        mock_job_repo_instance.insert.assert_called_once()
    
    @patch('src.service.audio_extract.env')
    @patch('src.service.audio_extract.EmailIntegration')
    @patch('src.service.audio_extract.AudioRepository')
    @patch('src.service.audio_extract.JobRepository')
    @patch('src.service.audio_extract.BatchRepository')
    @patch('src.service.audio_extract.GenesysIntegration')
    def test_get_audios_ids_filters_by_agent(self, mock_genesys, mock_batch_repo,
                                             mock_job_repo, mock_audio_repo,
                                             mock_email, mock_env):
        """Verifica que solo se incluyan conversaciones con agente"""
        # Arrange
        mock_env.BATCH_SIZE = 10
        mock_env.GENESYS_QUEUE_ID = "test-queue-id"
        
        # Crear conversación sin agente
        participant_no_agent = Mock()
        participant_no_agent.purpose = "customer"
        
        conv_no_agent = Mock()
        conv_no_agent.conversation_id = "conv-no-agent"
        conv_no_agent.conversation_start = datetime.now()
        conv_no_agent.participants = [participant_no_agent]
        
        # Crear conversación con agente
        participant_with_agent = Mock()
        participant_with_agent.purpose = "agent"
        
        conv_with_agent = Mock()
        conv_with_agent.conversation_id = "conv-with-agent"
        conv_with_agent.conversation_start = datetime.now()
        conv_with_agent.participants = [participant_with_agent]
        
        response = Mock()
        response.conversations = [conv_no_agent, conv_with_agent]
        
        mock_genesys_instance = Mock()
        mock_genesys.return_value = mock_genesys_instance
        
        mock_analytics_api = Mock()
        mock_analytics_api.post_analytics_conversations_details_query.return_value = response
        mock_genesys_instance.analytics_api = mock_analytics_api
        mock_genesys_instance.get_call_duration.return_value = 120000
        
        mock_job_repo_instance = Mock()
        mock_job_repo.return_value = mock_job_repo_instance
        job = JobModel(id=1, creation_date=datetime.now(), status="PROCESSING")
        mock_job_repo_instance.insert.return_value = job
        
        service = AudioExtractService()
        
        # Act
        conversations, _ = service.get_audios_ids_by_date_range(
            "2024-01-01T00:00:00",
            "2024-01-01T23:59:59"
        )
        
        # Assert
        assert len(conversations) == 1
        assert conversations[0].id_conversation == "conv-with-agent"
    
    @patch('src.service.audio_extract.env')
    @patch('src.service.audio_extract.EmailIntegration')
    @patch('src.service.audio_extract.AudioRepository')
    @patch('src.service.audio_extract.JobRepository')
    @patch('src.service.audio_extract.BatchRepository')
    @patch('src.service.audio_extract.GenesysIntegration')
    def test_get_audios_ids_api_exception(self, mock_genesys, mock_batch_repo,
                                          mock_job_repo, mock_audio_repo,
                                          mock_email, mock_env):
        """Verifica el manejo de excepciones de la API"""
        # Arrange
        mock_env.BATCH_SIZE = 10
        mock_env.GENESYS_QUEUE_ID = "test-queue-id"
        
        mock_genesys_instance = Mock()
        mock_genesys.return_value = mock_genesys_instance
        
        mock_analytics_api = Mock()
        mock_analytics_api.post_analytics_conversations_details_query.side_effect = ApiException("API Error")
        mock_genesys_instance.analytics_api = mock_analytics_api
        
        mock_job_repo_instance = Mock()
        mock_job_repo.return_value = mock_job_repo_instance
        job = JobModel(id=1, creation_date=datetime.now(), status="PROCESSING")
        mock_job_repo_instance.insert.return_value = job
        
        service = AudioExtractService()
        
        # Act
        conversations, returned_job = service.get_audios_ids_by_date_range(
            "2024-01-01T00:00:00",
            "2024-01-01T23:59:59"
        )
        
        # Assert
        assert len(conversations) == 0
        assert returned_job.id == 1
    
    @patch('src.service.audio_extract.datetime')
    @patch('src.service.audio_extract.EmailIntegration')
    @patch('src.service.audio_extract.AudioRepository')
    @patch('src.service.audio_extract.JobRepository')
    @patch('src.service.audio_extract.BatchRepository')
    @patch('src.service.audio_extract.GenesysIntegration')
    def test_execute_sunday_adjustment(self, mock_genesys, mock_batch_repo,
                                      mock_job_repo, mock_audio_repo, 
                                      mock_email, mock_datetime):
        """Verifica que si es domingo, se procese el sábado anterior"""
        # Arrange
        lima_tz = pytz.timezone("America/Lima")
        sunday = datetime(2024, 1, 7, 10, 0, 0, tzinfo=lima_tz)  # Domingo
        
        mock_datetime.now.return_value = sunday
        mock_datetime.strftime = datetime.strftime
        
        mock_genesys_instance = Mock()
        mock_genesys.return_value = mock_genesys_instance
        
        mock_job_repo_instance = Mock()
        mock_job_repo.return_value = mock_job_repo_instance
        
        mock_email_instance = Mock()
        mock_email.return_value = mock_email_instance
        
        service = AudioExtractService()
        
        job = JobModel(id=1, creation_date=datetime.now(), status="PROCESSING")
        service.get_audios_ids_by_date_range = Mock(return_value=([], job))
        
        # Act
        service.execute()
        
        # Assert
        # Verificar que se llamó con la fecha del sábado
        call_args = service.get_audios_ids_by_date_range.call_args[0]
        # El sábado sería 2024-01-06
        assert "2024-01-06" in call_args[0]

