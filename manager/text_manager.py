# text_manager.py

import pygame

class TextManager:
    """
    TextManager manages text resources and rendering text in the game.

    Attributes:
        text_templates (dict): A dictionary containing text templates.
        text_instances (list): A list to store text instances.

    Methods:
    - Setup
        - load_resources_from_manager(resource_manager): Load text resources from a ResourceManager.

    - Management
        - create_text_instance(template_name): Create a new text instance.
        - clear_texts(): Clear all text instances.
    """
    def __init__(self):
        self.text_templates = {}
        self.text_instances = []

    """
    Setup
        - load_resources
    """
    def load_resources(self, resource_manager):
        """
        Load text resources from a ResourceManager.

        Args:
            resource_manager (ResourceManager): The ResourceManager containing loaded text resources.
        """
        pass


    """
    Management
        - create_text_instance
        - clear_texts
    """
    def create_text_instance(self, template_name):
        """
        Create a text instance.

        Args:
            template_name (str): The name of the template to use for the text.

        Returns:
            Text: The created Text instance.
        """
        if template_name in self.text_templates:
            text_data = self.text_templates[template_name]
            new_text = Text(text_data)
            self.text_instances.append(new_text)
            return new_text
        else:
            raise ValueError(f"Template '{template_name}' not found in text resources.")

    def clear_texts(self):
        """
        Clear all text instances.
        """
        self.text_instances.clear()



class Text:
    """
    Text class for rendering and managing text.

    Attributes:
        text (str): The content of the text.
        font (pygame.font.Font): The font used for rendering the text.
        color (tuple): The color of the text in RGB format.
        position (tuple): The position of the text (x, y) on the screen.
        align (str): The alignment of the text inside the specified rect.

    Methods:
    - Setup (Text)
        - set_text(self, text): Set the text content.
        - set_font(self, font): Set the font for rendering the text.
        - set_color(self, color): Set the color of the text.
        - update_text(self): Update the text rendering.

    - Setup (Rect)
        - set_position(self, position): Set the position of the text.
        - set_align(self, align): Set the text alignment.
        - update_rect(self): Update the text's rectangular area.

    - Update and draw
        - update(self): Update the text.
        - draw(self, screen): Draw the text.
    """

    def __init__(self, data):
        """
        Initialize a Text instance.

        Args:
            data (dict): A dictionary containing text data.
        """
        self.font = data["font"]
        self.color = data["color"]
        self.text = data["text"]
        self.position = data["position"]
        self.align = data["align"]
        self.text_surface = None
        self.text_rect = None


    """
    Setup (Text)
        - set_text
        - set_font
        - set_color
        - update_text
    """
    def set_text(self, text):
        """
        Set the text content.

        Args:
            text (str): The text content to set.
        """
        self.text = text
        self.update_text()

    def set_font(self, font):
        """
        Set the font for rendering the text.

        Args:
            font (pygame.font.Font): The font to set.
        """
        self.font = font
        self.update_text()

    def set_color(self, color):
        """
        Set the color of the text.

        Args:
            color (tuple): The color of the text (R, G, B).
        """
        self.color = color
        self.update_text()

    def update_text(self):
        """
        Update the text surface with the current text, font, and color.
        """
        self.text_surface = self.font.render(self.text, True, self.color)
        self.update_rect()


    """
    Setup (Rect)
        - set_position
        - set_align
        - update_rect
    """
    def set_position(self, position):
        """
        Set the position of the text.

        Args:
            position (tuple): The position of the text (x, y).
        """
        self.position = position
        self.update_rect()

    def set_align(self, align):
        """
        Set the text alignment.

        Args:
            align (str): The text align.
        """
        self.align = align
        self.update_rect()

    def update_rect(self):
        """
        Update the text rect.
        """
        if self.align == "center":
            self.text_rect = self.text_surface.get_rect(center=self.position)
        elif self.align == "nw":
            self.text_rect = self.text_surface.get_rect(topleft=self.position)
        elif self.align == "n":
            self.text_rect = self.text_surface.get_rect(midtop=self.position)
        elif self.align == "ne":
            self.text_rect = self.text_surface.get_rect(topright=self.position)
        elif self.align == "w":
            self.text_rect = self.text_surface.get_rect(midleft=self.position)
        elif self.align == "e":
            self.text_rect = self.text_surface.get_rect(midright=self.position)
        elif self.align == "sw":
            self.text_rect = self.text_surface.get_rect(bottomleft=self.position)
        elif self.align == "s":
            self.text_rect = self.text_surface.get_rect(midbottom=self.position)
        elif self.align == "se":
            self.text_rect = self.text_surface.get_rect(bottomright=self.position)


    """
    Update and draw
        - update
        - draw
    """
    def update(self):
        """
        Placeholder for additional update logic.
        """
        pass

    def draw(self, screen):
        """
        Draw the text.

        Args:
            screen (pygame.Surface): The screen to draw the text on.
        """
        screen.blit(self.text_surface, self.text_rect)
