# logger.py

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
            - log_debug(message): Log a message at DEBUG level.
            - log_info(message): Log a message at INFO level.
            - log_warning(message): Log a message at WARNING level.
            - log_error(message, exception=None): Log a message at ERROR level and optionally raise an exception.
            - log_critical(message, exception=None): Log a message at CRITICAL level and optionally raise an exception.
            - log_event(message): Log a unique event message with context.

        Helper Methods:
            - log_message(level, message): Log a message at a specified logging level.
            - should_log_event(message): Determine whether an event should be logged.
            - get_calling_class_name(): Retrieve the name of the calling class.
            - get_session_id(): Retrieve the session ID associated with the logger.
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

        # Handler for session-specific log file (Rotate after 1MB)
        session_handler = RotatingFileHandler(self.log_file_path, maxBytes=1024000, encoding='utf-8')
        session_handler.setFormatter(formatter)
        session_handler.setLevel(logging.DEBUG)  # Adjust as needed
        self.logger.addHandler(session_handler)

        # Handler for console output (optional)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.encoding = 'utf-8'
        console_handler.setLevel(logging.DEBUG)  # Adjust as needed
        self.logger.addHandler(console_handler)

        # Log message indicating log file creation
        self.log_info(f"Log file created: {self.log_file_path}")

        # Dictionary to store unique events with timestamps
        self.unique_events = {}

    """
    Logging Methods
        - log_debug
        - log_info
        - log_warning
        - log_error
        - log_critical
        - log_event
    """
    def log_debug(self, message):
        """
        Log a message at DEBUG level.

        Args:
            message (str): Message to be logged.
        """
        self.log_message(logging.DEBUG, message)

    def log_info(self, message):
        """
        Log a message at INFO level.

        Args:
            message (str): Message to be logged.
        """
        self.log_message(logging.INFO, message)

    def log_warning(self, message):
        """
        Log a message at WARNING level.

        Args:
            message (str): Message to be logged.
        """
        self.log_message(logging.WARNING, message)

    def log_error(self, message, exception=None):
        """
        Log a message at ERROR level and raise .

        Args:
            message (str): Message to be logged.
            exception (type or None): Exception class to raise (default: None).
        """
        self.log_message(logging.ERROR, message)

        if exception:
            raise exception(message)

    def log_critical(self, message, exception=None):
        """
        Log a message at CRITICAL level and optionally raise an exception.

        Args:
            message (str): Message to be logged.
            exception (type or None): Exception class to raise (default: None).
        """
        self.log_message(logging.CRITICAL, message)

        if exception:
            raise exception(message)

    def log_event(self, event_message):
        """
        Log a unique event message with context.

        Args:
            event_message (str): Event message to be logged.
        """
        if self.should_log_event(event_message):
            calling_class = self.get_calling_class_name()
            self.log_info(f"{calling_class} - {event_message}")
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

    def should_log_event(self, message):
        """
        Determine whether an event should be logged.

        Args:
            message (str): Message to be logged.

        Returns:
            bool: True if the event should be logged, False otherwise.
        """
        current_time = datetime.now()
        time_since_last_event = current_time - self.unique_events.get(message, datetime.min)

        if message not in self.unique_events or time_since_last_event > self.event_time_threshold:
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
