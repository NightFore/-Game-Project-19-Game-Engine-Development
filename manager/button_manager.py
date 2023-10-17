# button_manager.py

import pygame

class ButtonManager:
    """
    ButtonManager class manages the creation, updating, and rendering of buttons.

    Attributes:
        buttons (list): A list of Button instances managed by the ButtonManager.

    Example:
        # Create a ButtonManager instance.
        button_manager = ButtonManager()

        # Create a button and add it to the manager.
        button = button_manager.create_button((100, 100), "Click Me")

        # In the game loop, update and draw the buttons.
        while running:
            button_manager.update()
            button_manager.draw(screen)

    Methods:
    - Initialization
        - __init__: Initialize the ButtonManager.

    - Button Management
        - create_button(position, text): Create a button and add it to the manager.
        - clear_buttons(): Clear all buttons from the manager.

    - Update and draw
        - update(): Update all buttons in the manager.
        - draw(screen): Draw all buttons on the screen.
    """
    def __init__(self):
        """
        Initialize the ButtonManager.
        """
        self.buttons = []

    def create_button(self, position, text):
        """
        Create a button and add it to the manager.

        Args:
            position (tuple): The position of the button.
            text (str): The text to display on the button.

        Returns:
            Button: The created button instance.
        """
        button = Button(position, text)
        self.buttons.append(button)
        return button

    def clear_buttons(self):
        """
        Clear all buttons from the manager.
        """
        self.buttons.clear()

    def update(self):
        """
        Update all buttons in the manager.
        """
        for button in self.buttons:
            button.update()

    def draw(self, screen):
        """
        Draw all buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        for button in self.buttons:
            button.draw(screen)


class Button:
    """
    Button class for creating interactive buttons.

    Attributes:
        position (tuple): The position of the button.
        text (str): The text to display on the button.
        font (pygame.font.Font): The font used for rendering the button's text.
        rect (pygame.Rect): The rectangular area that defines the button.
        clicked (bool): Indicates whether the button has been clicked.
    """
    def __init__(self, position, text):
        """
        Initialize the Button.

        Args:
            position (tuple): The position of the button.
            text (str): The text to display on the button.
        """
        self.position = position
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(position[0], position[1], 150, 50)
        self.clicked = False

    def update(self):
        """
        Update the button's state.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                if self.clicked:
                    self.clicked = False

    def draw(self, screen):
        """
        Draw the button.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        color = (0, 255, 0) if self.rect.collidepoint(pygame.mouse.get_pos()) else (255, 255, 255)
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
