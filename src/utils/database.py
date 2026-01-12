from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
import src.utils.environment as env

class Config:
    PG_URI = f"postgresql://{env.PG_USER}:{quote_plus(env.PG_PASSWORD)}@{env.PG_HOST}:{env.PG_PORT}/{env.PG_DATABASE}"

engine = create_engine(Config.PG_URI)
#Session = sessionmaker(bind=engine)
Base = declarative_base()