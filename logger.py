import logging
import os
import uuid
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta


class GameLogger:
    def __init__(self):
        # Determine the project path
        self.project_path = os.getcwd()

        # Create logs directory if it doesn't exist in the project path
        self.logs_dir = os.path.join(self.project_path, 'logs')
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        # Generate a unique session ID for this game instance
        self.session_id = str(uuid.uuid4())

        # Generate log file name based on current timestamp
        log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
        self.log_file_path = os.path.relpath(os.path.join(self.logs_dir, log_file_name), self.project_path)

        # Initialize logger
        self.logger = logging.getLogger(self.session_id)
        self.logger.setLevel(logging.DEBUG)  # Set overall logging level

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

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def event(self, event_message):
        current_time = datetime.now()

        # Check if the event has been logged within the last second
        if event_message not in self.unique_events or (current_time - self.unique_events[event_message]) > timedelta(
                seconds=1):
            self.logger.info(event_message)
            self.unique_events[event_message] = current_time  # Record the time the event was logged

    def get_session_id(self):
        return self.session_id
