# button_config.py

button_config = {
    'start_menu': {
        'start': {
            'x': 300, 'y': 250, 'width': 200, 'height': 50,
            'label': 'Start', 'color': (70, 130, 180), 'action': 'start_game'
        }
    },
    'main_menu': {
        'none': {
            'x': 50, 'y': 260, 'width': 200, 'height': 50,
            'label': 'None', 'color': (70, 130, 180), 'action': ''
        },
        'test': {
            'x': 300, 'y': 50, 'width': 200, 'height': 50,
            'label': 'Test', 'color': (70, 130, 180), 'action': "debug((800, 600), 42, 'abcdefghijklmnopqrstuvwxyz', True)"
        },
        'fullscreen': {
            'x': 50, 'y': 50, 'width': 200, 'height': 50,
            'label': 'Toggle Fullscreen', 'color': (70, 130, 180), 'action': 'window_manager.toggle_fullscreen'
        },
        'resizable': {
            'x': 50, 'y': 120, 'width': 200, 'height': 50,
            'label': 'Toggle Resizable', 'color': (70, 130, 180), 'action': 'window_manager.toggle_resizable'
        },
        'maximize': {
            'x': 50, 'y': 190, 'width': 200, 'height': 50,
            'label': 'Toggle Maximize', 'color': (70, 130, 180), 'action': 'window_manager.toggle_maximize'
        },
        'play_music_1': {
            'x': 300, 'y': 120, 'width': 200, 'height': 50,
            'label': 'Play Music 1', 'color': (70, 130, 180), 'action': 'main_manager.audio_manager.play_music("bgm_eight_Lament_Scarlet")'
        },
        'play_music_2': {
            'x': 300, 'y': 190, 'width': 200, 'height': 50,
            'label': 'Play Music 2', 'color': (70, 130, 180), 'action': 'audio_manager.play_music("bgm_nagumorizu_Strategy_Meeting")'
        },
        'play_music_3': {
            'x': 300, 'y': 260, 'width': 200, 'height': 50,
            'label': 'Play Music 3', 'color': (70, 130, 180), 'action': 'audio_manager.play_music("bgm_tak_mfk_冷月の舞踏_(Reigetsu_no_Buto)")'
        },
        'play_sound': {
            'x': 300, 'y': 330, 'width': 200, 'height': 50,
            'label': 'Play Sound', 'color': (70, 130, 180), 'action': 'audio_manager.play_sound("maou_se_onepoint09")'
        },
        'play_voice': {
            'x': 300, 'y': 400, 'width': 200, 'height': 50,
            'label': 'Play Voice', 'color': (70, 130, 180), 'action': 'audio_manager.play_voice("YouFulca_voice_07_cool_attack")'
        },
        'toggle_music': {
            'x': 550, 'y': 50, 'width': 200, 'height': 50,
            'label': 'Toggle Music', 'color': (70, 130, 180), 'action': 'audio_manager.toggle_music_playback'
        },
        'stop_music': {
            'x': 550, 'y': 120, 'width': 200, 'height': 50,
            'label': 'Stop Music', 'color': (70, 130, 180), 'action': 'audio_manager.stop_music'
        },
        'stop_sound': {
            'x': 550, 'y': 190, 'width': 200, 'height': 50,
            'label': 'Stop Sound', 'color': (70, 130, 180), 'action': 'audio_manager.stop_sound'
        },
        'stop_voice': {
            'x': 550, 'y': 260, 'width': 200, 'height': 50,
            'label': 'Stop Voice', 'color': (70, 130, 180), 'action': 'audio_manager.stop_voice'
        },
        'loop_music': {
            'x': 550, 'y': 330, 'width': 200, 'height': 50,
            'label': 'Loop Music', 'color': (70, 130, 180), 'action': 'audio_manager.set_bgm_loop(-1)'
        },
        'no_loop': {
            'x': 550, 'y': 400, 'width': 200, 'height': 50,
            'label': 'No Loop', 'color': (70, 130, 180), 'action': 'audio_manager.set_bgm_loop(0)'
        },
        'toggle_mute': {
            'x': 550, 'y': 470, 'width': 200, 'height': 50,
            'label': 'Toggle Mute', 'color': (70, 130, 180), 'action': 'audio_manager.toggle_audio_mute'
        },
        'volume_up': {
            'x': 300, 'y': 470, 'width': 200, 'height': 50,
            'label': 'Volume Up', 'color': (70, 130, 180), 'action': 'audio_manager.adjust_volume("master", 0.05)'
        },
        'volume_down': {
            'x': 300, 'y': 540, 'width': 200, 'height': 50,
            'label': 'Volume Down', 'color': (70, 130, 180), 'action': 'audio_manager.adjust_volume("master", -0.05)'
        }
    }
}
