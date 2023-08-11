# audio_manager.py

import pygame
from os import path
from handler.resource_handler import load_resources, load_resource, validate_resource

class AudioManager:
    RESOURCE_MAPPING = {
        "music": {
            "folder": None,
            "load": "load_music",
            "format": {".mp3", ".ogg"}
        },
        "sound_effect": {
            "folder": None,
            "load": "load_sound",
            "format": {".wav"}
        },
    }

    def __init__(self):
        pygame.mixer.init()
        self.sound_effects = {}
        self.music = {}
        self.loop = -1
        self.current_music_name = None
        self.music_folder = None
        self.sound_folder = None

    """
    Resource Manager
        - set_resource_mapping
        - load_resources
        - load_resource
    """
    def set_resource_mapping(self, music_folder, sound_folder):
        self.RESOURCE_MAPPING["music"]["folder"] = music_folder
        self.RESOURCE_MAPPING["sound_effect"]["folder"] = sound_folder

    def load_resources(self, resources_dict):
        """Load multiple resources from a dictionary."""
        load_resources(self, resources_dict)

    def load_resource(self, resource_name, resource_data):
        """Load a resource based on its type using the appropriate loading method."""
        load_resource(self, resource_name, resource_data)

    """
    Loading
        - load_music
        - load_sound
    """
    def load_music(self, name, data):
        """
        Load a piece of music from the specified data.

        Args:
            name (str): The name to assign to the loaded music.
            data (dict): A dictionary containing music data.
        """
        music_path = data["file_path"]
        pygame.mixer.music.load(music_path)
        self.music[name] = music_path

    def load_sound(self, name, data):
        """
        Load a sound effect from the specified data.

        Args:
            name (str): The name to assign to the loaded sound effect.
            data (dict): A dictionary containing sound effect data.
        """
        sound_path = data["file_path"]
        sound = pygame.mixer.Sound(sound_path)
        self.sound_effects[name] = sound

    """
    Playback
        - play_music
        - play_sound_effect
    """
    def play_music(self, name):
        """
        Play the music associated with the given name.

        Args:
            name (str): The name of the music to play.
        """
        if name in self.music:
            # Check if any music is currently playing
            current_music = pygame.mixer.music.get_busy()

            # Get the name of the currently playing music if there is any, else set it to None
            current_name = self.current_music_name if current_music else None

            # Check if the requested music is different from the currently playing one
            if current_name != name:
                # Load and play the new track
                pygame.mixer.music.load(self.music[name])
                pygame.mixer.music.play(self.loop)
                self.current_music_name = name

    def play_sound_effect(self, name):
        """
        Play the sound effect associated with the given name.

        Args:
            name (str): The name of the sound effect to play.
        """
        if name in self.sound_effects:
            self.sound_effects[name].play()

    """
    Settings
        - set_sound_effect_volume
        - set_music_volume
        - set_music_loop
    """
    def set_sound_effect_volume(self, volume):
        """
        Set the volume for all loaded sound effects.

        Args:
            volume (float): The volume to set (ranging from 0.0 to 1.0).
        """
        for sound in self.sound_effects.values():
            sound.set_volume(volume)

    def set_music_volume(self, volume):
        """
        Set the volume for the currently playing music.

        Args:
            volume (float): The volume to set (ranging from 0.0 to 1.0).
        """
        pygame.mixer.music.set_volume(volume)

    def set_music_loop(self, loop):
        """
        Set the loop behavior for playing music.

        Args:
            loop (int): The number of repetitions. -1 for looping indefinitely, 0 for no looping.
        """
        self.loop = loop

    """
    Controls
        - pause_music
        - unpause_music
        - stop_music
    """
    def pause_music(self):
        """
        Pause the currently playing music.
        """
        pygame.mixer.music.pause()

    def unpause_music(self):
        """
        Unpause the currently paused music.
        """
        pygame.mixer.music.unpause()

    def stop_music(self):
        """
        Stop the currently playing music.
        """
        pygame.mixer.music.stop()

# Debugging section
if __name__ == "__main__":
    from debug.debug_audio_manager import debug_audio_manager

    # Create an instance of AudioManager
    audio_manager = AudioManager()

    # Debug the AudioManager by running the debug function
    debug_audio_manager(audio_manager)
