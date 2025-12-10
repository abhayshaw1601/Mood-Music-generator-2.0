import nltk
import spotipy
import os
import uvicorn
from spotipy.oauth2 import SpotifyClientCredentials
from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

app = FastAPI()

# 1. Mount Static Files (CSS, JS, Images)
# This tells FastAPI to look in the current directory (".") for static files
app.mount("/static", StaticFiles(directory="."), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

# Download NLTK data to a specific directory to avoid permission errors on servers
nltk.download("vader_lexicon", download_dir="/tmp/nltk_data")
nltk.data.path.append("/tmp/nltk_data")

sia = SentimentIntensityAnalyzer()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ... (Keep your detect_mood function and SongRequest class as they are) ...

def detect_mood(text):
    score = sia.polarity_scores(text)
    compound = score["compound"]
    if compound >= 0.6: return "very happy "
    elif 0.3 <= compound < 0.6: return "happy "
    elif 0.05 <= compound < 0.3: return "calm / relaxed "
    elif -0.05 < compound < 0.05: return "neutral "
    elif -0.3 <= compound <= -0.05: return "sad "
    elif -0.6 <= compound < -0.3: return "very sad "
    else: return "angry "

class SongRequest(BaseModel):
    message: str
    platform: str = "both"
    language: str = "random"

# 2. Add a Route for the Homepage
@app.get("/")
async def read_index():
    return FileResponse('index.html')

# 3. Add Routes for other HTML pages if they exist
@app.get("/{page_name}.html")
async def read_page(page_name: str):
    if os.path.exists(f"{page_name}.html"):
        return FileResponse(f"{page_name}.html")
    return {"error": "Page not found"}

@app.post("/get_songs")
def get_songs(request: SongRequest):
    # ... (Keep your existing get_songs logic exactly the same) ...
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
        song_entry = {"name": name, "artist": artist}
        
        # Helper for YouTube Links
        sname = name.replace(" ", "+").replace("'", "")
        sartist = artist.replace(" ", "+").replace("'", "")
        yt_query = f"https://www.youtube.com/results?search_query={sname}+{sartist}"
        
        if platform in ["both", "spot"]:
            song_entry["spotify"] = spotify_url
        if platform in ["both", "yt"]:
            song_entry["youtube"] = yt_query

        song.append(song_entry)

    return {"mood": mood, "songs": song}

app.mount("/", StaticFiles(directory=".", html=True), name="public")

if __name__ == "__main__":
    # Important: Use os.environ.get('PORT') for deployment
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)