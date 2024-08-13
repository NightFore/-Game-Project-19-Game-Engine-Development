# ui_element.py

import pygame
from utils import setup_managers


class UIElement:
    """
    UIElement represents a graphical interface component.

    Attributes:
        Common Attributes:
            - config (dict): Configuration dictionary for the element.
            - element_type (str): The type of the UI element (e.g., 'button', 'image').
            - element_id (str): ID of the UI element.
            - managers (dict): Dictionary of manager instances.
            - logger (Logger): Logger instance for logging.

        Positional Attributes:
            - x (int): The x-coordinate of the UI element.
            - y (int): The y-coordinate of the UI element.
            - width (int): The width of the UI element.
            - height (int): The height of the UI element.

        Text Attributes:
            - label (str or None): The text label of the UI element.
            - font_name (str or None): The name of the font for the label.
            - font_size (int): The font size of the label.
            - color (tuple): The color of the UI element's text in RGB format.

        Image Attributes:
            - image_path (str or None): The file path of the image used for the UI element.

        Action Attributes:
            - action_str (str or None): The string representing the action to resolve.

        Pygame Objects:
            - font (pygame.font.Font or None): The font object used for rendering text.
            - image (pygame.Surface or None): The surface object for the image.
            - rect (pygame.Rect): The rectangle defining the element's position and size.
            - text_rect (pygame.Rect or None): The rectangle defining the position of the text.
            - text_surface (pygame.Surface or None): The surface object for the rendered text.
            - surface (pygame.Surface or None): The surface object used for drawing the element.

    Methods:
        Instance Setup:
            - setup_graphics(): Set up graphical properties for the UI element.

        Action Resolution:
            - resolve_action(action_str): Resolve the action string to a callable function.
            - default_action(): Default action when no action is defined.
            - parse_arguments(args_str): Parse a string of arguments into a tuple.

        Interaction:
            - is_hovered(mouse_pos): Check if the UI element is hovered by the mouse.
            - click(): Trigger the action associated with the UI element when clicked.

        Game Loop:
            - update(): Update the UI element's state.
            - draw(surface): Draw the UI element on the given surface.
    """
    def __init__(self, config, element_type, element_id, managers, logger):
        """
        Initialize the UIElement.

        Args:
            config (dict): Configuration dictionary for the element.
            element_type (str): The type of the UI element (e.g., 'button', 'image').
            element_id (str): ID of the UI element.
            managers (dict): Dictionary of manager instances.
            logger (Logger): Logger instance for logging.
        """
        # Store provided arguments
        self.config = config
        self.element_type = element_type
        self.element_id = element_id
        self.managers = managers
        self.logger = logger

        # Set up references to managers using the helper function
        setup_managers(self, managers)

        # Positional Attributes
        self.x = config['x']
        self.y = config['y']
        self.width = config['width']
        self.height = config['height']

        # Text Attributes
        self.label = config.get('label')
        self.font_name = config.get('font_name')
        self.font_size = config.get('font_size')
        self.color = config.get('color')

        # Image Attributes
        self.image_path = config.get('image')

        # Action Attributes
        self.action_str = config.get('action')

        # Initialize graphical properties
        self.font = None
        self.image = None
        self.rect = None
        self.text_rect = None
        self.text_surface = None
        self.surface = None

        # Debug (To Be Deleted)
        self.font_name = None
        self.font_size = 36
        self.font = pygame.font.Font(self.font_name, self.font_size)

        # Set up the graphical elements
        self.setup_graphics()

        # Resolve the action associated with this UI element
        self.action = self.resolve_action(self.action_str)

    """
    Instance Setup
        - setup_graphics
    """
    def setup_graphics(self):
        """
        Set up graphical properties for the UI element, such as images, rectangles, fonts, and colors.
        """
        # Load image if specified
        if self.image_path:
            try:
                self.image = pygame.image.load(self.image_path)
                self.rect = self.image.get_rect(topleft=(self.x, self.y))
                self.logger.log_info(f"Image loaded for {self.element_id} from {self.image_path}.")
            except pygame.error as e:
                self.logger.log_error(f"Failed to load image for {self.element_id} from {self.image_path}: {e}")
                self.image = None
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else:
            self.image = None
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Set up label and font if specified
        if self.label and self.font_name:
            self.font = pygame.font.Font(self.font_name, self.font_size)
            self.text_surface = self.font.render(self.label, True, self.color)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        else:
            self.text_surface = None
            self.text_rect = None

        # Set up color if specified and no image is loaded
        if not self.image and self.color:
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill(self.color)
        else:
            self.surface = None
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
        Check if the UI element is currently hovered by the mouse.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse cursor.

        Returns:
            bool: True if the mouse is hovering over the element, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        """
        Trigger the action associated with the UI element when it is clicked.
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
        Update the UI element's state based on mouse interactions.

        Args:
            mouse_pos (tuple): Current position of the mouse.
            mouse_clicks (list): List of mouse click states.
        """
        if self.is_hovered(mouse_pos) and mouse_clicks[1]:
            self.click()

    def draw(self, surface):
        """
        Draw the UI element on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the UI element on.
        """
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
            if self.label and self.font:
                text_surface = self.font.render(self.label, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=self.rect.center)
                surface.blit(text_surface, text_rect)
