from flask import Flask, render_template, redirect, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import requests
import json
import spotify
import os
from sentiment_analysis import analyze_text
from dotenv import load_dotenv

app = Flask(__name__)   # Flask constructor 

load_dotenv()

JOY_PLAYLIST1 = "spotify:playlist:7GhawGpb43Ctkq3PRP1fOL"
JOY_PLAYLIST2 = "spotify:playlist:4Fh0313D3PitYzICKHhZ7r"

app.secret_key = os.getenv("FLASK_SECRET_KEY")




# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def index():
    return render_template("index.html")

@app.route('/analysis-complete')
def analysis_complete():
    analysis = session.get("analysis", "error")

    joy_tracks1 = spotify.retrieve_playlist_tracks(JOY_PLAYLIST1)
    joy_tracks2 = spotify.retrieve_playlist_tracks(JOY_PLAYLIST2)

    rand_track = spotify.generate_random_track(joy_tracks1, joy_tracks2)
    track_name = rand_track['name']
    track_url = rand_track['external_urls']['spotify']
    track_pic = rand_track['album']['images'][1]['url']


    return render_template("analysis-complete.html",
                           track_name=track_name,
                           track_url=track_url,
                           track_pic=track_pic,
                           analysis=analysis)

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form.getlist("text")
    input_string = ''

    for ans in text:
        input_string += f"{ans} "
    print(input_string)
    session["analysis"] = analyze_text(input_string)
    return redirect("/analysis-complete")
    



  
if __name__=='__main__': 
   app.run(debug=True) 