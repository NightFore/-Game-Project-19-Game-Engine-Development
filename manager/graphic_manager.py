# graphic_manager.py
# This file contains the GraphicManager class responsible for loading and managing game graphics.

# Created by: NightFore
# Date: August 4, 2023

# Description:
# The GraphicManager class handles the loading of graphics resources such as images and animations.
# It provides functions to load graphics data from files and manage their display and animations.

# Usage:
# To use the GraphicManager, create an instance of the class and load graphics using the load_graphics method.
# You can then retrieve graphics data using the get_graphic method.

# Dependencies:
# This module depends on pygame for graphics handling.

# Note:
# This is a part of the game engine development project and is subject to updates and improvements.

import pygame
from os import path
from data.resource_data import GRAPHIC_FOLDER

class GraphicManager:
    def __init__(self):
        self.graphics = {}

    """
    Loading
        - load_resources
        - load_graphic
    """
    def load_resources(self, resources_dict):
        """
        Load multiple resources from a dictionary.

        Args:
            resources_dict (dict): A dictionary containing resource names as keys and data dictionaries as values.
        """
        for name, data in resources_dict.items():
            self.load_graphic(name, data)

    def load_graphic(self, name, data):
        """
        Load a single graphic resource from its data.

        Args:
            name (str): The name of the graphic resource.
            data (dict): A dictionary containing graphic resource data.
        """
        image_path = data["image"]
        image = pygame.image.load(image_path).convert_alpha()
        size_scaled = data.get("size_scaled", (image.get_width(), image.get_height()))

        # Add more data loading here if needed

        self.graphics[name] = {
            "image": image,
            "size_scaled": size_scaled
            # Add more data to store here if needed
        }


    def get_graphic(self, key):
        """
        Retrieve a graphic by its key.

        Args:
            key (str): The key of the graphic to retrieve.

        Returns:
            dict: A dictionary containing the graphic data.
        """
        return self.graphics.get(key, None)

# Example usage:
DICT_GRAPHIC = {
    "sprite": {
        "image": path.join(GRAPHIC_FOLDER, "sprite_image.png"),
        "size_scaled": (32, 32),  # Replace with actual size
        # Add more graphic data here
    },
    # Add more graphics here
}

graphic_manager = GraphicManager()
graphic_manager.load_graphics(DICT_GRAPHIC)
