import os

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import *
from django.views.generic import CreateView
from django.urls import reverse_lazy
import json


with open("currency.json", 'r') as file:
    data = json.loads(file.read())
    currencies = json.loads(data)['currencies']


class SignUp(CreateView):
    form_class = RegisterForm
    template_name = 'main/register_page.html'
    success_url = 'admin'

    def form_valid(self, form):
        user = form.save()
        return redirect('admin')


def show_header(request):
    if request.user.is_authenticated:
        menu = [
            {'title': "Котировки", "url_name": "12"},
            {'title': "Ваш Номер телефона", "url_name": "12"},
            {'title': "Выход", "url_name": "12"},

        ]
    else:
        menu = [
            {'title': "Вход", "url_name": "12"},
            {'title': "Регистрация", "url_name": "12"},

        ]
    context = {}
    context['menu'] = menu
    return render(request, 'main/base_header.html', context=context)


class SignIn(LoginView):
    form_class = LoginForm
    template_name = 'main/login_page.html'

    def get_success_url(self):
        return reverse_lazy('admin')


def logout_user(request):
    logout(request)
    return redirect('login')


def show_currencies(request):
    if request.user.is_authenticated:
        menu = [
            {'title': "Котировки", "url_name": "12"},
            {'title': "Ваш Номер телефона", "url_name": "12"},
            {'title': "Выход", "url_name": "12"},

        ]
    else:
        menu = [
            {'title': "Вход", "url_name": "12"},
            {'title': "Регистрация", "url_name": "12"},

        ]
    context = {}
    context['menu'] = menu
    context['currencies'] = currencies
    return render(request, "main/currency_page.html", context=context)
    # return render(requests, "main/show_currencies.html", context={"cur": currencies})
