import pygame
import random

from manager.audio_manager import AudioManager
from manager.window_manager import WindowManager

from data.constant_data import PROJECT_TITLE, SCREEN_SIZE, FPS, FIRST_SCREEN
from data.resource_data import DICT_MUSIC, DICT_SOUND_EFFECTS

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        random.seed()
        self.init()
        self.playing = True
        self.paused = False

    """
    Initialization
        - init
        - init_display
    """
    def init(self):
        self.load()
        self.new()
        self.init_display()

    def init_display(self):
        parent = self
        self.gameDisplay = WindowManager(parent=parent, project_title=self.project_title, screen_size=self.screen_size, FPS=self.FPS, first_screen=self.first_screen)



    """
    Load:
        - load
        - load_all_manager
        - load_all_data
        - load_all_resources
    """
    def load(self):
        self.load_all_manager()
        self.load_all_data()
        self.load_all_resources()

    def load_all_manager(self):
        self.audio_manager = AudioManager()

    def load_all_data(self):
        self.project_title = PROJECT_TITLE
        self.screen_size = self.screen_width, self.screen_height = SCREEN_SIZE
        self.FPS = FPS
        self.first_screen = FIRST_SCREEN



    def load_all_resources(self):
        self.audio_manager.load_resources(DICT_MUSIC, "sound_effects")
        self.audio_manager.load_resources(DICT_SOUND_EFFECTS, "music")

    """
    New
        - new
    """
    def new(self):
        pass

    # -------------------- #
    def update(self):
        self.gameDisplay.update()

    def draw(self):
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), (100, 100, 200, 150))
        self.gameDisplay.draw()

    # Game Loop ----------------------- #
    def run(self):
        while self.playing:
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


    @staticmethod
    def quit_game():
        pygame.quit()
        quit()

game = Game()
while True:
    game.run()
