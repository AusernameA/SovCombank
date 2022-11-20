import os

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import *
from django.views.generic import CreateView
from django.urls import reverse_lazy
import json
import requests


with open("currency.json", 'r') as file:
    data = json.loads(file.read())
    currencies = json.loads(data)['currencies']

with open("price.json", 'r') as file:
    data = json.loads(file.read())
    price = json.loads(data)['quotes']


def create_menu(request):
    if request.user.is_authenticated:
        # user is authenticated
        menu = [
            {'title': "Валюта", "url_name": "currencies"},
            # {'title': "Аналитика", "url_name": "12"},
            {'title': "Личный кабинет", "url_name": "personal_account"},
            {'title': "Выход", "url_name": "logout"},

        ]
    else:
        # user is not authenticated
        menu = [
            {'title': "Вход", "url_name": "sign_in"},
            {'title': "Регистрация", "url_name": "sign_up"},

        ]
    return menu


class SignUp(CreateView):
    form_class = RegisterForm
    template_name = 'main/register_page.html'
    success_url = 'admin'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main_page')

    def get_context_data(self, **kwargs):
        menu = create_menu(self.request)
        context = {}
        context['menu'] = menu
        return context


def personal_account(request):
    menu = create_menu(request)
    context = {}
    personal_info = [
        {'title1': "Мои финансы", 'title2': "Мои паспортные данные:"},
        {'title1': "0р", 'title2': request.user.passport_ID},
        {'title1': "0$", 'title2': request.user.passport_Series},
        {'title1': "0€", 'title2': "Телефон и пароль"},
        {'title1': '', 'title2': request.user.phone},
    ]
    context['menu'] = menu
    context['personal_info'] = personal_info
    return render(request, 'main/personal_account.html', context=context)


def main_page(request):
    menu = create_menu(request)
    context = {}
    context['menu'] = menu
    return render(request, 'main/main_page.html', context=context)


class SignIn(LoginView):

    form_class = LoginForm
    template_name = 'main/login_page.html'

    def get_success_url(self):
        return reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        menu = create_menu(self.request)
        context = {}
        context['menu'] = menu
        return context


def logout_user(request):
    logout(request)
    return redirect('sign_in')


def convert(currency_from, currency_to, amount):
    url = f"https://api.apilayer.com/currency_data/live?source={currency_from}&currencies={currency_to}"
    req = requests.get(url, headers={'apikey': 'SMNjaBEc5G3jtEUVQJx2bqsWe55oeRtN'})

    answer = float(list(json.loads(req.text)['quotes'].values())[0])
    answer *= float(amount)
    return answer


def show_currencies(request):
    amount_to = None
    if request.method == "POST":
        form = ConvertForm(request.POST)
        if form.is_valid():
            currency_from = request.POST['currency_from']
            currency_to = request.POST['currency_to']
            amount_from = request.POST['amount_from']
            amount_to = convert(currency_from, currency_to, amount_from)

            init = {
                'currency_from' : currency_from,
                'currency_to' : currency_to,
                'amount_from' : amount_from,
                'amount_to' : amount_to,
            }




    menu = create_menu(request)
    context = {}
    context['menu'] = menu
    context['currencies'] = currencies
    context['price'] = price
    context['amount_to'] = amount_to
    return render(request, "main/currency_page.html", context=context)
