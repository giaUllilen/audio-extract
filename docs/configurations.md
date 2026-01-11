# Variables de entorno

| Variable | Descripción | Valores |
|----------|-------------|---------|
| `PG_USER` | Usuario de la base de datos PostgreSQL | `db_admin`, `appuser`, `postgres` |
| `PG_PASSWORD` | Contraseña de la base de datos PostgreSQL | `MySecureP@ss2024`, `DatabasePass123!` |
| `PG_HOST` | Host/IP del servidor de base de datos PostgreSQL | `192.168.1.100`, `localhost`, `database.mycompany.com` |
| `PG_PORT` | Puerto del servidor de base de datos PostgreSQL | `5432`, `5433` |
| `PG_DATABASE` | Nombre de la base de datos PostgreSQL | `audio_production_db`, `call_center_db` |
| `GENESYS_CLOUD_CLIENT_ID` | ID del cliente para autenticación con Genesys Cloud | `1234-5678-910ef-ghij-adgkiumn` |
| `GENESYS_CLOUD_CLIENT_SECRET` | Secreto del cliente para autenticación con Genesys Cloud | `Xy9Zab8CdEfGh7IjKlM6nOpQrS5tUvWx4YzA3BcD2eF` |
| `GENESYS_QUEUE_ID` | ID de la cola de Genesys para filtrar llamadas | `f8e7d6c5-b4a3-2109-8765-fedcba098765` |
| `BATCH_SIZE` | Tamaño del lote para procesamiento de conversaciones |  `100`, `75`, `50` |
| `EMAILS` | Lista de emails separados por coma para notificaciones | `notifications@company.com`, `support@example.com,alerts@example.com` |
| `EMAIL_MESSAGE` | Mensaje personalizado para las notificaciones por email | `Sistema de audio: Sin actividad detectada`, `Reporte de procesamiento diario` |
| `NOTIFY_URL` | URL del servicio de notificaciones por email | `https://api.notifications.example.com/v2/send/email`, `http://localhost:9000/notify` |
| `LOG_LEVEL` | Nivel de logging de la aplicación | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `DEV_MODE` | Modo de desarrollo (habilita funciones adicionales) | `True`, `False` |
| `PORT` | Puerto en el que se ejecuta la aplicación | `3000`, `8080`, `5000` |
| `SWAGGER_UI` | Habilitar interfaz Swagger UI | `True`, `False` |
| `PROJECT_ID` | ID del proyecto en Google Cloud Platform | `my-gcp-project-2024`, `audio-processing-prod` |
