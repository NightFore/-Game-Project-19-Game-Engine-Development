# graphic_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class GraphicManager(TemplateManager):
    """
    GraphicManager manages graphic resources and their instances in the game.

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
        self.instance_class = GraphicInstance

        # Define resource types to load for this manager
        self.resource_types_to_load = ["image", "image_sequence", "rect"]




class GraphicInstance(TemplateInstance):
    """
    GraphicInstance represents an instance of a graphic resource.

    Attributes:
    - graphic_type (str): The type of the graphic instance.
    - pos (tuple): The position (x, y) of the graphic.
    - rect (Rect): The rectangle that defines the boundaries of the graphic.
    - align (str): The alignment of the graphic.
    - current_state (bool): The current state (active or inactive) of the graphic.

    Rect Attributes:
    - size (tuple): The size (width, height).
    - border_radius (int): The border radius of the graphic.
    - color_active (tuple): The active color of the graphic.
    - color_inactive (tuple): The inactive color of the graphic.
    - color_border (tuple): The border color of the graphic.
    - color (tuple): The current color of the graphic.

    Image Attributes:
    - image (Surface): The current displayed image.

    Image Sequence Attributes:
    - images (list): A list of images for image sequences.
    - image_duration (int): The duration (in seconds) between image changes in a sequence.
    - current_image (int): The index of the current image in the sequence.
    - time_elapsed (int): The time elapsed since the last update.

    Methods:
    - Management
        - set_pos(pos): Set the position of the graphic.
        - set_state(state): Set the state (active or inactive) of the graphic.

    - Inherited from TemplateInstance
        - update_rect: Update the rect of the graphic.

    - Render
        - update(): Update the graphic.
        - draw(): Draw the graphic.
    """
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)

        # Initialize state variables
        if "color_data" in instance_data:
            self.graphic_type = "rect"
        elif "filename" in instance_data:
            self.graphic_type = "image"
        elif "files" in instance_data:
            self.graphic_type = "image_sequence"

        # Initialize instance variables
        self.pos = (0, 0)
        self.align = "nw"
        self.current_state = False

        # Rect attributes
        if self.graphic_type == "rect":
            self.size = instance_data.get("size", None)
            self.border_radius = instance_data.get("border_radius", None)
            self.rect = pygame.Rect((self.pos[0], self.pos[1], self.size[0], self.size[1]))

            color_data = instance_data.get("color_data", None)
            if color_data:
                self.color_active = color_data.get("active", None)
                self.color_inactive = color_data.get("inactive", None)
                self.color_border = color_data.get("border", None)
            self.color = self.color_inactive

        # Image attributes
        elif self.graphic_type == "image":
            self.image = instance_data.get("image", None)
            self.rect = self.image.get_rect()

        # Image sequence attributes
        elif self.graphic_type == "image_sequence":
            self.images = instance_data.get("images", None)
            self.image_duration = instance_data.get("image_duration", None)
            self.image = self.images[self.current_image]
            self.rect = self.image.get_rect()
            self.current_image = 0
            self.time_elapsed = 0


    """
    Management
        - set_pos
        - set_state
    """
    def set_pos(self, pos):
        """
        Set the position of the graphic.
        """
        self.pos = self.rect[0], self.rect[1] = pos
        self.update_rect()

    def set_state(self, state):
        """
        Set the state (active or inactive) of the graphic.
        """
        self.current_state = state
        if state:
            if self.graphic_type == "rect":
                self.color = self.color_active
        else:
            if self.graphic_type == "rect":
                self.color = self.color_inactive

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
        if self.graphic_type == "image_sequence":
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

        if self.graphic_type == "rect":
            # Draw a colored rectangle
            pygame.draw.rect(self.screen, self.color, self.rect)

            # Draw a colored border if color_border is defined
            if self.color_border:
                pygame.draw.rect(self.screen, self.color_border, self.rect, self.border_radius)

        if self.graphic_type in ["image", "image_sequence"]:
            # Draw the image
            self.screen.blit(self.image, self.rect)
