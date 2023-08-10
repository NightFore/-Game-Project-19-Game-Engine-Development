# debug_scene_manager.py

import pygame

def debug_scene_manager(scene_manager, main_menu_scene, game_scene):
    # Initialize Pygame
    pygame.init()

    # Set up the screen and clock
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Add scenes to the SceneManager
    scene_manager.add_scene("main_menu", main_menu_scene)
    scene_manager.add_scene("game", game_scene)

    # Set the initial scene
    scene_manager.set_scene("main_menu")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the current scene
        scene_manager.update(1.0)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the current scene
        scene_manager.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Clean up and quit Pygame
    pygame.quit()
