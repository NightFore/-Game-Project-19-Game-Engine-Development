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
        Game State Attributes:
            - event (list): List to store pygame events.
            - playing (bool): Flag to control the main game loop.
            - paused (bool): Flag to indicate if the game is paused.
            - debug_mode (bool): Flag to toggle debug mode.

        Time Management Attributes:
            - clock (pygame.time.Clock): Clock object to manage frame rate.
            - dt (float): Delta time since the last frame.
            - total_play_time (float): Total play time in seconds.

        Input Handling Attributes:
            - mouse_pos (tuple): Current mouse position.
            - click (list): List to track mouse click states.

        Project Settings Attributes:
            - window_title (str): Title of the game window.
            - project_title (str): Title of the project.
            - FPS (int): Target frames per second.
            - screen_size (tuple): Size of the game screen.

        Miscellaneous Attributes:
            - logger (GameLogger): Logger instance for logging events.

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

        # Game State Attributes
        self.event = None
        self.playing = True
        self.paused = False
        self.debug_mode = False

        # Time Management Attributes
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick()
        self.total_play_time = 0

        # Input Handling Attributes
        self.mouse_pos = (0, 0)
        self.click = [None, False, False, False, False, False]

        # Project Settings Attributes
        self.window_title = "WINDOW_TITLE"
        self.project_title = "PROJECT_TITLE"
        self.FPS = 60
        self.screen_size = self.screen_width, self.screen_height = (800, 600)

        # Miscellaneous Attributes
        self.logger = Logger()
        self.logger.info(f"MainManager initialized")

        self.config = load_config()

        # Manager Attributes
        self.audio_manager = AudioManager()
        self.window_manager = WindowManager()

        # Initialize Managers
        self.audio_manager.initialize(self.config, self.logger)
        self.window_manager.initialize(self.config, self.logger)
        self.gameDisplay = self.window_manager.get_surface()

        self.button_font = pygame.font.Font(None, 36)

        # Pass managers to UIManager
        self.ui_manager = UIManager(self.button_font, self.gameDisplay, {
            'main_manager': self,
            'audio_manager': self.audio_manager,
            'window_manager': self.window_manager
        })

        # Load the initial menu
        self.ui_manager.load_menu('start_menu')

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

            # Handle quit event
            if event.type == pygame.QUIT:
                self.quit_game()

        # Update mouse position based on display_factor
        self.mouse_pos = self.window_manager.get_adjusted_mouse_position()

        self.ui_manager.handle_events(self.event, self.mouse_pos, self.click)

    def update(self):
        """
        Update the game state.
        """
        # Update game components
        self.window_manager.update(self.clock.get_fps())

    def draw(self):
        """
        Render the game frame.
        """
        # Clear the display
        self.gameDisplay.fill((0, 0, 0))

        # Debug
        self.gameDisplay.fill((30, 30, 30))
        pygame.draw.circle(self.gameDisplay, (255, 0, 0), (400, 300), 30)

        self.ui_manager.draw()

        # Draw the game components
        self.window_manager.draw()

        # Update the display
        pygame.display.flip()

    def quit_game(self):
        """
        Quit the game and clean up resources.
        """
        self.logger.info(f"Total game time: {self.total_play_time:.3f} seconds")
        pygame.quit()
        quit()


if __name__ == "__main__":
    game = MainManager()
    while True:
        game.run()
