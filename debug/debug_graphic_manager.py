# debug_graphic_manager.py

class DebugGraphicManager:
    def __init__(self, graphic_manager, game_display):
        self.graphic_manager = graphic_manager
        self.game_display = game_display

        # Create a single image graphic instance
        self.single_graphic = self.graphic_manager.create_graphic_instance("default_single", "image")

        # Create an image sequence graphic instance
        self.sequence_animation = self.graphic_manager.create_graphic_instance("default_sequence", "image_sequence")

        # Set a fixed dt for 60 FPS
        self.dt = 16.66

    def update(self):
        # Update the single graphic
        self.single_graphic.update(self.dt)

        # Update the sequence animation (provide elapsed time for animation)
        self.sequence_animation.update(self.dt)

    def draw(self):
        # Draw the single graphic
        self.single_graphic.draw(self.game_display, (100, 100))

        # Draw the sequence animation
        self.sequence_animation.draw(self.game_display, (300, 100))
