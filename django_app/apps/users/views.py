from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View

class SignupView(TemplateView):
    template_name = 'signup.html'

class LoginView(TemplateView):
    template_name = 'login.html'