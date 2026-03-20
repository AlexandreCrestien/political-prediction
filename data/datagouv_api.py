import requests, json
from pathlib import Path


def process_api_request(url):
	try:
		response = requests.get(url)
		response.raise_for_status()
		return response.json()
	except requests.exceptions.HTTPError as http_err:
		print(f"Erreur HTTP détectée : {http_err}")
	except Exception as e:
		print(f"Error: {str(e)}")
		return None


def get_json_data(filepath, url):

	if Path(filepath).exists():
		print('Le dataset existe déjà')
	else:
		data = process_api_request(url)

		if data:
			with open(filepath, "w") as file:
				json.dump(data, file)
			return True


url = "https://tabular-api.data.gouv.fr/api/resources/79b5cac4-4957-486b-bbda-322d80868224/data/"

filepath = 'data/src/src_datagouv/election_2022.json'


get_json_data(filepath, url)