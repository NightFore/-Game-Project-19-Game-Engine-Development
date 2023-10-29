# resource_data.py

DICT_RESOURCES = {
    "music": {
        "debug_music": {"filename": "debug_audio_music.mp3"},
    },
    "sound": {
        "debug_sound": {"filename": "debug_audio_sound.wav"},
    },
    "font": {
        "liberation_serif": {"filename": "LiberationSerif-Regular.ttf", "size": 24, "color": (255, 255, 255)},
    },
    "image": {
        "default_single": {"filename": "debug_graphic_manager_single.png"},
    },
    "image_sequence": {
        "default_sequence": {
            "files": [{"filename": "debug_graphic_manager_sequence_1.png"},
                      {"filename": "debug_graphic_manager_sequence_2.png"}],
            "image_duration": 0.2,
        },
    },
    "interface": {
        "default_interface": {
            "color": {"default": (0, 0, 0), "border": (255, 255, 255)},
            "rect": [50, 50, 400, 300], "hit_rect": [50, 50, 400, 300], "border_radius": 2
        },
    },
    "button": {
        "default_button": {"color": {"active": (0, 255, 0), "inactive": (255, 0, 0), "border": (0, 0, 255)}, "border_radius": 5},
    },
    "scene": {
        "MainMenuScene": {
            "buttons": {
                "start": {"graphic": "default_button", "rect": (640, 250, 300, 60), "text": "Start", "align": "center"},
                "settings": {"graphic": "default_button", "rect": (640, 320, 300, 60), "text": "Settings", "align": "center"},
                "debug_audio": {"graphic": "default_button", "rect": (640, 390, 300, 60), "text": "Debug Audio", "align": "center"},
                "pause_music": {"graphic": "default_button", "rect": (640, 460, 300, 60), "text": "Pause Music", "align": "center"},
                "toggle_music": {"graphic": "default_button", "rect": (640, 530, 300, 60), "text": "Toggle Music", "align": "center"},
                "toggle_zoom": {"graphic": "default_button", "rect": (640, 600, 300, 60), "text": "Toggle Zoom", "align": "center"},
                "quit_game": {"graphic": "default_button", "rect": (10, 10, 50, 50), "text": "X"},
            },
            "texts": [
                {"font": "liberation_serif", "position": (600, 300), "text": "Hello World!"},
                {"font": "liberation_serif", "position": (600, 360), "text": "Hello World 2!", "color": (0, 0, 0), "size": 20, "align": "nw"},
            ],
        },
        "GameScene": {
            "buttons": {
                "game_over": {"graphic": "default_button", "text": "Game Over", "rect": (400, 300, 200, 60)},
                "click_me": {"graphic": "default_button", "text": "Click Me!", "rect": (400, 400, 200, 60)},
            },
        },
        "SettingsScene": {
            "buttons": {
                "back": {"graphic": "default_button", "text": "Back", "rect": (300, 250, 300, 60)},
                "volume_up": {"graphic": "default_button", "text": "Volume Up", "rect": (300, 320, 300, 60)},
                "volume_down": {"graphic": "default_button", "text": "Volume Down", "rect": (300, 390, 300, 60)},
                "fullscreen": {"graphic": "default_button", "text": "Fullscreen", "rect": (300, 460, 300, 60)}
            }
        },
    }
}
