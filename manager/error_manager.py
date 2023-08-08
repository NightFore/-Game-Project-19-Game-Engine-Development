# error_manager.py

class GameError(Exception):
    """Base class for custom game exceptions."""
    pass

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
    def __init__(self, resource_type, resource_name, resource_path):
        super().__init__(resource_type, resource_name, resource_path, "not_found")

class ResourceInvalidFormatError(ResourceError):
    """Exception raised when a resource has an unsupported file format."""
    def __init__(self, resource_type, resource_name, resource_path):
        super().__init__(resource_type, resource_name, resource_path, "invalid_format")

# Error handling function
def handle_error(error_class, type, resource_name, details=None):
    """Raise an exception with the specified error type and an error message."""
    if details:
        raise error_class(type, resource_name, details)
    else:
        raise error_class(type, resource_name)
