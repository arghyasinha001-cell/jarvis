import pygame
from helpers import resource_path

pygame.mixer.init()

def start_hum():
    try:
        sound_file = resource_path("sounds/hum.mp3")
        # Check if music is already playing to avoid restarting it constantly
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play(loops=-1)
    except Exception as e:
        print(f"Hum Error: {e}")

def stop_hum():
    try:
        pygame.mixer.music.stop()
    except:
        pass