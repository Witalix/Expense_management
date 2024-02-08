import pytest
from django.contrib.auth.models import User
from management.models import UserProfile, Category, Expense, Budget, Income, PaymentMethod, Savings


@pytest.fixture
def user():
    user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
    return user


@pytest.fixture
def user_profile(user):
    user_profile = UserProfile.objects.create(user=user)
    return user_profile


@pytest.fixture
def category():
    category = Category.objects.create(name='Test Category', total_amount=100)
    return category


@pytest.fixture
def expense(category):
    expense = Expense.objects.create(amount=50, description='Test Expense', category=category)
    return expense


@pytest.fixture
def budget(user_profile, category):
    budget = Budget.objects.create(name='Test Budget', user=user_profile, amount=200)
    budget.categories.add(category)
    return budget


@pytest.fixture
def income(user_profile):
    income = Income.objects.create(amount=500, description='Test Income', date='2024-02-08', user=user_profile)
    return income


@pytest.fixture
def payment_method(category):
    payment_method = PaymentMethod.objects.create(name='Test Payment Method')
    payment_method.categories.add(category)
    return payment_method


@pytest.fixture
def savings(user_profile):
    savings = Savings.objects.create(goal_name='Test Savings Goal', goal_amount=1000, current_amount=500,
                                     user=user_profile)
    return savings
