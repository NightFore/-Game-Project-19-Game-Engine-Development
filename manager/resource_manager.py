import pygame
from os import path
from handler.error_handler import validate_file

class ResourceManager:
    """
    ResourceManager manages the loading and storage of various game resources such as graphics, audio, fonts, and more.

    Attributes:
        RESOURCE_MAPPING (dict): A dictionary mapping resource types to their respective loading methods and formats.
        resources (dict): A unified dictionary to store resources of different types.

    Example:
        # First, create instances of ResourceManager and others managers such as AudioManager or GraphicManager
        resource_manager = ResourceManager()
        audio_manager = AudioManager()
        graphic_manager = GraphicManager()

        # Set resource folders for specific resource types
        resource_manager.set_resource_folders({
            "music": "music_folder",
            "image": "image_folder"
        })

        # Load resources from a dictionary using the ResourceManager
        resource_dict = {
            "background_music": {
                "type": "music",
                "filename": "bg_music.mp3"
            },
            "player_image": {
                "type": "image",
                "filename": "player.png"
            }
        }
        resource_manager.load_resources(resource_dict)

        # Load resources from ResourceManager into AudioManager and GraphicManager
        audio_manager.musics = resource_manager.load_resources_from_manager("music")
        graphic_manager.images = resource_manager.load_resources_from_manager("image")

    Methods:
    - Resource Acquisition from ResourceManager:
        - load_resources_from_manager(resource_type, loaded_resources=None): Load resources of a specific type from a ResourceManager.

    - Resource Data Acquisition:
        - load_resources(resources_dict): Load multiple resources from a dictionary.
        - load_resource(resource_name, resource_data): Load a resource based on its type using the appropriate loading method.
        - get_info(resource_name): Get information about a specific resource.

    - Resource Type Preparation (load_data):
        - set_resource_folders(resource_folders): Set resource folders for specific resource types.
        - load_path: Load a single file, validate the file, and return the file path if valid.
        - load_file: Load a single file, update the resource data with the file path, and return the updated data.
        - load_files: Load multiple files, update the resource data with a list of file paths, and return the updated data.
        - load_rect: Load an interface rectangle resource from data.

    - Resource Loading Methods (load_type):
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
    Resource Acquisition from ResourceManager
        - load_resources_from_manager
    """
    def load_resources_from_manager(self, resource_type, loaded_resources=None):
        """
        Load resources of a specific type from a ResourceManager.

        Args:
            resource_type (str): The type of resources to load (e.g., 'music', 'sound').
            loaded_resources (dict): A dictionary to store the loaded resources (optional).

        Returns:
            dict: A dictionary containing the loaded resources of the specified type.
        """
        # Create a temporary dictionary to track already loaded resources
        if loaded_resources is None:
            loaded_resources = {}

        # Get the resources of the specified type from the ResourceManager
        resources = self.resources.get(resource_type, {})

        # Iterate through the resources
        for resource_name, resource in resources.items():
            # Check if the resource has not been loaded already to avoid duplicates
            if resource_name not in loaded_resources:
                loaded_resources[resource_name] = resource

        return loaded_resources


    """
    Resource Data Acquisition
        - load_resources_from_manager
        - load_resources
        - load_resource
        - get_info
    """
    def load_resources(self, resources_dict):
        """Load multiple resources from a dictionary.

        Args:
            resources_dict (dict): A dictionary containing resources to load.

        Raises:
            ValueError: If there is an issue with loading any of the resources.
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
        resource_info["load_data_function"](resource_name, resource_data)

    def get_info(self, resource_name, resource_data):
        """
        Get information about a specific resource.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data for the resource.

        Returns:
            dict: A dictionary containing information about the resource, including type, folder, supported formats, load type function, and load data function.
        """
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
    Resource Type Preparation (load_data)
        - set_resource_folders
        - load_path
        - load_file
        - load_files
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
    def load_path(resource_name, file_data, resource_info):
        """
        Load a single file, validate the file, and return the file path if valid.

        Args:
            resource_name (str): The name of the resource.
            file_data (dict): The data of the file to load.
            resource_info (dict): A dictionary containing resource information.

        Returns:
            str: The file path if everything is in order.

        Raises:
            ValueError: If there's an error during resource loading.
        """
        resource_filename = file_data.get("filename")
        resource_folder = resource_info.get("resource_folder")
        resource_type = resource_info.get("resource_type")
        supported_formats = resource_info.get("supported_formats")
        file_path = path.join(resource_folder, resource_filename)

        # Validate the loaded file using the appropriate validation method
        validate_file(file_path, resource_type, resource_name, supported_formats)

        return file_path

    def load_file(self, resource_name, resource_data, resource_info):
        """
        Load a single file, update the resource data with the file path, and return the updated data.
        """
        file_path = self.load_path(resource_name, resource_data, resource_info)
        resource_data["file_path"] = file_path

        return resource_data

    def load_files(self, resource_name, resource_data, resource_info):
        """
        Load multiple files, update the resource data with a list of file paths, and return the updated data.
        """
        files_data = resource_data.get("files")
        file_paths = []

        for file_data in files_data:
            file_path = self.load_path(resource_name, file_data, resource_info)
            file_paths.append(file_path)

        resource_data["file_paths"] = file_paths

        return resource_data

    @staticmethod
    def load_rect(resource_name, resource_data, resource_info):
        """
        Load an interface rectangle resource from data.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data for the resource.
            resource_info (dict): A dictionary containing resource information.

        Returns:
            dict: The updated resource data.
        """
        return resource_data


    """
    Resource Loading Methods (load_type)
        The following methods will update the ResourceManager resources in the appropriate type resource dictionary.
        Common Arguments:
            - name (str): The name of the resource.
            - data (dict): A dictionary containing resource-specific data.

        - AudioManager
            - load_music
            - load_sound
        - FontManager
            - load_font
        - GraphicManager
            - load_image
            - load_image_sequence
            - load_interface
    """
    # AudioManager
    def load_music(self, name, data):
        music_path = data["file_path"]
        pygame.mixer.music.load(music_path)
        self.resources["music"][name] = music_path

    def load_sound(self, name, data):
        sound_path = data["file_path"]
        sound = pygame.mixer.Sound(sound_path)
        self.resources["sound"][name] = sound

    # FontManager
    def load_font(self, name, data):
        font_path = data["file_path"]
        font_size = data.get("size")
        self.resources["font"][name] = pygame.font.Font(font_path, font_size)

    # GraphicManager
    def load_image(self, name, data):
        image_path = data["file_path"]
        data["image"] = pygame.image.load(image_path).convert_alpha()
        self.resources["image"][name] = data

    def load_image_sequence(self, name, data):
        frames = []
        for frame_path in data["file_paths"]:
            frame = pygame.image.load(frame_path).convert_alpha()
            frames.append(frame)
        data["frames"] = frames
        self.resources["image_sequence"][name] = data

    def load_interface(self, name, data):
        self.resources["interface"][name] = data

    def load_button(self, name, data):
        self.resources["button"][name] = data
