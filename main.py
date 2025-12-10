import nltk
import spotipy
import os
import uvicorn
import random
from spotipy.oauth2 import SpotifyClientCredentials
from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# --- SETUP ---
print("\n🔥 MOOD MUSIC: LANGUAGE-LOCKED LEGEND MODE ACTIVE 🔥\n")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

# Secure NLTK
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download("vader_lexicon", download_dir="/tmp/nltk_data")
    nltk.data.path.append("/tmp/nltk_data")

sia = SentimentIntensityAnalyzer()

# Auth
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --- 1. LEGEND POOLS ---
ARTIST_POOLS = {
    "hindi": [
        "Arijit Singh", "Badshah", "Neha Kakkar", "Pritam", "Shreya Ghoshal", 
        "Vishal Dadlani", "Sunidhi Chauhan", "Amit Trivedi", "Mika Singh", 
        "Yo Yo Honey Singh", "Sonu Nigam", "KK", "Mohit Chauhan", "Kumar Sanu", 
        "Udit Narayan", "Armaan Malik", "Jubin Nautiyal", "Sachin-Jigar"
    ],
    "bengali": [
        "Anupam Roy", "Jeet Gannguli", "Rupam Islam", "Timir Biswas", "Somlata Acharyya Chowdhury", 
        "Iman Chakraborty", "Lagnajita Chakraborty", "Sahana Bajpaie", "Arindom", "Rupankar Bagchi",
        "Fossils", "Chandrabindoo", "Cactus", "Bhoomi", "Moheener Ghoraguli",
        "Nachiketa", "Anjan Dutt", "Srikanto Acharya", "Lopamudra Mitra", 
        "Kishore Kumar", "Kumar Sanu", "Hemant Kumar", "Manna Dey"
    ],
    "punjabi": [
        "Diljit Dosanjh", "Karan Aujla", "AP Dhillon", "Sidhu Moose Wala", "Guru Randhawa",
        "Hardy Sandhu", "Ammy Virk", "B Praak", "Mankirt Aulakh", "Jassie Gill", "Sharry Mann"
    ],
    "english": [
        "Taylor Swift", "The Weeknd", "Harry Styles", "Justin Bieber", "Dua Lipa",
        "Coldplay", "Ed Sheeran", "Ariana Grande", "Bruno Mars", "Katy Perry"
    ]
}

# --- 2. MOOD ENGINE ---
def detect_mood(text):
    score = sia.polarity_scores(text)
    compound = score["compound"]

    if compound >= 0.5:
        return "Very Happy", "party dance"
    elif 0.1 <= compound < 0.5:
        return "Happy", "happy feel good"
    elif -0.1 < compound < 0.1:
        return "Calm", "soft acoustic"
    elif -0.5 <= compound <= -0.1:
        return "Sad", "sad emotional"
    elif compound < -0.5:
        return "Very Sad", "heartbreak soulful"
    else:
        return "Angry", "rock high energy"

class SongRequest(BaseModel):
    message: str
    platform: str = "both"
    language: str = "random"

# --- API ROUTES ---
@app.post("/get_songs")
def get_songs(request: SongRequest):
    user_text = request.message
    platform = request.platform
    language = request.language.lower().strip()

    display_mood, mood_keywords = detect_mood(user_text)

    market_code = "IN"
    all_valid_songs = []
    seen_urls = set()
    
    # 3. ACCUMULATOR LOOP
    attempts = 0
    max_attempts = 8 # Try up to 8 different artists
    
    while len(all_valid_songs) < 5 and attempts < max_attempts:
        attempts += 1
        search_query = ""
        current_artist = ""
        
        # A. Pick Artist & Build Query
        if language in ARTIST_POOLS:
            current_artist = random.choice(ARTIST_POOLS[language])
            
            # --- CRITICAL FIX: FORCE LANGUAGE IN QUERY ---
            # If language is Bengali, we add "Bangla" to the search query.
            # "Arijit Singh Bangla party dance" -> Forces Bengali results
            query_lang_tag = ""
            if language == "bengali": query_lang_tag = "Bangla"
            elif language == "hindi": query_lang_tag = "Bollywood"
            elif language == "punjabi": query_lang_tag = "Punjabi"
            
            search_query = f"{current_artist} {query_lang_tag} {mood_keywords}"
            print(f"🎯 Attempt {attempts}: {search_query}")
        else:
            if language == "english":
                market_code = "US"
                search_query = f"Top {mood_keywords} hits"
            else:
                search_query = f"{mood_keywords} music"
                
        # B. Fetch Songs
        try:
            result = sp.search(q=search_query, type='track', limit=10, market=market_code)
            
            if 'tracks' in result and 'items' in result['tracks']:
                for track in result['tracks']['items']:
                    if len(all_valid_songs) >= 10: break

                    name = track['name']
                    artist_name = track['artists'][0]['name']
                    url = track['external_urls']['spotify']
                    
                    if url in seen_urls: continue

                    # --- STRICT VALIDATION ---
                    if language in ARTIST_POOLS:
                        query_parts = current_artist.lower().split()
                        artist_lower = artist_name.lower()
                        
                        # Identity Check: Is this the Legend we asked for?
                        if not any(part in artist_lower for part in query_parts):
                            continue 

                    # Holidays Block
                    if "birthday" in name.lower() or "christmas" in name.lower():
                        continue

                    # Success
                    song_entry = {"name": name, "artist": artist_name}
                    if platform in ["both", "spot"]: song_entry["spotify"] = url
                    if platform in ["both", "yt"]:
                        sname = name.replace(" ", "+").replace("'", "")
                        sartist = artist_name.replace(" ", "+").replace("'", "")
                        song_entry["youtube"] = f"https://www.youtube.com/results?search_query={sname}+{sartist}"

                    all_valid_songs.append(song_entry)
                    seen_urls.add(url)

        except Exception as e:
            print(f"Error: {e}")
            continue
            
        if language not in ARTIST_POOLS: break

    # 4. SHUFFLE & RETURN
    final_songs = []
    if len(all_valid_songs) > 0:
        count = min(len(all_valid_songs), 5)
        final_songs = random.sample(all_valid_songs, count)

    return {"mood": display_mood, "songs": final_songs}

# --- STATIC FILES ---
app.mount("/", StaticFiles(directory=".", html=True), name="public")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)