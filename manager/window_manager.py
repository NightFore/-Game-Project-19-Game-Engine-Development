import pygame
import os
from pygame.locals import *

class WindowManager(pygame.Surface):
    def __init__(self, parent, project_title, screen_size, FPS, first_screen=False):
        """
        Initialize the ScaledGame instance.

        Args:
            parent: The parent object.
            project_title (str): The title of the game project.
            screen_size (tuple): The initial size of the game screen.
            FPS (int): Frames per second.
            first_screen (bool): Whether it's the first screen or not.
        """
        # Call the constructor of the parent class (pygame.Surface) with the specified screen_size
        super().__init__(screen_size)

        # Center window position
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Initialize display-related variables
        self.init_display_variables()

        # Parent
        self.parent = parent

        # Project Title
        self.project_title = project_title
        pygame.display.set_caption(self.project_title)

        # Game Settings
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        # Window Settings
        self.screen_gap = (0, 0)
        self.screen_size = screen_size

        # Required to set a good resolution for the game screen
        self.screen_info = pygame.display.Info()

        # Create the game window
        if not first_screen:
            self.create_game_window(screen_size, RESIZABLE)
        else:
            # Adjust height for title bar
            MENU_BAR_HEIGHT = 120
            self.create_game_window((self.screen_info.current_w, self.screen_info.current_h - MENU_BAR_HEIGHT), RESIZABLE)

    def init_display_variables(self):
        """
        Initialize display-related variables.
        """
        # Screen Scaling
        self.screen_scaled = None

        # Window Resizing
        self.resize = True

        # Zoom Settings
        self.set_zoom = False

        # Fullscreen Settings
        self.set_fullscreen = False

        # Scaling Factors
        self.factor_w = 1
        self.factor_h = 1

    def create_game_window(self, size, flags):
        """
        Create the game window with the specified size and flags.

        Args:
            size (tuple): Size of the window.
            flags: Pygame flags for the window.
        """
        self.screen = pygame.display.set_mode(size, flags)


    def get_resolution(self, ss, gs):
        """
        Calculate the scaled resolution based on aspect ratios.

        Args:
            ss (tuple): Current screen size.
            gs (tuple): Game screen size.

        Returns:
            tuple: Scaled resolution.
        """
        gap = gs[0] / gs[1]  # Game aspect ratio
        sap = ss[0] / ss[1]  # Scaled aspect ratio
        if gap > sap:
            # Divides the height by the factor which the width changes so the aspect ratio remains the same.
            factor = gs[0] / ss[0]
            new_h = gs[1] / factor
            screen_scaled = ss[0], new_h
        elif gap < sap:
            # Divides the width by the factor which the height changes so the aspect ratio remains the same.
            factor = gs[1] / ss[1]
            new_w = gs[0] / factor
            screen_scaled = new_w, ss[1]
        else:
            screen_scaled = self.screen.get_size()
        return int(screen_scaled[0]), int(screen_scaled[1])

    def fullscreen(self):
        """
        Toggle between fullscreen and windowed mode.
        """
        if not self.set_fullscreen:
            # Switch to fullscreen mode
            self.screen_gap = 0, 0
            self.screen_scaled = self.screen_size
            self.set_zoom = False
            self.screen = pygame.display.set_mode(self.screen_size, FULLSCREEN)
            self.factor_w = 1
            self.factor_h = 1
            self.set_fullscreen = True
        else:
            # Switch to windowed mode
            self.resize = True
            self.set_fullscreen = False

    def update(self):
        """
        Update the display and handle resizing.
        """
        # Display the current FPS in the window title
        pygame.display.set_caption(self.project_title + " (" + str(int(self.clock.get_fps())) + "FPS)")

        # Get current screen size
        ss = [self.screen.get_width(), self.screen.get_height()]

        # Handle resizing events
        for event in self.parent.event:
            if event.type == VIDEORESIZE:
                ss = [event.w, event.h]
                self.resize = not (self.set_zoom and (ss[0] == self.screen_info.current_w or ss[0] == self.screen_scaled[0]))

        # Fullscreen
        if self.set_fullscreen:
            self.screen.blit(self, self.screen_gap)

        # Resize
        elif self.resize:
            self.screen_scaled = self.get_resolution(ss, self.screen_size)

            # Zoom
            if ss[0] + self.screen_gap[0] == self.screen_info.current_w:
                self.screen_gap = int((self.screen_info.current_w - self.screen_scaled[0]) / 2), self.screen_gap[1]
                self.set_zoom = True
            elif self.set_zoom:
                self.screen_gap = 0, 0
                self.screen_scaled = self.screen_size
                self.set_zoom = False

            # Calculate screen dimensions
            screen_w = self.screen_scaled[0] + self.screen_gap[0] * 2
            screen_h = self.screen_scaled[1] + self.screen_gap[1] * 2

            # Calculate scaling factors
            self.factor_w = self.screen_scaled[0] / self.get_width()
            self.factor_h = self.screen_scaled[1] / self.get_height()

            # Update the game window size
            self.create_game_window((screen_w, screen_h), RESIZABLE)
            self.resize = False

    def draw(self):
        """
        Draw the game surface onto the screen.
        """
        # Add game to screen with the scaled size and gap required.
        self.screen.blit(pygame.transform.scale(self, self.screen_scaled), self.screen_gap)
        pygame.display.flip()
