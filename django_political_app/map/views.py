# views.py
import folium
import pandas as pd
from django.views.generic import TemplateView
from django.core.cache import cache
from folium.plugins import FastMarkerCluster

class MapView(TemplateView):
    template_name = 'map.html'

    def get_coords_df(self):
        """Charge le CSV en cache pour éviter le re-téléchargement à chaque requête."""
        df = cache.get('communes_coords')
        if df is None:
            url_coords = "https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"
            df = pd.read_csv(url_coords, sep=',', dtype=str,
                             usecols=['code_commune_INSEE', 'nom_commune_postal', 'latitude', 'longitude'])
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            df = df.dropna(subset=['latitude', 'longitude'])
            cache.set('communes_coords', df, timeout=60 * 60 * 24)  # Cache 24h
        return df

    def get_context_data(self, **kwargs):
        df = self.get_coords_df()

        m = folium.Map(location=[46.232193, 2.209667], zoom_start=6, tiles='cartodbpositron')

        # FastMarkerCluster : passe toutes les coords en une seule fois (JS natif, très rapide)
        callback = """
            function(row) {
                var marker = L.circleMarker(
                    new L.LatLng(row[0], row[1]),
                    {radius: 4, color: 'red', fillColor: 'red', fillOpacity: 0.8, weight: 0}
                );
                marker.bindTooltip(row[2] + ' : ' + row[3]);
                return marker;
            }
        """
        data = df[['latitude', 'longitude', 'nom_commune_postal', 'code_commune_INSEE']].values.tolist()
        FastMarkerCluster(data=data, callback=callback).add_to(m)

        return {"map": m._repr_html_()}