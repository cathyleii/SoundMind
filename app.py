from flask import Flask, render_template, redirect, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import requests
import json
import spotify
import torch
from transformers import AutoTokenizer, RobertaForSequenceClassification

app = Flask(__name__)   # Flask constructor 


JOY_PLAYLIST1 = "spotify:playlist:7GhawGpb43Ctkq3PRP1fOL"
JOY_PLAYLIST2 = "spotify:playlist:4Fh0313D3PitYzICKHhZ7r"





# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def index():

    tokenizer = AutoTokenizer.from_pretrained("FacebookAI/roberta-base")
    model = RobertaForSequenceClassification.from_pretrained("FacebookAI/roberta-base", problem_type="multi_label_classification")

    inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_class_ids = torch.arange(0, logits.shape[-1])[torch.sigmoid(logits).squeeze(dim=0) > 0.5]

# To train a model on `num_labels` classes, you can pass `num_labels=num_labels` to `.from_pretrained(...)`
    num_labels = len(model.config.id2label)
    model = RobertaForSequenceClassification.from_pretrained(
        "FacebookAI/roberta-base", num_labels=num_labels, problem_type="multi_label_classification"
    )

    labels = torch.sum(
        torch.nn.functional.one_hot(predicted_class_ids[None, :].clone(), num_classes=num_labels), dim=1
    ).to(torch.float)
    loss = model(**inputs, labels=labels).loss
    return render_template("index.html")

@app.route('/analysis-complete')
def analysis_complete():

    joy_tracks1 = spotify.retrieve_playlist_tracks(JOY_PLAYLIST1)
    joy_tracks2 = spotify.retrieve_playlist_tracks(JOY_PLAYLIST2)

    rand_track = spotify.generate_random_track(joy_tracks1, joy_tracks2)
    track_name = rand_track['name']
    track_url = rand_track['external_urls']['spotify']
    track_pic = rand_track['album']['images'][1]['url']


    return render_template("analysis-complete.html",
                           track_name=track_name,
                           track_url=track_url,
                           track_pic=track_pic)


  
if __name__=='__main__': 
   app.run(debug=True) 