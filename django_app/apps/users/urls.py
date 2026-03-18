from django import views
from django.urls import path
from apps.users.views import SignupView, LoginView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]