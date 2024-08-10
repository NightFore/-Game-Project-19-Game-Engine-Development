# base_manager.py
import inspect
import logging


class BaseManager:
    """
    Base class for all managers.

    Attributes:
        Common Attributes:
            - config (dict or None): Configuration dictionary.
            - managers (dict or None): Dictionary of manager instances.
            - logger (logging.Logger or None): Logger instance.
            - class_name (str): Name of the class.

        Specific Manager References:
            - main_manager (object or None): Reference to the main manager instance.
            - audio_manager (object or None): Reference to the audio manager instance.
            - window_manager (object or None): Reference to the window manager instance.

    Methods:
        Instance Setup:
            - initialize(config, managers=None, logger=None): Initialize the manager.
            - update_config(new_config, check_all_params=False): Update the configuration with new settings.
            - load_components(): Load necessary components based on the configuration.
            - load_specific_components(): Template method to be implemented in subclasses.

        Utility:
            - get_function_name(): Get the name of the current function dynamically.
            - log_debug(message): Log a message at DEBUG level.
            - log_info(message): Log a message at INFO level.
            - log_warning(message): Log a message at WARNING level.
            - log_error(message): Log a message at ERROR level and optionally raise an exception.
            - log_critical(message): Log a message at CRITICAL level and optionally raise an exception.
    """
    def __init__(self):
        # Common Attributes
        self.config = None
        self.managers = None
        self.logger = None
        self.class_name = None

        # Specific Manager References
        self.main_manager = None
        self.audio_manager = None
        self.window_manager = None

    """
    Instance Setup:
        - initialize
        - update_config
        - load_components
        - load_specific_components
    """
    def initialize(self, config, managers=None, logger=None):
        """
        Initialize the manager.

        Args:
            config (dict): Configuration dictionary.
            managers (dict or None): Dictionary of manager instances.
            logger (logging.Logger or None): Logger instance.
        """
        # Get the class name
        self.class_name = self.__class__.__name__

        # Set the logger
        self.logger = logger

        # Set up references to managers
        if managers:
            self.managers = managers
            self.main_manager = self.managers['main_manager']
            self.audio_manager = self.managers['audio_manager']
            self.window_manager = self.managers['window_manager']

        # Set the initial configuration
        self.update_config(config)

        # Log initialization
        self.log_info(f"{self.class_name} initialized.")

    def update_config(self, new_config, check_all_params=False):
        """
        Update the configuration with new settings.

        Args:
            new_config (dict): New configuration settings.
            check_all_params (bool): Flag to check if all parameters are present in new_config.
        """

        # Log configuration update
        self.log_info(f"Configuration update for {self.class_name}...")

        # Check if self.config is None
        if self.config is None:
            self.log_error(f"Configuration for {self.class_name} is not initialized.",
                           ValueError)

        # Get class-specific configuration from new_config
        class_config = new_config.get(self.class_name)
        if class_config is None:
            self.log_error(f"Configuration for {self.class_name} not found in new_config.",
                           ValueError)

        # Check for missing parameters if check_all_params is True
        if check_all_params:
            missing_params = [key for key in self.config if key not in class_config]

            # Raise error if any parameters are missing
            if missing_params:
                self.log_error(f"All parameters must be present in the new configuration. "
                               f"Missing parameters: {missing_params}",
                               ValueError)

        # Update configuration settings
        updated = False
        for key, value in class_config.items():
            if key in self.config and value != self.config[key]:
                updated = True
                old_value = self.config[key]
                self.config[key] = value
                self.log_debug(f"Updated {key}: {repr(old_value)} -> {repr(value)}")

        # Load components after configuration update
        if updated:
            self.load_components()
            self.log_info(f"Configuration update for {self.class_name} completed.")
        else:
            self.log_info(f"No configuration update detected for {self.class_name}.")

    def load_components(self):
        """
        Load necessary components based on the configuration.
        """
        self.log_info(f"Loading components for {self.class_name}...")

        try:
            # Call the subclass-specific method to load components
            self.load_specific_components()
            self.log_info(f"Loading components for {self.class_name} completed.")
        except Exception as e:
            self.log_error(f"Error loading components for {self.class_name}: {e}",
                           RuntimeError)

    def load_specific_components(self):
        """
        Template method to be implemented in subclasses.
        """
        # Log that the method should be implemented in subclasses
        self.log_error(f"Subclasses should implement {self.get_function_name()} method.",
                       NotImplementedError)

    """
    Utility:
        - get_function_name
        - log_debug
        - log_info
        - log_warning
        - log_error
        - log_critical
    """
    @staticmethod
    def get_function_name():
        """
        Get the name of the current function dynamically.
        """
        # Use inspect module to get the current function name
        frame = inspect.currentframe().f_back
        return frame.f_code.co_name

    def log_debug(self, message):
        """
        Log a message at DEBUG level.

        Args:
            message (str): Message to be logged.
        """
        if self.logger:
            self.logger.log_debug(message)
        else:
            print(message)

    def log_info(self, message):
        """
        Log a message at INFO level.

        Args:
            message (str): Message to be logged.
        """
        if self.logger:
            self.logger.log_info(message)
        else:
            print(message)

    def log_warning(self, message):
        """
        Log a message at WARNING level.

        Args:
            message (str): Message to be logged.
        """
        if self.logger:
            self.logger.log_warning(message)
        else:
            print(message)

    def log_error(self, message, exception=None):
        """
        Log a message at ERROR level and optionally raise an exception.

        Args:
            message (str): Message to be logged.
            exception (type or None): Exception class to raise (default: None).
        """
        if self.logger:
            self.logger.log_error(message, exception)
        else:
            print(message)

    def log_critical(self, message, exception=None):
        """
        Log a message at CRITICAL level and optionally raise an exception.

        Args:
            message (str): Message to be logged.
            exception (type or None): Exception class to raise (default: None).
        """
        if self.logger:
            self.logger.log_critical(message, exception)
        else:
            print(message)
