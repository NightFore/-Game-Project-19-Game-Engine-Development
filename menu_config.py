# menu_config.py

menu_config = {
    'start_menu': {
        "button": {
            'start': {
                'x': 300, 'y': 250, 'width': 200, 'height': 50, 'label': 'Start', 'color': (70, 130, 180),
                'action': "ui_manager.load_menu('main_menu')"
            },
            'test_features': {
                'x': 300, 'y': 350, 'width': 200, 'height': 50, 'label': 'Test Features', 'color': (70, 130, 180),
                'action': "ui_manager.load_menu('test_menu')"
            }
        },
        "label": {
            'title': {
                'x': 250, 'y': 150, 'width': 300, 'height': 100, 'label': 'Welcome to the Game!', 'color': (255, 255, 255),
                'font_name': None, 'font_size': 36, 'alignment': 'center'
            }
        },
    },
    'main_menu': {
        "button": {
            'none': {
                'x': 50, 'y': 260, 'width': 200, 'height': 50, 'label': 'None', 'color': (70, 130, 180),
                'action': ''
            },
            'test': {
                'x': 300, 'y': 50, 'width': 200, 'height': 50, 'label': 'Test', 'color': (70, 130, 180),
                'action': "debug((800, 600), 42, 'abcdefghijklmnopqrstuvwxyz', True)"
            },
            'fullscreen': {
                'x': 50, 'y': 50, 'width': 200, 'height': 50, 'label': 'Toggle Fullscreen', 'color': (70, 130, 180),
                'action': 'window_manager.toggle_fullscreen'
            },
            'resizable': {
                'x': 50, 'y': 120, 'width': 200, 'height': 50, 'label': 'Toggle Resizable', 'color': (70, 130, 180),
                'action': 'window_manager.toggle_resizable'
            },
            'maximize': {
                'x': 50, 'y': 190, 'width': 200, 'height': 50, 'label': 'Toggle Maximize', 'color': (70, 130, 180),
                'action': 'window_manager.toggle_maximize'
            },
            'play_music_1': {
                'x': 300, 'y': 120, 'width': 200, 'height': 50, 'label': 'Play Music 1', 'color': (70, 130, 180),
                'action': 'main_manager.audio_manager.play_music("bgm_eight_Lament_Scarlet")'
            },
            'play_music_2': {
                'x': 300, 'y': 190, 'width': 200, 'height': 50, 'label': 'Play Music 2', 'color': (70, 130, 180),
                'action': 'audio_manager.play_music("bgm_nagumorizu_Strategy_Meeting")'
            },
            'play_music_3': {
                'x': 300, 'y': 260, 'width': 200, 'height': 50, 'label': 'Play Music 3', 'color': (70, 130, 180),
                'action': 'audio_manager.play_music("bgm_tak_mfk_Dance_of_the_Cold_Moon")'
            },
            'play_sound': {
                'x': 300, 'y': 330, 'width': 200, 'height': 50, 'label': 'Play Sound', 'color': (70, 130, 180),
                'action': 'audio_manager.play_sound("maou_se_onepoint09")'
            },
            'play_voice': {
                'x': 300, 'y': 400, 'width': 200, 'height': 50, 'label': 'Play Voice', 'color': (70, 130, 180),
                'action': 'audio_manager.play_voice("YouFulca_voice_07_cool_attack")'
            },
            'toggle_music': {
                'x': 550, 'y': 50, 'width': 200, 'height': 50, 'label': 'Toggle Music', 'color': (70, 130, 180),
                'action': 'audio_manager.toggle_music_playback'
            },
            'stop_music': {
                'x': 550, 'y': 120, 'width': 200, 'height': 50, 'label': 'Stop Music', 'color': (70, 130, 180),
                'action': 'audio_manager.stop_music'
            },
            'stop_sound': {
                'x': 550, 'y': 190, 'width': 200, 'height': 50, 'label': 'Stop Sound', 'color': (70, 130, 180),
                'action': 'audio_manager.stop_sound'
            },
            'stop_voice': {
                'x': 550, 'y': 260, 'width': 200, 'height': 50, 'label': 'Stop Voice', 'color': (70, 130, 180),
                'action': 'audio_manager.stop_voice'
            },
            'loop_music': {
                'x': 550, 'y': 330, 'width': 200, 'height': 50, 'label': 'Loop Music', 'color': (70, 130, 180),
                'action': 'audio_manager.set_bgm_loop(-1)'
            },
            'no_loop': {
                'x': 550, 'y': 400, 'width': 200, 'height': 50, 'label': 'No Loop', 'color': (70, 130, 180),
                'action': 'audio_manager.set_bgm_loop(0)'
            },
            'toggle_mute': {
                'x': 550, 'y': 470, 'width': 200, 'height': 50, 'label': 'Toggle Mute', 'color': (70, 130, 180),
                'action': 'audio_manager.toggle_audio_mute'
            },
            'volume_up': {
                'x': 300, 'y': 470, 'width': 200, 'height': 50, 'label': 'Volume Up', 'color': (70, 130, 180),
                'action': 'audio_manager.adjust_volume("master", 0.05)'
            },
            'volume_down': {
                'x': 300, 'y': 540, 'width': 200, 'height': 50, 'label': 'Volume Down', 'color': (70, 130, 180),
                'action': 'audio_manager.adjust_volume("master", -0.05)'
            }
        },
        "label": {
            'header': {
                'x': 250, 'y': 20, 'width': 300, 'height': 25, 'label': 'Main Menu', 'color': (255, 255, 255),
                'font_name': None, 'font_size': 36, 'alignment': 'center'
            }
        }
    },
    'test_menu': {
        "button": {
            'back_to_start': {
                'x': 300, 'y': 400, 'width': 200, 'height': 50, 'label': 'Back to Start', 'color': (70, 130, 180),
                'action': "ui_manager.load_menu('start_menu')"
            },
            'quit_game': {
                'x': 400, 'y': 500,
                "width": 128, "height": 128, 'color': (70, 130, 180),
                'image_width': 64, 'image_height': 64,
                'image': 'assets/images/ui/ui_original_icon_exit.png',
                'action': 'main_manager.quit_game()'
            }
        },
        "label": {
            'test_header': {
                'x': 250, 'y': 50, 'width': 300, 'height': 100, 'label': 'Test New Features',
                'color': (255, 255, 255),
                'font_name': None,
                'font_size': 36,
                'alignment': 'center',
                'rect_color': (70, 130, 180),  # Background color of the box
                'border_color': (255, 255, 255),  # White border
                'border_width': 5  # Border thickness
            }
        }
    }
}
