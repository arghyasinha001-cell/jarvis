import sys
import keyboard
import threading
from speak import speak
from speech import listen
from commands import execute
from hum import start_hum, stop_hum
from alarm import start_alarm_thread
from helpers import resource_path
from playsound import playsound

WAKE_WORDS = ["jarvis", "jar", "jovis", "service", "travis"]
RUNNING    = False


def shutdown_system():
    global RUNNING
    RUNNING = False
    stop_hum()
    speak("System offline.")
    sys.exit(0)


def start_jarvis(gui_print=print):
    global RUNNING
    RUNNING = True

    def safe_print(text):
        gui_print(str(text))

    start_alarm_thread()
    keyboard.add_hotkey("q", shutdown_system)

    try:
        playsound(resource_path("sounds/startup.mp3"))
    except Exception:
        pass

    speak("System online.")
    safe_print("[SYSTEM] Online and listening...")

    while RUNNING:
        safe_print("[IDLE] Waiting for wake word...")
        query = listen()

        if query and any(alias in query for alias in WAKE_WORDS):
            safe_print("[ACTIVE] Wake word detected.")
            stop_hum()
            start_hum()
            speak("Yes?")
            stop_hum()

            active_mode = True
            while active_mode and RUNNING:
                command = listen()

                if not command:
                    safe_print("[IDLE] No command heard. Going idle.")
                    active_mode = False
                    continue

                safe_print(f"--> {command}")

                if "exit" in command or "quit" in command:
                    shutdown_system()
                    return

                if "go to sleep" in command:
                    speak("Going idle.")
                    active_mode = False
                    continue

                try:
                    execute(command, speak)
                except SystemExit:
                    # commands.py raises SystemExit on "shutdown" etc.
                    shutdown_system()
                    return
