from src.utils.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class JobModel(Base):
    __tablename__ = "job"
    __table_args__ = {"schema": "audios_sac"}

    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, nullable=False)
    notify_id = Column(String, nullable=False)
    output_attachment = Column(String,nullable=False)
    status = Column(String,nullable=False)