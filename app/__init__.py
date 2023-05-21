from flask import Flask, render_template, jsonify, request

#MYSQL CONNECTION
import mysql.connector, json, datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123412341234",
  database="gpusearch"
)

cursor = mydb.cursor()

#IMPORTS FOR THE IGDB API
from igdb.igdbapi_pb2 import GameResult
from igdb.wrapper import IGDBWrapper

wrapper = IGDBWrapper('ed7hmod9n4zphsnxhr3n10hab2h296','97p1lbcr39cvkwswygawm9aq2fkhbm')

## JINJA FOR INTEGRATING PYTHON CODE INTO THE .HTML FILES
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)

app = Flask(__name__)

## CODE FOR API'S

#GET GAME NAMES, URL'S AND ID'S. SEARCH BY NAME AND RETURN LISTS

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

#GET GAME NAME, COVER URL, RELEASE DATE AND SUMMARY, SEARCH BY ID, RETURN VARIABLES

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
    try:
        cover_url = game['cover'].get('url', '')
    except:
        cover_url = None
    try:
        rating = round(game['rating'])
    except:
        rating = None
    try:
        summary = game['summary']
    except:
        summary = None
    try:
        first_release_date=game['first_release_date']
        if first_release_date:
            first_release_date = datetime.datetime.fromtimestamp(first_release_date).strftime("%Y-%m-%d")
            release_date_year = first_release_date[0:4]
    except:
        release_date_year= None

    return game_name, game_id, cover_url, rating, summary, release_date_year

#GET GPU'S FROM DATABASE, SEARCH BY NAME

def getGPUs(name):
    query = f"SELECT min_gpu_nvidia, max_gpu_nvidia, min_gpu_amd, max_gpu_amd FROM games WHERE name = '{name}'"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        min_gpu_nvidia, max_gpu_nvidia, min_gpu_amd, max_gpu_amd = result
        return min_gpu_nvidia, max_gpu_nvidia, min_gpu_amd, max_gpu_amd
    else:
        return None

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
    #GET GAME INFORMATION
    id = request.form.get('game_id')
    game_name, game_id, cover_url, rating, summary, release_date_year = get_games_full(id)
    #GET GPU INFORMATION
    try:
        min_gpu_nvidia, max_gpu_nvidia, min_gpu_amd, max_gpu_amd = getGPUs(game_name)
    except:
        min_gpu_nvidia = None
        max_gpu_nvidia = None
        min_gpu_amd = None
        max_gpu_amd = None
    return render_template('index.html', game_name=game_name, game_id=game_id, cover_url=cover_url, rating=rating, summary=summary, 
                           release_date_year=release_date_year, min_gpu_nvidia=min_gpu_nvidia, max_gpu_nvidia=max_gpu_nvidia, 
                           min_gpu_amd=min_gpu_amd, max_gpu_amd=max_gpu_amd, zip=zip)
@app.route('/list')
def list():
    return render_template('list.html')