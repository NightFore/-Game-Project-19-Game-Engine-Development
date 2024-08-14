# ui_element.py

import pygame
from utils import setup_managers


class UIElement:
    """
    UIElement represents a graphical interface component.

    Attributes:
        Common Attributes:
            - element_type (str): The type of the UI element (e.g., 'button', 'image').
            - element_id (str): ID of the UI element.
            - config (dict): Configuration dictionary for the element.
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

        Game Loop:
            - update(): Update the UI element's state.
            - draw(surface): Draw the UI element on the given surface.
    """
    def __init__(self, element_type, element_id, config, managers, logger):
        """
        Initialize the UIElement.

        Args:
            element_type (str): The type of the UI element (e.g., 'button', 'image').
            element_id (str): ID of the UI element.
            config (dict): Configuration dictionary for the element.
            managers (dict): Dictionary of manager instances.
            logger (Logger): Logger instance for logging.
        """
        # Store provided arguments
        self.element_type = element_type
        self.element_id = element_id
        self.config = config
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
    Game Loop
        - update
        - draw
    """
    def update(self, mouse_pos, mouse_clicks):
        """
        Update the UI element's state based on mouse interactions.
        """
        pass

    def draw(self, surface):
        """
        Draw the UI element on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the UI element on.
        """

        if self.image:
            surface.blit(self.image, self.rect)
        elif self.surface:
            surface.blit(self.surface, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        if self.label and self.font:
            text_surface = self.font.render(self.label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
