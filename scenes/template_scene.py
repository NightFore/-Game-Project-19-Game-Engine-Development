from manager.scene_manager import SceneBase

class TemplateScene(SceneBase):
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
        pass

    def init_graphics(self):
        pass

    def update_buttons(self):
        pass

    def update_graphics(self, dt):
        pass

    def draw_graphics(self, screen):
        pass


    """
    Custom Functions
    """
    @staticmethod
    def hello_world():
        print("Hello World")
