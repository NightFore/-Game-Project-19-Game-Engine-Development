menu_config = {
    'start_menu': {
        "button": {
            'start': {
                'pos_x': 400, 'pos_y': 250, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Start',
                'action': "ui_manager.load_menu('main_menu')"
            },
            'test_features': {
                'pos_x': 400, 'pos_y': 350, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Test Features',
                'action': "ui_manager.load_menu('test_menu')"
            }
        },
        "label": {
            'title': {
                'pos_x': 400, 'pos_y': 100, 'rect_width': 300, 'rect_height': 100,
                'text_label': 'Welcome to the Game!', 'text_color': (255, 255, 255),
                'font_name': None, 'font_size': 36,
                'rect_color': (70, 130, 180), 'border_color': (255, 255, 255), 'border_width': 5
            }
        },
    },
    'main_menu': {
        "button": {
            'fullscreen': {
                'pos_x': 150, 'pos_y': 50, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Fullscreen',
                'action': 'window_manager.toggle_fullscreen'
            },
            'resizable': {
                'pos_x': 150, 'pos_y': 120, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Resizable',
                'action': 'window_manager.toggle_resizable'
            },
            'maximize': {
                'pos_x': 150, 'pos_y': 190, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Maximize',
                'action': 'window_manager.toggle_maximize'
            },
            'none': {
                'pos_x': 150, 'pos_y': 260, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'None',
                'action': ''
            },
            'test': {
                'pos_x': 400, 'pos_y': 50, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Test',
                'action': "debug((800, 600), 42, 'abcdefghijklmnopqrstuvwxyz', True)"
            },
            'play_music_1': {
                'pos_x': 400, 'pos_y': 120, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Music 1',
                'action': 'main_manager.audio_manager.play_music("bgm_eight_Lament_Scarlet")'
            },
            'play_music_2': {
                'pos_x': 400, 'pos_y': 190, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Music 2',
                'action': 'audio_manager.play_music("bgm_nagumorizu_Strategy_Meeting")'
            },
            'play_music_3': {
                'pos_x': 400, 'pos_y': 260, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Music 3',
                'action': 'audio_manager.play_music("bgm_tak_mfk_Dance_of_the_Cold_Moon")'
            },
            'play_sound': {
                'pos_x': 400, 'pos_y': 330, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Sound',
                'action': 'audio_manager.play_sound("maou_se_onepoint09")'
            },
            'play_voice': {
                'pos_x': 400, 'pos_y': 400, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Voice',
                'action': 'audio_manager.play_voice("YouFulca_voice_07_cool_attack")'
            },
            'volume_up': {
                'pos_x': 400, 'pos_y': 470, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Volume Up',
                'action': 'audio_manager.adjust_volume("master", 0.05)'
            },
            'volume_down': {
                'pos_x': 400, 'pos_y': 540, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Volume Down',
                'action': 'audio_manager.adjust_volume("master", -0.05)'
            },
            'toggle_music': {
                'pos_x': 650, 'pos_y': 50, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Music',
                'action': 'audio_manager.toggle_music_playback'
            },
            'stop_music': {
                'pos_x': 650, 'pos_y': 120, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Stop Music',
                'action': 'audio_manager.stop_music'
            },
            'stop_sound': {
                'pos_x': 650, 'pos_y': 190, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Stop Sound',
                'action': 'audio_manager.stop_sound'
            },
            'stop_voice': {
                'pos_x': 650, 'pos_y': 260, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Stop Voice',
                'action': 'audio_manager.stop_voice'
            },
            'loop_music': {
                'pos_x': 650, 'pos_y': 330, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Loop Music',
                'action': 'audio_manager.set_bgm_loop(-1)'
            },
            'no_loop': {
                'pos_x': 650, 'pos_y': 400, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'No Loop',
                'action': 'audio_manager.set_bgm_loop(0)'
            },
            'toggle_mute': {
                'pos_x': 650, 'pos_y': 470, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Mute',
                'action': 'audio_manager.toggle_audio_mute'
            },
        },
    },
    'test_menu': {
        "button": {
            'back_to_start': {
                'pos_x': 400, 'pos_y': 400, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Back to Start',
                'action': "ui_manager.load_menu('start_menu')"
            },
            'quit_game': {
                'pos_x': 800, 'pos_y': 0, 'rect_width': 64, 'rect_height': 64,
                'rect_color': (70, 130, 180), 'image_path': 'assets/images/ui/ui_original_icon_exit.png',
                'image_width': 64, 'image_height': 64,
                'action': 'main_manager.quit_game()',
                'align': 'ne',
                'shadow_enabled': False
            }
        },
        "label": {
            'test_header': {
                'pos_x': 400, 'pos_y': 100, 'rect_width': 300, 'rect_height': 50,
                'text_label': 'Test New Features', 'text_color': (255, 255, 255),
                'font_name': None, 'font_size': 36,
                'rect_color': (70, 130, 180), 'border_color': (255, 255, 255), 'border_width': 5,
                'layer': 2,
            },
            'layer_test': {
                'pos_x': 400, 'pos_y': 130, 'rect_width': 300, 'rect_height': 50,
                'text_label': 'Test Layer', 'text_color': (255, 255, 255),
                'font_name': None, 'font_size': 36,
                'rect_color': (70, 130, 180), 'border_color': (255, 255, 255), 'border_width': 5,
                'layer': 1,
            }
        }
    }
}
