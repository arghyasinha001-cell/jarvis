import os
import psutil
import datetime
import pyautogui
import pywhatkit
from history import log
from memory import load, save
from ai import ask_ai
from alarm import set_alarm
from helpers import resource_path
from playsound import playsound

memory = load()

SEARCH_PATHS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
]

APPS = {
    "spotify":    "spotify",
    "notepad":    "notepad",
    "calculator": "calc",
    "chrome":     "chrome",
    "code":       "code",
}


def find_file(name):
    print(f"[INFO] Searching for: {name}")
    for path in SEARCH_PATHS:
        for root, dirs, files in os.walk(path):
            for file in files:
                if name in file.lower():
                    return os.path.join(root, file)
    return None


def execute(query, speak):
    log(query)

    # ── 1. TIME & DATE ────────────────────────────────────────
    # These two are handled with standalone `if` statements so
    # "what is the date and time" triggers both. Everything else
    # is a clean elif chain so overlapping keywords (e.g. "time"
    # inside a reminder phrase) never short-circuit other commands.
    handled = False

    if "date" in query:
        speak(datetime.datetime.now().strftime("Today's date is %B %d, %Y"))
        handled = True
    if "time" in query and "remind" not in query and "timer" not in query:
        speak(datetime.datetime.now().strftime("The time is %I:%M %p"))
        handled = True

    if handled:
        return

    # ── 2. SYSTEM ─────────────────────────────────────────────
    if "cpu" in query:
        speak(f"CPU usage is {psutil.cpu_percent()} percent")

    elif "battery" in query:
        try:
            b = psutil.sensors_battery()
            if b:
                speak(f"Battery is at {int(b.percent)} percent")
            else:
                speak("No battery sensor found on this device.")
        except Exception:
            speak("I could not read the battery sensor.")

    elif "screenshot" in query:
        speak("Taking screenshot.")
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        speak(f"Saved as {filename}.")

    elif "volume up" in query:
        pyautogui.press("volumeup", presses=5)
        speak("Volume increased.")

    elif "volume down" in query:
        pyautogui.press("volumedown", presses=5)
        speak("Volume decreased.")

    elif "mute" in query:
        pyautogui.press("volumemute")
        speak("Muted.")

    # ── 3. ALARM / REMINDER ───────────────────────────────────
    elif "remind me" in query or "alarm" in query or "reminder" in query:
        speak("Setting reminder.")
        success, response = set_alarm(query)
        speak(response)

    # ── 4. MEMORY ─────────────────────────────────────────────
    elif "remember that" in query:
        fact = query.replace("remember that", "").strip()
        if fact:
            memory["note"] = fact
            save(memory)
            speak("I will remember that.")
        else:
            speak("What would you like me to remember?")

    elif "what do you remember" in query or "what did you remember" in query:
        note = memory.get("note")
        speak(f"You told me: {note}" if note else "I don't have anything stored yet.")

    # ── 5. MEDIA & WEB ───────────────────────────────────────
    elif "play" in query and "youtube" not in query:
        song = query.replace("play", "").strip()
        if song:
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
        else:
            speak("What would you like me to play?")

    elif "search for" in query or "google" in query:
        topic = query.replace("search for", "").replace("google", "").strip()
        if topic:
            speak(f"Searching Google for {topic}.")
            pywhatkit.search(topic)
        else:
            speak("What would you like me to search?")

    # ── 6. OPEN APP ───────────────────────────────────────────
    elif "open" in query:
        app_name = query.replace("open", "").strip()
        if app_name in APPS:
            speak(f"Opening {app_name}.")
            os.system(f"start {APPS[app_name]}")
        else:
            try:
                os.system(f"start {app_name}")
                speak(f"Opening {app_name}.")
            except Exception:
                speak(f"I don't know how to open {app_name}.")

    # ── 7. FILE SEARCH ────────────────────────────────────────
    elif "find" in query:
        filename = query.replace("find", "").strip()
        if filename:
            result = find_file(filename)
            if result:
                os.startfile(result)
                speak(f"Opening {filename}.")
            else:
                speak(f"I couldn't find a file matching {filename}.")
        else:
            speak("What file should I look for?")

    # ── 8. SHUTDOWN ───────────────────────────────────────────
    elif any(w in query for w in ("exit", "quit", "shutdown", "self destruct")):
        speak("Goodbye.")
        try:
            playsound(resource_path("sounds/shutdown.mp3"))
        except Exception:
            pass
        raise SystemExit(0)   # cleaner than bare exit(); caught by jarvis.py

    # ── 9. AI FALLBACK ────────────────────────────────────────
    else:
        speak("Thinking.")
        answer = ask_ai(query)
        speak(answer)
