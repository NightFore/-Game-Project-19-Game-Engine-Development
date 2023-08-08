# resource_manager.py

from os import path
from error_manager import ResourceNotFoundError, ResourceInvalidFormatError, handle_error

"""
Resource Loading
    - load_resources
    - load_resource
"""
def load_resources(manager, resources_dict):
    """Load multiple resources from a dictionary."""
    for resource_name, resource_data in resources_dict.items():
        load_resource(manager, resource_name, resource_data)

def load_resource(manager, resource_name, resource_data):
    """
    Load a resource based on its type using the appropriate loading method.

    Args:
        manager (ResourceManager): The resource manager instance.
        resource_name (str): The name of the resource.
        resource_data (dict): The data for the resource.
    """
    resource_type = resource_data.get("type")

    if resource_type is not None:
        resource_info = manager.RESOURCE_MAPPING.get(resource_type, {})
        load_method_name = resource_info.get("load")
        load_method = getattr(manager, load_method_name)

        resource_folder = resource_info.get("folder")
        supported_formats = resource_info.get("format")

        if "files" not in resource_data:
            # Load a single resource
            resource_filename = resource_data.get("filename")
            file_path = path.join(resource_folder, resource_filename)
            validate_resource(file_path, resource_type, resource_name, supported_formats)
            resource_data["file_path"] = file_path
        else:
            # Load multiple resources
            resources_data = resource_data.get("files")
            file_paths = [path.join(resource_folder, file_data["filename"]) for file_data in resources_data]
            validate_resources(file_paths, resource_type, resource_name, supported_formats)
            resource_data["file_paths"] = file_paths

        # Call the appropriate load method
        load_method(resource_name, resource_data)
    else:
        raise ValueError("Resource type not specified")

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
