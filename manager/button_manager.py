# button_manager.py

import pygame

class Button:
    """
    Button class for creating interactive buttons.
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

class ButtonManager:
    """
    ButtonManager class manages the creation, updating, and rendering of buttons.
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
