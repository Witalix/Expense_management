from django import forms
from .models import Category, Expense, Budget, Income, PaymentMethod, Savings


class CategoryForm(forms.Form):
    delete_category = forms.CharField(label='Delete Category', max_length=100, required=False)
    add_category = forms.CharField(label='Add Category', max_length=100, required=False)


class ExpenseForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.all())


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
        fields = ['name', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Payment Method Name'}),
            'categories': forms.CheckboxSelectMultiple()
        }
        required = {
            'name': False,
            'categories': False,
        }


class PaymentMethodActionForm(forms.Form):
    payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), empty_label=None)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['goal_name', 'goal_amount', 'current_amount', 'user']
