# player.py

import pygame
from pygame.math import Vector2
from manager.template_manager import TemplateInstance
from classes.project1_projectile import Projectile


class Player(TemplateInstance):
    """
    Player class represents the player character.
    """

    def __init__(self, instance_data, managers):
        # Call the constructor of the parent class (TemplateInstance)
        super().__init__(instance_data, managers)

        # Load player-specific attributes from the data file
        character_data = instance_data.get("class_data", {}).get("characters", {}).get("player", {})
        self.health = character_data.get("health", 100)
        self.defense = character_data.get("defense", 5)
        self.velocity = Vector2(0, 0)
        self.magic = character_data.get("magic", 10)
        self.mana = character_data.get("mana", 100)
        self.acceleration = character_data.get("acceleration", 2.0)
        self.level = character_data.get("level", 1)
        self.experience = character_data.get("experience", 0)
        self.attacks = character_data.get("attacks", {"basic_attack": 10, "special_attack": 20})
        self.current_attack = None  # The current selected attack

        # Load available projectiles from the data file
        self.available_projectiles = character_data.get("projectiles", [])
        self.projectiles = {}  # Dictionary to store projectile instances

        # Load player's graphic from the GraphicManager
        graphic_name = character_data.get("graphic")
        if graphic_name:
            self.graphic = managers["graphic_manager"].get_graphic_instance(graphic_name)
        else:
            self.graphic = None

    def move(self, direction):
        """
        Move the player in the specified direction.

        Parameters:
            - direction (Vector2): The direction vector.
        """
        if self.graphic:
            self.accelerate(direction)
            self.velocity += self.acceleration * self.dt
            self.graphic.pos += self.velocity * self.dt

    def accelerate(self, direction):
        """
        Apply acceleration to the player in the specified direction.

        Parameters:
            - direction (Vector2): The direction vector.
        """
        self.velocity += direction

    def set_pos(self, pos):
        """
        Set the initial position of the player.

        Parameters:
            - pos (tuple): The initial position (x, y).
        """
        if self.graphic:
            self.graphic.pos = Vector2(pos)

    def add_group(self, all_sprites_group, characters_group):
        all_sprites_group.add(self)
        characters_group.add(self)

    def level_up(self):
        """
        Level up the player.
        """
        if self.experience >= 100:
            self.level += 1
            self.experience -= 100

    def get_pos(self):
        """
        Get the current position of the player.

        Returns:
            - Vector2: The current position.
        """
        if self.graphic:
            return Vector2(self.graphic.pos)

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
                projectile = Projectile(projectile_data, self.managers, self, direction, projectile_speed,
                                        projectile_damage)

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
            # Handle player defeat (optional)
            pass
