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

        # Start Game
        if self.scene_buttons["start"].clicked_and_released:
            self.scene_manager.set_scene("GameScene")

        # Settings Menu
        if self.scene_buttons["settings"].clicked_and_released:
            self.scene_manager.set_scene("SettingsScene")

    def draw(self, screen):
        super().draw(screen)
