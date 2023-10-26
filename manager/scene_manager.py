# scene_manager.py

import pygame
import os
import inspect
import importlib

class SceneManager:
    """
    SceneManager handles game scenes and buttons.

    Attributes:
        scenes (dict): A dictionary containing loaded game scenes.
        managers (dict): A dictionary containing game managers.
        scenes_params (dict): A dictionary containing scene parameters.
        current_scene (SceneBase): The currently active game scene.

    Methods:
    - Setup
        - set_managers(managers): Load and set game managers in the SceneManager.
        - load_scene_parameters(params_dict): Load scene parameters from a dictionary and store them.
        - load_scenes_from_directory(directory): Load game scenes from Python files in the specified directory and add them to the SceneManager.

    - Management
        - set_scene(scene_name): Set the currently active game scene.

    - Update and Draw
        - update(dt): Update the current scene and buttons.
        - draw(screen): Draw the current scene and buttons on the screen.
    """
    def __init__(self):
        """
        Initialize the SceneManager.
        """
        self.scenes = {}
        self.managers = None
        self.scenes_params = None
        self.current_scene = None


    """
    Setup
        - set_managers
        - load_scene_parameters
        - load_scenes_from_directory
    """
    def set_managers(self, managers):
        """
        Load and set game managers in the SceneManager.

        Args:
            managers (dict): A dictionary containing game managers.
        """
        self.managers = managers

    def load_scenes_parameters(self, params_dict):
        """
        Load scenes parameters from a dictionary and store them.

        Args:
            params_dict (dict): A dictionary containing scenes parameters.
        """
        self.scenes_params = params_dict

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
                    if inspect.isclass(obj) and issubclass(obj, SceneBase) and obj != SceneBase:
                        # Create an instance of the scene class
                        scene_instance = obj()

                        # Check if scene parameters and managers are available
                        if self.scenes_params is not None and self.managers is not None:
                            # Configure the scene with scene parameters and managers
                            scene_instance.set_scene_settings(self.managers, self.scenes_params)

                        # Add the scene to the SceneManager
                        self.scenes[name] = scene_instance


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
        if scene_name in self.scenes:
            # Check if there is a currently active scene
            if self.current_scene:
                # Exit the current scene
                self.current_scene.exit()

            # Set the current scene to the specified scene
            self.current_scene = self.scenes[scene_name]

            # Enter the new scene
            self.current_scene.enter()


    """
    Update and Draw
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
        # Initialize game managers
        self.managers = None
        self.button_manager = None
        self.graphic_manager = None
        self.scene_manager = None

        # Initialize scene parameters and buttons
        self.scenes_params = None
        self.scene_buttons = {}


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
        self.create_buttons_from_dict(self.__class__.__name__)

    def create_buttons_from_dict(self, scene_name):
        """
        Create buttons based on button information retrieved from the scene_params.

        Args:
            scene_name (str): The name of the current scene.
        """
        # Retrieve button information for the specific scene from the scene_params dictionary
        scene_buttons_info = self.scenes_params[scene_name].get("buttons", {})

        # Iterate over each button information in the dictionary
        for name, button_info in scene_buttons_info.items():
            # Extract information for the button from the dictionary
            graphic = button_info.get("graphic", "default_button")
            text = button_info.get("text", None)
            rect = button_info.get("rect", {})

            # Create a button using the ButtonManager and the extracted information
            button = self.button_manager.create_button()

            # Update the button's graphic if specified, and it exists in the graphic manager
            if graphic in self.graphic_manager.buttons:
                button.set_graphic(self.graphic_manager.create_graphic_instance(graphic, "button"))
            else:
                raise ValueError(f"Graphic '{graphic}' not found in the graphic manager.")

            # Update the button's text if specified
            if text:
                button.set_text(text)

            # Update the button's rect if specified
            if rect:
                button.set_rect(rect)

            # Store the button in the scene_buttons dictionary using its name as the key
            self.scene_buttons[name] = button

    def exit(self):
        """
        Called when exiting the scene.
        """
        self.button_manager.clear_buttons()

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
