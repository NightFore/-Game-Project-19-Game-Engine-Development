# test.py

import pygame
from logger import setup_logger, log_event
from config import load_config


def main():
    # Setup logger
    logger = setup_logger()

    # Log the start of the game instance
    logger.info("Game instance started")

    # Initialize Pygame
    pygame.init()

    # Load configuration
    config = load_config()
    window_config = config['window']

    # Load window configuration
    width = window_config['width']
    height = window_config['height']
    title = window_config['title']

    # Setup window
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    logger.info(f"Created window: {title}")

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw elements
        pygame.draw.circle(screen, (255, 0, 0), (400, 300), 30)
        log_event(logger, "Created red circle at (400, 300)")

        # Update display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

    # Log the termination of the game engine
    logger.info("Game engine terminated")


if __name__ == "__main__":
    main()
