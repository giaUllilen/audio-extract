# Pruebas Unitarias - Audio Extract

Este directorio contiene todas las pruebas unitarias para el proyecto de extracción de audio.

## Estructura

```
tests/
├── __init__.py                      # Inicialización del módulo de tests
├── conftest.py                      # Fixtures compartidos y configuración de pytest
├── test_models.py                   # Pruebas para los modelos de datos
├── test_audio_repository.py         # Pruebas para AudioRepository
├── test_batch_repository.py         # Pruebas para BatchRepository
├── test_job_repository.py           # Pruebas para JobRepository
├── test_genesys_integration.py      # Pruebas para GenesysIntegration
├── test_email_integration.py        # Pruebas para EmailIntegration
├── test_audio_extract_service.py    # Pruebas para AudioExtractService
├── requirements-test.txt            # Dependencias para tests
└── README.md                        # Este archivo
```

## Instalación de Dependencias

Para ejecutar las pruebas, primero instala las dependencias necesarias:

```bash
pip install -r tests/requirements-test.txt
```

## Ejecutar las Pruebas

### Ejecutar todas las pruebas

```bash
pytest tests/
```

### Ejecutar un archivo de pruebas específico

```bash
pytest tests/test_audio_repository.py
```

### Ejecutar una prueba específica

```bash
pytest tests/test_audio_repository.py::TestAudioRepository::test_get_audio_success
```

### Ejecutar con cobertura de código

```bash
pytest --cov=src --cov-report=html tests/
```

Esto generará un reporte HTML en `htmlcov/index.html` que puedes abrir en tu navegador.

### Ejecutar con verbose

```bash
pytest -v tests/
```

### Ejecutar pruebas en paralelo

```bash
pytest -n auto tests/
```

## Cobertura de Pruebas

Las pruebas cubren los siguientes componentes:

### Modelos (`test_models.py`)
- ✅ AudioModel
- ✅ BatchModel
- ✅ JobModel

### Repositorios
- ✅ AudioRepository (`test_audio_repository.py`)
  - Operaciones CRUD
  - Manejo de excepciones
  
- ✅ BatchRepository (`test_batch_repository.py`)
  - Operaciones CRUD
  - Actualización de estados
  - Manejo de excepciones
  
- ✅ JobRepository (`test_job_repository.py`)
  - Inserción de jobs
  - Actualización de estados
  - Manejo de excepciones

### Integraciones
- ✅ GenesysIntegration (`test_genesys_integration.py`)
  - Autenticación
  - Obtención de metadatos
  - Procesamiento de batches
  - Extracción de duración de llamadas
  - Manejo de errores de API
  
- ✅ EmailIntegration (`test_email_integration.py`)
  - Conversión de milisegundos a formato HMS
  - Envío de emails
  - Manejo de múltiples destinatarios
  - Ajuste de fechas (domingo -> sábado)

### Servicios
- ✅ AudioExtractService (`test_audio_extract_service.py`)
  - Inicialización del servicio
  - Ejecución con y sin conversaciones
  - Filtrado de conversaciones con agente
  - Obtención de audios por rango de fechas
  - Ajuste de fechas para domingos
  - Manejo de excepciones de API

## Fixtures Compartidos (`conftest.py`)

El archivo `conftest.py` contiene fixtures reutilizables en todas las pruebas:

- `mock_engine`: Mock del engine de SQLAlchemy
- `mock_session`: Mock de sesión de SQLAlchemy
- `sample_audio_model`: AudioModel de ejemplo
- `sample_batch_model`: BatchModel de ejemplo
- `sample_job_model`: JobModel de ejemplo
- `lima_timezone`: Zona horaria de Lima
- `mock_genesys_client`: Mock del cliente Genesys
- `mock_conversation_api`: Mock de API de conversaciones
- `mock_recording_api`: Mock de API de grabaciones
- `mock_analytics_api`: Mock de API de analytics
- `sample_conversation_response`: Respuesta de conversación simulada
- `sample_recording_metadata`: Metadatos de grabación simulados

## Buenas Prácticas

1. **Usar mocks para dependencias externas**: Todas las pruebas usan mocks para bases de datos y APIs externas
2. **Probar casos exitosos y de error**: Cada función tiene pruebas para casos normales y excepciones
3. **Nombres descriptivos**: Los nombres de las pruebas describen claramente qué están probando
4. **Arrange-Act-Assert**: Las pruebas siguen el patrón AAA para mayor claridad
5. **Fixtures compartidos**: Usar fixtures de conftest.py para evitar duplicación

## Agregar Nuevas Pruebas

Para agregar nuevas pruebas:

1. Crea un nuevo archivo `test_<modulo>.py`
2. Importa pytest y los módulos necesarios
3. Crea una clase `Test<NombreModulo>`
4. Agrega métodos de prueba con el prefijo `test_`
5. Usa fixtures de `conftest.py` cuando sea necesario
6. Ejecuta las pruebas para verificar

Ejemplo:

```python
import pytest
from unittest.mock import Mock, patch

class TestMiModulo:
    def test_mi_funcion_exitosa(self, sample_audio_model):
        # Arrange
        ...
        
        # Act
        result = mi_funcion()
        
        # Assert
        assert result is not None
```

## Notas Importantes

- Las pruebas no requieren una base de datos real, todo está mockeado
- Las variables de entorno se mockean en cada prueba
- Se usa `unittest.mock` para simular comportamiento de APIs externas
- La cobertura de código debe mantenerse por encima del 80%

## Solución de Problemas

### Error: ModuleNotFoundError
Asegúrate de estar ejecutando pytest desde el directorio raíz del proyecto:
```bash
cd audio-extract/
pytest tests/
```

### Error: ImportError
Verifica que todas las dependencias estén instaladas:
```bash
pip install -r requirements.txt
pip install -r tests/requirements-test.txt
```

### Pruebas fallan por variables de entorno
Las pruebas mockean las variables de entorno, no deberías necesitar un archivo `.env` para ejecutar las pruebas.

