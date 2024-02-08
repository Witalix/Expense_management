import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from management.forms import ExpenseForm


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
