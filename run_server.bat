@echo off
echo ========================================================
echo   NISHI MAKEUP ARTIST & BEAUTY PARLOUR - SERVER LAUNCHER
echo ========================================================
echo.
echo Starting Django Development Server on http://127.0.0.1:8000 ...
echo.
echo Website URL:    http://127.0.0.1:8000/
echo Staff Portal:   http://127.0.0.1:8000/dashboard/
echo Django Admin:   http://127.0.0.1:8000/admin/
echo Superuser:      admin
echo Password:       admin123
echo.
echo Press Ctrl+C in this window to stop the server anytime.
echo ========================================================
echo.
if exist "%~dp0venv\Scripts\python.exe" (
    "%~dp0venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
) else (
    python manage.py runserver 127.0.0.1:8000
)
pause
