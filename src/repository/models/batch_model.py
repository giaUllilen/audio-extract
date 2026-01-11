from src.utils.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class BatchModel(Base):
    __tablename__ = "batch"
    __table_args__ = {"schema": "audios_sac"}

    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    process_date = Column(DateTime)

    audios_count = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    error_message = Column(String)
    
    genesys_batch_id = Column(String)
    gemini_batch_id = Column(String)
    gemini_category_batch_id = Column(String)
    gemini_typification_batch_id = Column(String)
    job_id = Column(Integer)
    