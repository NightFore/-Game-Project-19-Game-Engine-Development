# scene_manager.py

import pygame
import os
import inspect
import importlib
from manager.template_manager import TemplateManager, TemplateInstance

class SceneManager(TemplateManager):
    """
    SceneManager manages game scenes.

    Attributes:
        - resources (dict): A dictionary containing loaded resources.
        - instances (dict): A dictionary containing resource instances.
        - instance_class: The class used to create resource instances.
        - resource_types_to_load (list): A list of resource types to load for this manager.
        - current_scene (SceneBase): The currently active game scene.

    Methods:
        Setup:
            - load_scenes_from_directory(directory): Load game scenes from Python files in the specified directory and add them to the SceneManager.

        Management:
            - set_scene(scene_name): Set the currently active game scene.

        Render:
            - update(): Update the current scene.
            - draw(): Draw the current scene.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries
        self.managers = {}
        self.resources = {}
        self.instances = {}

        # Initialize the instance class for this manager
        self.instance_class = SceneBase

        # Define resource types to load for this manager
        self.resource_types_to_load = ["scene"]

        # Initialize manager-related attributes
        self.current_scene = None


    """
    Setup
        - load_scenes_from_directory
    """
    def load_scenes_from_directory(self, directory):
        """
        Load game scenes from Python files in the specified directory and add them to the SceneManager.

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
                    if inspect.isclass(obj) and issubclass(obj, self.instance_class) and obj != self.instance_class:
                        # Create an instance of the scene class
                        scene_instance = obj(self.resources, self.managers)

                        # Add the scene to the SceneManager
                        self.instances[name] = scene_instance


    """
    Management
        - set_scene
    """
    def set_scene(self, scene_name):
        """
        Set the currently active game scene.

        Args:
            scene_name (str): The name of the scene to set.
        """
        # Check if the scene_name exists in the SceneManager's scene dictionary
        if scene_name in self.instances:
            # Check if there is a currently active scene
            if self.current_scene:
                # Exit the current scene
                self.current_scene.exit()

            # Set the current scene to the specified scene
            self.current_scene = self.instances[scene_name]

            # Enter the new scene
            self.current_scene.enter()


    """
    Render
        - update
        - draw
    """
    def update(self):
        """
        Update the current scene.
        """
        if self.current_scene:
            self.current_scene.update()

    def draw(self):
        """
        Draw the current scene.
        """
        if self.current_scene:
            self.current_scene.draw()




class SceneBase(TemplateInstance):
    """
    SceneBase provides a base for game scenes.

    Attributes:
        - scene_buttons (dict): A dictionary containing buttons in the scene.
        - scene_graphics (dict): A dictionary containing graphics in the scene.
        - scene_texts (dict): A dictionary containing texts in the scene.

    Methods:
        Management:

        Lifecycle:
            - enter(): Called when entering the scene.
            - exit(): Called when exiting the scene.
            - update(): Update the scene.
            - draw(): Draw the scene.
    """
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)

        # Initialize instance variables
        self.scene_name = self.__class__.__name__
        self.scene_data = self.instance_data[self.scene_name]
        self.scene_buttons = {}
        self.scene_graphics = {}
        self.scene_texts = {}


    """
    Management
    """


    """
    Lifecycle
        - enter
        - exit
        - update
        - draw
    """
    def enter(self):
        """
        Called when entering the scene.
        """
        pass

    def exit(self):
        """
        Called when exiting the scene.
        """
        pass

    def update(self):
        """
        Update the scene.
        """
        super().update()

        # Update each button in the scene
        for button_instance in self.scene_buttons.values():
            button_instance.update()

        # Update each text in the scene
        for text_instance in self.scene_texts:
            text_instance.update()

    def draw(self):
        """
        Draw the scene.
        """
        super().draw()

        # Draw each button in the scene
        for button_instance in self.scene_buttons.values():
            button_instance.draw()

        # Draw each text in the scene
        for text_instance in self.scene_texts:
            text_instance.draw()
