# button_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class ButtonManager(TemplateManager):
    """
    ButtonManager manages buttons and their instances in the game.

    Attributes:
        Inherited from TemplateManager:
            - managers (dict): A dictionary containing game managers.
            - instances (dict): A dictionary containing button instances.
            - instance_class: The class used to create button instances.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries
        self.managers = {}
        self.instances = []

        # Initialize the instance class for this manager
        self.instance_class = ButtonInstance




class ButtonInstance(TemplateInstance):
    """
    ButtonInstance class for managing instances of buttons.

    Attributes:
        Specific to ButtonInstance:
            - clicked (bool): Indicates whether the button has been clicked.
            - clicked_and_released (bool): Indicates whether the button was clicked and released in the current frame.

        Inherited from TemplateInstance (Rect Attributes):
            - pos (tuple): The position (x, y) of the instance.
            - size (tuple): The size (width, height) of the instance.
            - rect (pygame.Rect): The rectangular area that defines the instance's position and size.
            - align (str): The alignment of the instance within its bounding rectangle.

        Inherited from TemplateInstance (Instance Attributes):
            - text (str): The text associated with the instance.
            - text_instance: The text instance associated with the instance.
            - graphic_instance: The graphic instance associated with the instance.

        Inherited from TemplateInstance (Game Attributes):
            - screen (pygame.Surface): The game display surface.
            - mouse_pos (tuple): The current mouse position.

    Methods:
    - Management
        - set_text(text: str): Set the text associated with the instance.

    - Render
        - update(): Update the button.
        - draw(): Draw the button.
    """
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)

        # Initialize button state variables
        self.clicked = False
        self.clicked_and_released = False

        # Initialize text
        self.set_text(self.text)


    """
    Management
        - set_text
    """
    def set_text(self, text):
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
        if self.rect.collidepoint(self.mouse_pos):
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
