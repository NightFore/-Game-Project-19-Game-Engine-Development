# scene_manager.py

import pygame
import os
import inspect
import importlib
from manager.template_manager import TemplateManager, TemplateInstance

class SceneManager(TemplateManager):
    """

    Attributes:
        current_scene (SceneBase): The currently active game scene.

    Methods:
    - Setup
        - load_scenes_from_directory(directory): Load game scenes from Python files in the specified directory and add them to the SceneManager.

    - Management
        - set_scene(scene_name): Set the currently active game scene.

    - Render
        - update(dt): Update the current scene and buttons.
        - draw(screen): Draw the current scene and buttons on the screen.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries to store resources and instances
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
                        scene_instance = obj()

                        # Check if scene parameters and managers are available
                        if self.resources is not None and self.managers is not None:
                            # Configure the scene with scene parameters and managers
                            scene_instance.set_scene_settings(self.managers, self.resources)
                        else:
                            raise ValueError("Scene parameters and managers must be loaded before configuring scenes.")

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
                self.button_manager.clear_buttons()

            # Set the current scene to the specified scene
            self.current_scene = self.instances[scene_name]

            # Enter the new scene
            self.current_scene.enter()
            self.create_buttons_from_dict(scene_name)
            # self.create_texts_from_dict(scene_name)

    def create_buttons_from_dict(self, scene_name):
        """
        """
        buttons_dict = self.resources[scene_name].get("buttons", {})
        for name, button_info in buttons_dict.items():
            # Create an instance
            button_instance = self.button_manager.create_button()

            #
            graphic = button_info["graphic"]
            rect = button_info["rect"]
            text = button_info.get("text", None)
            align = button_info.get("align", None)

            #
            graphic_instance = self.graphic_manager.create_resource_instance(graphic)
            button_instance.set_graphic(graphic_instance)
            button_instance.set_rect(rect)
            if text:
                button_instance.set_text(text)
            if text:
                button_instance.set_align(align)

            # Store the instance
            self.current_scene.scene_buttons[name] = button_instance

    def create_texts_from_dict(self, scene_name):
        """
        """
        texts_dict = self.resources[scene_name].get("texts", {})
        for text_info in texts_dict:
            # Create an instance
            text_instance = self.text_manager.create_text()

            #
            pos = text_info["pos"]
            text = text_info["text"]
            text_font = text_info["font"]
            text_size = text_info.get("size", None)
            text_color = text_info("color", None)
            align = text_info.get("align", None)

            #
            text_instance.set_pos(pos)
            text_instance.set_text(text)
            text_instance.set_text_font(text_font)
            if text_size:
                text_instance.set_text_size(text_size)
            if text_color:
                text_instance.set_text_color(text_color)
            if align:
                text_instance.set_align(align)

            # Store the instance
            self.current_scene.scene_texts.append(text_instance)


    """
    Render
        - update
        - draw
    """
    def update(self, dt):
        """
        Update the current scene and buttons.

        Args:
            dt (float): Time since last update.
        """
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen):
        """
        Draw the current scene and buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.current_scene:
            self.current_scene.draw(screen)



class SceneBase:
    """
    SceneBase provides a base for game scenes with buttons.

    Attributes:
        managers (dict): A dictionary containing game managers.
        button_manager: The manager for buttons.
        graphic_manager: The manager for graphics.
        scene_manager: The manager for scenes.
        scenes_params (dict): A dictionary of scene parameters.
        scene_buttons (dict): A dictionary containing buttons in the scene.

    Methods:
    - Scene Setup
        - set_scene_settings: Set the scene parameters for the scene.

    - Scene Lifecycle
        - enter: Called when entering the scene.
            - create_buttons_from_dict: Create buttons based on button information retrieved from the scene_params.
        - exit: Called when exiting the scene.
        - update: Update the scene.
        - draw: Draw the scene.
    """
    def __init__(self):
        """
        Initialize the SceneBase.
        """
        self.scene_name = self.__class__.__name__

        # Initialize managers
        self.managers = None
        self.button_manager = None
        self.graphic_manager = None
        self.scene_manager = None
        self.text_manager = None

        self.scenes_params = None
        self.scene_buttons = {}
        self.scene_texts = []


    """
    Setup
        - set_scene_settings
    """
    def set_scene_settings(self, managers, scenes_params):
        """
        Set the scene parameters for the scene.

        Args:
            managers (dict): A dictionary containing game managers.
            scenes_params (dict): The dictionary of scene parameters.
        """
        self.managers = managers
        self.button_manager = self.managers["button_manager"]
        self.graphic_manager = self.managers["graphic_manager"]
        self.scene_manager = self.managers["scene_manager"]
        self.text_manager = self.managers["text_manager"]
        self.scenes_params = scenes_params


    """
    Scene Lifecycle
        - enter
            - create_buttons_from_dict
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

    def update(self, dt):
        """
        Update the scene.

        Args:
            dt (float): Time since last update.
        """
        pass

    def draw(self, screen):
        """
        Draw the scene.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        pass
