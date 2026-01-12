@echo off
REM Script para ejecutar pruebas unitarias en Windows

echo ========================================
echo Ejecutando pruebas unitarias
echo ========================================
echo.

REM Verificar si pytest está instalado
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pytest no está instalado
    echo Instalando dependencias de prueba...
    pip install -r tests\requirements-test.txt
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias
        exit /b 1
    )
)

echo.
echo Ejecutando todas las pruebas...
echo.

python -m pytest tests\ -v

echo.
echo ========================================
echo Pruebas completadas
echo ========================================
echo.
echo Para ver la cobertura de código, ejecuta:
echo python -m pytest --cov=src --cov-report=html tests\
echo.

pause

