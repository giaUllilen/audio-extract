from src.utils.database import engine
from src.repository.models.batch_model import BatchModel
from src.utils.logger import logger
from sqlalchemy.orm import Session
from sqlalchemy import text

class BatchRepository:
    
    def get(self,id_conversation):
        logger.debug("[Repository] Inicio del metodo get")
        try:
            with Session(engine) as db:
                result = db.query(BatchModel).filter(id_conversation=id_conversation).first()
            return result
        except Exception as e:
            logger.error(f"Error en obtener el registro: {e}")
            return []
        
        
    def insert(self, batch) -> BatchModel:
        logger.debug("[Repository] Inicio del metodo insert para el batch con id: " + batch.genesys_batch_id)
        try:
            with Session(engine) as db:
                db.add(batch)
                db.commit()
                db.refresh(batch)
            return batch

        except Exception as e:
            logger.error(f"Error en insertar el registro: {e}")
            return None

    def update_status(self, gemini_batch_id: str, new_status: str) -> bool:
        logger.debug(f"[Repository] Actualizando estado del batch {gemini_batch_id} a '{new_status}'")
        try:
            with Session(engine) as db:
                batch = db.query(BatchModel).filter(BatchModel.gemini_batch_id == gemini_batch_id).first()

                if not batch:
                    logger.warning(f"No se encontró el batch con ID {gemini_batch_id}")
                    return False

                batch.status = new_status
                db.commit()
                db.refresh(batch)
                return True

        except Exception as e:
            logger.error(f"Error al actualizar el estado del batch {gemini_batch_id}: {e}")
            return False


    def delete(self, batch: BatchModel) -> bool:
        logger.debug("[Repository] Inicio del metodo delete")
        try:
            with Session(engine) as db:
                db.delete(batch)
                db.commit()
            success = True
        except Exception as e:
            logger.error(f"Error en eliminar el registro: {e}")
            success = False
        return success
