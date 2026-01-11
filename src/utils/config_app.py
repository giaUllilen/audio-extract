from decouple import config
from urllib.parse import quote_plus


class Config:
    # Ejemplo de conexion a Postgres
    PG_URI = f"postgresql://{config('PG_USER')}:{quote_plus(config('PG_PASSWORD'))}@{config('PG_HOST')}:{config('PG_PORT')}/{config('PG_DATABASE')}"

    # Ejemplo de conexion a MSSQL
    #MS_URI = f"mssql+pyodbc://{config('MS_USER')}:{quote_plus(config('MS_PASSWORD'))}@{config('MS_HOST')}:{config('MS_PORT')}/{config('MS_DATABASE')}"