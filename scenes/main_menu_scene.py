from manager.scene_manager import SceneBase

class MainMenuScene(SceneBase):
    def __init__(self):
        super().__init__()

    def enter(self):
        super().enter()
        self.graphic_manager = self.managers["graphic_manager"]

        # Create a single image graphic instance
        self.single_graphic = self.graphic_manager.create_graphic_instance("default_single", "image")

        # Create an image sequence graphic instance
        self.sequence_animation = self.graphic_manager.create_graphic_instance("default_sequence", "image_sequence")


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

        # Update the single graphic
        self.single_graphic.update(dt)

        # Update the sequence animation (provide elapsed time for animation)
        self.sequence_animation.update(dt)

    def draw(self, screen):
        super().draw(screen)

        # Draw the single graphic
        self.single_graphic.draw(screen, (100, 100))

        # Draw the sequence animation
        self.sequence_animation.draw(screen, (300, 100))
