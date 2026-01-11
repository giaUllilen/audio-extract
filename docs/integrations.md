# Integraciones

## APIs HTTP Externas

| Dependencia | Propósito | Focalpoint |
|-------------|-----------|------------|
| Genesys Cloud Platform API | Extracción de audios de conversaciones y metadata de grabaciones desde la plataforma Genesys Cloud | |
| API de Notificaciones (SendInBlue) | Envío de correos electrónicos de notificación sobre el proceso de extracción de audios | |

## Detalles de Integración

### 1. Genesys Cloud Platform API

**SDK Utilizado:** `PureCloudPlatformClientV2` (versión 222.0.0)

**Autenticación:**
- Tipo: OAuth 2.0 Client Credentials
- Configuración:
  - `GENESYS_CLOUD_CLIENT_ID`: ID del cliente para autenticación
  - `GENESYS_CLOUD_CLIENT_SECRET`: Secret del cliente para autenticación

**Endpoints/APIs Consumidas:**

#### 1.1. Analytics API - Query de Conversaciones
- **Método:** `post_analytics_conversations_details_query(query)`
- **Propósito:** Obtener conversaciones filtradas por rango de fechas y cola específica
- **Parámetros:**
  - `interval`: Rango de fechas en formato ISO 8601 (ej: "2024-01-01T00:00:00/2024-01-01T23:59:59")
  - `paging`: Paginación con `pageNumber` y `pageSize`
  - `order`: Orden ascendente ("asc")
  - `orderBy`: Ordenado por "conversationStart"
  - `segmentFilters`: Filtros por dimensión de cola (`queueId`)
- **Respuesta:** Lista de conversaciones con metadata incluyendo participantes, métricas y timestamps
- **Ubicación en código:** `src/service/audio_extract.py` - línea 92

#### 1.2. Recording API - Metadata de Grabaciones
- **Método:** `get_conversation_recordingmetadata(conversation_id)`
- **Propósito:** Obtener los metadatos de las grabaciones de una conversación específica
- **Parámetros:**
  - `conversation_id`: ID único de la conversación
- **Respuesta:** Lista de grabaciones asociadas a la conversación con sus IDs
- **Ubicación en código:** `src/integrations/genesys_integration.py` - línea 110

#### 1.3. Recording API - Obtener Grabaciones
- **Método:** `get_conversation_recordings(conversation_id)`
- **Propósito:** Obtener las grabaciones completas de una conversación
- **Parámetros:**
  - `conversation_id`: ID único de la conversación
- **Respuesta:** Datos completos de las grabaciones
- **Ubicación en código:** `src/integrations/genesys_integration.py` - línea 43

#### 1.4. Recording API - Batch Download Request
- **Método:** `post_recording_batchrequests(batch_submission)`
- **Propósito:** Crear una solicitud de descarga masiva de grabaciones
- **Parámetros:**
  - `batch_submission`: Objeto `BatchDownloadJobSubmission` que contiene:
    - `batch_download_request_list`: Lista de objetos `BatchDownloadRequest` con:
      - `conversation_id`: ID de la conversación
      - `recording_id`: ID de la grabación
- **Respuesta:** Objeto con el `id` del batch procesado en Genesys
- **Configuración:** Tamaño del batch controlado por `BATCH_SIZE` (variable de entorno)
- **Ubicación en código:** `src/integrations/genesys_integration.py` - línea 79

**Flujo de Integración:**
1. Autenticación mediante Client Credentials
2. Consulta de conversaciones por rango de fechas y cola específica (Analytics API)
3. Filtrado de conversaciones que tienen participante tipo "agent"
4. Extracción de duración de llamadas desde la métrica "tHandle" de las sesiones
5. Para cada conversación válida, obtención de metadata de grabaciones
6. Agrupación de grabaciones en lotes (batch) según `BATCH_SIZE`
7. Envío de solicitud de descarga masiva por cada lote
8. Almacenamiento de batch IDs en base de datos para seguimiento

**Manejo de Errores:**
- Se capturan excepciones del tipo `ApiException` del SDK
- Los errores se registran mediante el sistema de logging
- En caso de error al obtener metadata, se lanza una excepción `ValueError`

---

### 2. API de Notificaciones (SendInBlue)

**Protocolo:** HTTP REST
**Biblioteca Utilizada:** `requests` (versión 2.31.0)

**Endpoint:**

#### 2.1. Envío de Email
- **Método HTTP:** `POST`
- **URL:** Configurada en variable de entorno `NOTIFY_URL`
- **Propósito:** Enviar notificaciones por correo electrónico sobre el proceso de extracción de audios
- **Headers implícitos:** Content-Type: application/json
- **Body (JSON):**
  ```json
  {
    "title": "Transcripcion y Analisis de AUDIOS-SAC [fecha]",
    "subject": "Transcripcion y Analisis de AUDIOS-SAC [fecha]",
    "priority": "sendinblue",
    "htmlContent": "[Mensaje personalizado + fecha]",
    "to": [
      {
        "name": "",
        "email": "usuario@ejemplo.com"
      }
    ]
  }
  ```
- **Configuración:**
  - `NOTIFY_URL`: URL del endpoint de notificaciones
  - `EMAILS`: Lista de correos separados por comas
  - `EMAIL_MESSAGE`: Mensaje base del correo
- **Respuesta esperada:** Status HTTP 2xx para indicar éxito
- **Ubicación en código:** `src/integrations/email_integration.py` - línea 55

**Flujo de Integración:**
1. Cálculo de fecha de proceso (día anterior en zona horaria de Lima)
2. Ajuste de fecha si el día anterior es domingo (se toma el sábado)
3. Construcción del payload con título, asunto, contenido HTML y destinatarios
4. Envío de solicitud POST con datos en formato JSON
5. Validación de respuesta mediante `raise_for_status()`

**Manejo de Errores:**
- Se capturan excepciones del tipo `requests.exceptions.RequestException`
- Los errores se registran mediante el sistema de logging
- La excepción se propaga hacia arriba después de registrarse

**Cuándo se invoca:**
- Al finalizar el proceso de extracción de audios
- Cuando no se encuentran conversaciones para procesar (job marcado como SUCCESS)

