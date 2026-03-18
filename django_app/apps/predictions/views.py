from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View

# Create your views here.
class PredictionsView(TemplateView):
    template_name = 'predictions.html'