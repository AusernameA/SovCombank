from django.urls import path
from .views import *


urlpatterns = [
    path('sign_up/', SignUp.as_view(), name="sign_up"),
    path('sign_in/', SignIn.as_view(), name="sign_in"),
    path('currencies/', show_currencies, name="currencies"),
    path('logout/', logout_user, name="logout"),
    path('personal_account/', personal_account, name="personal_account"),
    path('', main_page, name="main_page"),

]