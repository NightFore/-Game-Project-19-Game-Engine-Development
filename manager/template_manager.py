import pygame

class TemplateManager:
    """
    TemplateManager handles resources and their instances in the game.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries to store resources and instances
        self.resources = {}
        self.instances = {}

        # Define resource types to load for this manager
        self.resource_types_to_load = []

        # Initialize manager-related attributes
        self.manager_specific_attribute = None

    """
    Setup
        - load_resources
    """
    def start_manager(self, managers):
        self.set_managers(managers)
        self.initialize_resources()

    def set_managers(self, managers):
        """
        Load and set game managers.

        Args:
            managers (dict): A dictionary containing game managers.
        """
        self.managers = managers
        self.audio_manager = self.managers["audio_manager"]
        self.button_manager = self.managers["button_manager"]
        self.graphic_manager = self.managers["graphic_manager"]
        self.resource_manager = self.managers["resource_manager"]
        self.scene_manager = self.managers["scene_manager"]
        self.text_manager = self.managers["text_manager"]
        self.window_manager = self.managers["window_manager"]

    def initialize_resources(self):
        # Check that resources have unique names
        all_resource_names = []

        for resource_type in self.resource_types_to_load:
            # Load resources for each resource type
            loaded_resources = self.resource_manager.load_resources_from_manager(resource_type)

            # Check if any of the loaded resource names already exist
            for resource_name in loaded_resources:
                if resource_name in all_resource_names:
                    raise ValueError(f"Duplicate resource name '{resource_name}' found in {resource_type}.")

            # Add the loaded resources to the self.resources dictionary
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
            new_instance = SubTemplate(resource_data)
            self.instances[template_name] = new_instance
            return new_instance
        else:
            raise ValueError(f"Template '{template_name}' not found in resource templates.")

    def clear_resources(self):
        """
        Clear all resource instances.
        """
        self.instances.clear()


    """
    Render
        - update
        - draw
    """
    def update(self):
        pass

    def draw(self):
        pass




class SubTemplate:
    """
    SubTemplate class for managing sub-templates of resources.
    """
    def __init__(self, data):
        """
        Initialize a SubTemplate instance.

        Args:
            data (dict): A dictionary containing sub-template data.
        """
        self.data = data
        self.pos = data.get("pos", None)
        self.size = data.get("size", None)
        self.rect = data.get("rect", None)
        self.align = data.get("align", None)
        self.text = data.get("text", None)
        self.font = data.get("font", None)
        self.color = data.get("color", None)
        self.graphic = data.get("graphic", None)
        self.border_color = data.get("border_color", None)
        self.border_size = data.get("border_size", None)
        self.text_rect = None
        self.text_surface = None

    def customize(self, resource_template):
        """
        Customize a resource template using the sub-template data.

        Args:
            resource_template: The resource template to be customized.
        """
        pass

    def customize_position(self, pos):
        if self.pos is not None:
            self.pos = pos
            self.update_rect()

    def customize_size(self, size):
        if self.size is not None:
            self.size = size
            self.update_rect()

    def customize_rect(self, rect):
        if self.rect is not None:
            self.rect = rect
            self.update_rect()

    def customize_alignment(self, align):
        if self.align is not None:
            self.align = align
            self.update_rect()

    def customize_text(self, text):
        if self.text is not None:
            self.text = text
            self.update_text()

    def customize_font(self, font):
        if self.font is not None:
            self.font = font
            self.update_text()

    def customize_color(self, color):
        if self.color is not None:
            self.color = color
            self.update_text()

    def customize_graphic(self, graphic):
        if self.graphic is not None:
            self.graphic = graphic

    def update_rect(self):
        pass

    def update_text(self):
        pass

    """
    Render
        - update
        - draw
    """
    def update(self):
        pass

    def draw(self, screen):
        """
        Draw the sub-template on the screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        if self.graphic:
            self.graphic.draw(screen)
        else:
            if self.color:
                pygame.draw.rect(screen, self.color, self.rect)

            if self.border_size:
                pygame.draw.rect(screen, self.border_color, self.rect, self.border_size)

        if self.text:
            screen.blit(self.text_surface, self.text_rect)
