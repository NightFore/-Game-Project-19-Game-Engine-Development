# ui_manager.py

import pygame
from typing import Optional
from menu_config import menu_config
from engine.base_manager import BaseManager
from engine.ui_element import UIElement


class UIManager(BaseManager):
    """
    UIManager handles the user interface components, such as buttons and menus.

    Attributes:
        Common Attributes:
            - config (dict): Configuration dictionary loaded from config.json.

        UIManager Attributes:
            - default_font_name (str): Name of the default font.
            - default_font_size (int): Size of the default font.
            - ui_elements (dict):
            - current_menu (str): Name of the currently loaded menu.
            - display (pygame.Surface): Surface for rendering UI components.
            - font (pygame.font.Font): Pygame font object for rendering text.

    Methods:
        Instance Setup:
            - load_specific_components(): Load specific components based on the configuration.
            - set_display(): Set the display surface for rendering UI components.

        Menu Management:
            - load_menu(menu_name): Load a menu from configuration.

        Game Loop:
            - update(mouse_pos, mouse_clicks): Update the UI state.
            - draw(): Render the UI frame.
    """
    def __init__(self):
        """
        Initialize the UIManager instance.
        """
        super().__init__()

        # Common Attributes
        self.config = {
            "default_font_name": Optional[str],
            "default_font_size": Optional[int]
        }

        # UIManager Attributes
        self.default_font_name = Optional[str]
        self.default_font_size = Optional[int]
        self.ui_elements = Optional[dict]
        self.current_menu = Optional[str]
        self.display = Optional[pygame.Surface]
        self.font = Optional[pygame.font.Font]

    """
    Instance Setup
        - load_specific_components
        - set_display
    """
    def load_specific_components(self):
        """
        Load specific components based on the configuration.
        """
        #
        self.default_font_name = self.config['default_font_name']
        self.default_font_size = self.config['default_font_size']

        #
        self.ui_elements = {}
        self.current_menu = None
        self.display = None
        self.font = pygame.font.Font(self.default_font_name, self.default_font_size)

    def set_display(self, display):
        """
        Set the display surface for rendering UI components.

        Args:
            display (pygame.Surface): The display surface to set.
        """
        self.display = display

    """
    Menu Management
        - load_menu
    """
    def load_menu(self, menu_name):
        """
        Load a menu from configuration.

        Args:
            menu_name (str): Name of the menu to load.
        """
        # Check if the specified menu name exists in the UI configuration
        if menu_name in menu_config:
            self.current_menu = menu_name
            self.ui_elements = {}

            for element_type, elements in menu_config[menu_name].items():
                for element_id, config in elements.items():
                    self.ui_elements[element_id] = UIElement(config, element_type, element_id,
                                                             self.managers, self.logger)
        else:
            self.log_error(f"Menu '{menu_name}' does not exist in the configuration.",
                           ValueError)

    """
    Game Loop
        - update
        - draw
    """
    def update(self, mouse_pos, mouse_clicks):
        """
        Update the game state.

        Args:
            mouse_pos: Current position of the mouse.
            mouse_clicks: List of mouse click states.
        """
        for element in self.ui_elements.values():
            if element.is_hovered(mouse_pos) and mouse_clicks[1]:
                element.click()

    def draw(self):
        """
        Render the game frame.
        """
        if self.display:
            for element in self.ui_elements.values():
                element.draw(self.display)
