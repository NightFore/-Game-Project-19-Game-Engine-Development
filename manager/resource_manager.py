# resource_manager.py

import pygame
from os import path
from manager.template_manager import TemplateManager

class ResourceManager(TemplateManager):
    """
    ResourceManager manages the loading and storage of various game resources.

    Attributes:
        RESOURCE_MAPPING (dict): A dictionary mapping resource types to their respective loading methods and formats.
        resources (dict): A unified dictionary to store resources of different types.

    Methods:
    - Setup
        - set_resource_folders: Set resource folders for specific resource types.

    - Resource Acquisition
        - load_resources: Load multiple resources from a dictionary.
        - load_resource: Load a resource based on its type and specific data.
        - get_info: Get information about a specific resource.

    - Resource Type Preparation (load_data)
        - load_files: Load multiple files, update the resource data with a list of file paths, and return the updated data.
        - load_file: Load a single file, update the resource data with the file path, and return the updated data.
        - load_path: Load a single file, validate the file, and return the file path if valid.

    - Resource Loading Methods (load_type)
        - load_music: Load music and return the path to the loaded music file.
        - load_sound: Load a sound and return the loaded sound object.
        - load_font: Load a font and return a Font object.
        - load_image: Load an image and return the data with the loaded image.
        - load_image_sequence: Load an image sequence and return the data with the loaded images.

    - Validation
        - validate_file: Validate a file's path and format for a specific resource.
    """
    RESOURCE_MAPPING = {
        # AudioManager
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
        # GraphicManager
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
        # TextManager
        "font": {
            "load_type": "load_file",
            "load_data": "load_font",
            "format": {".ttf"},
            "folder": None
        },
        # ButtonManager
        "button": {
            "load_type": None,
            "load_data": None,
        },
        # SceneManager
        "scene": {
            "load_type": None,
            "load_data": None,
        },
    }

    def __init__(self):
        # Initialize the manager as a subclass of TemplateManager
        super().__init__()

        # Initialize manager-related attributes
        self.resources = {resource_type: {} for resource_type in self.RESOURCE_MAPPING}


    """
    Setup
        - set_resource_folders
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


    """
    Resource Acquisition
        - load_resources
        - load_resource
        - get_info
    """
    def load_resources(self, resources_dict):
        """
        Load multiple resources from a dictionary.

        Args:
            resources_dict (dict): A dictionary containing resources to load.

        Raises:
            KeyError: If a resource with the same name already exists in self.resources.
        """
        for resource_type, resource_type_data in resources_dict.items():
            for resource_name, resource_data in resource_type_data.items():
                if resource_name in self.resources:
                    raise KeyError(f"Resource with name '{resource_name}' already exists in self.resources.")
                self.load_resource(resource_type, resource_name, resource_data)

    def load_resource(self, resource_type, resource_name, resource_data):
        """
        Load a resource based on its type and specific data.

        Args:
            resource_type (str): The type of the resource.
            resource_name (str): The name of the resource.
            resource_data (dict): The data for the resource.
        """
        # Step 1: Get the resource information from RESOURCE_MAPPING
        resource_info = self.get_info(resource_type)

        # Step 2: Load depending on the resource type
        load_type_function = resource_info["load_type_function"]
        if load_type_function is not None:
            resource_data = load_type_function(resource_name, resource_data, resource_info)

        # Step 3: Load depending on the resource data
        load_data_function = resource_info["load_data_function"]
        if load_data_function is not None:
            resource_data = load_data_function(resource_data)

        self.resources[resource_type][resource_name] = resource_data

    def get_info(self, resource_type):
        """
        Get information about a specific resource.

        Args:
            resource_type (str): The type of the resource.

        Returns:
            dict: A dictionary containing information about the resource, including type, folder, supported formats, load type function, and load data function.
        """
        # Step 1-1: Get the type information from RESOURCE_MAPPING
        type_info = self.RESOURCE_MAPPING.get(resource_type)
        if type_info is None:
            raise ValueError(f"Resource type '{resource_type}' does not exist in RESOURCE_MAPPING")

        # Step 1-2: Get resource folder and supported formats from type_info (if applicable)
        resource_folder = type_info.get("folder", None)
        supported_formats = type_info.get("format", set())

        # Step 1-3: Get the load type function from type_info
        load_type_function_name = type_info.get("load_type")
        if load_type_function_name is not None:
            load_type_function = getattr(self, load_type_function_name)
        else:
            load_type_function = None

        # Step 1-4: Get the load data function from type_info
        load_data_function_name = type_info.get("load_data")
        if load_data_function_name is not None:
            load_data_function = getattr(self, load_data_function_name)
        else:
            load_data_function = None

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
    Resource Type Loading (load_type)
        - load_files
        - load_file
        - load_path
    """
    def load_files(self, resource_name, resource_data, resource_info):
        """
        Load multiple files, update the resource data with a list of file paths, and return the updated data.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data of the files to load.
            resource_info (dict): A dictionary containing resource information.

        Returns:
            dict: The updated resource data with the "file_paths" field.
        """
        # Get the list of files to load from the resource data
        files_data = resource_data.get("files")
        file_paths = []

        # Load each file and collect their file paths
        for file_data in files_data:
            file_path = self.load_path(resource_name, file_data, resource_info)
            file_paths.append(file_path)

        # Update the resource data with the list of file paths
        resource_data["file_paths"] = file_paths

        return resource_data

    def load_file(self, resource_name, resource_data, resource_info):
        """
        Load a single file, update the resource data with the file path, and return the updated data.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data of the file to load.
            resource_info (dict): A dictionary containing resource information.

        Returns:
            dict: The updated resource data with the "file_path" field.
        """
        # Load the file and get the file path
        file_path = self.load_path(resource_name, resource_data, resource_info)

        # Update the resource data with the file path
        resource_data["file_path"] = file_path

        return resource_data

    def load_path(self, resource_name, resource_data, resource_info):
        """
        Load a single file, validate the file, and return the file path if valid.

        Args:
            resource_name (str): The name of the resource.
            resource_data (dict): The data of the file to load.
            resource_info (dict): A dictionary containing resource information.

        Returns:
            str: The file path of the loaded resource if it is valid.
        """
        # Extract resource details
        resource_filename = resource_data.get("filename")
        resource_folder = resource_info.get("resource_folder")
        resource_type = resource_info.get("resource_type")
        supported_formats = resource_info.get("supported_formats")
        file_path = path.join(resource_folder, resource_filename)

        # Validate the loaded file
        self.validate_file(file_path, resource_type, resource_name, supported_formats)

        return file_path


    """
    Resource Data Loading (load_data)
        - AudioManager
            - load_music
            - load_sound
        - FontManager
            - load_font
        - GraphicManager
            - load_image
            - load_image_sequence
    """
    # AudioManager
    def load_music(self, data):
        """
        Load music and return the path to the loaded music file.
        """
        music_path = data["file_path"]
        pygame.mixer.music.load(music_path)
        return music_path

    def load_sound(self, data):
        """
        Load a sound and return the loaded sound object.
        """
        sound_path = data["file_path"]
        return pygame.mixer.Sound(sound_path)

    # FontManager
    def load_font(self, data):
        """
        Load a font and return a Font object.
        """
        font_path = data["file_path"]
        font_size = data["size"]
        data["font"] = pygame.font.Font(font_path, font_size)
        return data

    # GraphicManager
    def load_image(self, data):
        """
        Load an image and return the data with the loaded image.
        """
        image_path = data["file_path"]
        data["image"] = pygame.image.load(image_path).convert_alpha()
        return data

    def load_image_sequence(self, data):
        """
        Load an image sequence and return the data with the loaded images.
        """
        images = []
        for image_path in data["file_paths"]:
            image = pygame.image.load(image_path).convert_alpha()
            images.append(image)
        data["images"] = images
        return data


    """
    Validation
        - validate_file
    """
    @staticmethod
    def validate_file(file_path, resource_type, resource_name, supported_formats):
        """
        Validate a file's path and format for a specific resource.

        Args:
            file_path (str): The path to the file to be validated.
            resource_type (str): The type of the resource.
            resource_name (str): The name of the resource.
            supported_formats (set): A set of supported file formats (extensions).

        Raises:
            ValueError: If the file path does not exist.
            ValueError: If the file format is not supported for the specified resource.
        """
        # Check if the file exists
        if not path.exists(file_path):
            raise ValueError(f"File path '{file_path}' for resource '{resource_name}' does not exist.")

        # Check if the file format (extension) is supported
        file_extension = path.splitext(file_path)[-1].lower()
        if file_extension not in supported_formats:
            raise ValueError(f"File format '{file_extension}' is not supported for resource '{resource_name}' of type '{resource_type}'.")
