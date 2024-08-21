import pygame
from utils import setup_managers


class UIElement:
    def __init__(self, element_type, element_id, config, managers, logger):
        # Core Attributes
        self.element_type = element_type
        self.element_id = element_id
        self.config = config
        self.managers = managers
        self.logger = logger

        # Set up references to managers
        setup_managers(self, managers)

        # Position Attributes
        self.position_x = config.get('position_x')
        self.position_y = config.get('position_y')

        # Rect Attributes
        self.rect_width = config.get('rect_width')
        self.rect_height = config.get('rect_height')
        self.rect_color = config.get('rect_color')
        self.rect_surface = None
        self.rect = None

        # Image Attributes
        self.image_path = config.get('image_path')
        self.image_width = config.get('image_width')
        self.image_height = config.get('image_height')
        self.image = None
        self.image_surface = None
        self.image_rect = None

        # Shadow Attributes
        self.shadow_enabled = config.get('shadow_enabled')
        self.shadow_color = config.get('shadow_color')
        self.shadow_offset = config.get('shadow_offset')
        self.shadow_blur = config.get('shadow_blur')
        self.shadow_surface = None

        # Text Attributes
        self.text_label = config.get('text_label', '')
        self.text_align = config.get('text_align', 'center')
        self.text_surface = None
        self.text_rect = None

        # Font Attributes
        self.font_name = config.get('font_name')
        self.font_size = config.get('font_size')
        self.font = None

        # Initialize Graphical Properties
        self.final_surface = None

        # Collision Attributes
        # Visibility Attributes
        # Layout Attributes
        # Shadow Attributes
        # Outline Attributes
        # Scroll Attributes
        # Tooltip Attributes
        # Hierarchy Attributes

        # Debug
        self.color = self.rect_color
        self.shadow_enabled = True
        self.shadow_offset = (5, 5)
        self.shadow_color = (255, 255, 255)
        self.font_size = 36
        self.text_color = (255, 255, 255)

        width = self.rect_width + self.shadow_offset[0]
        height = self.rect_height + self.shadow_offset[1]
        self.final_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Set up the graphical elements
        self.setup_graphics()

    def setup_graphics(self):
        """Initialize and set up all graphical components."""
        self.setup_rect()
        self.setup_image()
        self.setup_text()
        self.setup_shadow()
        self.compose_final_surface()

    def setup_rect(self):
        """
        Create and set up the surface for the rectangle.
        """
        if self.rect_width and self.rect_height:
            self.rect_surface = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
            self.rect_surface.fill(self.rect_color)
            self.rect = pygame.Rect(self.position_x, self.position_y, self.rect_width, self.rect_height)

    def setup_image(self):
        """
        Load and set up the image for the UI element.
        """
        if self.image_path:
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image_surface = self.image.copy()

            if self.image_width and self.image_height:
                self.image_surface = pygame.transform.scale(self.image_surface, (self.image_width, self.image_height))
                self.image_rect = pygame.Rect(self.position_x, self.position_y, self.image_width, self.image_height)
            else:
                self.image_rect = self.image.get_rect(topleft=(self.position_x, self.position_y))
                self.image_width, self.image_height = self.image_rect.size

    def setup_shadow(self):
        """
        Create and set up the shadow surface.
        """
        if self.shadow_enabled and self.rect_width and self.rect_height:
            shadow_width = self.rect_width + abs(self.shadow_offset[0])
            shadow_height = self.rect_height + abs(self.shadow_offset[1])
            self.shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
            shadow = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
            shadow.fill(self.shadow_color)
            shadow.set_alpha(self.shadow_blur)
            self.shadow_surface.blit(shadow, (max(0, self.shadow_offset[0]), max(0, self.shadow_offset[1])))

    def setup_text(self):
        """
        Set up the text for the UI element, including font and alignment.
        """
        if self.text_label and self.font_name:
            pass

        if True:
            self.font = pygame.font.Font(self.font_name, self.font_size)
            self.text_surface = self.font.render(self.text_label, True, self.text_color)
            self.text_rect = self.text_surface.get_rect()

    def compose_final_surface(self):
        """
        Compose the final surface by combining rect, image, shadow, and text.
        """
        if not self.final_surface:
            width, height = self.rect_width, self.rect_height
            if self.shadow_enabled:
                width += self.shadow_offset[0]
                height += self.shadow_offset[1]
            self.final_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        if self.shadow_surface:
            self.final_surface.blit(self.shadow_surface, (0, 0))
        if self.rect_surface:
            self.final_surface.blit(self.rect_surface, (0, 0))
        if self.image_surface:
            self.final_surface.blit(self.image_surface, (0, 0))
        if self.text_surface:
            self.final_surface.blit(self.text_surface, self.text_rect.topleft)

    def update(self, mouse_pos, mouse_clicks):
        pass

    def draw(self, surface):
        if self.final_surface:
            surface.blit(self.final_surface, (self.position_x, self.position_y))
