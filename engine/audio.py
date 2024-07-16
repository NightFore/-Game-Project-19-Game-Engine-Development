import pygame
import os
import json
import logging

# Constants
DEFAULT_VOLUME = 0.5
DEFAULT_MUSIC_VOLUME = 0.3
DEFAULT_SFX_VOLUME = 0.7
DEFAULT_VOICE_VOLUME = 0.5


class SoundManager:
    """
    SoundManager class handles all audio-related functionalities in the game.

    Attributes:
        config_path (str): Path to the configuration file (config.json).
        config_defaults (dict): Dictionary containing default values for audio configuration.

        Master Volume Controls:
        - master_volume (float): Master volume level for all audio (default: 0.5).
        - bgm_volume (float): Background music volume level (default: 0.3).
        - sfx_volume (float): Sound effects volume level (default: 0.7).
        - voice_volume (float): Voice clips volume level (default: 0.5).

        Asset Containers:
        - sound_effects (dict): Dictionary to store loaded sound effects.
        - music_tracks (dict): Dictionary to store loaded music tracks.
        - voice_clips (dict): Dictionary to store loaded voice clips.

    Methods:
        Initialization:
        - load_config(): Loads audio settings from config.json or uses defaults.
        - initialize_pygame(): Initializes Pygame mixer for sound playback.
        - load_assets(): Loads sound assets from the assets directory.

        Playback Controls:
        - play_sound_effect(effect_name): Plays a sound effect by name.
        - play_music(track_name, loop): Plays music track by name.
        - play_voice_clip(clip_name): Plays a voice clip by name.
        - stop_music(): Stops the currently playing music.
        - pause_music(): Pauses the currently playing music.
        - unpause_music(): Unpauses the currently paused music.

        Volume Controls:
        - set_master_volume(volume): Sets the master volume for all audio.
        - get_master_volume(): Retrieves the current master volume.
        - get_bgm_volume(): Retrieves the current background music volume.
        - get_sfx_volume(): Retrieves the current sound effects volume.
        - get_voice_volume(): Retrieves the current voice clips volume.

        Configuration Management:
        - save_config(): Saves the current audio settings to config.json.
    """

    def __init__(self, config_path):
        """
        Initialize the SoundManager instance.

        Args:
            config_path (str): Path to the configuration file (config.json).
        """
        self.config_path = config_path
        self.config_defaults = {
            "audio": {
                "master_volume": DEFAULT_VOLUME,
                "bgm_volume": DEFAULT_MUSIC_VOLUME,
                "sfx_volume": DEFAULT_SFX_VOLUME,
                "voice_volume": DEFAULT_VOICE_VOLUME
            }
        }
        self.logger = logging.getLogger(__name__)
        self.master_volume = DEFAULT_VOLUME
        self.bgm_volume = DEFAULT_MUSIC_VOLUME
        self.sfx_volume = DEFAULT_SFX_VOLUME
        self.voice_volume = DEFAULT_VOICE_VOLUME

        self.sound_effects = {}
        self.music_tracks = {}
        self.voice_clips = {}

        self.current_music_name = None
        self.current_voice_clip_name = None

        self.load_config()
        self.initialize_pygame()
        self.load_assets()
        self.logger.info("SoundManager initialized.")

    def load_config(self):
        """
        Load audio settings from the configuration file (config.json).
        If the file doesn't exist or settings are missing, use default values.
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
                audio_config = config_data.get("audio", {})
                self.master_volume = audio_config.get("master_volume", self.config_defaults["audio"]["master_volume"])
                self.bgm_volume = audio_config.get("bgm_volume", self.config_defaults["audio"]["bgm_volume"])
                self.sfx_volume = audio_config.get("sfx_volume", self.config_defaults["audio"]["sfx_volume"])
                self.voice_volume = audio_config.get("voice_volume", self.config_defaults["audio"]["voice_volume"])
                self.logger.info(f"Config loaded from '{self.config_path}'")
        else:
            self.master_volume = self.config_defaults["audio"]["master_volume"]
            self.bgm_volume = self.config_defaults["audio"]["bgm_volume"]
            self.sfx_volume = self.config_defaults["audio"]["sfx_volume"]
            self.voice_volume = self.config_defaults["audio"]["voice_volume"]
            self.logger.warning(f"Config file '{self.config_path}' not found. Using default audio settings.")

    def initialize_pygame(self):
        """
        Initialize Pygame mixer for sound playback.
        """
        pygame.mixer.pre_init(44100, -16, 2, 512)  # Initialize mixer settings
        pygame.mixer.init()
        self.logger.debug("Pygame mixer initialized.")

    def load_assets(self):
        """
        Load sound assets from the assets directory.
        """
        # Implement loading sound effects, music tracks, and voice clips as per your project structure
        # Example: self.sound_effects = load_sound_effects()
        pass

    def play_sound_effect(self, effect_name):
        """
        Play a sound effect by name.

        Args:
            effect_name (str): Name of the sound effect to play.
        """
        # Implement playing sound effects from the loaded sound_effects dictionary
        if effect_name in self.sound_effects:
            self.sound_effects[effect_name].play()

    def play_music(self, track_name, loop=False):
        """
        Play a music track by name.

        Args:
            track_name (str): Name of the music track to play.
            loop (bool, optional): Whether to loop the music track. Default is False.
        """
        # Implement playing music tracks from the loaded music_tracks dictionary
        if track_name in self.music_tracks:
            pygame.mixer.music.load(self.music_tracks[track_name])
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music_name = track_name

    def play_voice_clip(self, clip_name):
        """
        Play a voice clip by name.

        Args:
            clip_name (str): Name of the voice clip to play.
        """
        # Implement playing voice clips from the loaded voice_clips dictionary
        if clip_name in self.voice_clips:
            self.voice_clips[clip_name].play()

    def stop_music(self):
        """
        Stop the currently playing music.
        """
        pygame.mixer.music.stop()
        self.current_music_name = None

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

    def set_master_volume(self, volume):
        """
        Set the master volume level for all audio.

        Args:
            volume (float): Master volume level (0.0 to 1.0).
        """
        self.master_volume = max(0.0, min(1.0, volume))
        # Implement setting master volume for all audio using Pygame mixer

    def get_master_volume(self):
        """
        Get the current master volume level.

        Returns:
            float: Current master volume level.
        """
        return self.master_volume

    def set_bgm_volume(self, volume):
        """
        Set the background music volume level.

        Args:
            volume (float): Background music volume level (0.0 to 1.0).
        """
        self.bgm_volume = max(0.0, min(1.0, volume))
        # Implement setting background music volume using Pygame mixer

    def get_bgm_volume(self):
        """
        Get the current background music volume level.

        Returns:
            float: Current background music volume level.
        """
        return self.bgm_volume

    def set_sfx_volume(self, volume):
        """
        Set the sound effects volume level.

        Args:
            volume (float): Sound effects volume level (0.0 to 1.0).
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        # Implement setting sound effects volume using Pygame mixer

    def get_sfx_volume(self):
        """
        Get the current sound effects volume level.

        Returns:
            float: Current sound effects volume level.
        """
        return self.sfx_volume

    def set_voice_volume(self, volume):
        """
        Set the voice clips volume level.

        Args:
            volume (float): Voice clips volume level (0.0 to 1.0).
        """
        self.voice_volume = max(0.0, min(1.0, volume))
        # Implement setting voice clips volume using Pygame mixer

    def get_voice_volume(self):
        """
        Get the current voice clips volume level.

        Returns:
            float: Current voice clips volume level.
        """
        return self.voice_volume

    def save_config(self):
        """
        Save the current audio settings to the configuration file (config.json).
        """
        config_data = {
            "audio": {
                "master_volume": self.master_volume,
                "bgm_volume": self.bgm_volume,
                "sfx_volume": self.sfx_volume,
                "voice_volume": self.voice_volume
            }
        }
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        self.logger.info(f"Saved audio configuration to '{self.config_path}'")
