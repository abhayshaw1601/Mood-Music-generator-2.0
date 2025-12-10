import nltk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def detect_mood(text):
    score = sia.polarity_scores(text)
    compound = score["compound"]

    if compound >= 0.6:
        return "very happy "
    elif 0.3 <= compound < 0.6:
        return "happy "
    elif 0.05 <= compound < 0.3:
        return "calm / relaxed "
    elif -0.05 < compound < 0.05:
        return "neutral "
    elif -0.3 <= compound <= -0.05:
        return "sad "
    elif -0.6 <= compound < -0.3:
        return "very sad "
    else:
        return "angry "


class SongRequest(BaseModel):
    message: str
    platform: str = "both"
    language: str = "random"

@app.post("/get_songs")
def get_songs(request: SongRequest):
    user_text = request.message
    platform = request.platform
    language = request.language

    mood = detect_mood(user_text)
    if language and language != "random":
        mood =f"{language} {mood}"

    result = sp.search(q=mood, type='track', limit=5)

    song = []

    for track in result['tracks']['items']:
        name = track['name']
        artist = track['artists'][0]['name']
        spotify_url = track['external_urls']['spotify']
        sname = name.replace(" ", "+")
        sname = sname.replace("'", "")
        sartist = artist.replace(" ", "+")
        sartist = sartist.replace("'", "")
        yt_query = f"https://www.youtube.com/results?search_query={sname}+{sartist}"

        song_entry = {"name": name, "artist": artist}
        if platform in ["both", "spot"]:
            song_entry["spotify"] = spotify_url
        if platform in ["both", "yt"]:
            song_entry["youtube"] = yt_query

        song.append(song_entry)

    return {"mood": mood, "songs": song}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
