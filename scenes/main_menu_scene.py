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

        if self.scene_buttons["start"].clicked_and_released:
            self.scene_manager.set_scene("GameScene")

    def draw(self, screen):
        super().draw(screen)
