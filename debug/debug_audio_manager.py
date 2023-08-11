# debug_audio_manager.py

import pygame
from os import path

def debug_audio_manager(audio_manager):
    pygame.init()

    # Load the debug music and sound effect using absolute file paths.
    # path.dirname(__file__) gets the directory of the current script,
    # and path.join combines it with the filenames to create absolute file paths.
    # Since absolute paths are provided, they ignore the MUSIC_FOLDER and SOUND_FOLDER.
    music = {
        "debug_music": {
            "type": "music",
            "filename": path.join(path.dirname(__file__), "debug_music.mp3"),
        },
    }

    sound_effects = {
        "debug_sound": {
            "type": "sound_effect",
            "filename": path.join(path.dirname(__file__), "debug_sound.wav"),
        },
    }

    # Load the debug audios into the audio manager
    audio_manager.load_resources(music)
    audio_manager.load_resources(sound_effects)

    # Play some music and sound effects for testing
    audio_manager.play_music("debug_music")
    audio_manager.play_sound_effect("debug_sound")

    # Set volume and loop for testing
    audio_manager.set_sound_effect_volume(0.5)
    audio_manager.set_music_volume(0.3)
    audio_manager.set_music_loop(-1)

    # Pause and resume music for testing
    audio_manager.pause_music()
    pygame.time.wait(2000)
    audio_manager.unpause_music()

    # Stop music for testing
    pygame.time.wait(5000)
    audio_manager.stop_music()

    pygame.quit()
