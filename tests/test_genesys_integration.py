"""
Pruebas unitarias para GenesysIntegration
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.integrations.genesys_integration import GenesysIntegration
from src.repository.models.audio_model import AudioModel
from src.repository.models.job_model import JobModel
from PureCloudPlatformClientV2.rest import ApiException


class TestGenesysIntegration:
    """Pruebas para GenesysIntegration"""
    
    @patch('src.integrations.genesys_integration.env')
    def test_init(self, mock_env):
        """Verifica la inicialización de GenesysIntegration"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-client-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        # Act
        integration = GenesysIntegration()
        
        # Assert
        assert integration.client_id == "test-client-id"
        assert integration.client_secret == "test-secret"
        assert integration.conversation_api is None
        assert integration.recording_api is None
        assert integration.analytics_api is None
    
    @patch('src.integrations.genesys_integration.genesys_sdk')
    @patch('src.integrations.genesys_integration.env')
    def test_authenticate_success(self, mock_env, mock_genesys_sdk):
        """Verifica la autenticación exitosa con Genesys"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-client-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        mock_api_client = Mock()
        mock_genesys_sdk.ApiClient.return_value = mock_api_client
        
        integration = GenesysIntegration()
        
        # Act
        integration.authenticate()
        
        # Assert
        mock_api_client.get_client_credentials_token.assert_called_once_with(
            "test-client-id",
            "test-secret"
        )
        assert integration.conversation_api is not None
        assert integration.recording_api is not None
        assert integration.analytics_api is not None
    
    @patch('src.integrations.genesys_integration.genesys_sdk')
    @patch('src.integrations.genesys_integration.env')
    def test_authenticate_failure(self, mock_env, mock_genesys_sdk):
        """Verifica el manejo de errores en la autenticación"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-client-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        mock_api_client = Mock()
        mock_api_client.get_client_credentials_token.side_effect = ApiException("Auth failed")
        mock_genesys_sdk.ApiClient.return_value = mock_api_client
        
        integration = GenesysIntegration()
        
        # Act
        integration.authenticate()
        
        # Assert - No debe lanzar excepción, solo logear el error
        assert integration.conversation_api is None
    
    @patch('src.integrations.genesys_integration.env')
    def test_get_recording_metadata_success(self, mock_env, sample_recording_metadata):
        """Verifica que se puedan obtener los metadatos de grabación"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        integration = GenesysIntegration()
        integration.recording_api = Mock()
        integration.recording_api.get_conversation_recordings.return_value = sample_recording_metadata
        
        # Act
        result = integration.get_recording_metadata("conv-123")
        
        # Assert
        assert result is not None
        assert len(result) > 0
        assert result[0].conversation_id == "conv-123"
    
    @patch('src.integrations.genesys_integration.env')
    def test_get_recording_metadata_api_exception(self, mock_env):
        """Verifica el manejo de excepciones al obtener metadatos"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        integration = GenesysIntegration()
        integration.recording_api = Mock()
        integration.recording_api.get_conversation_recordings.side_effect = ApiException("Error")
        
        # Act
        result = integration.get_recording_metadata("conv-123")
        
        # Assert
        assert result is None
    
    @patch('src.integrations.genesys_integration.env')
    def test_get_call_duration_with_thandle(self, mock_env):
        """Verifica que se pueda extraer la duración de la llamada"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        # Crear mock de recording con métricas
        metric_mock = Mock()
        metric_mock.name = "tHandle"
        metric_mock.value = 120000  # 2 minutos
        
        session_mock = Mock()
        session_mock.metrics = [metric_mock]
        
        participant_mock = Mock()
        participant_mock.purpose = "agent"
        participant_mock.sessions = [session_mock]
        
        recording_mock = Mock()
        recording_mock.conversation_id = "conv-123"
        recording_mock.participants = [participant_mock]
        
        integration = GenesysIntegration()
        
        # Act
        duration = integration.get_call_duration(recording_mock)
        
        # Assert
        assert duration == 120000
    
    @patch('src.integrations.genesys_integration.env')
    def test_get_call_duration_without_thandle(self, mock_env):
        """Verifica el comportamiento cuando no hay métrica tHandle"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        participant_mock = Mock()
        participant_mock.purpose = "agent"
        participant_mock.sessions = []
        
        recording_mock = Mock()
        recording_mock.conversation_id = "conv-123"
        recording_mock.participants = [participant_mock]
        
        integration = GenesysIntegration()
        
        # Act
        duration = integration.get_call_duration(recording_mock)
        
        # Assert
        assert duration == 0
    
    @patch('src.integrations.genesys_integration.env')
    def test_add_conversation_to_batch_success(self, mock_env, sample_recording_metadata):
        """Verifica que se pueda agregar una conversación al batch"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        integration = GenesysIntegration()
        integration.recording_api = Mock()
        integration.recording_api.get_conversation_recordingmetadata.return_value = sample_recording_metadata
        
        # Act
        result = integration.add_conversation_to_batch("conv-123")
        
        # Assert
        assert result is not None
        assert len(result.batch_download_request_list) > 0
        assert result.batch_download_request_list[0].conversation_id == "conv-123"
    
    @patch('src.integrations.genesys_integration.env')
    def test_add_conversation_to_batch_no_recordings(self, mock_env):
        """Verifica el comportamiento cuando no hay grabaciones"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        
        integration = GenesysIntegration()
        integration.recording_api = Mock()
        integration.recording_api.get_conversation_recordingmetadata.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            integration.add_conversation_to_batch("conv-123")
        
        assert "No se encontraron grabaciones" in str(exc_info.value)
    
    @patch('src.integrations.genesys_integration.env')
    @patch('src.integrations.genesys_integration.BatchRepository')
    @patch('src.integrations.genesys_integration.AudioRepository')
    def test_init_batch_download_empty_list(self, mock_audio_repo, mock_batch_repo, mock_env):
        """Verifica el comportamiento con lista vacía de conversaciones"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        mock_env.BATCH_SIZE = 10
        
        integration = GenesysIntegration()
        job = JobModel(id=1, creation_date=datetime.now(), status="PROCESSING")
        
        # Act
        result = integration.init_batch_download([], job, "2024-01-01T00:00:00")
        
        # Assert
        assert result is None
    
    @patch('src.integrations.genesys_integration.env')
    @patch('src.integrations.genesys_integration.BatchRepository')
    @patch('src.integrations.genesys_integration.AudioRepository')
    def test_init_batch_download_with_conversations(self, mock_audio_repo, mock_batch_repo, mock_env):
        """Verifica el procesamiento de conversaciones en batches"""
        # Arrange
        mock_env.GENESYS_CLOUD_CLIENT_ID = "test-id"
        mock_env.GENESYS_CLOUD_CLIENT_SECRET = "test-secret"
        mock_env.BATCH_SIZE = 2
        
        mock_batch_repo_instance = Mock()
        mock_batch_repo.return_value = mock_batch_repo_instance
        mock_batch_repo_instance.insert.return_value = Mock(genesys_batch_id="batch-123")
        
        mock_audio_repo_instance = Mock()
        mock_audio_repo.return_value = mock_audio_repo_instance
        
        integration = GenesysIntegration()
        integration.recording_api = Mock()
        integration.batch_db = mock_batch_repo_instance
        integration.audio_db = mock_audio_repo_instance
        
        # Mock para add_conversation_to_batch
        mock_batch_submission = Mock()
        mock_batch_request = Mock()
        mock_batch_submission.batch_download_request_list = [mock_batch_request]
        integration.add_conversation_to_batch = Mock(return_value=mock_batch_submission)
        
        # Mock para post_recording_batchrequests
        mock_batch_result = Mock()
        mock_batch_result.id = "genesys-batch-123"
        integration.recording_api.post_recording_batchrequests.return_value = mock_batch_result
        
        conversations = [
            AudioModel(id_conversation="conv-1", status="PENDING", 
                      creation_date=datetime.now(), call_date=datetime.now(), call_duration=60000),
            AudioModel(id_conversation="conv-2", status="PENDING",
                      creation_date=datetime.now(), call_date=datetime.now(), call_duration=60000)
        ]
        
        job = JobModel(id=1, creation_date=datetime.now(), status="PROCESSING")
        
        # Act
        integration.init_batch_download(conversations, job, "2024-01-01T00:00:00")
        
        # Assert
        assert mock_batch_repo_instance.insert.called
        assert mock_audio_repo_instance.insert.call_count == 2

