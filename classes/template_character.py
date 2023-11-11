# template_character.py

import pygame
from pygame.math import Vector2
from manager.template_manager import TemplateInstance
from classes.project1_projectile import Projectile

class TemplateCharacter(TemplateInstance, pygame.sprite.Sprite):
    """
    TemplateCharacter class represents a generic character template.

    Attributes:
        Character Attributes:
            - health (int): The health points of the character.
            - defense (int): The defense points of the character.
            - magic (int): The magic points of the character.
            - mana (int): The mana points of the character.

        Movement Attributes:
            - velocity (Vector2): The velocity vector of the character.
            - acceleration (float): The acceleration magnitude of the character.

        Leveling and Experience Attributes:
            - level (int): The level of the character.
            - experience (int): The experience points of the character.
            - experience_thresholds (list): The thresholds for leveling up.

        Attack Attributes:
            - attacks (dict): The dictionary of available attacks with corresponding damage values.
            - current_attack (str): The currently selected attack.

        Projectile Attributes:
            - available_projectiles (list): The list of available projectiles for the character.
            - projectiles (dict): The dictionary to store projectile instances.

        Graphic Attributes:
            - graphic (GraphicInstance): The graphic instance associated with the character.

    Methods:
        Movement:
            - move_to_position(position): Move the character to the specified position.
            - move_to_tile(tile_index): Move the character to the specified tile index.
            - accelerate(direction): Apply acceleration to the character in the specified direction.

        Initialization:
            - set_initial_position(pos): Set the initial position of the character.
            - add_to_groups(all_sprites_group, characters_group): Add the character to sprite groups.

        Leveling and Experience:
            - level_up(): Level up the character.
            - get_experience_value(): Get the experience value gained by defeating this character.
            - gain_experience(experience_amount): Gain experience points.

        Event Handling:
            - handle_events(): Handle generic events for the character.

        Graphic Configuration:
            - configure_graphic(graphic_data): Configure the graphic appearance of the character.

        Miscellaneous:
            - get_position(): Get the current position of the character.

        Input Handling:
            - handle_keyboard_input(): Handle keyboard input for movement and attack.

        Combat:
            - attack(attack_name): Perform an attack based on the specified attack.
            - receive_damage(damage): Receive damage and update health.
    """
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)

        # Character Attributes
        character_data = instance_data.get("class_data", {}).get("characters", {}).get("template_character", {})
        self.health = character_data.get("health", 100)
        self.defense = character_data.get("defense", 5)
        self.magic = character_data.get("magic", 10)
        self.mana = character_data.get("mana", 100)

        # Movement Attributes
        self.velocity = Vector2(0, 0)
        self.acceleration = character_data.get("acceleration", 2.0)

        # Leveling and Experience Attributes
        self.level = character_data.get("level", 1)
        self.experience = character_data.get("experience", 0)
        self.experience_thresholds = character_data.get("experience_thresholds", [100, 200, 300])

        # Attack Attributes
        self.attacks = character_data.get("attacks", {"basic_attack": 10, "special_attack": 20})
        self.current_attack = None  # The current selected attack

        # Projectile Attributes
        self.available_projectiles = character_data.get("projectiles", [])
        self.projectiles = {}  # Dictionary to store projectile instances

        # Graphic Attributes
        graphic_name = character_data.get("graphic")
        if graphic_name:
            self.graphic = managers["graphic_manager"].get_graphic_instance(graphic_name)
        else:
            self.graphic = None



    """
    Movement:
        - move_to_position
        - move_to_tile
        - accelerate
    """
    def move_to_position(self, position):
        """
        Move the character to the specified position.

        Parameters:
            - position (Vector2): The target position.
        """
        if self.graphic:
            self.accelerate(position - self.graphic.pos)
            self.velocity += self.acceleration * self.dt
            self.graphic.pos += self.velocity * self.dt

    def move_to_tile(self, tile_index):
        """
        Move the character to the specified tile index.

        Parameters:
            - tile_index (Vector2 or tuple): The target tile index.
        """
        # Implement logic for moving to a tile index
        pass

    def accelerate(self, direction):
        """
        Apply acceleration to the character in the specified direction.

        Parameters:
            - direction (Vector2): The direction vector.
        """
        self.velocity += direction



    """
    Initialization:
        - set_initial_position
        - add_to_groups
    """
    def set_initial_position(self, pos):
        """
        Set the initial position of the character.

        Parameters:
            - pos (tuple): The initial position (x, y).
        """
        if self.graphic:
            self.graphic.pos = Vector2(pos)

    def add_to_groups(self, all_sprites_group, characters_group):
        all_sprites_group.add(self)
        characters_group.add(self)



    """
    Leveling and Experience:
        - level_up
        - get_experience_value
        - gain_experience
    """
    def level_up(self):
        """
        Level up the character.
        """
        if self.experience >= self.experience_thresholds[self.level - 1]:
            self.level += 1
            self.experience -= self.experience_thresholds[self.level - 2]

    def get_experience_value(self):
        """
        Get the experience value gained by defeating this character.

        Returns:
            - int: The experience value.
        """
        return sum(self.experience_thresholds)

    def gain_experience(self, experience_amount):
        """
        Gain experience points.

        Parameters:
            - experience_amount (int): The amount of experience points gained.
        """
        self.experience += experience_amount
        self.level_up()



    """
    Event Handling:
        - handle_events
    """
    def handle_events(self):
        """
        Handle generic events for the character.
        """
        # Implement event handling logic



    """
    Graphic Configuration:
        - configure_graphic
    """
    def configure_graphic(self, graphic_data):
        """
        Configure the graphic appearance of the character.

        Parameters:
            - graphic_data (dict): Data for configuring the character's graphic.
        """
        # Implement graphic configuration logic



    """
    Miscellaneous:
        - get_position
    """
    def get_position(self):
        """
        Get the current position of the character.

        Returns:
            - Vector2: The current position.
        """
        if self.graphic:
            return Vector2(self.graphic.pos)



    """
    Input Handling:
        - handle_keyboard_input
    """
    def handle_keyboard_input(self):
        """
        Handle keyboard input for movement and attack.
        """
        events = self.managers["main_manager"].events

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.accelerate(Vector2(-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.accelerate(Vector2(1, 0))
                elif event.key == pygame.K_UP:
                    self.accelerate(Vector2(0, -1))
                elif event.key == pygame.K_DOWN:
                    self.accelerate(Vector2(0, 1))
                elif event.key == pygame.K_1:
                    self.attack("basic_attack")
                elif event.key == pygame.K_2:
                    self.attack("special_attack")



    """
    Combat:
        - attack
        - receive_damage
    """
    def attack(self, attack_name):
        """
        Perform an attack based on the specified attack.

        Parameters:
            - attack_name (str): The name of the attack.
        """
        if self.current_attack is not None:
            direction = Vector2(1, 0)  # Default direction (right)
            projectile_speed = 10  # Adjust as needed
            projectile_damage = self.attacks.get(attack_name, 0)

            # Retrieve projectile data from available projectiles
            projectile_data = next((proj for proj in self.available_projectiles if proj["name"] == attack_name), None)

            if projectile_data:
                # Create a new Projectile instance
                projectile = Projectile(projectile_data, self.managers, self, direction, projectile_speed, projectile_damage)

                # Add the projectile to the game manager's list of instances
                self.managers["main_manager"].instances.append(projectile)

    def receive_damage(self, damage):
        """
        Receive damage and update health.

        Parameters:
            - damage (int): The amount of damage received.
        """
        self.health -= max(0, damage - self.defense)
        if self.health <= 0:
            self.kill()
