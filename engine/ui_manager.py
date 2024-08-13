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
            - ui_elements (dict): Dictionary of UI elements, keyed by their IDs.
            - current_menu (str): Name of the currently loaded menu.
            - display (pygame.Surface): Surface for rendering UI components.

    Methods:
        Instance Setup:
            - load_specific_components(): Load specific components based on the configuration.
            - set_display(display): Set the display surface for rendering UI components.

        Menu Management:
            - load_menu(menu_name): Load a menu from configuration.

        Game Loop:
            - update(mouse_pos, mouse_clicks): Update the UI state based on mouse interactions.
            - draw(): Render the UI elements on the display surface.
    """
    def __init__(self):
        """
        Initialize the UIManager instance.
        """
        super().__init__()

        # Common Attributes
        self.config = {
        }

        # UIManager Attributes
        self.default_font_name = Optional[str]
        self.default_font_size = Optional[int]
        self.ui_elements = Optional[dict]
        self.current_menu = Optional[str]
        self.display = Optional[pygame.Surface]

    """
    Instance Setup
        - load_specific_components
        - set_display
    """
    def load_specific_components(self):
        """
        Load specific components based on the configuration.
        """
        # Set Manager attributes
        self.ui_elements = {}
        self.current_menu = None
        self.display = None

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

            # Iterate over the elements in the menu configuration and initialize UIElements
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
        Update the UI state based on mouse interactions.

        Args:
            mouse_pos (tuple): Current position of the mouse.
            mouse_clicks (list): List of mouse click states.
        """
        # Iterate over each UI element and check for hover and click interactions
        for element in self.ui_elements.values():
            element.update(mouse_pos, mouse_clicks)

    def draw(self):
        """
        Render the UI elements on the display surface.
        """
        if self.display:
            # Draw each UI element on the display surface
            for element in self.ui_elements.values():
                element.draw(self.display)
