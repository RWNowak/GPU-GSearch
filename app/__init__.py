from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'My Flask App'
    return render_template('index.html', title=title)
