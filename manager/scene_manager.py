# scene_manager.py

import pygame
import os
import inspect
import importlib

from manager.button_manager import ButtonManager

class SceneManager:
    """
    SceneManager class manages the scenes and buttons of the game.
    """

    def __init__(self):
        """
        Initialize the SceneManager.
        """
        self.scenes = {}
        self.scenes_params = None
        self.current_scene = None
        self.button_manager = ButtonManager()

    def load_scenes_params(self, params_dict):
        """
        Load scene parameters from a dictionary and store them.

        Args:
            params_dict (dict): A dictionary containing scene parameters.
        """
        self.scenes_params = params_dict

    def load_scenes_from_directory(self, directory):
        """
        Load scenes from Python files in the specified directory and add them to the SceneManager.

        Args:
            directory (str): The directory containing the scene Python files.
        """
        # Iterate over the files in the specified directory
        for filename in os.listdir(directory):
            # Check if the file is a Python file and not an __init__.py file
            if filename.endswith(".py") and filename != "__init__.py":
                # Get the module name without the file extension
                module_name = os.path.splitext(filename)[0]

                # Import the module dynamically
                module = importlib.import_module(f"{directory}.{module_name}")

                # Iterate over the objects in the imported module
                for name, obj in inspect.getmembers(module):
                    # Check if the object is a class and a subclass of SceneBase (excluding SceneBase itself)
                    if inspect.isclass(obj) and issubclass(obj, SceneBase) and obj != SceneBase:
                        # Create an instance of the scene class and add it to the SceneManager
                        scene_instance = obj(self)
                        self.add_scene(name, scene_instance)

    def add_scene(self, name, scene):
        """
        Add a scene to the manager.

        Args:
            name (str): The name of the scene.
            scene (SceneBase): The scene to add.
        """
        self.scenes[name] = scene
        scene.set_button_manager(self.button_manager)

    def set_scene(self, name):
        """
        Set the current scene.

        Args:
            name (str): The name of the scene to set.
        """
        if name in self.scenes:
            if self.current_scene:
                self.current_scene.exit()
                self.button_manager.clear_buttons()
            self.current_scene = self.scenes[name]
            self.current_scene.set_scene_params(self.scenes_params)
            self.current_scene.enter()

    def update(self, dt):
        """
        Update the current scene and buttons.

        Args:
            dt (float): Time since last update.
        """
        if self.current_scene:
            self.current_scene.update(dt)
            self.button_manager.update()

    def draw(self, screen):
        """
        Draw the current scene and buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.current_scene:
            self.current_scene.draw(screen)
            self.button_manager.draw(screen)

class SceneBase:
    """
    SceneBase class provides a base for scenes with buttons.
    """

    def __init__(self, scene_manager):
        """
        Initialize the SceneBase.

        Args:
            scene_manager (SceneManager): The SceneManager instance.
        """
        self.scene_manager = scene_manager
        self.scene_params = None
        self.button_manager = None

    def set_scene_params(self, scene_params):
        """
        Set the scene parameters for the scene.

        Args:
            scene_params (dict): The dictionary of scene parameters.
        """
        self.scene_params = scene_params

    def set_button_manager(self, button_manager):
        """
        Set the button manager for the scene.

        Args:
            button_manager (ButtonManager): The button manager to set.
        """
        self.button_manager = button_manager

    def create_buttons_from_dict(self, scene_name):
        """
        Create buttons based on button information retrieved from the scene_params.

        Args:
            scene_name (str): The name of the scene to retrieve button information for.
        """
        # Retrieve button information for the specific scene from the scene_params dictionary
        scene_button_infos = self.scene_params.get(scene_name, {}).get("buttons", [])

        # Initialize an empty dictionary to store the created buttons
        self.buttons = {}

        # Iterate over each button information in the list
        for button_info in scene_button_infos:
            # Extract information for the button from the dictionary
            name = button_info["name"]
            position = button_info["position"]
            text = button_info["text"]

            # Create a button using the ButtonManager and the extracted information
            button = self.button_manager.create_button(position, text)

            # Store the button in the buttons dictionary using its name as the key
            self.buttons[name] = button

    def enter(self):
        """
        Called when entering the scene.
        """
        self.create_buttons_from_dict(self.__class__.__name__)

    def exit(self):
        """
        Called when exiting the scene.
        """
        pass

    def update(self, dt):
        """
        Update the scene.

        Args:
            dt (float): Time since last update.
        """
        pass

    def draw(self, screen):
        """
        Draw the scene and its buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        pass
