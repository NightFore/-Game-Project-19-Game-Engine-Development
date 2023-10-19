import pygame
from manager.scene_manager import SceneBase

class SettingsScene(SceneBase):
    def __init__(self):
        super().__init__()

    def enter(self):
        super().enter()
        self.audio_manager = self.managers["audio_manager"]
        self.button_manager = self.managers["button_manager"]
        self.window_manager = self.managers["window_manager"]

    def exit(self):
        super().exit()

    def update(self, dt):
        super().update(dt)

        # Volume Up
        if self.buttons["volume_up"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.audio_manager.set_music_volume(self.audio_manager.music_volume + 0.1)

        # Volume Down
        if self.buttons["volume_down"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.audio_manager.set_music_volume(self.audio_manager.music_volume - 0.1)

        # Toggle Fullscreen
        if self.buttons["fullscreen_toggle"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.window_manager.toggle_fullscreen()

    def draw(self, screen):
        super().draw(screen)
