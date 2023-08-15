import pygame
from pygame.locals import *

import random
from os import path

from manager.audio_manager import AudioManager
from manager.button_manager import ButtonManager
from manager.graphic_manager import GraphicManager
from manager.scene_manager import SceneManager
from manager.window_manager import WindowManager
from data.constant_data import PROJECT_TITLE, SCREEN_SIZE, FPS
from data.resource_data import DICT_AUDIO, DICT_GRAPHIC, DICT_SCENE

from debug.debug_audio_manager import DebugAudioManager
from debug.debug_graphic_manager import DebugGraphicManager
from debug.debug_data import DEBUG_DICT_AUDIO, DEBUG_DICT_GRAPHIC, DEBUG_DICT_SCENE

class Game:
    """
    Initialization
    """
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.font.init()
        random.seed()
        self.clock = pygame.time.Clock()
        self.playing = True
        self.paused = False
        self.debug_mode = True
        self.debug_updates = []
        self.debug_draws = []
        self.init_game()
        self.load_game()
        self.start_game()

    def init_game(self):
        self.init_folders()
        self.init_managers()
        self.init_resource_mapping()
        self.init_scene_instances()
        self.init_display()

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

    def init_managers(self):
        self.audio_manager = AudioManager()
        self.button_manager = ButtonManager()
        self.graphic_manager = GraphicManager()
        self.scene_manager = SceneManager()
        self.window_manager = WindowManager()

    def init_resource_mapping(self):
        self.audio_manager.set_resource_mapping(self.music_folder, self.sound_folder)
        self.graphic_manager.set_resource_mapping(self.graphic_folder)

    def init_scene_instances(self):
        self.scene_manager.load_scenes_from_directory("scenes")

    def init_display(self):
        self.project_title = PROJECT_TITLE
        self.screen_size = self.screen_width, self.screen_height = SCREEN_SIZE
        self.FPS = FPS
        self.gameDisplay = self.window_manager.create_window_instance(self.project_title, self.screen_size)



    """
    Loading
    """
    def load_game(self):
        if not self.debug_mode:
            self.load_resources()
        else:
            self.load_debug_resources()

    def load_resources(self):
        self.audio_manager.load_resources(DICT_AUDIO)
        self.graphic_manager.load_resources(DICT_GRAPHIC)
        self.scene_manager.load_scenes_params(DICT_SCENE)

    def load_debug_resources(self):
        self.audio_manager.load_resources(DEBUG_DICT_AUDIO)
        self.graphic_manager.load_resources(DEBUG_DICT_GRAPHIC)
        self.scene_manager.load_scenes_params(DEBUG_DICT_SCENE)



    """
    Startup
    """
    def start_game(self):
        self.start_managers()
        self.start_debug_mode()
        self.scene_manager.set_scene("MainMenuScene")

    def start_managers(self):
        self.audio_manager.init_manager()

    def start_debug_mode(self):
        if self.debug_mode:
            debug_managers = [
                DebugAudioManager(self.audio_manager),
                DebugGraphicManager(self.graphic_manager, self.window_manager)]

            for debug_manager in debug_managers:
                self.debug_updates.append(debug_manager.update)
                self.debug_draws.append(debug_manager.draw)


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
                self.gameDisplay.resize()

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
        self.scene_manager.update(self.dt)

        if self.debug_mode:
            for debug_update_func in self.debug_updates:
                debug_update_func()

        self.gameDisplay.update(self.clock.get_fps())


    def draw(self):
        self.gameDisplay.fill((30, 30, 30))
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), (100, 100, 200, 150))
        self.scene_manager.draw(self.gameDisplay)

        if self.debug_mode:
            for debug_draw_func in self.debug_draws:
                debug_draw_func()

        self.gameDisplay.draw()

    def quit_game(self):
        # pygame.image.save(self.gameDisplay, "screenshot.png")
        pygame.quit()
        quit()

game = Game()
while True:
    game.run()
