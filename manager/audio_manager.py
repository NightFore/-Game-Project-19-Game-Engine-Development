# audio_manager.py

import pygame

class AudioManager:
    """
    AudioManager handles music and sound effects in the game.

    Attributes:
        loop (int): The number of repetitions for music (-1 for looping indefinitely, 0 for no looping).
        current_music_name (str): The name of the currently playing music.
        musics (dict): A dictionary containing loaded music tracks.
        sounds (dict): A dictionary containing loaded sound effects.
        sound_volume (float): The volume level for all loaded sound effects (ranging from 0.0 to 1.0).
        music_volume (float): The volume level for the currently playing music (ranging from 0.0 to 1.0).

    Example:
        First, define a ResourceManager and load audio resources into it.
        Then, create an AudioManager, load audio resources from the ResourceManager, and play background music.

        audio_manager = AudioManager()
        audio_manager.load_resources_from_manager(resource_manager)
        audio_manager.play_music("background_music")

    Dependencies:
        - ResourceManager: A separate ResourceManager instance is required to load audio resources.

    Methods:
        - init_manager: Initialize the AudioManager.
        - load_resources_from_manager(resource_manager): Load music and sound resources from a ResourceManager.
        - play_music(music_name): Play a music track by name.
        - play_sound(sound_name): Play a sound effect by name.
        - set_sound_volume(volume): Set the volume for all loaded sound effects.
        - set_music_volume(volume): Set the volume for the currently playing music.
        - set_music_loop(loop): Set the loop behavior for playing music.
        - pause_music(): Pause the currently playing music.
        - resume_music(): Resume the paused music.
        - stop_music(): Stop playing the current music.
    """
    def __init__(self):
        pygame.mixer.quit()
        pygame.mixer.init()
        self.musics = {}
        self.sounds = {}
        self.current_music_name = None
        self.music_volume = 1.0
        self.sound_volume = 1.0
        self.loop = -1

    """
    Resources
        - load_resources_from_manager    
    """
    def load_resources_from_manager(self, resource_manager):
        """
        Load music and sound resources from a ResourceManager.

        Args:
            resource_manager (ResourceManager): The ResourceManager containing loaded resources.
        """
        # Create a temporary dictionary to track already loaded resources
        loaded_resources = {}

        # Add existing resources to the temporary dictionary
        loaded_resources.update(self.musics)
        loaded_resources.update(self.sounds)

        # Iterate through the resources in the ResourceManager
        for resource_name, resource in resource_manager.resources["music"].items():
            # Check if the resource has not been loaded already to avoid duplicates
            if resource_name not in loaded_resources:
                self.musics[resource_name] = resource

        for resource_name, resource in resource_manager.resources["sound"].items():
            if resource_name not in loaded_resources:
                self.sounds[resource_name] = resource

    """
    Playback
        - play_music
        - play_sound
    """
    def play_music(self, name):
        """
        Play the music associated with the given name.

        Args:
            name (str): The name of the music to play.

        Raises:
            ValueError: If the specified 'name' is not found in the AudioManager's music collection.
        """
        print(self.musics, self.sounds)
        if name in self.musics:
            # Check if any music is currently playing
            current_music = pygame.mixer.music.get_busy()

            # Get the name of the currently playing music if there is any, else set it to None
            current_name = self.current_music_name if current_music else None

            # Check if the requested music is different from the currently playing one
            if current_name != name:
                # Load and play the new track
                pygame.mixer.music.load(self.musics[name])
                pygame.mixer.music.play(self.loop)
                self.current_music_name = name
        else:
            raise ValueError(f"Music '{name}' does not exist in the AudioManager's music collection.")

    def play_sound(self, name):
        """
        Play the sound effect associated with the given name.

        Args:
            name (str): The name of the sound effect to play.

        Raises:
            ValueError: If the specified 'name' is not found in the AudioManager's sound collection.
        """
        if name in self.sounds:
            self.sounds[name].play()
        else:
            raise ValueError(f"Sound '{name}' does not exist in the AudioManager's sound collection.")

    """
    Settings
        - set_music_volume
        - set_sound_volume
        - set_music_loop
    """
    def set_music_volume(self, volume):
        """
        Set the volume for the currently playing music.

        Args:
            volume (float or int): The volume to set (ranging from 0.0 to 1.0).

        Raises:
            ValueError: If the volume is not a float or int, or if it's not within the valid range [0.0, 1.0].
        """
        if (isinstance(volume, int) or isinstance(volume, float)) and not(0 <= volume <= 1):
            raise ValueError("Volume must be a float or int between 0.0 and 1.0")

        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        """
        Set the volume for all loaded sound effects.

        Args:
            volume (float or int): The volume to set (ranging from 0.0 to 1.0).

        Raises:
            ValueError: If the volume is not a float or int, or if it's not within the valid range [0.0, 1.0].
        """
        print(volume, isinstance(volume, int), isinstance(volume, float), 0 <= volume <= 1, (isinstance(volume, int) or isinstance(volume, float)) and 0 <= volume <= 1)
        if (isinstance(volume, int) or isinstance(volume, float)) and not(0 <= volume <= 1):
            raise ValueError("Volume must be a int or float between 0.0 and 1.0")

        self.sound_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

    def set_music_loop(self, loop):
        """
        Set the loop behavior for playing music.

        Args:
            loop (int): The number of repetitions. -1 for looping indefinitely, 0 for no looping.
        """
        if not isinstance(loop, int) or (loop != -1 and loop != 0):
            raise ValueError("The 'loop' argument must be an integer (-1 for looping indefinitely, 0 for no looping).")
        else:
            self.loop = loop

    """
    Controls
        - pause_music
        - unpause_music
        - stop_music
    """
    @staticmethod
    def pause_music():
        """
        Pause the currently playing music.
        """
        pygame.mixer.music.pause()

    @staticmethod
    def unpause_music():
        """
        Unpause the currently paused music.
        """
        pygame.mixer.music.unpause()

    @staticmethod
    def stop_music():
        """
        Stop the currently playing music.
        """
        pygame.mixer.music.stop()
