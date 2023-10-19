import pygame
from manager.scene_manager import SceneBase

class GameScene(SceneBase):
    def __init__(self):
        super().__init__()

    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def update(self, dt):
        super().update(dt)

        # Check if the "game_over" button is clicked
        if self.buttons["game_over"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.buttons["game_over"].clicked = True
            else:
                if self.buttons["game_over"].clicked:
                    self.buttons["game_over"].clicked = False
                    self.scene_manager.set_scene("MainMenuScene")

        # Check if the "click_me" button is clicked
        if self.buttons["click_me"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.buttons["click_me"].clicked = True
            else:
                if self.buttons["click_me"].clicked:
                    self.buttons["click_me"].clicked = False
                    print("Hello World")

        # Reset button states
        for button in self.buttons.values():
            button.clicked = False

    def draw(self, screen):
        super().draw(screen)
