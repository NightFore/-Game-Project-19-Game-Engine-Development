# ui_manager.py

import pygame
import random
from pygame.rect import Rect
from pygame.font import Font
from engine.base_manager import BaseManager


class BaseButton:
    def __init__(self, position, size, color, text, click_callback=None, release_callback=None):
        self.rect = Rect(position, size)
        self.color = color
        self.default_color = color
        self.text = text
        self.font = Font(None, 32)  # Adjust font size here
        self.click_callback = click_callback
        self.release_callback = release_callback
        self.hold_color = pygame.Color('red')  # Color when button is held
        self.clicked = False
        self.held = False

    def is_clicked(self, mouse_pos):
        """
        Check if the button is clicked.

        Args:
            mouse_pos (tuple): Current mouse position (x, y).

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        """
        Draw the button on the given surface.

        Args:
            surface (pygame.Surface): Surface to draw the button on.
        """
        pygame.draw.rect(surface, self.color, self.rect)
        self.draw_text_centered(surface)

    def draw_text_centered(self, surface):
        """
        Draw text centered within the button.

        Args:
            surface (pygame.Surface): Surface to draw the text on.
        """
        text_render = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=self.rect.center)
        surface.blit(text_render, text_rect)

    def handle_event(self, event):
        """
        Handle events for the button.

        Args:
            event (pygame.event.Event): Pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if self.is_clicked(mouse_pos) and not self.clicked:
                    self.clicked = True
                    if self.click_callback:
                        self.click_callback(self)
            elif event.button == 3:  # Right mouse button
                mouse_pos = pygame.mouse.get_pos()
                if self.is_clicked(mouse_pos):
                    if self.on_right_click():
                        return
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button release
                self.clicked = False
                if self.release_callback:
                    self.release_callback(self)
        elif event.type == pygame.MOUSEMOTION:
            if self.clicked:
                if self.on_hold():
                    return

    def on_click(self):
        """
        Handle click event for the button.
        """
        if self.click_callback:
            self.click_callback(self)

    def on_release(self):
        """
        Handle release event for the button.
        """
        if self.release_callback:
            self.release_callback(self)

    def on_hold(self):
        """
        Handle hold event for the button (change color while held).
        """
        if not self.held:
            self.color = self.hold_color
            self.held = True
        return True

    def on_right_click(self):
        """
        Handle right click event for the button (destroy the button).
        """
        return False


class CountdownButton(BaseButton):
    def __init__(self, position, size, color, text, countdown_start, click_callback=None, release_callback=None):
        super().__init__(position, size, color, text, click_callback, release_callback)
        self.countdown_start = countdown_start
        self.countdown = countdown_start
        self.timer_event = pygame.USEREVENT + 1
        self.hold_event = pygame.USEREVENT + 2

    def start_countdown(self):
        """
        Start the countdown timer for the button.
        """
        pygame.time.set_timer(self.timer_event, 1000)
        pygame.time.set_timer(self.hold_event, 1000)

    def stop_countdown(self):
        """
        Stop the countdown timer for the button.
        """
        pygame.time.set_timer(self.timer_event, 0)
        pygame.time.set_timer(self.hold_event, 0)

    def update_text(self):
        """
        Update the button text based on countdown.
        """
        self.text = str(self.countdown)

    def reset(self):
        """
        Reset the countdown to a random number.
        """
        self.countdown = random.randint(5, 15)
        self.update_text()

    def handle_event(self, event):
        """
        Handle events specific to CountdownButton.

        Args:
            event (pygame.event.Event): Pygame event to handle.
        """
        super().handle_event(event)
        if event.type == self.timer_event:
            self.countdown -= 1
            self.update_text()
            if self.countdown <= 0:
                self.stop_countdown()
        elif event.type == self.hold_event:
            if self.clicked:
                print(f"Current countdown number for '{self.text}': {self.countdown}")

    def on_click(self):
        """
        Handle click event for CountdownButton.
        """
        super().on_click()
        self.reset()

    def on_release(self):
        """
        Handle release event for CountdownButton.
        """
        super().on_release()
        self.color = self.default_color

    def on_hold(self):
        """
        Handle hold event for CountdownButton (change color while held).
        """
        return super().on_hold()

    def on_right_click(self):
        """
        Handle right click event for CountdownButton (destroy the button).
        """
        self.stop_countdown()
        return True


class UIManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.buttons = []

    def create_button(self, position, size, color, text, click_callback=None, release_callback=None):
        button = BaseButton(position, size, color, text, click_callback, release_callback)
        self.buttons.append(button)

    def create_countdown_button(self, position, size, color, text, countdown_start, click_callback=None,
                               release_callback=None):
        button = CountdownButton(position, size, color, text, countdown_start, click_callback, release_callback)
        self.buttons.append(button)

    def handle_events(self, events):
        """
        Handle events for all UI elements.

        Args:
            events (list): List of pygame events to handle.
        """
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def update(self):
        """
        Update UI elements.
        """
        for button in self.buttons:
            if isinstance(button, CountdownButton):
                button.update_text()

    def draw(self, surface):
        """
        Draw UI elements on the given surface.

        Args:
            surface (pygame.Surface): Surface to draw UI elements on.
        """
        for button in self.buttons:
            button.draw(surface)

    def clear_buttons(self):
        """
        Clear all buttons from the UI manager.
        """
        self.buttons = []


# Sample callback function for button clicks
def button_click_callback(button):
    print(f"Button '{button.text}' clicked!")


# Sample callback function for countdown button clicks
def countdown_button_click_callback(button):
    print(f"Countdown Button '{button.text}' clicked!")


# Sample callback function for creating a set of countdown buttons
def create_countdown_buttons(ui_manager):
    ui_manager.clear_buttons()
    for i in range(10):
        button_text = f"Button {i+1}"
        ui_manager.create_countdown_button((random.randint(50, 750), random.randint(50, 550)),
                                           (100, 50), pygame.Color('blue'), button_text,
                                           random.randint(5, 15), countdown_button_click_callback)
    for button in ui_manager.buttons:
        button.start_countdown()


# Sample callback function for initializing the UI manager and creating initial UI elements
def initialize_ui_manager(ui_manager):
    ui_manager.clear_buttons()
    ui_manager.create_button((300, 250), (200, 100), pygame.Color('green'), "Start Game",
                             lambda button: create_countdown_buttons(ui_manager))


# Sample main function to demonstrate usage
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("UI Manager Demo")
    clock = pygame.time.Clock()

    ui_manager = UIManager()
    initialize_ui_manager(ui_manager)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        ui_manager.handle_events(events)
        ui_manager.update()

        screen.fill((30, 30, 30))
        ui_manager.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
