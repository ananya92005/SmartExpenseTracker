# Installation & Setup Guide

## Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **Virtual Environment** - Recommended for isolated dependencies
- **Git** - For cloning the repository (optional)

## Windows Installation

### Step 1: Clone and Navigate to Project
```bash
git clone https://github.com/ananya92005/SmartExpenseTracker.git
cd SmartExpenseTracker
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```bash
# Copy example env file
copy .env.example .env

# Edit .env file with your settings (optional for development)
# Important: Keep DEBUG=True for development, change to False for production
```

### Step 5: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
# Example: username=admin, email=admin@example.com, password=Admin123!
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The server will start at: `http://localhost:8000/`

### Step 8: Access the Application
- **API Root**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **API Documentation**: See README.md

---

## macOS/Linux Installation

### Step 1: Clone and Navigate to Project
```bash
git clone https://github.com/ananya92005/SmartExpenseTracker.git
cd SmartExpenseTracker
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env file if needed
nano .env
```

### Step 5: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The server will start at: `http://localhost:8000/`

---

## Automated Setup (Windows)

If you prefer automated setup on Windows, run:

```bash
setup.bat
```

This script will:
- Create virtual environment
- Install dependencies
- Copy .env file
- Run migrations
- Create superuser

---

## Docker Setup

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Steps

1. **Build and start services:**
```bash
docker-compose up -d
```

2. **Run migrations:**
```bash
docker-compose exec web python manage.py migrate
```

3. **Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

4. **Access the application:**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

5. **Stop services:**
```bash
docker-compose down
```

---

## Post-Installation Setup

### 1. Create Test Data

Option A: Using the API test script
```bash
python test_api.py
```

Option B: Manually via API
```bash
# Register a user
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Access Admin Panel

1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Manage users, expenses, and insights

---

## Common Commands

### Run Server
```bash
python manage.py runserver
```

### Run Migrations
```bash
python manage.py migrate
python manage.py makemigrations
```

### Create Migrations After Model Changes
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Shell (Test queries)
```bash
python manage.py shell

# Example in shell:
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> users = User.objects.all()
>>> print(users)
```

### Run Tests
```bash
python manage.py test
python manage.py test -v 2  # Verbose output
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Reset Database
```bash
# Delete database (WARNING: This deletes all data)
rm db.sqlite3  # Unix/Mac
del db.sqlite3  # Windows

# Run migrations again
python manage.py migrate
python manage.py createsuperuser
```

---

## Troubleshooting

### Module Not Found Errors
**Problem:** `ModuleNotFoundError: No module named 'rest_framework'`

**Solution:**
```bash
# Make sure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

### Database Migration Errors
**Problem:** `ProgrammingError: table "users_customuser" does not exist`

**Solution:**
```bash
python manage.py migrate --run-syncdb
python manage.py migrate
```

### Port Already in Use
**Problem:** `Address already in use (0.0.0.0:8000)`

**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill process using port 8000
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### JWT Token Issues
**Problem:** `Authentication Failed` or `Invalid Token`

**Solution:**
- Ensure token is in Authorization header: `Authorization: Bearer <token>`
- Check token hasn't expired (1 hour default)
- Refresh token if expired: `POST /api/users/token/refresh/`

### Static Files Not Loading
**Problem:** Admin panel looks broken, CSS not loading

**Solution:**
```bash
python manage.py collectstatic --noinput
```

---

## Environment Variables Reference

```env
# Django
SECRET_KEY=your-super-secret-key
DEBUG=True (False for production)
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (development)
DATABASE_URL=sqlite:///db.sqlite3

# Database (production PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT Tokens (in seconds)
ACCESS_TOKEN_LIFETIME=3600 (1 hour)
REFRESH_TOKEN_LIFETIME=604800 (7 days)

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Next Steps

1. **Read API Documentation** - See [README.md](README.md) for complete API endpoints
2. **Test the API** - Run `python test_api.py` to test all endpoints
3. **Create Frontend** - Build a React/Vue/Angular frontend to consume the API
4. **Setup Database** - Switch from SQLite to PostgreSQL for production
5. **Deploy** - Deploy to production using Gunicorn, uWSGI, or cloud platforms

---

## Support & Resources

- **Django Documentation:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **Scikit-learn:** https://scikit-learn.org/
- **GitHub Issues:** https://github.com/ananya92005/SmartExpenseTracker/issues
