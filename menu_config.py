menu_config = {
    'start_menu': {
        "button": {
            'start': {
                'position_x': 300, 'position_y': 250, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Start',
                'action': "ui_manager.load_menu('main_menu')"
            },
            'test_features': {
                'position_x': 300, 'position_y': 350, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Test Features',
                'action': "ui_manager.load_menu('test_menu')"
            }
        },
        "label": {
            'title': {
                'position_x': 250, 'position_y': 150, 'rect_width': 300, 'rect_height': 100,
                'text_label': 'Welcome to the Game!', 'text_color': (255, 255, 255),
                'font_name': None, 'font_size': 36, 'text_align': 'center',
                'rect_color': (70, 130, 180), 'border_color': (255, 255, 255), 'border_width': 5
            }
        },
    },
    'main_menu': {
        "button": {
            'none': {
                'position_x': 50, 'position_y': 260, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'None',
                'action': ''
            },
            'test': {
                'position_x': 300, 'position_y': 50, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Test',
                'action': "debug((800, 600), 42, 'abcdefghijklmnopqrstuvwxyz', True)"
            },
            'fullscreen': {
                'position_x': 50, 'position_y': 50, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Fullscreen',
                'action': 'window_manager.toggle_fullscreen'
            },
            'resizable': {
                'position_x': 50, 'position_y': 120, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Resizable',
                'action': 'window_manager.toggle_resizable'
            },
            'maximize': {
                'position_x': 50, 'position_y': 190, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Maximize',
                'action': 'window_manager.toggle_maximize'
            },
            'play_music_1': {
                'position_x': 300, 'position_y': 120, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Music 1',
                'action': 'main_manager.audio_manager.play_music("bgm_eight_Lament_Scarlet")'
            },
            'play_music_2': {
                'position_x': 300, 'position_y': 190, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Music 2',
                'action': 'audio_manager.play_music("bgm_nagumorizu_Strategy_Meeting")'
            },
            'play_music_3': {
                'position_x': 300, 'position_y': 260, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Music 3',
                'action': 'audio_manager.play_music("bgm_tak_mfk_Dance_of_the_Cold_Moon")'
            },
            'play_sound': {
                'position_x': 300, 'position_y': 330, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Sound',
                'action': 'audio_manager.play_sound("maou_se_onepoint09")'
            },
            'play_voice': {
                'position_x': 300, 'position_y': 400, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Play Voice',
                'action': 'audio_manager.play_voice("YouFulca_voice_07_cool_attack")'
            },
            'toggle_music': {
                'position_x': 550, 'position_y': 50, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Music',
                'action': 'audio_manager.toggle_music_playback'
            },
            'stop_music': {
                'position_x': 550, 'position_y': 120, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Stop Music',
                'action': 'audio_manager.stop_music'
            },
            'stop_sound': {
                'position_x': 550, 'position_y': 190, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Stop Sound',
                'action': 'audio_manager.stop_sound'
            },
            'stop_voice': {
                'position_x': 550, 'position_y': 260, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Stop Voice',
                'action': 'audio_manager.stop_voice'
            },
            'loop_music': {
                'position_x': 550, 'position_y': 330, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Loop Music',
                'action': 'audio_manager.set_bgm_loop(-1)'
            },
            'no_loop': {
                'position_x': 550, 'position_y': 400, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'No Loop',
                'action': 'audio_manager.set_bgm_loop(0)'
            },
            'toggle_mute': {
                'position_x': 550, 'position_y': 470, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Toggle Mute',
                'action': 'audio_manager.toggle_audio_mute'
            },
            'volume_up': {
                'position_x': 300, 'position_y': 470, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Volume Up',
                'action': 'audio_manager.adjust_volume("master", 0.05)'
            },
            'volume_down': {
                'position_x': 300, 'position_y': 540, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Volume Down',
                'action': 'audio_manager.adjust_volume("master", -0.05)'
            }
        },
        "label": {
            'header': {
                'position_x': 250, 'position_y': 20, 'rect_width': 300, 'rect_height': 25,
                'text_label': 'Main Menu', 'text_color': (255, 255, 255),
                'font_name': None, 'font_size': 36, 'text_align': 'center',
                'rect_color': (70, 130, 180), 'border_color': (255, 255, 255), 'border_width': 5
            }
        }
    },
    'test_menu': {
        "button": {
            'back_to_start': {
                'position_x': 300, 'position_y': 400, 'rect_width': 200, 'rect_height': 50,
                'rect_color': (70, 130, 180), 'text_label': 'Back to Start',
                'action': "ui_manager.load_menu('start_menu')"
            },
            'quit_game': {
                'position_x': 100, 'position_y': 400, 'rect_width': 64, 'rect_height': 64,
                'rect_color': (70, 130, 180), 'image_path': 'assets/images/ui/ui_original_icon_exit.png',
                'image_width': 64, 'image_height': 64,
                'action': 'main_manager.quit_game()',
            }
        },
        "label": {
            'test_header': {
                'position_x': 250, 'position_y': 50, 'rect_width': 300, 'rect_height': 100,
                'text_label': 'Test New Features', 'text_color': (255, 255, 255),
                'font_name': None, 'font_size': 36, 'text_align': 'center',
                'rect_color': (70, 130, 180), 'border_color': (255, 255, 255), 'border_width': 5
            }
        }
    }
}
