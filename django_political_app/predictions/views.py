from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import PredictionService
# Create your views here.
class PredictionsView(LoginRequiredMixin, TemplateView):
    template_name = 'predictions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Récupération du code INSEE depuis l'URL (?code_insee=59009)
        code_insee = self.request.GET.get('code_insee', '').strip()
        
        context['search_query'] = code_insee
        context['prediction_data'] = None
        context['error'] = None

        if code_insee:
            service = PredictionService()
            api_response = service.get_prediction_commune(code_insee)
            
            if api_response and api_response.get('status') == 'success':
                context['prediction_data'] = api_response
            else:
                context['error'] = f"Aucune donnée trouvée pour le code {code_insee}."
        
        return context
    

def commune_autocomplete(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) < 1: # On a dit 1 pour plus de réactivité !
        return JsonResponse({'results': []})
    
    service = PredictionService()
    # search_communes renvoie déjà la liste 'data'
    communes = service.search_communes(query=query)
    
    results = []
    for commune in communes:
        results.append({
            'id': commune['code_insee'],
            'text': f"{commune['city']} ({commune['code_insee']})"
        })
            
    return JsonResponse({'results': results})