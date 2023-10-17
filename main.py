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
    """
    Initialization
    """
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        random.seed()
        self.total_play_time = 0
        self.clock = pygame.time.Clock()
        self.playing = True
        self.paused = False
        self.debug_mode = True
        self.init_game()
        self.load_game()
        self.start_game()

    def init_game(self):
        self.init_folders()
        self.init_dict()
        self.init_managers()

    def init_folders(self):
        self.game_folder = path.dirname(__file__)

        if not self.debug_mode:
            self.resources_folder = path.join(self.game_folder, "resources")
            self.font_folder = path.join(self.resources_folder, "font")
            self.graphic_folder = path.join(self.resources_folder, "graphic")
            self.music_folder = path.join(self.resources_folder, "music")
            self.sound_folder = path.join(self.resources_folder, "sound")
        else:
            self.debug_folder = path.join(self.game_folder, "debug")
            self.font_folder = path.join(self.debug_folder, "debug_resources")
            self.graphic_folder = path.join(self.debug_folder, "debug_resources")
            self.music_folder = path.join(self.debug_folder, "debug_resources")
            self.sound_folder = path.join(self.debug_folder, "debug_resources")

        self.resource_type_folders = {
            "music": self.music_folder,
            "sound": self.sound_folder,
            "image": self.graphic_folder,
            "image_sequence": self.graphic_folder,
            "font": self.font_folder,
        }

    def init_dict(self):
        if not self.debug_mode:
            self.audio_dict = DICT_AUDIO
            self.font_dict = DICT_FONT
            self.graphic_dict = DICT_GRAPHIC
            self.scene_dict = DICT_SCENE
        else:
            self.audio_dict = DEBUG_DICT_AUDIO
            self.font_dict = DEBUG_DICT_FONT
            self.graphic_dict = DEBUG_DICT_GRAPHIC
            self.scene_dict = DEBUG_DICT_SCENE

    def init_managers(self):
        self.audio_manager = AudioManager()
        self.button_manager = ButtonManager()
        self.graphic_manager = GraphicManager()
        self.resource_manager = ResourceManager()
        self.scene_manager = SceneManager()
        self.font_manager = FontManager()
        self.window_manager = WindowManager()



    """
    Loading
    """
    def load_game(self):
        self.load_display()
        self.load_resources()
        self.load_scenes()

    def load_display(self):
        """
        Initialize game display settings.
        """
        self.project_title = PROJECT_TITLE
        self.screen_size = self.screen_width, self.screen_height = SCREEN_SIZE
        self.FPS = FPS
        self.gameDisplay = self.window_manager.create_window_instance(self.project_title, self.screen_size)

    def load_resources(self):
        # ResourceManager
        self.resource_manager.set_resource_folders(self.resource_type_folders)
        self.resource_manager.load_resources(self.audio_dict)
        self.resource_manager.load_resources(self.graphic_dict)

        # Dependent Managers
        self.audio_manager.load_resources(self.resource_manager)
        self.graphic_manager.load_resources(self.resource_manager)

    def load_scenes(self):
        self.scene_manager.load_scenes_from_directory("scenes")
        self.scene_manager.load_scenes_params(self.scene_dict)



    """
    Startup
    """
    def start_game(self):
        self.start_managers()
        self.start_debug_mode()

    def start_managers(self):
        self.scene_manager.set_scene("MainMenuScene")

    def start_debug_mode(self):
        self.debug_updates = []
        self.debug_draws = []

        if self.debug_mode:
            debug_managers = [
                DebugAudioManager(self.audio_manager),
                DebugGraphicManager(self.graphic_manager, self.window_manager)]

            for debug_manager in debug_managers:
                self.debug_updates.append(debug_manager.update)
                self.debug_draws.append(debug_manager.draw)

    """
    Update
        - calculate_total_play_time
    """
    def calculate_total_play_time(self):
        # Calculate the elapsed time since the last frame update
        elapsed_time = self.dt

        # Add the elapsed time to the total play time
        self.total_play_time += elapsed_time


    """
    Game Loop
        - start_game
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
                elif event.key == pygame.K_F5:
                    self.start_game()
                elif event.key == pygame.K_F11:
                    self.window_manager.update_display_mode(toggle_fullscreen=True)

            # Handle quit event
            if event.type == pygame.QUIT:
                self.quit_game()

    def update(self):
        # Check if the game is not paused before performing updates
        if not self.paused:
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
