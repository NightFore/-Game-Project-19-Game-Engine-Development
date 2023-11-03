# graphic_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class TextManager(TemplateManager):
    """
    TextManager manages text resources and their instances in the game.

    Attributes:
        - resources (dict): A dictionary containing loaded resources.
        - instances (dict): A dictionary containing resource instances.
        - instance_class: The class used to create resource instances.
        - resource_types_to_load (list): A list of resource types to load for this manager.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries
        self.resources = {}
        self.instances = {}

        # Initialize the instance class for this manager
        self.instance_class = TextInstance

        # Define resource types to load for this manager
        self.resource_types_to_load = ["font"]




class TextInstance(TemplateInstance):
    """
    TextInstance represents an instance of a text resource.

    Attributes:
        Specific to TextInstance:
            - pos (tuple): The position (x, y) of the instance.
            - rect (Rect): The rectangle that defines the boundaries of the instance.
            - text (str): The text content to be displayed.
            - text_surface (Surface): The surface containing the rendered text.
            - text_rect (Rect): The rectangle that defines the boundaries of the text.

            Font Attributes:
                - font (Font): The font used for rendering the text.
                - font_size (int): The font size.
                - font_color (tuple): The color of the text.
                - font_path (str): The file path to the font.

        Inherited Attributes from TemplateInstance:
            - screen (pygame.Surface): The game display surface.

    Methods:
        Rect Management:
            - set_pos(tuple): Set the position of the instance.
            - update_rect: Update the instance's bounding rectangle.

        Text Management:
            - set_text(text): Set the text content.
            - set_font_size(size): Set the font size.
            - update_text: Update the rendered text and its rectangle.

        Render:
            - update(): Update the instance.
            - draw(): Draw the instance.
    """
    def __init__(self, data, managers):
        # Call the constructor of the parent class (TemplateInstance)
        super().__init__(data, managers)

        # Initialize instance variables
        self.pos = None
        self.rect = None
        self.text = None
        self.text_surface = None
        self.text_rect = None

        # Font attributes
        self.font = data.get("font", None)
        self.font_size = data.get("size", None)
        self.font_color = data.get("color", None)
        self.font_path = data.get("file_path", None)


    """
    Rect Management:
        - set_pos
        - update_rect
    """
    def set_pos(self, pos):
        """
        Set the position of the instance.
        """
        self.pos = pos
        self.update_rect()

    def update_rect(self):
        """
        Update the instance's bounding rectangle
        """
        if self.text_rect:
            self.text_rect.center = self.pos


    """
    Text Management:
        - set_text
        - set_font_size
        - update_text
    """
    def set_text(self, text):
        """
        Set the text content to be displayed.
        """
        self.text = text
        self.update_text()

    def set_font_size(self, size):
        """
        Set the font size.
        """
        self.font_size = size
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.update_text()

    def update_text(self):
        """
        Update the rendered text and its rectangle.
        """
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect()
        self.update_rect()


    """
    Render:
        - update
        - draw
    """
    def update(self):
        """
        Update the instance.
        """
        super().update()

    def draw(self):
        """
        Draw the instance.
        """
        super().draw()

        if self.text_rect:
            self.screen.blit(self.text_surface, self.text_rect)
