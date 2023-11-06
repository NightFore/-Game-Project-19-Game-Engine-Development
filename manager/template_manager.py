# template_manager.py

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
        Setup
            - set_managers(managers): Load and set game managers.
            - set_resources(): Load resources of specified types and store them in the resources dictionary.

        Management
            - create_resource_instance(resource_name): Create a resource instance from a resource template.
            - clear_resources(): Clear all resource instances managed by this manager.
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
        self.main_manager = self.managers["main_manager"]
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
    def create_resource_instance(self, resource_name):
        """
        Create a resource instance from a resource template.

        Args:
            resource_name (str): The name of the resource template to use for the resource.

        Returns:
            TemplateInstance: The created resource instance.

        Raises:
            ValueError: If the specified resource template does not exist in the resources dictionary.
        """
        if resource_name in self.resources:
            resource_data = self.resources[resource_name]
            new_instance = self.instance_class(resource_data, self.managers)
            self.instances[resource_name] = new_instance
            return new_instance
        else:
            raise ValueError(f"Template '{resource_name}' not found in resource templates.")

    def clear_resources(self):
        """
        Clear all resource instances managed by this manager.
        """
        self.instances.clear()




class TemplateInstance:
    """
    TemplateInstance class for managing instances of resources.

    Attributes:
        Inherited Attributes from TemplateManager:
            - instance_data (dict): Input data for this instance.
            - managers (dict): A dictionary containing game managers.

        Inherited Attributes from MainManager:
            - screen (pygame.Surface): The game display surface.
            - mouse_pos (tuple): The current mouse position.
            - dt (float): Time since the last frame update.

    Methods:
        Render:
            - update (): Update the instance.
            - draw (): Draw the instance.
    """
    def __init__(self, instance_data, managers):
        # Store the input data specific to this instance.
        self.instance_data = instance_data

        # Set the managers used for this instance.
        self.managers = managers
        self.main_manager = self.managers["main_manager"]
        self.audio_manager = self.managers["audio_manager"]
        self.button_manager = self.managers["button_manager"]
        self.graphic_manager = self.managers["graphic_manager"]
        self.resource_manager = self.managers["resource_manager"]
        self.scene_manager = self.managers["scene_manager"]
        self.text_manager = self.managers["text_manager"]
        self.window_manager = self.managers["window_manager"]

        # Game attributes
        self.screen = self.main_manager.gameDisplay
        self.mouse_pos = self.main_manager.mouse_pos
        self.dt = self.main_manager.dt


    """
    Render:
        - update
        - draw
    """
    def update(self):
        """
        Update the instance.
        """
        self.mouse_pos = self.main_manager.mouse_pos
        self.dt = self.main_manager.dt

    def draw(self):
        """
        Draw the instance.
        """
        pass
