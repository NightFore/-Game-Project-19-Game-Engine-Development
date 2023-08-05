import pygame
from os import path

MUSIC_FOLDER = path.join("data", "music")
SOUND_FOLDER = path.join("data", "sound_effects")

class AudioManager:
    RESOURCE_MAPPING = {
        "sound_effects": "load_sound",
        "music": "load_music",
    }

    def __init__(self):
        pygame.mixer.init()
        self.sound_effects = {}
        self.music = {}
        self.loop = -1
        self.current_music_name = None

    """
    Loading
        - load_resources
        - load_music
        - load_sound
    """
    def load_resources(self, resource_dict, resource_type):
        """
        Load multiple resources of a given type from a dictionary.

        Args:
            resource_dict (dict): A dictionary containing resource names as keys and file paths as values.
            resource_type (str): The type of resources being loaded ("sound_effects" or "music").
        """
        load_method_name = self.RESOURCE_MAPPING.get(resource_type)
        if load_method_name is not None:
            load_method = getattr(self, load_method_name)
        else:
            raise ValueError("Invalid resource type")

        for name, filename in resource_dict.items():
            load_method(name, filename)

    def load_music(self, name, filename):
        """
        Load a piece of music from the specified file.

        Args:
            name (str): The name to assign to the loaded music.
            filename (str): The filename of the music to load.
        """
        file_path = path.join(MUSIC_FOLDER, filename)
        try:
            self.music[name] = file_path
            pygame.mixer.music.load(file_path)
        except pygame.error:
            print(f"Error loading music: {filename}")

    def load_sound(self, name, filename):
        """
        Load a sound effect from the specified file.

        Args:
            name (str): The name to assign to the loaded sound effect.
            filename (str): The filename of the sound effect to load.
        """
        file_path = path.join(SOUND_FOLDER, filename)
        try:
            sound = pygame.mixer.Sound(file_path)
            self.sound_effects[name] = sound
        except pygame.error:
            print(f"Error loading sound effect: {filename}")

    """
    Play
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
            current_music = pygame.mixer.music.get_busy()
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

audio_manager = AudioManager()

if __name__ == "__main__":
    from debug.debug_audio_manager import debug

    # Create an instance of AudioManager
    audio_manager = AudioManager()

    # Debug the AudioManager by running the debug function
    debug(audio_manager)
