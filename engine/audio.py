# audio.py
import pygame
import os
import logging

# Constants
DEFAULT_VOLUME = 0.5
DEFAULT_MUSIC_VOLUME = 0.3
DEFAULT_SFX_VOLUME = 0.7
DEFAULT_VOICE_VOLUME = 0.5


class AudioManager:
    """
    AudioManager class handles all audio-related functionalities in the game.

    Attributes:
        config (dict): Configuration dictionary loaded from config.json.
        logger (logging.Logger): Logger instance for logging messages.

        Master Volume Controls:
        - master_volume (float): Master volume level for all audio (default: 0.5).
        - bgm_volume (float): Background music volume level (default: 0.3).
        - sfx_volume (float): Sound effects volume level (default: 0.7).
        - voice_volume (float): Voice clips volume level (default: 0.5).

        Asset Containers:
        - sound_effects (dict): Dictionary to store loaded sound effects.
        - music_tracks (dict): Dictionary to store loaded music tracks.
        - voice_clips (dict): Dictionary to store loaded voice clips.

        Playback State:
        - current_music_name (str or None): Name of currently playing music track.
        - current_voice_clip_name (str or None): Name of currently playing voice clip.
    """

    def __init__(self):
        """
        Initialize the AudioManager instance.
        """
        self.config = None
        self.logger = None

        self.master_volume = DEFAULT_VOLUME
        self.bgm_volume = DEFAULT_MUSIC_VOLUME
        self.sfx_volume = DEFAULT_SFX_VOLUME
        self.voice_volume = DEFAULT_VOICE_VOLUME

        self.sound_effects = {}
        self.music_tracks = {}
        self.voice_clips = {}

        self.current_music_name = None
        self.current_voice_clip_name = None

    def initialize(self, config, logger):
        """
        Initialize the AudioManager with configuration and logger.

        Args:
            config (dict): Configuration dictionary loaded from config.json.
            logger (logging.Logger): Logger instance for logging messages.
        """
        self.config = config
        self.logger = logger

        self.load_audio_settings()
        self.initialize_pygame()
        self.load_assets()
        self.logger.info("AudioManager initialized.")

    def load_audio_settings(self):
        """
        Load audio settings from the configuration dictionary.
        """
        if self.config:
            audio_config = self.config.get("audio", {})
            self.master_volume = audio_config.get("master_volume", DEFAULT_VOLUME)
            self.bgm_volume = audio_config.get("bgm_volume", DEFAULT_MUSIC_VOLUME)
            self.sfx_volume = audio_config.get("sfx_volume", DEFAULT_SFX_VOLUME)
            self.voice_volume = audio_config.get("voice_volume", DEFAULT_VOICE_VOLUME)
            self.logger.info("Audio settings loaded.")
        else:
            self.logger.warning("Configuration dictionary is not set.")

    def initialize_pygame(self):
        """
        Initialize Pygame mixer for sound playback.
        """
        pygame.mixer.pre_init(44100, -16, 2, 512)  # Initialize mixer settings
        pygame.mixer.init()
        self.logger.debug("Pygame mixer initialized.")

    def load_assets(self):
        """
        Load sound assets from the assets directory based on project structure.
        """
        assets_folder = "assets"
        for root, dirs, files in os.walk(assets_folder):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(".mp3") or file_path.endswith(".wav"):
                    if "bgm" in root:
                        self.music_tracks[os.path.splitext(file)[0]] = file_path
                    elif "sfx" in root:
                        self.sound_effects[os.path.splitext(file)[0]] = pygame.mixer.Sound(file_path)
                    elif "voice" in root:
                        self.voice_clips[os.path.splitext(file)[0]] = pygame.mixer.Sound(file_path)

    def play_sound_effect(self, effect_name):
        """
        Play a sound effect by name.

        Args:
            effect_name (str): Name of the sound effect to play.
        """
        if effect_name in self.sound_effects:
            self.sound_effects[effect_name].play()

    def play_music(self, track_name, loop=False):
        """
        Play a music track by name.

        Args:
            track_name (str): Name of the music track to play.
            loop (bool, optional): Whether to loop the music track. Default is False.
        """
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
        pygame.mixer.music.set_volume(self.master_volume)

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
        pygame.mixer.music.set_volume(self.bgm_volume)

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

    def get_voice_volume(self):
        """
        Get the current voice clips volume level.

        Returns:
            float: Current voice clips volume level.
        """
        return self.voice_volume
