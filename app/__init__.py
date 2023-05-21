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
                release_date_year = release_date[0:4]
                release_dates.append(release_date_year)
            
    return game_names, game_ids, cover_list, release_dates

def get_games_full(id):
    byte_array = wrapper.api_request(
        'games',
        f'fields name, cover.url, first_release_date, rating, summary; where id = {id};'
    )

    response_text = byte_array.decode('utf-8')
    data = json.loads(response_text)

    game = data[0]  # Assuming there is only one game in the data

    game_name = game['name']
    game_id = game['id']
    cover_url = game['cover'].get('url', '')
    try:
        rating = round(game['rating'])
    except:
        rating = 'Unrated';
    summary = game['summary']
    first_release_date=game['first_release_date']
    if first_release_date:
        first_release_date = datetime.datetime.fromtimestamp(first_release_date).strftime("%Y-%m-%d")
        release_date_year = first_release_date[0:4]

    return game_name, game_id, cover_url, rating, summary, release_date_year

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
@app.route('/find_gpu', methods=['POST'])
def find_gpu():
    id = request.form.get('game_id')
    game_name, game_id, cover_url, rating, summary, release_date_year = get_games_full(id)
    return render_template('index.html', game_name=game_name, game_id=game_id, cover_url=cover_url, rating=rating, summary=summary, release_date_year=release_date_year, zip=zip)
@app.route('/list')
def list():
    return render_template('list.html')