from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View

from django.views import View
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib import messages

class SignupView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/home")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, "signup.html", {"form": SignupForm()})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            # login(request, user)
            messages.success(request, "Inscription réussie. Vous êtes maintenant connecté.")
            return redirect("/home")
        return render(request, "signup.html", {"form": form})

class LoginView(TemplateView):
    template_name = 'login.html'