from django.urls import path
from .views import AccueilView

urlpatterns = [
    path('accueil/', AccueilView.as_view(), name='accueil'),
]