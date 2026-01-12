"""
Pruebas unitarias para los modelos de datos
"""
import pytest
from datetime import datetime
from src.repository.models.audio_model import AudioModel
from src.repository.models.batch_model import BatchModel
from src.repository.models.job_model import JobModel


class TestAudioModel:
    """Pruebas para el modelo AudioModel"""
    
    def test_audio_model_creation(self):
        """Verifica que se pueda crear un AudioModel correctamente"""
        audio = AudioModel(
            id_conversation="test-123",
            status="PENDING",
            creation_date=datetime.now(),
            call_date=datetime.now(),
            call_duration=60000
        )
        
        assert audio.id_conversation == "test-123"
        assert audio.status == "PENDING"
        assert audio.call_duration == 60000
        assert isinstance(audio.creation_date, datetime)
        assert isinstance(audio.call_date, datetime)
    
    def test_audio_model_with_optional_fields(self):
        """Verifica que se puedan asignar campos opcionales"""
        audio = AudioModel(
            id_conversation="test-456",
            status="SUCCESS",
            creation_date=datetime.now(),
            call_date=datetime.now(),
            call_duration=120000,
            reason="Test reason",
            summary="Test summary",
            initial_feeling="positive",
            final_feeling="satisfied",
            batch_id=1
        )
        
        assert audio.reason == "Test reason"
        assert audio.summary == "Test summary"
        assert audio.initial_feeling == "positive"
        assert audio.final_feeling == "satisfied"
        assert audio.batch_id == 1
    
    def test_audio_model_tablename(self):
        """Verifica que el nombre de tabla sea correcto"""
        assert AudioModel.__tablename__ == "audio"
        assert AudioModel.__table_args__["schema"] == "audios_sac"


class TestBatchModel:
    """Pruebas para el modelo BatchModel"""
    
    def test_batch_model_creation(self):
        """Verifica que se pueda crear un BatchModel correctamente"""
        batch = BatchModel(
            start_date=datetime.now(),
            audios_count=10,
            status="PENDING GENESYS"
        )
        
        assert batch.audios_count == 10
        assert batch.status == "PENDING GENESYS"
        assert isinstance(batch.start_date, datetime)
    
    def test_batch_model_with_all_fields(self):
        """Verifica que se puedan asignar todos los campos"""
        now = datetime.now()
        batch = BatchModel(
            start_date=now,
            end_date=now,
            process_date=now,
            audios_count=25,
            status="SUCCESS",
            error_message=None,
            genesys_batch_id="gen-123",
            gemini_batch_id="gem-456",
            gemini_category_batch_id="cat-789",
            gemini_typification_batch_id="typ-012",
            job_id=1
        )
        
        assert batch.genesys_batch_id == "gen-123"
        assert batch.gemini_batch_id == "gem-456"
        assert batch.job_id == 1
        assert batch.audios_count == 25
    
    def test_batch_model_tablename(self):
        """Verifica que el nombre de tabla sea correcto"""
        assert BatchModel.__tablename__ == "batch"
        assert BatchModel.__table_args__["schema"] == "audios_sac"


class TestJobModel:
    """Pruebas para el modelo JobModel"""
    
    def test_job_model_creation(self):
        """Verifica que se pueda crear un JobModel correctamente"""
        job = JobModel(
            creation_date=datetime.now(),
            status="PROCESSING"
        )
        
        assert job.status == "PROCESSING"
        assert isinstance(job.creation_date, datetime)
    
    def test_job_model_with_all_fields(self):
        """Verifica que se puedan asignar todos los campos"""
        job = JobModel(
            id=1,
            creation_date=datetime.now(),
            notify_id="notif-123",
            output_attachment="path/to/file.csv",
            status="SUCCESS"
        )
        
        assert job.id == 1
        assert job.notify_id == "notif-123"
        assert job.output_attachment == "path/to/file.csv"
        assert job.status == "SUCCESS"
    
    def test_job_model_tablename(self):
        """Verifica que el nombre de tabla sea correcto"""
        assert JobModel.__tablename__ == "job"
        assert JobModel.__table_args__["schema"] == "audios_sac"

