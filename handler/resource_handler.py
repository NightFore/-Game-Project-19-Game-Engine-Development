# resource_manager.py

from os import path
from handler.error_handler import ResourceNotFoundError, ResourceInvalidFormatError, handle_error

"""
Validators
    - validate_resources
    - validate_resource
"""
def validate_resources(file_paths, resource_type, resource_name, supported_formats):
    """
    Validate the file paths and formats of a list of resources.
    """
    for file_path in file_paths:
        validate_resource(file_path, resource_type, resource_name, supported_formats)

def validate_resource(file_path, resource_type, resource_name, supported_formats):
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
