from os import path

DEBUG_DICT_AUDIO = {
    "debug_music": {
        "type": "music",
        "filename": "debug_audio_music.mp3",
    },
    "debug_sound": {
        "type": "sound",
        "filename": "debug_audio_sound.wav",
    },
}

DEBUG_DICT_FONT = {
    "liberation_serif_font_data": {
        "type": "font",
        "file_path": "LiberationSerif-Regular.ttf",
        "size": 24
    }
}

DEBUG_DICT_GRAPHIC = {
    "default_single": {
        "type": "image",
        "filename": "debug_graphic_manager_single.png",
    },
    "default_sequence": {
        "type": "image_sequence",
        "files": [
            {"filename": "debug_graphic_manager_sequence_1.png"},
            {"filename": "debug_graphic_manager_sequence_2.png"},
        ],
        "frame_duration": 200,
    },
    "default_interface": {
        "type": "interface",
        "color": {
            "default": (0, 0, 0),
            "border": (255, 255, 255),
        },
        "rect": {"x": 50, "y": 50, "width": 400, "height": 300},
        "hit_rect": {"x": 50, "y": 50, "width": 400, "height": 300},
        "border": {"width": 2, "height": 2}
    },
    "default_button": {
        "type": "button",
        "color": {
            "active": (0, 255, 0),
            "inactive": (255, 0, 0),
            "border": (0, 0, 255)
        },
        "rect": {"x": 100, "y": 100, "width": 200, "height": 50},
        "hit_rect": {"x": 100, "y": 100, "width": 200, "height": 50},
        "border": {"width": 2, "height": 2}
    },
}

DEBUG_DICT_SCENE = {
    "MainMenuScene": {
        "buttons": [
            {"name": "start", "position": (200, 150), "text": "Start"}
        ],
    },
    "GameScene": {
        "buttons": [
            {"name": "game_over", "position": (200, 150), "text": "Game Over"},
            {"name": "click_me", "position": (200, 250), "text": "Click Me!"}
        ],
    },
}