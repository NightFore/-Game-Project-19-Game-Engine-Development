# utils.py

def setup_managers(instance, managers):
    """
    Set up references to managers for the given instance.

    Args:
        instance: The object instance to set up managers for.
        managers (dict): Dictionary of manager instances.
    """
    if managers:
        instance.managers = managers
        instance.main_manager = managers.get('main_manager')
        instance.audio_manager = managers.get('audio_manager')
        instance.window_manager = managers.get('window_manager')
        instance.ui_manager = managers.get('ui_manager')
        # Add more managers as needed

