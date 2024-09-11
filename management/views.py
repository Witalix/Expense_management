import csv
from io import StringIO
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db import IntegrityError

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from .models import Category, Expense, Budget, PaymentMethod, Income
from .forms import CategoryForm, ExpenseForm, BudgetForm, PaymentMethodForm, \
    PaymentMethodActionForm, IncomeForm, PaymentMethodDeleteForm


class NewHomeView(View):
    def get(self, request):

        payment_methods = PaymentMethod.objects.filter(is_active=True)
        selected_method_id = request.GET.get('method_id')

        if selected_method_id:
            selected_payment_method = get_object_or_404(
                PaymentMethod, pk=selected_method_id)
        else:
            selected_payment_method = payment_methods.first(
            ) if payment_methods.exists() else None

        expenses = Expense.objects.filter(
            payment_method=selected_payment_method) if selected_payment_method else []
        labels = [expense.category.name for expense in expenses]
        values = [float(expense.amount) for expense in expenses]

        return render(request, 'base_Static.html', {
            'labels': labels,
            'values': values,
            'payment_methods': payment_methods,
            'selected_payment_method': selected_payment_method
        })


class CreateCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'create_category.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            add_category = form.cleaned_data.get('add_category')
            if add_category:

                category, created = Category.objects.get_or_create(
                    name=add_category,
                    user=request.user
                )

                if not created and not category.is_active:
                    category.is_active = True
                    category.save()

            return redirect('category_list')

        return render(request, 'create_category.html', {'form': form})


class ExpenseEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        form = ExpenseForm(instance=expense, user=request.user)
        return render(request, 'edit_expense.html', {'form': form, 'expense': expense})

    def post(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
        return render(request, 'edit_expense.html', {'form': form, 'expense': expense})


class CreateExpenseView(LoginRequiredMixin, View):
    def get(self, request):
        form = ExpenseForm(user=request.user)
        return render(request, 'create_expense.html', {'form': form})

    def post(self, request):
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
        return render(request, 'create_expense.html', {'form': form})


class CreatePaymentMethodView(LoginRequiredMixin, View):
    def get(self, request):
        form = PaymentMethodForm()
        return render(request, 'payment_method_form.html', {'form': form})

    def post(self, request):
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            add_paymentmethod = form.cleaned_data.get('add_paymentmethod')
            if add_paymentmethod:

                payment_method, created = PaymentMethod.objects.get_or_create(
                    name=add_paymentmethod)
                if created:
                    payment_method.is_active = True
                    payment_method.save()
                else:

                    payment_method.is_active = True
                    payment_method.save()
                categories = form.cleaned_data.get('categories')
                payment_method.categories.set(categories)

            delete_paymentmethod = form.cleaned_data.get(
                'delete_paymentmethod')
            if delete_paymentmethod:
                delete_paymentmethod.is_active = False
                delete_paymentmethod.save()

        return render(request, 'payment_method_form.html', {'form': form})


class ConfirmPaymentMethodDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        payment_method = get_object_or_404(PaymentMethod, pk=pk)
        return render(request, 'confirm_payment_method_delete.html', {'payment_method': payment_method})

    def post(self, request, pk):
        payment_method = get_object_or_404(PaymentMethod, pk=pk)
        payment_method.is_active = False
        payment_method.save()
        return redirect('payment_method_list')


class ExpenseListView(LoginRequiredMixin, View):
    def get(self, request):

        sort_by = request.GET.get('sort_by', '-date')

        expenses = Expense.objects.filter(user=request.user).order_by(sort_by)

        form = ExpenseForm(user=request.user)

        return render(request, 'expense_list.html', {
            'expenses': expenses,
            'form': form,
            'sort_by': sort_by
        })

    def post(self, request):
        if 'bulk_delete' in request.POST:

            selected_expenses = request.POST.getlist('selected_expenses')
            Expense.objects.filter(
                id__in=selected_expenses, user=request.user).delete()
            return redirect('expense_list')

        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')

        expenses = Expense.objects.filter(user=request.user).order_by('-date')
        return render(request, 'expense_list.html', {'expenses': expenses, 'form': form})


class DeleteExpenseView(LoginRequiredMixin, View):
    def get(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        return render(request, 'confirm_delete_expense.html', {'expense': expense})

    def post(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return redirect('expense_list')


class PaymentMethodListView(LoginRequiredMixin, View):
    def get(self, request):
        form = PaymentMethodForm()
        payment_methods = PaymentMethod.objects.filter(is_active=True)
        return render(request, 'payment_method_list.html', {'form': form, 'payment_methods': payment_methods})

    def post(self, request):
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            add_paymentmethod = form.cleaned_data.get('add_paymentmethod')
            categories = form.cleaned_data.get('categories')
            delete_paymentmethod = form.cleaned_data.get(
                'delete_paymentmethod')

            if add_paymentmethod:
                if not PaymentMethod.objects.filter(name=add_paymentmethod, is_active=True).exists():
                    payment_method = PaymentMethod(name=add_paymentmethod)
                    payment_method.save()
                    payment_method.categories.set(categories)

            if delete_paymentmethod:

                payment_method = PaymentMethod.objects.get(
                    pk=delete_paymentmethod.pk)
                payment_method.is_active = False
                payment_method.save()

        return redirect('payment_method_list')


class CategoryListView(LoginRequiredMixin, View):
    def get(self, request):
        form = CategoryForm()

        categories = Category.objects.filter(user=request.user)
        return render(request, 'category_list.html', {'form': form, 'categories': categories})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            add_category = form.cleaned_data.get('add_category')
            if add_category:

                Category.objects.get_or_create(
                    name=add_category, user=request.user)
            return redirect('category_list')

        categories = Category.objects.filter(user=request.user)
        return render(request, 'category_list.html', {'form': form, 'categories': categories})


class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        return render(request, 'confirm_delete_category.html', {'category': category})

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect('category_list')


class IncomeView(LoginRequiredMixin, View):
    def get(self, request):
        form = IncomeForm()
        payment_methods = PaymentMethod.objects.filter(user=request.user)
        total_expenses = None

        user_income = Income.objects.filter(
            user=request.user).aggregate(Sum('amount'))['amount__sum']

        if 'payment_method' in request.GET:
            payment_method_id = request.GET['payment_method']
            payment_method = get_object_or_404(
                PaymentMethod, id=payment_method_id, user=request.user)
            total_expenses = Expense.objects.filter(
                payment_method=payment_method, user=request.user).aggregate(Sum('amount'))['amount__sum']

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
            income.user = request.user
            income.save()
            return redirect('income')

        return render(request, 'income.html', {'form': form})


class ExportExpensesView(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

        writer = csv.writer(response)
        writer.writerow(['Amount', 'Date', 'Category', 'Payment Method'])

        expenses = Expense.objects.filter(user=request.user)

        for expense in expenses:
            writer.writerow([
                expense.amount,
                expense.date,
                expense.category.name if expense.category else '',
                expense.payment_method.name if expense.payment_method else ''
            ])

        return response


class ImportExpensesView(LoginRequiredMixin, View):
    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        if not csv_file:

            return redirect('expense_list')

        data = csv_file.read().decode('utf-8')
        csv_data = StringIO(data)
        reader = csv.DictReader(csv_data)

        for row in reader:
            category_name = row.get('Category')
            payment_method_name = row.get('Payment Method')

            category = Category.objects.filter(name=category_name).first()
            if not category:
                category = Category.objects.create(
                    name=category_name,
                    user=request.user,
                    is_active=True
                )

            payment_method = PaymentMethod.objects.filter(
                name=payment_method_name).first()
            if not payment_method:
                payment_method = PaymentMethod.objects.create(
                    name=payment_method_name,
                    user=request.user,
                    is_active=True
                )

            Expense.objects.create(
                amount=row.get('Amount'),
                date=row.get('Date'),
                category=category,
                payment_method=payment_method,
                user=request.user
            )

        return redirect('expense_list')


def bulk_delete_expenses(request):
    if request.method == 'POST':

        expense_ids = request.POST.getlist('expenses')

        if expense_ids:
            Expense.objects.filter(
                id__in=expense_ids, user=request.user).delete()

        return redirect('expense_list')
