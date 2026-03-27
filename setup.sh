#!/bin/bash
# Setup script for Smart Expense Tracker

echo "🚀 Smart Expense Tracker - Django Backend Setup"
echo "================================================"

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate  # Windows
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate  # macOS/Linux
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f ".env" ]; then
    echo "📋 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py createsuperuser

# Collect static files (optional)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo "🚀 To start the development server, run:"
echo "   python manage.py runserver"
echo ""
echo "📚 Access API at: http://localhost:8000/api/"
echo "🔧 Access admin at: http://localhost:8000/admin/"
