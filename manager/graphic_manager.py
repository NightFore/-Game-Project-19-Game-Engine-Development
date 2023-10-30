# graphic_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class GraphicManager(TemplateManager):
    """
    GraphicManager manages graphic resources and their instances in the game.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries
        self.resources = {}
        self.instances = {}

        # Initialize the instance class for this manager
        self.instance_class = GraphicInstance

        # Define resource types to load for this manager
        self.resource_types_to_load = ["image", "image_sequence", "interface", "button"]




class GraphicInstance(TemplateInstance):
    """
    GraphicInstance represents an instance of a graphic resource.

    Attributes:
        Specific to GraphicInstance:
            image (pygame.Surface): The image associated with the graphic instance.
            images (list): A list of images for animations.
            image_duration (int): The duration between image changes for animations.
            current_image (int): The index of the current image in the animation sequence.
            color_data (dict): Data related to colors.
            color_active (tuple): The active color for the graphic instance.
            color_inactive (tuple): The inactive color for the graphic instance.
            color_border (tuple): The color for the border of the graphic instance.
            color (tuple): The current color of the graphic instance.

        Inherited from TemplateInstance:
            pos (tuple): The position (x, y) of the graphic instance.
            size (tuple): The size (width, height) of the graphic instance.
            rect (pygame.Rect): The rectangular area of the graphic instance.
            border_radius (int): The radius of the border, if applicable.
            align (str): The alignment of the graphic instance (e.g., 'center', 'left', 'right').
            dt (int): The time passed since the last frame.
            time_elapsed (int): The time elapsed since the last update.

    Methods:
    - Render
        - update(): Update the graphic instance.
        - draw(): Draw the graphic instance.
    """
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
        self.border_radius = data.get("border_radius", None)

    """
    Render
        - update
        - draw
    """
    def update(self):
        """
        Update the graphic instance
        """
        super().update()

        # Check if there is an image sequence to animate
        if self.image_duration:
            # Cycle through images in the sequence
            if self.time_elapsed >= self.image_duration:
                self.time_elapsed = 0
                self.current_image = (self.current_image + 1) % len(self.images)
                self.image = self.images[self.current_image]

    def draw(self):
        """
        Draw the graphic instance.
        """
        super().draw()

        # Draw a colored rectangle if color is defined
        if self.color:
            pygame.draw.rect(self.screen, self.color, self.rect)

        # Draw a colored border if color_border is defined
        if self.color_border:
            pygame.draw.rect(self.screen, self.color_border, self.rect, self.border_radius)

        # Draw the image if it exists
        if self.image:
            self.screen.blit(self.image, self.pos)
