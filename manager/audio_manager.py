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
        # Example dictionary for loading music and sound resources:
        audio_dict = {
            "background_music": {
                "type": "music",
                "filename": "background_music.mp3",
            },
            "explosion_sound": {
                "type": "sound",
                "filename": "explosion.wav",
            },
        }

        # Create an AudioManager instance and load resources:
        audio_manager = AudioManager()
        audio_manager.load_resources(audio_dict)

        # Play music and sound:
        audio_manager.play_music("background_music")
        audio_manager.play_sound("explosion_sound")

    Dependencies:
        - ResourceManager: A separate ResourceManager instance is required to load audio resources.

    Methods:
    - Resource Loading
        - load_resources_from_manager(resource_manager): Load music and sound resources from a ResourceManager.

    - Playback:
        - play_music(music_name): Play a music track by name.
        - play_sound(sound_name): Play a sound effect by name.

    - Settings:
        - set_music_volume(volume): Set the volume for the currently playing music.
        - set_sound_volume(volume): Set the volume for all loaded sound effects.
        - set_music_loop(loop): Set the loop behavior for playing music.
        - increment_sound_volume(increment): Increment the sound volume (0.0 to 1.0).
        - increment_music_volume(increment): Increment the music volume (0.0 to 1.0).

    - Validation Functions:
        - validate_volume(volume): Validate the volume for sound and music.
        - validate_music_loop(loop): Validate the loop behavior for playing music.
        - validate_increment(increment): Validate that the volume increment is a float or int.

    - Controls:
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
    Resource Loading
        - load_resources
    """
    def load_resources(self, resource_manager):
        """
        Load music and sound resources from a ResourceManager.

        Args:
            resource_manager (ResourceManager): The ResourceManager containing loaded resources.
        """
        self.musics = resource_manager.load_resources_from_manager("music")
        self.sounds = resource_manager.load_resources_from_manager("sound")


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
        - increment_sound_volume
        - increment_music_volume
    """
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
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

    def set_music_volume(self, volume):
        """
        Set the volume for the currently playing music.

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

        new_volume = self.sound_volume + increment
        self.set_sound_volume(max(0.0, min(1.0, new_volume)))

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

        new_volume = self.music_volume + increment
        self.set_music_volume(max(0.0, min(1.0, new_volume)))


    """
    Validation Functions
        - validate_volume
        - validate_music_loop
        - validate_increment
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
