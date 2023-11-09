from manager.scene_manager import SceneBase

class Project1SettingsScene(SceneBase):
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

    def update_buttons(self):
        super().update_buttons()

        # Return to MainMenuScene
        if self.scene_buttons["return"].clicked_and_released:
            self.scene_manager.set_scene("MainMenuScene")

        # Music Volume
        if self.scene_buttons["music_volume_up"].clicked_and_released:
            self.audio_manager.increment_music_volume(0.1)
            self.update_text_volume()
        if self.scene_buttons["music_volume_down"].clicked_and_released:
            self.audio_manager.increment_music_volume(-0.1)
            self.update_text_volume()

        # Sound Volume
        if self.scene_buttons["sound_volume_up"].clicked_and_released:
            self.audio_manager.increment_sound_volume(0.1)
            self.update_text_volume()
        if self.scene_buttons["sound_volume_down"].clicked_and_released:
            self.audio_manager.increment_sound_volume(-0.1)
            self.update_text_volume()

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
        self.update_text_volume()

    def update_custom(self):
        pass

    def draw_custom(self):
        pass

    def update_text_volume(self):
        music_volume = str(int(100*self.audio_manager.music_volume)) + "/100"
        sound_volume = str(int(100*self.audio_manager.sound_volume)) + "/100"
        self.scene_texts["volume_music"].set_text(music_volume)
        self.scene_texts["volume_sound"].set_text(sound_volume)