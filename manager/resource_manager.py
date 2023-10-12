import pygame
from os import path
from handler.error_handler import validate_files, validate_file

class ResourceManager:
    """
    ResourceManager manages the loading and storage of various game resources such as graphics, audio, fonts, and more.

    Attributes:
        RESOURCE_MAPPING (dict): A dictionary mapping resource types to their respective loading methods and formats.
        resources (dict): A unified dictionary to store resources of different types.

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

    Methods:
        - init_manager: Initialize the ResourceManager
        - set_resource_folders(resource_folders): Set resource folders for specific resource types.

        Data Loading Methods:
            - load_resources(resources_dict): Load multiple resources from a dictionary.
            - load_resource(resource_name, resource_data): Load a resource based on its type using the appropriate loading method.
            - load_files(resource_name, resource_data, resource_folder, resource_type, supported_formats): Load multiple resources from data.
            - load_file(resource_name, resource_data, resource_folder, resource_type, supported_formats): Load a single resource from data.
            - load_rect(resource_name, resource_data): Load an interface rectangle resource from data.

        Resource Loading Methods:
            - load_music(name, data): Load a music resource.
            - load_sound(name, data): Load a sound effect resource.
            - load_font(name, data): Load a font resource.
            - load_image(name, data): Load a single image resource.
            - load_image_sequence(name, data): Load an image sequence as an animation.
            - load_interface(name, data): Load an interface rectangle.
    """
    RESOURCE_MAPPING = {
        # Note: Make sure to initialize the 'folder' values using 'set_resource_folders'.
        "music": {
            "load_type": "load_file",
            "load_data": "load_music",
            "format": {".mp3", ".wav", ".ogg"},
            "folder": None
        },
        "sound": {
            "load_type": "load_file",
            "load_data": "load_sound",
            "format": {".mp3", ".wav", ".ogg"},
            "folder": None
        },
        "font": {
            "load_type": "load_file",
            "load_data": "load_font",
            "format": {".ttf"},
            "folder": None
        },
        "image": {
            "load_type": "load_file",
            "load_data": "load_image",
            "format": {".png", ".jpg", ".jpeg", ".gif"},
            "folder": None
        },
        "image_sequence": {
            "load_type": "load_files",
            "load_data": "load_image_sequence",
            "format": {".png", ".jpg", ".jpeg", ".gif"},
            "folder": None,
        },
        "interface": {
            "load_type": "load_rect",
            "load_data": "load_interface",
        },
        "button": {
            "load_type": "load_rect",
            "load_data": "load_button",
        },
    }

    def __init__(self):
        self.resources = {resource_type: {} for resource_type in self.RESOURCE_MAPPING}

    """
    Resource Data Acquisition
        - load_resources
        - load_resource
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
        Load a resource based on its type and specific data.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data for the resource.

        Raises:
            ValueError: If the 'type' field is missing or improperly defined in resource_data.
            ValueError: If the specified resource type is not valid or not supported.
        """
        # Step 1: Get the resource information from RESOURCE_MAPPING
        resource_info = self.get_info(resource_name, resource_data)

        # Step 2: Load the appropriate resource type
        resource_data = resource_info["load_type_function"](resource_name, resource_data, resource_info)

        # Step 3: Load the specific resource data
        resource_info["load_data_function"](resource_name, resource_data, resource_info)

    def get_info(self, resource_name, resource_data):
        # Step 1-1: Get the resource type from resource data
        resource_type = resource_data.get("type")
        if resource_type is None:
            raise ValueError(f"The 'type' field is missing or improperly defined for the resource '{resource_name}'.")

        # Step 1-2: Get the type information from RESOURCE_MAPPING
        type_info = self.RESOURCE_MAPPING.get(resource_type)
        if type_info is None:
            raise ValueError(f"The resource type '{resource_type}' specified for '{resource_name}' is not valid or not supported.")

        # Step 1-3: Get resource folder and supported formats from type_info (if applicable)
        resource_folder = type_info.get("folder", None)
        supported_formats = type_info.get("format", set())

        # Step 1-4: Get the load type function from type_info
        load_type_function_name = type_info.get("load_type")
        load_type_function = getattr(self, load_type_function_name)

        # Step 1-5: Get the load data function from type_info
        load_data_function_name = type_info.get("load_data")
        load_data_function = getattr(self, load_data_function_name)

        # Return all relevant information as a dictionary
        resource_info = {
            "resource_type": resource_type,
            "resource_folder": resource_folder,
            "supported_formats": supported_formats,
            "load_type_function": load_type_function,
            "load_data_function": load_data_function
        }

        return resource_info

    """
    Resource Type Preparation
        - set_resource_folders
        - load_files
        - load_file
        - load_rect
    """
    def set_resource_folders(self, resource_folders):
        """
        Set resource folders for specific resource types.

        Args:
            resource_folders (dict): A dictionary specifying resource folders for specific resource types.

        Raises:
            ValueError: If the specified resource type is invalid.
        """
        for resource_type, folder in resource_folders.items():
            if resource_type in self.RESOURCE_MAPPING:
                self.RESOURCE_MAPPING[resource_type]["folder"] = folder
            else:
                raise ValueError(f"Invalid resource type '{resource_type}'.")

    @staticmethod
    def load_files(resource_name, resource_data, resource_folder, resource_type, supported_formats):
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
    def load_file(resource_name, resource_data, resource_folder, resource_type, supported_formats):
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
    def load_rect(resource_name, resource_data):
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
    Resource Loading Methods
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
        self.resources["music"][name] = music_path

    def load_sound(self, name, data):
        """
        Load a sound effect from the specified data.

        Args:
            name (str): The name to assign to the loaded sound effect.
            data (dict): A dictionary containing sound effect data.
        """
        sound_path = data["file_path"]
        sound = pygame.mixer.Sound(sound_path)
        self.resources["sound"][name] = sound

    def load_font(self, name, data):
        """
        Load a font resource.

        Args:
            name (str): The name of the font resource.
            data (dict): A dictionary containing font resource data.
        """
        font_path = data["file_path"]
        font_size = data.get("size")
        self.resources["font"][name] = pygame.font.Font(font_path, font_size)

    def load_image(self, name, data):
        """
        Load a single image resource from its data.

        Args:
            name (str): The name of the image resource.
            data (dict): A dictionary containing image resource data.
        """
        image_path = data["file_path"]
        data["image"] = pygame.image.load(image_path).convert_alpha()
        self.resources["image"][name] = data

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
        self.resources["image_sequence"][name] = data

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
        self.resources["interface"][name] = data

    def load_button(self, name, data):
        pass

    def load_collision(self, name, data):
        pass
