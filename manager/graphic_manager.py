# graphic_manager.py

import pygame

class GraphicManager:
    """
    GraphicManager handles graphic resources and their instances in the game.

    Attributes:
        images (dict): A dictionary containing loaded image resources.
        image_sequences (dict): A dictionary containing loaded image sequence resources.
        interfaces (dict): A dictionary containing loaded interface resources.
        buttons (dict): A dictionary containing loaded button resources.

    Example:
        # Example dictionary for loading image and image sequence resources:
        graphic_dict = {
            "player_ship": {
                "type": "image",
                "filename": "player_ship.png",
            },
            "explosion_sequence": {
                "type": "image_sequence",
                "files": [
                    {"filename": "explosion_1.png"},
                    {"filename": "explosion_2.png"},
                    {"filename": "explosion_3.png"},
                ],
                "frame_duration": 100,
            },
        }

        # Create a GraphicManager instance and load resources:
        graphic_manager = GraphicManager()
        graphic_manager.load_resources(graphic_dict)

        # In your game loop, create graphic instances as needed and use them.
        while running:
            # Example: Creating an image graphic instance on-the-fly
            player_ship = graphic_manager.create_graphic_instance("player_ship", "image")

            # Update graphic instances
            player_ship.update()

            # Draw graphic instances on the screen
            player_ship.draw(screen)

    Dependencies:
        ResourceManager: A separate ResourceManager instance is required to load graphic resources.

    Methods:
    - Setup
        - load_resources_from_manager(resource_manager): Load music and sound resources from a ResourceManager.

    - Management
        - create_graphic_instance(name, resource_type): Create an instance of the appropriate graphic class.
    """
    def __init__(self):
        # Initialize dictionaries to store resource data
        self.images = {}
        self.image_sequences = {}
        self.interfaces = {}
        self.buttons = {}


    """
    Setup
        - load_resources
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
        self.buttons = resource_manager.load_resources_from_manager("button")


    """
    Management
        - create_graphic_instance
    """
    def create_graphic_instance(self, name, resource_type):
        """
        Create an instance of the appropriate graphic class based on the resource type.

        Args:
            name (str): The name of the resource.
            resource_type (str): The type of the resource.

        Returns:
            Graphic: An instance of the appropriate graphic class.
        """
        if resource_type == "image":
            return ImageGraphic(name, self.images[name])
        elif resource_type == "image_sequence":
            return ImageSequenceGraphic(name, self.image_sequences[name])
        elif resource_type == "interface":
            return InterfaceGraphic(name, self.interfaces[name])
        elif resource_type == "button":
            return ButtonGraphic(name, self.buttons[name])
        else:
            raise ValueError("Unknown resource type: {}".format(resource_type))



class ImageGraphic:
    def __init__(self, name, data):
        """
        Initialize an ImageGraphic instance.

        Args:
            name (str): The name of the graphic.
            data (dict): A dictionary containing graphic data.
        """
        self.name = name
        self.image = data["image"]

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
    def __init__(self, name, data):
        """
        Initialize an ImageSequenceGraphic instance.

        Args:
            name (str): The name of the graphic.
            data (dict): A dictionary containing graphic data.
        """
        self.name = name
        self.frames = data["frames"]
        self.frame_duration = data["frame_duration"]
        self.current_frame = 0
        self.time_elapsed = 0

    def update(self, dt):
        """
        Update the animation frame based on elapsed time.

        Args:
            dt (int): The time elapsed since the last update (in milliseconds).
        """
        self.time_elapsed += dt
        if self.time_elapsed >= self.frame_duration:
            self.time_elapsed = 0
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
    def __init__(self, name, data):
        """
        Initialize an InterfaceGraphic instance.

        Args:
            name (str): The name of the graphic.
            data (dict): A dictionary containing graphic data.
        """
        self.name = name
        self.rect = data["rect"]
        self.hit_rect = data["hit_rect"]

        color_data = data["color"]
        self.default_color = color_data.get("default", (0, 0, 0))
        self.border_color = color_data.get("border", (255, 255, 255))

        self.border_size = data.get("border_size", 0)

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
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_size)



class ButtonGraphic:
    def __init__(self, name, data):
        """
        Initialize an ButtonGraphic instance.

        Args:
            name (str): The name of the graphic.
            data (dict): A dictionary containing graphic data.
        """
        self.name = name
        self.rect = pygame.Rect(0, 0, 0, 0)

        color_data = data["color"]
        self.color_active = color_data.get("active", (0, 0, 0))
        self.color_inactive = color_data.get("inactive", (255, 0, 0))
        self.border_color = color_data.get("border", (255, 255, 255))
        self.color = self.color_inactive

        self.border_size = data.get("border_size", 0)

    def set_rect(self, rect):
        """
        Set the rectangular area for the button graphic.

        Args:
            rect (tuple or pygame.Rect): The rectangular area (x, y, width, height) for the button graphic.
        """
        self.rect = pygame.Rect(rect)

    def update(self):
        pass

    def draw(self, screen):
        """
        Draw the filled rectangle with a border on the screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_size)
