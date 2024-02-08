from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect

from django.views import View
from .models import Category, Expense, Budget, PaymentMethod
from .forms import CategoryForm, ExpenseForm, BudgetForm, PaymentMethodForm, \
    PaymentMethodActionForm


class HomeView(View):
    def get(self, request):
        return render(request, 'base.html', )


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
            # Create Expense
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
