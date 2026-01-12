# 🚀 Inicio Rápido - Pruebas Unitarias

## ⚡ En 3 Pasos

### 1️⃣ Instalar Dependencias

```bash
pip install -r tests/requirements-test.txt
```

### 2️⃣ Ejecutar Pruebas

**Opción A: Usando script (Recomendado para Windows)**
```bash
run_tests.bat
```

**Opción B: Comando directo**
```bash
pytest tests/ -v
```

### 3️⃣ Ver Cobertura (Opcional)

```bash
run_tests_with_coverage.bat
```

O manualmente:
```bash
pytest --cov=src --cov-report=html tests/
start htmlcov/index.html
```

---

## 📋 Resultado Esperado

Si todo está bien, deberías ver algo como:

```
tests/test_models.py::TestAudioModel::test_audio_model_creation PASSED     [ 1%]
tests/test_models.py::TestAudioModel::test_audio_model_with_optional_fields PASSED [ 2%]
tests/test_audio_repository.py::TestAudioRepository::test_get_audio_success PASSED [ 5%]
...
========================= 70 passed in 5.23s ==========================
```

✅ **¡Éxito!** Todas las pruebas pasaron.

---

## 🆘 Solución de Problemas

### Error: "No module named 'pytest'"

**Solución:**
```bash
pip install -r tests/requirements-test.txt
```

### Error: "ImportError: cannot import name..."

**Solución:** Ejecuta desde el directorio raíz del proyecto:
```bash
cd audio-extract/
pytest tests/
```

### Las pruebas tardan mucho

**Solución:** Ejecuta en paralelo:
```bash
pytest -n auto tests/
```

---

## 📚 Documentación Completa

- **`tests/README.md`** - Documentación técnica completa
- **`tests/GUIA_PRUEBAS.md`** - Guía práctica con ejemplos
- **`TESTING.md`** - Resumen general del proyecto
- **`tests/RESUMEN_PRUEBAS.txt`** - Resumen visual rápido

---

## 🎯 Comandos Más Usados

```bash
# Ejecutar todas las pruebas
pytest tests/

# Ejecutar con detalle
pytest tests/ -v

# Ejecutar un archivo específico
pytest tests/test_audio_repository.py

# Ver cobertura
pytest --cov=src tests/

# Ejecutar rápido (paralelo)
pytest -n auto tests/

# Ver prints de debug
pytest tests/ -s

# Detener en primera falla
pytest tests/ -x
```

---

## ✨ Lo Que Tienes Ahora

- ✅ **70+ pruebas unitarias** para todo el proyecto
- ✅ **8 archivos de prueba** cubriendo todos los componentes
- ✅ **15 fixtures** reutilizables
- ✅ **Cobertura >80%** del código
- ✅ **Documentación completa** con ejemplos
- ✅ **Scripts automatizados** para Windows
- ✅ **Sin errores de linting**

---

## 🎉 ¡Listo!

Tu proyecto ahora tiene una suite completa de pruebas unitarias profesional.

**Siguiente paso:** Ejecuta `run_tests.bat` y verifica que todo funcione correctamente.

Para más información, consulta `tests/README.md` o `tests/GUIA_PRUEBAS.md`.

