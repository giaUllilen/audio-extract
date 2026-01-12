# audio-extract

## Descripción y propósito

El servicio **audio-extract** es una aplicación de procesamiento periódico que se encarga de extraer y gestionar audios de llamadas del sistema Genesys Cloud. Su función principal es:

- Consultar conversaciones telefónicas del día anterior desde Genesys Cloud
- Filtrar llamadas que incluyan participantes de tipo "agente" 
- Procesar los audios en lotes (batches) para optimizar el rendimiento
- Almacenar la información de audios y trabajos en base de datos PostgreSQL
- Enviar notificaciones por email sobre el estado del procesamiento
- Gestionar el ciclo de vida completo de los trabajos de extracción de audio

El servicio está diseñado para ejecutarse de forma automática y manejar grandes volúmenes de conversaciones de manera eficiente, excluyendo automáticamente los domingos del procesamiento.

## Repositorio

https://github.com/Interseguro/audio-extract.git

## Requisitos

- Python 3.10 o superior

## Estructura del proyecto

```
audio-extract/                       # Directorio raíz del proyecto de extracción de audio
├── src/                            # Código fuente principal del proyecto
│   ├── service/                    # Servicios de negocio de la aplicación
│   │   ├── __init__.py             # Inicializador del módulo service
│   │   └── audio_extract.py        # Implementación principal del servicio de extracción de audio
│   ├── utils/                      # Utilidades y herramientas comunes
│   │   ├── __init__.py             # Inicializador del módulo utils
│   │   ├── environment.py          # Configuración de variables de entorno
│   │   ├── logger.py               # Sistema de registro de eventos y logs
│   │   ├── threads.py              # Utilidades para manejo de hilos y concurrencia
│   │   ├── config_app.py           # Configuración principal de la aplicación
│   │   ├── database.py             # Configuración de conexión a base de datos
│   │   └── database_executes.py    # Ejecuciones SQL y operaciones de base de datos
│   ├── repository/                 # Capa de acceso a datos (patrón Repository)
│   │   ├── __init__.py             # Inicializador del módulo repository
│   │   ├── models/                 # Definiciones de modelos de datos (SQLAlchemy)
│   │   │   ├── __init__.py         # Inicializador del módulo models
│   │   │   ├── job_model.py        # Modelo para trabajos/tareas de procesamiento
│   │   │   ├── audio_model.py      # Modelo para información de audios y conversaciones
│   │   │   └── batch_model.py      # Modelo para procesamiento por lotes
│   │   ├── job_repository.py       # Repositorio para operaciones CRUD con trabajos
│   │   ├── audio_repository.py     # Repositorio para operaciones CRUD con audios
│   │   └── batch_repository.py     # Repositorio para operaciones CRUD con lotes
│   └── integrations/               # Integraciones con servicios externos
│       ├── __init__.py             # Inicializador del módulo integrations
│       ├── genesys_integration.py  # Integración con la plataforma Genesys Cloud
│       └── email_integration.py    # Integración para envío de notificaciones por email
├── main.py                         # Punto de entrada principal de la aplicación
├── requirements.txt                # Dependencias del proyecto Python
├── Dockerfile                      # Configuración para construcción de imagen Docker
├── runLocal.bat                    # Script para ejecutar la aplicación localmente en Windows
└── README.md                       # Documentación principal del proyecto
```

## Quickstart

Para levantar este servicio en ambiente local, ejecuta los siguientes comandos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/Interseguro/audio-extract.git
cd audio-extract

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno (ver sección Configuración esencial)

# 4. Ejecutar en Windows
runLocal.bat

# 4. Ejecutar en Linux/Mac
python main.py
```

## Configuración esencial

Las siguientes variables de entorno son necesarias para levantar este servicio:

### Base de datos PostgreSQL
```bash
PG_USER=tu_usuario_postgres
PG_PASSWORD=tu_password_postgres
PG_HOST=tu_host_postgres
PG_PORT=5432
PG_DATABASE=tu_database_postgres
```

### Genesys Cloud
```bash
GENESYS_CLOUD_CLIENT_ID=tu_client_id_genesys
GENESYS_CLOUD_CLIENT_SECRET=tu_client_secret_genesys
GENESYS_QUEUE_ID=id_de_la_cola_a_filtrar
```

### Configuración de procesamiento
```bash
BATCH_SIZE=90                        # Tamaño de lote para procesamiento
LOG_LEVEL=DEBUG                      # Nivel de logging
DEV_MODE=True                        # Modo desarrollo
```

### Notificaciones por email
```bash
NOTIFY_URL=url_del_servicio_de_notificaciones
EMAILS=email1@domain.com,email2@domain.com
EMAIL_MESSAGE=mensaje_personalizado_para_notificaciones
```

### Google Cloud (para servicios adicionales)
```bash
PROJECT_ID=tu_project_id_gcp
GOOGLE_APPLICATION_CREDENTIALS=ruta_al_archivo_credenciales.json
```

## Despliegue

**Dónde vive:** GCP Cloud Run

**Ambientes:** Dev / Stg / Prod → docs/deployment.md