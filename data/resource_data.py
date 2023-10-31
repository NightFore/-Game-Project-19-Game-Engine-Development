# resource_data.py
"""
DICT_FILES
    AudioManager
        - music
        - sound
    GraphicManager
        - image
        - image_sequence
    TextManager
        - font
DICT_DATA
    ButtonManager
        - button
DICT_INSTANCES
    SceneManager
        - scene
"""
DICT_FILES = {
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

    # TextManager
    "font": {
        "liberation_serif": {"filename": "LiberationSerif-Regular.ttf", "size": 24, "color": (255, 255, 255)},
    },

}

DICT_DATA = {
    # ButtonManager
    "button": {
        "default": {
            "font_name": "liberation_serif", "size": (300, 60), "border_radius": 5, "align": "center",
            "color": {"active": (0, 255, 0), "inactive": (255, 0, 0), "border": (0, 0, 255)},
        },
        "icon": {
            "font_name": "liberation_serif", "size": (50, 50), "border_radius": 5, "align": "nw",
            "color": {"active": (0, 255, 0), "inactive": (255, 0, 0), "border": (0, 0, 255)},
        },
    },
}

DICT_SCENES = {
    # SceneManager
    "scene": {
        "MainMenuScene": {
            "buttons": {
                "start": {"button": "default", "pos": (640, 250), "text": "Start"},
                "settings": {"button": "default", "pos": (640, 320), "text": "Settings"},
                "debug_audio": {"button": "default", "pos": (640, 390), "text": "Debug Audio"},
                "pause_music": {"button": "default", "pos": (640, 460), "text": "Pause Music"},
                "toggle_music": {"button": "default", "pos": (640, 530), "text": "Toggle Music"},
                "toggle_zoom": {"button": "default", "pos": (640, 600), "text": "Toggle Zoom"},
                "quit_game": {"button": "icon", "pos": (10, 10), "text": "X"},
            },
            "texts": {
                "text_001": {"font": "liberation_serif", "pos": (600, 300), "text": "Hello World!"},
            },
        },
    }
}