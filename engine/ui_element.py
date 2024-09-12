# ui_element.py

import pygame
from utils import setup_managers

DEFAULT_CONFIG = {
    'pos_x': 0,
    'pos_y': 0,
    'align': 'center',
    'rectangle_enabled': True,
    'image_enabled': True,
    'shadow_enabled': True,
    'shadow_color': (255, 255, 255),
    'shadow_offset': (5, 5),
    'shadow_blur': 150,
    'text_enabled': True,
    'text_color': (255, 255, 255),
    'text_align': 'center',
    'text_font_size': 36,
    'hover_color': (255, 0, 0),
    'outline_enabled': True,
    'outline_color': (0, 255, 255),
    'outline_border': 1,
    'collision_enabled': True,
    'collision_color': (255, 0, 0),
    'collision_border': 1,
    'state_active': True,
    'state_visible': True,
    'layer': 0,
    'drag_enabled': True,
    'drag_exclusive': True
}


class UIElement:
    def __init__(self, element_type, element_id, config, managers, logger):
        """
        Initialize UIElement with its type, ID, config, and necessary managers.

        Args:
            element_type (str): The type of element.
            element_id (str): The unique ID for the element.
            config (dict): A configuration dictionary for element properties.
            managers (dict): External managers for handling dependencies.
            logger (Logger): Logger instance for logging warnings or info.
        """
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

        # Rectangle Attributes
        self.rectangle_enabled = self.config.get('rectangle_enabled')
        self.rectangle_width = self.config.get('rectangle_width')
        self.rectangle_height = self.config.get('rectangle_height')
        self.rectangle_color = self.config.get('rectangle_color')
        self.rectangle_surface = None
        self.rectangle_rect = None

        # Image Attributes
        self.image_enabled = self.config.get('image_enabled')
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
        self.text_enabled = self.config.get('text_enabled')
        self.text_label = self.config.get('text_label')
        self.text_color = self.config.get('text_color')
        self.text_align = self.config.get('text_align')
        self.text_font_name = self.config.get('text_font_name')
        self.text_font_size = self.config.get('text_font_size')
        self.text_surface = None
        self.text_rect = None
        self.text_font = None

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
        self.state_active = self.config.get('state_active')
        self.state_visible = self.config.get('state_visible')
        
        # TBD Attributes
        self.layer = self.config.get('layer')

        # Drag Attributes
        self.drag_enabled = self.config.get('drag_enabled')
        self.drag_exclusive = self.config.get('drag_exclusive')
        self.dragging = False
        self.drag_offset = None
        self.original_pos = None

        # Initialize graphical components
        self.setup_graphics()

    """
    Helper Methods
    - create_surface_rect
    - align_rect
    """
    def create_surface_rect(self, width, height,
                            position=None, align=None,
                            color=None, alpha=None,
                            shape=None, border_thickness=None):
        # Create the surface with or without alpha channel
        surface_flags = pygame.SRCALPHA if alpha is not None else 0
        surface = pygame.Surface((width, height), surface_flags)

        # Create a rect from the surface
        rect = surface.get_rect()

        # Handle color and shape drawing operations
        if color:
            if shape is None:
                surface.fill(color)
            elif shape == "rect":
                pygame.draw.rect(surface, color, rect, border_thickness or 0)
            elif shape == "circle":
                radius = min(rect.width, rect.height) // 2
                pygame.draw.circle(surface, color, rect.center, radius, border_thickness or 0)
            else:
                self.logger.log_warning(f"Unknown shape: {shape}")
        elif shape:
            self.logger.log_warning(f"Unknown color: {color}")

        # Set surface transparency if alpha is provided
        if alpha:
            surface.set_alpha(alpha)

        # Set alignment and position (default if not provided)
        align = align or self.align
        position = position or (self.pos_x, self.pos_y)
        self.align_rect(rect, align, position)

        return surface, rect

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

    """
    Setup Methods
    - setup_graphics
        - setup_image
        - setup_rect
        - setup_shadow
        - setup_collision
        - setup_text
    """
    def setup_graphics(self):
        """Initialize and set up all graphical components."""
        self.setup_image()
        self.setup_rect()
        self.setup_shadow()
        self.setup_collision()
        self.setup_text()

    def setup_image(self):
        """
        Set up the image surface and rect.
        """
        if not self.image_enabled or not self.image_path:
            return

        # Load the image surface with alpha transparency
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image_surface = self.image.copy()

        # Check if specific dimensions for the image are provided
        if self.image_width and self.image_height:
            self.image_surface = pygame.transform.scale(self.image_surface, (self.image_width, self.image_height))
        else:
            self.image_width, self.image_height = self.image_surface.get_size()

        # Create the image rect
        self.image_rect = self.image_surface.get_rect()

        # Align the image rect
        self.align_rect(self.image_rect, self.align, (self.pos_x, self.pos_y))

    def setup_rect(self):
        """
        Set up the rectangle surface and rect.
        """
        if not self.rectangle_enabled:
            return

        # Create the rectangle surface and rect; fill the surface
        self.rectangle_surface, self.rectangle_rect = self.create_surface_rect(
            self.rectangle_width, self.rectangle_height,
            position=(self.pos_x, self.pos_y), align=self.align,
            color=self.rectangle_color, alpha=False,
            shape=None, border_thickness=None
        )

    def setup_shadow(self):
        """
        Set up the shadow surface and rect.
        """
        if not self.shadow_enabled:
            return

        # Calculate shadow position based on rectangle position and offset
        self.shadow_pos_x = self.rectangle_rect.x + self.shadow_offset[0]
        self.shadow_pos_y = self.rectangle_rect.y + self.shadow_offset[1]

        # Create the shadow surface and rect; fill the surface
        self.shadow_surface, self.shadow_rect = self.create_surface_rect(
            self.rectangle_width, self.rectangle_height,
            position=(self.shadow_pos_x, self.shadow_pos_y), align='nw',
            color=self.rectangle_color, alpha=self.shadow_blur,
            shape=None, border_thickness=None,
        )

    def setup_collision(self):
        """
        Update the collision surface and rect.
        """
        if not self.collision_enabled:
            return

        # Determine the size of the collision surface
        if self.collision_width and self.collision_height:
            width, height = (self.collision_width, self.collision_height)
        elif self.rectangle_width and self.rectangle_height:
            width, height = self.rectangle_surface.get_size()
        elif self.image_path:
            width, height = self.image_surface.get_size()
        else:
            width, height = (0, 0)
            self.logger.log_warning(f"Collision rect for element '{self.element_id}' could not be initialized.")

        # Create the collision surface and rect
        self.collision_surface, self.collision_rect = self.create_surface_rect(
            width, height,
            position=(self.pos_x, self.pos_y), align=self.align,
            color=self.collision_color, alpha=255,
            shape="rect", border_thickness=self.collision_border,
        )

    def setup_text(self):
        """
        Set up the text surface and rect.
        """
        if not self.text_enabled:
            return

        # Initialize the text_font
        self.text_font = pygame.font.Font(self.text_font_name, self.text_font_size)

        # Create the text surface and rect
        self.text_surface = self.text_font.render(self.text_label, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()

        # Align the text rect
        self.align_rect(self.text_rect, self.text_align, (self.pos_x, self.pos_y))

    """
    Update Methods
    - update_graphics
        - update_rect
        - update_outline
    - update_events
        - update_click
        - update_scroll
        - update_hover
        - update_drag
    """
    def update_graphics(self):
        self.update_rect()
        self.update_outline()

    def update_events(self, mouse_pos):
        self.update_drag(mouse_pos)
        self.update_hover(mouse_pos)

    def update_rect(self):
        """
        Update the positions of the rects based on alignment and position.
        """
        if self.rectangle_rect:
            self.align_rect(self.rectangle_rect, self.align, (self.pos_x, self.pos_y))
        if self.image_rect:
            self.align_rect(self.image_rect, self.align, (self.pos_x, self.pos_y))
        if self.shadow_rect:
            self.shadow_pos_x = self.rectangle_rect.x + self.shadow_offset[0]
            self.shadow_pos_y = self.rectangle_rect.y + self.shadow_offset[1]
            self.align_rect(self.shadow_rect, 'nw', (self.shadow_pos_x, self.shadow_pos_y))
        if self.text_rect:
            self.align_rect(self.text_rect, self.text_align, (self.pos_x, self.pos_y))
        if self.collision_rect:
            self.align_rect(self.collision_rect, self.align, (self.pos_x, self.pos_y))

    def update_outline(self):
        """
        Update the outline surface and rect.
        """
        if not self.outline_enabled:
            return

        # Initialize a list for all defined rectangles
        rects = [self.rectangle_rect, self.image_rect, self.shadow_rect, self.text_rect]

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

    def update_click(self):
        pass

    def update_scroll(self):
        pass

    def update_hover(self, mouse_pos):
        """
        Update the hover logic.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse cursor.
        """
        # Determine if the mouse is hovering over the collision rect
        self.hovered_state = self.collision_rect.collidepoint(mouse_pos)
        if self.rectangle_surface and self.hover_color:
            # Change the rect color based on the hover state
            self.rectangle_surface.fill(self.hover_color if self.hovered_state else self.rectangle_color)

    def update_drag(self, mouse_pos):
        """
        Update the drag logic.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse cursor.
        """
        if not self.drag_enabled:
            return

        mouse_buttons = pygame.mouse.get_pressed()

        # Left mouse button is pressed
        if mouse_buttons[0]:
            if self.dragging:
                if mouse_buttons[2]:
                    # Right mouse button cancels dragging
                    self.dragging = False
                    self.pos_x, self.pos_y = self.original_pos
                else:
                    # Update position based on the current mouse position and the calculated drag offset
                    self.pos_x = mouse_pos[0] - self.drag_offset[0]
                    self.pos_y = mouse_pos[1] - self.drag_offset[1]
            elif self.collision_rect.collidepoint(mouse_pos):
                # Check if the mouse is within the element's rectangle to start dragging
                self.dragging = True

                # Store the original position before starting the drag
                self.original_pos = (self.pos_x, self.pos_y)

                # Calculate the drag offset differently based on the alignment
                offset_x = mouse_pos[0] - self.rectangle_rect.centerx
                offset_y = mouse_pos[1] - self.rectangle_rect.centery

                # Adjust the offset if the alignment is not centered
                if self.align != 'center':
                    # Adjust the x-offset based on horizontal alignment
                    if 'w' in self.align:
                        offset_x = mouse_pos[0] - self.rectangle_rect.left
                    elif 'e' in self.align:
                        offset_x = mouse_pos[0] - self.rectangle_rect.right

                    # Adjust the y-offset based on vertical alignment
                    if 'n' in self.align:
                        offset_y = mouse_pos[1] - self.rectangle_rect.top
                    elif 's' in self.align:
                        offset_y = mouse_pos[1] - self.rectangle_rect.bottom

                # Store the calculated drag offset
                self.drag_offset = (offset_x, offset_y)
        else:
            # Stop dragging when the mouse button is released
            self.dragging = False

    """
    Game Loop
    - update
    - draw
    """
    def update(self, mouse_pos, mouse_clicks):
        if not self.state_active:
            return

        self.update_graphics()
        self.update_events(mouse_pos)

    def draw(self, surface):
        if not self.state_visible:
            return

        if self.shadow_surface:
            surface.blit(self.shadow_surface, self.shadow_rect)
        if self.rectangle_surface:
            surface.blit(self.rectangle_surface, self.rectangle_rect)
        if self.image_surface:
            surface.blit(self.image_surface, self.image_rect)
        if self.text_surface:
            surface.blit(self.text_surface, self.text_rect)
        if self.outline_surface:
            surface.blit(self.outline_surface, self.outline_rect)
        if self.collision_surface:
            surface.blit(self.collision_surface, self.collision_rect)
