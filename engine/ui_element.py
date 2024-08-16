import pygame
from utils import setup_managers


class UIElement:
    def __init__(self, element_type, element_id, config, managers, logger):
        # Existing attributes
        self.element_type = element_type
        self.element_id = element_id
        self.config = config
        self.managers = managers
        self.logger = logger

        # Set up references to managers using the helper function
        setup_managers(self, managers)

        # Positional Attributes
        self.x = config['x']
        self.y = config['y']
        self.width = config['width']
        self.height = config['height']

        # Text Attributes
        self.label = config.get('label')
        self.font_name = config.get('font_name')
        self.font_size = config.get('font_size')
        self.color = config.get('color')

        # Image Attributes
        self.image_path = config.get('image')

        # Action Attributes
        self.action_str = config.get('action')

        # New Attributes
        self.border_color = config.get('border_color', (0, 0, 0))
        self.border_width = config.get('border_width', 0)
        self.hover_color = config.get('hover_color', None)
        self.click_color = config.get('click_color', None)
        self.opacity = config.get('opacity', 255)
        self.visible = config.get('visible', True)
        self.enabled = config.get('enabled', True)
        self.padding = config.get('padding', (0, 0))
        self.margin = config.get('margin', (0, 0))
        self.text_align = config.get('text_align', 'center')

        # Initialize graphical properties
        self.font = None
        self.image = None
        self.rect = None
        self.text_rect = None
        self.text_surface = None
        self.surface = None

        # Debug (To Be Deleted)
        self.font_name = None
        self.font_size = 36
        self.font = pygame.font.Font(self.font_name, self.font_size)

        # Set up the graphical elements
        self.setup_graphics()

    def setup_graphics(self):
        # Load image if specified
        if self.image_path:
            try:
                self.image = pygame.image.load(self.image_path).convert_alpha()
                self.image.set_alpha(self.opacity)
                self.rect = self.image.get_rect(topleft=(self.x, self.y))
                self.logger.log_info(f"Image loaded for {self.element_id} from {self.image_path}.")
            except pygame.error as e:
                self.logger.log_error(f"Failed to load image for {self.element_id} from {self.image_path}: {e}")
                self.image = None
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else:
            self.image = None
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Set up label and font if specified
        if self.label and self.font_name:
            self.font = pygame.font.Font(self.font_name, self.font_size)
            self.text_surface = self.font.render(self.label, True, self.color)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
            if self.text_align == 'left':
                self.text_rect.midleft = self.rect.midleft
            elif self.text_align == 'right':
                self.text_rect.midright = self.rect.midright
        else:
            self.text_surface = None
            self.text_rect = None

        # Set up color if specified and no image is loaded
        if not self.image and self.color:
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill(self.color)
            self.surface.set_alpha(self.opacity)
        else:
            self.surface = None

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
