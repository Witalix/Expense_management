from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView, UpdateView

from account.forms import LoginForm, RegisterForm, GroupPermissionAddForm


# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', 'home')
                return redirect(next)
        return render(request, 'add_form.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})


class CreateGroup(CreateView):
    model = Group
    fields = ['name']
    template_name = 'add_form.html'
    success_url = reverse_lazy('add_group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = Group.objects.all()
        context['groups'] = group
        return context


class GroupPermissionView(UpdateView):
    model = Group
    form_class = GroupPermissionAddForm
    template_name = 'add_form.html'

    def get_success_url(self):
        return reverse('group_permission', args=(self.object.id,))
