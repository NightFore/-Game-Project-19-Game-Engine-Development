# template_manager.py

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

    def clear_resources(self):
        """
        Clear all resource instances.
        """
        self.instances.clear()




class TemplateInstance:
    """
    TemplateInstance class for managing instances of resources.
    """
    def __init__(self, data, managers):
        # Store the input data for this instance.
        self.data = data

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

        # Rect attributes
        self.pos = data.get("pos", None)
        self.size = data.get("size", None)
        self.rect = data.get("rect", None)
        self.border_radius = data.get("border_radius", None)
        self.align = data.get("align", None)

        # Text attributes
        self.text = data.get("text", None)
        self.text_font = data.get("text_font", None)
        self.text_color = data.get("text_color", None)
        self.text_rect = None
        self.text_surface = None

        # Graphic attribute
        self.graphic = data.get("graphic", None)

        # Time attributes
        self.dt = self.game_manager.dt
        self.time_elapsed = 0

        # Screen attribute
        self.screen = self.game_manager.gameDisplay

    def set_position(self, pos):
        self.pos = pos
        self.rect[0], self.rect[1] = pos
        self.update_rect()

    def set_size(self, size):
        self.size = size
        self.rect[2], self.rect[3] = size
        self.update_rect()

    def set_rect(self, rect):
        self.rect = rect
        self.pos = self.rect[0], self.rect[1]
        self.size = self.rect[2], self.rect[3]
        self.update_rect()

    def set_align(self, align):
        self.align = align
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
        self.update_rect()

    def set_text(self, text):
        self.text = text
        self.update_text()

    def set_font(self, text_font):
        self.text_font = text_font
        self.update_text()

    def set_text_color(self, text_color):
        self.text_color = text_color
        self.update_text()

    def set_graphic(self, graphic):
        self.graphic = graphic

    def update_rect(self):
        if self.text:
            self.text_rect.center = self.rect.center
        if self.graphic:
            self.graphic.update_rect()
            self.graphic.update_text()

    def update_text(self):
        if self.text:
            self.text_surface = self.text_font.render(self.text, True, self.text_color)
            self.text_rect = self.text_surface.get_rect()
            self.text_rect.center = self.rect.center

    def update(self):
        self.dt = self.game_manager.dt
        self.time_elapsed += self.dt

    def draw(self):
        if self.graphic:
            self.graphic.draw(self.screen)

        if self.text:
            self.screen.blit(self.text_surface, self.text_rect)
