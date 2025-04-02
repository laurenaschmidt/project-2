# trading/scripts.py

import requests
from models import Pokemon

def fetch_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        name = data['name']
        number = data['id']
        types = [type_info['type']['name'] for type_info in data['types']]
        type_str = ', '.join(types)
        image_url = data['sprites']['front_default']


        pokemon, created = Pokemon.objects.get_or_create(
            number=number,
            defaults={
                'name': name.capitalize(),
                'type': type_str,
                'image_url': image_url,
            }
        )

        if not created:
            pokemon.name = name.capitalize()
            pokemon.type = type_str
            pokemon.image_url = image_url
            pokemon.save()

        print(f"Pokémon {name.capitalize()} saved to the database.")
    else:
        print(f"Failed to retrieve data for Pokémon ID {pokemon_id}")
