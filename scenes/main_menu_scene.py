import pygame
from manager.scene_manager import SceneBase

class MainMenuScene(SceneBase):
    def __init__(self):
        super().__init__()

    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def update(self, dt):
        super().update(dt)

        if self.buttons["start"].clicked:
            self.managers["scene_manager"].set_scene("GameScene")

    def draw(self, screen):
        super().draw(screen)
