import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from management.forms import ExpenseForm
from account.forms import LoginForm, RegisterForm, GroupPermissionAddForm
from .models import Income, PaymentMethod, Expense
from mixer.backend.django import mixer


@pytest.mark.django_db
def test_budget_list_view():
    client = Client()
    url = reverse('budget_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_expense_view_get():
    client = Client()
    url = reverse('create_expense')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ExpenseForm)


@pytest.mark.django_db
def test_create_expense_view_post():
    client = Client()
    url = reverse('create_expense')
    data = {'amount': 100, 'description': 'Test expense', 'date': '2024-02-08'}
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_payment_method_list_view():
    client = Client()
    url = reverse('payment_method_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_payment_method_view_get_authenticated():
    user = User.objects.create(username='testuser')
    client = Client()
    client.force_login(user)
    url = reverse('create_payment_method')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_payment_method_view_post_authenticated():
    user = User.objects.create(username='testuser')
    client = Client()
    client.force_login(user)
    url = reverse('create_payment_method')
    data = {'name': 'Test Payment Method'}
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_list_view():
    client = Client()
    url = reverse('category_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_category_view_get():
    client = Client()
    url = reverse('category_create')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/')


@pytest.mark.django_db
def test_create_category_view_post():
    client = Client()
    url = reverse('category_create')
    data = {'name': 'Test Category'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/')


@pytest.mark.django_db
def test_login_view(client):
    url = reverse('login_view')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], LoginForm)


@pytest.mark.django_db
def test_logout_view(client, logged_in_user):
    url = reverse('logout_view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_registration_view(client):
    url = reverse('register_view')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], RegisterForm)


@pytest.mark.django_db
def test_group_permission_view(client, group):
    url = reverse('group_permission', kwargs={'pk': group.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], GroupPermissionAddForm)


@pytest.mark.django_db
def test_income_view_get(authenticated_user):
    url = reverse('income')
    response = authenticated_user.get(url)
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_income_view_post_valid_data(authenticated_user, create_payment_method):
    url = reverse('income')
    data = {
        'amount': 1000,
        'payment_method': create_payment_method.id
    }
    response = authenticated_user.post(url, data)
    assert response.status_code == 302
    assert Income.objects.filter(amount=1000).exists()


@pytest.mark.django_db
def test_income_view_total_expenses(authenticated_user, create_income, create_payment_method):
    mixer.blend(Expense, payment_method=create_payment_method, amount=500)
    url = reverse('income')
    response = authenticated_user.get(url + '?payment_method=' + str(create_payment_method.id))
    assert response.status_code == 200
    assert 'total_expenses' in response.context
