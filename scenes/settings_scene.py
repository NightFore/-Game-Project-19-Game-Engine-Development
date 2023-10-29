from manager.scene_manager import SceneBase

class SettingsScene(SceneBase):
    def __init__(self, data, managers):
        super().__init__(data, managers)

    def enter(self):
        super().enter()
        self.audio_manager = self.managers["audio_manager"]
        self.window_manager = self.managers["window_manager"]

    def exit(self):
        super().exit()

    def update(self):
        super().update()

        # Return to MainMenuScene
        if self.scene_buttons["back"].clicked_and_released:
            self.scene_manager.set_scene("MainMenuScene")

        # Volume Up
        if self.scene_buttons["volume_up"].clicked_and_released:
            self.audio_manager.increment_music_volume(0.1)

        # Volume Down
        if self.scene_buttons["volume_down"].clicked_and_released:
            self.audio_manager.increment_music_volume(-0.1)

        # Toggle Fullscreen
        if self.scene_buttons["fullscreen"].clicked_and_released:
            self.window_manager.toggle_fullscreen()

    def draw(self):
        super().draw()
