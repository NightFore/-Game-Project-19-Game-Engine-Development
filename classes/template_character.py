# template_character.py

import pygame
from pygame.math import Vector2 as vec

from manager.template_manager import TemplateInstance
from classes.project1_projectile import Projectile


class TemplateCharacter(TemplateInstance, pygame.sprite.Sprite):
    """
    TemplateCharacter class represents a generic character template.

    Attributes:
        Specific to TemplateCharacter:
            Character Attributes:
                - Health (int): The health points of the character.
                - Defense (int): The defense points of the character.
                - Magic (int): The magic points of the character.
                - Mana (int): The mana points of the character.

            Movement Attributes:
                - Velocity (vec): The current velocity of the character.
                - Max_movement_velocity (vec): The maximum movement velocity of the character.
                - Acceleration (vec): The acceleration vector for the character's movement.

            Direction Vectors:
                - Directions (dict): Dictionary mapping movement directions to vector values.

            Leveling and Experience Attributes:
                - Level (int): The level of the character.
                - Experience (int): The current experience points of the character.
                - Experience_thresholds (list): List of experience thresholds required for each level.

            Attack Attributes:
                - Attacks (dict): Dictionary of available attacks and their damage values.
                - Current_attack: The currently selected attack.

            Projectile Attributes:
                - Available_projectiles (list): List of available projectile types.
                - Projectiles (dict): Dictionary to store projectile instances.

            Graphic Attributes:
                - Graphic: The graphic instance associated with the character.

            Index Position Management:
                - Use_index_position (bool): Determines if using (x, y) or index positions.

        Inherited Attributes from TemplateInstance:
            - dt: The time difference between frames.

    Methods:
        Setup:
            - add_to_group(group): Add the character to the specified group.

        Graphic:
            - set_graphic(graphic_instance): Set the graphic instance for the character.
            - set_pos(pos): Set the position of the character.
            - set_size(size): Set the size of the character.
            - get_pos(): Get the current position of the character.

        Movement:
            - move_to_pos(position): Move the character to the specified position.
            - move_to_tile(tile_index): Move the character to the specified tile index.
            - move_position_increment(increment): Move the character's position by the specified increment.
            - move_tile_increment(increment): Move the character to the next tile position by the specified increment.
            - update_position(): Update the position based on the current velocity.
            - update_velocity(): Update the velocity based on acceleration.
            - set_movement_acceleration(acceleration): Set the movement acceleration of the character.
            - tile_index_to_position(tile_index): Convert tile index to (x, y) position.

        Experience:
            - level_up(): Level up the character.
            - stats_upgrade(): Upgrade the character's stats based on the new level.
            - gain_experience(experience_amount): Gain experience points.

        Combat:
            - use_attack(attack_name): Use the specified attack.
            - receive_damage(damage): Receive damage and update health.
            - get_projectile_data(attack_name): Retrieve projectile data for a given attack.

        Event Handling:
            - handle_events(): Handle generic events for the character.

        Input Handling:
            - configure_keys(keys): Configure the keys for movement and attack.
            - set_movement_key(direction, key): Set the key for a specific movement direction.
            - set_attack_key(attack_name, key): Set the key for a specific attack.
            - handle_keyboard_input(): Handle keyboard input for movement and attack.
    """
    def __init__(self, instance_data, managers):
        super().__init__(instance_data, managers)
        # Character Attributes
        character_data = instance_data.get("class_data", {}).get("characters", {}).get("template_character", {})
        self.health = character_data.get("health", 100)
        self.defense = character_data.get("defense", 5)
        self.magic = character_data.get("magic", 10)
        self.mana = character_data.get("mana", 100)

        # Direction vectors
        self.directions = {
            "left": vec(-1, 0),
            "right": vec(1, 0),
            "up": vec(0, -1),
            "down": vec(0, 1)
        }

        # Movement Attributes
        self.velocity = vec(0, 0)
        self.max_movement_velocity = vec(*character_data.get("max_movement_velocity", (5.0, 5.0)))
        self.acceleration = vec(*character_data.get("acceleration", (2.0, 2.0)))

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

        # Index Position Management
        self.use_index_position = character_data.get("use_index_position", False)  # Determines if using (x, y) or index positions.

        # Configure keys during initialization
        self.configure_keys(instance_data.get("class_data", {}).get("characters", {}).get("keys", {}))

    """
    Setup:
        - add_to_group
    """
    def add_to_group(self, group):
        """
        Add the character to the specified group.

        Parameters:
            - group: The sprite group to add the character to.
        """
        group.add(self)

    """
    Graphic:
        - set_graphic
        - set_pos
        - set_size
        - get_pos
    """
    def set_graphic(self, graphic_instance):
        """
        Set the graphic instance for the character.

        Parameters:
            - graphic_instance: The graphic instance to associate with the character.
        """
        self.graphic = graphic_instance

    def set_pos(self, pos):
        """
        Set the position of the character.

        Parameters:
            - pos: The new position (vec).
        """
        if self.graphic:
            self.graphic.pos = pos

    def set_size(self, size):
        """
        Set the size of the character.

        Parameters:
            - size: The new size.
        """
        if self.graphic:
            self.graphic.size = size

    def get_pos(self):
        """
        Get the current position of the character.

        Returns:
            - vec: The current position.
        """
        if self.graphic:
            return self.graphic.pos

    """
    Movement:
        - move_to_pos
        - move_to_tile
        - move_position_increment
        - move_tile_increment
        - update_position
        - update_velocity
    """

    def move_to_pos(self, position):
        """
        Move the character to the specified position.

        Parameters:
            - position (vec or tuple): The target position. Either (x, y) or tile index.
        """
        if self.graphic:
            if self.use_index_position:
                # Convert tile index to (x, y) position
                position = self.tile_index_to_position(position)

            self.movement_acceleration = position - self.graphic.pos
            self.velocity += self.movement_acceleration * self.dt
            self.graphic.pos += self.velocity * self.dt

    def tile_index_to_position(self, tile_index):
        """
        Convert tile index to (x, y) position.

        Parameters:
            - tile_index (vec or tuple): The tile index.

        Returns:
            - vec: The corresponding (x, y) position.
        """
        # Implement logic to convert tile index to (x, y) position
        pass

    def move_to_tile(self, tile_index):
        """
        Move the character to the specified tile index.

        Parameters:
            - tile_index (vec or tuple): The target tile index.
        """
        # Implement logic for moving to a tile index
        pass

    def move_position_increment(self, increment):
        """
        Move the character's position by the specified increment.

        Parameters:
            - increment (vec): The increment for the position.
        """
        if self.graphic:
            self.graphic.pos += increment

    def move_tile_increment(self, increment):
        """
        Move the character to the next tile position by the specified increment.

        Parameters:
            - increment (vec): The increment for the tile position.
        """
        # Implement logic for moving to the next tile position
        pass

    def set_movement_acceleration(self, acceleration):
        """
        Set the movement acceleration of the character.

        Parameters:
            - acceleration (vec): The movement acceleration vector.
        """
        self.movement_acceleration = acceleration

    def update_position(self):
        """
        Update the position based on the current velocity.
        """
        if self.graphic:
            self.graphic.pos += self.velocity * self.dt

    def update_velocity(self):
        """
        Update the velocity based on acceleration.
        """
        # Update velocity based on acceleration
        self.velocity += self.acceleration * self.dt

        # Limit velocity to max_movement_velocity
        self.velocity.x = min(self.velocity.x, self.max_movement_velocity.x)
        self.velocity.y = min(self.velocity.y, self.max_movement_velocity.y)

    """
    Experience:
        - level_up
        - stats_upgrade
        - gain_experience
    """
    def level_up(self):
        """
        Level up the character.
        """
        if self.experience >= self.experience_thresholds[self.level - 1]:
            self.level += 1
            self.experience -= self.experience_thresholds[self.level - 2]
            self.stats_upgrade()

    def stats_upgrade(self):
        """
        Upgrade the character's stats based on the new level.
        """
        # Implement logic for upgrading stats
        pass

    def gain_experience(self, experience_amount):
        """
        Gain experience points.

        Parameters:
            - experience_amount (int): The amount of experience points gained.
        """
        self.experience += experience_amount
        self.level_up()

    """
    Combat:
        - use_attack
        - receive_damage
    """

    def use_attack(self, attack_name):
        """
        Use the specified attack.

        Parameters:
            - attack_name (str): The name of the attack.
        """
        if self.current_attack is not None:
            direction = vec(1, 0)  # Default direction (right)
            projectile_speed = 10  # Adjust as needed
            projectile_damage = self.attacks.get(attack_name, 0)

            # Retrieve projectile data from available projectiles
            projectile_data = self.get_projectile_data(attack_name)

            if projectile_data:
                # Create a new Projectile instance
                projectile = Projectile(projectile_data, self.managers, self, direction, projectile_speed,
                                        projectile_damage)

                # Add the projectile to the game manager's list of instances
                self.managers["main_manager"].instances.append(projectile)

    def get_projectile_data(self, attack_name):
        """
        Retrieve projectile data for a given attack.

        Parameters:
            - attack_name (str): The name of the attack.

        Returns:
            - dict: Projectile data.
        """
        return next((proj for proj in self.available_projectiles if proj["name"] == attack_name), None)

    def receive_damage(self, damage):
        """
        Receive damage and update health.

        Parameters:
            - damage (int): The amount of damage received.
        """
        self.health -= max(0, damage - self.defense)
        if self.health <= 0:
            self.kill()

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
    Input Handling:
        - handle_keyboard_input
    """
    def configure_keys(self, keys):
        """
        Configure the keys for movement and attack.

        Parameters:
            - keys (dict): A dictionary containing key configurations.
        """
        self.movement_keys = keys.get("movement", {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN})
        self.attack_keys = keys.get("attacks", {"basic_attack": pygame.K_1, "special_attack": pygame.K_2})

    def set_movement_key(self, direction, key):
        """
        Set the key for a specific movement direction.

        Parameters:
            - direction (str): The movement direction (e.g., "left", "right", "up", "down").
            - key: The pygame key constant.
        """
        self.movement_keys[direction] = key

    def set_attack_key(self, attack_name, key):
        """
        Set the key for a specific attack.

        Parameters:
            - attack_name (str): The name of the attack.
            - key: The pygame key constant.
        """
        self.attack_keys[attack_name] = key

    def handle_keyboard_input(self):
        """
        Handle keyboard input for movement and attack.
        """
        events = self.managers["main_manager"].events

        for event in events:
            if event.type == pygame.KEYDOWN:
                for direction, key in self.movement_keys.items():
                    if event.key == key:
                        self.set_movement_acceleration(self.movement_acceleration * self.directions[direction])

                for attack, key in self.attack_keys.items():
                    if event.key == key:
                        self.use_attack(attack)

            elif event.type == pygame.KEYUP:
                for direction, key in self.movement_keys.items():
                    if event.key == key:
                        self.set_movement_acceleration(vec(0, 0))
