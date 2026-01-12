"""
Configuración compartida para las pruebas unitarias
"""
import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.repository.models.audio_model import AudioModel
from src.repository.models.batch_model import BatchModel
from src.repository.models.job_model import JobModel
from src.utils.database import Base


@pytest.fixture
def mock_engine():
    """Mock del engine de SQLAlchemy"""
    return Mock()


@pytest.fixture
def mock_session():
    """Mock de la sesión de SQLAlchemy"""
    session = MagicMock(spec=Session)
    return session


@pytest.fixture
def sample_audio_model():
    """Fixture que retorna un AudioModel de ejemplo"""
    return AudioModel(
        id=1,
        id_conversation="test-conv-123",
        status="PENDING",
        creation_date=datetime.now(),
        call_date=datetime.now(),
        call_duration=60000,
        reason="Test reason",
        summary="Test summary",
        batch_id=1
    )


@pytest.fixture
def sample_batch_model():
    """Fixture que retorna un BatchModel de ejemplo"""
    return BatchModel(
        id=1,
        genesys_batch_id="genesys-123",
        gemini_batch_id="gemini-123",
        audios_count=10,
        start_date=datetime.now(),
        process_date=datetime.now(),
        status="PENDING GENESYS",
        job_id=1
    )


@pytest.fixture
def sample_job_model():
    """Fixture que retorna un JobModel de ejemplo"""
    return JobModel(
        id=1,
        creation_date=datetime.now(),
        status="PROCESSING"
    )


@pytest.fixture
def lima_timezone():
    """Fixture que retorna la zona horaria de Lima"""
    return pytz.timezone("America/Lima")


@pytest.fixture
def mock_genesys_client():
    """Mock del cliente de Genesys"""
    mock_client = Mock()
    mock_client.get_client_credentials_token = Mock()
    return mock_client


@pytest.fixture
def mock_conversation_api():
    """Mock de la API de conversaciones de Genesys"""
    return Mock()


@pytest.fixture
def mock_recording_api():
    """Mock de la API de grabaciones de Genesys"""
    return Mock()


@pytest.fixture
def mock_analytics_api():
    """Mock de la API de analytics de Genesys"""
    return Mock()


@pytest.fixture
def sample_conversation_response():
    """Mock de una respuesta de conversación de Genesys"""
    participant_mock = Mock()
    participant_mock.purpose = "agent"
    
    session_mock = Mock()
    metric_mock = Mock()
    metric_mock.name = "tHandle"
    metric_mock.value = 120000  # 2 minutos en milisegundos
    session_mock.metrics = [metric_mock]
    participant_mock.sessions = [session_mock]
    
    conv_mock = Mock()
    conv_mock.conversation_id = "conv-123"
    conv_mock.conversation_start = datetime.now()
    conv_mock.participants = [participant_mock]
    
    response = Mock()
    response.conversations = [conv_mock]
    
    return response


@pytest.fixture
def sample_recording_metadata():
    """Mock de metadata de grabación"""
    recording = Mock()
    recording.conversation_id = "conv-123"
    recording.id = "rec-456"
    return [recording]

