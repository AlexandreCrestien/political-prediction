import requests

class GeoService:
    BASE_URL = "https://geo.api.gouv.fr"

    def get_all_departments(self):
        url = f"{self.BASE_URL}/departements?fields=nom,code"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else []

    def get_department_data(self, department_code):
        """
        Récupère la chef-lieu (préfecture) et toutes les communes d'un département.
        """
        # 1. Récupérer les infos du département (pour trouver la préfecture)
        dept_url = f"{self.BASE_URL}/departements/{department_code}?fields=nom,code,chefLieu"
        dept_resp = requests.get(dept_url)
        
        # 2. Récupérer toutes les communes du département
        communes_url = f"{self.BASE_URL}/communes?codeDepartement={department_code}&fields=nom,code,centre,population"
        communes_resp = requests.get(communes_url)

        if dept_resp.status_code == 200 and communes_resp.status_code == 200:
            dept_info = dept_resp.json()
            communes = communes_resp.json()
            
            # On cherche les coordonnées de la préfecture pour centrer la carte
            # Le chefLieu est un code commune.
            center_coords = [46.2276, 2.2137]  # Par défaut : Centre de la France
            chef_lieu_code = dept_info.get('chefLieu')
            
            points = []
            for c in communes:
                if 'centre' in c:
                    # Format API : [longitude, latitude] -> Folium [latitude, longitude]
                    lat, lon = c['centre']['coordinates'][1], c['centre']['coordinates'][0]
                    points.append({'nom': c['nom'], 'lat': lat, 'lon': lon})
                    
                    if c['code'] == chef_lieu_code:
                        center_coords = [lat, lon]
            
            return {
                "center": center_coords,
                "communes": points,
                "dept_nom": dept_info.get('nom')
            }
        return None