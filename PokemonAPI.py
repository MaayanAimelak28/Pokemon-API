import requests
import json
import random
import webbrowser # to open the HTML file


# get a list of all pokemons from the PokeAPI website.
def all_the_data():
    url = 'https://pokeapi.co/api/v2/pokemon/?offset=100&limit=100'
    pokemon_json_file = requests.get(url).json() # get all the data
    pokemon_names_and_urls = pokemon_json_file["results"] # extract names and urls
    return pokemon_names_and_urls

# return a list of pokemon names from the provided names and urls.
def name_list(pokemon_names_and_urls):
    pokemon_name_list = []
    for pok in pokemon_names_and_urls:
        pokemon_name_list.append(pok['name'])
    return pokemon_name_list


# create a JSON file containing details of a specific pokemon and return its data
def make_json_file(pokemon_names_and_urls, defult_pokemon_index=0):
    new_url = pokemon_names_and_urls[defult_pokemon_index]['url']
    data_schema = requests.get(new_url).json()
    data = {'name': data_schema['name'], 'id': data_schema['id'], 'height': data_schema['height'],
            'weight': data_schema['weight'], 'base_experience': data_schema['base_experience']}
    # open the JSON file and write the pokemon data as a list
    with open('output.json', 'w') as f:
        json.dump([data], f, indent=4)  # write a list with one pokemon

    return data

# extract the data from the JSON file and return it
def extract_data_from_json():
    # open the JSON file and read the data
    with open('output.json', 'r') as f:
        loaded_data = json.load(f)
    return loaded_data

# return the index of a new pokemon in the list of names and urls
def download_details(pokemon_name, pokemon_names_and_urls):
    for index, pokemon in enumerate(pokemon_names_and_urls):
        if pokemon['name'] == pokemon_name:
            return index


# update the JSON file with the new list of pokemons
def update_json_file(pokemons_list):
    with open('output.json', 'w') as f:
        json.dump(pokemons_list, f, indent=4)
    return pokemons_list


# generate HTML file to display the pokemons
def generate_html():
    pokemons = extract_data_from_json()  # load the pokemons data from JSON file
    # the HTML content
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokémon List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 20px;
            text-align: center; 
        }
        h1 {
            color: #1E90FF;
        }
        .pokemon {
            border: 1px solid #ccc;
            padding: 10px;
            margin: 10px auto; 
            background-color: #fff;
            display: inline-block; 
            align-items: center;
        }
        .pokemon img {
            margin-right: 20px;
        }
    </style>
</head>
<body>
    <h1>Pokémon List</h1>
    """

    # add each pokemon to the HTML content
    for pokemon in pokemons:
        pokemon_id = pokemon['id']  # get the pokemon id
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"  # image URL
        html_content += f"""
        <div class="pokemon">
            <img src="{image_url}" alt="{pokemon['name']}" />
            <div>
                <h2>{pokemon['name'].capitalize()}</h2>
                <p>ID: {pokemon['id']}</p>
                <p>Height: {pokemon['height']}</p>
                <p>Weight: {pokemon['weight']}</p>
                <p>Base Experience: {pokemon['base_experience']}</p>
            </div>
        </div>
        """

    # close the HTML content
    html_content += """
    </body>
    </html>
    """

    # write the HTML content to a file
    with open('pokemon_API.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    webbrowser.open(r'C:\Users\maaya\Downloads\AWS\python\PokemonAPI\pokemon_API.html')


# Main function: prompt the user to draw a pokemon. If yes, randomly choose a pokemon.
# if the chosen pokemon is in the existing list, retrieve its attributes,
# otherwise, fetch the pokemon's details from the API and update the list.
def collect_pokemons():
    data_names_urls = all_the_data()  # retrieve all the data
    pokemon_name_list = name_list(data_names_urls) # create the pokemon name list and return it

    # initialize the JSON file and add the first pokemon to the list.
    make_json_file(data_names_urls)

    valid_flag = False
    print('\nWelcome to my PokemonAPI Project!\n')
    while valid_flag == False:
        user_input = input('Do you like to draw a Pokémon? (Y or N) ').lower()

        if user_input == 'y':
            random_pokemon = random.choice(pokemon_name_list)  # randomly choose a pokemon

            # check if the random_pokemon is already in output.json
            current_pokemons = extract_data_from_json()  # get the current list of pokemons
            # create a list of existing pokemon names from the current pokemon data
            existing_names = []
            for pokemon in current_pokemons:
                existing_names.append(pokemon['name'])
            # check if the randomly selected pokemon is already in the existing names list
            if random_pokemon in existing_names:
                show_data = extract_data_from_json()  # extract details for the existing pokemon
                print('\nThis Pokemon in our names list: ' + str(random_pokemon))
            else:  # random_pokemon is not in JSON
                new_index_pok = download_details(random_pokemon, data_names_urls) # get index for the new pokemon
                new_pokemon = make_json_file(data_names_urls, new_index_pok) # create JSON for the new pokemon
                print('\nNew Pokemon: ' + str(new_pokemon))

                # update the existing list and write to output.json
                current_pokemons.append(new_pokemon)  # add the new pokemon to the list
                updated_json = update_json_file(current_pokemons)  # update the JSON file
                show_data = extract_data_from_json()  # get updated details

        else:  # user_input equal to any input
            # give a farewell greeting to the user and exit
            print('\nGoodBye!\n')
            valid_flag = True



# run the project
collect_pokemons()
# generate the HTML file
generate_html()

