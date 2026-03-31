import requests

class DetailService:
    BASE_URL = 'http://0.0.0.0:8080'

    def get_detail_communes(self, page=1, limit=25, search=None):
        limit = min(int(limit), 100)  # Limite à 100 pour éviter les requêtes trop lourdes
        skip = (page - 1) * limit
        url = f"{self.BASE_URL}/communes/?skip={skip}&limit={limit}"
        params = {
            "skip": skip,
            "limit": limit
        }
        
        if search:
            params["search"] = search

        try:
            reponse = requests.get(url, params=params)
            if reponse.status_code == 200:
                return reponse.json()
        except Exception as e:
            print(f"Erreur lors de la récupération des détails des communes : {e}")
        return {"total": 0, "page": page, "limit": limit, "data": []}