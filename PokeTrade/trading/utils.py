import requests
from .models import Pokemon


def fetch_pokemon(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            'name': data['name'],
            'id': data['id'],
            'types': data['types'],
            'sprites': data['sprites']
        }
    else:
        return None
