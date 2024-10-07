import requests
import json
import random

# get the all pokemons from the pokeapi website
def all_the_data():
    url = 'https://pokeapi.co/api/v2/pokemon/?offset=100&limit=100'
    pokemon_json_file = requests.get(url).json() # all the data
    pokemon_names_and_urls = pokemon_json_file["results"] # names and urls
    return pokemon_names_and_urls


def name_list(pokemon_names_and_urls):
    pokemon_name_list = []
    for pok in pokemon_names_and_urls:
        pokemon_name_list.append(pok['name'])

    return pokemon_name_list


# write the first pokemon to a new json file
def make_json_file(pokemon_names_and_urls, defult_pokemon_index=0):
    new_url = pokemon_names_and_urls[defult_pokemon_index]['url']
    data_schema = requests.get(new_url).json()
    data = {'name': data_schema['name'], 'id': data_schema['id'], 'height': data_schema['height'],
            'weight': data_schema['weight'], 'base_experience': data_schema['base_experience']}
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)

    # open the JSON file and read the data
    with open('output.json', 'r') as f:
        loaded_data = json.load(f)

    return loaded_data

def extract_data_from_json():
    # open the json file and read the data
    with open('output.json', 'r') as f:
        loaded_data = json.load(f)
    return loaded_data

def download_details(pokemon_name, pokemon_names_and_urls):
    for index, pokemon in enumerate(pokemon_names_and_urls):
        if pokemon['name'] == pokemon_name:
            return index



def update_json_file(pokemons_list):
    with open('output.json', 'w') as f:
        json.dump(pokemons_list, f, indent=4)
    return pokemons_list


def collect_pokemons():
    data_names_urls = all_the_data()  # all the data

    pokemon_name_list = name_list(data_names_urls)  # make the pokemon name list and return it
    print('\npokemon_name_list : ' + str(pokemon_name_list))

    # init the json file and the first pokemon in it in list
    pokemons_list = [make_json_file(data_names_urls)]
    print('\npokemons_list : ' + str(pokemons_list))

    valid_flag = False
    print('\nWelcome to my PokemonAPI Project!\n')
    while valid_flag == False:
        user_input = input('Do you like to draw a Pokémon? (Y or N) ').lower()

        if user_input == 'y':
            random_pokemon = random.choice(pokemon_name_list)  # random choice from the name list
            #print('\nrandom_pokemon : ' + str(random_pokemon))

            if random_pokemon in pokemons_list[0]['name']:
                show_data = extract_data_from_json()  # extract its details and present nicely to user

            else:  # random_pokemon is not in json_pokemon_file
                # Download the details, save to DB, present nicely to user
                new_index_pok = download_details(random_pokemon,data_names_urls)

                new_pokemon = make_json_file(data_names_urls, new_index_pok)
                print('\nNew Pokemon : ' + str(new_pokemon))
                pokemons_list.append(new_pokemon)  # Add the new pokemon to the list

                updated_json = update_json_file(pokemons_list)

                show_data = extract_data_from_json()  # extract its details and present nicely to user


        else:  # user_input == 'n'
            # Give a farewell greeting to the user and exit
            print('\nGoodBye!\n')
            valid_flag = True


# run the project
collect_pokemons()
