from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from .models import Category, Expense, Budget, PaymentMethod, Income
from .forms import CategoryForm, ExpenseForm, BudgetForm, PaymentMethodForm, \
    PaymentMethodActionForm, IncomeForm


class NewHomeView(View):
    def get(self, request):
        payment_methods = PaymentMethod.objects.all()
        selected_method_id = request.GET.get('method_id')

        if selected_method_id:
            selected_payment_method = PaymentMethod.objects.get(pk=selected_method_id)
        else:
            selected_payment_method = payment_methods.first()

        expenses = Expense.objects.filter(payment_method=selected_payment_method)
        labels = [expense.category.name for expense in expenses]
        values = [float(expense.amount) for expense in expenses]

        return render(request, 'base_Static.html',
                      {'labels': labels, 'values': values, 'payment_methods': payment_methods,
                       'selected_payment_method': selected_payment_method})


class CreateCategoryView(LoginRequiredMixin, View):
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
            Expense.objects.create(
                amount=amount,
                description=description,
                date=date,
                category=category,
                payment_method=payment_method,
            )

        return render(request, 'create_expense.html', {'form': form, 'action_form': action_form})


class CreatePaymentMethodView(LoginRequiredMixin, View):
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
            payment_method_name = form.cleaned_data['name']
            categories = form.cleaned_data.get('categories')

            existing_payment_method = PaymentMethod.objects.filter(name=payment_method_name).first()

            if existing_payment_method:
                existing_payment_method.categories.add(*categories)
            else:
                payment_method = form.save(commit=False)
                payment_method.save()
                payment_method.categories.set(categories)

            return redirect('create_payment_method')

        payment_methods = PaymentMethod.objects.all()
        return render(request, self.template_name, {'form': form, 'payment_methods': payment_methods})


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


class CategoryListView(View):

    def get(self, request):
        categories = Category.objects.all()
        form = CategoryForm()
        return render(request, 'category_list.html', {'categories': categories, 'form': form})


class IncomeView(View):
    def get(self, request):
        form = IncomeForm()
        payment_methods = PaymentMethod.objects.all()
        total_expenses = None

        user_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum']

        if 'payment_method' in request.GET:
            payment_method_id = request.GET['payment_method']
            payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
            total_expenses = Expense.objects.filter(payment_method=payment_method).aggregate(Sum('amount'))[
                'amount__sum']

        remaining_amount = None
        if user_income is not None and total_expenses is not None:
            remaining_amount = user_income - total_expenses

        return render(request, 'income.html', {
            'form': form,
            'payment_methods': payment_methods,
            'total_expenses': total_expenses,
            'user_income': user_income,
            'remaining_amount': remaining_amount
        })

    def post(self, request):
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            user = request.user
            income.user = user
            income.save()
            return redirect('income')

        return render(request, 'income.html', {'form': form})