from django import forms
from .models import Category, Budget, Income, PaymentMethod, Expense



class CategoryForm(forms.Form):
    add_category = forms.CharField(
        label='Add Category', max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter category name'})
    )

    def clean_add_category(self):
        add_category = self.cleaned_data.get('add_category')
        if add_category and Category.objects.filter(name=add_category).exists():
            raise forms.ValidationError(f'Category "{add_category}" already exists.')
        return add_category




# forms.py
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'payment_method', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['date'].required = True
        self.fields['payment_method'].queryset = PaymentMethod.objects.filter(is_active=True)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)  # Tylko aktywne kategorie

        if user:
            if self.instance and self.instance.pk:
                self.instance.user = user




class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'user', 'categories', 'amount']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount']
        widgets = {
            'description': forms.TextInput(attrs={'required': False}),
            'date': forms.DateInput(attrs={'required': False}),
        }


class PaymentMethodForm(forms.Form):
    add_paymentmethod = forms.CharField(
        label='Add Payment Method', max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter payment method name'})
    )
    delete_paymentmethod = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.filter(is_active=True),
        required=False,
        empty_label='Select payment method to delete',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def clean_add_paymentmethod(self):
        add_paymentmethod = self.cleaned_data.get('add_paymentmethod')
        if add_paymentmethod and PaymentMethod.objects.filter(name=add_paymentmethod, is_active=True).exists():
            raise forms.ValidationError(f'Payment method "{add_paymentmethod}" already exists.')
        return add_paymentmethod


class PaymentMethodDeleteForm(forms.Form):
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        empty_label='Select payment method to delete',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    confirm_delete = forms.BooleanField(
        label='Confirm deletion',
        required=True
    )


class PaymentMethodActionForm(forms.Form):
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(), empty_label=None)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class PaymentMethodSelectionForm(forms.Form):
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(), label='Choose Payment Method')
