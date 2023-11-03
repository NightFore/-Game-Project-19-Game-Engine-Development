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
            - text (str): The text content to be displayed.
            - text_surface (Surface): The surface containing the rendered text.
            - text_rect (Rect): The rectangle that defines the boundaries of the text.
            - align (str): The alignment of the instance.

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
            - set_align(str): Set the alignment of the instance within its bounding rectangle.
            - update_rect: Update the instance's bounding rectangle.

        Text Management:
            - set_text(text): Set the text content.
            - set_font_size(size): Set the font size.
            - update_text: Update the rendered text and its rectangle.

        Render:
            - update(): Update the instance.
            - draw(): Draw the instance.
    """
    def __init__(self, instance_data, managers):
        # Call the constructor of the parent class (TemplateInstance)
        super().__init__(instance_data, managers)

        # Initialize instance variables
        self.pos = (0, 0)
        self.text = ""

        # Font attributes
        self.font = instance_data.get("font", None)
        self.font_size = instance_data.get("size", None)
        self.font_color = instance_data.get("color", None)
        self.font_path = instance_data.get("file_path", None)

        # Set the initial text_surface and text_rect
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect()

        # Set the initial alignment
        self.align = instance_data.get("align", None)
        self.set_align(self.align)


    """
    Rect Management:
        - set_pos
        - set_align
        - update_rect
    """
    def set_pos(self, pos):
        """
        Set the position of the instance.
        """
        self.pos = pos
        self.update_rect()

    def set_align(self, align):
        """
        Set the alignment of the instance within its bounding rectangle.
        """
        self.align = align
        self.update_rect()

    def update_rect(self):
        """
        Update the instance's bounding rectangle.
        """
        if self.align == "center":
            self.text_rect.center = self.pos
        if self.align == "nw":
            self.text_rect.topleft = self.pos
        if self.align == "ne":
            self.text_rect.topright = self.pos
        if self.align == "sw":
            self.text_rect.bottomleft = self.pos
        if self.align == "se":
            self.text_rect.bottomright = self.pos
        if self.align == "n":
            self.text_rect.midtop = self.pos
        if self.align == "s":
            self.text_rect.midbottom = self.pos
        if self.align == "e":
            self.text_rect.midright = self.pos
        if self.align == "w":
            self.text_rect.midleft = self.pos


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
