from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
import os

from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'apps', 'core')
# Create your views here.
class AccueilView(TemplateView):
    template_name = 'accueil/accueil.html'
