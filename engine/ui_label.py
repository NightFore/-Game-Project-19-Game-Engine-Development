# ui_label.py

import pygame
from engine.ui_element import UIElement


class UILabel(UIElement):
    """
    UILabel represents a label element in the UI.

    Attributes:
        Inherits from UIElement:
            - element_type (str): The type of the UI element.
            - element_id (str): ID of the UI element.
            - config (dict): Configuration dictionary for the element.
            - managers (dict): Dictionary of manager instances.
            - logger (Logger): Logger instance for logging.
            - x, y, width, height, label, font_name, font_size, color, image_path,
              font, rect, text_rect, text_surface, surface

        UILabel Attributes:
            - alignment (str): Text alignment within the label ('left', 'center', 'right').

    Methods:
        Game Loop:
            - update(mouse_pos, mouse_clicks): Update the UILabel state.
            - draw(surface): Draw the UILabel on the given surface.
    """
    def __init__(self, element_id, config, managers, logger):
        """
        Initialize the UILabel.

        Args:
            element_id (str): ID of the UI element.
            config (dict): Configuration dictionary for the element.
            managers (dict): Dictionary of manager instances.
            logger (Logger): Logger instance for logging.
        """
        super().__init__('label', element_id, config, managers, logger)

        # UIButton Attributes
        self.alignment = config.get('alignment', 'center')

    """
    Game Loop
        - update
        - draw
    """
    def update(self, mouse_pos, mouse_clicks):
        """
        Update the UILabel state.

        Args:
            mouse_pos (tuple): Current position of the mouse.
            mouse_clicks (list): List of mouse click states.
        """
        super().update(mouse_pos, mouse_clicks)

    def draw(self, surface):
        """
        Draw the UILabel on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the UILabel on.
        """
        if self.label and self.font:
            self.text_surface = self.font.render(self.label, True, self.color)
            if self.alignment == 'left':
                self.text_rect = self.text_surface.get_rect(topleft=self.rect.topleft)
            elif self.alignment == 'right':
                self.text_rect = self.text_surface.get_rect(topright=self.rect.topright)
            elif self.alignment == 'center':
                self.text_rect = self.text_surface.get_rect(center=self.rect.center)
            else:
                self.text_rect = self.text_surface.get_rect()
            surface.blit(self.text_surface, self.text_rect)
