# resource_data.py

"""
DICT_RESOURCES
    AudioManager
        - music
        - sound
    GraphicManager
        - image
        - image_sequence
        - rect
    TextManager
        - font
DICT_INSTANCES
    ButtonManager
        - button
DICT_SCENES
    SceneManager
        - scene
"""

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
            "image_duration": 0.5,
        },
    },
    "rect": {
        "default_rect": {
            "size": (300, 50), "border_radius": 5,
            "color_data": {"active": (0, 255, 0), "inactive": (255, 0, 0), "border": (0, 0, 255)},
        },
        "default_icon": {
            "size": (50, 50), "border_radius": 5,
            "color_data": {"active": (0, 255, 0), "inactive": (255, 0, 0), "border": (0, 0, 255)},
        }
    },

    # TextManager
    "font": {
        "liberation_serif": {"filename": "LiberationSerif-Regular.ttf", "size": 24, "color": (255, 255, 255)},
    },
}



DICT_INSTANCES = {
    # ButtonManager
    "button": {
        "button_interface": {"graphic_name": "default_rect", "font_name": "liberation_serif", "align": "center"},
        "button_icon": {"graphic_name": "default_icon", "font_name": "liberation_serif", "align": "nw"},
        "button_image": {"graphic_name": "default_single", "font_name": "liberation_serif", "align": "nw"},
    },
}



DICT_SCENES = {
    # SceneManager
    "scene": {
        "MainMenuScene": {
            "buttons": {
                "start": {"button": "button_interface", "pos": (640, 250), "text": "Start"},
                "settings": {"button": "button_interface", "pos": (640, 320), "text": "Settings"},
                "debug_audio": {"button": "button_interface", "pos": (640, 390), "text": "Debug Audio"},
                "pause_music": {"button": "button_interface", "pos": (640, 460), "text": "Pause Music"},
                "toggle_music": {"button": "button_interface", "pos": (640, 530), "text": "Toggle Music"},
                "toggle_zoom": {"button": "button_interface", "pos": (640, 600), "text": "Toggle Zoom"},
                "quit_game": {"button": "button_icon", "pos": (10, 10), "text": "X"},
            },
            "graphics": {
                "test_single": {"graphic": "default_single", "pos": (10, 100), "align": "nw"},
                "test_sequence": {"graphic": "default_sequence", "pos": (640, 100), "align": "center"}
            }
        },
        "GameScene": {
            "buttons": {
            },
        },
        "SettingsScene": {
            "buttons": {
            },
        },
        "TemplateScene": {
            "buttons": {
            },
        },
    }
}
