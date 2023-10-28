# graphic_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class GraphicManager(TemplateManager):
    """
    GraphicManager handles graphic resources and their instances in the game.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries to store resources and instances
        self.resources = {}
        self.instances = {}

        # Define resource types to load for this manager
        self.resource_types_to_load = ["image", "image_sequence", "interface", "button"]

        # Initialize manager-related attributes
        self.manager_specific_attribute = None

class Graphic(TemplateInstance):
    def __init__(self, data, managers):
        super().__init__(data, managers)

    def update(self):
        super().update()

    def draw(self):
        super().draw()
