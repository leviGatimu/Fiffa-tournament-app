# ⚽ Pitchside Pro: Tournament Hub

> **Turn your local FIFA/EAFC game nights into a broadcast-quality league.**

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-green.svg?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg?style=for-the-badge)

**Pitchside Pro** is a locally hosted web application that manages your gaming tournaments. It features a stunning "Clean Glass" UI, real-time league tables, automated fixture generation, and a mid-season transfer market.

---

## ✨ Key Features

### 🏆 **Real League Integration**
* **Pre-Loaded Databases:** Instantly load teams and logos for the **Premier League**, **La Liga**, **Bundesliga**, **Serie A**, and **Ligue 1**.
* **Visual Selection:** Pick your team by clicking their official crest—no typing required.

### 📊 **Professional Analytics**
* **Live Table:** Tracks Points, Goal Difference (GD), Wins, Draws, Losses, and Clean Sheets (CS).
* **Golden Boot Race:** A live tracker on the dashboard showing the top goalscorer.
* **Form Guide:** Visual indicators (🟢 Wins / 🔴 Losses) to track momentum.

### 🎮 **Dynamic Gameplay**
* **Smart Scheduling:** Matches are auto-generated in a round-robin format.
* **Mid-Season Manager:** Friend joined late? Someone rage quit? Add or remove players instantly without breaking the schedule.
* **Broadcast History:** Match results are displayed in a TV-style "Full Time" feed.

### 🎨 **Visuals & Audio**
* **Clean Glass UI:** A modern, translucent interface designed to look great on large TV screens.
* **Sound Effects:** Audio cues for clicking buttons and confirming goals.
* **Champion Celebration:** A confetti explosion and trophy ceremony animation when the season ends.

---

## 📂 Project Structure

Ensure your folder looks like this for everything to work correctly:

```text
Pitchside-Pro/
│
├── app.py                # The main game engine (Python)
├── fifa_tournament.db    # Database (Auto-created on first run)
├── README.md             # This instruction manual
└── templates/
    └── index.html        # The visual interface (HTML/Tailwind)
```

🚀 Installation & Setup
1. Install Python
Make sure you have Python installed. If not, download it from python.org.

2. Install Requirements
Open your terminal (Command Prompt or PowerShell) in this folder and run:

Bash

pip install flask flask-sqlalchemy
3. Launch the Hub
Run the application with this command:

Bash

python app.py
4. Open in Browser
Open Chrome, Edge, or Firefox and go to: http://127.0.0.1:5000

📖 How to Use
Phase 1: Pre-Season Setup
Click the "Setup" button in the top navigation.

Select League: Choose a league (e.g., Premier League) to set the background theme and team list.

Add Managers: Enter player names (e.g., "Kenny") and click a Team Logo from the grid.

Click "Start Season". The system will generate the entire fixture list automatically.

Phase 2: Matchday
Go to the "Matches" tab.

Look at the "Pending List" and click "Add" on the games you want to play now.

These games move to the "Live Broadcast" section.

Click "Play", enter the score (e.g., 3 - 2), add highlights notes (e.g., "90th min winner"), and confirm.

Phase 3: Mid-Season Transfers
Adding a Player: Go to Setup > Mid-Season Manager. Enter their name, pick a team, and click "Add". They will be scheduled to play everyone else.

Removing a Player: Go to Setup > Mid-Season Manager. Click the red REMOVE button next to a player. They will be deleted, and their unplayed matches will be cancelled (played matches remain in history).

Phase 4: The Finale
Once every match is marked as completed, a Champion Screen will automatically trigger with the winner's stats and a trophy celebration.

🔧 Troubleshooting
🛑 "Internal Server Error" / Database Bugs
If you updated the code and the site crashes, your database is likely outdated.

Go to this URL in your browser: http://127.0.0.1:5000/hard_reset

This forces a factory reset of the system.

🖼️ "Images Not Loading"
The app uses online URLs for logos.

If you are offline or the link is blocked, the system automatically replaces the broken logo with a generic Shield Icon so the layout stays perfect.

🔊 "No Sound?"
Modern browsers block auto-playing audio. Click anywhere on the page once to "wake up" the audio engine.

💻 Tech Stack
Backend: Python (Flask)

Database: SQLite (via SQLAlchemy)

Frontend: HTML5, TailwindCSS (CDN)

Interactivity: Alpine.js (Lightweight JavaScript)

Effects: Canvas Confetti

Built for the love of the game. ⚽
