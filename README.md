# Smart Expense Tracker - Django Backend

A professional Django REST Framework backend for smart expense tracking with machine learning-powered insights and predictions.

## 🎯 Features

### Core Features
- ✅ **JWT Authentication** - Secure login/signup with token-based authentication
- ✅ **Expense Management** - Add, update, delete, and fetch expenses
- ✅ **Advanced Filtering** - Filter expenses by date, category, and amount
- ✅ **User Profiles** - Manage user information and preferences
- ✅ **Expense Categories** - 8 predefined categories for organized tracking

### Analytics & ML Features
- ✅ **Expense Clustering** - KMeans clustering to identify spending patterns
- ✅ **Expense Prediction** - Linear Regression for predicting next month's expenses
- ✅ **Smart Insights** - AI-powered spending analysis and suggestions
- ✅ **Spending Trends** - Daily and weekly spending trend analysis
- ✅ **Monthly Summaries** - Category-wise and overall expense summaries

## 🏗️ Project Structure

```
SmartExpenseTracker/
├── config/                          # Django project configuration
│   ├── settings.py                 # Settings with JWT, CORS, REST config
│   ├── urls.py                     # Main URL routing
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application
│
├── users/                           # User management app
│   ├── models.py                   # CustomUser model extending Django's AbstractUser
│   ├── serializers.py              # User serializers for registration/login
│   ├── views.py                    # User authentication and profile management
│   ├── urls.py                     # User endpoints routing
│   └── admin.py                    # Django admin interface
│
├── expenses/                        # Expense management app
│   ├── models.py                   # Expense model with categories
│   ├── serializers.py              # Expense serializers
│   ├── views.py                    # Expense CRUD and filtering endpoints
│   ├── urls.py                     # Expense endpoints routing
│   └── admin.py                    # Django admin interface
│
├── analytics/                       # Analytics and ML app
│   ├── models.py                   # ExpenseInsight model for storing ML results
│   ├── serializers.py              # Analytics data serializers
│   ├── views.py                    # ML prediction and insight endpoints
│   ├── urls.py                     # Analytics endpoints routing
│   └── admin.py                    # Django admin interface
│
├── ml_models/                       # Machine learning modules
│   ├── preprocessing.py            # Data preprocessing and feature engineering
│   ├── clustering.py               # KMeans clustering implementation
│   ├── prediction.py               # Linear Regression predictions
│   └── models/                     # Saved ML models (joblib)
│
├── manage.py                        # Django management command
├── requirements.txt                 # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore file
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/ananya92005/SmartExpenseTracker.git
cd SmartExpenseTracker
```

#### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set your configuration
# Important: Change SECRET_KEY to a secure value for production
```

#### 5. Apply Migrations
```bash
python manage.py migrate
```

#### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

#### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints

#### Register User
```
POST /users/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
}

Response: 201 Created
{
    "message": "User registered successfully",
    "user": {...},
    "refresh": "token...",
    "access": "token..."
}
```

#### Login User
```
POST /users/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "SecurePass123!"
}

Response: 200 OK
{
    "message": "Login successful",
    "user": {...},
    "refresh": "token...",
    "access": "token..."
}
```

#### Get JWT Token
```
POST /users/token/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "SecurePass123!"
}

Response: 200 OK
{
    "access": "token...",
    "refresh": "token..."
}
```

#### Refresh Token
```
POST /users/token/refresh/
Content-Type: application/json

{
    "refresh": "token..."
}

Response: 200 OK
{
    "access": "new_token..."
}
```

#### Get User Profile
```
GET /users/profile/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": null,
    "created_at": "2024-03-27T10:00:00Z"
}
```

### Expense Endpoints

#### Create Expense
```
POST /expenses/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "amount": 45.50,
    "category": "FOOD",
    "date": "2024-03-27",
    "description": "Lunch at restaurant"
}

Response: 201 Created
{
    "id": 1,
    "amount": "45.50",
    "category": "FOOD",
    "category_display": "Food & Dining",
    "date": "2024-03-27",
    "description": "Lunch at restaurant",
    "created_at": "2024-03-27T10:00:00Z",
    "updated_at": "2024-03-27T10:00:00Z"
}
```

#### List Expenses
```
GET /expenses/?limit=20&offset=0
Authorization: Bearer <access_token>

Query Parameters:
- category: FOOD, TRANSPORTATION, UTILITIES, ENTERTAINMENT, HEALTHCARE, EDUCATION, SHOPPING, OTHER
- date_from: YYYY-MM-DD
- date_to: YYYY-MM-DD
- ordering: date, amount, created_at (-field for descending)

Response: 200 OK
{
    "count": 50,
    "next": "http://localhost:8000/api/expenses/?offset=20",
    "previous": null,
    "results": [...]
}
```

#### Get Expense Detail
```
GET /expenses/{id}/
Authorization: Bearer <access_token>

Response: 200 OK
{...}
```

#### Update Expense
```
PUT /expenses/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "amount": 50.00,
    "category": "FOOD",
    "date": "2024-03-27",
    "description": "Updated description"
}

Response: 200 OK
{...}
```

#### Partial Update
```
PATCH /expenses/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "amount": 50.00
}

Response: 200 OK
{...}
```

#### Delete Expense
```
DELETE /expenses/{id}/
Authorization: Bearer <access_token>

Response: 204 No Content
```

#### List Categories
```
GET /expenses/categories/
Authorization: Bearer <access_token>

Response: 200 OK
[
    {"value": "FOOD", "label": "Food & Dining"},
    {"value": "TRANSPORTATION", "label": "Transportation"},
    ...
]
```

#### Expense Summary
```
GET /expenses/summary/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "total": 1234.56,
    "count": 45,
    "average": 27.43,
    "by_category": {
        "Food & Dining": 450.00,
        "Transportation": 200.00,
        ...
    }
}
```

#### Monthly Summary
```
GET /expenses/monthly-summary/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "current_month_total": 500.00,
    "monthly_data": [
        {"month": "March 2024", "total": 500.00},
        {"month": "February 2024", "total": 450.00},
        ...
    ]
}
```

#### Category-wise Summary
```
GET /expenses/category-summary/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "Food & Dining": {
        "total": 450.00,
        "count": 15,
        "average": 30.00
    },
    "Transportation": {
        "total": 200.00,
        "count": 8,
        "average": 25.00
    }
}
```

### Analytics & ML Endpoints

#### Get Expense Insights
```
GET /analytics/insights/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "total_spending": 1234.56,
    "average_expense": 27.43,
    "highest_category": "Food & Dining",
    "highest_category_amount": 450.00,
    "category_breakdown": {...},
    "suggestions": [
        "Your Food & Dining spending is significantly higher than average...",
        "Your average daily spending is $41.15..."
    ]
}
```

#### Expense Clustering
```
GET /analytics/clustering/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "clusters": [0, 1, 0, 2, 1, 0, ...],
    "silhouette_score": 0.45,
    "interpretation": "Expenses grouped into spending patterns..."
}
```

#### Expense Prediction
```
GET /analytics/prediction/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "next_month_prediction": 1200.00,
    "next_week_prediction": 300.00,
    "confidence": 0.85,
    "interpretation": "Based on historical spending patterns..."
}
```

#### Spending Trends
```
GET /analytics/spending-trends/
Authorization: Bearer <access_token>

Response: 200 OK
{
    "daily_spending": {
        "2024-03-01": 50.00,
        "2024-03-02": 75.00,
        ...
    },
    "weekly_spending": [
        {"week": "Week 1", "total": 300.00},
        {"week": "Week 2", "total": 250.00},
        ...
    ]
}
```

## 🛠️ Key Technologies

### Backend Framework
- **Django 4.2** - High-level Python web framework
- **Django REST Framework** - Toolkit for building REST APIs
- **djangorestframework-simplejwt** - JWT authentication

### Database
- **SQLite** - Default development database (use PostgreSQL for production)

### Machine Learning
- **Scikit-learn** - ML algorithms (KMeans, LinearRegression)
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### Data Storage
- **Joblib** - ML model serialization and storage

### API Features
- **Django CORS Headers** - Cross-Origin Resource Sharing
- **Django Filters** - Advanced filtering capabilities

## 🔐 Security Features

- **JWT Authentication** - Stateless token-based authentication
- **CORS Configuration** - Restricted cross-origin access
- **Password Hashing** - Django's built-in password hashing
- **Environment Variables** - Sensitive configuration via .env

## 🚀 Production Deployment

### Database Migration
Replace SQLite with PostgreSQL in production:

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'expense_tracker',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Configuration
```
SECRET_KEY=your-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Run with Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📝 Admin Interface

Access Django admin at: `http://localhost:8000/admin/`

Login with your superuser credentials to manage:
- Users
- Expenses
- Expense Insights

## 🐛 Troubleshooting

### Migration Issues
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Database Reset
```bash
# Remove db.sqlite3 and run migrations
python manage.py migrate
python manage.py createsuperuser
```

### Permission Denied
Ensure you have proper permissions and JWT token in Authorization header:
```
Authorization: Bearer your_access_token_here
```

## 📞 Support

For issues or questions, please create an issue on GitHub.

## 📄 License

This project is open source and available under the MIT License.

Run the Streamlit app and use the sidebar to navigate between features.