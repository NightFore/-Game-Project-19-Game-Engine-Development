from button import Button
from button_config import button_config


class UIManager:
    def __init__(self, font, screen, managers):
        """
        Initialize UIManager with font, screen, and managers.

        Args:
            font: Font object for rendering text.
            screen: Surface object for rendering UI.
            managers: Dictionary of manager instances.
        """
        self.font = font
        self.screen = screen
        self.managers = managers
        self.main_manager = self.managers['main_manager']
        self.audio_manager = self.managers['audio_manager']
        self.window_manager = self.managers['window_manager']
        self.buttons = []
        self.current_menu = None

    def load_menu(self, menu_name):
        """
        Load a menu from configuration.

        Args:
            menu_name: Name of the menu to load.
        """
        self.current_menu = menu_name
        self.buttons = []

        if menu_name in button_config:
            for button_id, config in button_config[menu_name].items():
                x = config['x']
                y = config['y']
                width = config['width']
                height = config['height']
                label = config['label']
                color = config['color']
                action_str = config.get('action')
                action = self.resolve_action(action_str)

                button = Button(x, y, width, height, label, color, self.font, action)
                self.buttons.append(button)

    def resolve_action(self, action_str):
        """
        Resolve action string to a callable function with arguments.

        Args:
            action_str: String representing the action to resolve.

        Returns:
            Callable function corresponding to the action string with arguments.
        """
        if not action_str:
            return None

        try:
            # Extract method and arguments from action_str
            action_parts = action_str.split('(', 1)
            method_str = action_parts[0].strip()
            args_str = action_parts[1][:-1] if len(action_parts) > 1 else ''  # Remove trailing ')'

            # Parse arguments
            args = self.parse_arguments(args_str)

            # Handle nested method calls
            method_parts = method_str.split('.')
            if len(method_parts) > 1:
                # Method is in a nested manager
                obj = self
                for part in method_parts[:-1]:
                    obj = getattr(obj, part, None)
                    if obj is None:
                        raise AttributeError(f"Manager or method '{'.'.join(method_parts[:-1])}' not found.")
                method_name = method_parts[-1]
                if hasattr(obj, method_name):
                    method = getattr(obj, method_name)
                    return lambda: method(*args)
            else:
                # Direct method on UIManager
                if hasattr(self, method_str):
                    method = getattr(self, method_str)
                    return lambda: method(*args)
        except Exception as e:
            print(f"Error resolving action '{action_str}': {e}")

        return None

    def parse_arguments(self, args_str):
        """
        Parse a string of arguments into a tuple of arguments.

        Args:
            args_str: String representing arguments in the format 'arg1, arg2, ...'

        Returns:
            Tuple of parsed arguments.
        """
        import ast

        # Convert the arguments string to a tuple of arguments
        try:
            args = ast.literal_eval(f"({args_str})")
            return args if isinstance(args, tuple) else (args,)
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing arguments '{args_str}': {e}")
            return ()

    def draw(self):
        """
        Draw all buttons in the current menu.
        """
        for button in self.buttons:
            button.draw(self.screen)

    def handle_events(self, events, mouse_pos, mouse_clicks):
        """
        Handle button clicks.

        Args:
            events: List of pygame events.
            mouse_pos: Current position of the mouse.
            mouse_clicks: List of mouse click states.
        """
        for button in self.buttons:
            if button.is_hovered(mouse_pos) and mouse_clicks[1]:
                button.click()

    def start_game(self):
        """
        Switch to the main menu.
        """
        self.load_menu('main_menu')
