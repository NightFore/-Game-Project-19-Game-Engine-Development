# resource_data.py

DICT_RESOURCES = {
    # AudioManager
    "music": {
        "debug_music": {"filename": "debug_audio_music.mp3"},
    },
    "sound": {
        "debug_sound": {"filename": "debug_audio_sound.wav"},
    },

    # GraphicManager
    "image": {
        "default_single": {"filename": "debug_graphic_manager_single.png"},
    },
    "image_sequence": {
        "default_sequence": {
            "files": [{"filename": "debug_graphic_manager_sequence_1.png"},
                      {"filename": "debug_graphic_manager_sequence_2.png"}],
            "image_duration": 1,
        },
    },
    "interface": {
        "default_interface": {
            "color": {"default": (0, 0, 0), "border": (255, 255, 255)},
            "rect": (50, 50, 400, 300), "hit_rect": (50, 50, 400, 300), "border_radius": 2
        },
    },
    "button": {
        "default_button": {"color": {"active": (0, 255, 0), "inactive": (255, 0, 0), "border": (0, 0, 255)}, "border_radius": 5},
    },

    # TextManager
    "font": {
        "liberation_serif": {"filename": "LiberationSerif-Regular.ttf", "size": 24, "color": (255, 255, 255)},
    },

    # SceneManager
    "scene": {
        "MainMenuScene": {
            "buttons": {
                "start": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "rect": (640, 250, 300, 60), "text": "Start", "align": "center"},
                "settings": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "rect": (640, 320, 300, 60), "text": "Settings", "align": "center"},
                "debug_audio": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "rect": (640, 390, 300, 60), "text": "Debug Audio", "align": "center"},
                "pause_music": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "rect": (640, 460, 300, 60), "text": "Pause Music", "align": "center"},
                "toggle_music": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "rect": (640, 530, 300, 60), "text": "Toggle Music", "align": "center"},
                "toggle_zoom": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "rect": (640, 600, 300, 60), "text": "Toggle Zoom", "align": "center"},
                "quit_game": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "rect": (10, 10, 50, 50), "text": "X"},
            },
            "texts": [
                {"font": "liberation_serif", "position": (600, 300), "text": "Hello World!"},
                {"font": "liberation_serif", "position": (600, 360), "text": "Hello World 2!"},
            ],
        },
        "GameScene": {
            "buttons": {
                "game_over": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "text": "Game Over", "rect": (400, 300, 200, 60)},
                "click_me": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "text": "Click Me!", "rect": (400, 400, 200, 60)},
            },
        },
        "SettingsScene": {
            "buttons": {
                "back": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "text": "Back", "rect": (300, 250, 300, 60)},
                "volume_up": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "text": "Volume Up", "rect": (300, 320, 300, 60)},
                "volume_down": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "text": "Volume Down", "rect": (300, 390, 300, 60)},
                "fullscreen": {
                    "graphic_name": "default_button", "font_name": "liberation_serif",
                    "text": "Fullscreen", "rect": (300, 460, 300, 60)}
            }
        },
    }
}
