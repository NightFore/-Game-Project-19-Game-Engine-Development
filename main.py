import pygame
from pygame.locals import *

import random
from os import path

from manager.audio_manager import AudioManager
from manager.button_manager import ButtonManager
from manager.graphic_manager import GraphicManager
from manager.resource_manager import ResourceManager
from manager.scene_manager import SceneManager
from manager.text_manager import TextManager
from manager.window_manager import WindowManager

from data.constant_data import PROJECT_TITLE, SCREEN_SIZE, FPS
from data.resource_data import DICT_RESOURCES

class GameManager:
    """
    The Game class manages the initialization, setup, loading, and execution of a game using the Pygame framework.

    Attributes:
        playing (bool): A flag that indicates if the game is currently running.
        paused (bool): A flag that indicates if the game is in a paused state.
        debug_mode (bool): A flag that indicates if the game is running in debug mode.
        clock (pygame.time.Clock): The Pygame clock used for controlling the game's frame rate.
        dt (float): The time passed since the last frame update, in seconds.
        total_play_time (float): The total play time of the game in seconds.
        mouse_pos (tuple): The adjusted position of the mouse based on display_factor.
        project_title (str): The title of the game project.
        FPS (int): The desired frames per second for the game's execution.
        screen_size (tuple): The dimensions of the game window (width, height).
        gameDisplay (pygame.Surface): The Pygame surface representing the game's display window.

    Methods:
    - Setup:
        - setup_game: Initialize the game environment.
        - setup_folders: Set up resource folders.
        - setup_managers: Initialize game managers.
        - setup_managers_settings: Set up manager settings.
        - setup_managers_resources: Load and set resources for managers.
        - setup_display: Configure display settings.
        - setup_scenes: Load game scenes and button graphics.

    - Game Loop:
        - run: The main game loop that handles game events, updates, and drawing.
        - events: Handle game events, including user input and window events.
        - update: Update game components, including scenes, managers.
        - draw: Draw game components, scenes, managers.
        - quit_game: Exit the game, print total play time, and clean up resources.
    """
    def __init__(self):
        # Initialize the game
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        random.seed()

        # Set initial game state flags
        self.playing = True
        self.paused = False
        self.debug_mode = False

        # Initialize game-related variables
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick()
        self.total_play_time = 0
        self.mouse_pos = (0, 0)

        # Launch the game
        self.setup_game()
        self.scene_manager.set_scene("MainMenuScene")


    """
    Setup
        - setup_game
        - setup_folders
        - setup_managers
        - setup_managers_settings
        - setup_managers_resources
        - setup_display
        - setup_scenes
    """
    def setup_game(self):
        """
        Initialize the game environment.
        """
        self.setup_folders()
        self.setup_managers()
        self.setup_managers_settings()
        self.setup_managers_resources()
        self.setup_display()
        self.setup_scenes()

    def setup_folders(self):
        """
        Set up resource folders.
        """
        # Get the directory of the current script file
        self.game_folder = path.dirname(__file__)

        # Define the base resources folder
        self.resources_folder = path.join(self.game_folder, "resources")

        # Define individual resource folders
        self.music_folder = path.join(self.resources_folder, "music")
        self.sound_folder = path.join(self.resources_folder, "sound")
        self.graphic_folder = path.join(self.resources_folder, "graphic")
        self.font_folder = path.join(self.resources_folder, "font")

        # Define resource type folders (see ResourceManagers)
        self.resource_type_folders = {
            "music": self.music_folder,
            "sound": self.sound_folder,
            "image": self.graphic_folder,
            "image_sequence": self.graphic_folder,
            "font": self.font_folder,
        }

    def setup_managers(self):
        """
        Initialize game managers.
        """
        self.managers = {
            "game_manager": self,
            "audio_manager": AudioManager(),
            "button_manager": ButtonManager(),
            "graphic_manager": GraphicManager(),
            "resource_manager": ResourceManager(),
            "scene_manager": SceneManager(),
            "text_manager": TextManager(),
            "window_manager": WindowManager()
        }
        self.audio_manager = self.managers["audio_manager"]
        self.button_manager = self.managers["button_manager"]
        self.graphic_manager = self.managers["graphic_manager"]
        self.resource_manager = self.managers["resource_manager"]
        self.scene_manager = self.managers["scene_manager"]
        self.text_manager = self.managers["text_manager"]
        self.window_manager = self.managers["window_manager"]

    def setup_managers_settings(self):
        """
        Set up manager settings.
        """
        # Set resource folders for the ResourceManager
        self.resource_manager.set_resource_folders(self.resource_type_folders)

        # Set managers dictionary for all managers that require it
        for manager in self.managers.values():
            if hasattr(manager, 'set_managers'):
                manager.set_managers(self.managers)

    def setup_managers_resources(self):
        """
        Load and set resources for managers.
        """
        # Load resources from the resources dictionary
        self.resources_dict = DICT_RESOURCES
        self.resource_manager.load_resources(self.resources_dict)

        # Set resources dictionary for all managers that require it
        for manager in self.managers.values():
            if hasattr(manager, 'set_resources'):
                manager.set_resources()

    def setup_display(self):
        """
        Configure display settings.
        """
        self.project_title = PROJECT_TITLE
        self.FPS = FPS
        self.screen_size = self.screen_width, self.screen_height = SCREEN_SIZE
        self.gameDisplay = self.window_manager.create_window_instance(self.project_title, self.screen_size)

    def setup_scenes(self):
        """
        Load game scenes and button data.
        """
        # Load scenes from the 'scenes' directory
        self.scene_manager.load_scenes_from_directory("scenes")

        # Load button graphics for scenes
        self.scene_manager.load_buttons_data()


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
            self.total_play_time += self.dt
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
                elif event.key == pygame.K_h:
                    self.debug_mode = not self.debug_mode
                elif event.key == pygame.K_F4:
                    self.window_manager.update_display_mode(toggle_zoom=True)
                elif event.key == pygame.K_F11:
                    self.window_manager.update_display_mode(toggle_fullscreen=True)

            # Handle quit event
            if event.type == pygame.QUIT:
                self.quit_game()

        # Update mouse position based on display_factor
        self.mouse_pos = self.window_manager.get_adjusted_mouse_position()

    def update(self):
        # Update game components
        self.scene_manager.update()
        self.window_manager.update(self.clock.get_fps())

    def draw(self):
        # Debug
        self.gameDisplay.fill((30, 30, 30))
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), (100, 100, 200, 150))

        # Draw the game components
        self.scene_manager.draw()
        self.window_manager.draw()

    def quit_game(self):
        # pygame.image.save(self.gameDisplay, "screenshot.png")
        print(f"Total game time: {self.total_play_time:.3f} seconds")
        pygame.quit()
        quit()

game = GameManager()
while True:
    game.run()
