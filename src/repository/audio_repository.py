from src.utils.database import engine
from src.repository.models.audio_model import AudioModel
from src.utils.logger import logger
from sqlalchemy.orm import Session
from sqlalchemy import text

class AudioRepository:

    def get(self, id_conversation: str) -> AudioModel:
        logger.debug("[Repository] Inicio del metodo get")
        try:
            with Session(engine) as db:
                result = db.query(AudioModel).filter(AudioModel.id_conversation == id_conversation).first()
            return result
        except Exception as e:
            logger.error(f"Error en obtener el registro: {e}")
            raise
        
    def insert(self, audio: AudioModel) -> AudioModel:
        logger.debug(f"[Repository] Inicio del metodo insert para el audio:{audio.id_conversation}" )
        try:
            with Session(engine) as db:
                db.add(audio)
                db.commit()
                db.refresh(audio)
            return audio

        except Exception as e:
            logger.error(f"Error en insertar el registro: {e}")
            raise

    def delete(self, audio: AudioModel) -> bool:
        logger.debug("[Repository] Inicio del metodo delete")
        try:
            with Session(engine) as db:
                db.delete(audio)
                db.commit()
            success = True
        except Exception as e:
            logger.error(f"Error en eliminar el registro: {e}")
            success = False
        return success
