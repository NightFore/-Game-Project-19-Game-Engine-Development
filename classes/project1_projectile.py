# projectile.py

import pygame
from pygame.math import Vector2
from manager.template_manager import TemplateInstance

class Projectile(TemplateInstance):
    """
    Projectile class represents a projectile fired by a character.
    """
    def __init__(self, instance_data, managers, owner, direction, speed, damage):
        # Call the constructor of the parent class (TemplateInstance)
        super().__init__(instance_data, managers)

        # Load projectile attributes from the data file
        projectile_data = instance_data.get("class_data", {}).get("projectiles", {}).get(instance_data.get("name", ""), {})
        self.owner = owner
        self.direction = direction.normalize() if direction.length() != 0 else Vector2(1, 0)
        self.speed = projectile_data.get("speed", speed)
        self.damage = projectile_data.get("damage", damage)

        # Load projectile's graphic from the GraphicManager
        graphic_name = projectile_data.get("graphic")
        if graphic_name:
            self.graphic = managers["graphic_manager"].get_graphic_instance(graphic_name)
        else:
            self.graphic = None

    def update(self):
        """
        Update the projectile's position.
        """
        self.graphic.pos += self.direction * self.speed * self.dt

    def check_collision(self, target):
        """
        Check if the projectile collides with a target.

        Parameters:
            - target (TemplateInstance): The target instance.

        Returns:
            - bool: True if a collision occurs, False otherwise.
        """
        return self.graphic.rect.colliderect(target.graphic.rect)

    def set_pos(self, pos):
        """
        Set the initial position of the projectile.

        Parameters:
            - pos (tuple): The initial position (x, y).
        """
        if self.graphic:
            self.graphic.pos = Vector2(pos)

    def get_pos(self):
        """
        Get the current position of the projectile.

        Returns:
            - Vector2: The current position.
        """
        if self.graphic:
            return Vector2(self.graphic.pos)
