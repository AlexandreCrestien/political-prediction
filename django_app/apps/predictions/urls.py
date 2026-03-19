from django.urls import path
from .views import PredictionsView

urlpatterns = [
    path('predictions/', PredictionsView.as_view(), name='predictions'),
]