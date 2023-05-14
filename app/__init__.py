from urllib.parse import urljoin
import mysql.connector
from flask import Flask, render_template, jsonify, request
from igdb.igdbapi_pb2 import GameResult
from igdb.wrapper import IGDBWrapper
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123412341234",
  database="gpusearch"
)

cursor = mydb.cursor()

app = Flask(__name__)

## CODE FOR API'S

wrapper = IGDBWrapper('ed7hmod9n4zphsnxhr3n10hab2h296','97p1lbcr39cvkwswygawm9aq2fkhbm')

# Search for ID by name

def get_game_id(name):
    byte_array = wrapper.api_request(
            'games.pb',
            f'fields id, name; search "{name}"; where version_parent = null;'
          )
    games_message = GameResult()
    games_message.ParseFromString(byte_array) 
    game_id = games_message.games[0].id
    return game_id
    
#Get cover URL

def get_game_cover(game_id):
    byte_array = wrapper.api_request(
                'covers',
                f'fields url; where id = {game_id};'
            )
    json_response = json.loads(byte_array.decode())
    url = json_response[0]['url']
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
    search_term = request.form['search_term']
    cursor.execute("SELECT name, release_date FROM games WHERE name=%s", (search_term,))
    results = cursor.fetchone()
    name = results[0]
    release_date = results[1]
    game_id = get_game_id(search_term)
    cover_url = get_game_cover(game_id)
    return render_template('index.html', name=name, release_date=release_date, cover_url=cover_url)
# @app.route('/autocomplete')
# def autocomplete():
    query = request.args.get('query')
    sql = "SELECT name FROM game WHERE name LIKE %s"
    cursor.execute(sql, ('%' + query + '%',))
    results = cursor.fetchall()
    return jsonify([result[0] for result in results])


