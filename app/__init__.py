from flask import Flask, render_template, jsonify, request
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123412341234",
  database="gpusearch"
)

cursor = mydb.cursor()

app = Flask(__name__)

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
    return render_template('index.html', name=name, release_date=release_date )

# @app.route('/autocomplete')
# def autocomplete():
    query = request.args.get('query')
    sql = "SELECT name FROM game WHERE name LIKE %s"
    cursor.execute(sql, ('%' + query + '%',))
    results = cursor.fetchall()
    return jsonify([result[0] for result in results])
