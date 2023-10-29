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

        # Initialize the instance class for this manager
        self.instance_class = Graphic

        # Define resource types to load for this manager
        self.resource_types_to_load = ["image", "image_sequence", "interface", "button"]

        # Initialize manager-related attributes
        self.manager_specific_attribute = None

class Graphic(TemplateInstance):
    def __init__(self, data, managers):
        super().__init__(data, managers)

        # Image attributes
        self.image = data.get("image", None)
        self.images = data.get("images", None)
        self.image_duration = data.get("image_duration", None)
        self.current_image = 0

        if self.images:
            self.image = self.images[self.current_image]
        if self.image:
            self.set_rect(self.image.get_rect())

        # Color attributes
        self.color_data = data.get("color", {})
        self.color_active = self.color_data.get("active", None)
        self.color_inactive = self.color_data.get("inactive", None)
        self.color_border = self.color_data.get("border", None)
        self.color = self.color_inactive

    def update(self):
        super().update()

        if self.image_duration:
            if self.time_elapsed >= self.image_duration:
                self.time_elapsed = 0
                self.current_image = (self.current_image + 1) % len(self.images)
                self.image = self.images[self.current_image]

    def draw(self):
        super().draw()

        if self.color:
            pygame.draw.rect(self.screen, self.color, self.rect)

        if self.color_border:
            pygame.draw.rect(self.screen, self.color_border, self.rect, self.border_radius)

        if self.image:
            self.screen.blit(self.image, self.pos)

