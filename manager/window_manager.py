# window_manager.py

import pygame
import os
from pygame.locals import *

MENU_BAR_HEIGHT = 120
FLAGS = RESIZABLE

class WindowManager(pygame.Surface):
    def __init__(self):
        """
        Initialize the WindowManager instance.
        """
        # Call the constructor of the parent class (pygame.Surface)
        super().__init__((800, 600))  # Default initial size

        # Screen Scaling
        self.screen_scaled = None

        # Window Resizing
        self.resize = True

        # Window Mode Settings
        self.is_fullscreen = False
        self.is_zoom = False

        # Scaling Factors
        self.factor_w = 1
        self.factor_h = 1

        # Other initializations
        self.parent = None
        self.project_title = ""
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.screen_gap = (0, 0)
        self.screen_size = (800, 600)
        self.screen_scaled = (800, 600)
        self.screen_info = pygame.display.Info()

    def create_window_instance(self, size, parent=None, project_title=None, FPS=None, first_screen=False):
        """
        Create a window instance with the specified size.

        Args:
            size (tuple): Size of the window.
            parent: The parent object.
            project_title (str): The title of the game project.
            FPS (int): Frames per second.
            first_screen (bool): Whether it's the first screen or not.

        Returns:
            pygame.Surface: The created window instance.
        """
        self.parent = parent
        if project_title:
            self.project_title = project_title
            pygame.display.set_caption(self.project_title)
        if FPS:
            self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.screen_gap = (0, 0)
        self.screen_size = size
        self.screen_scaled = size

        # Required to set a good resolution for the game screen
        self.screen_info = pygame.display.Info()

        if first_screen:
            self.screen_size = (self.screen_info.current_w, self.screen_info.current_h - MENU_BAR_HEIGHT)
            self.screen_scaled = self.screen_size
            self.create_game_window(self.screen_size)
        else:
            self.create_game_window(self.screen_size)

        # Returns the instance of the created window.
        return self

    def create_game_window(self, size, flags=FLAGS):
        """
        Create the game window with the specified size.

        Args:
            size (tuple): Size of the window.
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

    def toggle_fullscreen(self):
        """
        Toggle between fullscreen and windowed mode.
        """
        if not self.is_fullscreen:
            # Switch to fullscreen mode
            self.is_fullscreen = True
            self.is_zoom = False
            self.screen_gap = 0, 0
            self.screen_scaled = self.screen_size
            self.screen = pygame.display.set_mode(self.screen_size, FULLSCREEN)
            self.factor_w = 1
            self.factor_h = 1
        else:
            # Switch to windowed mode
            self.is_fullscreen = False
            self.window_resize()

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

        if self.is_zoom:
            screen_info = pygame.display.Info()
            ss = screen_info.current_w, screen_info.current_h
            self.screen_scaled = self.get_resolution(ss, self.screen_size)
            self.screen_gap = int((self.screen_info.current_w - self.screen_scaled[0]) / 2), self.screen_gap[1]
            self.is_fullscreen = False
        else:
            self.screen_gap = 0, 0
            self.screen_scaled = self.screen_size
        self.window_resize()

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
                self.resize = not (self.is_zoom and (ss[0] == self.screen_info.current_w or ss[0] == self.screen_scaled[0]))

        if ss[0] != self.screen_scaled[0] and ss[1] != self.screen_scaled[1]:
            self.resize = True

        screen_info = pygame.display.Info()

        print((screen_info.current_w, screen_info.current_h), self.screen_scaled, ss, [self.screen.get_width(), self.screen.get_height()])
        # Resize
        if self.resize:
            self.screen_scaled = self.get_resolution(ss, self.screen_size)

            # Detect zoom
            if ss[0] + self.screen_gap[0] == self.screen_info.current_w or self.is_zoom:
                self.toggle_zoom()
            else:
                self.window_resize()

    def window_resize(self):
        # Reset resize flag
        self.resize = False

        # Calculate screen dimensions
        screen_w = self.screen_scaled[0] + self.screen_gap[0] * 2
        screen_h = self.screen_scaled[1] + self.screen_gap[1] * 2

        # Calculate scaling factors
        self.factor_w = self.screen_scaled[0] / self.get_width()
        self.factor_h = self.screen_scaled[1] / self.get_height()

        # Update the game window size
        self.create_game_window((screen_w, screen_h))


    def draw(self):
        """
        Draw the game surface onto the screen.
        """
        # Add game to screen with the scaled size and gap required.
        self.screen.blit(pygame.transform.scale(self, self.screen_scaled), self.screen_gap)
        pygame.display.flip()



"""
Unused (Zoom related)
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