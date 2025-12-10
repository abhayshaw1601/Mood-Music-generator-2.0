
# 🎵 Mood Music Generator 2.0

<div align="center">

### 🎧 AI-Powered Music Discovery Based on Your Emotions

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Spotify](https://img.shields.io/badge/API-Spotify-1DB954)
![Vanta.js](https://img.shields.io/badge/Frontend-Vanta.js-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## 📖 About

**Mood Music Generator 2.0** is an intelligent web application that curates music playlists based on your current emotional state. Unlike standard music players, it uses **Natural Language Processing (NLP)** to analyze your text input, determines your sentiment, and fetches perfectly matching tracks from Spotify and YouTube.

The interface is built with a stunning **Glassmorphism UI**, featuring 3D tilt effects and a dynamic, fog-animated background powered by WebGL.

---

## ✨ Key Features

* **🧠 AI Mood Detection:** Uses **NLTK VADER** sentiment analysis to understand if you are *Happy, Sad, Calm, Angry,* or *Neutral*.
* **🎹 Smart Recommendations:** Fetches tracks dynamically using the **Spotify API**.
* **📺 Dual-Platform Playback:**
    * **Spotify:** Embedded player for instant previews.
    * **YouTube:** Direct links to music videos or lyric versions.
* **🌐 Language Support:** Filter songs by language (English, Hindi, Punjabi, Bengali).
* **🎨 Immersive UI/UX:**
    * **Vanta.js:** 3D animated Fog background.
    * **Glassmorphism:** Modern, translucent card design.
    * **Tilt.js:** Interactive 3D hover effects on buttons.
* **⚡ High Performance:** Built on **FastAPI** for lightning-fast responses.

---

## 👀 Glimpse of the App

### Home Screen (Dark/Light Mode)
![Home Screen](![light mode](image-2.png))
![Home Screen](![dark mode](image-1.png))

### Music Recommendations
![Results Screen](![result ](image-3.png))

---

## 🛠️ Tech Stack

**Backend:**
* **Python:** Core logic.
* **FastAPI:** High-performance web framework.
* **Spotipy:** Lightweight Python library for the Spotify Web API.
* **NLTK:** Natural Language Toolkit for sentiment analysis.

**Frontend:**
* **HTML5 / CSS3:** Responsive layout with CSS Variables.
* **JavaScript (ES6):** Async fetch API and DOM manipulation.
* **Libraries:** `Vanta.js` (Background), `Three.js` (3D Engine), `Vanilla-Tilt.js` (Interactivity), `Anime.js` (Animations).

---

## 🚀 Installation & Setup

### 1. Prerequisites
* Python installed on your machine.
* A **Spotify Developer Account** (to get API keys).

### 2. Clone the Repository
```bash
git clone [https://github.com/abhayshaw1601/Mood-Music-generator.git](https://github.com/abhayshaw1601/Mood-Music-generator.git)
cd Mood-Music-generator


### 3\. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4\. Install Dependencies

```bash
pip install -r requirements.txt
```

*Note: If you encounter errors, make sure you have `wheel` installed (`pip install wheel`).*

### 5\. Configure API Keys

Create a file named `.env` in the root directory and add your Spotify credentials.
**Important:** Use the exact variable names below to match the code.

```ini
client_id=YOUR_SPOTIFY_CLIENT_ID
client_secret=YOUR_SPOTIFY_CLIENT_SECRET
```

### 6\. Run the Application

Start the FastAPI server using Uvicorn.

```bash
python main.py
```

The app will be live at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

-----

## 🔧 Troubleshooting

### 🐢 Animation Lag / High GPU Usage

If the background animation feels slow or your laptop heats up:

1.  Go to **Windows Graphics Settings**.
2.  Add **Chrome/Edge** to the list.
3.  Set it to **"High Performance"** (NVIDIA/AMD GPU) instead of Integrated Graphics.
4.  Ensure "Hardware Acceleration" is enabled in your browser settings.

### 🐍 "Module Not Found" Errors

If you see errors like `Import "nltk" could not be resolved`:

1.  Ensure your virtual environment is **active** (you should see `(venv)` in your terminal).
2.  Press `Ctrl + Shift + P` in VS Code -\> "Python: Select Interpreter" -\> Choose the one inside `venv`.

-----

## 🤝 Contributions

Contributions are welcome\!

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

-----

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

-----

\<div align="center"\>
Made with ❤️ and 🎵 by \<a href="https://www.google.com/search?q=https://github.com/abhayshaw1601"\>Abhay Shaw\</a\>
\</div\>

```
```
