"""
URL configuration for ExpanseManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from management import views

urlpatterns = [
    path('budgets/', views.BudgetListView.as_view(), name='budget_list'),
    path('create_budget/', views.CreateBudgetView.as_view(), name='create_budget'),

    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('create_expense/', views.CreateExpenseView.as_view(), name='create_expense'),


    path('incomes/', views.IncomeListView.as_view(), name='income_list'),
    path('create_income/', views.CreateIncomeView.as_view(), name='create_income'),

    path('payment_methods/', views.PaymentMethodListView.as_view(), name='payment_method_list'),
    path('create_payment_method/', views.CreatePaymentMethodView.as_view(), name='create_payment_method'),

    path('savings/', views.SavingsListView.as_view(), name='savings_list'),
    path('create_savings/', views.CreateSavingsView.as_view(), name='create_savings'),

    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('create_category/', views.CreateCategoryView.as_view(), name='category_create'),

]
