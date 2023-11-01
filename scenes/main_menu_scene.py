from manager.scene_manager import SceneBase

class MainMenuScene(SceneBase):
    def __init__(self, data, managers):
        super().__init__(data, managers)

    """
    Scene Management
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


    """
    Custom Functions
    """
    def debug_audio_manager(self):
        self.audio_manager.play_music("debug_music")
        self.audio_manager.play_sound("debug_sound")
