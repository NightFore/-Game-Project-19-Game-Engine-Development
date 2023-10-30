# graphic_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class TextManager(TemplateManager):
    """
    TextManager manages text resources and their instances in the game.
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

        Inherited from TemplateInstance:

    Methods:
    - Render
        - update(): Update the graphic instance.
        - draw(): Draw the graphic instance.
    """
    def __init__(self, data, managers):
        super().__init__(data, managers)

        self.font = data.get("font", None)
        self.font_size = data.get("size", None)
        self.font_color = data.get("color", None)

    def set_text(self, text):
        self.text = str(text)
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center



    """
    Render
        - update
        - draw
    """
    def update(self):
        """
        Update the text instance
        """
        super().update()

    def draw(self):
        """
        Draw the text instance.
        """
        super().draw()

        self.screen.blit(self.text_surface, self.text_rect)
