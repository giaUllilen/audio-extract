"""
Pruebas unitarias para EmailIntegration
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import pytz
from src.integrations.email_integration import EmailIntegration
import requests


class TestEmailIntegration:
    """Pruebas para EmailIntegration"""
    
    @patch('src.integrations.email_integration.AudioRepository')
    def test_init(self, mock_audio_repo):
        """Verifica la inicialización de EmailIntegration"""
        # Act
        integration = EmailIntegration()
        
        # Assert
        assert integration.audio_db is not None
    
    def test_milliseconds_to_hms_zero(self):
        """Verifica conversión de 0 milisegundos"""
        # Arrange
        with patch('src.integrations.email_integration.AudioRepository'):
            integration = EmailIntegration()
        
        # Act
        result = integration.milliseconds_to_hms(0)
        
        # Assert
        assert result == "00:00:00"
    
    def test_milliseconds_to_hms_one_minute(self):
        """Verifica conversión de 1 minuto"""
        # Arrange
        with patch('src.integrations.email_integration.AudioRepository'):
            integration = EmailIntegration()
        
        # Act
        result = integration.milliseconds_to_hms(60000)  # 1 minuto
        
        # Assert
        assert result == "00:01:00"
    
    def test_milliseconds_to_hms_complex(self):
        """Verifica conversión de tiempo complejo"""
        # Arrange
        with patch('src.integrations.email_integration.AudioRepository'):
            integration = EmailIntegration()
        
        # Act
        result = integration.milliseconds_to_hms(3665000)  # 1h 1m 5s
        
        # Assert
        assert result == "01:01:05"
    
    def test_milliseconds_to_hms_hours(self):
        """Verifica conversión con horas"""
        # Arrange
        with patch('src.integrations.email_integration.AudioRepository'):
            integration = EmailIntegration()
        
        # Act
        result = integration.milliseconds_to_hms(7200000)  # 2 horas
        
        # Assert
        assert result == "02:00:00"
    
    @patch('src.integrations.email_integration.requests.post')
    @patch('src.integrations.email_integration.env')
    @patch('src.integrations.email_integration.AudioRepository')
    def test_send_email_success(self, mock_audio_repo, mock_env, mock_post):
        """Verifica el envío exitoso de email"""
        # Arrange
        mock_env.EMAILS = "user1@test.com,user2@test.com"
        mock_env.EMAIL_MESSAGE = "Test message for"
        mock_env.NOTIFY_URL = "http://test.com/notify"
        
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        integration = EmailIntegration()
        
        # Act
        integration.send_email()
        
        # Assert
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]['json']['priority'] == 'sendinblue'
        assert len(call_args[1]['json']['to']) == 2
    
    @patch('src.integrations.email_integration.requests.post')
    @patch('src.integrations.email_integration.env')
    @patch('src.integrations.email_integration.AudioRepository')
    def test_send_email_request_exception(self, mock_audio_repo, mock_env, mock_post):
        """Verifica el manejo de excepciones al enviar email"""
        # Arrange
        mock_env.EMAILS = "user1@test.com"
        mock_env.EMAIL_MESSAGE = "Test message"
        mock_env.NOTIFY_URL = "http://test.com/notify"
        
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        
        integration = EmailIntegration()
        
        # Act & Assert
        with pytest.raises(requests.exceptions.RequestException):
            integration.send_email()
    
    @patch('src.integrations.email_integration.datetime')
    @patch('src.integrations.email_integration.requests.post')
    @patch('src.integrations.email_integration.env')
    @patch('src.integrations.email_integration.AudioRepository')
    def test_send_email_sunday_adjustment(self, mock_audio_repo, mock_env, mock_post, mock_datetime):
        """Verifica que si es domingo, se ajuste a sábado"""
        # Arrange
        lima_tz = pytz.timezone("America/Lima")
        # Crear un domingo
        sunday = datetime(2024, 1, 7, 10, 0, 0, tzinfo=lima_tz)  # Domingo
        
        mock_datetime.now.return_value = sunday
        mock_env.EMAILS = "test@test.com"
        mock_env.EMAIL_MESSAGE = "Test"
        mock_env.NOTIFY_URL = "http://test.com"
        
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        integration = EmailIntegration()
        
        # Act
        integration.send_email()
        
        # Assert
        mock_post.assert_called_once()
        # Verificar que la fecha en el título sea del sábado (06/01/2024)
        call_args = mock_post.call_args
        assert "06/01/2024" in call_args[1]['json']['title']
    
    @patch('src.integrations.email_integration.requests.post')
    @patch('src.integrations.email_integration.env')
    @patch('src.integrations.email_integration.AudioRepository')
    def test_send_email_multiple_recipients(self, mock_audio_repo, mock_env, mock_post):
        """Verifica que se puedan enviar emails a múltiples destinatarios"""
        # Arrange
        mock_env.EMAILS = "user1@test.com, user2@test.com, user3@test.com"
        mock_env.EMAIL_MESSAGE = "Test message"
        mock_env.NOTIFY_URL = "http://test.com/notify"
        
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        integration = EmailIntegration()
        
        # Act
        integration.send_email()
        
        # Assert
        call_args = mock_post.call_args
        recipients = call_args[1]['json']['to']
        assert len(recipients) == 3
        assert recipients[0]['email'] == "user1@test.com"
        assert recipients[1]['email'] == "user2@test.com"
        assert recipients[2]['email'] == "user3@test.com"

