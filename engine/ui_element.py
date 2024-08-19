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

        # Set up references to managers using the helper function
        setup_managers(self, managers)

        # Positional Attributes
        self.x = config.get('x')
        self.y = config.get('y')
        self.width = config.get('width')
        self.height = config.get('height')

        # Text Attributes
        self.label = config.get('label', '')
        self.font_name = config.get('font_name', None)
        self.font_size = config.get('font_size', 24)
        self.color = config.get('color', (255, 255, 255))

        # Image Attributes
        self.image_path = config.get('image')

        # Action Attributes
        self.action_str = config.get('action')

        # Enhanced Attributes
        self.border_color = config.get('border_color', (0, 0, 0))
        self.border_width = config.get('border_width', 0)
        self.hover_color = config.get('hover_color')
        self.click_color = config.get('click_color')
        self.opacity = config.get('opacity', 255)
        self.visible = config.get('visible', True)
        self.enabled = config.get('enabled', True)
        self.padding = config.get('padding', (0, 0, 0, 0))  # top, right, bottom, left
        self.margin = config.get('margin', (0, 0, 0, 0))  # top, right, bottom, left
        self.text_align = config.get('text_align', 'center')
        self.corner_radius = config.get('corner_radius', 0)
        self.shadow_enabled = config.get('shadow_enabled', False)
        self.shadow_color = config.get('shadow_color', (0, 0, 0))
        self.shadow_offset = config.get('shadow_offset', (5, 5))
        self.shadow_blur = config.get('shadow_blur', 5)
        self.tooltip_text = config.get('tooltip_text', '')
        self.tooltip_font = config.get('tooltip_font', self.font_name)
        self.tooltip_text_color = config.get('tooltip_text_color', (255, 255, 255))
        self.tooltip_background_color = config.get('tooltip_background_color', (0, 0, 0))
        self.draggable = config.get('draggable', False)
        self.auto_hide = config.get('auto_hide', False)
        self.parent = None
        self.children = []
        self.scrollable = config.get('scrollable', False)
        self.scroll_offset = config.get('scroll_offset', (0, 0))
        self.outline_mode = config.get('outline_mode', False)
        self.outline_color = config.get('outline_color', (255, 0, 0))
        self.outline_thickness = config.get('outline_thickness', 1)

        # Initialize Graphical Properties
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.image = None
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_rect = None
        self.text_surface = None
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Debug (To Be Deleted)
        self.font_name = None
        self.font_size = 36
        self.font = pygame.font.Font(self.font_name, self.font_size)

        self.image_width = config.get('image_width')
        self.image_height = config.get('image_height')
        self.image_rect = None

        # Set up the graphical elements
        self.setup_graphics()

    def setup_graphics(self):
        """Initialize and set up all graphical components."""
        self.setup_rect()
        self.setup_image()
        self.setup_text()
        self.setup_color()

    def setup_rect(self):
        """
        Set up the rectangle for the UI element, used for background or borders.
        """
        # Initialize rectangle with the specified size or default
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def setup_image(self):
        """
        Load and set up the image for the UI element.
        Image size can be used to set the rectangle size if no explicit size is provided.
        """
        if self.image_path:
            # Load and process the image
            self.image = pygame.image.load(self.image_path).convert_alpha()

            # Use provided image size if specified
            if self.image_width and self.image_height:
                self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
                self.image_rect = pygame.Rect(self.x, self.y, self.image_width, self.image_height)
            else:
                self.image_rect = self.image.get_rect(topleft=(self.x, self.y))

            # Apply opacity if specified
            self.image.set_alpha(self.opacity)

    def setup_text(self):
        """
        Set up the text for the UI element, including font and alignment.
        """
        if self.label and self.font_name:
            self.font = pygame.font.Font(self.font_name, self.font_size)
            self.text_surface = self.font.render(self.label, True, self.color)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
            if self.text_align == 'left':
                self.text_rect.midleft = self.rect.midleft
            elif self.text_align == 'right':
                self.text_rect.midright = self.rect.midright

    def setup_color(self):
        """
        Set up the color for the UI element if no image is provided.
        """
        if not self.image and self.color:
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill(self.color)
            self.surface.set_alpha(self.opacity)

    def update(self, mouse_pos, mouse_clicks):
        if not self.visible:
            return

        if self.rect.collidepoint(mouse_pos):
            if self.hover_color:
                self.surface.fill(self.hover_color)
            if any(mouse_clicks):
                if self.click_color:
                    self.surface.fill(self.click_color)

    def draw(self, surface):
        if not self.visible:
            return

        # Draw the element
        if self.image:
            surface.blit(self.image, self.rect)
        elif self.surface:
            surface.blit(self.surface, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # Draw the border if specified
        if self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        # Draw the label
        if self.label and self.font:
            text_surface = self.font.render(self.label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
