from decouple import config

# Conexion a base de datos
PG_USER = config("PG_USER", default="test_user")
PG_PASSWORD = config("PG_PASSWORD", default="test_password")
PG_HOST = config("PG_HOST", default="localhost")
PG_PORT = config("PG_PORT", cast=int, default=5432)
PG_DATABASE = config("PG_DATABASE", default="test_db")
GENESYS_CLOUD_CLIENT_ID = config("GENESYS_CLOUD_CLIENT_ID", default="test_client_id")
GENESYS_CLOUD_CLIENT_SECRET = config("GENESYS_CLOUD_CLIENT_SECRET", default="test_secret")
BATCH_SIZE = config("BATCH_SIZE", cast=int, default=100)
GENESYS_QUEUE_ID = config("GENESYS_QUEUE_ID", default="test_queue_id")
EMAILS = config("EMAILS", default="test@example.com")
EMAIL_MESSAGE = config("EMAIL_MESSAGE", default="Test message")
NOTIFY_URL = config("NOTIFY_URL", default="http://localhost:8080")
LOG_LEVEL = config("LOG_LEVEL", default="DEBUG")
