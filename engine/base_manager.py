# base_manager.py
import inspect


class BaseManager:
    """
    Base class for all managers.

    Attributes:
        config (dict or None): Configuration dictionary.
        logger (logging.Logger or None): Logger instance.

    Methods:
        Instance Setup:
            - initialize(config, logger): Initialize the manager with configuration and logger.
            - update_config(new_config, check_all_params=False): Update the configuration with new settings.
            - load_components(): Load necessary components based on the configuration.
            - load_specific_components(): Template method to be implemented in subclasses.

        Utility:
            - get_function_name(): Get the name of the current function dynamically.
    """
    def __init__(self):
        self.config = None
        self.logger = None

    """
    Instance Setup:
        - initialize
        - update_config
        - load_components
        - load_specific_components
    """
    def initialize(self, config=None, logger=None):
        """
        Initialize the manager with configuration and logger.

        Args:
            config (dict or None): Configuration dictionary.
            logger (logging.Logger or None): Logger instance.
        """
        # Set the initial configuration and logger
        self.config = config
        self.logger = logger

        # Update configuration with initial settings
        self.update_config(config)

        # Log initialization
        message = f"{self.__class__.__name__} initialized"
        if self.logger:
            self.logger.info(message)
        else:
            print(message)

    def update_config(self, new_config, check_all_params=False):
        """
        Update the configuration with new settings.

        Args:
            new_config (dict): New configuration settings.
            check_all_params (bool): Flag to check if all parameters are present in new_config.
        """
        # Get the class name
        class_name = self.__class__.__name__

        # Log configuration update
        self.logger.info(f"Configuration update for {class_name}...")

        # Get class-specific configuration from new_config
        class_config = new_config.get(class_name)
        if class_config is None:
            message = f"Configuration for {class_name} not found in new_config."
            if self.logger:
                self.logger.error(message)
            else:
                raise ValueError(message)

        # Check for missing parameters if check_all_params is True
        if check_all_params:
            missing_params = [key for key in self.config if key not in class_config]

            # Raise error if any parameters are missing
            if missing_params:
                message = (f"All parameters must be present in the new configuration. "
                           f"Missing parameters: {missing_params}")
                if self.logger:
                    self.logger.error(message)
                else:
                    raise ValueError(message)

        # Update configuration settings
        updated = False
        for key, value in new_config.items():
            if key in self.config and value != self.config[key]:
                # Update the configuration value
                self.config[key] = value
                updated = True

                # Log the updated configuration value
                message = f"\t{key} = {repr(value)}"
                if self.logger:
                    self.logger.debug(message)
                else:
                    print(message)

        # Perform actions if configuration was updated
        if updated:
            # Load components after configuration update
            self.load_components()

            # Log completion of configuration update
            message = f"Configuration update for {class_name} completed."
            if self.logger:
                self.logger.info(message)
            else:
                print(message)
        else:
            # Log no configuration update detected
            message = f"No configuration update detected for {class_name}."
            if self.logger:
                self.logger.info(message)
            else:
                print(message)

    def load_components(self):
        """
        Load necessary components based on the configuration.
        """
        # Get the class name
        class_name = self.__class__.__name__

        # Log loading components
        self.logger.info(f"Loading components for {class_name}...")

        try:
            # Call the subclass-specific method to load components
            self.load_specific_components()

            # Log completion of component loading
            message = f"Loading components for {class_name} completed."
            if self.logger:
                self.logger.info(message)
            else:
                print(message)
        except Exception as e:
            # Log error if component loading fails
            message = f"Error loading components for {class_name}: {e}"
            if self.logger:
                self.logger.error(message)
            else:
                raise message

    def load_specific_components(self):
        """
        Template method to be implemented in subclasses.
        """
        # Log that the method should be implemented in subclasses
        message = f"Subclasses should implement {self.get_function_name()} method."
        if self.logger:
            self.logger.error(message)
        else:
            raise NotImplementedError(message)

    """
    Utility:
        - get_function_name
    """
    @staticmethod
    def get_function_name():
        """
        Get the name of the current function dynamically.
        """
        # Use inspect module to get the current function name
        frame = inspect.currentframe().f_back
        return frame.f_code.co_name
