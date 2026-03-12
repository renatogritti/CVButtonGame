import pygame
import os
from config import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        sound_dir = os.path.join('assets', 'sounds')
        
        # Mapping of keys to filenames for SFX
        sound_map = {
            'start': SOUND_START,
            'kick': SOUND_KICK,
            'goal': SOUND_GOAL,
            'hit_player': SOUND_HIT_PLAYER,
            'hit_wall': SOUND_HIT_WALL
        }

        for key, filename in sound_map.items():
            path = os.path.join(sound_dir, filename)
            try:
                if os.path.exists(path):
                    self.sounds[key] = pygame.mixer.Sound(path)
                else:
                    # Silently fail if file not present, user might still be adding them
                    self.sounds[key] = None
            except Exception as e:
                print(f"Error loading sound {path}: {e}")
                self.sounds[key] = None

    def play(self, key):
        sound = self.sounds.get(key)
        if sound:
            sound.play()

    def play_bgm(self):
        # Using music mixer for long loopable file
        path = os.path.join('assets', 'sounds', SOUND_BGM)
        try:
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.3) # Low volume as requested
                pygame.mixer.music.play(-1) # Loop forever
        except Exception as e:
            print(f"Error playing BGM {path}: {e}")

    def stop_bgm(self):
        pygame.mixer.music.stop()
