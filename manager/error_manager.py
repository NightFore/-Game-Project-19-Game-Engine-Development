class GameError(Exception):
    """Base class for custom game exceptions."""
    pass

class ResourceNotFoundError(GameError):
    """Exception raised when a resource is not found."""
    DEFAULT_MESSAGE = "not found at"

    def __init__(self, resource_type, resource_name, resource_path):
        error_message = f"\n{resource_type.capitalize()} '{resource_name}' {self.DEFAULT_MESSAGE}\n'{resource_path}'."
        super().__init__(error_message)

class ResourceInvalidFormatError(GameError):
    """Exception raised when a resource has an unsupported file format."""
    DEFAULT_MESSAGE = "has an unsupported format"

    def __init__(self, resource_type, resource_name):
        error_message = f"\n{resource_type.capitalize()} '{resource_name}' {self.DEFAULT_MESSAGE}."
        super().__init__(error_message)

class ResourceLoadError(GameError):
    """Exception raised when an error occurs during resource loading."""
    def __init__(self, resource_type, resource_name, message):
        super().__init__(f"Unable to load {resource_type} '{resource_name}': {message}")

# Error handling function
def handle_error(error_class, type, resource_name, details=None):
    """Raise an exception with the specified error type and an error message."""
    if details:
        raise error_class(type, resource_name, details)
    else:
        raise error_class(type, resource_name)
