from manager.scene_manager import SceneBase

class MainMenuScene(SceneBase):
    def __init__(self):
        super().__init__()

    """
    Scene Management
    """
    def enter(self):
        super().enter()
        self.init_managers()
        self.init_graphics()

    def exit(self):
        super().exit()

    def update(self, dt):
        super().update(dt)
        self.update_buttons()
        self.update_graphics(dt)

    def draw(self, screen):
        super().draw(screen)
        self.draw_graphics(screen)


    """
    Scene Logic
    """
    def init_managers(self):
        self.game_manager = self.managers["game_manager"]
        self.audio_manager = self.managers["audio_manager"]
        self.graphic_manager = self.managers["graphic_manager"]
        self.window_manager = self.managers["window_manager"]

    def init_graphics(self):
        self.single_graphic = self.graphic_manager.create_graphic_instance("default_single", "image")
        self.sequence_animation = self.graphic_manager.create_graphic_instance("default_sequence", "image_sequence")

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

    def update_graphics(self, dt):
        self.single_graphic.update(dt)
        self.sequence_animation.update(dt)

    def draw_graphics(self, screen):
        self.single_graphic.draw(screen, (100, 100))
        self.sequence_animation.draw(screen, (300, 100))


    """
    Custom Functions
    """
    def debug_audio_manager(self):
        self.audio_manager.play_music("debug_music")
        self.audio_manager.play_sound("debug_sound")
