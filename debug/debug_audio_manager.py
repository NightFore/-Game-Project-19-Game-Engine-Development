# debug_audio_manager.py

import pygame
from os import path

def debug_audio_manager(audio_manager):
    # Play some music and sound effects
    audio_manager.play_music("debug_music")
    audio_manager.play_sound_effect("debug_sound")

    # Set volume and loop
    audio_manager.set_sound_effect_volume(0.5)
    audio_manager.set_music_volume(0.3)
    audio_manager.set_music_loop(-1)

    # Pause and resume music
    pygame.time.wait(1000)
    audio_manager.pause_music()
    pygame.time.wait(1000)
    audio_manager.unpause_music()

    # Stop music
    pygame.time.wait(2500)
    audio_manager.stop_music()
