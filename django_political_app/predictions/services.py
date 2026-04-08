import requests
import os

class PredictionService:
    BASE_URL_LOCAL=os.environ.get("BASE_URL_LOCAL")

    def get_prediction_commune(self, code_insee):
        url = f"{self.BASE_URL_LOCAL}/predict/2027/{code_insee}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erreur API: {e}")
            return None
        
    def search_communes(self, query):
        # Ajout du / après communes et vérification de la construction de l'URL
        url = f"{self.BASE_URL_LOCAL}/communes/?search={query}&limit=50&light=true"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Ton service renvoie déjà le contenu de ['data']
                return response.json().get('data', [])
            return []
        except Exception as e:
            print(f"Erreur API: {e}")
            return []