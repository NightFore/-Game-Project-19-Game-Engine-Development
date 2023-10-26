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
        "frame_duration": 0.2,
    },
    "default_interface": {
        "type": "interface",
        "color": {"default": (0, 0, 0), "border": (255, 255, 255)},
        "rect": {"x": 50, "y": 50, "width": 400, "height": 300},
        "hit_rect": {"x": 50, "y": 50, "width": 400, "height": 300},
        "border_size": 2
    },
    "default_button": {
        "type": "button",
        "color": {"active": (0, 255, 0), "inactive": (255, 0, 0), "border": (0, 0, 255)},
        "border_size": 5
    },
}
DEBUG_DICT_SCENE = {
    "MainMenuScene": {
        "buttons": {
            "start": {"graphic": "default_button", "text": "Start", "rect": (300, 250, 300, 60)},
            "settings": {"graphic": "default_button", "text": "Settings", "rect": (300, 320, 300, 60)},
            "debug_audio": {"graphic": "default_button", "text": "Debug Audio", "rect": (300, 390, 300, 60)},
            "pause_music": {"graphic": "default_button", "text": "Pause Music", "rect": (300, 460, 300, 60)},
            "toggle_music": {"graphic": "default_button", "text": "Toggle Music", "rect": (300, 530, 300, 60)},
        },
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
