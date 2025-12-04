import pygame
from ..game_state import GameState
from ..logger import log

class SoundSystem:
    """Manages sound effects in the game."""

    def __init__(self):
        """Initializes the SoundSystem."""
        # Check if pygame mixer is initialized
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error as e:
                log.warning(f"Could not initialize pygame mixer: {e}")

        # Placeholder for sound loading
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        """Loads sound files. (Placeholders for now)"""
        # In a real implementation, we would load .wav or .ogg files here.
        # self.sounds["attack"] = pygame.mixer.Sound("assets/sounds/attack.wav")
        # For now, we will just use keys to acknowledge they exist.
        self.sounds["attack"] = None
        self.sounds["move"] = None
        self.sounds["select"] = None
        self.sounds["create"] = None
        self.sounds["death"] = None

    def play_sound(self, sound_name: str):
        """Plays a sound by name.

        Args:
            sound_name: The name of the sound to play.
        """
        if sound_name in self.sounds:
            log.info(f"[SoundSystem] Playing sound: {sound_name}")
            # if self.sounds[sound_name]:
            #     self.sounds[sound_name].play()
        else:
            log.warning(f"[SoundSystem] Sound not found: {sound_name}")

    def update(self, game_state: GameState):
        """Processes events from the game state to play sounds.

        Args:
            game_state: The current game state containing the event queue.
        """
        # Iterate over a copy or modify carefully if removing events
        # We assume this system runs last or near the end and can consume sound events?
        # Or we just iterate and consume only sound events.

        # We need to process events but not remove non-sound events if other systems use them.
        # However, typically events in a frame are consumed.
        # Let's assume for now we just process "sound" events and remove them from the queue?
        # Or better, just read them. But if we don't remove them, they play every frame.
        # So we must remove processed events.

        remaining_events = []
        for event in game_state.event_queue:
            if event["type"] == "sound":
                sound_name = event["data"].get("name")
                if sound_name:
                    self.play_sound(sound_name)
            else:
                remaining_events.append(event)

        # Replace the event queue with remaining events
        game_state.event_queue = remaining_events
