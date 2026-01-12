"""
Pruebas unitarias para BatchRepository
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.repository.batch_repository import BatchRepository
from src.repository.models.batch_model import BatchModel


class TestBatchRepository:
    """Pruebas para BatchRepository"""
    
    @patch('src.repository.batch_repository.Session')
    @patch('src.repository.batch_repository.engine')
    def test_insert_batch_success(self, mock_engine, mock_session_class, sample_batch_model):
        """Verifica que se pueda insertar un batch correctamente"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        
        repo = BatchRepository()
        
        # Act
        result = repo.insert(sample_batch_model)
        
        # Assert
        assert result is not None
        mock_session.add.assert_called_once_with(sample_batch_model)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_batch_model)
    
    @patch('src.repository.batch_repository.Session')
    @patch('src.repository.batch_repository.engine')
    def test_insert_batch_exception(self, mock_engine, mock_session_class, sample_batch_model):
        """Verifica el manejo de excepciones al insertar un batch"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.commit.side_effect = Exception("Database error")
        
        repo = BatchRepository()
        
        # Act
        result = repo.insert(sample_batch_model)
        
        # Assert
        assert result is None
    
    @patch('src.repository.batch_repository.Session')
    @patch('src.repository.batch_repository.engine')
    def test_update_status_success(self, mock_engine, mock_session_class, sample_batch_model):
        """Verifica que se pueda actualizar el estado de un batch"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_batch_model
        
        repo = BatchRepository()
        
        # Act
        result = repo.update_status("gemini-123", "SUCCESS")
        
        # Assert
        assert result is True
        assert sample_batch_model.status == "SUCCESS"
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_batch_model)
    
    @patch('src.repository.batch_repository.Session')
    @patch('src.repository.batch_repository.engine')
    def test_update_status_batch_not_found(self, mock_engine, mock_session_class):
        """Verifica el comportamiento cuando el batch no existe"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        repo = BatchRepository()
        
        # Act
        result = repo.update_status("non-existent-id", "SUCCESS")
        
        # Assert
        assert result is False
    
    @patch('src.repository.batch_repository.Session')
    @patch('src.repository.batch_repository.engine')
    def test_update_status_exception(self, mock_engine, mock_session_class, sample_batch_model):
        """Verifica el manejo de excepciones al actualizar el estado"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_batch_model
        mock_session.commit.side_effect = Exception("Update error")
        
        repo = BatchRepository()
        
        # Act
        result = repo.update_status("gemini-123", "SUCCESS")
        
        # Assert
        assert result is False
    
    @patch('src.repository.batch_repository.Session')
    @patch('src.repository.batch_repository.engine')
    def test_delete_batch_success(self, mock_engine, mock_session_class, sample_batch_model):
        """Verifica que se pueda eliminar un batch correctamente"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        
        repo = BatchRepository()
        
        # Act
        result = repo.delete(sample_batch_model)
        
        # Assert
        assert result is True
        mock_session.delete.assert_called_once_with(sample_batch_model)
        mock_session.commit.assert_called_once()
    
    @patch('src.repository.batch_repository.Session')
    @patch('src.repository.batch_repository.engine')
    def test_delete_batch_exception(self, mock_engine, mock_session_class, sample_batch_model):
        """Verifica el manejo de excepciones al eliminar un batch"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.commit.side_effect = Exception("Delete error")
        
        repo = BatchRepository()
        
        # Act
        result = repo.delete(sample_batch_model)
        
        # Assert
        assert result is False

