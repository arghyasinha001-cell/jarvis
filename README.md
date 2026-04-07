# 🤖 J.A.R.V.I.S. — AI Voice Assistant

A voice-activated desktop assistant powered by **Google Gemini**, with a **CustomTkinter GUI**, **Microsoft Edge TTS** voice output, SMS-style reminders, system controls, file search, and more.

---

## ✨ Features

| Feature | Detail |
|---|---|
| **Wake-word activation** | Say "Jarvis" to activate from idle |
| **AI answers** | Powered by Gemini 2.0 Flash |
| **Natural voice output** | Microsoft Edge TTS (`en-US-ChristopherNeural`) |
| **Time & date** | Spoken on request |
| **Reminders / alarms** | "Remind me to check the oven in 10 minutes" |
| **System stats** | CPU usage, battery percentage |
| **Screenshot** | Auto-saved with timestamp |
| **Volume control** | Up / down / mute |
| **App launcher** | Open Spotify, Notepad, Chrome, VS Code… |
| **YouTube playback** | "Play Believer" |
| **Google search** | Opens browser with results |
| **File finder** | Searches Desktop, Downloads, Documents |
| **Memory** | "Remember that…" / "What do you remember?" |
| **Ambient hum** | Looping background sound while idle |
| **Command history** | Every command logged to `history.log` |
| **GUI** | Dark CustomTkinter interface with live console |

---

## 📁 Project Structure

```
Jarvis/
├── gui.py              ← Entry point (GUI)
├── jarvis.py           ← Core loop & wake-word logic
├── commands.py         ← All command handlers
├── ai.py               ← Gemini AI integration
├── speak.py            ← Edge TTS + pygame playback
├── speech.py           ← Microphone → text (Google SR)
├── alarm.py            ← Reminder / alarm system
├── hum.py              ← Ambient background sound
├── memory.py           ← Persistent JSON memory
├── history.py          ← Command logger
├── helpers.py          ← resource_path() utility
├── responses.py        ← Random acknowledgement phrases
├── test_import.py      ← Verify your Gemini API key
├── config.py           ← YOUR credentials (gitignored)
├── config.py.example   ← Template — copy and fill in
├── requirements.txt
├── Jarvis.spec         ← PyInstaller build config
├── logo.ico
└── sounds/
    ├── startup.mp3
    ├── shutdown.mp3
    └── hum.mp3
```

---

## 🚀 Quick Start

### 1. Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.9 – 3.11 | 3.12+ may have issues with some audio libs |
| Working microphone | Required for voice input |
| Speakers / headphones | Required for TTS output |
| Internet connection | Needed for Gemini AI, Edge TTS, and Google SR |

> **Windows only** — `keyboard`, `pyautogui`, and `os.system("start ...")` are Windows-specific. Linux/macOS users will need to adapt those calls.

### 2. Clone & install

```bash
git clone https://github.com/arghyasinha001-cell/jarvis.git
cd jarvis

python -m venv venv
venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

> If `pyaudio` fails to install, download the matching `.whl` from
> [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
> and install it manually: `pip install PyAudio‑0.2.14‑cpXX‑cpXX‑win_amd64.whl`

### 3. Add your Gemini API key

```bash
copy config.py.example config.py   # Windows
# or
cp config.py.example config.py     # Linux / macOS
```

Open `config.py` and paste your key:

```python
GEMINI_API_KEY = "AIzaSy-YOUR-KEY-HERE"
```

Get a free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

### 4. Add sound files

Create a `sounds/` folder and add three MP3 files:

```
sounds/
├── startup.mp3     # Played when Jarvis comes online
├── shutdown.mp3    # Played on exit
└── hum.mp3         # Looped ambient sound while idle
```

Any short MP3 works. The app runs fine without them (errors are caught silently).

### 5. Run

```bash
python gui.py
```

Click **INITIALIZE**, then say **"Jarvis"** to wake it up.

---

## 🎙️ Voice Commands

| Say… | Action |
|---|---|
| `"Jarvis"` | Wake up from idle |
| `"What time is it"` | Speaks current time |
| `"What is today's date"` | Speaks current date |
| `"CPU usage"` | Speaks CPU % |
| `"Battery percentage"` | Speaks battery level |
| `"Take a screenshot"` | Saves PNG with timestamp |
| `"Volume up / down / mute"` | Adjusts system volume |
| `"Remind me to [task] in [N] minutes"` | Sets a timed reminder |
| `"Remember that [fact]"` | Saves a note to memory |
| `"What do you remember"` | Recalls saved note |
| `"Play [song name]"` | Opens YouTube |
| `"Search for [topic]"` | Google search |
| `"Open [app]"` | Launches app (Spotify, Chrome, etc.) |
| `"Find [filename]"` | Searches Desktop/Downloads/Documents |
| `"Who was Einstein"` | Answered by Gemini AI |
| `"Go to sleep"` | Returns to idle mode |
| `"Exit"` / `"Quit"` | Shuts down Jarvis |

Press **Q** at any time as a keyboard shortcut to shut down.

---

## 🏗️ Build an EXE (optional)

```bash
pip install pyinstaller
pyinstaller Jarvis.spec
```

The executable is written to `dist/Jarvis.exe`. The `sounds/` folder is bundled automatically by the spec file.

> Note: The built EXE still reads `config.py` from the same directory — keep it alongside the EXE and never distribute it publicly.

---

## ⚙️ Customisation

| Where | What to change |
|---|---|
| `speak.py` → `VOICE` | Change TTS voice (see [Edge TTS voices](https://github.com/rany2/edge-tts#voices-list)) |
| `speech.py` → `r.energy_threshold` | Raise if mic picks up too much noise; lower if it misses you |
| `jarvis.py` → `WAKE_WORDS` | Add your own wake words |
| `commands.py` → `APPS` | Add more app shortcuts |
| `commands.py` → `SEARCH_PATHS` | Add more folders for file search |
| `jarvis.py` → `ALERT_COOLDOWN` | *(alarm.py)* Change reminder check interval |

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: pyaudio` | Install the prebuilt `.whl` (see step 2 above) |
| Speech not recognised | Check microphone permissions; adjust `energy_threshold` in `speech.py` |
| Gemini returns "overloaded" | Free-tier rate limit hit; wait a minute and try again |
| TTS produces no sound | Ensure `pygame.mixer` can access your audio device; check speakers |
| `config.py not found` warning | Copy `config.py.example` → `config.py` and add your key |
| App launches but no sound files | Create a `sounds/` folder; the app runs without them |
| `keyboard` requires admin | Run the terminal as Administrator on Windows |

---

## 📄 License

MIT — see `LICENSE` for details.
