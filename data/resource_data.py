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
        "font_title": {"filename": "LiberationSerif-Regular.ttf", "size": 36, "color": (255, 255, 255), "align": "center"},
        "font_body": {"filename": "LiberationSerif-Regular.ttf", "size": 24, "color": (255, 255, 255), "align": "center"},
    },
}



DICT_INSTANCES = {
    # ButtonManager
    "button": {
        "button_interface": {"graphic": "default_rect", "font": "font_body", "align": "center"},
        "button_icon": {"graphic": "default_icon", "font": "font_body", "align": "nw"},
        "button_image": {"graphic": "default_single", "font": "font_body", "align": "nw"},
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
                "debug_selection": {"button": "button_interface", "pos": (640, 670), "text": "Debug Selection"},
                "quit_game": {"button": "button_icon", "pos": (10, 10), "text": "X"},
            },
            "graphics": {
                "single": {"graphic": "default_single", "pos": (10, 100), "align": "nw"},
                "sequence": {"graphic": "default_sequence", "pos": (640, 150), "align": "center"}
            },
            "texts": {
                "project_title": {"font": "font_title", "pos": (640, 50), "align": "center"},
            }
        },
        "GameScene": {
            "buttons": {
                "game_over": {"button": "button_interface", "pos": (640, 250), "text": "Game Over"},
                "click_me": {"button": "button_interface", "pos": (640, 320), "text": "Click Me!"},
            },
            "graphics": {},
            "texts": {}
        },
        "SettingsScene": {
            "buttons": {
                "return": {"button": "button_interface", "pos": (100, 350), "text": "Return to Main Menu", "align": "nw"},
                "music_volume_up": {"button": "button_interface", "pos": (100, 400), "text": "Music Volume Up", "align": "nw"},
                "music_volume_down": {"button": "button_interface", "pos": (100, 450), "text": "Music Volume Down", "align": "nw"},
                "sound_volume_up": {"button": "button_interface", "pos": (100, 500), "text": "Sound Volume Up", "align": "nw"},
                "sound_volume_down": {"button": "button_interface", "pos": (100, 550), "text": "Sound Volume Down", "align": "nw"},
            },
            "graphics": {},
            "texts": {
                "settings": {"font": "font_body", "pos": (50, 300), "text": "Settings", "align": "nw"},
                "volume_music": {"font": "font_body", "pos": (450, 425)},
                "volume_sound": {"font": "font_body", "pos": (450, 525)},
            }
        },
        "LevelSelectionScene": {
            "buttons": {},
            "graphics": {},
            "texts": {}
        },
        "TemplateScene": {
            "buttons": {},
            "graphics": {},
            "texts": {}
        },
    }
}
