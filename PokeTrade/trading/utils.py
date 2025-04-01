import requests
from .models import Pokemon

def fetch_pokemon(pokemon_name):
    try:
        return Pokemon.objects.get(name__iexact=pokemon_name)
    except Pokemon.DoesNotExist:
        pass

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        number = data['id']
        types = ', '.join([type_info['type']['name'].capitalize() for type_info in data['types']])
        image = data['sprites']['front_default']

        # Save Pokémon to the database
        pokemon = Pokemon.objects.create(
            name=name,
            number=number,
            type=types,
            image=image
        )
        return pokemon
    else:
        return None
