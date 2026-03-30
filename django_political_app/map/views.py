import folium
from django.views.generic import TemplateView
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import GeoService

class MapView(LoginRequiredMixin, TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = GeoService()

        # 1. On cache la liste des départements (ça ne change presque jamais)
        departments = cache.get('all_departments')
        if not departments:
            departments = service.get_all_departments()
            cache.set('all_departments', departments, timeout=60 * 60 * 24)

        # 2. Récupération du code sélectionné
        dept_code = self.request.GET.get('department', '75')
        
        # 3. On cache les données du département pour éviter les appels API inutiles
        cache_key = f'dept_data_{dept_code}'
        data = cache.get(cache_key)
        if not data:
            data = service.get_department_data(dept_code)
            cache.set(cache_key, data, timeout=60 * 60 * 2) # Cache 2h

        if data:
            # Création de la carte
            m = folium.Map(
                location=data['center'], 
                zoom_start=9,
                tiles="cartodbpositron"
            )

            # --- LE POINT FAÇON GOOGLE MAPS (Pour la préfecture) ---
            folium.Marker(
                location=data['center'],
                popup=f"Préfecture : {data['dept_nom']}",
                tooltip="Cliquez pour voir",
                icon=folium.Icon(color="red", icon="info-sign") # "Pin" classique
            ).add_to(m)

            # --- LES AUTRES COMMUNES ---
            for commune in data['communes']:
                # On évite de doubler le point si c'est la préfecture
                if commune['nom'] != data['dept_nom']:
                    folium.CircleMarker(
                        location=[commune['lat'], commune['lon']],
                        radius=4,
                        popup=commune['nom'],
                        color="#3273dc",
                        fill=True,
                        fill_opacity=0.6,
                        weight=1
                    ).add_to(m)

            context['map'] = m._repr_html_()
            context['dept_nom'] = data['dept_nom']
            context['current_dept'] = dept_code
            context['departments'] = departments
        
        return context