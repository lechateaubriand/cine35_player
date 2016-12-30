# all the imports
import os.path
import pickle
import subprocess
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import env_variables
from classes.util.ListDir import ListDir
import scripts.stop_automatic_ba
import scripts.launch_automatic_ba
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
    save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
    stop = pickle.load(open(save_file, "rb"))
    return render_template('main_page.html', stop=stop)

@app.route('/show_playlist')
def show_playlist():
    # selectionner tous les repertoires du lieu de stockage
    # et les mettre sous forme de dictionnaire
    # numero de semaine: [liste des fichiers]
    movie_list = ListDir.list_directory(env_variables.ba_directory, 'mp4')
    whole_movie_list = sorted([os.path.basename(x) for x in movie_list])
    slide_list = ListDir.list_directory(env_variables.ba_directory, 'jpg')
    whole_slide_list = sorted([os.path.basename(x) for x in slide_list])
    return render_template('show_playlist.html', whole_ba_list=whole_movie_list, whole_slide_list=whole_slide_list)


@app.route('/launch_playlist_all_prog')
def launch_playlist_all_prog():
    """
    lancement de la lecture des ba dont la date de programmation n'est pas depassee
    """
    scripts.launch_automatic_ba.main()        
    return render_template('main_page.html')


@app.route('/stop_playlist')
def stop_playlist():
    """
    vue utilisee pour arreter la lecture des bande-annonce 
    """
    scripts.stop_automatic_ba.main()
    return render_template('stop_playlist.html')


@app.route('/shutdown_pc')
def shutdown_pc():
    """
    vue utilisee pour arreter le PC
    """
    # Simple shutdown command
    subprocess.call(['sudo', 'shutdown', '-h', 'now'])
    return render_template('shutdown_pc.html')
