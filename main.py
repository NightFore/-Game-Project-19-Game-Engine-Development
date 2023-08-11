import pygame
import random
from os import path

from manager.audio_manager import AudioManager
from manager.button_manager import ButtonManager
from manager.graphic_manager import GraphicManager
from manager.scene_manager import SceneManager
from manager.window_manager import WindowManager

from data.constant_data import PROJECT_TITLE, SCREEN_SIZE, FPS, FIRST_SCREEN
from data.resource_data import DICT_MUSIC, DICT_SOUND_EFFECTS
from data.debug_data import DEBUG_DICT_AUDIO, DEBUG_DICT_GRAPHIC, DEBUG_DICT_SCENE

class Game:
    """
    Initialization
    """
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        random.seed()
        self.playing = True
        self.paused = False
        self.debug_mode = True
        self.load()
        self.new()



    """
    Loading
        - load_folders
        - load_managers
        - load_resource_mapping
        - load_window_instance
        - load_constants
        - load_resources
        
    Debug
        - load_debug_resources
    """
    def load(self):
        self.load_folders()
        self.load_managers()
        self.load_resource_mapping()
        self.load_window_instance()
        self.load_constants()
        self.load_resources()

        if self.debug_mode:
            self.load_debug_resources()

    def load_folders(self):
        self.game_folder = path.dirname(__file__)
        self.resources_folder = path.join(self.game_folder, "resources")
        self.font_folder = path.join(self.resources_folder, "font")
        self.graphic_folder = path.join(self.resources_folder, "graphic")
        self.music_folder = path.join(self.resources_folder, "music")
        self.sound_folder = path.join(self.resources_folder, "sound")

    def load_managers(self):
        self.audio_manager = AudioManager()
        self.button_manager = ButtonManager()
        self.graphic_manager = GraphicManager()
        self.scene_manager = SceneManager()
        self.window_manager = WindowManager()

    def load_resource_mapping(self):
        self.audio_manager.set_resource_mapping(self.music_folder, self.sound_folder)
        self.graphic_manager.set_resource_mapping(self.graphic_folder)

    def load_window_instance(self):
        self.project_title = PROJECT_TITLE
        self.screen_size = self.screen_width, self.screen_height = SCREEN_SIZE
        self.FPS = FPS
        self.first_screen = FIRST_SCREEN
        self.gameDisplay = self.window_manager.create_window_instance(self.screen_size, self, self.project_title, self.FPS, self.first_screen)


    def load_constants(self):
        pass

    def load_resources(self):
        pass

    def load_debug_resources(self):
        self.audio_manager.load_resources(DEBUG_DICT_AUDIO)
        self.graphic_manager.load_resources(DEBUG_DICT_GRAPHIC)
        self.scene_manager.load_scene_params(DEBUG_DICT_SCENE)



    """
    New
        - new
    """
    def new(self):
        pass

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
            self.dt = self.gameDisplay.clock.tick(self.FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        self.quit_game()

    def events(self):
        """Click: None, Left, Middle, Right, Scroll Up, Scroll Down"""
        self.click = [None, False, False, False, False, False]

        """Events"""
        self.event = pygame.event.get()

    def update(self):
        self.gameDisplay.update()

    def draw(self):
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), (100, 100, 200, 150))
        self.gameDisplay.draw()

    def quit_game(self):
        # pygame.image.save(self.gameDisplay, "screenshot.png")
        pygame.quit()
        quit()

game = Game()
while True:
    game.run()
