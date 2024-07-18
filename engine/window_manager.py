# window_manager.py

import pygame
import os
import ctypes
from typing import Optional
from pygame.locals import *
from engine.base_manager import BaseManager


class WindowManager(BaseManager):
    """
    WindowManager manages the game window and its display modes.

    Attributes:
        Common Attributes:
            - config (dict): Configuration dictionary loaded from config.json.
            - logger (logging.Logger): Logger instance for logging messages.

        Game Attributes:
            - title (str): The title of the window.
            - game_size (tuple): The size of the game window in (width, height).

        Display Attributes:
            - screen_info (pygame.display.Info): Information about the display.
            - screen_scaled (tuple): Scaled size of the game surface on the screen.
            - screen_gap (tuple): Gap around the game surface on the screen.
            - display_factor (float): Factor for scaling based on display resolution.
            - display (pygame.Surface): Main display surface managed by the window manager.
            - surface (pygame.Surface): Surface for rendering game content.

        Flags Attributes:
            - flags (int): Flags for display mode.
            - is_resizable (bool): Flag indicating if the window is resizable.
            - is_fullscreen (bool): Flag indicating if the window is in fullscreen mode.
            - is_maximized (bool): Flag indicating if the window is maximized.x

    Methods:
        Instance Setup:
            - load_specific_components(): Load specific components based on the configuration.
            - set_title(title): Set the title of the window.
            - set_size(size): Set the size of the window.
            - set_flags(flags): Set the display flags of the window.
            - set_logger(logger): Set the logger instance.
            - get_surface(): Retrieve the pygame.Surface used for rendering game content.

        Window Management:
            - toggle_fullscreen(): Toggle the fullscreen mode of the window.
            - toggle_resizable(): Toggle the resizable mode of the window.
            - toggle_maximize(): Toggle the maximize mode of the window.
            - detect_maximize(): Detect and toggle maximize flag based on current state.
            - maximize_window(): Maximize the game window on Windows.
            - restore_window(): Restore the game window to its initial size on Windows.

        Display Management:
            - adjust_display(): Adjust the window display based on current settings.
            - adjust_aspect_ratio(): Adjust the aspect ratio for maintaining proper scaling during resizing.
            - resize(): Resize the window while considering maximize and screen width.

        Input Handling:
            - get_adjusted_mouse_position(): Get the adjusted mouse position based on display_factor.

        Update and Drawing:
            - update(frame_rate): Update the display with the current frame rate.
            - draw(): Draw the game surface onto the display.
    """
    def __init__(self):
        """
        Initialize the WindowManager instance.
        """
        super().__init__()

        # Common Attributes
        self.config = {
            "title": Optional[str],
            "width": Optional[int],
            "height": Optional[int],
            "fullscreen": Optional[bool],
            "resizable": Optional[bool],
            "maximized": Optional[bool]
        }
        self.logger = None

        # Set the environment variable to center the game window.
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Game Attributes
        self.title = Optional[str]
        self.game_size = Optional[tuple]

        # Display Attributes
        self.screen_info = pygame.display.Info()
        self.screen_scaled = Optional[tuple]
        self.screen_gap = Optional[tuple]
        self.display_factor = 1
        self.display = pygame.display.set_mode((0, 0), HIDDEN)
        self.surface = pygame.Surface((0, 0))

        # Flags Attributes
        self.is_fullscreen = Optional[bool]
        self.is_resizable = Optional[bool]
        self.is_maximized = Optional[bool]
        self.flags = Optional[int]

    """
    Instance Setup
        - load_specific_components
        - set_title
        - set_size
        - set_flags
        - set_logger
        - get_surface
    """
    def load_specific_components(self):
        """
        Load specific components based on the configuration.
        """
        # Set Manager attributes
        self.set_title()
        self.set_size()
        self.set_flags()

        # Adjust the display based on new settings
        self.adjust_display()

    def set_title(self):
        """
        Set the title of the window.
        """
        self.title = self.config["title"]
        pygame.display.set_caption(self.title)

    def set_size(self):
        """
        Set the size of the window.
        """
        self.game_size = (self.config["width"], self.config["height"])
        self.screen_scaled = self.game_size
        self.screen_gap = (0, 0)
        self.surface = pygame.Surface(self.game_size)

    def set_flags(self):
        """
        Set the display flags of the window.
        """
        self.is_fullscreen = self.config["fullscreen"]
        self.is_resizable = self.config["resizable"]
        self.is_maximized = self.config["maximized"]

        self.flags = 0
        if self.is_fullscreen:
            self.flags |= FULLSCREEN
        if self.is_resizable:
            self.flags |= RESIZABLE

    def get_surface(self):
        """
        Retrieve the pygame.Surface used for rendering game content.

        Returns:
            pygame.Surface: The surface used for rendering game content.
        """
        return self.surface

    """
    Window Management
        - toggle_fullscreen
        - toggle_resizable
        - toggle_maximize
        - detect_maximize
        - maximize_window
        - restore_window
    """
    def toggle_fullscreen(self):
        """
        Toggle the fullscreen mode of the window.
        """
        # Toggle the fullscreen mode
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            # Switch to fullscreen mode
            self.flags |= FULLSCREEN
            self.flags &= ~RESIZABLE

            # Reset screen properties
            self.screen_gap = (0, 0)
            self.screen_scaled = self.game_size
        else:
            # Switch to windowed mode
            self.flags &= ~FULLSCREEN

            # Restore resizable flag if previously set
            if self.is_resizable:
                self.flags |= RESIZABLE

        # Check and restore maximized state if transitioning from fullscreen to windowed mode
        if self.is_fullscreen and self.is_maximized:
            self.restore_window()
            self.log_debug(f"Resizable mode disabled")

        # Adjust the display based on new settings
        self.adjust_display()

        # Log the action if logger is defined
        action = "enabled" if self.is_fullscreen else "disabled"
        self.log_debug(f"Fullscreen mode {action}")

    def toggle_resizable(self):
        """
        Toggle the resizable mode of the window.
        """
        if not self.is_fullscreen and not self.is_maximized:
            # Toggle the resizable mode
            self.is_resizable = not self.is_resizable

            if self.is_resizable:
                # Switch to resizable mode
                self.flags |= RESIZABLE
                self.flags &= ~FULLSCREEN
            else:
                # Switch to windowed mode
                self.flags &= ~RESIZABLE

            # Adjust the display based on new settings
            self.adjust_display()

            # Log the action if logger is defined
            action = "enabled" if self.is_resizable else "disabled"
            self.log_debug(f"Resizable mode {action}")
        else:
            # Handle cases where toggle is ignored
            if self.is_fullscreen:
                self.log_debug("Window is in fullscreen mode. Resizable mode toggle ignored.")
            elif self.is_maximized:
                self.log_debug("Window is maximized. Resizable mode toggle ignored.")

    def toggle_maximize(self):
        """
        Toggle the maximize mode of the window.
        """
        if self.is_resizable and not self.is_fullscreen:
            hwnd = pygame.display.get_wm_info()['window']
            current_state = ctypes.windll.user32.IsZoomed(hwnd)
            if current_state:
                # If currently maximized, restore to normal size
                self.restore_window()
            else:
                # If not currently maximized, maximize the window
                self.maximize_window()
        else:
            # Handle cases where toggle is ignored
            if self.is_fullscreen:
                self.log_debug("Window is in fullscreen mode. Maximize operation ignored.")
            else:
                self.log_debug("Window is not resizable. Maximize operation ignored.")

    def detect_maximize(self):
        """
        Detect and toggle maximize flag based on current state.
        """
        # Toggle the maximize mode
        self.is_maximized = not self.is_maximized

        if self.is_maximized:
            # Adjust screen_gap when maximize is enabled to center the game surface.
            self.screen_gap = int((self.screen_info.current_w - self.screen_scaled[0]) / 2), self.screen_gap[1]
        else:
            # Reset screen properties
            self.screen_gap = (0, 0)
            self.screen_scaled = self.game_size

        # Log the action if logger is defined
        if self.logger:
            action = "enabled" if self.is_maximized else "disabled"
            self.log_debug(f"Maximize mode {action}")

    @staticmethod
    def maximize_window():
        """
        Maximize the game window on Windows.
        """
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE = 3

    @staticmethod
    def restore_window():
        """
        Restore the game window to its initial size on Windows.
        """
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9

    """
    Display Management
        - adjust_display
        - adjust_aspect_ratio
        - resize
    """
    def adjust_display(self):
        """
        Adjust the window display based on current settings.
        """
        # Calculate screen dimensions
        screen_w = self.screen_scaled[0] + self.screen_gap[0] * 2
        screen_h = self.screen_scaled[1] + self.screen_gap[1] * 2
        screen_size = screen_w, screen_h

        # Set the display mode with the calculated dimensions and provided flags.
        self.display = pygame.display.set_mode(screen_size, self.flags)

    def adjust_aspect_ratio(self):
        """
        Adjust the aspect ratio for maintaining proper scaling during resizing.
        """
        # Get the display and game screen sizes
        ss = self.display.get_size()
        gs = self.game_size

        # Calculate the display and game aspect ratios
        sap = ss[0] / ss[1]
        gap = gs[0] / gs[1]

        # Store the current scaled size including the gap for logging
        previous_scaled_size = (
            self.screen_scaled[0] + self.screen_gap[0] * 2,
            self.screen_scaled[1] + self.screen_gap[1] * 2
        )

        if sap < gap:
            # Adjust based on width scaling factor to maintain aspect ratio
            self.display_factor = ss[0] / gs[0]
            self.screen_scaled = ss[0], int(gs[1] * self.display_factor)
        elif sap > gap:
            # Adjust based on height scaling factor to maintain aspect ratio
            self.display_factor = ss[1] / gs[1]
            self.screen_scaled = int(gs[0] * self.display_factor), ss[1]

        # Log the new screen size
        if previous_scaled_size != ss:
            self.log_debug(f"Updated display size: {previous_scaled_size} -> {ss}")

    def resize(self):
        """
        Resize the window while considering maximize and screen width.
        """
        # Adjust aspect ratio based on current display size
        self.adjust_aspect_ratio()

        # Detect maximize if enabled or if screen width matches current display width
        if self.is_maximized or self.display.get_width() == self.screen_info.current_w:
            self.detect_maximize()

        # Adjust the display based on new settings
        self.adjust_display()

    """
    Input Handling
        - get_adjusted_mouse_position
    """
    def get_adjusted_mouse_position(self):
        """
        Get the adjusted mouse position based on display_factor.

        Returns:
            tuple: Adjusted mouse position (x, y).
        """
        # Get the mouse coordinates
        x, y = pygame.mouse.get_pos()

        # Adjust the mouse coordinates based on display_factor
        adjusted_x = int(x / self.display_factor + 0.5) - self.screen_gap[0]
        adjusted_y = int(y / self.display_factor + 0.5) - self.screen_gap[1]

        return adjusted_x, adjusted_y

    """
    Update and Drawing
        - update
        - draw
    """
    def update(self, frame_rate):
        """
        Update the display.

        Args:
            frame_rate (float): Current frame rate in frames per second.
        """
        # Display the current FPS in the window title
        pygame.display.set_caption(f"{self.title} ({int(frame_rate)} FPS)")

    def draw(self):
        """
        Draw the game surface onto the display.
        """
        # Scale and blit the game surface onto the display
        scaled_surface = pygame.transform.scale(self.surface, self.screen_scaled)
        self.display.blit(scaled_surface, self.screen_gap)

        # Update the display
        pygame.display.flip()
