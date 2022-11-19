from django.urls import path
from .views import SignUp, SignIn


urlpatterns = [
    path('sign_up', SignUp.as_view(), name="sign_up"),
    path('sign_in', SignIn.as_view(), name="sign_in")
]