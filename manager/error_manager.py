class GameError(Exception):
    """Base class for custom game exceptions."""
    pass

class ResourceNotFoundError(GameError):
    """Exception raised when a resource is not found."""
    def __init__(self, resource_name, resource_path):
        error_message = f"\nImage '{resource_name}' not found at\n'{resource_path}'."
        super().__init__(error_message)

class InvalidImageFormatError(GameError):
    """Exception raised when an image has an unsupported file format."""
    def __init__(self, image_name):
        error_message = f"\nImage '{image_name}' has an unsupported format."
        super().__init__(error_message)

class ResourceLoadError(GameError):
    """Exception raised when an error occurs during resource loading."""
    def __init__(self, resource_name, message):
        self.resource_name = resource_name
        self.message = message
        super().__init__(f"Unable to load resource '{resource_name}': {message}")

# Error handling function
def handle_error(error_class, message):
    """Raise an exception with the specified error type and an error message."""
    raise error_class(message)
