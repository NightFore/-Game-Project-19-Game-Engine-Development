import logging
import os
import uuid
import inspect
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta


class Logger:
    """
    Logger manages logging for the application.

    Attributes:
        Project Attributes:
            - project_path (str): The path to the project directory.
            - logs_dir (str): Path to the logs directory within the project.

        Logging Attributes:
            - session_id (str): Unique session ID for the current logging instance.
            - log_file_path (str): Path to the current log file.
            - logger (logging.Logger): Logger instance for handling log messages.
            - event_time_threshold (timedelta): Time threshold for event logging.

        Event Tracking Attributes:
            - unique_events (dict): Dictionary to store unique events with timestamps.

    Methods:
        Logging Methods:
            - debug: Log a message at DEBUG level.
            - info: Log a message at INFO level.
            - warning: Log a message at WARNING level.
            - error: Log a message at ERROR level.
            - critical: Log a message at CRITICAL level.
            - event: Log a unique event message with context.

        Helper Methods:
            - log_message: Log a message at a specified logging level.
            - should_log_event: Determine whether an event should be logged based on uniqueness and time threshold.
            - get_calling_class_name: Retrieve the name of the calling class.
            - get_session_id: Retrieve the session ID associated with the logger.
    """
    def __init__(self):
        """
        Initialize the Logger instance.
        """
        # Determine the project path
        self.project_path = os.getcwd()

        # Create logs directory if it doesn't exist in the project path
        self.logs_dir = os.path.join(self.project_path, 'logs')
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        # Generate a unique session ID for this instance
        self.session_id = str(uuid.uuid4())

        # Generate log file name based on current timestamp
        log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
        self.log_file_path = os.path.relpath(os.path.join(self.logs_dir, log_file_name), self.project_path)

        # Initialize logger
        self.logger = logging.getLogger(self.session_id)
        self.logger.setLevel(logging.DEBUG)  # Set overall logging level

        # Define a time threshold for event logging
        self.event_time_threshold = timedelta(seconds=1)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Handler for session-specific log file
        session_handler = RotatingFileHandler(self.log_file_path, maxBytes=1024000)  # Rotate after 1MB
        session_handler.setFormatter(formatter)
        session_handler.setLevel(logging.DEBUG)  # Adjust as needed
        self.logger.addHandler(session_handler)

        # Handler for console output (optional)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)  # Adjust as needed
        self.logger.addHandler(console_handler)

        # Log message indicating log file creation
        self.logger.info(f"Log file created: {self.log_file_path}")

        # Dictionary to store unique events with timestamps
        self.unique_events = {}

    """
    Logging Methods
        - debug
        - info
        - warning
        - error
        - critical
        - event
    """
    def debug(self, message):
        """
        Log a message at DEBUG level.

        Args:
            message (str): Message to be logged.
        """
        self.log_message(logging.DEBUG, message)

    def info(self, message):
        """
        Log a message at INFO level.

        Args:
            message (str): Message to be logged.
        """
        self.log_message(logging.INFO, message)

    def warning(self, message):
        """
        Log a message at WARNING level.

        Args:
            message (str): Message to be logged.
        """
        self.log_message(logging.WARNING, message)

    def error(self, message):
        """
        Log a message at ERROR level.

        Args:
            message (str): Message to be logged.
        """
        self.log_message(logging.ERROR, message)

    def critical(self, message):
        """
        Log a message at CRITICAL level.

        Args:
            message (str): Message to be logged.
        """
        self.log_message(logging.CRITICAL, message)

    def event(self, event_message):
        """
        Log a unique event message with context.

        Args:
            event_message (str): Event message to be logged.
        """
        if self.should_log_event(event_message):
            calling_class = self.get_calling_class_name()
            self.logger.info(f"{calling_class} - {event_message}")
            self.unique_events[event_message] = datetime.now()

    """
    Helper Methods
        - log_message
        - get_calling_class_name
        - get_session_id
    """
    def log_message(self, level, message):
        """
        Log a message at a specified logging level with the calling class context.

        Args:
            level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
            message (str): Message to be logged.
        """
        calling_class = self.get_calling_class_name()
        self.logger.log(level, f"{calling_class} - {message}")

    def should_log_event(self, event_message):
        """
        Determine whether an event should be logged based on uniqueness and time threshold.

        Args:
            event_message (str): The event message to be logged.

        Returns:
            bool: True if the event should be logged, False otherwise.
        """
        current_time = datetime.now()
        time_since_last_event = current_time - self.unique_events.get(event_message, datetime.min)

        if event_message not in self.unique_events or time_since_last_event > self.event_time_threshold:
            return True
        else:
            return False

    @staticmethod
    def get_calling_class_name():
        """
        Retrieve the name of the calling class in the call stack.

        Returns:
            str: Name of the calling class if found, otherwise 'Unknown'.
        """
        frame = inspect.currentframe().f_back
        while frame:
            caller_class = frame.f_locals.get('self', None)
            if caller_class is not None and not isinstance(caller_class, Logger):
                return type(caller_class).__name__
            frame = frame.f_back
        return 'Unknown'

    def get_session_id(self):
        """
        Retrieve the session ID associated with the logger.

        Returns:
            str: Session ID.
        """
        return self.session_id
