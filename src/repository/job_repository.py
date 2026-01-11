from src.utils.database import engine
from src.repository.models.job_model import JobModel
from src.utils.logger import logger
from sqlalchemy.orm import Session
from sqlalchemy import text

class JobRepository:
        
    def insert(self, job:JobModel) -> JobModel:
        logger.debug("[Repository] Inicio del metodo insert")
        try:
            with Session(engine) as db:
                db.add(job)
                db.commit()
                db.refresh(job)

            job_model = JobModel(
                id = job.id,
                creation_date = job.creation_date
            )
            return job_model

        except Exception as e:
            logger.error(f"Error en insertar el registro: {e}")
            return None

    def update_status(self, job_id: int, new_status: str) -> bool:
        logger.debug(f"[Repository] Actualizando estado del job {job_id} a {new_status}")
        try:
            with Session(engine) as db:
                job = db.query(JobModel).filter(JobModel.id == job_id).first()
                if job:
                    job.status = new_status
                    db.commit()
                    logger.info(f"[Repository] Job {job_id} actualizado al estado {new_status}")
                    return True
                else:
                    logger.warning(f"[Repository] Job {job_id} no encontrado")
                    return False
        except Exception as e:
            logger.error(f"[Repository] Error al actualizar el estado del job {job_id}: {e}")
            return False