import pygame
import random
from pygame.locals import *
from config import load_config
from engine.ui_manager import UIManager
from logger import Logger
from engine.audio_manager import AudioManager
from engine.window_manager import WindowManager


class MainManager:
    """
    MainManager handles the main game loop and overall game state management.

    Attributes:
        Common Attributes:
            - config (dict): Configuration dictionary loaded from config.json.
            - logger (logging.Logger): Logger instance for logging messages.

        Game State Attributes:
            - event (list): List to store pygame events.
            - playing (bool): Flag to control the main game loop.
            - paused (bool): Flag to indicate if the game is paused.
            - debug_mode (bool): Flag to toggle debug mode.

        Time Management Attributes:
            - FPS (int): Target frames per second.
            - total_play_time (float): Total play time in seconds.
            - clock (pygame.time.Clock): Clock object to manage frame rate.
            - dt (float): Delta time since the last frame.

        Input Handling Attributes:
            - mouse_pos (tuple): Current mouse position.
            - click (list): List to track mouse click states.

        Manager Attributes:
            - window_manager (WindowManager): Instance of the WindowManager.

    Methods:
        Game Loop:
            - run(): Main game loop. Handles events, updates game state, and renders the frame.
            - events(): Handle user input events.
            - update(): Update the game state.
            - draw(): Render the game frame.
            - quit_game(): Quit the game and clean up resources.
    """
    def __init__(self):
        """
        Initialize the MainManager instance and set up the game.
        """
        # Initialize pygame and random seed
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        random.seed()

        # Common Attributes
        self.config = load_config()
        self.logger = Logger()

        # Game State Attributes
        self.event = None
        self.playing = True
        self.paused = False
        self.debug_mode = False

        # Time Management Attributes
        self.FPS = 60
        self.total_play_time = 0
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.FPS) / 1000

        # Input Handling Attributes
        self.mouse_pos = (0, 0)
        self.click = [None, False, False, False, False, False]

        # Manager Attributes
        self.main_manager = self
        self.audio_manager = AudioManager()
        self.ui_manager = UIManager()
        self.window_manager = WindowManager()

        self.managers = {
            'main_manager': self.main_manager,
            'audio_manager': self.audio_manager,
            'window_manager': self.window_manager
        }

        # Initialize Managers
        self.audio_manager.initialize(self.config, self.managers, self.logger)
        self.ui_manager.initialize(self.config, self.managers, self.logger)
        self.window_manager.initialize(self.config, self.managers, self.logger)
        self.display = self.window_manager.get_surface()

        # Pass managers to UIManager
        self.ui_manager.set_display(self.display)

        # Load the initial menu
        self.ui_manager.load_menu('start_menu')

        self.logger.log_info(f"MainManager initialized")

    """
    Game Loop
        - run
        - events
        - update
        - draw
        - quit_game
    """
    def run(self):
        """
        Main game loop. Handles events, updates game state, and renders the frame.
        """
        while self.playing:
            # Calculate delta time and increment total play time (in seconds)
            self.dt = self.clock.tick(self.FPS) / 1000
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
        """
        Handle user input events.
        """
        # Click: None, Left, Middle, Right, Scroll Up, Scroll Down
        self.click = [None, False, False, False, False, False]

        # Get events
        self.event = pygame.event.get()
        for event in self.event:
            # Handle window resizing event
            if event.type == VIDEORESIZE:
                self.window_manager.resize()

            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click[1] = True
                elif event.button == 2:
                    self.click[2] = True
                elif event.button == 3:
                    self.click[3] = True
                elif event.button == 4:
                    self.click[4] = True
                elif event.button == 5:
                    self.click[5] = True

            # Handle keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                elif event.key == pygame.K_h:
                    self.debug_mode = not self.debug_mode
                elif event.key == pygame.K_F4:
                    self.window_manager.toggle_maximize()
                elif event.key == pygame.K_F6:
                    self.window_manager.toggle_resizable()
                elif event.key == pygame.K_F11:
                    self.window_manager.toggle_fullscreen()

            # Debug
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.audio_manager.play_music("bgm_eight_Lament_Scarlet")
                elif event.key == pygame.K_2:
                    self.audio_manager.play_music("bgm_nagumorizu_Strategy_Meeting")
                elif event.key == pygame.K_3:
                    self.audio_manager.play_music("bgm_tak_mfk_冷月の舞踏_(Reigetsu_no_Buto)")
                elif event.key == pygame.K_4:
                    self.audio_manager.play_sound("maou_se_onepoint09")
                elif event.key == pygame.K_5:
                    self.audio_manager.play_voice("YouFulca_voice_07_cool_attack")
                elif event.key == pygame.K_m:
                    self.audio_manager.toggle_music_playback()
                elif event.key == pygame.K_v:
                    self.audio_manager.stop_music()
                elif event.key == pygame.K_b:
                    self.audio_manager.stop_sound()
                elif event.key == pygame.K_n:
                    self.audio_manager.stop_voice()
                elif event.key == pygame.K_o:
                    self.audio_manager.set_bgm_loop(-1)  # Infinite loop
                elif event.key == pygame.K_p:
                    self.audio_manager.set_bgm_loop(0)   # No loop
                elif event.key == pygame.K_u:
                    self.audio_manager.toggle_audio_mute()  # Toggle mute/unmute
                elif event.key == pygame.K_KP_PLUS:
                    self.audio_manager.adjust_volume("master", 0.05)
                elif event.key == pygame.K_KP_MINUS:
                    self.audio_manager.adjust_volume("master", -0.05)

            # Handle quit event
            if event.type == pygame.QUIT:
                self.quit_game()

        # Update mouse position based on display_factor
        self.mouse_pos = self.window_manager.get_adjusted_mouse_position()

    def update(self):
        """
        Update the game state.
        """
        # Update game components
        self.window_manager.update(self.clock.get_fps())

        self.ui_manager.update(self.mouse_pos, self.click)

    def draw(self):
        """
        Render the game frame.
        """
        # Clear the display
        self.display.fill((0, 0, 0))

        # Debug
        self.display.fill((30, 30, 30))
        pygame.draw.circle(self.display, (255, 0, 0), (400, 300), 30)

        # Draw the game components
        self.ui_manager.draw()
        self.window_manager.draw()

    def quit_game(self):
        """
        Quit the game and clean up resources.
        """
        self.logger.log_info(f"Total game time: {self.total_play_time:.3f} seconds")
        pygame.quit()
        quit()


if __name__ == "__main__":
    game = MainManager()
    while True:
        game.run()
