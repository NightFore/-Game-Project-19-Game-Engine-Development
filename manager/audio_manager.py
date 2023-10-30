# audio_manager.py

import pygame
from manager.template_manager import TemplateManager

class AudioManager(TemplateManager):
    """
    AudioManager manages music and sound effects in the game.

    Attributes:
        Specific to AudioManager:
            - current_music_name (str): The name of the currently playing music.
            - music_volume (float): The volume of the currently playing music (0.0 to 1.0).
            - sound_volume (float): The volume for all loaded sound effects (0.0 to 1.0).
            - loop (int): The number of repetitions for playing music (-1 for looping indefinitely, 0 for no looping).

        Inherited from TemplateManager:
            - resources (dict): A dictionary containing loaded audio resources.
            - resource_types_to_load (list): A list of resource types to load for this manager.

    Methods:
    - Settings
        - set_music_volume(volume: float or int): Set the music volume.
        - set_sound_volume(volume: float or int): Set the volume for all loaded sound effects.
        - increment_music_volume(increment: float or int): Increment the music volume.
        - increment_sound_volume(increment: float or int): Increment the sound volume.
        - set_music_loop(loop: int): Set the loop behavior for playing music.

    - Management
        - play_music(name: str): Play the music associated with the given name.
        - play_sound(name: str): Play the sound effect associated with the given name.
        - stop_music(): Stop the currently playing music.
        - pause_music(): Pause the currently playing music.
        - unpause_music(): Unpause the currently paused music.
        - toggle_music(): Toggle the music state between paused and playing.

    - Validation
        - validate_volume(volume: float or int): Validate volume value (type and range).
        - validate_music_loop(loop: int): Validate the loop behavior for playing music.
        - validate_increment(increment: float or int): Validate the volume increment value (type).
        - validate_audio_resource(name: str, resource_type: str): Validate the existence of the audio resource.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries
        self.resources = {}

        # Define resource types to load for this manager
        self.resource_types_to_load = ["music", "sound"]

        # Initialize manager-related attributes
        self.current_music_name = None
        self.music_volume = 1.0
        self.sound_volume = 1.0
        self.loop = -1


    """
    Settings
        - set_music_volume
        - set_sound_volume
        - increment_music_volume
        - increment_sound_volume
        - set_music_loop
    """
    def set_music_volume(self, volume):
        """
        Set the music volume.

        Args:
            volume (float or int): The volume to set (ranging from 0.0 to 1.0).

        Raises:
            TypeError: If the volume is not a float or int.
            ValueError: If the volume is not within the valid range [0.0, 1.0].
        """
        # Validate the volume
        self.validate_volume(volume)

        # Set the volume for the currently playing music
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        """
        Set the volume for all loaded sound effects.

        Args:
            volume (float or int): The volume to set (ranging from 0.0 to 1.0).

        Raises:
            TypeError: If the volume is not a float or int.
            ValueError: If the volume is not within the valid range [0.0, 1.0].
        """
        # Validate the volume
        self.validate_volume(volume)

        # Set the volume for sound effects
        self.sound_volume = volume
        for sound in self.resources.values():
            sound.set_volume(self.sound_volume)

    def increment_music_volume(self, increment):
        """
        Increment the music volume.

        Args:
            increment (float or int): The amount to increment the volume (can be positive or negative).

        Raises:
            TypeError: If the increment is not a float or int.
        """
        # Validate the increment
        self.validate_increment(increment)

        # Set the volume for the currently playing music
        self.music_volume = max(0.0, min(1.0, self.music_volume + increment))
        self.set_music_volume(self.music_volume)

    def increment_sound_volume(self, increment):
        """
        Increment the sound volume.

        Args:
            increment (float or int): The amount to increment the volume (can be positive or negative).

        Raises:
            TypeError: If the increment is not a float or int.
        """
        # Validate the increment
        self.validate_increment(increment)

        # Set the volume for sound effects
        self.sound_volume = max(0.0, min(1.0, self.sound_volume + increment))
        self.set_sound_volume(self.sound_volume)

    def set_music_loop(self, loop):
        """
        Set the loop behavior for playing music.

        Args:
            loop (int): The number of repetitions. -1 for looping indefinitely, 0 for no looping.

        Raises:
            TypeError: If 'loop' is not an integer.
            ValueError: If 'loop' is not within the valid values (-1 or 0).
        """
        # Validate the loop behavior
        self.validate_music_loop(loop)

        # Set the loop behavior for playing music
        self.loop = loop


    """
    Management
        - play_music
        - play_sound
        - stop_music
        - pause_music
        - unpause_music
        - toggle_music
    """
    def play_music(self, name):
        """
        Play the music associated with the given name.

        Args:
            name (str): The name of the music to play.

        Raises:
            ValueError: If the specified 'name' is not found in the AudioManager's audio resources.
        """
        # Validate the audio resource existence
        self.validate_audio_resource(name, "music", self.resources)

        # Check if any music is currently playing
        current_music = pygame.mixer.music.get_busy()

        # Get the name of the currently playing music if there is any, else set it to None
        current_name = self.current_music_name if current_music else None

        # Check if the requested music is different from the currently playing one
        if current_name != name:
            # Load and play the new track
            pygame.mixer.music.load(self.resources[name])
            pygame.mixer.music.play(self.loop)
            self.current_music_name = name

    def play_sound(self, name):
        """
        Play the sound effect associated with the given name.

        Args:
            name (str): The name of the sound effect to play.

        Raises:
            ValueError: If the specified 'name' is not found in the AudioManager's audio resources.
        """
        # Validate the audio resource existence
        self.validate_audio_resource(name, "sound", self.resources)

        # Play the sound effect
        self.resources[name].play()

    @staticmethod
    def stop_music():
        """
        Stop the currently playing music.
        """
        pygame.mixer.music.stop()

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
    def toggle_music():
        """
        Toggle the music state between paused and playing.
        """
        if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() > 0:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()


    """
    Validation
        - validate_volume
        - validate_music_loop
        - validate_increment
        - validate_audio_resource
    """
    @staticmethod
    def validate_volume(volume):
        """
        Validate the volume value to ensure it's of the correct type and within the valid range [0.0, 1.0].

        Args:
            volume (float or int): The volume value to validate.

        Raises:
            TypeError: If the volume is not a float or int.
            ValueError: If the volume is not within the valid range [0.0, 1.0].
        """
        if not (isinstance(volume, int) or isinstance(volume, float)):
            raise TypeError("Volume must be an int or float.")
        if not (0.0 <= volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0.")

    @staticmethod
    def validate_increment(increment):
        """
        Validate that the volume increment is a float or int.

        Args:
            increment (float or int): The increment to be validated.

        Raises:
            TypeError: If the increment is not a float or int.
        """
        if not isinstance(increment, (float, int)):
            raise TypeError("Volume increment must be a float or int.")

    @staticmethod
    def validate_music_loop(loop):
        """
        Validate the loop behavior for playing music.

        Args:
            loop (int): The number of repetitions. -1 for looping indefinitely, 0 for no looping.

        Raises:
            TypeError: If 'loop' is not an integer.
            ValueError: If 'loop' is not within the valid values (-1 or 0).
        """
        if not isinstance(loop, int):
            raise TypeError("The 'loop' argument must be an integer.")
        if loop not in [-1, 0]:
            raise ValueError("The 'loop' argument must be -1 for looping indefinitely or 0 for no looping.")

    @staticmethod
    def validate_audio_resource(name, resource_type, resources):
        """
        Validate if the specified 'name' exists in the AudioManager's audio resources.

        Args:
            name (str): The name of the audio resource to validate.
            resource_type (str): The type of audio resource ("music" or "sound").
            resources (dict): The dictionary of audio resources managed by the AudioManager.

        Raises:
            ValueError: If the specified 'name' is not found in the AudioManager's audio resources.
        """
        if name not in resources:
            raise ValueError(f"{resource_type.capitalize()} '{name}' does not exist in the AudioManager's audio resources.")
