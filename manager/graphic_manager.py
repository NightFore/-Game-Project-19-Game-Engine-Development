# graphic_manager.py

import pygame
import copy
from os import path
from resource_manager import load_resources, load_resource, validate_resource

# Path to the folders containing resources
GRAPHIC_FOLDER = path.join("resources", "graphic")

class GraphicManager:
    RESOURCE_MAPPING = {
        "image": {
            "folder": GRAPHIC_FOLDER,
            "load": "load_image",
            "format": {".png", ".jpg", ".jpeg", ".gif"}
        },
        "image_sequence": {
            "folder": GRAPHIC_FOLDER,
            "load": "load_image_sequence",
            "format": {".png", ".jpg", ".jpeg", ".gif"}
        },
    }

    def __init__(self):
        self.graphics = {}

    """
    Resource Manager
        - load_resources
        - load_resource
    """
    def load_resources(self, resources_dict):
        """Load multiple resources from a dictionary."""
        load_resources(self, resources_dict)

    def load_resource(self, resource_name, resource_data):
        """Load a resource based on its type using the appropriate loading method."""
        load_resource(self, resource_name, resource_data)

    """
    Loading
        - load_image
        - load_image_sequence
    """
    def load_image(self, name, data):
        """
        Load a single image resource from its data.

        Args:
            name (str): The name of the image resource.
            data (dict): A dictionary containing image resource data.
        """
        image_path = data["file_path"]
        image = pygame.image.load(image_path).convert_alpha()
        self.graphics[name] = Graphic(data, image)

    def load_image_sequence(self, name, data):
        """
        Load an image sequence as an animation.

        Args:
            name (str): The name of the image sequence.
            data (dict): A dictionary containing image sequence data.
        """
        frames = []
        for frame_path in data["file_paths"]:
            frame = pygame.image.load(frame_path).convert_alpha()
            frames.append(frame)
        self.graphics[name] = Animation(data, frames)

    def create_graphic_instance(self, key):
        """
        Create an instance of a graphic or animation.

        Args:
            key (str): The key of the graphic to create an instance of.

        Returns:
            Graphic or Animation: An instance of the graphic or animation.
        """
        graphic_data = self.graphics.get(key, None)
        if graphic_data:
            if isinstance(graphic_data, Graphic):
                return Graphic(copy.deepcopy(graphic_data.data), graphic_data.image.copy())
            elif isinstance(graphic_data, Animation):
                copied_images = [image.copy() for image in graphic_data.frames]
                return Animation(copy.deepcopy(graphic_data.data), copied_images)
        return None

class Graphic:
    def __init__(self, data, image):
        """
        Initialize a Graphic instance.

        Args:
            data (dict): A dictionary containing image resource data.
            image (pygame.Surface): The image to be displayed.
        """
        self.data = data
        self.image = image

    def update(self):
        """
        Update the Graphic instance.
        """
        pass

    def draw(self, surface, position):
        """
        Draw the graphic on a surface at the specified position.

        Args:
            surface (pygame.Surface): The surface to draw the graphic on.
            position (tuple): The (x, y) position to draw the graphic at.
        """
        surface.blit(self.image, position)

class Animation:
    def __init__(self, data, frames):
        """
        Initialize an Animation instance.

        Args:
            data (dict): A dictionary containing animation data.
            frames (list): A list of pygame.Surface objects representing animation frames.
        """
        self.data = data
        self.frames = frames
        self.frame_duration = data.get("frame_duration", 100)
        self.current_frame = 0
        self.time_elapsed = 0

    def update(self, dt):
        """
        Update the Animation instance based on the elapsed time.

        Args:
            dt (int): The time (in milliseconds) since the last update.
        """
        self.time_elapsed += dt
        if self.time_elapsed >= self.frame_duration:
            self.time_elapsed = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen, position):
        """
        Draw the current frame of the animation on the screen at the specified position.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
            position (tuple): The (x, y) position to draw the animation frame at.
        """
        screen.blit(self.frames[self.current_frame], position)

# Debugging section
if __name__ == "__main__":
    from debug.debug_graphic_manager import debug_graphic_manager

    # Create an instance of GraphicManager
    graphic_manager = GraphicManager()

    # Debug the GraphicManager by running the debug function
    debug_graphic_manager(graphic_manager)
