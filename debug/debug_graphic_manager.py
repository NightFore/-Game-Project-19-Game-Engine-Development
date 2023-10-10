# debug_graphic_manager.py

import pygame

class DebugGraphicManager:
    def __init__(self, graphic_manager, gameDisplay):
        self.graphic_manager = graphic_manager
        self.gameDisplay = gameDisplay
        # self.single_graphic = self.graphic_manager.create_graphic_instance("single")
        # self.sequence_animation = self.graphic_manager.create_graphic_instance("sequence")

    def update(self):
        pass
        # self.single_graphic.update()
        # self.sequence_animation.update(10)

    def draw(self):
        pass
        # Draw the single graphic
        # self.single_graphic.draw(self.gameDisplay, (100, 100))

        # Draw the sequence animation
        # self.sequence_animation.draw(self.gameDisplay, (300, 100))

