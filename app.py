from flask import Flask, render_template, redirect, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import json
import spotify
import os
import sentiment_analysis
from dotenv import load_dotenv

app = Flask(__name__)   # Flask constructor 

load_dotenv()

JOY_PLAYLIST1 = "spotify:playlist:7GhawGpb43Ctkq3PRP1fOL"
JOY_PLAYLIST2 = "spotify:playlist:4Fh0313D3PitYzICKHhZ7r"

SAD_PLAYLIST1 = "spotify:playlist:1XE7rQIGl1NFtWEAfwn4b9"
SAD_FEAR_PLAYLIST = "spotify:playlist:2cLa9xr9SArrzy0wXnW8m2"
FEAR_PLAYLIST_INSTRUMENTALS = "spotify:playlist:7LI3zw8HLkjKo5YpvA26KG"

ANGER_PLAYLIST1 = "spotify:playlist:10egOYgYVWoviGAfdpiRty"
ANGER_PLAYLIST_RAP = "spotify:playlist:4WEn4bQ84SdvLIkwWqa1H8"



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

    emotions = sentiment_analysis.get_emotions(analysis)

    for emotion in emotions:
        if emotion != "disgust" and emotion != "surprise" and emotion != "neutral":
            top_emotion = emotion
            break

    match top_emotion:
        case "sadness":
            playlist1 = SAD_PLAYLIST1
            playlist2 = SAD_FEAR_PLAYLIST
        case "fear":
            playlist1 = SAD_FEAR_PLAYLIST
            playlist2 = FEAR_PLAYLIST_INSTRUMENTALS
        case "joy":
            playlist1 = JOY_PLAYLIST1
            playlist2 = JOY_PLAYLIST2
        case "anger":
            playlist1 = ANGER_PLAYLIST1
            playlist2 = ANGER_PLAYLIST_RAP
        
    

    tracks1 = spotify.retrieve_playlist_tracks(playlist1)
    tracks2 = spotify.retrieve_playlist_tracks(playlist2)

    rand_track1 = spotify.generate_random_track(tracks1)
    rand_track2 = spotify.generate_random_track(tracks2)

    # track1_name = rand_track1['name']
    # track1_url = rand_track1['external_urls']['spotify']
    # track1_pic = rand_track1['album']['images'][1]['url']
    track1_name = spotify.get_track_name(rand_track1)
    track2_name = spotify.get_track_name(rand_track2)

    track1_url = spotify.get_track_url(rand_track1)
    track2_url = spotify.get_track_url(rand_track2)

    track1_pic = spotify.get_track_pic(rand_track1)
    track2_pic = spotify.get_track_pic(rand_track2)

    artist1_name = spotify.get_artist(rand_track1)
    artist2_name = spotify.get_artist(rand_track2)


    return render_template("analysis-complete.html",
                           track1_name=track1_name,
                           track1_url=track1_url,
                           track1_pic=track1_pic,
                           track2_name=track2_name,
                           track2_url=track2_url,
                           track2_pic=track2_pic,
                           analysis=analysis,
                           top_emotion=top_emotion.title(),
                           artist1_name=artist1_name,
                           artist2_name=artist2_name)

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
        session["analysis"] = sentiment_analysis.analyze_text(input_string)
        return redirect("/analysis-complete")
    



  
if __name__=='__main__': 
   app.run(debug=True) 