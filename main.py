import pygame
import random
from pygame.locals import *
from config import load_config
from logger import Logger
from engine.audio_manager import AudioManager
from engine.window_manager import WindowManager
from engine.button import Button

class MainManager:
    """
    MainManager handles the main game loop and overall game state management.
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

        # Font for buttons
        self.button_font = pygame.font.Font(None, 36)

        # Initialize Button List
        self.buttons = []

        # Create start button
        self.create_start_button()

    def create_start_button(self):
        """
        Create the start button.
        """
        self.buttons.append(
            Button(300, 250, 200, 50, 'Start', (70, 130, 180), self.button_font, self.start_game)
        )

    def start_game(self):
        """
        Create the main menu buttons and hide the start button.
        """
        # Add main menu buttons
        self.buttons = [
            Button(50, 50, 200, 50, 'Toggle Fullscreen', (70, 130, 180), self.button_font, self.window_manager.toggle_fullscreen),
            Button(50, 120, 200, 50, 'Toggle Resizable', (70, 130, 180), self.button_font, self.window_manager.toggle_resizable),
            Button(50, 190, 200, 50, 'Toggle Maximize', (70, 130, 180), self.button_font, self.window_manager.toggle_maximize),
            Button(300, 120, 200, 50, 'Play Music 1', (70, 130, 180), self.button_font, lambda: self.audio_manager.play_music("bgm_eight_Lament_Scarlet")),
            Button(300, 190, 200, 50, 'Play Music 2', (70, 130, 180), self.button_font, lambda: self.audio_manager.play_music("bgm_nagumorizu_Strategy_Meeting")),
            Button(300, 260, 200, 50, 'Play Music 3', (70, 130, 180), self.button_font, lambda: self.audio_manager.play_music("bgm_tak_mfk_冷月の舞踏_(Reigetsu_no_Buto)")),
            Button(300, 330, 200, 50, 'Play Sound', (70, 130, 180), self.button_font, lambda: self.audio_manager.play_sound("maou_se_onepoint09")),
            Button(300, 400, 200, 50, 'Play Voice', (70, 130, 180), self.button_font, lambda: self.audio_manager.play_voice("YouFulca_voice_07_cool_attack")),
            Button(550, 50, 200, 50, 'Toggle Music', (70, 130, 180), self.button_font, self.audio_manager.toggle_music_playback),
            Button(550, 120, 200, 50, 'Stop Music', (70, 130, 180), self.button_font, self.audio_manager.stop_music),
            Button(550, 190, 200, 50, 'Stop Sound', (70, 130, 180), self.button_font, self.audio_manager.stop_sound),
            Button(550, 260, 200, 50, 'Stop Voice', (70, 130, 180), self.button_font, self.audio_manager.stop_voice),
            Button(550, 330, 200, 50, 'Loop Music', (70, 130, 180), self.button_font, lambda: self.audio_manager.set_bgm_loop(-1)),  # Infinite loop
            Button(550, 400, 200, 50, 'No Loop', (70, 130, 180), self.button_font, lambda: self.audio_manager.set_bgm_loop(0)),  # No loop
            Button(550, 470, 200, 50, 'Toggle Mute', (70, 130, 180), self.button_font, self.audio_manager.toggle_audio_mute),
            Button(550, 540, 200, 50, 'Volume Up', (70, 130, 180), self.button_font, lambda: self.audio_manager.adjust_volume("master", 0.05)),
            Button(550, 610, 200, 50, 'Volume Down', (70, 130, 180), self.button_font, lambda: self.audio_manager.adjust_volume("master", -0.05))
        ]

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

        # Check for button clicks
        for button in self.buttons:
            if button.is_hovered(self.mouse_pos) and any(self.click):
                button.click()

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

        # Draw the buttons
        for button in self.buttons:
            button.draw(self.gameDisplay)

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
