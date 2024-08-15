# ui_button.py

import pygame
from engine.ui_element import UIElement


class UIButton(UIElement):
    """
    UIButton represents a clickable button element in the UI.

    Attributes:
        Inherits from UIElement:
            - element_type (str): The type of the UI element.
            - element_id (str): ID of the UI element.
            - config (dict): Configuration dictionary for the element.
            - managers (dict): Dictionary of manager instances.
            - logger (Logger): Logger instance for logging.
            - x, y, width, height, label, font_name, font_size, color, image_path, action_str,
              font, image, rect, text_rect, text_surface, surface

        UIButton Attributes:
            - hover_color (tuple): Color when the button is hovered (optional).
            - default_color (tuple): Default color of the button.
            - action (Callable): The action to be executed when the button is clicked.

    Methods:
        Action Resolution:
            - resolve_action(action_str): Resolve the action string to a callable function with arguments.
            - default_action(): Defines a default action when the specified action cannot be found.
            - parse_arguments(args_str): Parses a string of arguments into a tuple of arguments.

        Interaction:
            - is_hovered(mouse_pos): Triggers the action associated with hovering over the button.
            - click(): Triggers the action associated with clicking the button.

        Game Loop:
            - update(mouse_pos, mouse_clicks): Updates the UIButton's state.
            - draw(surface): Draws the UIButton on the provided surface.
    """
    def __init__(self, element_id, config, managers, logger):
        """
        Initialize the UIButton.

        Args:
            element_id (str): ID of the UI element.
            config (dict): Configuration dictionary for the element.
            managers (dict): Dictionary of manager instances.
            logger (Logger): Logger instance for logging.
        """
        super().__init__('button', element_id, config, managers, logger)

        # UIButton Attributes
        self.hover_color = config.get('hover_color')
        self.default_color = self.color

        # Resolve the action associated with this button
        self.action = self.resolve_action(self.action_str)

    """
    Action Resolution
        - resolve_action
        - default_action
        - parse_arguments
    """
    def resolve_action(self, action_str):
        """
        Resolve the action string to a callable function with arguments.

        Args:
            action_str (str): String representing the action to resolve.

        Returns:
            Callable: Function corresponding to the action string with arguments.
        """
        if not action_str:
            return None

        try:
            action_parts = action_str.split('(', 1)
            method_str = action_parts[0].strip()
            args_str = action_parts[1][:-1] if len(action_parts) > 1 else ''
            args = self.parse_arguments(args_str)

            method_parts = method_str.split('.')
            if len(method_parts) > 1:
                # Resolve method in the context of managers
                obj = self
                for part in method_parts[:-1]:
                    obj = getattr(obj, part, None)
                    if obj is None:
                        self.logger.log_warning(f"Manager or method '{'.'.join(method_parts[:-1])}' not found.")
                        return lambda: self.default_action()
                method_name = method_parts[-1]
                if hasattr(obj, method_name):
                    method = getattr(obj, method_name)
                    return lambda: method(*args)
                else:
                    self.logger.log_warning(f"Method '{method_name}' not found in manager"
                                            f" '{'.'.join(method_parts[:-1])}'.")
                    return lambda: self.default_action()
            else:
                # Resolve method within the class itself
                if hasattr(self, method_str):
                    method = getattr(self, method_str)
                    return lambda: method(*args)
                else:
                    self.logger.log_warning(f"Method '{method_str}' not found in UIElement.")
                    return lambda: self.default_action()
        except Exception as e:
            self.logger.log_error(f"Error resolving action '{action_str}': {e}")
            return lambda: self.default_action()

    def default_action(self):
        """
        Default action to be used when an element action is not defined.
        """
        self.logger.log_warning(f"Action for element '{self.element_id}' is not defined.")

    @staticmethod
    def parse_arguments(args_str):
        """
        Parse a string of arguments into a tuple of arguments.

        Args:
            args_str (str): String representing arguments in the format 'arg1, arg2, ...'

        Returns:
            tuple: Tuple of parsed arguments.
        """
        import ast
        try:
            args = ast.literal_eval(f"({args_str})")
            return args if isinstance(args, tuple) else (args,)
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing arguments '{args_str}': {e}")
            return ()

    """
    Interaction
        - is_hovered
        - click
    """
    def is_hovered(self, mouse_pos):
        """
        Triggers the action associated with hovering over the button.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse cursor.

        Returns:
            bool: True if the mouse is hovering over the button, False otherwise.
        """
        hovered = self.rect.collidepoint(mouse_pos)
        if hovered and self.hover_color:
            self.surface.fill(self.hover_color)
        elif self.default_color:
            self.surface.fill(self.default_color)
        return hovered

    def click(self):
        """
        Triggers the action associated with clicking the button.
        """
        if self.action:
            self.action()

    """
    Game Loop
        - update
        - draw
    """
    def update(self, mouse_pos, mouse_clicks):
        """
        Update the UIButton state.

        Args:
            mouse_pos (tuple): Current position of the mouse.
            mouse_clicks (list): List of mouse click states.
        """
        super().update(mouse_pos, mouse_clicks)
        if self.is_hovered(mouse_pos) and mouse_clicks[1]:
            self.click()

    def draw(self, surface):
        """
        Draw the UIButton on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the UIButton on.
        """
        super().draw(surface)
