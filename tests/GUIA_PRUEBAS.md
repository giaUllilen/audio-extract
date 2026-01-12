# Guía de Pruebas Unitarias - Audio Extract

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Ejecución de Pruebas](#ejecución-de-pruebas)
4. [Estructura de las Pruebas](#estructura-de-las-pruebas)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Interpretación de Resultados](#interpretación-de-resultados)
7. [Mejores Prácticas](#mejores-prácticas)

## 📖 Introducción

Este proyecto cuenta con una suite completa de pruebas unitarias que valida el funcionamiento de todos los componentes principales:

- **Modelos de datos**: AudioModel, BatchModel, JobModel
- **Repositorios**: AudioRepository, BatchRepository, JobRepository
- **Integraciones**: GenesysIntegration, EmailIntegration
- **Servicios**: AudioExtractService

Todas las pruebas están aisladas y no requieren acceso a base de datos o servicios externos reales.

## 🔧 Instalación

### Paso 1: Instalar dependencias principales

```bash
pip install -r requirements.txt
```

### Paso 2: Instalar dependencias de testing

```bash
pip install -r tests/requirements-test.txt
```

### Verificar instalación

```bash
python -m pytest --version
```

Deberías ver algo como: `pytest 7.4.3`

## 🚀 Ejecución de Pruebas

### Opción 1: Usando los scripts de Windows

#### Ejecutar todas las pruebas
```bash
run_tests.bat
```

#### Ejecutar con reporte de cobertura
```bash
run_tests_with_coverage.bat
```

### Opción 2: Usando comandos directos

#### Ejecutar todas las pruebas
```bash
pytest tests/
```

#### Ejecutar con modo verbose (más detalle)
```bash
pytest tests/ -v
```

#### Ejecutar un archivo específico
```bash
pytest tests/test_audio_repository.py
```

#### Ejecutar una clase específica
```bash
pytest tests/test_audio_repository.py::TestAudioRepository
```

#### Ejecutar una prueba específica
```bash
pytest tests/test_audio_repository.py::TestAudioRepository::test_get_audio_success
```

#### Ejecutar con cobertura
```bash
pytest --cov=src --cov-report=html --cov-report=term tests/
```

#### Ejecutar en paralelo (más rápido)
```bash
pytest -n auto tests/
```

#### Ejecutar solo pruebas que fallaron la última vez
```bash
pytest --lf tests/
```

#### Ver resultados con mayor detalle
```bash
pytest tests/ -vv --tb=long
```

## 📁 Estructura de las Pruebas

```
tests/
├── __init__.py                      # Inicialización
├── conftest.py                      # Fixtures compartidos
├── test_models.py                   # Pruebas de modelos (28 pruebas)
├── test_audio_repository.py         # Pruebas de AudioRepository (6 pruebas)
├── test_batch_repository.py         # Pruebas de BatchRepository (7 pruebas)
├── test_job_repository.py           # Pruebas de JobRepository (5 pruebas)
├── test_genesys_integration.py      # Pruebas de GenesysIntegration (11 pruebas)
├── test_email_integration.py        # Pruebas de EmailIntegration (8 pruebas)
├── test_audio_extract_service.py    # Pruebas de AudioExtractService (7 pruebas)
└── requirements-test.txt            # Dependencias
```

**Total aproximado: 70+ pruebas unitarias**

## 💡 Ejemplos de Uso

### Ejemplo 1: Desarrollar una nueva funcionalidad

```bash
# 1. Escribe tu código nuevo en src/

# 2. Escribe las pruebas en tests/test_mi_modulo.py

# 3. Ejecuta solo tus nuevas pruebas
pytest tests/test_mi_modulo.py -v

# 4. Verifica la cobertura de tu código
pytest --cov=src.mi_modulo --cov-report=term-missing tests/test_mi_modulo.py
```

### Ejemplo 2: Debugging de una prueba fallida

```bash
# Ejecutar con más información
pytest tests/test_audio_repository.py -vv --tb=long

# Ver output completo (incluyendo prints)
pytest tests/test_audio_repository.py -s

# Detener en la primera falla
pytest tests/test_audio_repository.py -x
```

### Ejemplo 3: Verificar antes de hacer commit

```bash
# Ejecutar todas las pruebas rápidamente
pytest tests/ -n auto

# Si todo pasa, ejecutar con cobertura completa
pytest --cov=src --cov-report=term-missing tests/

# Verificar que la cobertura sea > 80%
```

### Ejemplo 4: Generar reporte para el equipo

```bash
# Generar reporte HTML de cobertura
pytest --cov=src --cov-report=html tests/

# El reporte estará en htmlcov/index.html
# Abrirlo en el navegador
start htmlcov/index.html
```

## 📊 Interpretación de Resultados

### Salida exitosa

```
tests/test_audio_repository.py::TestAudioRepository::test_get_audio_success PASSED [16%]
tests/test_audio_repository.py::TestAudioRepository::test_insert_audio_success PASSED [33%]
...
========================= 70 passed in 5.23s ==========================
```

✅ **Todo correcto**: Todas las pruebas pasaron

### Salida con fallas

```
tests/test_audio_repository.py::TestAudioRepository::test_get_audio_success FAILED [16%]

================================= FAILURES =================================
_______________ TestAudioRepository.test_get_audio_success ________________

    def test_get_audio_success(self):
        ...
>       assert result.id_conversation == "test-conv-123"
E       AssertionError: assert 'different-id' == 'test-conv-123'

tests/test_audio_repository.py:25: AssertionError
```

❌ **Hay problema**: La prueba falló. El ID obtenido no coincide con el esperado.

### Reporte de cobertura

```
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
src/repository/audio_repository.py        43      2    95%   45-46
src/repository/batch_repository.py        64      5    92%   78-82
src/service/audio_extract.py             145     10    93%   120-130
--------------------------------------------------------------------
TOTAL                                    1250     85    93%
```

- **Stmts**: Líneas de código
- **Miss**: Líneas no cubiertas por pruebas
- **Cover**: Porcentaje de cobertura
- **Missing**: Números de línea sin cubrir

🎯 **Objetivo**: Mantener cobertura > 80%

## ✅ Mejores Prácticas

### 1. Ejecutar pruebas frecuentemente

```bash
# Antes de cada commit
pytest tests/ -n auto

# Después de modificar un módulo
pytest tests/test_mi_modulo.py
```

### 2. Mantener alta cobertura

```bash
# Verificar qué falta cubrir
pytest --cov=src --cov-report=term-missing tests/

# Enfocarse en las líneas "Missing"
```

### 3. Escribir pruebas para bugs

Cuando encuentres un bug:

1. Escribe una prueba que reproduzca el bug
2. Verifica que la prueba falle
3. Corrige el código
4. Verifica que la prueba ahora pase

```python
def test_bug_fix_conversation_with_no_participants(self):
    """Verifica que no falle cuando una conversación no tiene participantes"""
    # Esta prueba fallaría antes del fix
    conv = Mock()
    conv.participants = None  # Bug: esto causaba error
    
    # Después del fix, debería manejarse correctamente
    result = service.process_conversation(conv)
    assert result is not None
```

### 4. Usar fixtures para evitar duplicación

```python
# Mal ❌
def test_audio_insert(self):
    audio = AudioModel(
        id_conversation="test-123",
        status="PENDING",
        creation_date=datetime.now(),
        ...
    )
    # usar audio

# Bien ✅
def test_audio_insert(self, sample_audio_model):
    # usar sample_audio_model directamente
```

### 5. Nombrar pruebas descriptivamente

```python
# Mal ❌
def test_audio(self):
    ...

# Bien ✅
def test_get_audio_returns_correct_audio_by_conversation_id(self):
    ...
```

### 6. Seguir patrón Arrange-Act-Assert

```python
def test_update_status_success(self):
    # Arrange: Preparar datos y mocks
    mock_session = MagicMock()
    repo = JobRepository()
    
    # Act: Ejecutar la función a probar
    result = repo.update_status(1, "SUCCESS")
    
    # Assert: Verificar resultados
    assert result is True
    mock_session.commit.assert_called_once()
```

## 🔍 Troubleshooting

### Problema: "No module named 'pytest'"

**Solución**:
```bash
pip install -r tests/requirements-test.txt
```

### Problema: "ImportError: cannot import name 'X' from 'src.Y'"

**Solución**: Asegúrate de ejecutar pytest desde el directorio raíz:
```bash
cd audio-extract/
pytest tests/
```

### Problema: Pruebas lentas

**Solución**: Ejecutar en paralelo:
```bash
pytest -n auto tests/
```

### Problema: Quiero ver los prints de debug

**Solución**: Usar flag -s:
```bash
pytest tests/test_mi_modulo.py -s
```

## 📚 Recursos Adicionales

- [Documentación oficial de pytest](https://docs.pytest.org/)
- [Documentación de unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Documentación de pytest-cov](https://pytest-cov.readthedocs.io/)

## 🎓 Comandos Rápidos de Referencia

```bash
# Básicos
pytest tests/                                    # Ejecutar todas
pytest tests/test_X.py                          # Ejecutar archivo
pytest tests/test_X.py::TestClass::test_method # Ejecutar método

# Con opciones útiles
pytest tests/ -v                                # Verbose
pytest tests/ -s                                # Ver prints
pytest tests/ -x                                # Detener en primera falla
pytest tests/ -n auto                           # Paralelo
pytest tests/ --lf                              # Solo las que fallaron
pytest tests/ -k "test_get"                     # Solo pruebas con "test_get"

# Cobertura
pytest --cov=src tests/                         # Cobertura básica
pytest --cov=src --cov-report=html tests/       # Reporte HTML
pytest --cov=src --cov-report=term-missing tests/ # Ver líneas faltantes

# Scripts Windows
run_tests.bat                                   # Ejecutar todas
run_tests_with_coverage.bat                     # Con cobertura
```

---

**¿Preguntas?** Consulta el archivo `tests/README.md` o la documentación de pytest.

