# graphic_manager.py

import pygame

class GraphicManager:
    """
    GraphicManager handles graphic resources and their instances in the game.

    Attributes:
        images (dict): A dictionary containing loaded image resources.
        image_sequences (dict): A dictionary containing loaded image sequence resources.
        interfaces (dict): A dictionary containing loaded interface resources.
        graphics (dict): A dictionary containing instances of graphic resources.

    Example:
        # First, define a ResourceManager and load graphic resources into it.
        # Then, create an GraphicManager, load graphic resources from the ResourceManager, and create instance:

        graphic_manager = GraphicManager()
        graphic_manager.load_resources(resource_manager)

        In your game loop, update and draw the graphics using the GraphicManager.

        while running:
            # Update graphic instances
            graphic_manager.update()

            # Draw graphic instances on the screen
            graphic_manager.draw(screen)

    Dependencies:
        ResourceManager: A separate ResourceManager instance is required to load graphic resources.

    Methods:
    - Resource Loading
        - load_resources_from_manager(resource_manager): Load music and sound resources from a ResourceManager.
        - create_graphics: Create instances for loaded graphic resources.

    - Graphic Management
        - update: Update the logic of graphic instances.
        - draw(screen): Draw graphic instances on the screen.
    """
    def __init__(self):
        # Initialize dictionaries to store resource data
        self.images = {}
        self.image_sequences = {}
        self.interfaces = {}

        # Dictionary to store graphic instances
        self.graphics = {}


    """
    Resources Loading
        - load_resources
        - create_graphics
    """
    def load_resources(self, resource_manager):
        """
        Load graphic resources from a ResourceManager.

        Args:
            resource_manager (ResourceManager): The ResourceManager containing loaded resources.
        """
        self.images = resource_manager.load_resources_from_manager("image")
        self.image_sequences = resource_manager.load_resources_from_manager("image_sequence")
        self.interfaces = resource_manager.load_resources_from_manager("interface")

        # Create instances for the loaded resources
        self.create_graphics()

    def create_graphics(self):
        """
        Create instances for loaded resources.
        """
        # Create instances for images
        for name, data in self.images.items():
            image = data["image"]
            self.graphics[name] = ImageGraphic(name, image)

        # Create instances for image sequences
        for name, data in self.image_sequences.items():
            frames = data["frames"]
            frame_duration = data["frame_duration"]
            self.graphics[name] = ImageSequenceGraphic(name, frames, frame_duration)

        # Create instances for interfaces
        for name, data in self.interfaces.items():
            color_data = data["color"]
            rect = data["rect"]
            hit_rect = data["hit_rect"]
            border_data = data["border"]
            self.graphics[name] = InterfaceGraphic(name, color_data, border_data, rect, hit_rect)





    """
    Graphic Management
        - update
        - draw
    """
    def update(self, dt):
        """
        Update the logic of graphic instances.

        Args:
            dt (int): The time elapsed since the last update (in milliseconds).
        """
        for graphic in self.graphics.values():
            graphic.update(dt)

    def draw(self, screen):
        """
        Draw graphic instances on the screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        for graphic in self.graphics.values():
            graphic.draw(screen)



class ImageGraphic:
    def __init__(self, name, image):
        """
        Initialize an ImageGraphic instance.

        Args:
            name (str): The name of the graphic.
            image (pygame.Surface): The image to be displayed.
        """
        self.name = name
        self.image = image

    def update(self, *args, **kwargs):
        """
        Update method for ImageGraphic (not used).
        """
        pass

    def draw(self, screen, position):
        """
        Draw the ImageGraphic on the screen at the specified position.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
            position (tuple): The (x, y) position to draw the image.
        """
        screen.blit(self.image, position)

class ImageSequenceGraphic:
    def __init__(self, name, frames, frame_duration):
        """
        Initialize an ImageSequenceGraphic instance.

        Args:
            name (str): The name of the graphic.
            frames (list): A list of pygame.Surface frames for the animation.
            frame_duration (int): The duration (in milliseconds) of each frame.
        """
        self.name = name
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.frame_elapsed = 0

    def update(self, dt):
        """
        Update the animation frame based on elapsed time.

        Args:
            dt (int): The time elapsed since the last update (in milliseconds).
        """
        self.frame_elapsed += dt
        if self.frame_elapsed >= self.frame_duration:
            self.frame_elapsed = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen, position):
        """
        Draw the current frame of the ImageSequenceGraphic on the screen at the specified position.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
            position (tuple): The (x, y) position to draw the frame.
        """
        screen.blit(self.frames[self.current_frame], position)

class InterfaceGraphic:
    def __init__(self, name, color_data, border_data, rect, hit_rect):
        """
        Initialize an InterfaceGraphic instance.

        Args:
            name (str): The name of the graphic.
            color_data (dict): A dictionary containing color attributes, e.g., {"default": (0, 0, 0), "border": (255, 255, 255)}.
            border_data (dict): A dictionary containing border attributes, e.g., {"width": 2, "height": 2}.
            rect (pygame.Rect): The bounding rectangle of the graphic.
            hit_rect (pygame.Rect): The collision detection rectangle.
        """
        self.name = name
        self.default_color = color_data.get("default", (0, 0, 0))
        self.border_color = color_data.get("border", (255, 255, 255))
        self.border_width = border_data.get("width", 0)
        self.border_height = border_data.get("height", 0)
        self.rect = rect
        self.hit_rect = hit_rect

    def check_collision(self, other_rect):
        """
        Check if the interface graphic collides with another rectangle.

        Args:
            other_rect (pygame.Rect): The other rectangle for collision detection.

        Returns:
            bool: True if there is a collision, False otherwise.
        """
        return self.hit_rect.colliderect(other_rect)

    def update(self, *args, **kwargs):
        """
        Update method for InterfaceGraphic (not used).
        """
        pass

    def draw(self, screen):
        """
        Draw the filled rectangle with a border on the screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        pygame.draw.rect(screen, self.default_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
