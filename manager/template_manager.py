# template_manager.py

class TemplateManager:
    """
    TemplateManager manages resources and their instances in the game.

    Attributes:
        managers (dict): A dictionary containing game managers.
        resources (dict): A dictionary containing loaded resources.
        instances (dict): A dictionary containing resource instances.
        instance_class: The class used to create resource instances.
        resource_types_to_load (list): A list of resource types to load for this manager.
        manager_specific_attribute: An attribute specific to this manager.

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

    def clear_resources(self):
        """
        Clear all resource instances.
        """
        self.instances.clear()




class TemplateInstance:
    """
    TemplateInstance class for managing instances of resources.

    Attributes:
        data (dict): Input data for this instance.
        managers (dict): A dictionary containing game managers.
        mouse_pos: The current mouse position.
        screen: The game display surface.
        dt (float): Time since the last frame update.
        time_elapsed (float): Time elapsed since instance creation.

    Methods:
    - Rect Management
        - set_position(pos: tuple): Set the position of the instance.
        - set_size(size: tuple): Set the size of the instance.
        - set_rect(rect: tuple): Set the bounding rectangle of the instance.
        - set_align(align: str): Set the alignment of the instance within its bounding rectangle.
        - update_rect(): Update the instance's bounding rectangle.

    - Text Management
        - set_text(text: str): Set the text associated with the instance.
        - set_text_font(text_font): Set the font used for rendering text.
        - set_text_size(text_size: int): Set the size of the text.
        - set_text_color(text_color: tuple): Set the color of the text.
        - update_text(): Update the rendered text.

    - Graphic Management
        - set_graphic(graphic): Set the graphic resource associated with the instance.
        - update_graphic(): Update the graphic resource.

    - Render
        - update(): Update the instance.
        - draw(): Draw the instance.
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
        self.text_font = data.get("font", None)
        self.text_size = data.get("size", None)
        self.text_color = data.get("color", None)
        self.text_rect = None
        self.text_surface = None

        # Graphic attribute
        self.graphic = data.get("graphic", None)

        # Game attributes
        self.mouse_pos = self.game_manager.mouse_pos
        self.screen = self.game_manager.gameDisplay
        self.dt = self.game_manager.dt
        self.time_elapsed = 0


    """
    Rect Management
        - set_position
        - set_size
        - set_rect
        - set_align
        - update_rect
    """
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

    def update_rect(self):
        if self.text:
            self.text_rect.center = self.rect.center
        if self.graphic:
            self.graphic.update_rect()
            self.graphic.update_text()


    """
    Text Management
        - set_text
        - set_text_font
        - set_text_size
        - set_text_color
        - update_text
    """
    def set_text(self, text):
        self.text = text
        self.update_text()

    def set_text_font(self, text_font):
        self.text_font = text_font
        self.update_text()

    def set_text_size(self, text_size):
        self.text_size = text_size
        self.update_text()

    def set_text_color(self, text_color):
        self.text_color = text_color
        self.update_text()

    def update_text(self):
        if self.text:
            self.text_surface = self.text_font.render(self.text, True, self.text_color)
            self.text_rect = self.text_surface.get_rect()
            self.text_rect.center = self.rect.center


    """
    Graphic Management
        - set_graphic
        - update_graphic
    """
    def set_graphic(self, graphic):
        self.graphic = graphic
        self.update_graphic()

    def update_graphic(self):
        pass


    """
    Render
        - update
        - draw
    """
    def update(self):
        self.mouse_pos = self.game_manager.mouse_pos
        self.dt = self.game_manager.dt
        self.time_elapsed += self.dt

    def draw(self):
        if self.graphic:
            self.graphic.draw(self.screen)

        if self.text:
            self.screen.blit(self.text_surface, self.text_rect)
