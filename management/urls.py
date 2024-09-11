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

    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),

    path('create_expense/', views.CreateExpenseView.as_view(), name='create_expense'),
    path('expenses/edit/<int:pk>/',
         views.ExpenseEditView.as_view(), name='edit_expense'),
    path('expenses/delete/<int:pk>/',
         views.DeleteExpenseView.as_view(), name='delete_expense'),


    path('payment_methods/', views.PaymentMethodListView.as_view(),
         name='payment_method_list'),
    path('create_payment_method/', views.CreatePaymentMethodView.as_view(),
         name='create_payment_method'),
    path('payment-methods/delete/<int:pk>/',
         views.ConfirmPaymentMethodDeleteView.as_view(), name='confirm_payment_method_delete'),

    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('create_category/', views.CreateCategoryView.as_view(),
         name='create_category'),
    path('delete_category/<int:category_id>/',
         views.DeleteCategoryView.as_view(), name='delete_category'),

    path('income/', views.IncomeView.as_view(), name='income'),



    path('export_expenses/', views.ExportExpensesView.as_view(), name='export_expenses'),
    path('import_expenses/', views.ImportExpensesView.as_view(), name='import_expenses'),
    path('bulk_delete_expenses/', views.bulk_delete_expenses, name='bulk_delete_expenses'),

]
