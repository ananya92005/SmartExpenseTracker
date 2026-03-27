"""
Sample test cases for the Smart Expense Tracker API.
These can be run using: python manage.py test
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from expenses.models import Expense, ExpenseCategory
from datetime import datetime, timedelta

User = get_user_model()


class UserAuthenticationTestCase(TestCase):
    """Test cases for user authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_registration(self):
        """Test successful user registration"""
        response = self.client.post('/api/users/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_user_login(self):
        """Test successful user login"""
        # First create user
        User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        # Login
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/users/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class ExpenseTestCase(TestCase):
    """Test cases for expense management"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_expense(self):
        """Test creating an expense"""
        expense_data = {
            'amount': 50.00,
            'category': ExpenseCategory.FOOD,
            'date': datetime.now().date().isoformat(),
            'description': 'Test expense'
        }
        response = self.client.post('/api/expenses/', expense_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], '50.00')
    
    def test_get_expenses(self):
        """Test retrieving expenses"""
        # Create test expense
        Expense.objects.create(
            user=self.user,
            amount=50.00,
            category=ExpenseCategory.FOOD,
            date=datetime.now().date(),
            description='Test expense'
        )
        
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_expense_summary(self):
        """Test expense summary endpoint"""
        response = self.client.get('/api/expenses/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertIn('count', response.data)


class AnalyticsTestCase(TestCase):
    """Test cases for analytics and ML endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create sample expenses
        for i in range(10):
            Expense.objects.create(
                user=self.user,
                amount=50.00 + i * 10,
                category=ExpenseCategory.FOOD if i % 2 == 0 else ExpenseCategory.TRANSPORTATION,
                date=datetime.now().date() - timedelta(days=i),
                description=f'Test expense {i}'
            )
    
    def test_insights_endpoint(self):
        """Test insights endpoint"""
        response = self.client.get('/api/analytics/insights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_spending', response.data)
        self.assertIn('suggestions', response.data)
    
    def test_spending_trends_endpoint(self):
        """Test spending trends endpoint"""
        response = self.client.get('/api/analytics/spending-trends/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('daily_spending', response.data)
        self.assertIn('weekly_spending', response.data)
