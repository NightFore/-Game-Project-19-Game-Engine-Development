# graphic_manager.py

import pygame
import copy
from os import path

from error_manager import ResourceNotFoundError, InvalidImageFormatError, ResourceLoadError, handle_error

GRAPHIC_FOLDER = path.join("resources", "graphic")

class Graphic:
    def __init__(self, image, scaled_size):
        """
        Initialize a Graphic instance.

        Args:
            image (pygame.Surface): The image to be displayed.
            scaled_size (tuple): The scaled size of the image (width, height).
        """
        self.image = image
        self.scaled_size = scaled_size

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
    def __init__(self, images, frame_duration):
        """
        Initialize an Animation instance.

        Args:
            images (list): A list of pygame.Surface objects representing animation frames.
            frame_duration (int): The duration (in milliseconds) of each frame in the animation.
        """
        self.images = images
        self.frame_duration = frame_duration
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
            self.current_frame = (self.current_frame + 1) % len(self.images)

    def draw(self, screen, position):
        """
        Draw the current frame of the animation on the screen at the specified position.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
            position (tuple): The (x, y) position to draw the animation frame at.
        """
        screen.blit(self.images[self.current_frame], position)

class GraphicManager:
    RESOURCE_MAPPING = {
        "image": "load_image",
        "image_sequence": "load_image_sequence",
    }

    def __init__(self):
        self.graphics = {}

    """
    Loading
        - load_resources
        - load_image
        - load_image_sequence
    """
    def load_resources(self, resources_dict):
        """
        Load multiple resources from a dictionary.

        Args:
            resources_dict (dict): A dictionary containing resource names as keys and data dictionaries as values.
        """
        for name, data in resources_dict.items():
            resource_type = data.get("type")
            if resource_type is not None:
                load_method_name = self.RESOURCE_MAPPING.get(resource_type)
                if load_method_name is not None:
                    load_method = getattr(self, load_method_name)
                    load_method(name, data)
                else:
                    raise ValueError("Invalid resource type")
            else:
                raise ValueError("Resource type not specified")

    def load_image(self, name, data):
        """
        Load a single image resource from its data.

        Args:
            name (str): The name of the image resource.
            data (dict): A dictionary containing image resource data.
        """
        try:
            image_path = path.join(GRAPHIC_FOLDER, data["image"])
            if not path.exists(image_path):
                raise ResourceNotFoundError(data['image'], image_path)
            if not self.is_supported_image_format(image_path):
                raise InvalidImageFormatError(data['image'])

            # Load the image and convert to alpha format
            image = pygame.image.load(image_path).convert_alpha()
            scaled_size = data.get("scaled_size", (image.get_width(), image.get_height()))
            self.graphics[name] = Graphic(image, scaled_size)

        except (pygame.error, ResourceNotFoundError, InvalidImageFormatError) as e:
            self.graphics[name] = None
            raise ResourceLoadError(data['image'], str(e))

    def load_image_sequence(self, name, data):
        """
        Load an image sequence as an animation.

        Args:
            name (str): The name of the image sequence.
            data (dict): A dictionary containing image sequence data.
        """
        try:
            images = []
            for frame_data in data["images"]:
                frame_path = path.join(GRAPHIC_FOLDER, frame_data["image"])
                if not path.exists(frame_path):
                    raise ResourceNotFoundError(frame_data['image'], frame_path)
                if not self.is_supported_image_format(frame_path):
                    raise InvalidImageFormatError(frame_data['image'])

                # Load the image and convert to alpha format
                image = pygame.image.load(frame_path).convert_alpha()
                scaled_size = frame_data.get("scaled_size", (image.get_width(), image.get_height()))
                images.append(image)

            frame_duration = data.get("frame_duration", 100)  # Default duration in milliseconds
            self.graphics[name] = Animation(images, frame_duration)

        except (pygame.error, ResourceNotFoundError, InvalidImageFormatError) as e:
            self.graphics[name] = None
            raise ResourceLoadError(name, str(e))

    def is_supported_image_format(self, image_path):
        """
        Check if the image format of the specified image path is supported.

        Args:
            image_path (str): The path of the image file.

        Returns:
            bool: True if the image format is supported, False otherwise.
        """
        # List of supported image formats (extensions)
        supported_formats = ['.png', '.jpg', '.jpeg', '.gif']

        # Get the file extension of the image path and convert to lowercase
        image_format = path.splitext(image_path)[-1].lower()

        # Check if the image format is in the list of supported formats
        return image_format in supported_formats

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
                return Graphic(graphic_data.image.copy(), graphic_data.scaled_size)
            elif isinstance(graphic_data, Animation):
                copied_images = [image.copy() for image in graphic_data.images]
                return Animation(copied_images, graphic_data.frame_duration)
        return None

if __name__ == "__main__":
    from debug.debug_graphic_manager import debug

    # Create an instance of GraphicManager
    graphic_manager = GraphicManager()

    # Debug the GraphicManager by running the debug function
    debug(graphic_manager)
