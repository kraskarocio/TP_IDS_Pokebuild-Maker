from flask import Blueprint, render_template, request, session
from datetime import timedelta
import requests

frontend_blueprint = Blueprint('frontend', __name__)
frontend_blueprint.secret_key = 'Si'
frontend_blueprint.permanent_session_lifetime = timedelta(days=7)

def fetch_data():
    builds = requests.get('http://pokebuild-backend:5000/api/builds/').json()
    pokemons = requests.get('http://pokebuild-backend:5000/api/pokemons/').json()
    return builds, pokemons

def get_pokemon_id(build):
    return [
        build.get(f'pokemon_id_{j+1}', -1) if build.get(f'pokemon_id_{j+1}') is not None else -1
        for j in range(6)
    ]

def get_pokedex_id(pokemon_list, pokemons):
    result = []
    for pokemon_id in pokemon_list:
        if pokemon_id == -1 or pokemon_id - 1 >= len(pokemons):
            result.append('000')
        else:
            result.append(str(pokemons[pokemon_id - 1]['pokedex_id']).zfill(3))
    return result

def get_build_dict(builds, pokemons):
    build_dict = {}
    for build in builds:
        result = get_pokedex_id(get_pokemon_id(build), pokemons)
        build_row = {
            'owner_id': build['owner_id'],
            'build_name': build['build_name'],
            'timestamp': build['timestamp']
        }

        for j in range(6):
            build_row[f'pokemon_id_{j+1}'] = result[j]
        build_dict[build['id']] = build_row

    return build_dict


def get_info_pokemons(pokemons): #pokemons es un json
    info_dic = {}
    i = 0 #debe tener abilidades, lvl, name -- claves('ability_1', 'ability_2', 'ability_3', 'ability_4', 'level', 'name')
    for pokemon in pokemons: #cada pokemon representa un diccionario
        info = {
            'ability_1' : pokemon['ability_1'],
            'ability_2' : pokemon['ability_2'],
            'ability_3' : pokemon['ability_3'],
            'ability_4' : pokemon['ability_4'],
            'id' : pokemon['id'],
            'level' : pokemon['level'],
            'name' : pokemon['name']
            }
        info_dic[i] = info
        i=i+1 
    return info_dic


def get_pokemon_name_by_id(pokedex_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokedex_id}')
    if response.status_code == 200:
        pokemon_data = response.json()  # Aquí se corrige el uso de json()
        return pokemon_data['name']
    else:
        return None


def get_user_pokemons(user_id):
    user_pokemons=requests.get(f'http://pokebuild-backend:5000/api/pokemons_by_user/{user_id}').json()
    pokemons_dict = []
    for pokemon in user_pokemons:
        especie_pokemon= get_pokemon_name_by_id(pokemon['pokedex_id'])
        build_row = {
            'name': pokemon['name'],
            'especie': especie_pokemon,
            'level': pokemon['level'],
            'ability_1': pokemon['ability_1'],
            'ability_2': pokemon['ability_2'],
            'ability_3': pokemon['ability_3'],
            'ability_4':pokemon['ability_4']
        }
        pokemons_dict.append(build_row)
    return pokemons_dict


@frontend_blueprint.route('/')
@frontend_blueprint.route('/home')
@frontend_blueprint.route('/home/')
def index():
    builds, pokemons = fetch_data()
    build_dict = get_build_dict(builds, pokemons)
    return render_template('home.html', build_dict=build_dict)


@frontend_blueprint.route('/pop-up-test')
def pop_up_test():
    return render_template('pop-up-test.html')

@frontend_blueprint.route('/build_list_container')
def build_list_container():
    return render_template("build_list_container.html")

@frontend_blueprint.route('/login_register')
def login_register():
    return render_template('login_register.html')

@frontend_blueprint.route('/add_pokemon_form', methods=["POST", "GET"]) #Hasta que este el POST endpoint de pokemon, tiene esto.
def add_pokemon_form():
    pokemons = requests.get("http://localhost:5000/api/get_all_pokemons").json()
    if request.method == "POST":
        return render_template("home.html")
    return render_template('add_pokemon_form.html', pokemons=pokemons['pokemons'])

@frontend_blueprint.route('/pokemon_container/')
def pokemon_container():
    # user_id = 9 #quitar para despues
    # pokemons = requests.get(f'http://pokebuild-backend:5000/api/pokemons_by_user/{user_id}').json()
    # asd = get_info_pokemons(pokemons)
    # print(asd)
    return render_template('pokemon_container.html') #, pokemons=asd
    #pokemons_dic = get_user_pokemons(user_id)
    #print(pokemons_dic)
    #return render_template('pokemon_container.html', pokemons=pokemons_dic)