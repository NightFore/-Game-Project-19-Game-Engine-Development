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
    'draggable': True
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
        self.shadow_pos_x = None
        self.shadow_pos_y = None

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
        self.outline_pos_x = None
        self.outline_pos_y = None

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

        # Drag Attributes
        self.draggable = self.config.get('draggable')
        self.drag_offset = None
        self.dragging = False
        self.original_pos = None

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
        self.setup_collision()

    def setup_rect(self):
        """
        Set up the rectangle surface and rect.
        """
        if self.rect_width and self.rect_height:
            # Create the rectangle surface and rect
            self.rect_surface = pygame.Surface((self.rect_width, self.rect_height))
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)

            # Fill the rectangle surface
            self.rect_surface.fill(self.rect_color)

            # Align the rectangle rect
            self.align_rect(self.rect, self.align, (self.pos_x, self.pos_y))

    def setup_image(self):
        """
        Set up the image surface and rect.
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

            # Align the image rect
            self.align_rect(self.image_rect, self.align, (self.pos_x, self.pos_y))

    def setup_shadow(self):
        """
        Set up the shadow surface and rect.
        """
        if self.shadow_enabled:
            # Create the shadow surface and rect
            self.shadow_surface = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
            self.shadow_rect = self.shadow_surface.get_rect()

            # Fill the rectangle surface and apply blur
            self.shadow_surface.fill(self.shadow_color)
            self.shadow_surface.set_alpha(self.shadow_blur)

            # Align the shadow rect
            self.shadow_pos_x = self.rect.x + self.shadow_offset[0]
            self.shadow_pos_y = self.rect.y + self.shadow_offset[1]
            self.align_rect(self.shadow_rect, 'nw', (self.shadow_pos_x, self.shadow_pos_y))

    def setup_text(self):
        """
        Set up the text surface and rect.
        """
        if self.text_label:
            # Initialize the font
            self.font = pygame.font.Font(self.font_name, self.font_size)

            # Create the text surface and rect
            self.text_surface = self.font.render(self.text_label, True, self.text_color)
            self.text_rect = self.text_surface.get_rect()

            # Align the text rect
            self.align_rect(self.text_rect, self.text_align, (self.pos_x, self.pos_y))

    def setup_collision(self):
        """
        Update the collision surface and rect.
        """
        if self.collision_enabled:
            if self.collision_width and self.collision_height:
                size = (self.collision_width, self.collision_height)
            elif self.rect_width and self.rect_height:
                size = self.rect_surface.get_size()
            elif self.image_path:
                size = self.image_surface.get_size()
            else:
                size = (0, 0)
                self.logger.log_warning(f"Collision rect for element '{self.element_id}' could not be initialized.")

            # Create the collision surface and rect
            self.collision_surface = pygame.Surface(size, pygame.SRCALPHA)
            self.collision_rect = self.collision_surface.get_rect()

            # Draw the collision on the surface
            pygame.draw.rect(self.collision_surface, self.collision_color, self.collision_rect, self.collision_border)

            # Align the collision rect
            self.align_rect(self.collision_rect, self.align, (self.pos_x, self.pos_y))

    def align_rect(self, rect, align, position):
        """
        Align the rectangle based on the provided alignment and position.
        """
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
            self.logger.log_warning(f"Unsupported alignment value '{align}' provided.")

    def update_rect(self):
        """
        Update the positions of the rects based on alignment and position.
        """
        if self.rect:
            self.align_rect(self.rect, self.align, (self.pos_x, self.pos_y))
        if self.image_rect:
            self.align_rect(self.image_rect, self.align, (self.pos_x, self.pos_y))
        if self.shadow_rect:
            self.shadow_pos_x = self.rect.x + self.shadow_offset[0]
            self.shadow_pos_y = self.rect.y + self.shadow_offset[1]
            self.align_rect(self.shadow_rect, 'nw', (self.shadow_pos_x, self.shadow_pos_y))
        if self.text_rect:
            self.align_rect(self.text_rect, self.text_align, (self.pos_x, self.pos_y))
        if self.collision_rect:
            self.align_rect(self.collision_rect, self.align, (self.pos_x, self.pos_y))

    def update_outline(self):
        """
        Update the outline surface and rect.
        """
        if self.outline_enabled:
            # Initialize a list for all defined rectangles
            rects = [self.rect, self.image_rect, self.shadow_rect, self.text_rect]

            # Remove None values from the list
            rects = [r for r in rects if r]

            # Calculate the bounding box that contains all the rects
            min_x = min(r.x for r in rects)
            min_y = min(r.y for r in rects)
            max_x = max(r.right for r in rects)
            max_y = max(r.bottom for r in rects)
            width = max_x - min_x
            height = max_y - min_y

            # Create a new outline rect if the bounding box has changed
            if pygame.Rect(min_x, min_y, width, height) != self.outline_rect:
                # Update the outline position
                self.outline_pos_x, self.outline_pos_y = (min_x, min_y)

                # Create the outline surface and rect
                self.outline_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                self.outline_rect = self.outline_surface.get_rect()

                # Draw the outline on the surface
                pygame.draw.rect(self.outline_surface, self.outline_color, self.outline_rect, self.outline_border)

                # Align the outline rect
                self.align_rect(self.outline_rect, 'nw', (self.outline_pos_x, self.outline_pos_y))

    def update_hover(self, mouse_pos):
        """
        Handle the hover logic.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse cursor.
        """
        # Determine if the mouse is hovering over the collision rect
        self.hovered_state = self.collision_rect.collidepoint(mouse_pos)
        if self.rect_surface and self.hover_color:
            # Change the rect color based on the hover state
            self.rect_surface.fill(self.hover_color if self.hovered_state else self.rect_color)

    def update_drag(self, mouse_pos):
        """
        Handle the drag logic.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse cursor.
        """
        if self.draggable:
            mouse_buttons = pygame.mouse.get_pressed()

            # Left mouse button is pressed
            if mouse_buttons[0]:
                if self.dragging:
                    # Update position based on the current mouse position and the calculated drag offset
                    self.pos_x = mouse_pos[0] - self.drag_offset[0]
                    self.pos_y = mouse_pos[1] - self.drag_offset[1]

                    # Right mouse button cancels dragging
                    if mouse_buttons[2]:
                        self.dragging = False
                        self.pos_x, self.pos_y = self.original_pos
                elif self.collision_rect.collidepoint(mouse_pos):
                    # Check if the mouse is within the element's rectangle to start dragging
                    self.dragging = True

                    # Store the original position before starting the drag
                    self.original_pos = (self.pos_x, self.pos_y)

                    # Calculate the drag offset differently based on the alignment
                    offset_x = mouse_pos[0] - self.rect.centerx
                    offset_y = mouse_pos[1] - self.rect.centery

                    # Adjust the offset if the alignment is not centered
                    if self.align != 'center':
                        # Adjust the x-offset based on horizontal alignment
                        if 'w' in self.align:
                            offset_x = mouse_pos[0] - self.rect.left
                        elif 'e' in self.align:
                            offset_x = mouse_pos[0] - self.rect.right

                        # Adjust the y-offset based on vertical alignment
                        if 'n' in self.align:
                            offset_y = mouse_pos[1] - self.rect.top
                        elif 's' in self.align:
                            offset_y = mouse_pos[1] - self.rect.bottom

                    # Store the calculated drag offset
                    self.drag_offset = (offset_x, offset_y)
            else:
                # Stop dragging when the mouse button is released
                self.dragging = False

    def update(self, mouse_pos, mouse_clicks):
        if not self.active:
            return

        self.update_rect()
        self.update_outline()
        self.update_hover(mouse_pos)
        self.update_drag(mouse_pos)

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
