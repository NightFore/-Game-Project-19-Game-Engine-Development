import pygame
from pygame.locals import *

import random
from os import path

from engine.window_manager import WindowManager


class MainManager:
    """
    """
    def __init__(self):
        # Initialize the game
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        random.seed()

        # Initialize game state flags
        self.playing = True
        self.paused = False
        self.debug_mode = False

        # Initialize time-related variables
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick()
        self.total_play_time = 0

        # Initialize input handling
        self.mouse_pos = (0, 0)

        # Initialize project settings
        self.window_title = "WINDOW_TITLE"
        self.project_title = "PROJECT_TITLE"
        self.FPS = 60
        self.screen_size = self.screen_width, self.screen_height = (800, 600)

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

        """
        Initialize game managers.
        """
        self.managers = {
            "main_manager": self,
            "window_manager": WindowManager()
        }
        self.window_manager = self.managers["window_manager"]

        """
        Configure display settings.
        """
        flags = RESIZABLE
        self.gameDisplay = self.window_manager.create_window_instance(self.window_title, self.screen_size, flags)

        self.click = None
        self.event = None

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
            # Calculate the time since the last frame (in seconds)
            self.dt = self.clock.tick(self.FPS) / 1000

            # Increment the total play time
            self.total_play_time += self.dt

            # Handle user events
            self.events()

            # Update the game state if not paused
            if not self.paused:
                self.update()

            # Render the current frame
            self.draw()

        # Quit the game when the main loop ends
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
                    self.window_manager.toggle_zoom()
                elif event.key == pygame.K_F6:
                    self.window_manager.toggle_resizable()
                elif event.key == pygame.K_F11:
                    self.window_manager.toggle_fullscreen()

            # Handle quit event
            if event.type == pygame.QUIT:
                self.quit_game()

        # Update mouse position based on display_factor
        self.mouse_pos = self.window_manager.get_adjusted_mouse_position()

    def update(self):
        # Update game components
        self.window_manager.update(self.clock.get_fps())

        # Debug
        debug = False
        if debug:
            print(self.mouse_pos)
            print(self.window_manager.is_resizable, self.window_manager.is_fullscreen, self.window_manager.is_zoom)

    def draw(self):
        # Debug
        self.gameDisplay.fill((30, 30, 30))
        pygame.draw.circle(self.gameDisplay, (255, 0, 0), (400, 300), 30)

        # Draw the game components
        self.window_manager.draw()

    def quit_game(self):
        # pygame.image.save(self.gameDisplay, "screenshot.png")
        print(f"Total game time: {self.total_play_time:.3f} seconds")
        pygame.quit()
        quit()


game = MainManager()
while True:
    game.run()
