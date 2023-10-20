import pygame
from pygame.locals import *

import random
from os import path

from manager.audio_manager import AudioManager
from manager.button_manager import ButtonManager
from manager.graphic_manager import GraphicManager
from manager.resource_manager import ResourceManager
from manager.scene_manager import SceneManager
from manager.font_manager import FontManager
from manager.window_manager import WindowManager

from data.constant_data import PROJECT_TITLE, SCREEN_SIZE, FPS
from data.resource_data import DICT_AUDIO, DICT_FONT, DICT_GRAPHIC, DICT_SCENE

from debug.debug_audio_manager import DebugAudioManager
from debug.debug_graphic_manager import DebugGraphicManager
from debug.debug_data import DEBUG_DICT_AUDIO, DEBUG_DICT_FONT, DEBUG_DICT_GRAPHIC, DEBUG_DICT_SCENE

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        random.seed()
        self.total_play_time = 0
        self.clock = pygame.time.Clock()
        self.playing = True
        self.paused = False
        self.debug_mode = True
        self.setup_game()
        self.load_game()
        self.start_game()


    """
    Setup
        - setup_folders
        - setup_dict
        - setup_managers
        - setup_managers_settings
        - setup_display
    """
    def setup_game(self):
        """
        Initial setup for the game.
        """
        self.setup_folders()
        self.setup_dict()
        self.setup_managers()
        self.setup_managers_settings()
        self.setup_display()

    def setup_folders(self):
        """
        Configure folder paths based on debug mode.
        """
        self.game_folder = path.dirname(__file__)

        # Define the base resources folder
        base_folder = "resources" if not self.debug_mode else path.join("debug", "debug_resources")
        self.resources_folder = path.join(self.game_folder, base_folder)

        # Define individual resource folders
        self.font_folder = path.join(self.resources_folder, "font")
        self.graphic_folder = path.join(self.resources_folder, "graphic")
        self.music_folder = path.join(self.resources_folder, "music")
        self.sound_folder = path.join(self.resources_folder, "sound")

        # Define resource type folders (see ResourceManagers)
        self.resource_type_folders = {
            "music": self.music_folder,
            "sound": self.sound_folder,
            "image": self.graphic_folder,
            "image_sequence": self.graphic_folder,
            "font": self.font_folder,
        }

    def setup_dict(self):
        """
        Configure game dictionaries based on debug mode.
        """
        if not self.debug_mode:
            # Use regular dictionaries for non-debug mode.
            self.audio_dict = DICT_AUDIO
            self.font_dict = DICT_FONT
            self.graphic_dict = DICT_GRAPHIC
            self.scene_dict = DICT_SCENE
        else:
            # Use debug dictionaries for debug mode.
            self.audio_dict = DEBUG_DICT_AUDIO
            self.font_dict = DEBUG_DICT_FONT
            self.graphic_dict = DEBUG_DICT_GRAPHIC
            self.scene_dict = DEBUG_DICT_SCENE

    def setup_managers(self):
        """
        Create and configure game managers.
        """
        # Create individual variables for managers
        self.audio_manager = AudioManager()
        self.button_manager = ButtonManager()
        self.graphic_manager = GraphicManager()
        self.resource_manager = ResourceManager()
        self.scene_manager = SceneManager()
        self.font_manager = FontManager()
        self.window_manager = WindowManager()

        # Regroup managers under a single variable
        self.managers = {
            "audio_manager": self.audio_manager,
            "button_manager": self.button_manager,
            "graphic_manager": self.graphic_manager,
            "resource_manager": self.resource_manager,
            "scene_manager": self.scene_manager,
            "font_manager": self.font_manager,
            "window_manager": self.window_manager
        }

    def setup_managers_settings(self):
        """
        Configure game managers and their settings.
        """
        # Set resource folders for the ResourceManager
        self.resource_manager.set_resource_folders(self.resource_type_folders)

        # Set managers for the SceneManager
        self.scene_manager.set_managers(self.managers)

    def setup_display(self):
        """
        Configure game display settings.
        """
        self.project_title = PROJECT_TITLE
        self.FPS = FPS
        self.screen_size = self.screen_width, self.screen_height = SCREEN_SIZE
        self.gameDisplay = self.window_manager.create_window_instance(self.project_title, self.screen_size)


    """
    Loading
        - load_managers_resources
        - load_scenes
    """
    def load_game(self):
        """
        Initial loading for the game.
        """
        self.load_managers_resources()
        self.load_scenes()

    def load_managers_resources(self):
        """
        Load resources for game managers.
        """
        # Load resources using the ResourceManager
        self.resource_manager.load_resources(self.audio_dict)
        self.resource_manager.load_resources(self.graphic_dict)

        # Load resources for other dependent managers
        self.audio_manager.load_resources(self.resource_manager)
        self.graphic_manager.load_resources(self.resource_manager)

    def load_scenes(self):
        """
        Load game scenes.
        """
        self.scene_manager.load_scenes_from_directory("scenes")
        self.scene_manager.load_scenes_params(self.scene_dict)


    """
    Startup
        - start_managers
        - start_debug_mode
    """
    def start_game(self):
        """
        Initialize game startup procedures.
        """
        self.start_managers()
        self.start_debug_mode()

    def start_managers(self):
        """
        Initialize game managers for the initial scene.
        """
        # Set the initial scene to "MainMenuScene"
        self.scene_manager.set_scene("MainMenuScene")

    def start_debug_mode(self):
        """
        Initialize debug mode and create debug update and draw lists.
        """
        # Create empty debug update and draw lists
        self.debug_updates = []
        self.debug_draws = []

        # Initialize debug handlers
        debug_handlers = [
            DebugAudioManager(self.audio_manager),
            DebugGraphicManager(self.graphic_manager, self.window_manager)]

        for debug_handler in debug_handlers:
            # Add debug update and draw functions to the lists
            self.debug_updates.append(debug_handler.update)
            self.debug_draws.append(debug_handler.draw)


    """
    Game Loop
        - run
        - events
        - update
        - draw
        - quit_game
    """
    def run(self):
        while self.playing:
            self.dt = self.clock.tick(self.FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        self.quit_game()

    def events(self):
        """Click: None, Left, Middle, Right, Scroll Up, Scroll Down"""
        self.click = [None, False, False, False, False, False]

        """Handle Events"""
        self.event = pygame.event.get()
        for event in self.event:
            # Handle window resizing event
            if event.type == VIDEORESIZE:
                self.window_manager.resize()

            # Check for keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                elif event.key == pygame.K_F4:
                    self.window_manager.update_display_mode(toggle_zoom=True)
                elif event.key == pygame.K_F11:
                    self.window_manager.update_display_mode(toggle_fullscreen=True)

            # Handle quit event
            if event.type == pygame.QUIT:
                self.quit_game()

    """
    Update
        - calculate_total_play_time
    """
    def update(self):
        # Update game time if the game is not paused
        self.calculate_total_play_time()

        # Update the scene manager with the time elapsed since the last update
        self.scene_manager.update(self.dt)

        # Debug: If debug mode is enabled, perform debug operations
        if self.debug_mode:
            for debug_update_func in self.debug_updates:
                debug_update_func()

        # Update the display with the current frames per second (FPS)
        self.window_manager.update(self.clock.get_fps())

    def calculate_total_play_time(self):
        # Calculate the elapsed time since the last frame update
        elapsed_time = self.dt

        # Add the elapsed time to the total play time
        self.total_play_time += elapsed_time


    def draw(self):
        self.gameDisplay.fill((30, 30, 30))
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), (100, 100, 200, 150))
        self.scene_manager.draw(self.gameDisplay)

        if self.debug_mode:
            for debug_draw_func in self.debug_draws:
                debug_draw_func()

        self.window_manager.draw()

    def quit_game(self):
        # pygame.image.save(self.gameDisplay, "screenshot.png")
        print(f"Total game time: {self.total_play_time:.3f} seconds")
        pygame.quit()
        quit()

game = Game()
while True:
    game.run()
