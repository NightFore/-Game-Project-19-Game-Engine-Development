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
        current_scene (SceneBase): The currently active game scene.

    Methods:
    - Setup
        - load_scenes_from_directory(directory): Load game scenes from Python files in the specified directory and add them to the SceneManager.
        - load_buttons_graphics(): Pre-load graphic instances for buttons in all scenes.

    - Management
        - set_scene(scene_name): Set the currently active game scene.

    - Render
        - update(): Update the current scene and buttons.
        - draw(): Draw the current scene and buttons on the screen.
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
        - load_buttons_graphics
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

    def load_buttons_data(self):
        """
        Pre-load data for buttons in all scenes.
        """
        for scene_name, scene_data in self.resources.items():
            buttons_data = scene_data.get("buttons", {})

            for button_name, button_info in buttons_data.items():
                graphic_name = button_info.get("graphic")
                if graphic_name:
                    graphic_instance = self.graphic_manager.create_resource_instance(graphic_name)
                    button_info["graphic_instance"] = graphic_instance

                font_name = button_info.get("font")
                if font_name:
                    font_instance = self.text_manager.create_resource_instance(font_name)
                    button_info["font_instance"] = font_instance

                rect_data = button_info.get("rect")
                if rect_data:
                    button_info["rect"] = pygame.Rect(rect_data)



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
        Update the current scene and buttons.
        """
        if self.current_scene:
            self.current_scene.update()

    def draw(self):
        """
        Draw the current scene and buttons on the screen.
        """
        if self.current_scene:
            self.current_scene.draw()




class SceneBase(TemplateInstance):
    """
    SceneBase provides a base for game scenes.

    Attributes:
        scene_buttons (dict): A dictionary containing buttons in the scene.
        scene_texts (dict): A dictionary containing texts in the scene.

    Methods:
    - Management
        - set_scene(scene_name): Set the currently active game scene.
        - create_buttons_from_dict(scene_name): Create buttons for the specified scene based on a dictionary of button data.
        - create_texts_from_dict(scene_name): Create text instances for the specified scene based on a dictionary of text data.

    - Lifecycle
        - enter: Called when entering the scene.
        - exit: Called when exiting the scene.
        - update: Update the scene.
        - draw: Draw the scene.
    """
    def __init__(self, data, managers):
        """
        Initialize the SceneBase.

        Args:
            data (dict): Data for initializing the scene.
            managers (dict): A dictionary containing game managers.
        """
        super().__init__(data, managers)
        self.scene_name = self.__class__.__name__
        self.scene_buttons = {}
        self.scene_texts = []


    """
    Management
        - create_buttons_from_dict
        - create_texts_from_dict
    """
    def create_buttons_from_dict(self):
        """
        Create buttons for the specified scene based on a dictionary of button data.
        """
        buttons_dict = self.instance_data[self.scene_name].get("buttons", {})
        for name, button_info in buttons_dict.items():
            # Create an instance using the manager
            button_instance = self.button_manager.create_instance_from_data(button_info)
            self.scene_buttons[name] = button_instance

    def create_texts_from_dict(self):
        """
        Create text instances for the specified scene based on a dictionary of text data.
        """
        texts_dict = self.instance_data[self.scene_name].get("texts", {})
        for text_info in texts_dict:
            # Create an instance
            text_instance = self.text_manager.create_text()

            # Extract information
            pos = text_info["pos"]
            text = text_info["text"]
            text_font = text_info["font"]
            text_size = text_info.get("size", None)
            text_color = text_info("color", None)
            align = text_info.get("align", None)

            # Set properties
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
            self.scene_texts.append(text_instance)


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
        self.create_buttons_from_dict()
        # self.create_texts_from_dict()

    def exit(self):
        """
        Called when exiting the scene.
        """
        self.button_manager.clear_buttons()

    def update(self):
        """
        Update the scene.
        """
        super().update()

        # Update each button in the scene
        for button in self.scene_buttons.values():
            button.update()

        # Update each text in the scene
        for text in self.scene_texts:
            text.update()

    def draw(self):
        """
        Draw the scene.
        """
        super().draw()

        # Draw each button in the scene
        for button in self.scene_buttons.values():
            button.draw()

        # Draw each text in the scene
        for text in self.scene_texts:
            text.draw()
