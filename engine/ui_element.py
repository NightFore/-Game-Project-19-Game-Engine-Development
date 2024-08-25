# ui_element.py

import pygame
from utils import setup_managers

DEFAULT_CONFIG = {
    'pos_x': 0,
    'pos_y': 0,
    'align': 'center',
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
    'active': True,
    'visible': True,
    'layer': 0,
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
        self.pos_x = self.config.get('pos_x')
        self.pos_y = self.config.get('pos_y')
        self.align = self.config.get('align')

        # Rect Attributes
        self.rect_width = self.config.get('rect_width')
        self.rect_height = self.config.get('rect_height')
        self.rect_color = self.config.get('rect_color')
        self.rect = None
        self.rect_surface = None

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
        self.shadow_rect = None

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
        self.outline_rect = None
        self.outline_surface = None

        # Collision Attributes
        self.collision_enabled = self.config.get('collision_enabled')
        self.collision_width = self.config.get('collision_width')
        self.collision_height = self.config.get('collision_height')
        self.collision_color = self.config.get('collision_color')
        self.collision_border = self.config.get('collision_border')
        self.collision_rect = None
        self.collision_surface = None

        # Hover Attributes
        self.hover_color = self.config.get('hover_color')
        self.hovered_state = False

        # State Attributes
        self.active = self.config.get('active')
        self.visible = self.config.get('visible')
        self.layer = self.config.get('layer')

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

    def setup_rect(self):
        """
        Create and set up the surface for the rectangle.
        """
        if self.rect_width and self.rect_height:
            # Create the rect surface
            self.rect_surface = pygame.Surface((self.rect_width, self.rect_height))
            self.rect_surface.fill(self.rect_color)

            # Create the rect
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)

            # Align the object
            self.align_rect(self.rect, self.align, (self.pos_x, self.pos_y))

    def setup_image(self):
        """
        Load and set up the image for the UI element.
        """
        if self.image_path:
            # Load the image surface with alpha transparency
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image_surface = self.image.copy()

            # Check if specific dimensions for the image are provided
            if self.image_width and self.image_height:
                # Resize the image to the specified dimensions
                self.image_surface = pygame.transform.scale(self.image_surface, (self.image_width, self.image_height))
            else:
                # If dimensions are not specified, get the original size of the image
                self.image_width, self.image_height = self.image_surface.get_size()

            # Create the image rect
            self.image_rect = self.image_surface.get_rect()

            # Align the object
            self.align_rect(self.image_rect, self.align, (self.pos_x, self.pos_y))

    def setup_shadow(self):
        """
        Create and set up the shadow surface.
        """
        if self.shadow_enabled:
            # Create the shadow surface
            self.shadow_surface = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
            self.shadow_surface.fill(self.shadow_color)
            self.shadow_surface.set_alpha(self.shadow_blur)

            # Create the shadow rect
            self.shadow_rect = pygame.Rect(
                self.rect.x + self.shadow_offset[0],
                self.rect.y + self.shadow_offset[1],
                self.rect_width,
                self.rect_height
            )

    def setup_text(self):
        """
        Set up the text for the UI element, including font and alignment.
        """
        if self.text_label:
            # Load the font with the specified name and size
            self.font = pygame.font.Font(self.font_name, self.font_size)

            # Create the text surface with the specified color
            self.text_surface = self.font.render(self.text_label, True, self.text_color)

            # Create the text rect based on the rendered surface
            self.text_rect = self.text_surface.get_rect()

            # Align the text rect based on the alignment configuration and position
            self.align_rect(self.text_rect, self.text_align, (self.pos_x, self.pos_y))

    def align_rect(self, rect, align, position):
        if align == 'center':
            rect.center = position
        elif align == 'nw':
            rect.topleft = position
        elif align == 'n':
            rect.midtop = position
        elif align == 'ne':
            rect.topright = position
        elif align == 'e':
            rect.midright = position
        elif align == 'se':
            rect.bottomright = position
        elif align == 's':
            rect.midbottom = position
        elif align == 'sw':
            rect.bottomleft = position
        elif align == 'w':
            rect.midleft = position
        else:
            self.logger.log_warning(
                f"Unsupported alignment value '{align}' provided.")

    def update_outline(self):
        """Create and set up the surface for the outline, considering all defined rectangles."""
        if self.outline_enabled:
            # Initialize a list for all defined rectangles
            rects = [self.rect, self.shadow_rect, self.image_rect]

            # Remove None values from the list
            rects = [r for r in rects if r]

            # Calculate the min and max coordinates to encapsulate all rectangles
            min_x = min(r.x for r in rects)
            min_y = min(r.y for r in rects)
            max_x = max(r.right for r in rects)
            max_y = max(r.bottom for r in rects)

            # Define the outline rect based on the min and max coordinates
            self.outline_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

            # Create the surface for the outline
            self.outline_surface = pygame.Surface(self.outline_rect.size, pygame.SRCALPHA)

            # Draw the outline border on the outline surface
            pygame.draw.rect(self.outline_surface, self.outline_color,
                             self.outline_surface.get_rect(), self.outline_border)

    def update_collision(self):
        """
        Create and set up the collision surface based on available sizes:
        - Config-defined size
        - Rect size
        - Image size
        """
        if self.collision_enabled:
            # Create the collision rect
            if self.collision_width and self.collision_height:
                self.collision_rect = pygame.Rect(self.pos_x, self.pos_y, self.collision_width, self.collision_height)
            elif self.rect:
                self.collision_rect = self.rect.copy()
            elif self.image_rect:
                self.collision_rect = self.image_rect.copy()
            else:
                self.collision_rect = pygame.Rect(self.pos_x, self.pos_y, 0, 0)

            # Create the collision surface
            self.collision_surface = pygame.Surface(self.collision_rect.size, pygame.SRCALPHA)

            # Draw the collision border on the collision surface
            pygame.draw.rect(self.collision_surface, self.collision_color,
                             self.collision_surface.get_rect(), self.collision_border)

    def update_hover(self, mouse_pos):
        """
        Updates the hover state of the UI element based on mouse position.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse cursor.
        """
        self.hovered_state = self.rect.collidepoint(mouse_pos)
        if self.rect_surface and self.hover_color:
            if self.hovered_state:
                self.rect_surface.fill(self.hover_color)
            else:
                self.rect_surface.fill(self.rect_color)

    def update(self, mouse_pos, mouse_clicks):
        if not self.active:
            return

        self.update_outline()
        self.update_collision()
        self.update_hover(mouse_pos)
        self.update_drag(mouse_pos, mouse_clicks)
        self.setup_graphics()

    def draw(self, surface):
        if not self.visible:
            return

        if self.shadow_surface:
            surface.blit(self.shadow_surface, self.shadow_rect)
        if self.rect_surface:
            surface.blit(self.rect_surface, self.rect)
        if self.image_surface:
            surface.blit(self.image_surface, self.image_rect)
        if self.text_surface:
            surface.blit(self.text_surface, self.text_rect)
        if self.outline_surface:
            surface.blit(self.outline_surface, self.outline_rect)
        if self.collision_surface:
            surface.blit(self.collision_surface, self.collision_rect)
