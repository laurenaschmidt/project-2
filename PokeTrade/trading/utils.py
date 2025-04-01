import requests


def fetch_pokemon(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            'name': data['name'].capitalize(),
            'number': data['id'],
            'type': [type_info['type']['name'].capitalize() for type_info in data['types']],
            'image': data['sprites']['front_default']
        }
    else:
        return None
