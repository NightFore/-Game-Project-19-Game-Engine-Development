# debug_audio_manager.py

import pygame

class DebugAudioManager:
    def __init__(self, audio_manager):
        self.audio_manager = audio_manager

        # Timer to track waiting intervals
        self.wait_timer = 0

        # Initial state is to play music and sound effects
        self.state = "play"

        # Set volume and loop
        self.audio_manager.set_sound_effect_volume(0.5)
        self.audio_manager.set_music_volume(0.3)
        self.audio_manager.set_music_loop(-1)

    def update(self):
        # Update the wait timer and change state accordingly
        self.wait_timer += 1
        if self.state == "play":
            # Play music and sound effect
            if self.wait_timer == 1:
                self.audio_manager.play_music("debug_music")
                self.audio_manager.play_sound_effect("debug_sound")

            # Pause music
            elif self.wait_timer == 60:
                self.audio_manager.pause_music()

            # Resume music
            elif self.wait_timer == 120:
                self.audio_manager.unpause_music()

            # Stop music
            elif self.wait_timer == 180:
                self.audio_manager.stop_music()
                self.state = "done"

    def draw(self):
        pass
