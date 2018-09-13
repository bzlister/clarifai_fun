import os
import sqlite3

from flask import (Flask, request, session, g, redirect, url_for, abort,
    render_template, flash)

from . import clarifi

#IMG_FOLDER = os.path.join('static', 'photo')

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#app.config['UPLOAD_FOLDER'] = IMG_FOLDER
@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['query']
    num_runs_string = request.form['autoruns']
    if num_runs_string == '':
        num_runs_string = '1'
    num_runs = int(num_runs_string)
    relatibility = int(request.form['relate'])
    num_runs = max(1, num_runs)
    num_runs = min(5, num_runs)
    processed_text = text.upper()
    result = clarifi.imageSearch(processed_text, num_runs, relatibility)
    filename = result['lastImage']
    seed = result['seed']
    return render_template("index.html", user_image = filename, ret_text=seed, relate_val=relatibility)

#@app.route('/index')
#def show_index():
    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
 #   return render_template("index.html", user_image = filename)
