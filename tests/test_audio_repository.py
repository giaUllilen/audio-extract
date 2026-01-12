"""
Pruebas unitarias para AudioRepository
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.repository.audio_repository import AudioRepository
from src.repository.models.audio_model import AudioModel


class TestAudioRepository:
    """Pruebas para AudioRepository"""
    
    @patch('src.repository.audio_repository.Session')
    @patch('src.repository.audio_repository.engine')
    def test_get_audio_success(self, mock_engine, mock_session_class, sample_audio_model):
        """Verifica que se pueda obtener un audio por ID de conversación"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_audio_model
        
        repo = AudioRepository()
        
        # Act
        result = repo.get("test-conv-123")
        
        # Assert
        assert result is not None
        assert result.id_conversation == "test-conv-123"
        mock_session.query.assert_called_once_with(AudioModel)
    
    @patch('src.repository.audio_repository.Session')
    @patch('src.repository.audio_repository.engine')
    def test_get_audio_not_found(self, mock_engine, mock_session_class):
        """Verifica el comportamiento cuando no se encuentra un audio"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        repo = AudioRepository()
        
        # Act
        result = repo.get("non-existent-id")
        
        # Assert
        assert result is None
    
    @patch('src.repository.audio_repository.Session')
    @patch('src.repository.audio_repository.engine')
    def test_insert_audio_success(self, mock_engine, mock_session_class, sample_audio_model):
        """Verifica que se pueda insertar un audio correctamente"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        
        repo = AudioRepository()
        
        # Act
        result = repo.insert(sample_audio_model)
        
        # Assert
        assert result is not None
        mock_session.add.assert_called_once_with(sample_audio_model)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_audio_model)
    
    @patch('src.repository.audio_repository.Session')
    @patch('src.repository.audio_repository.engine')
    def test_insert_audio_exception(self, mock_engine, mock_session_class, sample_audio_model):
        """Verifica el manejo de excepciones al insertar un audio"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.commit.side_effect = Exception("Database error")
        
        repo = AudioRepository()
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repo.insert(sample_audio_model)
        
        assert "Database error" in str(exc_info.value)
    
    @patch('src.repository.audio_repository.Session')
    @patch('src.repository.audio_repository.engine')
    def test_delete_audio_success(self, mock_engine, mock_session_class, sample_audio_model):
        """Verifica que se pueda eliminar un audio correctamente"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        
        repo = AudioRepository()
        
        # Act
        result = repo.delete(sample_audio_model)
        
        # Assert
        assert result is True
        mock_session.delete.assert_called_once_with(sample_audio_model)
        mock_session.commit.assert_called_once()
    
    @patch('src.repository.audio_repository.Session')
    @patch('src.repository.audio_repository.engine')
    def test_delete_audio_exception(self, mock_engine, mock_session_class, sample_audio_model):
        """Verifica el manejo de excepciones al eliminar un audio"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.commit.side_effect = Exception("Delete error")
        
        repo = AudioRepository()
        
        # Act
        result = repo.delete(sample_audio_model)
        
        # Assert
        assert result is False

