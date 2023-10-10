import pygame
from os import path
from handler.error_handler import validate_files, validate_file

DEFAULT_FONT_SIZE = 24

class ResourceManager:
    """
    ResourceManager manages the loading and storage of various game resources such as graphics, audio, fonts, and more.

    Attributes:
        RESOURCE_MAPPING (dict): A dictionary mapping resource types to their respective loading methods and formats.
        music_resources (dict): A dictionary containing loaded music resources.
        sound_resources (dict): A dictionary containing loaded sound effect resources.
        button_resources (dict): A dictionary containing loaded button resources.
        font_resources (dict): A dictionary containing loaded font resources.
        image_resources (dict): A dictionary containing loaded image resources.
        image_sequence_resources (dict): A dictionary containing loaded image sequence (animation) resources.
        interface_resources (dict): A dictionary containing loaded interface (rectangular) resources.
        collision_resources (dict): A dictionary containing loaded collision resources.

    Example:
        # First, create instances of ResourceManager, AudioManager, GraphicManager, and OtherManager
        resource_manager = ResourceManager()
        audio_manager = AudioManager()
        graphic_manager = GraphicManager()
        other_manager = OtherManager()

        # Set resource folders for specific resource types
        resource_manager.set_resource_folders({"music": "music_folder", "image": "image_folder"})

        # Load resources from a dictionary using the ResourceManager
        resource_manager.load_resources({
            "background_music": {"type": "music", "filename": "bg_music.mp3"},
            "player_image": {"type": "image", "filename": "player.png"}
        })

        # Load resources from ResourceManager into AudioManager, GraphicManager, and OtherManager
        audio_manager.load_resources_from_manager(resource_manager)
        graphic_manager.load_resources_from_manager(resource_manager)
        other_manager.load_resources_from_manager(resource_manager)

        # Access loaded resources through AudioManager, GraphicManager, and OtherManager
        music = audio_manager.get_music("background_music")
        image = graphic_manager.get_image("player_image")
        other_resource = other_manager.get_resource("other_resource")

    Methods:
        - init_manager: Initialize the ResourceManager
        - set_resource_folders(resource_folders): Set resource folders for specific resource types.

        Data Loading Methods:
            - load_resources(resources_dict): Load multiple resources from a dictionary.
            - load_resource(resource_name, resource_data): Load a resource based on its type using the appropriate loading method.
            - load_multiple_resources(resource_name, resource_data, resource_folder, resource_type, supported_formats): Load multiple resources from data.
            - load_single_resource(resource_name, resource_data, resource_folder, resource_type, supported_formats): Load a single resource from data.
            - load_rect_resource(resource_name, resource_data): Load an interface rectangle resource from data.

        Resource Loading Methods:
            - load_music(name, data): Load a music resource.
            - load_sound(name, data): Load a sound effect resource.
            - load_font(name, data): Load a font resource.
            - load_image(name, data): Load a single image resource.
            - load_image_sequence(name, data): Load an image sequence as an animation.
            - load_interface(name, data): Load an interface rectangle.

    Note:
        You should customize the RESOURCE_MAPPING dictionary to define resource types, loading methods, and supported formats.
    """
    RESOURCE_MAPPING = {
        "music": {
            "load_data": "load_single_resource",
            "load_instance": "load_music",
            "folder": "TBD",  # Source folder for music resources (to be determined).
            "format": {".mp3", ".wav", ".ogg"}
        },
        "sound": {
            "load_data": "load_single_resource",
            "load_instance": "load_sound",
            "folder": "TBD",  # Source folder for sound effect resources (to be determined).
            "format": {".mp3", ".wav", ".ogg"}
        },
        "image": {
            "load_data": "load_single_resource",
            "load_instance": "load_image",
            "folder": "TBD",  # Source folder for image resources (to be determined).
            "format": {".png", ".jpg", ".jpeg", ".gif"}
        },
        "image_sequence": {
            "load_data": "load_multiple_resources",
            "load_instance": "load_image_sequence",
            "folder": "TBD",  # Source folder for image sequence resources (to be determined).
            "format": {".png", ".jpg", ".jpeg", ".gif"}
        },
        "font": {
            "load_data": "load_single_resource",
            "load_instance": "load_font",
            "folder": "TBD",  # Source folder for font resources (to be determined).
            "format": {".ttf"}
        },
        "interface": {
            "load_data": "load_rect_resource",
            "load_instance": "load_interface",
        },
        "button": {
            "load_data": "load_rect_resource",
            "load_instance": "load_button",
        },
    }

    def __init__(self):
        self.init_manager()

    def init_manager(self):
        """
        Initialize the ResourceManager when it is created or after a game restart.
        """
        # AudioManager
        self.music_resources = {}
        self.sound_resources = {}

        # ButtonManager
        self.button_resources = {}

        # FontManager
        self.font_resources = {}

        # GraphicManager
        self.image_resources = {}
        self.image_sequence_resources = {}
        self.interface_resources = {}
        self.button_resources = {}
        self.collision_resources = {}

    def set_resource_folders(self, resource_folders):
        """
        Set resource folders for specific resource types.

        Args:
            resource_folders (dict): A dictionary specifying resource folders for specific resource types.

        Raises:
            ValueError: If the specified resource type is invalid.

        Example:
            Define resource folders for different resource types and associate them with the ResourceManager.

            resource_manager = ResourceManager()
            folders = {
                "music": "music_folder",
                "image": "image_folder",
                "sound": "sound_folder",
            }
            resource_manager.set_resource_folders(folders)
        """
        for resource_type, folder in resource_folders.items():
            if resource_type in self.RESOURCE_MAPPING:
                self.RESOURCE_MAPPING[resource_type]["folder"] = folder
            else:
                raise ValueError(f"Invalid resource type '{resource_type}'.")

    """
    Data Loading
        - load_resources
        - load_resource
        - load_multiple_resources
        - load_single_resource
        - load_rect_resource
    """
    def load_resources(self, resources_dict):
        """Load multiple resources from a dictionary.

        Args:
            resources_dict (dict): A dictionary containing resources to load.
        """
        for resource_name, resource_data in resources_dict.items():
            self.load_resource(resource_name, resource_data)

    def load_resource(self, resource_name, resource_data):
        """
        Load a resource based on its type using the appropriate loading method.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data for the resource.

        Raises:
            ValueError: If the resource type is missing or not properly defined.
            ValueError: If the specified resource type is invalid for the resource.
            ValueError: If 'resource_folder' and 'supported_formats' are not properly defined.
            ValueError: If there's an error loading data for the resource.
            ValueError: If there's an error loading an instance of the resource.
        """
        # Step 1: Get the resource type from resource data
        resource_type = resource_data.get("type")
        if resource_type is None:
            raise ValueError(f"Resource type is missing or not properly defined for resource '{resource_name}'.")

        # Step 2: Check if the specified resource type exists in RESOURCE_MAPPING
        resource_info = self.RESOURCE_MAPPING.get(resource_type)
        if resource_info is None:
            raise ValueError(f"Invalid resource type '{resource_type}' for resource '{resource_name}'.")

        # Step 3: Get resource folder and supported formats from resource_info
        resource_folder = resource_info.get("folder", None)
        supported_formats = resource_info.get("format", set())

        # Step 4: Verify that 'resource_folder' and 'supported_formats' are correctly defined in RESOURCE_MAPPING
        if resource_folder is None and len(supported_formats) > 0:
            raise ValueError(
                f"'resource_folder' is not defined for resource '{resource_name}' but 'supported_formats' is defined.")
        elif resource_folder is not None and len(supported_formats) == 0:
            raise ValueError(
                f"'supported_formats' are not defined for resource '{resource_name}' but 'resource_folder' is defined.")

        # Step 5: Call the load_data_function
        load_data_function_name = resource_info.get("load_data")
        load_data_function = getattr(self, load_data_function_name)
        try:
            if load_data_function_name == "load_rect_resource":
                resource_data = load_data_function(resource_name, resource_data)
            else:
                resource_data = load_data_function(resource_name, resource_data, resource_folder, resource_type, supported_formats)
        except Exception as e:
            raise ValueError(f"Error loading data for resource '{resource_name}': {str(e)}")

        # Step 6: Call the load_instance_function
        load_instance_function_name = resource_info.get("load_instance")
        load_instance_function = getattr(self, load_instance_function_name)
        try:
            load_instance_function(resource_name, resource_data)
        except Exception as e:
            raise ValueError(f"Error loading instance for resource '{resource_name}': {str(e)}")

    @staticmethod
    def load_multiple_resources(resource_name, resource_data, resource_folder, resource_type, supported_formats):
        """
        Load multiple resources from data.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data for the resource.
            resource_folder (str): The source folder of the resources.
            resource_type (str): The type of the resources.
            supported_formats (set): The supported file formats for the resources.

        Returns:
            dict: The updated resource data.

        Raises:
            ValueError: If there's an error during resource loading.
        """
        resources_data = resource_data.get("files")
        file_paths = [path.join(resource_folder, file_data["filename"]) for file_data in resources_data]

        # Validate the resource paths and formats for each file
        validate_files(file_paths, resource_type, resource_name, supported_formats)
        resource_data["file_paths"] = file_paths

        return resource_data

    @staticmethod
    def load_single_resource(resource_name, resource_data, resource_folder, resource_type, supported_formats):
        """
        Load a single resource from data.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data for the resource.
            resource_folder (str): The source folder of the resource.
            resource_type (str): The type of the resource.
            supported_formats (set): The supported file formats for the resource.

        Returns:
            dict: The updated resource data.

        Raises:
            ValueError: If there's an error during resource loading.
        """
        resource_filename = resource_data.get("filename")
        file_path = path.join(resource_folder, resource_filename)

        # Validate the current resource loaded using the appropriate validation method
        validate_file(file_path, resource_type, resource_name, supported_formats)
        resource_data["file_path"] = file_path

        return resource_data

    @staticmethod
    def load_rect_resource(resource_name, resource_data):
        """
        Load an interface rectangle resource from data.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data for the resource.

        Returns:
            dict: The updated resource data.

        Raises:
            ValueError: If the 'rect' data is missing or invalid.
        """
        rect_data = resource_data.get("rect")
        if rect_data is None:
            raise ValueError(f"Missing 'rect' data for rect resource '{resource_name}'.")

        x = rect_data.get("x")
        y = rect_data.get("y")
        width = rect_data.get("width")
        height = rect_data.get("height")

        if x is None or y is None or width is None or height is None:
            raise ValueError(f"Invalid 'rect' data for rect resource '{resource_name}'. Missing or invalid variables.")

        # Create and return a pygame.Rect object
        resource_data["rect"] = pygame.Rect(x, y, width, height)
        return resource_data

    """
    Resource loading
        - AudioManager
            - load_music
            - load_sound
        - FontManager
            - load_font
        - GraphicManager
            - load_image
            - load_image_sequence
    """
    def load_music(self, name, data):
        """
        Load a piece of music from the specified data.

        Args:
            name (str): The name to assign to the loaded music.
            data (dict): A dictionary containing music data.
        """
        music_path = data["file_path"]
        pygame.mixer.music.load(music_path)
        self.music_resources[name] = music_path

    def load_sound(self, name, data):
        """
        Load a sound effect from the specified data.

        Args:
            name (str): The name to assign to the loaded sound effect.
            data (dict): A dictionary containing sound effect data.
        """
        sound_path = data["file_path"]
        sound = pygame.mixer.Sound(sound_path)
        self.sound_resources[name] = sound

    def load_font(self, name, data):
        """
        Load a font resource.

        Args:
            name (str): The name of the font resource.
            data (dict): A dictionary containing font resource data.
        """
        font_path = data["file_path"]
        font_size = data.get("size", DEFAULT_FONT_SIZE)
        self.font_resources[name] = pygame.font.Font(font_path, font_size)

    def load_image(self, name, data):
        """
        Load a single image resource from its data.

        Args:
            name (str): The name of the image resource.
            data (dict): A dictionary containing image resource data.
        """
        image_path = data["file_path"]
        data["image"] = pygame.image.load(image_path).convert_alpha()
        self.image_resources[name] = data

    def load_image_sequence(self, name, data):
        """
        Load an image sequence as an animation.

        Args:
            name (str): The name of the image sequence.
            data (dict): A dictionary containing image sequence data.
        """
        frames = []
        for frame_path in data["file_paths"]:
            frame = pygame.image.load(frame_path).convert_alpha()
            frames.append(frame)
        data["frames"] = frames
        self.image_sequence_resources[name] = data

    def load_interface(self, name, data):
        """
        Load an interface rectangle.

        Args:
            name (str): The name of the interface rectangle.
            data (dict): A dictionary containing interface rectangle data.
        """
        rect = data.get("rect")
        data["rect"] = rect

        # Create an instance of InterfaceRect and store it
        self.interface_resources[name] = data

    def load_button(self, name, data):
        pass

    def load_collision(self, name, data):
        pass
