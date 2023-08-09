# debug_scene_manager.py

import pygame

def debug_scene_manager(scene_manager, main_menu_scene, game_scene):
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    scene_manager.add_scene("main_menu", main_menu_scene)
    scene_manager.add_scene("game", game_scene)

    scene_manager.set_scene("main_menu")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        scene_manager.update(1.0)
        screen.fill((0, 0, 0))
        scene_manager.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
