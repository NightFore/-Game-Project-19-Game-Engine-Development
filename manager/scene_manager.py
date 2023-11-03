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
            - initialize_scene_buttons(): Initialize and create button instances for the current scene.
            - initialize_scene_graphics(): Initialize and create graphic instances for the current scene.
            - initialize_scene_texts(): Initialize and create text instances for the current scene.

        Lifecycle:
            - enter(): Called when entering the scene.
            - exit(): Called when exiting the scene.
            - update(): Update the scene.
            - draw(): Draw the scene.

        Scene Logic:
            - init_buttons(self): Initialize buttons for the scene. Override this method in derived classes for button setup.
            - init_graphics(self): Initialize graphics for the scene. Override this method in derived classes for graphic setup.
            - init_texts(self): Initialize texts for the scene. Override this method in derived classes for text setup.
            - update_buttons(self): Update buttons in the scene.
            - update_graphics(self): Update graphics in the scene.
            - update_texts(self): Update texts in the scene.
            - draw_buttons(self): Draw buttons in the scene.
            - draw_graphics(self): Draw graphics in the scene.
            - draw_texts(self): Draw texts in the scene.

        Custom Functions:
            - init_custom(self): Initialize custom scene logic. Override this method in derived classes for custom scene setup.
            - update_custom(self): Update custom scene logic. Override this method in derived classes for custom updates.
            - draw_custom(self): Draw custom scene elements. Override this method in derived classes for custom drawing.
    """
    def __init__(self, instance_data, managers):
        # Call the constructor of the parent class (TemplateInstance)
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
    def initialize_scene_buttons(self):
        """
        Initialize and create button instances for the current scene.
        """
        # Get the button data for the current scene
        button_dict = self.scene_data.get("buttons", {})

        # Iterate through the button data
        for button_name, button_data in button_dict.items():
            button_resource = button_data.get("button", None)
            button_pos = button_data.get("pos", (0, 0))
            button_text = button_data.get("text", "")
            button_align = button_data.get("align", None)

            # Check if a valid button resource is specified
            if button_resource:
                # Create a button instance
                button_instance = self.button_manager.create_resource_instance(button_resource)
                button_instance.set_pos(button_pos)
                button_instance.set_text(button_text)
                button_instance.set_align(button_align)

                # Add the button instance to the scene_buttons dictionary
                self.scene_buttons[button_name] = button_instance

    def initialize_scene_graphics(self):
        """
        Initialize and create graphic instances for the current scene.
        """
        # Get the graphic data for the current scene
        graphic_dict = self.scene_data.get("graphics", {})

        # Iterate through the graphic data
        for graphic_name, graphic_data in graphic_dict.items():
            graphic_resource = graphic_data.get("graphic", None)
            graphic_pos = graphic_data.get("pos", (0, 0))
            graphic_align = graphic_data.get("align", None)

            # Check if a valid graphic resource is specified
            if graphic_resource:
                # Create a graphic instance
                graphic_instance = self.graphic_manager.create_resource_instance(graphic_resource)
                graphic_instance.set_pos(graphic_pos)
                graphic_instance.set_align(graphic_align)

                # Add the graphic instance to the scene_graphics dictionary
                self.scene_graphics[graphic_name] = graphic_instance

    def initialize_scene_texts(self):
        """
        Initialize and create text instances for the current scene.
        """
        # Get the text data for the current scene
        text_dict = self.scene_data.get("texts", {})

        # Iterate through the text data
        for text_name, text_data in text_dict.items():
            font_resource = text_data.get("font", None)
            text_pos = text_data.get("pos", (0, 0))
            text_text = text_data.get("text", "")
            text_align = text_data.get("align", None)

            # Check if a valid text resource is specified
            if font_resource:
                # Create a text instance
                text_instance = self.text_manager.create_resource_instance(font_resource)
                text_instance.set_pos(text_pos)
                text_instance.set_text(text_text)
                text_instance.set_align(text_align)

                # Add the text instance to the scene_texts dictionary
                self.scene_texts[text_name] = text_instance


    """
    Lifecycle
    """
    def enter(self):
        """
        Called when entering the scene.
        """
        self.initialize_scene_buttons()
        self.initialize_scene_graphics()
        self.initialize_scene_texts()
        self.init_buttons()
        self.init_graphics()
        self.init_texts()
        self.init_custom()

    def exit(self):
        """
        Called when exiting the scene.
        """
        self.scene_buttons = {}
        self.scene_graphics = {}
        self.scene_texts = {}

    def update(self):
        """
        Update the scene.
        """
        super().update()
        self.update_buttons()
        self.update_graphics()
        self.update_texts()
        self.update_custom()

    def draw(self):
        """
        Draw the scene.
        """
        super().draw()
        self.draw_buttons()
        self.draw_graphics()
        self.draw_texts()
        self.draw_custom()


    """
    Scene Logic
    """
    def init_buttons(self):
        """
        Initialize buttons for the scene. Override this method in derived classes for button setup.
        """
        pass

    def init_graphics(self):
        """
        Initialize graphics for the scene. Override this method in derived classes for graphic setup.
        """
        pass

    def init_texts(self):
        """
        Initialize texts for the scene. Override this method in derived classes for text setup.
        """
        pass

    def update_buttons(self):
        """
        Update buttons in the scene.
        """
        for button_instance in self.scene_buttons.values():
            button_instance.update()

    def update_graphics(self):
        """
        Update graphics in the scene.
        """
        for graphic_instance in self.scene_graphics.values():
            graphic_instance.update()

    def update_texts(self):
        """
        Update texts in the scene.
        """
        for text_instance in self.scene_texts.values():
            text_instance.update()

    def draw_buttons(self):
        """
        Draw buttons in the scene.
        """
        for button_instance in self.scene_buttons.values():
            button_instance.draw()

    def draw_graphics(self):
        """
        Draw graphics in the scene.
        """
        for graphic_instance in self.scene_graphics.values():
            graphic_instance.draw()

    def draw_texts(self):
        """
        Draw texts in the scene.
        """
        for text_instance in self.scene_texts.values():
            text_instance.draw()


    """
    Custom Functions
    """
    def init_custom(self):
        """
        Initialize custom scene logic. Override this method in derived classes for custom scene setup.
        """
        pass

    def update_custom(self):
        """
        Update custom scene logic. Override this method in derived classes for custom updates.
        """
        pass

    def draw_custom(self):
        """
        Draw custom scene elements. Override this method in derived classes for custom drawing.
        """
        pass
