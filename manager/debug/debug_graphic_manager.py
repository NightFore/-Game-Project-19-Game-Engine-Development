# debug_graphic_manager.py

import pygame
from os import path

def debug(graphic_manager):
    pygame.init()

    # Set up the display
    display_width = 800
    display_height = 400
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Debug Graphic Manager")

    # Load the debug images using absolute file paths.
    # path.dirname(__file__) gets the directory of the current script,
    # and path.join combines it with the filenames to create absolute file paths.
    # Since absolute paths are provided, they ignore the GRAPHIC_FOLDER.
    images = {
        "single": {
            "type": "image",
            "filename": path.join(path.dirname(__file__), "debug_graphic_manager_single.png"),
        },
        "sequence": {
            "type": "image_sequence",
            "files": [
                {"filename": path.join(path.dirname(__file__), "debug_graphic_manager_sequence_1.png")},
                {"filename": path.join(path.dirname(__file__), "debug_graphic_manager_sequence_2.png")},
                # Add more frames as needed
            ],
            "frame_duration": 200,
        }
    }

    # Load the debug images into the graphic manager
    graphic_manager.load_resources(images)

    # Get graphic and animation instances
    single_graphic = graphic_manager.create_graphic_instance("single")
    sequence_animation = graphic_manager.create_graphic_instance("sequence")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with white color
        screen.fill((255, 255, 255))

        # Update and draw the single graphic
        single_graphic.update()
        single_graphic.draw(screen, (100, 100))

        # Update and draw the sequence animation
        dt = clock.tick(60)  # Get time passed in milliseconds since last frame
        sequence_animation.update(dt)  # Update animation based on time passed
        sequence_animation.draw(screen, (300, 100))  # Draw current frame of animation

        # Update the display
        pygame.display.flip()

    pygame.quit()
