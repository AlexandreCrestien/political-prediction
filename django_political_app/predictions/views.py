from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class PredictionsView(LoginRequiredMixin, TemplateView):
    template_name = 'predictions.html'