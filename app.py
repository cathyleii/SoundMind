from flask import Flask, render_template, redirect, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import json
import spotify
import os
from sentiment_analysis import analyze_text
from dotenv import load_dotenv

app = Flask(__name__)   # Flask constructor 

load_dotenv()

JOY_PLAYLIST1 = "spotify:playlist:7GhawGpb43Ctkq3PRP1fOL"
JOY_PLAYLIST2 = "spotify:playlist:4Fh0313D3PitYzICKHhZ7r"

SAD_PLAYLIST1 = "spotify:playlist:1XE7rQIGl1NFtWEAfwn4b9"

SAD_FEAR_COMFORT_PLAYLIST = "spotify:playlist:2cLa9xr9SArrzy0wXnW8m2"

FEAR_PLAYLIST1 = "spotify:playlist:12M8uwtzZqKHKSbBFbhGFy"
FEAR_PLAYLIST_INSTRUMENTALS = "spotify:playlist:7LI3zw8HLkjKo5YpvA26KG"

ANGER_PLAYLIST1 = "spotify:playlist:10egOYgYVWoviGAfdpiRty"
ANGER_PLAYLIST_RAP = "spotify:playlist:4WEn4bQ84SdvLIkwWqa1H8"

NEUTRAL_TOP_50 = "spotify:playlist:37i9dQZEVXbMDoHDwVN2tF"
NEUTRAL_TODAYS_HITS = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M"

app.secret_key = os.getenv("FLASK_SECRET_KEY")




# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def index():
    unfilled_fields = session.pop("unfilled_fields", False)
    return render_template("index.html", unfilled_fields=unfilled_fields)

@app.route('/analysis-complete')
def analysis_complete():
    analysis = session.get("analysis", "Error: Something went wrong, please try again.")

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
    try:
        q1_text = request.form["q1_text"]
        q2_text = request.form["q2_text"]
        q3_text = request.form.get("q3_text")
        mood = request.form["mood"]
    except KeyError:
        session["unfilled_fields"] = True
        return redirect("/")
    else:
        if not q1_text or not q2_text:
            session["unfilled_fields"] = True
            return redirect("/")
        
        input_string = f"I feel {mood} because {q1_text}. {q2_text} {q3_text}"
        print(input_string)
        session["analysis"] = analyze_text(input_string)
        return redirect("/analysis-complete")
    



  
if __name__=='__main__': 
   app.run(debug=True) 