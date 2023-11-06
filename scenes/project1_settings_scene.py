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
