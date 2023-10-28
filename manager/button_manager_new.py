# button_manager.py

import pygame
from manager.template_manager import TemplateManager, TemplateInstance

class ButtonManager(TemplateManager):
    """
    ButtonManager manages the creation, updating, and rendering of buttons.

    Attributes:
        buttons (list): A list of Button instances managed by the ButtonManager.

    Methods:
    - Management
        - create_button(): Create a button and add it to the manager.
        - clear_buttons(): Clear all buttons from the manager.

    - Update and draw
        - update(mouse_pos): Update all buttons in the manager.
        - draw(screen): Draw all buttons on the screen.
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
        self.buttons = []


    """
    Render
        - update
        - draw
    """
    def update(self, mouse_pos):
        """
        Update all buttons in the manager.

        Args:
            mouse_pos (tuple): The current position of the mouse (x, y).
        """
        for button in self.buttons:
            button.update(mouse_pos)

    def draw(self, screen):
        """
        Draw all buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        for button in self.buttons:
            button.draw(screen)





class Button(TemplateInstance):
    def __init__(self, data, managers):
        """
        Initialize the Button.
        """
        super().__init__(data, managers)
        self.clicked = False
        self.clicked_and_released = False


    """
    Game Loop
        - update
        - draw
    """
    def update(self, mouse_pos):
        """
        Update the button's state.

        Args:
            mouse_pos (tuple): The current mouse rect in (x, y) coordinates.
        """
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                self.clicked_and_released = False
            else:
                if self.clicked:
                    self.clicked_and_released = True
                elif self.clicked_and_released:
                    self.clicked_and_released = False
                self.clicked = False
            self.graphic.color = self.graphic.color_active
        else:
            self.clicked = False
            self.clicked_and_released = False
            self.graphic.color = self.graphic.color_inactive

    def draw(self):
        """
        Draw the button.
        """
        super().draw()
