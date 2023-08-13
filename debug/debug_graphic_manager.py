# debug_graphic_manager.py

import pygame
from os import path

def debug_graphic_manager(graphic_manager, gameDisplay):
    # Get graphic and animation instances
    single_graphic = graphic_manager.create_graphic_instance("single")
    sequence_animation = graphic_manager.create_graphic_instance("sequence")

    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                gameDisplay.resize()
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with white color
        gameDisplay.fill((255, 255, 255))

        # Update and draw the single graphic
        single_graphic.update()
        single_graphic.draw(gameDisplay, (100, 100))

        # Update and draw the sequence animation based on time passed
        sequence_animation.update(dt)
        sequence_animation.draw(gameDisplay, (300, 100))

        gameDisplay.update(clock.get_fps())
        gameDisplay.draw()


    pygame.quit()
