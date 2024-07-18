# audio_manager.py

import pygame
import os
from typing import Optional
from engine.base_manager import BaseManager


class AudioManager(BaseManager):
    """
    AudioManager manages all audio-related functionalities in the game.

    Attributes:
        Common Attributes:
            - config (dict): Configuration dictionary loaded from config.json.
            - logger (logging.Logger): Logger instance for logging messages.

        Volume Attributes:
            - master_volume (float): Master volume level for all audio.
            - bgm_volume (float): Background music volume level.
            - sfx_volume (float): Sound effects volume level
            - voice_volume (float): Voice clips volume level.
            - mute (bool): Indicates if audio is muted.

        Audio Attributes:
            - library_path (str): Path to the audio library.
            - library_sfx (dict): Dictionary to store loaded sound effects.
            - library_bgm (dict): Dictionary to store loaded music tracks.
            - library_voice (dict): Dictionary to store loaded voice clips.

        Playback Attributes:
            - bgm_loop (int): Indicates if background music should loop (0 for no loop, -1 for infinite loop).
            - current_music_name (str): Name of currently playing music track.
            - current_voice_clip_name (str): Name of currently playing voice clip.
            - music_paused (bool): Indicates if the background music is currently paused.
    Methods:
        Instance Setup:
            - load_specific_components(): Loads specific audio components based on the configuration.
            - load_settings(): Loads settings from the configuration.
            - load_library(): Loads all audio assets from the specified library path.
            - load_audio_files(folder_path): Helper function to load audio files from a specified folder.

        Playback Control:
            - play_music(music_name): Plays the specified background music.
            - play_sound(sound_name): Plays the specified sound effect.
            - play_voice(voice_name): Plays the specified voice clip.
            - stop_music(): Stops the currently playing background music.
            - stop_sound(): Stops all currently playing sound effects.
            - stop_voice(): Stops all currently playing voice clips.
            - set_bgm_loop(loop): Set whether background music should loop.
            - toggle_music_playback(): Toggles between pausing and unpausing the music playback.

        Volume Control:
            - set_master_volume(volume): Sets the master volume level.
            - set_bgm_volume(volume): Sets the background music volume level.
            - set_sfx_volume(volume): Sets the sound effects volume level.
            - set_voice_volume(volume): Sets the voice clips volume level.
            - adjust_volume(volume_type, step): Adjusts the specified volume level by a step.
            - increment_volume(volume_type, step): Increments the specified volume level by a step.
            - decrement_volume(volume_type, step): Decrements the specified volume level by a step.
            - mute_audio(): Mutes all audio.
            - unmute_audio(): Unmutes all audio.
            - toggle_audio_mute(): Toggles between muting and unmuting the audio.
    """
    def __init__(self):
        """
        Initialize the AudioManager instance.
        """
        super().__init__()

        # Common Attributes
        self.config = {
            "volume_master": Optional[float],
            "volume_bgm": Optional[float],
            "volume_sfx": Optional[float],
            "volume_voice": Optional[float],
            "library_path": Optional[str],
            "mute": Optional[bool],
            "bgm_loop": Optional[int]
        }
        self.logger = None

        # Volume Attributes
        self.volume_master = Optional[float]
        self.volume_bgm = Optional[float]
        self.volume_sfx = Optional[float]
        self.volume_voice = Optional[float]
        self.mute = Optional[bool]

        # Audio Attributes
        self.library_path = Optional[str]
        self.library_sfx = Optional[dict]
        self.library_bgm = Optional[dict]
        self.library_voice = Optional[dict]

        # Playback Attributes
        self.bgm_loop = Optional[int]
        self.current_music_name = Optional[str]
        self.current_voice_clip_name = Optional[str]
        self.music_paused = False

    """
    Instance Setup
        - load_specific_components
        - load_settings
        - load_library
        - load_audio_files
    """
    def load_specific_components(self):
        """
        Load specific components based on the configuration.
        """
        # Set Manager attributes
        self.load_settings()
        self.load_library()

    def load_settings(self):
        """
        Load settings from configuration.
        """
        self.volume_master = self.config["volume_master"]
        self.volume_bgm = self.config["volume_bgm"]
        self.volume_sfx = self.config["volume_sfx"]
        self.volume_voice = self.config["volume_voice"]
        self.mute = self.config["mute"]
        self.bgm_loop = self.config["bgm_loop"]

    def load_library(self):
        """
        Load all audio assets from the specified library path.
        """
        # Set the library path from configuration
        self.library_path = self.config["library_path"]

        # Load background music (bgm)
        bgm_path = os.path.join(self.library_path, "bgm")
        self.library_bgm = self.load_audio_files(bgm_path)

        # Load sound effects (sfx)
        sfx_path = os.path.join(self.library_path, "sfx")
        self.library_sfx = self.load_audio_files(sfx_path)

        # Load voice clips (voice)
        voice_path = os.path.join(self.library_path, "voice")
        self.library_voice = self.load_audio_files(voice_path)

    def load_audio_files(self, folder_path):
        """
        Helper function to load audio files from a specified folder.

        Args:
            folder_path (str): Path to the folder containing audio files.

        Returns:
            dict: Dictionary mapping file names to loaded pygame.mixer.Sound objects.
        """
        audio_library = {}

        def is_valid_file(audio_filename, extensions):
            """Check if the filename ends with valid extensions."""
            return any(audio_filename.lower().endswith(ext) for ext in extensions)

        # Determine the category based on the folder name
        if "bgm" in folder_path.lower():
            category = "music"
        elif "sfx" in folder_path.lower() or "voice" in folder_path.lower():
            category = "sound"
        else:
            category = "unknown"

        # Check if the folder path exists
        if os.path.exists(folder_path):
            # Iterate over files in the folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                base_filename = os.path.splitext(filename)[0]
                try:
                    if category == "music" and is_valid_file(filename, (".wav", ".mp3")):
                        # Load as music
                        audio_library[base_filename] = file_path
                        self.log_debug(f"Loaded background music: {filename}")
                    elif category in "sound" and is_valid_file(filename, (".wav", ".mp3")):
                        # Load as sound
                        sound = pygame.mixer.Sound(file_path)
                        audio_library[base_filename] = sound
                        self.log_debug(f"Loaded {category} file: {filename}")
                    else:
                        # Log a warning for unsupported file extensions
                        self.log_warning(f"Ignoring file {filename} with unsupported extension in {folder_path}")

                except pygame.error as e:
                    self.log_error(f"Error loading audio file {filename}: {e}")

        # Log the number of files loaded
        num_files_loaded = len(audio_library)
        self.log_info(f"Loaded {num_files_loaded} audio files from {folder_path}")

        return audio_library

    """
    Playback Control
        - play_music
        - play_sound
        - play_voice
        - stop_music
        - stop_sound
        - stop_voice
        - set_bgm_loop
        - toggle_music_playback
    """
    def play_music(self, music_name):
        """
        Play the specified background music.

        Args:
            music_name (str): Name of the music track to play.
        """
        if music_name in self.library_bgm:
            if self.current_music_name == music_name:
                # Check if the music is already playing
                if self.music_paused:
                    # Resume the paused music playback
                    pygame.mixer.music.unpause()
                    self.music_paused = False
                    self.log_debug(f"Resumed background music: {music_name}")
                elif pygame.mixer.music.get_busy():
                    # Music is already playing
                    self.log_debug(f"{music_name} is already playing.")
            else:
                # Load and play the specified music track
                pygame.mixer.music.load(self.library_bgm[music_name])
                pygame.mixer.music.play(self.bgm_loop)
                self.current_music_name = music_name
                self.music_paused = False
                self.log_debug(f"Playing background music: {music_name}")
        else:
            # Log a warning if the specified music track is not found
            self.log_warning(f"Cannot find {music_name} in the background music library.")

    def play_sound(self, sound_name):
        """
        Play the specified sound effect.

        Args:
            sound_name (str): Name of the sound effect to play.
        """
        if sound_name in self.library_sfx:
            # Play the specified sound effect
            self.library_sfx[sound_name].play()
            self.log_debug(f"Playing sound effect: {sound_name}")
        else:
            # Log a warning if the specified sound effect is not found
            self.log_warning(f"Cannot find {sound_name} in the sound effects library.")

    def play_voice(self, voice_name):
        """
        Play the specified voice clip.

        Args:
            voice_name (str): Name of the voice clip to play.
        """
        if voice_name in self.library_voice:
            # Play the specified voice clip
            self.library_voice[voice_name].play()
            self.current_voice_clip_name = voice_name
            self.log_debug(f"Playing voice clip: {voice_name}")
        else:
            # Log a warning if the specified voice clip is not found
            self.log_warning(f"Cannot find {voice_name} in the voice clips library.")

    def stop_music(self):
        """
        Stop the currently playing background music.
        """
        if pygame.mixer.music.get_busy() or self.music_paused:
            pygame.mixer.music.stop()
            self.current_music_name = None
            self.music_paused = False
            self.log_debug("Stopped background music.")
        else:
            self.log_debug("No background music is currently playing.")

    def stop_sound(self):
        """
        Stop all currently playing sound effects.
        """
        for sound in self.library_sfx.values():
            sound.stop()
        self.log_debug("Stopped all sound effects.")

    def stop_voice(self):
        """
        Stop all currently playing voice clips.
        """
        for sound in self.library_voice.values():
            sound.stop()
        self.current_voice_clip_name = None
        self.log_debug("Stopped all voice clips.")

    def set_bgm_loop(self, loop):
        """
        Set whether background music should loop.

        Args:
            loop (int): Loop behavior for background music.
                - -1: Infinite loop.
                - 0: No loop.
                - Any positive integer: Number of times to loop the music.
        """
        previous_loop = self.bgm_loop
        self.bgm_loop = loop
        self.log_debug(f"Updated bgm_loop: {previous_loop} -> {loop}")

    def pause_music(self):
        """
        Pause the currently playing background music.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.music_paused = True
            self.log_debug(f"Paused background music: {self.current_music_name}")
        else:
            self.log_debug("No background music is currently playing to pause.")

    def toggle_music_playback(self):
        """
        Toggle between pausing and unpausing the music playback.
        """
        if self.music_paused:
            self.play_music(self.current_music_name)
        elif pygame.mixer.music.get_busy():
            self.pause_music()
        else:
            # No music is playing or paused
            self.log_warning("No background music is currently playing to pause or unpause.")

    """
    Volume Control:
        - set_master_volume
        - set_bgm_volume
        - set_sfx_volume
        - set_voice_volume
        - adjust_volume
        - increment_volume
        - decrement_volume
        - mute_audio
        - unmute_audio
        - toggle_audio_mute
    """
    def set_master_volume(self, volume):
        """
        Set the master volume level.

        Args:
            volume (float): Master volume level (0.0 to 1.0).
        """
        if 0.0 <= volume <= 1.0:
            # Update master volume attribute
            previous_volume = self.volume_master
            self.volume_master = round(volume, 2)

            # Set master volume for background music
            pygame.mixer.music.set_volume(self.volume_master * self.volume_bgm)

            # Adjust volumes for sound effects relative to master volume
            for sound in self.library_sfx.values():
                sound.set_volume(self.volume_master * self.volume_sfx)

            # Adjust volumes for voice clips relative to master volume
            for sound in self.library_voice.values():
                sound.set_volume(self.volume_master * self.volume_voice)

            self.log_debug(f"Updated volume_master: {previous_volume} -> {self.volume_master}")
        else:
            self.log_warning("Volume value must be between 0.0 and 1.0.")

    def set_bgm_volume(self, volume):
        """
        Set the background music volume level.

        Args:
            volume (float): Background music volume level (0.0 to 1.0).
        """
        if 0.0 <= volume <= 1.0:
            previous_volume = self.volume_bgm
            self.volume_bgm = round(volume, 2)
            pygame.mixer.music.set_volume(self.volume_master * self.volume_bgm)
            self.log_debug(f"Updated volume_bgm: {previous_volume} -> {self.volume_bgm}")
        else:
            self.log_warning("Volume value must be between 0.0 and 1.0.")

    def set_sfx_volume(self, volume):
        """
        Set the sound effects volume level.

        Args:
            volume (float): Sound effects volume level (0.0 to 1.0).
        """
        if 0.0 <= volume <= 1.0:
            previous_volume = self.volume_sfx
            self.volume_sfx = round(volume, 2)
            for sound in self.library_sfx.values():
                sound.set_volume(self.volume_master * self.volume_sfx)
            self.log_debug(f"Updated volume_sfx: {previous_volume} -> {self.volume_sfx}")
        else:
            self.log_warning("Volume value must be between 0.0 and 1.0.")

    def set_voice_volume(self, volume):
        """
        Set the voice clips volume level.

        Args:
            volume (float): Voice clips volume level (0.0 to 1.0).
        """
        if 0.0 <= volume <= 1.0:
            previous_volume = self.volume_sfx
            self.volume_sfx = round(volume, 2)
            for sound in self.library_voice.values():
                sound.set_volume(self.volume_master * self.volume_sfx)
            self.log_debug(f"Updated volume_voice: {previous_volume} -> {self.volume_sfx}")
        else:
            self.log_warning("Volume value must be between 0.0 and 1.0.")

    def adjust_volume(self, volume_type, step):
        """
        Adjust the specified volume level (master, bgm, sfx, or voice).

        Args:
            volume_type (str): Type of volume to adjust ("master", "bgm", "sfx", "voice").
            step (float): Step to increment or decrement the volume level.
        """
        # Valid volume types
        valid_volume_types = ["master", "bgm", "sfx", "voice"]

        # Check if the provided volume type is valid
        if volume_type not in valid_volume_types:
            self.log_warning(f"Invalid volume type: {volume_type}. Must be one of {valid_volume_types}.")
            return

        # Get current volume level
        current_volume = getattr(self, f'volume_{volume_type}')

        # Calculate new volume ensuring it's within 0.0 to 1.0
        new_volume = min(1.0, max(0.0, current_volume + step))

        # Set the new volume level
        getattr(self, f'set_{volume_type}_volume')(new_volume)

    def increment_volume(self, volume_type, step):
        """
        Increment the specified volume level (master, bgm, sfx, or voice).

        Args:
            volume_type (str): Type of volume to increment ("master", "bgm", "sfx", "voice").
            step (float): Step to increment the volume level.
        """
        self.adjust_volume(volume_type, step)

    def decrement_volume(self, volume_type, step):
        """
        Decrement the specified volume level (master, bgm, sfx, or voice).

        Args:
            volume_type (str): Type of volume to decrement ("master", "bgm", "sfx", "voice").
            step (float): Step to decrement the volume level.
        """
        self.adjust_volume(volume_type, -step)

    def mute_audio(self):
        """
        Mute all audio.
        """
        pygame.mixer.music.set_volume(0)
        for sound in self.library_sfx.values():
            sound.set_volume(0)
        for sound in self.library_voice.values():
            sound.set_volume(0)
        previous_mute = self.mute
        self.mute = True
        if self.mute != previous_mute:
            self.log_debug(f"Updated mute: {previous_mute} -> {self.mute}")

    def unmute_audio(self):
        """
        Unmute all audio.
        """
        pygame.mixer.music.set_volume(self.volume_master * self.volume_bgm)
        for sound in self.library_sfx.values():
            sound.set_volume(self.volume_master * self.volume_sfx)
        for sound in self.library_voice.values():
            sound.set_volume(self.volume_master * self.volume_voice)
        previous_mute = self.mute
        self.mute = False
        if self.mute != previous_mute:
            self.log_debug(f"Updated mute: {previous_mute} -> {self.mute}")

    def toggle_audio_mute(self):
        """
        Toggle between muting and unmuting the audio.
        """
        if self.mute:
            self.unmute_audio()
        else:
            self.mute_audio()
