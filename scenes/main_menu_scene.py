class MainMenuScene(SceneBase):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)

    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def update(self, dt):
        super().update(dt)

        # Check if the "start" button is clicked
        if self.buttons["start"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.buttons["start"].clicked = True
            else:
                if self.buttons["start"].clicked:
                    self.buttons["start"].clicked = False
                    self.scene_manager.set_scene("game")

    def draw(self, screen):
        super().draw(screen)