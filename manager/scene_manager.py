# scene_manager.py

import pygame
from button_manager import ButtonManager

class SceneManager:
    """
    SceneManager class manages the scenes and buttons of the game.
    """

    def __init__(self):
        """
        Initialize the SceneManager.
        """
        self.scenes = {}
        self.current_scene = None
        self.button_manager = ButtonManager()

    def add_scene(self, name, scene):
        """
        Add a scene to the manager.

        Args:
            name (str): The name of the scene.
            scene (SceneBase): The scene to add.
        """
        self.scenes[name] = scene
        scene.set_button_manager(self.button_manager)

    def set_scene(self, name):
        """
        Set the current scene.

        Args:
            name (str): The name of the scene to set.
        """
        if name in self.scenes:
            if self.current_scene:
                self.current_scene.exit()
                self.button_manager.clear_buttons()
            self.current_scene = self.scenes[name]
            self.current_scene.enter()

    def update(self, dt):
        """
        Update the current scene and buttons.

        Args:
            dt (float): Time since last update.
        """
        if self.current_scene:
            self.current_scene.update(dt)
            self.button_manager.update()

    def draw(self, screen):
        """
        Draw the current scene and buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.current_scene:
            self.current_scene.draw(screen)
            self.button_manager.draw(screen)

class SceneBase:
    """
    SceneBase class provides a base for scenes with buttons.
    """

    def __init__(self):
        """
        Initialize the SceneBase.
        """
        self.button_manager = None

    def set_button_manager(self, button_manager):
        """
        Set the button manager for the scene.

        Args:
            button_manager (ButtonManager): The button manager to set.
        """
        self.button_manager = button_manager

    def enter(self):
        """
        Called when entering the scene.
        """
        pass

    def exit(self):
        """
        Called when exiting the scene.
        """
        pass

    def update(self, dt):
        """
        Update the scene.

        Args:
            dt (float): Time since last update.
        """
        pass

    def draw(self, screen):
        """
        Draw the scene and its buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        pass

class MainMenuScene(SceneBase):
    """
    MainMenuScene class represents the main menu scene of the game.
    """

    def __init__(self, scene_manager):
        """
        Initialize the MainMenuScene.
        """
        super().__init__()
        self.scene_manager = scene_manager
        self.start_button = None

    def enter(self):
        """
        Called when entering the main menu scene.
        """
        super().enter()
        self.start_button = self.button_manager.create_button((200, 150), "Start")

    def exit(self):
        """
        Called when exiting the main menu scene.
        """
        pass

    def update(self, dt):
        """
        Update the main menu scene and its buttons.

        Args:
            dt (float): Time since last update.
        """
        super().update(dt)
        if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.start_button.clicked = True
            else:
                if self.start_button.clicked:
                    self.start_button.clicked = False
                    scene_manager.set_scene("game")

    def draw(self, screen):
        """
        Draw the main menu scene and its buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        super().draw(screen)

class GameScene(SceneBase):
    """
    GameScene class represents the game scene of the game.
    """

    def __init__(self, scene_manager):
        """
        Initialize the GameScene.
        """
        super().__init__()
        self.scene_manager = scene_manager
        self.game_over_button = None
        self.click_me_button = None

    def enter(self):
        """
        Called when entering the game scene.
        """
        super().enter()
        self.game_over_button = self.button_manager.create_button((200, 150), "Game Over")
        self.click_me_button = self.button_manager.create_button((200, 250), "Click Me!")
        self.game_over_button.clicked = False
        self.click_me_button.clicked = False

    def exit(self):
        """
        Called when exiting the game scene.
        """
        super().exit()

    def update(self, dt):
        """
        Update the game scene and its buttons.

        Args:
            dt (float): Time since last update.
        """
        super().update(dt)

        if self.game_over_button.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.game_over_button.clicked:
                self.game_over_button.clicked = True
            elif not pygame.mouse.get_pressed()[0] and self.game_over_button.clicked:
                self.game_over_button.clicked = False
                self.scene_manager.set_scene("main_menu")

        if self.click_me_button.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.click_me_button.clicked:
                self.click_me_button.clicked = True
            elif not pygame.mouse.get_pressed()[0] and self.click_me_button.clicked:
                self.click_me_button.clicked = False
                print("Hello World")

    def draw(self, screen):
        """
        Draw the game scene and its buttons on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        super().draw(screen)

# Debugging section
if __name__ == "__main__":
    from debug.debug_scene_manager import debug_scene_manager

    # Initialize Pygame
    pygame.init()

    # Create an instance of SceneManager
    scene_manager = SceneManager()

    # Create instances of scenes
    main_menu_scene = MainMenuScene(scene_manager)
    game_scene = GameScene(scene_manager)

    # Debug the SceneManager by running the debug function
    debug_scene_manager(scene_manager, main_menu_scene, game_scene)

    pygame.quit()
