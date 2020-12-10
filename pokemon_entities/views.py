import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def map_pokemon_for_view(pokemon, entities):
    pokemon_dict = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': pokemon.image.url,
        'description': pokemon.description,
        'entities': []
    }

    for entity in entities:
        pokemon_dict['entities'].append({
            'level': pokemon.level,
            'lat': entity.lat,
            'lon': entity.lon
        })

    return pokemon_dict


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = pokemon.get_entities()
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                pokemon.title, request.build_absolute_uri(pokemon.image.url))

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)

    if pokemon is None:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entity = pokemon.get_entities()

    for entity in pokemon_entity:
        add_pokemon(folium_map, entity.lat, entity.lon, pokemon.title,
                    request.build_absolute_uri(pokemon.image.url))

    pokemon_dict = map_pokemon_for_view(pokemon, pokemon_entity)

    if pokemon.previous_evolution is not None:
        previous_evolution = pokemon.previous_evolution
        pokemon_dict['previous_evolution'] = {
            "title_ru": previous_evolution.title,
            "pokemon_id": previous_evolution.id,
            "img_url": previous_evolution.image.url
        }

    pokemon_next_evolution = pokemon.next_evolution.all().first()

    if pokemon_next_evolution is not None:
        pokemon_dict['next_evolution'] = {
            "title_ru": pokemon_next_evolution.title,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": pokemon_next_evolution.image.url
        }

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_dict})
