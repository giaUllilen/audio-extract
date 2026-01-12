@echo off
REM Script para ejecutar pruebas con reporte de cobertura

echo ========================================
echo Ejecutando pruebas con cobertura
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
echo Ejecutando pruebas con cobertura...
echo.

python -m pytest --cov=src --cov-report=html --cov-report=term-missing tests\

if errorlevel 1 (
    echo.
    echo [ERROR] Algunas pruebas fallaron
    echo.
) else (
    echo.
    echo ========================================
    echo Pruebas completadas exitosamente
    echo ========================================
    echo.
    echo Reporte HTML generado en: htmlcov\index.html
    echo.
    
    REM Preguntar si desea abrir el reporte
    set /p OPEN_REPORT="¿Deseas abrir el reporte de cobertura? (S/N): "
    if /i "%OPEN_REPORT%"=="S" (
        start htmlcov\index.html
    )
)

echo.
pause

