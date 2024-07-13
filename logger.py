import logging
import os
import uuid
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

# Dictionary to store unique events with timestamps
unique_events = {}


def setup_logger():
    # Determine the project path
    project_path = os.getcwd()

    # Create logs directory if it doesn't exist in the project path
    logs_dir = os.path.join(project_path, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Generate a unique session ID for this game instance
    session_id = str(uuid.uuid4())

    # Generate log file name based on current timestamp
    log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_file_path = os.path.relpath(os.path.join(logs_dir, log_file_name), project_path)

    # Main logger
    logger = logging.getLogger(session_id)
    logger.setLevel(logging.DEBUG)  # Set overall logging level

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Handler for session-specific log file
    session_handler = RotatingFileHandler(os.path.join(project_path, log_file_path), maxBytes=1024000, backupCount=3)  # Rotate after 1MB
    session_handler.setFormatter(formatter)
    session_handler.setLevel(logging.DEBUG)  # Adjust as needed
    logger.addHandler(session_handler)

    # Handler for console output (optional)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)  # Adjust as needed
    logger.addHandler(console_handler)

    # Log message indicating log file creation
    logger.info(f"Log file created: {log_file_path}")

    return logger


def log_event(logger, event_message):
    current_time = datetime.now()

    # Check if the event has been logged within the last second
    if event_message not in unique_events or (current_time - unique_events[event_message]) > timedelta(seconds=1):
        logger.info(event_message)
        unique_events[event_message] = current_time  # Record the time the event was logged
