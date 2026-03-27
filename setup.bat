@echo off
REM Setup script for Smart Expense Tracker on Windows

echo.
echo 🚀 Smart Expense Tracker - Django Backend Setup
echo ================================================
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Copy environment file
if not exist ".env" (
    echo 📋 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your configuration
)

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py migrate

REM Create superuser
echo 👤 Creating superuser...
python manage.py createsuperuser

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To start the development server, run:
echo    python manage.py runserver
echo.
echo 📚 Access API at: http://localhost:8000/api/
echo 🔧 Access admin at: http://localhost:8000/admin/
echo.
pause
