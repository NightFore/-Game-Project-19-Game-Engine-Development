from manager.scene_manager import SceneBase

class LevelSelectionScene(SceneBase):
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
        for i in range(1, 18+1):
            button_name = i
            button_resource = "button_interface"
            button_pos = (10+400*((i-1) // 10), 10+70*((i-1) % 10))
            button_text = i
            button_align = "nw"

            button_instance = self.button_manager.create_resource_instance(button_resource)
            button_instance.set_pos(button_pos)
            button_instance.set_text(button_text)
            button_instance.set_align(button_align)
            self.scene_buttons[button_name] = button_instance

    def update_custom(self):
        pass

    def draw_custom(self):
        pass
