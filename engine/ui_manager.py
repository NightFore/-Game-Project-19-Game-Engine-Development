# ui_manager.py

import pygame
from typing import Optional
from button import Button
from button_config import button_config
from engine.base_manager import BaseManager


class UIManager(BaseManager):
    """
    UIManager handles the user interface components, such as buttons and menus.

    Attributes:
        Common Attributes:
            - config (dict): Configuration dictionary loaded from config.json.

        UI Attributes:
            - default_font_name (str): Name of the default font.
            - default_font_size (int): Size of the default font.
            - font (pygame.font.Font): Pygame font object for rendering text.
            - display (pygame.Surface): Surface for rendering UI components.
            - buttons (dict): Dictionary of button instances with button IDs as keys.
            - current_menu (str): Name of the currently loaded menu.

    Methods:
        Instance Setup:
            - load_specific_components(): Load specific components based on the configuration.

        Menu Management:
            - load_menu(menu_name): Load a menu from configuration.
            - resolve_action(action_str): Resolve action string to a callable function with arguments.
            - parse_arguments(args_str): Parse a string of arguments into a tuple of arguments.

        Game Control:
            - start_game(): Switch to the main menu.

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

        # UI Attributes
        self.default_font_name = Optional[str]
        self.default_font_size = Optional[int]
        self.font = Optional[pygame.font.Font]
        self.display = Optional[pygame.Surface]
        self.buttons = Optional[dict]
        self.current_menu = Optional[str]

    """
    Instance Setup
        - load_specific_components
    """
    def load_specific_components(self):
        """
        Load specific components based on the configuration.
        """
        self.default_font_name = self.config['default_font_name']
        self.default_font_size = self.config['default_font_size']
        self.font = pygame.font.Font(self.default_font_name, self.default_font_size)
        self.buttons = {}
        self.current_menu = None

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
        - resolve_action
        - parse_arguments
    """
    def load_menu(self, menu_name):
        """
        Load a menu from configuration.

        Args:
            menu_name (str): Name of the menu to load.
        """
        self.current_menu = menu_name
        self.buttons = {}

        # Check if the specified menu name exists in the button configuration
        if menu_name in button_config:
            # Iterate through each button configuration in the specified menu
            for button_id, config in button_config[menu_name].items():
                # Extract button properties from the configuration
                x = config['x']
                y = config['y']
                width = config['width']
                height = config['height']
                label = config['label']
                color = config['color']
                action_str = config.get('action')

                # Resolve the action string to a callable function or default action
                action = self.resolve_action(action_str, button_id)

                # Create a Button instance with the extracted properties and action
                button = Button(x, y, width, height, label, color, self.font, action)

                # Store the created button instance in the buttons dictionary using button_id as the key
                self.buttons[button_id] = button
        else:
            # Log a warning if the specified menu name does not exist in the button configuration
            self.log_warning(f"Menu '{menu_name}' does not exist in the button configuration.")

    def resolve_action(self, action_str, button_id):
        """
        Resolve action string to a callable function with arguments.

        Args:
            action_str (str): String representing the action to resolve.
            button_id (str): ID of the button to associate with the action.

        Returns:
            Callable function corresponding to the action string with arguments,
            or a default function that logs a warning if the action is not defined.
        """
        # If no action string is provided, return None
        if not action_str:
            return None

        try:
            # Split the action string to extract method name and arguments
            action_parts = action_str.split('(', 1)
            method_str = action_parts[0].strip()

            # Remove trailing ')'
            args_str = action_parts[1][:-1] if len(action_parts) > 1 else ''

            # Convert arguments string into a tuple
            args = self.parse_arguments(args_str)

            # Handle nested method calls (e.g., manager.method)
            method_parts = method_str.split('.')
            if len(method_parts) > 1:
                # Method is in a nested manager
                obj = self
                for part in method_parts[:-1]:
                    obj = getattr(obj, part, None)
                    if obj is None:
                        self.log_warning(f"Manager or method '{'.'.join(method_parts[:-1])}' not found.")
                        return lambda: self.default_action(button_id)
                method_name = method_parts[-1]
                if hasattr(obj, method_name):
                    method = getattr(obj, method_name)
                    return lambda: method(*args)
                else:
                    self.log_warning(f"Method '{method_name}' not found in manager '{'.'.join(method_parts[:-1])}'.")
                    return lambda: self.default_action(button_id)
            else:
                # Direct method on UIManager
                if hasattr(self, method_str):
                    method = getattr(self, method_str)
                    return lambda: method(*args)
                else:
                    self.log_warning(f"Method '{method_str}' not found in UIManager.")
                    return lambda: self.default_action(button_id)
        except Exception as e:
            self.log_error(f"Error resolving action '{action_str}': {e}")
            return lambda: self.default_action(button_id)

    def default_action(self, button_id):
        """
        Default action to be used when a button action is not defined.

        Args:
            button_id (str): The ID of the button that triggered this action.
        """
        self.log_warning(f"Action for button '{button_id}' is not defined.")

    @staticmethod
    def parse_arguments(args_str):
        """
        Parse a string of arguments into a tuple of arguments.

        Args:
            args_str (str): String representing arguments in the format 'arg1, arg2, ...'

        Returns:
            Tuple of parsed arguments.
        """
        import ast

        try:
            args = ast.literal_eval(f"({args_str})")
            return args if isinstance(args, tuple) else (args,)
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing arguments '{args_str}': {e}")
            return ()

    """
    Game Control
        - start_game
    """
    def start_game(self):
        """
        Switch to the main menu.
        """
        self.load_menu('main_menu')

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
        for button_id, button in self.buttons.items():
            if button.is_hovered(mouse_pos) and mouse_clicks[1]:
                button.click()

    def draw(self):
        """
        Render the game frame.
        """
        if self.display:
            for button in self.buttons.values():
                button.draw(self.display)
