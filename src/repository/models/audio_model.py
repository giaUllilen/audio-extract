from src.utils.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class AudioModel(Base):
    __tablename__ = "audio"
    __table_args__ = {"schema": "audios_sac"}

    id = Column(Integer, primary_key=True)
    id_conversation = Column(String, nullable=False) #Genesys
    status = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    call_date = Column(DateTime, nullable=False)
    call_duration = Column(Integer, nullable=False)

    reason = Column(String)
    reason_short = Column(String)
    summary = Column(String)

    initial_feeling = Column(String)
    final_feeling = Column(String)
    product_type = Column(String)
    category_typification = Column(String)
    typification = Column(String)
    typification_reason = Column(String) 

    batch_id = Column(Integer, ForeignKey("audios_sac.batch.id"))  

