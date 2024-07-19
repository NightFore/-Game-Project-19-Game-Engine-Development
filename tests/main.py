# main.py

import pygame
from ui_manager import UIManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("UI Manager Example")
    clock = pygame.time.Clock()

    ui_manager = UIManager()
    ui_manager.load_main_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui_manager.handle_events(event)

        screen.fill((30, 30, 30))  # Clear screen with a dark color
        ui_manager.draw_ui(screen)  # Draw UI elements on the screen

        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
