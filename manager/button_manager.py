# button_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class ButtonManager(TemplateManager):
    """
    ButtonManager manages button resources and their instances in the game.
    """
    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize dictionaries
        self.instances = []

        # Initialize the instance class for this manager
        self.instance_class = ButtonInstance




class ButtonInstance(TemplateInstance):
    """
    ButtonInstance class for managing instances of buttons.

    Attributes:
        clicked (bool): Indicates whether the button has been clicked.
        clicked_and_released (bool): Indicates whether the button was clicked and released in the current frame.

    Methods:
    - Render
        - update(): Update the button.
        - draw(): Draw the button.
    """
    def __init__(self, data, managers):
        super().__init__(data, managers)

        self.clicked = False
        self.clicked_and_released = False


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
            self.graphic.color = self.graphic.color_active
        else:
            # Mouse is not over the button, reset the button state and color
            self.clicked = False
            self.clicked_and_released = False
            self.graphic.color = self.graphic.color_inactive

    def draw(self):
        """
        Draw the button.
        """
        super().draw()
