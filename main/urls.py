from django.urls import path
from .views import *


urlpatterns = [
    path('sign_up/', SignUp.as_view(), name="sign_up"),
    path('sign_in/', SignIn.as_view(), name="sign_in"),
    path('currencies/', show_currencies, name="currencies"),
    path('header/', show_header, name="header")
]