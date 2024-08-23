# ui_element.py

import pygame
from utils import setup_managers

DEFAULT_CONFIG = {
    'pos_x': 0,
    'pos_y': 0,
    'shadow_enabled': True,
    'shadow_color': (255, 255, 255),
    'shadow_offset': (5, 5),
    'shadow_blur': 150,
    'text_color': (255, 255, 255),
    'text_align': 'center',
    'font_size': 36,
    'hover_color': (255, 0, 0),
    'outline_enabled': True,
    'outline_color': (0, 255, 255),
    'outline_border': 1,
    'collision_enabled': True,
    'collision_color': (255, 0, 0),
    'collision_border': 1,
}


class UIElement:
    def __init__(self, element_type, element_id, config, managers, logger):
        # Core Attributes
        self.element_type = element_type
        self.element_id = element_id
        self.config = {**DEFAULT_CONFIG, **config}
        self.managers = managers
        self.logger = logger

        # Set up references to managers
        setup_managers(self, managers)

        # Position Attributes
        self.pos_x = self.config.get('position_x')
        self.pos_y = self.config.get('position_y')

        # Rect Attributes
        self.rect_width = self.config.get('rect_width')
        self.rect_height = self.config.get('rect_height')
        self.rect_color = self.config.get('rect_color')
        self.rect_surface = None
        self.rect = None

        # Image Attributes
        self.image_path = self.config.get('image_path')
        self.image_width = self.config.get('image_width')
        self.image_height = self.config.get('image_height')
        self.image = None
        self.image_surface = None
        self.image_rect = None

        # Shadow Attributes
        self.shadow_enabled = self.config.get('shadow_enabled')
        self.shadow_color = self.config.get('shadow_color')
        self.shadow_offset = self.config.get('shadow_offset')
        self.shadow_blur = self.config.get('shadow_blur')
        self.shadow_surface = None

        # Text Attributes
        self.text_label = self.config.get('text_label')
        self.text_color = self.config.get('text_color')
        self.text_align = self.config.get('text_align')
        self.text_surface = None
        self.text_rect = None

        # Font Attributes
        self.font_name = self.config.get('font_name')
        self.font_size = self.config.get('font_size')
        self.font = None

        # Outline Attributes
        self.outline_enabled = self.config.get('outline_enabled')
        self.outline_color = self.config.get('outline_color')
        self.outline_border = self.config.get('outline_border')
        self.outline_surface = None
        self.outline_rect = None

        # Collision Attributes
        self.collision_enabled = self.config.get('collision_enabled')
        self.collision_width = self.config.get('collision_width')
        self.collision_height = self.config.get('collision_height')
        self.collision_color = self.config.get('collision_color')
        self.collision_border = self.config.get('collision_border')
        self.collision_surface = None
        self.collision_rect = None

        # Hover Attributes
        self.hover_color = self.config.get('hover_color')
        self.hovered_state = False

        # Initialize Graphical Properties
        self.final_surface = None
        self.final_rect = None

        # Visibility Attributes
        # Layout Attributes
        # Scroll Attributes
        # Tooltip Attributes
        # Hierarchy Attributes

        # Set up the graphical elements
        self.setup_graphics()

    def setup_graphics(self):
        """Initialize and set up all graphical components."""
        self.setup_rect()
        self.setup_image()
        self.setup_text()
        self.setup_shadow()
        self.update_final_surface()

    def setup_rect(self):
        """
        Create and set up the surface for the rectangle.
        """
        if self.rect_width and self.rect_height:
            self.rect_surface = pygame.Surface((self.rect_width, self.rect_height))
            self.rect_surface.fill(self.rect_color)
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)

    def setup_image(self):
        """
        Load and set up the image for the UI element.
        """
        if self.image_path:
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image_surface = self.image.copy()

            if self.image_width and self.image_height:
                self.image_surface = pygame.transform.scale(self.image_surface, (self.image_width, self.image_height))
                self.image_rect = pygame.Rect(self.pos_x, self.pos_y, self.image_width, self.image_height)
            else:
                self.image_rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
                self.image_width, self.image_height = self.image_rect.size

    def setup_shadow(self):
        """
        Create and set up the shadow surface.
        """
        if self.shadow_enabled:
            # Calculate the dimensions of the shadow surface to include the shadow offset
            shadow_width = self.rect_width + abs(self.shadow_offset[0])
            shadow_height = self.rect_height + abs(self.shadow_offset[1])
            self.shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)

            # Create a smaller surface for the shadow itself
            shadow = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
            shadow.fill(self.shadow_color)
            shadow.set_alpha(self.shadow_blur)

            # Calculate the offset position for the shadow
            offset_x = max(0, self.shadow_offset[0])
            offset_y = max(0, self.shadow_offset[1])

            # Blit the shadow onto the shadow surface at the calculated offset
            self.shadow_surface.blit(shadow, (offset_x, offset_y))

    def setup_text(self):
        """
        Set up the text for the UI element, including font and alignment.
        """
        if self.text_label:
            self.font = pygame.font.Font(self.font_name, self.font_size)
            self.text_surface = self.font.render(self.text_label, True, self.text_color)
            self.text_rect = self.text_surface.get_rect()

    def update_final_surface(self):
        """Update the final surface size based on all graphical components."""
        width, height = self.rect_width, self.rect_height
        if self.shadow_enabled:
            width += self.shadow_offset[0]
            height += self.shadow_offset[1]
        self.final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.final_rect = self.final_surface.get_rect()

    def update_outline(self):
        """Create and set up the surface for the outline."""
        if self.outline_enabled:
            # Create the outline rect and surface
            self.outline_rect = self.final_rect.copy()
            self.outline_surface = pygame.Surface(self.outline_rect.size, pygame.SRCALPHA)

            # Draw the outline border
            pygame.draw.rect(self.outline_surface, self.outline_color,
                             self.outline_surface.get_rect(), self.outline_border)

    def update_collision(self):
        """
        Create and set up the collision surface based on various fallback sizes:
        - Config-defined size
        - Rect size
        - Image size
        - Final surface size
        """
        if self.collision_enabled:
            # Determine the collision rect based on available attributes
            if self.collision_width and self.collision_height:
                collision_rect = pygame.Rect(self.pos_x, self.pos_y, self.collision_width, self.collision_height)
            elif self.rect:
                collision_rect = self.rect.copy()
            elif self.image_rect:
                collision_rect = self.image_rect.copy()
            else:
                collision_rect = self.final_rect.copy()

            # Create the collision surface and set its rect
            self.collision_surface = pygame.Surface(collision_rect.size, pygame.SRCALPHA)
            self.collision_rect = collision_rect

            # Draw the collision border on the collision surface
            pygame.draw.rect(self.collision_surface, self.collision_color,
                             self.collision_surface.get_rect(), self.collision_border)

    def update_hover(self, mouse_pos):
        """
        Updates the hover state of the UI element based on mouse position.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse cursor.
        """
        self.hovered_state = self.collision_rect.collidepoint(mouse_pos)
        if self.hovered_state and self.hover_color:
            self.rect_surface.fill(self.hover_color)
        elif self.rect_color:
            self.rect_surface.fill(self.rect_color)

    def update(self, mouse_pos, mouse_clicks):
        self.update_final_surface()
        self.update_outline()
        self.update_collision()
        self.update_hover(mouse_pos)

    def draw(self, surface):
        # Clear the final surface before blit
        self.final_surface.fill((0, 0, 0, 0))

        # Draw the elements
        if self.shadow_surface:
            self.final_surface.blit(self.shadow_surface, (0, 0))
        if self.rect_surface:
            self.final_surface.blit(self.rect_surface, (0, 0))
        if self.image_surface:
            self.final_surface.blit(self.image_surface, (0, 0))
        if self.text_surface:
            self.final_surface.blit(self.text_surface, (0, 0))
        if self.outline_surface:
            self.final_surface.blit(self.outline_surface, (0, 0))
        if self.collision_surface:
            self.final_surface.blit(self.collision_surface, (0, 0))

        # Blit final surface to the main screen
        surface.blit(self.final_surface, (self.pos_x, self.pos_y))
