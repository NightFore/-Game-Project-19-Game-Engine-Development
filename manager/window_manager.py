# window_manager.py

import pygame
import os
from pygame.locals import *

class WindowManager(pygame.Surface):
    def __init__(self):
        """
        Initialize the WindowManager instance.
        """
        # Set the environment variable to center the game window.
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Retrieve information about the display's capabilities.
        self.screen_info = pygame.display.Info()

        # Initialize the display window with a hidden mode.
        self.display = pygame.display.set_mode((0, 0), HIDDEN)

    def create_window_instance(self, project_title, size):
        """
        Create a window instance with the specified size.

        Args:
            project_title (str): The title of the game project.
            size (tuple): Size of the window in (width, height).

        Returns:
            pygame.Surface: The created window instance.
        """
        # Initialize the project title.
        self.project_title = project_title

        # Initialize screen properties
        self.game_size = size
        self.screen_scaled = self.game_size
        self.screen_gap = (0, 0)

        # Initialize window mode
        self.is_fullscreen = False
        self.is_zoom = False

        # Initialize the display scaling factor.
        self.display_factor = 1

        # Set caption and create the game window
        pygame.display.set_caption(self.project_title)
        self.update_display_mode()

        # Call the constructor of the parent class (pygame.Surface).
        pygame.Surface.__init__(self, size)

        # Return the instance of the created window.
        return self

    def update_display_mode(self, flags=RESIZABLE):
        """
        Create the game window with the specified size.

        Args:
            flags (int): Flags for display mode.
        """
        # Calculate the scaled resolution and adjust window properties accordingly.
        self.adjust_aspect_ratio()

        # Adjust screen_gap if zoom is enabled to center the game surface.
        if self.is_zoom:
            self.screen_gap = int((self.screen_info.current_w - self.screen_scaled[0]) / 2), self.screen_gap[1]

        # Calculate screen dimensions
        screen_w = self.screen_scaled[0] + self.screen_gap[0] * 2
        screen_h = self.screen_scaled[1] + self.screen_gap[1] * 2

        # Set the display mode with the calculated dimensions and provided flags.
        self.display = pygame.display.set_mode((screen_w, screen_h), flags)

    def adjust_aspect_ratio(self):
        """
        Adjust the aspect ratio for maintaining proper scaling during resizing.

        Returns:
            tuple: Scaled resolution.
        """
        # Get the display and game screen sizes
        ss = self.display.get_size()
        gs = self.game_size

        # Calculate the display and game aspect ratios
        sap = ss[0] / ss[1]
        gap = gs[0] / gs[1]

        # The order of the inequality signs determines whether, during a one-sided resizing,
        # the window size is reduced (as currently implemented) or increased.
        if sap < gap:
            # To maintain the aspect ratio, divide the height by the width scaling factor.
            self.display_factor = ss[0] / gs[0]
            self.screen_scaled = ss[0], int(gs[1] * self.display_factor)
        elif sap > gap:
            # To maintain the aspect ratio, divide the width by the height scaling factor.
            self.display_factor = ss[1] / gs[1]
            self.screen_scaled = int(gs[0] * self.display_factor), ss[1]

    def toggle_fullscreen(self):
        """
        Toggle between fullscreen and windowed mode.
        """
        if not self.is_fullscreen:
            # Switch to fullscreen mode
            self.is_fullscreen = True
            self.is_zoom = False
            self.screen_gap = 0, 0
            self.screen_scaled = self.game_size
            self.display = pygame.display.set_mode(self.game_size, FULLSCREEN)
            self.factor_w = 1
            self.factor_h = 1
        else:
            # Switch to windowed mode
            self.is_fullscreen = False
            self.resize()

    def toggle_zoom(self, enable_zoom=None):
        """
        Toggle between zoom and original size mode, or set the zoom mode based on the enable_zoom argument.

        Args:
            enable_zoom (bool or None): True to enable zoom, False to disable, None to toggle.
        """
        if enable_zoom is None:
            # Toggle the zoom mode
            self.is_zoom = not self.is_zoom
        else:
            # Set the zoom mode based on the enable_zoom argument
            self.is_zoom = enable_zoom

        # Reset screen properties if zoom is disabled
        if not self.is_zoom:
            self.screen_gap = 0, 0
            self.screen_scaled = self.game_size

        # Update the display mode to reflect the changes
        if enable_zoom is not None:
            self.update_display_mode()

    def resize(self):
        """
        Resize the game window while considering zoom and screen width.
        """
        # Detect zoom
        if self.is_zoom or self.display.get_width() == self.screen_info.current_w:
            self.toggle_zoom()

        # Update the display mode to reflect resizing changes
        self.update_display_mode()

    def update(self, frame_rate):
        """
        Update the display.

        Args:
            frame_rate (int): Current frame rate in frames per second.
        """
        # Display the current FPS in the window title
        pygame.display.set_caption(f"{self.project_title} ({int(frame_rate)} FPS)")

    def draw(self):
        """
        Draw the game surface onto the screen.
        """
        # Add game to screen with the scaled size and gap required.
        self.display.blit(pygame.transform.scale(self, self.screen_scaled), self.screen_gap)
        pygame.display.flip()



"""
Unused
"""
# import ctypes
# from ctypes import wintypes

# def get_taskbar_height():
#     taskbar_hwnd = ctypes.windll.user32.FindWindowW(u"Shell_TrayWnd", None)
#     rect = wintypes.RECT()
#     ctypes.windll.user32.GetWindowRect(taskbar_hwnd, ctypes.byref(rect))
#     return rect.bottom - rect.top

# def get_window_title_bar_size():
#     title_bar_height = ctypes.windll.user32.GetSystemMetrics(4)  # SM_CYCAPTION
#     border_height = ctypes.windll.user32.GetSystemMetrics(6)  # SM_CYSIZEFRAME
#     unknown_offset = -1
#     return title_bar_height + border_height + unknown_offset

# def get_total_window_height():
#     window_height = get_window_title_bar_size()
#     taskbar_height = get_taskbar_height()
#     return window_height + taskbar_height
