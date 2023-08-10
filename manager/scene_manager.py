# scene_manager.py

import pygame
from button_manager import ButtonManager

DICT_BUTTONS = {
    "MainMenuScene": [
        {"name": "start", "position": (200, 150), "text": "Start"}
    ],
    "GameScene": [
        {"name": "game_over", "position": (200, 150), "text": "Game Over"},
        {"name": "click_me", "position": (200, 250), "text": "Click Me!"}
    ]
}

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

    def __init__(self, scene_manager):
        """
        Initialize the SceneBase.

        Args:
            scene_manager (SceneManager): The SceneManager instance.
        """
        self.scene_manager = scene_manager
        self.button_manager = None

    def set_button_manager(self, button_manager):
        """
        Set the button manager for the scene.

        Args:
            button_manager (ButtonManager): The button manager to set.
        """
        self.button_manager = button_manager

    def create_buttons_from_dict(self, scene_name):
        """
        Create buttons based on button information retrieved from the dictionary.

        Args:
            scene_name (str): The name of the scene to retrieve button information for.
        """
        # Retrieve button information from the dictionary based on the scene name
        button_infos = DICT_BUTTONS.get(scene_name, [])

        # Initialize an empty dictionary to store the created buttons
        self.buttons = {}

        # Iterate over each button information in the list
        for button_info in button_infos:
            # Extract information for the button from the dictionary
            name = button_info["name"]
            position = button_info["position"]
            text = button_info["text"]

            # Create a button using the ButtonManager and the extracted information
            button = self.button_manager.create_button(position, text)

            # Store the button in the buttons dictionary using its name as the key
            self.buttons[name] = button

    def enter(self):
        """
        Called when entering the scene.
        """
        self.create_buttons_from_dict(self.__class__.__name__)

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
    def __init__(self, scene_manager):
        super().__init__(scene_manager)

    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def update(self, dt):
        super().update(dt)

        # Check if the "start" button is clicked
        if self.buttons["start"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.buttons["start"].clicked = True
            else:
                if self.buttons["start"].clicked:
                    self.buttons["start"].clicked = False
                    self.scene_manager.set_scene("game")

    def draw(self, screen):
        super().draw(screen)

class GameScene(SceneBase):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)

    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def update(self, dt):
        super().update(dt)

        # Check if the "game_over" button is clicked
        if self.buttons["game_over"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.buttons["game_over"].clicked = True
            else:
                if self.buttons["game_over"].clicked:
                    self.buttons["game_over"].clicked = False
                    self.scene_manager.set_scene("main_menu")

        # Check if the "click_me" button is clicked
        if self.buttons["click_me"].rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.buttons["click_me"].clicked = True
            else:
                if self.buttons["click_me"].clicked:
                    self.buttons["click_me"].clicked = False
                    print("Hello World")

        # Reset button states
        for button in self.buttons.values():
            button.clicked = False

    def draw(self, screen):
        super().draw(screen)

# Debugging section
if __name__ == "__main__":
    from debug.debug_scene_manager import debug_scene_manager

    # Create an instance of SceneManager
    scene_manager = SceneManager()

    # Create instances of scenes
    main_menu_scene = MainMenuScene(scene_manager)
    game_scene = GameScene(scene_manager)

    # Debug the SceneManager by running the debug function
    debug_scene_manager(scene_manager, main_menu_scene, game_scene)
