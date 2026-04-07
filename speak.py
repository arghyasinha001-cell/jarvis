import asyncio
import edge_tts
import pygame
import os

# Initialise mixer here so speak.py works even if hum.py hasn't been imported yet
if not pygame.mixer.get_init():
    pygame.mixer.init()

from hum import stop_hum

# Voice options: "en-US-ChristopherNeural", "en-GB-RyanNeural"
VOICE       = "en-US-ChristopherNeural"
OUTPUT_FILE = "response.mp3"


def speak(text):
    stop_hum()
    print(f"JARVIS: {text}")

    async def _generate():
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(OUTPUT_FILE)

    try:
        asyncio.run(_generate())

        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()

    except Exception as e:
        print(f"[VOICE ERROR]: {e}")

    finally:
        # Always clean up the temp file, even if playback failed
        if os.path.exists(OUTPUT_FILE):
            try:
                os.remove(OUTPUT_FILE)
            except Exception:
                pass
