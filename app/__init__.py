from urllib.parse import urljoin
import mysql.connector, json, datetime
from flask import Flask, render_template, jsonify, request
from igdb.igdbapi_pb2 import GameResult
from igdb.wrapper import IGDBWrapper


import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123412341234",
  database="gpusearch"
)

cursor = mydb.cursor()

app = Flask(__name__)

wrapper = IGDBWrapper('ed7hmod9n4zphsnxhr3n10hab2h296','97p1lbcr39cvkwswygawm9aq2fkhbm')

## CODE FOR API'S

#Get names, id's and cover urls

def get_games(name):
    byte_array = wrapper.api_request(
        'games',
        f'fields id, name, cover.url, first_release_date; search "{name}"; where version_parent = null;'
    )
    
    response_text = byte_array.decode('utf-8')  
    data = json.loads(response_text)  

    game_names = []
    game_ids = []
    cover_list = []
    release_dates = []

    previous_name = None
    for game in data:
        current_name=game['name']
        if current_name!=previous_name:
            game_names.append(current_name)
            game_ids.append(game['id'])
            cover_list.append(game.get('cover', {}).get('url', ''))
            release_date=game.get('first_release_date')
            if release_date:
                release_date = datetime.datetime.fromtimestamp(release_date).strftime("%Y-%m-%d")
                release_dates.append(release_date)
            
    return game_names, game_ids, cover_list, release_dates
    

# Get game names and ID's from searching by name

#def get_games(name):
    byte_array = wrapper.api_request(
        'games.pb',
        f'fields id, name; search "{name}"; where version_parent = null;'
    )
    games_message = GameResult()
    games_message.ParseFromString(byte_array)

    games_dict = {}
    for game in games_message.games:
        games_dict[game.id] = (game.name)

    return games_dict

#Get ID of the chosen game

# def get_game_id(name):
    byte_array = wrapper.api_request(
            'games.pb',
            f'fields id, name; search "{name}"; where version_parent = null;'
          )
    games_message = GameResult()
    games_message.ParseFromString(byte_array) 
    game_id = games_message.games[0].id
    return game_id

#Get cover URL

# def get_game_cover(game_id):
    byte_array = wrapper.api_request(
                'covers',
                f'fields url; where id = {game_id};'
            )
    json_response = json.loads(byte_array.decode())
    try:
        url = json_response[0]['url']
    except:
        url = ""
    return url

## ROUTES

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    game_names, game_ids, cover_list, release_dates = get_games(search_term)
    return render_template('list.html', game_names=game_names, game_ids=game_ids, cover_list=cover_list, release_dates=release_dates, zip=zip)
@app.route('/list')
def list():
    return render_template('list.html')