from os import path

DEBUG_DICT_AUDIO = {
    "debug_music": {
        "type": "music",
        "filename": "debug_audio_music.mp3",
    },
    "debug_sound": {
        "type": "sound_effect",
        "filename": "debug_audio_sound.wav",
    },
}

DEBUG_DICT_GRAPHIC = {
    "single": {
        "type": "image",
        "filename": "debug_graphic_manager_single.png",
    },
    "sequence": {
        "type": "image_sequence",
        "files": [
            {"filename": "debug_graphic_manager_sequence_1.png"},
            {"filename": "debug_graphic_manager_sequence_2.png"},
        ],
        "frame_duration": 200,
    }
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