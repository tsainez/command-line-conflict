import pygame
from pathlib import Path

class SoundSystem:
    """Handles playing sounds and music."""

    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds = {}
            self.sound_path = Path(__file__).resolve().parent.parent / "sounds"

            # Load sound effects
            self._load_sound("gunshot", "gunshot.wav")
            self._load_sound("explosion", "explosion.wav")

            # Load background music
            music_file = self.sound_path / "music.ogg"
            if music_file.exists():
                pygame.mixer.music.load(str(music_file))
            else:
                print(f"Warning: Music file not found at {music_file}")

        except pygame.error as e:
            print(f"Error initializing sound system: {e}")
            self.sounds = None
            pygame.mixer.quit()

    def _load_sound(self, name: str, filename: str):
        """Helper to load a single sound effect."""
        if not pygame.mixer.get_init():
            return

        filepath = self.sound_path / filename
        if filepath.exists():
            self.sounds[name] = pygame.mixer.Sound(str(filepath))
        else:
            print(f"Warning: Sound file not found at {filepath}")

    def play_music(self, loops=-1):
        """Plays the background music."""
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy() == 0:
            pygame.mixer.music.play(loops)

    def play_sound(self, name: str):
        """Plays a sound effect by name."""
        if pygame.mixer.get_init() and name in self.sounds:
            self.sounds[name].play()
