# window_manager.py

import pygame
import os
from pygame.locals import *


class WindowManager(pygame.Surface):
    """
    WindowManager manages the game window and its display modes.

    Attributes:
        Game Settings Attributes:
            - window_title (str): The title of the game project.
            - game_size (tuple): The size of the game window in (width, height).

        Display Settings Attributes:
            - screen_info (pygame.Surface): Information about the display's capabilities.
            - screen_scaled (tuple): The scaled screen resolution for maintaining aspect ratio.
            - screen_gap (tuple): Gap used to center the game surface when zoomed.
            - display_factor (float): Factor used for scaling the display.
            - display (pygame.Surface): The game window surface.

        Flags Attributes:
            - flags (int): Flags for the display mode.
            - is_fullscreen (bool): Indicates if the game is in fullscreen mode.
            - is_zoom (bool): Indicates if the game is in zoom mode.

    Example:
        # Create a WindowManager instance with the specified project title and size.
        window_manager = WindowManager()
        window_manager.create_window_instance("My Game", (800, 600))

        # Main game loop setup
        clock = pygame.time.Clock()
        running = True

        # Toggle fullscreen mode.
        window_manager.toggle_fullscreen()

        # Toggle zoom mode.
        window_manager.toggle_zoom()

        # Main game loop
        while running:
            for event in pygame.event.get():
                # Handle window resizing event
                if event.type == VIDEORESIZE:
                    window_manager.resize()

            # Get the current frame rate
            frame_rate = clock.get_fps()

            # Update the display and draw the game
            window_manager.update(frame_rate)
            window_manager.draw()

    Methods:
        Initialization:
            - create_window_instance(window_title, size): Create a window instance with the specified size.

        Display Management:
            - toggle_fullscreen(): Toggle between fullscreen and windowed mode.
            - toggle_zoom(): Toggle between zoom and original size mode.

        Size Management:
            - resize(): Resize the game window while considering zoom and screen width.
            - update_display_mode(toggle_fullscreen, toggle_zoom, flags, resize): Update the game window.
            - adjust_aspect_ratio(): Adjust the aspect ratio for maintaining proper scaling during resizing.

        Input Handling:
            - get_adjusted_mouse_position(): Get the adjusted mouse position based on display_factor.

        Render:
            - update(frame_rate): Update the display with the current frame rate.
            - draw(): Draw the game surface onto the screen.
    """

    def __init__(self):
        """
        Initialize the WindowManager instance.
        """
        super().__init__((0, 0))

        # Set the environment variable to center the game window.
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Retrieve information about the display's capabilities.
        self.screen_info = pygame.display.Info()

        # Initialize the display window with a hidden mode.
        self.display_factor = 1
        self.display = pygame.display.set_mode((0, 0), HIDDEN)

        #

        self.window_title = None
        self.game_size = None
        self.screen_scaled = None
        self.screen_gap = None
        self.flags = None
        self.is_resizable = True
        self.is_fullscreen = None
        self.is_zoom = None

        self.logger = None

    """
    Initialization
        - create_window_instance
        - set_title
        - set_size
        - set_flags
        - set_logger
    """
    def create_window_instance(self, window_title="", size=(800, 600), flags=0, logger=None):
        """
        Create a window instance.

        Args:
            window_title (str): The title of the window.
            size (tuple): Size of the window in (width, height).
            flags (int or None): Flags for display mode.
            logger (GameLogger or None): Logger instance for logging events.

        Returns:
            pygame.Surface: The created window instance.
        """
        # Initialize the window surface with the given size
        super().__init__(size)

        # Set
        self.set_title(window_title)
        self.set_size(size)
        self.set_flags(flags)
        self.set_logger(logger)

        # Update display mode based on initial settings
        self.update_display_mode()

        # Return the instance of the created window
        return self

    def set_title(self, window_title):
        """
        Set the title of the window.

        Args:
            window_title (str): The title of the window.
        """
        self.window_title = window_title
        pygame.display.set_caption(self.window_title)

    def set_size(self, size):
        """
        Set the size of the window.

        Args:
            size (tuple): Size of the window in (width, height).
        """
        self.game_size = size
        self.screen_scaled = self.game_size
        self.screen_gap = (0, 0)

    def set_flags(self, flags):
        """
        Set the display flags of the window.

        Args:
            flags (int or None): Flags for display mode.
        """
        self.flags = flags
        self.is_fullscreen = bool(flags & FULLSCREEN)
        self.is_resizable = bool(flags & RESIZABLE)
        self.is_zoom = False

    def set_logger(self, logger):
        """
        Set the logger instance.

        Args:
            logger (GameLogger or None): Logger instance for logging events.
        """
        self.logger = logger

    """
    Display flags Management
        - toggle_fullscreen
        - toggle_resizable
        - toggle_zoom
    """
    def toggle_fullscreen(self):
        """
        Toggle the fullscreen flag.
        """
        # Toggle the fullscreen mode
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            # Switch to fullscreen mode
            self.flags |= FULLSCREEN
            self.flags &= ~RESIZABLE  # Ensure resizable is turned off if fullscreen is on

            # Reset screen properties
            self.screen_gap = 0, 0
            self.screen_scaled = self.game_size
        else:
            # Switch to windowed mode
            self.flags &= ~FULLSCREEN

            # Restore resizable flag if previously set
            if self.is_resizable:
                self.flags |= RESIZABLE

        # Log the action if logger is defined
        if self.logger:
            action = "enabled" if self.is_fullscreen else "disabled"
            self.logger.info(f"Fullscreen mode {action}")

        """
        WIP
        """
        # Calculate screen dimensions
        screen_w = self.screen_scaled[0] + self.screen_gap[0] * 2
        screen_h = self.screen_scaled[1] + self.screen_gap[1] * 2

        # Set the display mode with the calculated dimensions and provided flags.
        self.display = pygame.display.set_mode((screen_w, screen_h), self.flags)

    def toggle_resizable(self):
        """
        Toggle the resizable flag.
        """
        # Toggle the resizable mode
        self.is_resizable = not self.is_resizable

        if self.is_resizable:
            # Switch to resizable mode
            self.flags |= RESIZABLE
            self.flags &= ~FULLSCREEN  # Ensure fullscreen is turned off if resizable is on
        else:
            # Switch to windowed mode
            self.flags &= ~RESIZABLE

        # Log the action if logger is defined
        if self.logger:
            action = "enabled" if self.is_resizable else "disabled"
            self.logger.info(f"Resizable mode {action}")

        """
        WIP
        """
        # Calculate screen dimensions
        screen_w = self.screen_scaled[0] + self.screen_gap[0] * 2
        screen_h = self.screen_scaled[1] + self.screen_gap[1] * 2

        # Set the display mode with the calculated dimensions and provided flags.
        self.display = pygame.display.set_mode((screen_w, screen_h), self.flags)

    def toggle_zoom(self):
        """
        Toggle the zoom flag.
        """
        # Toggle the zoom mode
        self.is_zoom = not self.is_zoom

        if self.is_zoom:
            # Adjust screen_gap when zoom is enabled to center the game surface.
            self.screen_gap = int((self.screen_info.current_w - self.screen_scaled[0]) / 2), self.screen_gap[1]
        else:
            # Reset screen properties
            self.screen_gap = 0, 0
            self.screen_scaled = self.game_size

        # Log the action if logger is defined
        if self.logger:
            action = "enabled" if self.is_zoom else "disabled"
            self.logger.info(f"Zoom mode {action}")

        """
        WIP
        """
        # Calculate screen dimensions
        screen_w = self.screen_scaled[0] + self.screen_gap[0] * 2
        screen_h = self.screen_scaled[1] + self.screen_gap[1] * 2

        # Set the display mode with the calculated dimensions and provided flags.
        self.display = pygame.display.set_mode((screen_w, screen_h), self.flags)

    """
    Size Management
        - adjust_aspect_ratio
        - update_display_mode
        - resize
    """
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

        # The inequality signs' order decides size reduction (current) or increase in one-sided resizing.
        if sap < gap:
            # To maintain the aspect ratio, divide the height by the width scaling factor.
            self.display_factor = ss[0] / gs[0]
            self.screen_scaled = ss[0], int(gs[1] * self.display_factor)
        elif sap > gap:
            # To maintain the aspect ratio, divide the width by the height scaling factor.
            self.display_factor = ss[1] / gs[1]
            self.screen_scaled = int(gs[0] * self.display_factor), ss[1]

    def update_display_mode(self, toggle_fullscreen=False, toggle_zoom=False, flags=None, resize=True):
        """
        Update the game window.

        Args:
            toggle_fullscreen (bool): Toggle fullscreen mode.
            toggle_zoom (bool): Toggle zoom mode.
            flags (int or None): Flags for display mode.
            resize (bool): Whether to resize the window.
        """
        # Calculate the scaled resolution and adjust window properties accordingly.
        self.adjust_aspect_ratio()

        # Toggle fullscreen mode if requested and not in zoom mode.
        if toggle_fullscreen and not self.is_zoom:
            self.toggle_fullscreen()
            resize = True

        # Toggle zoom mode if requested and not in fullscreen mode.
        elif toggle_zoom and not self.is_fullscreen:
            self.toggle_zoom()
            resize = True

        # Update display flags if provided.
        if flags is not None:
            self.flags = flags

        # Resize the display window if requested.
        if resize:
            # Calculate screen dimensions
            screen_w = self.screen_scaled[0] + self.screen_gap[0] * 2
            screen_h = self.screen_scaled[1] + self.screen_gap[1] * 2

            # Set the display mode with the calculated dimensions and provided flags.
            self.display = pygame.display.set_mode((screen_w, screen_h), self.flags)

    def resize(self):
        """
        Resize the game window while considering zoom and screen width.
        """
        # Detect zoom
        detect_zoom = False
        if self.is_zoom or self.display.get_width() == self.screen_info.current_w:
            detect_zoom = True

        # Update the display mode to reflect resizing changes
        self.update_display_mode(toggle_zoom=detect_zoom, resize=True)

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
        pygame.display.set_caption(f"{self.window_title} ({int(frame_rate)} FPS)")

    def draw(self):
        """
        Draw the game surface onto the screen.
        """
        # Add game to screen with the scaled size and gap required.
        self.display.blit(pygame.transform.scale(self, self.screen_scaled), self.screen_gap)
        pygame.display.flip()
