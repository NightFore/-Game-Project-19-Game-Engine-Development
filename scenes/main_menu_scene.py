from manager.scene_manager import SceneBase

class MainMenuScene(SceneBase):
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)


    """
    Scene Management
    """
    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def update(self):
        super().update()
        self.update_buttons()

    def draw(self):
        super().draw()


    """
    Scene Logic
    """
    def update_buttons(self):
        if self.scene_buttons["start"].clicked_and_released:
            self.scene_manager.set_scene("GameScene")
        if self.scene_buttons["settings"].clicked_and_released:
            self.scene_manager.set_scene("SettingsScene")
        if self.scene_buttons["debug_audio"].clicked_and_released:
            self.debug_audio_manager()
        if self.scene_buttons["pause_music"].clicked_and_released:
            self.audio_manager.pause_music()
        if self.scene_buttons["toggle_music"].clicked_and_released:
            self.audio_manager.toggle_music()
        if self.scene_buttons["toggle_zoom"].clicked_and_released:
            self.window_manager.toggle_zoom()
        if self.scene_buttons["quit_game"].clicked_and_released:
            self.game_manager.quit_game()


    """
    Custom Functions
    """
    def debug_audio_manager(self):
        self.audio_manager.play_music("debug_music")
        self.audio_manager.play_sound("debug_sound")
