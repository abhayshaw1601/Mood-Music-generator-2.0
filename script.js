document.addEventListener("DOMContentLoaded", () => {
    // 1. Cache DOM Elements for better performance
    const elements = {
        userInput: document.getElementById("moodInput"),
        platformSelect: document.getElementById("link-select"),
        languageSelect: document.getElementById("language-select"),
        sendBtn: document.getElementById("sendButton"),
        responseArea: document.getElementById("responseArea"),
        resultsSection: document.getElementById("resultsSection"),
        toggleBtn: document.getElementById("themeToggle"),
        moodButtons: document.querySelectorAll(".mood-btn"),
        genrePills: document.querySelectorAll(".genre-pill"),
    };

    // Filter state
    let currentGenre = 'all';

    const API_URL = "http://127.0.0.1:5000/get_songs";

    // 1.5 Initialize Dark Mode from LocalStorage
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark");
        elements.toggleBtn.textContent = "☀️";
    }

    // 2. Vanta.js Configuration & Management
    let vantaEffect = null;

    const vantaOptions = {
        light: {
            highlightColor: 0xff6b6b,
            midtoneColor: 0x764ba2,
            lowlightColor: 0x2a1b3d,
            baseColor: 0x1a1a2e,
            blurFactor: 0.6,
            speed: 1.2
        },
        dark: {
            highlightColor: 0x4ecdc4, // Teal/Cyan accent
            midtoneColor: 0x0f2027,   // Dark Blue/Green
            lowlightColor: 0x203a43,  // Dark Slate
            baseColor: 0x050505,      // Deep Black
            blurFactor: 0.8,
            speed: 1.0
        }
    };

    const initVanta = (theme) => {
        try {
            if (window.VANTA) {
                // If effect exists, destroy it first to update options
                if (vantaEffect) vantaEffect.destroy();

                const opts = theme === 'dark' ? vantaOptions.dark : vantaOptions.light;

                vantaEffect = VANTA.FOG({
                    el: "body",
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    minHeight: 200.00,
                    minWidth: 200.00,
                    ...opts
                });
            }
        } catch (e) {
            console.warn("Vanta JS failed to load - falling back to CSS background.");
        }
    };

    // Initial Load
    initVanta(document.body.classList.contains("dark") ? "dark" : "light");

    // Force Vanta to resize on window events
    const forceVantaResize = () => {
        if (vantaEffect && vantaEffect.resize) {
            vantaEffect.resize();
        }
    };

    window.addEventListener('resize', forceVantaResize);
    window.addEventListener('scroll', forceVantaResize);

    // Force initial resize after a delay to ensure proper rendering
    setTimeout(forceVantaResize, 100);
    setTimeout(forceVantaResize, 500);


    // 3. Player Creation Helpers
    const createSpotifyPlayer = (spotifyUrl) => {
        if (!spotifyUrl) return '';
        const trackId = spotifyUrl.split('/track/')[1]?.split('?')[0];
        if (!trackId) return '';

        return `
            <div class="spotify-player">
                <iframe 
                  src="https://open.spotify.com/embed/track/${trackId}?utm_source=generator&theme=0" 
                  width="100%" 
                  height="152" 
                  frameBorder="0" 
                  allowfullscreen="" 
                  allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                  loading="lazy">
                </iframe>
            </div>`;
    };

    const createYouTubePlayer = (songName, artist) => {
        // Safer URL encoding for special characters
        const query = encodeURIComponent(`${songName} ${artist}`);
        const searchUrl = `https://www.youtube.com/results?search_query=${query}`;
        const musicUrl = `https://music.youtube.com/search?q=${query}`;

        return `
            <div class="youtube-player">
                <div class="youtube-art-placeholder">
                    <img src="https://img.icons8.com/ios-filled/100/ffffff/youtube-play.png" alt="Play">
                </div>
                <div class="youtube-info-area">
                    <div>
                        <h4>${songName}</h4>
                        <p>${artist}</p>
                    </div>
                    <div class="youtube-controls">
                        <a href="${searchUrl}" target="_blank" class="yt-btn play">▶ Play</a>
                        <a href="${musicUrl}" target="_blank" class="yt-btn search">Music App</a>
                    </div>
                </div>
            </div>`;
    };

    // 4. Main Fetch Logic
    const fetchSongs = async () => {
        const moodText = elements.userInput.value.trim();
        const platform = elements.platformSelect.value;
        const language = elements.languageSelect.value;

        if (!moodText) return alert("Please enter mood or select a mood button.");
        if (!platform) return alert("Please select a platform.");
        if (!language) return alert("Please select a language.");

        // Show Loading State
        elements.resultsSection.style.display = "block";
        elements.responseArea.innerHTML = '<p style="text-align:center;">🎧 Curating your playlist...</p>';

        // Anime.js Entrance for Results Section
        anime({
            targets: elements.resultsSection,
            opacity: [0, 1],
            translateY: [20, 0],
            duration: 800,
            easing: 'easeOutExpo'
        });

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: moodText, platform, language })
            });

            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();
            renderSongs(data.songs, platform);

        } catch (error) {
            console.error("Error:", error);
            elements.responseArea.innerHTML = "<p>Something went wrong. Please check your connection.</p>";
        }
    };

    // 5. Render Logic (Optimized with DocumentFragment)
    const renderSongs = (songs, platform) => {
        elements.responseArea.innerHTML = "";
        const fragment = document.createDocumentFragment();

        songs.forEach((song) => {
            const container = document.createElement('div');
            container.className = 'song-container';

            // Determine what to show
            const showSpotify = (platform === 'both' || platform === 'spot');
            const showYoutube = (platform === 'both' || platform === 'yt');

            let playersHTML = '';
            let linksHTML = '';

            // Build Spotify
            if (showSpotify) {
                if (song.spotify) {
                    playersHTML += createSpotifyPlayer(song.spotify);
                    linksHTML += `<a href="${song.spotify}" target="_blank" class="platform-link spotify-link">🎵 Open in Spotify</a>`;
                } else if (platform === 'spot') {
                    playersHTML += '<p style="text-align:center; opacity:0.7;">Spotify preview unavailable</p>';
                }
            }

            // Build YouTube
            if (showYoutube) {
                playersHTML += createYouTubePlayer(song.name, song.artist);
                if (song.youtube) {
                    linksHTML += `<a href="${song.youtube}" target="_blank" class="platform-link youtube-link">📺 Search on YouTube</a>`;
                }
            }

            container.innerHTML = `
                <div class="song-info">
                    <h4>${song.name}</h4>
                    <p>by ${song.artist}</p>
                </div>
                <div class="player-container ${platform === 'both' ? 'dual-player' : 'single-player'}">
                    ${playersHTML}
                </div>
                <div class="song-links">
                    ${linksHTML}
                </div>
            `;
            fragment.appendChild(container);
        });

        // Batch update the DOM (Performance Boost)
        elements.responseArea.appendChild(fragment);

        // Anime.js Staggered List Animation
        anime({
            targets: '.song-container',
            opacity: [0, 1],
            translateY: [20, 0],
            delay: anime.stagger(100), // 100ms delay between each
            duration: 800,
            easing: 'easeOutCubic'
        });
    };

    // 6. Event Listeners
    elements.sendBtn.addEventListener("click", fetchSongs);
    elements.userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") fetchSongs();
    });

    elements.toggleBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        const isDark = document.body.classList.contains("dark");
        elements.toggleBtn.textContent = isDark ? "☀️" : "🌙";
        localStorage.setItem("theme", isDark ? "dark" : "light");

        // Refresh Vanta with new colors
        initVanta(isDark ? "dark" : "light");
    });

    // Mood Button Logic with Animation
    elements.moodButtons.forEach(button => {
        button.addEventListener("click", () => {
            const mood = button.getAttribute("data-mood");
            elements.userInput.value = `I'm feeling ${mood}`;

            // Cleaner animation using Web Animations API
            elements.userInput.animate([
                { background: "rgba(255, 107, 107, 0.2)", borderColor: "var(--accent)" },
                { background: "rgba(255, 255, 255, 0.9)", borderColor: "var(--glass-border)" }
            ], { duration: 1000 });

            elements.userInput.focus();
        });
    });

    // Genre Pills Handler
    elements.genrePills.forEach(pill => {
        pill.addEventListener('click', () => {
            // Remove active from all
            elements.genrePills.forEach(p => p.classList.remove('active'));
            // Add active to clicked
            pill.classList.add('active');
            currentGenre = pill.getAttribute('data-genre');

            // Anime.js pulse effect
            anime({
                targets: pill,
                scale: [1, 1.1, 1],
                duration: 300,
                easing: 'easeOutElastic(1, .5)'
            });

            console.log(`Genre filter: ${currentGenre}`);
        });
    });

    // Set default genre active
    if (elements.genrePills.length > 0) {
        elements.genrePills[0].classList.add('active');
    }
});
// ===== MOBILE OPTIMIZATIONS =====

// 1. Touch feedback for better mobile UX
const addTouchFeedback = () => {
    const touchElements = document.querySelectorAll('.mood-btn, .platform-link, .youtube-btn, .social-link');
    
    touchElements.forEach(element => {
        element.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
            this.style.transition = 'transform 0.1s ease';
        }, { passive: true });
        
        element.addEventListener('touchend', function() {
            setTimeout(() => {
                this.style.transform = '';
                this.style.transition = '';
            }, 100);
        }, { passive: true });
    });
};

// 2. Prevent zoom on double tap for iOS
const preventDoubleTabZoom = () => {
    let lastTouchEnd = 0;
    document.addEventListener('touchend', function (event) {
        const now = (new Date()).getTime();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
};

// 3. Optimize Vanta.js for mobile performance
const optimizeVantaForMobile = () => {
    if (window.innerWidth <= 768) {
        // Reduce Vanta performance on mobile for better battery life
        if (vantaEffect) {
            vantaEffect.setOptions({
                speed: 0.8,
                blurFactor: 0.4,
                zoom: 1.2
            });
        }
    }
};

// 4. Handle orientation changes
const handleOrientationChange = () => {
    window.addEventListener('orientationchange', () => {
        setTimeout(() => {
            // Refresh Vanta after orientation change
            if (vantaEffect) {
                vantaEffect.resize();
            }
            
            // Adjust layout if needed
            const container = document.querySelector('.container');
            if (container && window.innerWidth <= 768) {
                container.style.minHeight = 'auto';
            }
        }, 100);
    });
};

// 5. Improve scroll performance on mobile
const optimizeScrolling = () => {
    let ticking = false;
    
    const updateScrollElements = () => {
        // Add scroll-based optimizations here if needed
        ticking = false;
    };
    
    const requestTick = () => {
        if (!ticking) {
            requestAnimationFrame(updateScrollElements);
            ticking = true;
        }
    };
    
    window.addEventListener('scroll', requestTick, { passive: true });
};

// 6. Mobile-specific form improvements
const improveMobileForms = () => {
    const inputs = document.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        // Prevent zoom on focus for iOS
        input.addEventListener('focus', function() {
            if (window.innerWidth <= 768) {
                this.style.fontSize = '16px';
            }
        });
        
        // Add touch-friendly styling
        input.addEventListener('touchstart', function() {
            this.style.borderColor = 'var(--accent)';
        }, { passive: true });
        
        input.addEventListener('blur', function() {
            this.style.borderColor = '';
        });
    });
};

// 7. Initialize mobile optimizations
const initMobileOptimizations = () => {
    if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
        document.body.classList.add('touch-device');
        addTouchFeedback();
        preventDoubleTabZoom();
        improveMobileForms();
    }
    
    optimizeVantaForMobile();
    handleOrientationChange();
    optimizeScrolling();
    
    // Add mobile-specific classes
    if (window.innerWidth <= 768) {
        document.body.classList.add('mobile-device');
    }
    
    // Update on resize
    window.addEventListener('resize', () => {
        if (window.innerWidth <= 768) {
            document.body.classList.add('mobile-device');
        } else {
            document.body.classList.remove('mobile-device');
        }
        optimizeVantaForMobile();
    }, { passive: true });
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileOptimizations);
} else {
    initMobileOptimizations();
}