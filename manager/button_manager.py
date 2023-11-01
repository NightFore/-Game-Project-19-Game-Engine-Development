# button_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class ButtonManager(TemplateManager):
    """
    ButtonManager manages buttons and their instances in the game.

    Attributes:
        managers (dict): A dictionary containing game managers.
        resources (dict): A dictionary containing loaded resources.
        instances (dict): A dictionary containing resource instances.
        instance_class: The class used to create resource instances.
        resource_types_to_load (list): A list of resource types to load for this manager.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries
        self.managers = {}
        self.resources = {}
        self.instances = {}

        # Initialize the instance class for this manager
        self.instance_class = ButtonInstance

        # Define resource types to load for this manager
        self.resource_types_to_load = ["button"]




class ButtonInstance(TemplateInstance):
    """
    ButtonInstance class for managing instances of buttons.

    Args:
        instance_data (dict): A dictionary containing instance-specific data.
        managers (dict): A dictionary containing various game managers.

    Attributes:
        clicked (bool): A flag indicating if the button has been clicked.
        clicked_and_released (bool): A flag indicating if the button has been clicked and released.
        pos (tuple): The position of the button.
        text (str): The text displayed on the button.
        align (str): The alignment of the button.
        graphic_instance (GraphicInstance): The graphic instance associated with the button.
        text_instance (TextInstance): The text instance associated with the button.

    Methods:
    - Management
        - set_pos(pos): Set the position of the button.
        - set_text(text): Set the text of the button.
    - Render
        - update(): Update the button's state.
        - draw(): Draw the button.
    """
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)

        # Initialize button state variables
        self.clicked = False
        self.clicked_and_released = False

        # Initialize instance variables
        self.pos = None
        self.text = None
        self.align = instance_data.get("align", None)

        # Create a text instance if a font_name is provided
        font_name = instance_data.get("font_name", None)
        if font_name:
            self.text_instance = self.text_manager.create_resource_instance(font_name)

        # Create a graphic instance based on graphic_name
        graphic_name = instance_data.get("graphic_name", None)
        self.graphic_instance = self.graphic_manager.create_resource_instance(graphic_name)


    """
    Management
        - set_pos
        - set_text
    """
    def set_pos(self, pos):
        """
        Set the position of the button.
        """
        self.pos = pos
        self.graphic_instance.set_pos(pos)
        if self.text_instance:
            self.text_instance.set_pos(pos)

    def set_text(self, text):
        """
        Set the text of the button.
        """
        self.text = text
        if self.text_instance:
            self.text_instance.set_text(text)


    """
    Render
        - update
        - draw
    """
    def update(self):
        """
        Update the button.
        """
        super().update()


        # Check if the mouse is over the button.
        if self.graphic_instance.rect.collidepoint(self.mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # Mouse button is pressed
                self.clicked = True
                self.clicked_and_released = False
            else:
                # Mouse button is released
                if self.clicked:
                    self.clicked_and_released = True
                elif self.clicked_and_released:
                    self.clicked_and_released = False
                self.clicked = False
            # Change the button's color to the active state
            self.graphic_instance.color = self.graphic_instance.color_active
        else:
            # Mouse is not over the button, reset the button state and color
            self.clicked = False
            self.clicked_and_released = False
            self.graphic_instance.color = self.graphic_instance.color_inactive

    def draw(self):
        """
        Draw the button.
        """
        super().draw()
