# graphic_manager.py
# This file contains the GraphicManager class responsible for loading and managing game graphics.

# Created by: NightFore
# Date: August 4, 2023

# Description:
# The GraphicManager class handles the loading of graphics resources such as images and animations.
# It provides functions to load graphics data from files and manage their display and animations.

# Usage:
# To use the GraphicManager, create an instance of the class and load graphics using the load_resources method.
# You can then retrieve graphics data using the create_graphic_instance method.

# Dependencies:
# This module depends on pygame for graphics handling.

# Note:
# This is a part of the game engine development project and is subject to updates and improvements.

import pygame
from os import path

GRAPHIC_FOLDER = path.join("data", "graphic")

class Graphic:
    def __init__(self, image, scaled_size):
        self.image = image
        self.scaled_size = scaled_size

    def update(self):
        # Add update logic here if needed
        pass

    def draw(self, screen, position):
        screen.blit(self.image, position)

class Animation:
    def __init__(self, images, frame_duration):
        self.images = images
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_elapsed = 0

    def update(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed >= self.frame_duration:
            self.time_elapsed = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)

    def draw(self, screen, position):
        screen.blit(self.images[self.current_frame], position)

class GraphicManager:
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
            if "image_paths" in data:
                self.load_image_sequence(name, data)
            else:
                self.load_image(name, data)

    def load_image(self, name, data):
        """
        Load a single image resource from its data.

        Args:
            name (str): The name of the image resource.
            data (dict): A dictionary containing image resource data.
        """
        image_path = path.join(GRAPHIC_FOLDER, data["image"])
        image = pygame.image.load(image_path).convert_alpha()
        scaled_size = data.get("scaled_size", (image.get_width(), image.get_height()))

        # Add more data loading here if needed

        self.graphics[name] = Graphic(image, scaled_size)

    def load_image_sequence(self, name, data):
        """
        Load an image sequence as an animation.

        Args:
            name (str): The name of the image sequence.
            data (dict): A dictionary containing image sequence data.
        """
        image_paths = [path.join(GRAPHIC_FOLDER, p) for p in data["image_paths"]]
        images = [pygame.image.load(p).convert_alpha() for p in image_paths]
        frame_duration = data.get("frame_duration", 100)  # Default duration in milliseconds

        self.graphics[name] = Animation(images, frame_duration)

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
                return Graphic(graphic_data.image, graphic_data.scaled_size)
            elif isinstance(graphic_data, Animation):
                return Animation(graphic_data.images, graphic_data.frame_duration)
        return None

if __name__ == "__main__":
    from debug.debug_graphic_manager import debug

    # Create an instance of GraphicManager
    graphic_manager = GraphicManager()

    # Debug the GraphicManager by running the debug function
    debug(graphic_manager)
