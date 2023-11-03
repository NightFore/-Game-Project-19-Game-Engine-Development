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
        Specific to GraphicInstance:
            - graphic_type (str): The type of the graphic instance.
            - pos (tuple): The position (x, y) of the instance.
            - rect (Rect): The rectangle that defines the boundaries of the instance.
            - align (str): The alignment of the instance.
            - current_state (bool): The current state (active or inactive) of the instance.

            Rect Attributes:
                - size (tuple): The size (width, height) of the rect.
                - border_radius (int): The border radius of the rect.
                - color_active (tuple): The active color of the rect.
                - color_inactive (tuple): The inactive color of the rect.
                - color_border (tuple): The border color of the rect.
                - color (tuple): The current color of the rect.

            Image Attributes:
                - image (Surface): The current displayed image.

            Image Sequence Attributes:
                - images (list): A list of images for image sequences.
                - image_duration (int): The duration (in seconds) between image changes in a sequence.
                - current_image (int): The index of the current image in the sequence.
                - time_elapsed (int): The time elapsed since the last update of the current image in the sequence.

        Inherited Attributes from TemplateInstance:
            - screen (pygame.Surface): The game display surface.
            - dt (float): Time since the last frame update.

    Methods:
        Management:
            - set_pos(tuple): Set the position of the instance.
            - set_size(tuple): Set the size of the instance.
            - set_align(str): Set the alignment of the instance within its bounding rectangle.
            - set_state(bool): Set the state (active or inactive) of the instance.
            - update_rect(): Update the instance's bounding rectangle.

        Render:
            - update(): Update the instance.
            - draw(): Draw the instance.
    """
    def __init__(self, instance_data, managers):
        # Call the constructor of the parent class (TemplateInstance)
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

            color_data = instance_data.get("color_data", None)
            if color_data:
                self.color_active = color_data.get("active", None)
                self.color_inactive = color_data.get("inactive", None)
                self.color_border = color_data.get("border", None)

            # Set the initial rect and color
            self.rect = pygame.Rect((self.pos[0], self.pos[1], self.size[0], self.size[1]))
            self.color = self.color_inactive

        # Image attributes
        elif self.graphic_type == "image":
            self.image = instance_data.get("image", None)

            # Set the initial rect
            self.rect = self.image.get_rect()

        # Image sequence attributes
        elif self.graphic_type == "image_sequence":
            # Get the list of images for the sequence
            self.images = instance_data.get("images", None)
            self.image_duration = instance_data.get("image_duration", None)

            # Initialize the current image index and elapsed time
            self.current_image = 0
            self.time_elapsed = 0

            # Set the initial image and rect
            self.image = self.images[self.current_image]
            self.rect = self.image.get_rect()


    """
    Management:
        - set_pos
        - set_state
    """
    def set_pos(self, pos):
        """
        Set the position of the instance.
        """
        self.pos = self.rect[0], self.rect[1] = pos
        self.update_rect()

    def set_size(self, size):
        """
        Set the size of the instance.
        """
        if self.graphic_type == "rect":
            self.size = self.rect[2], self.rect[3] = size
            self.update_rect()

    def set_align(self, align):
        """
        Set the alignment of the instance within its bounding rectangle.
        """
        self.align = align
        self.update_rect()

    def set_state(self, state):
        """
        Set the state (active or inactive) of the instance.
        """
        self.current_state = state
        if state:
            if self.graphic_type == "rect":
                self.color = self.color_active
        else:
            if self.graphic_type == "rect":
                self.color = self.color_inactive

    def update_rect(self):
        """
        Update the instance's bounding rectangle.
        """
        if self.align == "center":
            self.rect.center = self.pos
        if self.align == "nw":
            self.rect.topleft = self.pos
        if self.align == "ne":
            self.rect.topright = self.pos
        if self.align == "sw":
            self.rect.bottomleft = self.pos
        if self.align == "se":
            self.rect.bottomright = self.pos
        if self.align == "n":
            self.rect.midtop = self.pos
        if self.align == "s":
            self.rect.midbottom = self.pos
        if self.align == "e":
            self.rect.midright = self.pos
        if self.align == "w":
            self.rect.midleft = self.pos


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

        # Check if there is an image sequence to animate
        if self.graphic_type == "image_sequence":
            # Cycle through images in the sequence
            self.time_elapsed += self.dt
            if self.time_elapsed >= self.image_duration:
                self.time_elapsed = 0
                self.current_image = (self.current_image + 1) % len(self.images)
                self.image = self.images[self.current_image]

    def draw(self):
        """
        Draw the instance.
        """
        super().draw()

        if self.graphic_type == "rect":
            # Draw a colored rectangle
            pygame.draw.rect(self.screen, self.color, self.rect)

            # Draw a colored border if color_border is defined
            if self.color_border:
                pygame.draw.rect(self.screen, self.color_border, self.rect, self.border_radius)

        if self.graphic_type in ["image", "image_sequence"]:
            # Draw the current image
            self.screen.blit(self.image, self.rect)
