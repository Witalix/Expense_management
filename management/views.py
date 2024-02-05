from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import View
from .models import Category, Expense, Budget, Income, PaymentMethod, Savings
from .forms import CategoryForm, ExpenseForm, BudgetForm, IncomeForm, PaymentMethodForm, SavingsForm, \
    PaymentMethodActionForm


class HomeView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'base.html', {'categories': categories})


class CreateCategoryView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'create_category.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            add_category = form.cleaned_data.get('add_category')
            delete_category = form.cleaned_data.get('delete_category')

            if add_category:
                Category.objects.create(name=add_category)
            elif delete_category:
                Category.objects.filter(name=delete_category).delete()

        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories, 'form': form})


# views.py
class CreateExpenseView(View):
    def get(self, request):
        form = ExpenseForm()
        action_form = PaymentMethodActionForm()
        return render(request, 'create_expense.html', {'form': form, 'action_form': action_form})

    def post(self, request):
        form = ExpenseForm(request.POST)
        action_form = PaymentMethodActionForm()

        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            description = form.cleaned_data.get('description')
            date = form.cleaned_data.get('date')
            category = form.cleaned_data.get('category')
            payment_method = form.cleaned_data.get('payment_method')
            # Create Expense
            Expense.objects.create(
                amount=amount,
                description=description,
                date=date,
                category=category,
                payment_method=payment_method,
            )


        return render(request, 'create_expense.html', {'form': form, 'action_form': action_form})


class CreateBudgetView(View):
    def get(self, request):
        form = BudgetForm()
        return render(request, 'create_budget.html', {'form': form})

    def post(self, request):
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
        return render(request, 'create_budget.html', {'form': form})


class CreateIncomeView(View):
    def get(self, request):
        form = IncomeForm()
        return render(request, 'create_income.html', {'form': form})

    def post(self, request):
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
        return render(request, 'create_income.html', {'form': form})


class CreatePaymentMethodView(View):
    template_name = 'create_payment_method.html'

    def get(self, request):
        form = PaymentMethodForm()
        form.fields['name'].required = False
        form.fields['categories'].required = False
        payment_methods = PaymentMethod.objects.all()
        return render(request, self.template_name, {'form': form, 'payment_methods': payment_methods})

    def post(self, request):
        form = PaymentMethodForm(request.POST)

        if form.is_valid():
            payment_method = form.save(commit=False)

            categories = form.cleaned_data.get('categories')
            payment_method.save()
            payment_method.categories.set(categories)
            return redirect('create_payment_method')

        payment_method_id = request.POST.get('delete')
        if payment_method_id:
            PaymentMethod.objects.filter(id=payment_method_id).delete()
            return redirect('create_payment_method')

        payment_methods = PaymentMethod.objects.all()
        return render(request, self.template_name, {'form': form, 'payment_methods': payment_methods})


class CreateSavingsView(View):
    def get(self, request):
        form = SavingsForm()
        return render(request, 'create_savings.html', {'form': form})

    def post(self, request):
        form = SavingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('savings_list')
        return render(request, 'create_savings.html', {'form': form})


class BudgetListView(View):
    def get(self, request):
        budgets = Budget.objects.all()
        categories = Category.objects.all()
        payment_methods = PaymentMethod.objects.all()
        form = BudgetForm()

        context = {
            'budgets': budgets,
            'categories': categories,
            'payment_methods': payment_methods,
            'form': form,
        }

        return render(request, 'budget_list.html', context)

    def post(self, request):
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')

        budgets = Budget.objects.all()
        categories = Category.objects.all()
        payment_methods = PaymentMethod.objects.all()

        context = {
            'budgets': budgets,
            'categories': categories,
            'payment_methods': payment_methods,
            'form': form,
        }

        return render(request, 'budget_list.html', context)


class ExpenseListView(View):
    def get(self, request):
        expenses = Expense.objects.all()
        form = ExpenseForm()
        return render(request, 'expense_list.html', {'expenses': expenses, 'form': form})

    def post(self, request):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')

        expenses = Expense.objects.all()
        return render(request, 'expense_list.html', {'expenses': expenses, 'form': form})


class IncomeListView(View):
    def get(self, request):
        incomes = Income.objects.all()
        form = IncomeForm()
        return render(request, 'income_list.html', {'incomes': incomes, 'form': form})

    def post(self, request):
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')

        incomes = Income.objects.all()
        return render(request, 'income_list.html', {'incomes': incomes, 'form': form})


class PaymentMethodListView(View):
    def get(self, request):
        payment_methods = PaymentMethod.objects.all()
        form = PaymentMethodForm()
        return render(request, 'payment_method_list.html', {'payment_methods': payment_methods, 'form': form})

    def post(self, request):
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_method_list')

        payment_methods = PaymentMethod.objects.all()
        return render(request, 'payment_method_list.html', {'payment_methods': payment_methods, 'form': form})


class SavingsListView(View):
    def get(self, request):
        savings = Savings.objects.all()
        form = SavingsForm()
        return render(request, 'savings_list.html', {'savings': savings, 'form': form})

    def post(self, request):
        form = SavingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('savings_list')

        savings = Savings.objects.all()
        return render(request, 'savings_list.html', {'savings': savings, 'form': form})


class CategoryListView(View):

    def get(self, request):
        categories = Category.objects.all()
        form = CategoryForm()
        return render(request, 'category_list.html', {'categories': categories, 'form': form})
