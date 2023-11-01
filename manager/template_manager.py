# template_manager.py

import pygame

class TemplateManager:
    """
    TemplateManager manages resources and their instances in the game.

    Attributes:
    - managers (dict): A dictionary containing game managers.
    - resources (dict): A dictionary containing loaded resources.
    - instances (dict): A dictionary containing resource instances.
    - instance_class: The class used to create resource instances.
    - resource_types_to_load (list): A list of resource types to load for this manager.
    - manager_specific_attribute: An attribute specific to this manager.

    Methods:
    - Setup
        - set_managers(managers: dict): Load and set game managers.
        - set_resources(): Load resources of specified types and store them in the resources dictionary.

    - Management
        - create_resource_instance(template_name: str): Create a resource instance from a template.
        - clear_resources(): Clear all resource instances.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries
        self.managers = {}
        self.resources = {}
        self.instances = {}

        # Initialize the instance class for this manager
        self.instance_class = TemplateInstance

        # Define resource types to load for this manager
        self.resource_types_to_load = []

        # Initialize manager-related attributes
        self.manager_specific_attribute = None


    """
    Setup
        - set_managers
        - set_resources
    """
    def set_managers(self, managers):
        """
        Load and set game managers.

        Args:
            managers (dict): A dictionary containing game managers.
        """
        self.managers = managers
        self.game_manager = self.managers["game_manager"]
        self.audio_manager = self.managers["audio_manager"]
        self.button_manager = self.managers["button_manager"]
        self.graphic_manager = self.managers["graphic_manager"]
        self.resource_manager = self.managers["resource_manager"]
        self.scene_manager = self.managers["scene_manager"]
        self.text_manager = self.managers["text_manager"]
        self.window_manager = self.managers["window_manager"]

    def set_resources(self):
        for resource_type in self.resource_types_to_load:
            # Load resources for each resource type
            loaded_resources = self.resource_manager.resources[resource_type]

            # Add the loaded resources to the resources dictionary
            self.resources.update(loaded_resources)


    """
    Management
        - create_resource_instance
        - clear_resources
    """
    def create_resource_instance(self, template_name):
        """
        Create a resource instance from a template.

        Args:
            template_name (str): The name of the template to use for the resource.

        Returns:
            The created resource instance.
        """
        if template_name in self.resources:
            resource_data = self.resources[template_name]
            new_instance = self.instance_class(resource_data, self.managers)
            self.instances[template_name] = new_instance
            return new_instance
        else:
            raise ValueError(f"Template '{template_name}' not found in resource templates.")

    def create_instance_from_data(self, instance_data):
        """
        Create an instance (button, text, etc.) from a dictionary of data.

        Args:
            instance_data (dict): A dictionary containing instance information.

        Returns:
            The created instance.
        """
        new_instance = self.instance_class(instance_data, self.managers)
        return new_instance

    def clear_resources(self):
        """
        Clear all resource instances.
        """
        self.instances.clear()




class TemplateInstance:
    """
    TemplateInstance class for managing instances of resources.

    Inherited Attributes from GameManager:
    - instance_data (dict): Input data for this instance.
    - managers (dict): A dictionary containing game managers.

    Game Attributes:
    - screen (pygame.Surface): The game display surface.
    - mouse_pos (tuple): The current mouse position.
    - dt (float): Time since the last frame update.

    Methods:
    - Management
        - set_align(str): Set the alignment of the instance within its bounding rectangle.
        - update_rect(): Update the instance's bounding rectangle.

    - Render
        - update(): Update the instance.
        - draw(): Draw the instance.
    """
    def __init__(self, instance_data, managers):
        # Store the input data specific to this instance.
        self.instance_data = instance_data

        # Set the managers used for this instance.
        self.managers = managers
        self.game_manager = self.managers["game_manager"]
        self.audio_manager = self.managers["audio_manager"]
        self.button_manager = self.managers["button_manager"]
        self.graphic_manager = self.managers["graphic_manager"]
        self.resource_manager = self.managers["resource_manager"]
        self.scene_manager = self.managers["scene_manager"]
        self.text_manager = self.managers["text_manager"]
        self.window_manager = self.managers["window_manager"]

        # Game attributes
        self.screen = self.game_manager.gameDisplay
        self.mouse_pos = self.game_manager.mouse_pos
        self.dt = self.game_manager.dt


    """
    Management
        - set_align
        - update_rect
    """
    def set_align(self, align):
        self.align = align
        self.update_rect()

    def update_rect(self):
        if self.align == "center":
            self.rect.center = self.pos
        if self.align == "nw":
            self.rect.topleft = self.pos
        if self.align == "ne":
            self.rect.topright = self.pos
        if self.align == "sw":
            self.rect.bottomleft = self.pos
        if self.align == "se":
            self.rect.bottomright = self.pos
        if self.align == "n":
            self.rect.midtop = self.pos
        if self.align == "s":
            self.rect.midbottom = self.pos
        if self.align == "e":
            self.rect.midright = self.pos
        if self.align == "w":
            self.rect.midleft = self.pos


    """
    Render
        - update
        - draw
    """
    def update(self):
        self.mouse_pos = self.game_manager.mouse_pos
        self.dt = self.game_manager.dt

    def draw(self):
        pass
