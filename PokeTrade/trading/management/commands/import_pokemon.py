from django.core.management.base import BaseCommand

from trading.models import Pokemon
from trading.utils import fetch_pokemon


class Command(BaseCommand):
    help = 'Imports multiple Pokémon into the database'

    def handle(self, *args, **kwargs):
        pokemon_names = ['pikachu', 'bulbasaur', 'charmander', 'squirtle', 'jigglypuff']  # Add more names here

        for pokemon_name in pokemon_names:
            data = fetch_pokemon(pokemon_name)
            if data:
                pokemon, created = Pokemon.objects.get_or_create(
                    name=data['name'].capitalize(),
                    number=data['id'],
                    type=', '.join([t['type']['name'].capitalize() for t in data['types']]),
                    image=data['sprites']['front_default'] if data['sprites']['front_default'] else None
                )
                if created:
                    pokemon.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully added {pokemon_name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to add {pokemon_name}'))

