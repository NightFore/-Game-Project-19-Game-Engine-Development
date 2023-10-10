# error_handler.py

from os import path

"""
Errors
    - GameError
        - ResourceError
            - ResourceNotFoundError
            - ResourceInvalidFormatError
"""
class GameError(Exception):
    """Base class for custom game exceptions."""

class ResourceError(GameError):
    """Base exception class for resource-related errors."""
    DEFAULT_MESSAGES = {
        "not_found": "not found at",
        "invalid_format": "has an unsupported format",
    }

    def __init__(self, resource_type, resource_name, resource_path, error_type):
        default_message = self.DEFAULT_MESSAGES.get(error_type)
        if default_message is None:
            raise ValueError(f"Invalid error type: {error_type}")

        error_message = f"{resource_type.capitalize()} '{resource_name}' {default_message}.\n'{resource_path}'."
        super().__init__(error_message)

class ResourceNotFoundError(ResourceError):
    """Exception raised when a resource is not found."""

class ResourceInvalidFormatError(ResourceError):
    """Exception raised when a resource has an unsupported file format."""



"""
Validation
    - validate_resources
    - validate_resource
"""
def validate_files(file_paths, resource_type, resource_name, supported_formats):
    """
    Validate the file paths and formats of a list of resources.

    Args:
        file_paths (list): List of file paths to validate.
        resource_type (str): The type of the resource.
        resource_name (str): The name of the resource.
        supported_formats (set): The set of supported formats for the resource.
    """
    for file_path in file_paths:
        validate_file(file_path, resource_type, resource_name, supported_formats)

def validate_file(file_path, resource_type, resource_name, supported_formats):
    """
    Validate the file path and format of a single resource.

    Args:
        file_path (str): The path to the resource file.
        resource_type (str): The type of the resource.
        resource_name (str): The name of the resource.
        supported_formats (set): The set of supported formats for the resource.
    """
    if not path.exists(file_path):
        handle_error(ResourceNotFoundError, resource_type, resource_name, file_path)
    if not path.splitext(file_path)[1] in supported_formats:
        handle_error(ResourceInvalidFormatError, resource_type, resource_name, file_path)

"""
Handler
    handle_error
"""
def handle_error(error_type, resource_type, resource_name, file_path):
    """
    Handle a resource loading error.

    Args:
        error_type (Type[Exception]): The type of error to raise.
        resource_type (str): The type of the resource.
        resource_name (str): The name of the resource.
        file_path (str): The path to the resource file.
    """
    error_message = f"Error loading {resource_type} resource '{resource_name}' from '{file_path}'."
    raise error_type(resource_type, resource_name, file_path, error_message)
