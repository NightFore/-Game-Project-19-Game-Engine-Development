from manager.scene_manager import SceneBase

class MainMenuScene(SceneBase):
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)


    """
    Lifecycle
    """
    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def update(self):
        super().update()

    def draw(self):
        super().draw()


    """
    Scene Logic
    """
    def init_buttons(self):
        super().init_buttons()

    def init_graphics(self):
        super().init_graphics()

    def init_texts(self):
        super().init_texts()
        self.scene_texts["project_title"].set_text(self.game_manager.project_title)

    def update_buttons(self):
        super().update_buttons()
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

    def update_graphics(self):
        super().update_graphics()

    def update_texts(self):
        super().update_texts()

    def draw_buttons(self):
        super().draw_buttons()

    def draw_graphics(self):
        super().draw_graphics()

    def draw_texts(self):
        super().draw_texts()


    """
    Custom Functions
    """
    def init_custom(self):
        pass

    def update_custom(self):
        pass

    def draw_custom(self):
        pass

    def debug_audio_manager(self):
        self.audio_manager.play_music("debug_music")
        self.audio_manager.play_sound("debug_sound")
