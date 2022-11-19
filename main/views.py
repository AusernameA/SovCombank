from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import *
from django.views.generic import CreateView
from django.urls import reverse_lazy


class SignUp(CreateView):
    form_class = RegisterForm
    template_name = 'main/sign_up.html'
    success_url = 'admin'

    def form_valid(self, form):
        user = form.save()
        return redirect('admin')


class SignIn(LoginView):
    form_class = LoginForm
    template_name = 'main/sign_in.html'

    def get_success_url(self):
        return reverse_lazy('admin')


def logout_user(request):
    logout(request)
    return redirect('login')


