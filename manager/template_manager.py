class TemplateManager:
    """
    TemplateManager handles resources and their instances in the game.

    Attributes:
        resources (dict): A dictionary containing resource templates.
        instances (dict): A dictionary containing resource instances.

    Methods:
    - Setup
        - load_resources_from_manager(resource_manager): Load resource templates from a ResourceManager.

    - Management
        - create_resource_instance(template_name): Create a new resource instance.
        - clear_resources(): Clear all resource instances.

    - Render
        - update
        - draw
    """
    def __init__(self):
        self.resources = {}
        self.instances = {}


    """
    Setup
        - load_resources
    """
    def load_resources(self, resource_manager):
        """
        Load resource templates from a ResourceManager.

        Args:
            resource_manager (ResourceManager): The ResourceManager containing loaded resource templates.
        """
        self.resource_templates = resource_manager.load_resources_from_manager("templates")


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
