"""
Pruebas unitarias para JobRepository
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.repository.job_repository import JobRepository
from src.repository.models.job_model import JobModel


class TestJobRepository:
    """Pruebas para JobRepository"""
    
    @patch('src.repository.job_repository.Session')
    @patch('src.repository.job_repository.engine')
    def test_insert_job_success(self, mock_engine, mock_session_class):
        """Verifica que se pueda insertar un job correctamente"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        
        job = JobModel(
            creation_date=datetime.now(),
            status="PROCESSING"
        )
        job.id = 1  # Simular ID generado por la BD
        
        repo = JobRepository()
        
        # Act
        result = repo.insert(job)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert isinstance(result.creation_date, datetime)
        mock_session.add.assert_called_once_with(job)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(job)
    
    @patch('src.repository.job_repository.Session')
    @patch('src.repository.job_repository.engine')
    def test_insert_job_exception(self, mock_engine, mock_session_class):
        """Verifica el manejo de excepciones al insertar un job"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.commit.side_effect = Exception("Database error")
        
        job = JobModel(
            creation_date=datetime.now(),
            status="PROCESSING"
        )
        
        repo = JobRepository()
        
        # Act
        result = repo.insert(job)
        
        # Assert
        assert result is None
    
    @patch('src.repository.job_repository.Session')
    @patch('src.repository.job_repository.engine')
    def test_update_status_success(self, mock_engine, mock_session_class, sample_job_model):
        """Verifica que se pueda actualizar el estado de un job"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_job_model
        
        repo = JobRepository()
        
        # Act
        result = repo.update_status(1, "SUCCESS")
        
        # Assert
        assert result is True
        assert sample_job_model.status == "SUCCESS"
        mock_session.commit.assert_called_once()
    
    @patch('src.repository.job_repository.Session')
    @patch('src.repository.job_repository.engine')
    def test_update_status_job_not_found(self, mock_engine, mock_session_class):
        """Verifica el comportamiento cuando el job no existe"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        repo = JobRepository()
        
        # Act
        result = repo.update_status(999, "SUCCESS")
        
        # Assert
        assert result is False
    
    @patch('src.repository.job_repository.Session')
    @patch('src.repository.job_repository.engine')
    def test_update_status_exception(self, mock_engine, mock_session_class, sample_job_model):
        """Verifica el manejo de excepciones al actualizar el estado"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = sample_job_model
        mock_session.commit.side_effect = Exception("Update error")
        
        repo = JobRepository()
        
        # Act
        result = repo.update_status(1, "SUCCESS")
        
        # Assert
        assert result is False

