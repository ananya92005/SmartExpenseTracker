# Architecture & Design Documentation

## Project Overview

Smart Expense Tracker is a Django REST Framework backend application that provides:
- User authentication with JWT
- Expense tracking and management
- Machine learning-powered analytics and predictions
- RESTful API for frontend integration

## Technical Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - REST API toolkit
- **djangorestframework-simplejwt** - JWT authentication

### Machine Learning
- **Scikit-learn** - ML algorithms
- **Pandas & NumPy** - Data processing
- **Joblib** - Model persistence

### Database
- **SQLite** - Development (development environment)
- **PostgreSQL** - Production (recommended)

### API Features
- **Django Filters** - Advanced filtering
- **Django CORS Headers** - Cross-origin support

## Architecture Design

### 1. Modular Structure

The project is organized into independent Django apps:

```
project/
├── config/          # Project settings & routing
├── users/           # Authentication & user management
├── expenses/        # Expense CRUD & summaries
├── analytics/       # ML & insights
└── ml_models/       # Machine learning algorithms
```

**Benefits:**
- Easy to maintain and scale
- Reusable components
- Clear separation of concerns
- Independent testing

### 2. Authentication Flow

```
Client -> Register/Login -> Get JWT Token -> Include in Headers -> API Calls
                                |
                          ✓ Verified --> Access Granted
                          ✗ Invalid  --> 401 Unauthorized
```

**JWT Token Structure:**
- **Header:** Algorithm (HS256)
- **Payload:** User info, token type, expiration
- **Signature:** Secure verification

### 3. Data Models

#### User Model
```python
CustomUser (extends AbstractUser)
├── username (unique)
├── email (unique)
├── password (hashed)
├── first_name
├── last_name
├── phone_number
├── created_at
└── updated_at
```

#### Expense Model
```python
Expense
├── user (FK → CustomUser)
├── amount (decimal)
├── category (choice field)
├── date
├── description
├── created_at
└── updated_at
```

#### ExpenseInsight Model
```python
ExpenseInsight
├── user (OneToOne → CustomUser)
├── clustering_data (JSON)
├── prediction_data (JSON)
├── avg_spending
├── savings_suggestion
└── last_updated
```

### 4. API Response Format

All API responses follow a consistent format:

**Success Response:**
```json
{
    "id": 1,
    "data": "...",
    "message": "Operation successful"
}
```

**Error Response:**
```json
{
    "error": "Error message",
    "status_code": 400,
    "details": {...}
}
```

### 5. Pagination

List endpoints use cursor/page-based pagination:

```
GET /api/expenses/?page=1&limit=20

Response includes:
- count: total items
- next: next page URL
- previous: previous page URL
- results: array of items
```

### 6. Filtering & Searching

Advanced filtering capabilities:

```
GET /api/expenses/?category=FOOD&date_from=2024-01-01&date_to=2024-12-31
GET /api/expenses/?search=restaurant&ordering=-date
```

## ML Pipeline

### Data Preprocessing
1. **Normalization** - Standardize features (mean-std)
2. **Feature Engineering** - Create meaningful features
3. **Data Validation** - Check minimum samples

### Clustering (KMeans)
```
Input: Expense features [amount, day_of_week, day_of_month, days_since]
↓
Preprocessing (normalization)
↓
KMeans Clustering (n_clusters=3)
↓
Output: Cluster assignments, centers, silhouette score
│
└─ Save model via Joblib
```

### Prediction (Linear Regression)
```
Input: Time-series data [days_elapsed] → amounts
↓
Preprocessing & normalization
↓
Train LinearRegression model
↓
Predict next 7 & 30 days
↓
Output: Predicted totals with confidence score
│
└─ Save model via Joblib
```

## API Endpoint Organization

### Users App
```
POST   /api/users/register/        - Register new user
POST   /api/users/login/           - Login user
POST   /api/users/token/           - Get JWT tokens
POST   /api/users/token/refresh/   - Refresh access token
GET    /api/users/profile/         - Get current user profile
PUT    /api/users/update-profile/  - Update user profile
```

### Expenses App
```
GET    /api/expenses/                    - List expenses (with filters)
POST   /api/expenses/                    - Create expense
GET    /api/expenses/{id}/               - Get expense detail
PUT    /api/expenses/{id}/               - Update expense
PATCH  /api/expenses/{id}/               - Partial update
DELETE /api/expenses/{id}/               - Delete expense
GET    /api/expenses/categories/         - List categories
GET    /api/expenses/summary/            - Overall summary
GET    /api/expenses/monthly-summary/    - Monthly summary
GET    /api/expenses/category-summary/   - Category breakdown
```

### Analytics App
```
GET    /api/analytics/insights/          - AI insights & suggestions
GET    /api/analytics/clustering/        - Expense clustering (KMeans)
GET    /api/analytics/prediction/        - Next month prediction (Linear Regression)
GET    /api/analytics/spending-trends/   - 30-day spending trends
```

## Security Features

### Authentication
- **JWT Tokens** - Stateless, secure token-based auth
- **Access Token Lifetime** - 1 hour default
- **Refresh Token** - 7 days, can be refreshed

### Authorization
- **IsAuthenticated** - Required for most endpoints
- **AllowAny** - Only for registration/login
- **User Isolation** - Users can only access their own data

### Data Protection
- **Password Hashing** - Django's PBKDF2 algorithm
- **CORS** - Restricted to allowed origins
- **HTTPS** - Recommended for production
- **Environment Variables** - Sensitive config not in code

## Performance Optimizations

### Database Queries
```python
# Efficient indexing
indexes = [
    models.Index(fields=['user', 'date']),
    models.Index(fields=['user', 'category']),
]
```

### Caching Strategy
- ML models cached after training
- User expense data filtered by user_id
- Pagination for large datasets

### Async Processing (Future)
- Use Celery for heavy ML computations
- Queue ML training jobs
- Notify users via WebSocket

## Deployment Considerations

### Development
- SQLite database
- DEBUG = True
- Runserver on 0.0.0.0:8000

### Production
- PostgreSQL database
- DEBUG = False
- Gunicorn/uWSGI servers
- Nginx reverse proxy
- HTTPS/SSL certificate
- Environment variables from secrets

### Scaling
- Horizontal scaling with load balancers
- Database replication
- Cache layer (Redis)
- Async task queue (Celery)

## Future Enhancements

1. **Real-time Notifications** - WebSocket for alerts
2. **Advanced ML** - Time series forecasting (LSTM, ARIMA)
3. **Budget Management** - Set and track budgets
4. **Expense Sharing** - Multi-user expense tracking
5. **Mobile App** - React Native or Flutter
6. **OCR Integration** - Receipt image parsing
7. **Bank Integration** - Automatic transaction import
8. **Export Features** - PDF, CSV reports

## Testing Strategy

### Unit Tests
- Model tests
- Serializer tests
- View tests

### Integration Tests
- API endpoint tests
- Database transaction tests
- Authentication flow tests

### ML Tests
- Data preprocessing tests
- Model accuracy tests
- Prediction tests

## Development Workflow

1. **Create branch** from main
2. **Make changes** in feature branch
3. **Write tests** for new functionality
4. **Run tests** - `python manage.py test`
5. **Create PR** with description
6. **Code review** & approval
7. **Merge** to main
8. **Deploy** to production
