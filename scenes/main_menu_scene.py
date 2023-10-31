from manager.scene_manager import SceneBase

class MainMenuScene(SceneBase):
    def __init__(self, data, managers):
        super().__init__(data, managers)

    """
    Scene Management
    """
    def enter(self):
        super().enter()
        self.init_managers()
        self.init_graphics()

    def exit(self):
        super().exit()

    def update(self):
        super().update()
        self.update_buttons()
        self.update_graphics(self.dt)

    def draw(self):
        super().draw()
        self.draw_graphics(self.screen)


    """
    Scene Logic
    """
    def init_managers(self):
        self.game_manager = self.managers["game_manager"]
        self.audio_manager = self.managers["audio_manager"]
        self.graphic_manager = self.managers["graphic_manager"]
        self.window_manager = self.managers["window_manager"]

    def init_graphics(self):
        self.single_graphic = self.graphic_manager.create_resource_instance("default_single")
        self.sequence_animation = self.graphic_manager.create_resource_instance("default_sequence")
        self.single_graphic.set_pos((100, 100))
        self.sequence_animation.set_pos((300, 100))

        self.test = self.text_manager.create_resource_instance("liberation_serif")
        self.test.set_pos((900, 600))
        self.test.set_text("Test")

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
        self.single_graphic.update()
        self.sequence_animation.update()
        self.test.update()

    def draw_graphics(self, screen):
        self.single_graphic.draw()
        self.sequence_animation.draw()
        self.test.draw()


    """
    Custom Functions
    """
    def debug_audio_manager(self):
        self.audio_manager.play_music("debug_music")
        self.audio_manager.play_sound("debug_sound")
