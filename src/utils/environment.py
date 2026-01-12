from decouple import config

# Conexion a base de datos
PG_USER = config("PG_USER")
PG_PASSWORD = config("PG_PASSWORD")
PG_HOST = config("PG_HOST")
PG_PORT = config("PG_PORT", cast=int)
PG_DATABASE = config("PG_DATABASE")
GENESYS_CLOUD_CLIENT_ID = config("GENESYS_CLOUD_CLIENT_ID")
GENESYS_CLOUD_CLIENT_SECRET = config("GENESYS_CLOUD_CLIENT_SECRET")
BATCH_SIZE = config("BATCH_SIZE",cast=int)
GENESYS_QUEUE_ID = config("GENESYS_QUEUE_ID")
EMAILS = config("EMAILS")
EMAIL_MESSAGE = config("EMAIL_MESSAGE")
NOTIFY_URL = config("NOTIFY_URL")
