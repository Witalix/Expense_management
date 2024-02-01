from django import forms
from .models import Category, Expense, Budget, Income, PaymentMethod, Savings


class CategoryForm(forms.Form):
    delete_category = forms.CharField(label='Delete Category', max_length=100, required=False)
    add_category = forms.CharField(label='Add Category', max_length=100, required=False)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date', 'user', 'category']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'user', 'categories', 'amount']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'description', 'date', 'user']


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name']


class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['goal_name', 'goal_amount', 'current_amount', 'user']
