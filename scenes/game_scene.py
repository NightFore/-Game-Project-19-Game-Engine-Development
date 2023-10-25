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

        # Return to the Main Menu
        if self.scene_buttons["game_over"].clicked_and_released:
            self.scene_manager.set_scene("MainMenuScene")

        # Test Button
        if self.scene_buttons["click_me"].clicked_and_released:
            print("Hello World")

    def draw(self, screen):
        super().draw(screen)
