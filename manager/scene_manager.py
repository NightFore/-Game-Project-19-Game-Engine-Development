# scene_manager.py

import pygame
import os
import inspect
import importlib

from manager.button_manager import ButtonManager

class SceneManager:
    """
    SceneManager handles game scenes and buttons.

    Attributes:
        scenes (dict): A dictionary containing loaded game scenes.
        scenes_params (dict): A dictionary containing scene parameters.
        current_scene (SceneBase): The currently active game scene.

    Methods:
    - Initial Loading
        - set_managers(managers): Load and set game managers in the SceneManager.
        - load_scene_parameters(params_dict): Load scene parameters from a dictionary and store them.
        - load_scenes_from_directory(directory): Load game scenes from Python files in the specified directory and add them to the SceneManager.

    - Scene Management
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
        self.scenes_params = None
        self.current_scene = None


    """
    Initial Loading
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
                        # Create an instance of the scene class and add it to the SceneManager
                        scene_instance = obj(self.scenes_params, self.managers)
                        self.scenes[name] = scene_instance


    """
    Scene Management
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
                # Exit the current scene and clear its buttons
                self.current_scene.exit()
                self.managers["button_manager"].clear_buttons()

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
        scene_params (dict): A dictionary containing scene parameters.
        button_manager (ButtonManager): A ButtonManager instance for managing buttons in scenes.

    Example:
        # Create a custom scene class that inherits from SceneBase.
        class CustomScene(SceneBase):
            def __init__(self, scene_manager):
                super().__init__(scene_manager)

            def enter(self):
                # Called when entering the scene.
                # Add custom code here.

            def exit(self):
                # Called when exiting the scene.
                # Add custom code here.

            def update(self, dt):
                # Update the scene.
                # Add custom code here.

            def draw(self, screen):
                # Draw the scene and its buttons on the screen.
                # Add custom code here.

    Dependencies:
        - SceneManager: A SceneManager instance is required for managing game scenes.
        - ButtonManager: A ButtonManager instance is used to manage buttons in scenes.

    Methods:
    - Scene Initialization
        - set_scene_params(scene_params): Set scene parameters for the scene.
        - set_button_manager(button_manager): Set the ButtonManager instance for the scene.

    - Button Management
        - create_buttons_from_dict(scene_name): Create buttons based on scene parameters.

    - Scene Lifecycle
        - enter(): Called when entering the scene. Create and configure buttons here.
        - exit(): Called when exiting the scene.
        - update(dt): Update the scene.
        - draw(screen): Draw the scene and its buttons on the screen.
    """
    def __init__(self, scenes_params, managers):
        """
        Initialize the SceneBase.
        """
        self.scenes_params = None
        self.button_manager = None


    """
    Scene Initialization
        - set_scene_params
        - set_button_manager
    """
    def set_scene_settings(self, managers, scene_params):
        """
        Set the scene parameters for the scene.

        Args:
            managers
            scene_params (dict): The dictionary of scene parameters.
        """
        self.managers = managers
        self.scene_params = scene_params

    def set_button_manager(self, button_manager):
        """
        Set the button manager for the scene.

        Args:
            button_manager (ButtonManager): The button manager to set.
        """
        self.button_manager = button_manager


    """
    Button Management
        - create_buttons_from_dict
    """
    def create_buttons_from_dict(self, scene_name):
        """
        Create buttons based on button information retrieved from the scene_params.

        Args:
            scene_name (str): The name of the scene to retrieve button information for.
        """
        # Retrieve button information for the specific scene from the scene_params dictionary
        scene_button_info = self.scene_params.get(scene_name, {}).get("buttons", [])

        # Initialize an empty dictionary to store the created buttons
        self.buttons = {}

        # Iterate over each button information in the list
        for button_info in scene_button_info:
            # Extract information for the button from the dictionary
            name = button_info["name"]
            position = button_info["position"]
            text = button_info["text"]

            # Create a button using the ButtonManager and the extracted information
            button = self.button_manager.create_button(position, text)

            # Store the button in the buttons dictionary using its name as the key
            self.buttons[name] = button


    """
    Scene Lifecycle
        - enter
        - exit
        - update
        - draw
    """
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
