# button_manager.py

import pygame

class ButtonManager:
    """
    ButtonManager class manages the creation, updating, and rendering of buttons.

    Attributes:
        buttons (list): A list of Button instances managed by the ButtonManager.

    Methods:
    - Setup
        - set_managers(graphic_manager): Set the graphic manager for the buttons.

    - Management
        - create_button(): Create a button and add it to the manager.
        - clear_buttons(): Clear all buttons from the manager.

    - Update and draw
        - update(mouse_pos): Update all buttons in the manager.
        - draw(screen): Draw all buttons on the screen.
    """
    def __init__(self):
        """
        Initialize the ButtonManager.
        """
        self.buttons = []


    """
    Setup
        - set_managers
    """
    def set_managers(self, graphic_manager):
        self.graphic_manager = graphic_manager


    """
    Management
        - create_button
        - clear_buttons
    """
    def create_button(self):
        """
        Create a button instance.

        Returns:
            Button: The created button instance.
        """
        button = Button()
        self.buttons.append(button)
        return button

    def clear_buttons(self):
        """
        Clear all buttons from the manager.
        """
        self.buttons.clear()


    """
    Update and draw
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



class Button:
    """
    Button class for creating interactive buttons.

    Attributes:
        graphic (str or Graphic): The graphic associated with the button.
        text (str): The text to display on the button.
        rect (pygame.Rect): The rectangular area that defines the button.
        font (pygame.font.Font): The font used for rendering the button's text.
        clicked (bool): Indicates whether the button has been clicked.
        clicked_and_released (bool): Indicates whether the button was clicked and released in the current frame.

    Methods:
    - Setup
        - set_graphic(graphic): Set the graphic for the button.
        - set_text(text): Set the text to display on the button.
        - set_rect(rect): Set the rectangular area that defines the button.

    - Update and draw
        - update(mouse_pos): Update the button's state.
        - draw(screen): Draw the button.
    """
    def __init__(self):
        """
        Initialize the Button.
        """
        self.graphic = None
        self.text = None
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.clicked = False
        self.clicked_and_released = False


    """
    Setup
        - set_graphic(graphic): Set the graphic for the button.
        - set_text(text): Set the text to display on the button.
        - set_rect(rect): Set the rectangular area that defines the button.
    """
    def set_graphic(self, graphic):
        """
        Set the graphic for the button.

        Args:
            graphic (Graphic): The graphic associated with the button.
        """
        self.graphic = graphic

    def set_text(self, text):
        """
        Set the text to display on the button.

        Args:
            text (str): The text to display on the button.
        """
        self.text = text

    def set_rect(self, rect):
        """
        Set the rectangular area that defines the button.

        Args:
            rect (tuple or pygame.Rect): The rectangular area (x, y, width, height) to define the button.
        """
        self.rect = pygame.Rect(rect)
        self.graphic.set_rect(self.rect)


    """
    Update and draw
        - update
        - draw
    """
    def update(self, mouse_pos):
        """
        Update the button's state.

        Args:
            mouse_pos (tuple): The current mouse position in (x, y) coordinates.
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

    def draw(self, screen):
        """
        Draw the button.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        self.graphic.draw(screen)
        if self.text:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
