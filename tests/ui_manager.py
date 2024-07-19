# ui_manager.py

import pygame
import random
from pygame.rect import Rect
from pygame.font import Font
from engine.base_manager import BaseManager


class UIElement:
    def __init__(self, position, size, color):
        self.rect = Rect(position, size)
        self.color = color


class BaseButton(UIElement):
    def __init__(self, position, size, color, text):
        super().__init__(position, size, color)
        self.text = text
        self.font = Font(None, 32)  # Adjust font size here

    def is_clicked(self, mouse_pos):
        """
        Check if the button is clicked.

        Args:
            mouse_pos (tuple): Current mouse position (x, y).

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)

    def draw_text_centered(self, surface):
        """
        Draw text centered within the button.

        Args:
            surface (pygame.Surface): Surface to draw the text on.
        """
        text_render = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=self.rect.center)
        surface.blit(text_render, text_rect)


class CountdownButton(BaseButton):
    def __init__(self, position, size, color, text, countdown_start):
        super().__init__(position, size, color, text)
        self.countdown_start = countdown_start
        self.countdown = countdown_start
        self.timer_event = pygame.USEREVENT + 1

    def start_countdown(self):
        """
        Start the countdown timer for the button.
        """
        pygame.time.set_timer(self.timer_event, 1000)

    def stop_countdown(self):
        """
        Stop the countdown timer for the button.
        """
        pygame.time.set_timer(self.timer_event, 0)

    def update_text(self):
        """
        Update the button text based on countdown.
        """
        self.text = str(self.countdown)

    def reset(self):
        """
        Reset the button text and countdown.
        """
        self.text = self.initial_text
        self.countdown = self.countdown_start

    def handle_event(self, event):
        """
        Handle events specific to CountdownButton.

        Args:
            event (pygame.event.Event): Pygame event to handle.
        """
        if event.type == self.timer_event:
            self.countdown -= 1
            self.update_text()
            if self.countdown <= 0:
                self.stop_countdown()


class UIManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.ui_elements = []
        self.selected_button = None

    def load_main_screen(self):
        # Load main screen button
        button_position = (300, 250)
        button_size = (200, 50)
        button_color = (50, 150, 255)
        button_text = "Start Game"
        main_button = BaseButton(button_position, button_size, button_color, button_text)
        self.ui_elements.append(main_button)

    def load_game_screen(self):
        # Clear existing UI elements
        self.ui_elements.clear()

        # Load a dozen CountdownButtons with countdown text
        button_positions = [
            (100, 100), (300, 100), (500, 100),
            (100, 250), (300, 250), (500, 250),
            (100, 400), (300, 400), (500, 400),
            (100, 550), (300, 550), (500, 550)
        ]
        for pos in button_positions:
            button_size = (100, 50)
            button_color = (50, 150, 255)
            button_text = "10"  # Initial countdown value
            game_button = CountdownButton(pos, button_size, button_color, button_text, countdown_start=10)
            self.ui_elements.append(game_button)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                for element in self.ui_elements:
                    if isinstance(element, BaseButton):
                        if element.is_clicked(mouse_pos):
                            if element.text == "Start Game":
                                self.load_game_screen()
                            else:
                                # Handle specific behavior for CountdownButton on click
                                if isinstance(element, CountdownButton):
                                    element.text = str(random.randint(1, 20))
                                    element.start_countdown()
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for element in self.ui_elements:
                if isinstance(element, BaseButton):
                    if element.rect.collidepoint(mouse_pos):
                        element.color = (150, 150, 255)  # Light blue when mouse over
                    else:
                        element.color = (50, 150, 255)   # Normal color
        else:
            for element in self.ui_elements:
                if isinstance(element, CountdownButton):
                    element.handle_event(event)

    def draw_ui(self, surface):
        for element in self.ui_elements:
            if isinstance(element, BaseButton):
                pygame.draw.rect(surface, element.color, element.rect)
                element.draw_text_centered(surface)
