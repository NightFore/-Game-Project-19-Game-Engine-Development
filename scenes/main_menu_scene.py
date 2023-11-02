from manager.scene_manager import SceneBase

class MainMenuScene(SceneBase):
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)

    """
    Scene Management
    """
    def enter(self):
        super().enter()

        self.init_debug()

    def exit(self):
        super().exit()

    def update(self):
        super().update()

    def draw(self):
        super().draw()


    """
    Scene Logic
    """
    def init_debug(self):
        button_dict = self.scene_data.get("buttons", {})
        print(self.scene_data)
        print(button_dict)

        for button_name, button_data in button_dict.items():
            button_resource = button_data.get("button", None)
            button_pos = button_data.get("pos", (0, 0))
            button_text = button_data.get("text", "")
            print(button_name, button_data)

            if button_resource:
                button_instance = self.button_manager.create_resource_instance(button_resource)
                button_instance.set_pos(button_pos)
                button_instance.set_text(button_text)

                # Add the button instance to the scene_buttons dictionary
                self.scene_buttons[button_name] = button_instance


    """
    Custom Functions
    """
    def debug_audio_manager(self):
        self.audio_manager.play_music("debug_music")
        self.audio_manager.play_sound("debug_sound")
