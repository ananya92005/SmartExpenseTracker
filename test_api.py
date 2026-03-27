"""
API Testing Script for Smart Expense Tracker
Run this script to test all API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:8000/api'

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")

# Global variables
access_token = None
user_id = None

def test_registration():
    """Test user registration"""
    print_header("Testing User Registration")
    
    global access_token, user_id
    
    data = {
        'username': f'testuser_{datetime.now().timestamp()}',
        'email': f'test_{datetime.now().timestamp()}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/users/register/', json=data)
        if response.status_code == 201:
            result = response.json()
            access_token = result['access']
            user_id = result['user']['id']
            print_success(f"User registered: {data['username']}")
            print_success(f"Access token received")
            return True
        else:
            print_error(f"Registration failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_get_profile():
    """Test getting user profile"""
    print_header("Testing Get User Profile")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/users/profile/', headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print_success(f"Profile retrieved")
            print(f"  Username: {profile['username']}")
            print(f"  Email: {profile['email']}")
            return True
        else:
            print_error(f"Failed to get profile: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_create_expense():
    """Test creating an expense"""
    print_header("Testing Create Expense")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    expenses_to_create = [
        {'amount': 45.50, 'category': 'FOOD', 'description': 'Lunch'},
        {'amount': 85.00, 'category': 'TRANSPORTATION', 'description': 'Uber ride'},
        {'amount': 120.00, 'category': 'UTILITIES', 'description': 'Electricity bill'},
    ]
    
    for expense in expenses_to_create:
        expense['date'] = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        try:
            response = requests.post(f'{BASE_URL}/expenses/', json=expense, headers=headers)
            if response.status_code == 201:
                result = response.json()
                print_success(f"Expense created: ${result['amount']} ({result['category_display']})")
            else:
                print_error(f"Failed to create expense: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")

def test_list_expenses():
    """Test listing expenses"""
    print_header("Testing List Expenses")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/expenses/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            print_success(f"Expenses retrieved: {result['count']} total")
            for expense in result['results'][:3]:
                print(f"  • ${expense['amount']} - {expense['category_display']} on {expense['date']}")
            return True
        else:
            print_error(f"Failed to list expenses: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_expense_summary():
    """Test expense summary"""
    print_header("Testing Expense Summary")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/expenses/summary/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            print_success("Expense summary retrieved")
            print(f"  Total Spending: ${result['total']}")
            print(f"  Average Expense: ${result['average']}")
            print(f"  Number of Expenses: {result['count']}")
            print("  By Category:")
            for category, amount in result['by_category'].items():
                print(f"    • {category}: ${amount}")
            return True
        else:
            print_error(f"Failed to get summary: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_monthly_summary():
    """Test monthly summary"""
    print_header("Testing Monthly Summary")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/expenses/monthly-summary/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            print_success("Monthly summary retrieved")
            print(f"  Current Month Total: ${result['current_month_total']}")
            return True
        else:
            print_error(f"Failed to get monthly summary: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_insights():
    """Test insights endpoint"""
    print_header("Testing Insights")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/analytics/insights/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            print_success("Insights retrieved")
            print(f"  Total Spending: ${result.get('total_spending', 0)}")
            print(f"  Average Expense: ${result.get('average_expense', 0)}")
            if result.get('suggestions'):
                print("  Suggestions:")
                for suggestion in result['suggestions']:
                    print(f"    • {suggestion}")
            return True
        else:
            print_info(f"Insights not available yet (need more data): {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_clustering():
    """Test clustering endpoint"""
    print_header("Testing Clustering (ML)")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/analytics/clustering/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            print_success("Clustering completed")
            print(f"  Silhouette Score: {result.get('silhouette_score', 'N/A')}")
            print(f"  Interpretation: {result.get('interpretation', 'N/A')}")
            return True
        else:
            print_info(f"Clustering not available yet (need at least 3 expenses): {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_prediction():
    """Test prediction endpoint"""
    print_header("Testing Prediction (ML)")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/analytics/prediction/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            print_success("Prediction completed")
            print(f"  Next Month Prediction: ${result.get('next_month_prediction', 'N/A')}")
            print(f"  Next Week Prediction: ${result.get('next_week_prediction', 'N/A')}")
            print(f"  Confidence: {result.get('confidence', 'N/A'):.2%}")
            print(f"  Interpretation: {result.get('interpretation', 'N/A')}")
            return True
        else:
            print_info(f"Prediction not available yet (need at least 7 expenses): {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_spending_trends():
    """Test spending trends endpoint"""
    print_header("Testing Spending Trends")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/analytics/spending-trends/', headers=headers)
        if response.status_code == 200:
            result = response.json()
            print_success("Spending trends retrieved")
            print("  Weekly Spending:")
            for week in result.get('weekly_spending', []):
                print(f"    • {week['week']}: ${week['total']}")
            return True
        else:
            print_error(f"Failed to get trends: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}Smart Expense Tracker - API Test Suite{Colors.END}")
    print(f"Base URL: {BASE_URL}\n")
    
    print_info("Make sure the Django server is running (python manage.py runserver)")
    
    # Run tests
    if not test_registration():
        print_error("Registration failed. Stopping tests.")
        return
    
    if test_get_profile():
        test_create_expense()
        test_list_expenses()
        test_expense_summary()
        test_monthly_summary()
        test_insights()
        test_clustering()
        test_prediction()
        test_spending_trends()
    
    print_header("Test Suite Complete")
    print_success("All available tests have been executed!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Testing interrupted by user{Colors.END}")
    except Exception as e:
        print_error(f"Fatal error: {str(e)}")
