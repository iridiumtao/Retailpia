import configparser
import pygame
import os

class LocalConfig(object):
    """
    Use configparser to generate or load config from config.ini file
    """

    def __init__(self):
        self.skip_story = None
        self.config = configparser.ConfigParser(comment_prefixes = None, allow_no_value = True)

        if not os.path.isfile('config.ini'):
            print("No local config. Loading default.")
            self.generate_default_config()
        else:
            self.config.read('config.ini')

        self.load_game_config()

    def generate_default_config(self):
        """
        生成 config.ini
        """
        self.config['SCREEN'] = {'RESOLUTION_WIDTH' : '1280',
                                 'RESOLUTION_HEIGHT' : '720',
                                 '# Set fullscreen to TRUE may cause some problem on system resolution.' : None,
                                 'FULLSCREEN' : 'FALSE',
                                 'SCALED' : 'TRUE',
                                 'NOFRAME' : 'FALSE',
                                 'OPENGL' : 'FALSE',
                                 'display_index' : '0',
                                 '# VSYNC only works with the OPENGL or SCALED flags set TRUE' : None,
                                 'vsync' : '1'}
        self.config['GAME'] = {'skip_story' : 'FALSE'}
        self.save_config()

    def load_screen_config(self):
        """
        載入 SCREEN 設定
        """
        try:
            screen = self.config['SCREEN']

            resolution_width = int(screen['resolution_width'])
            resolution_height = int(screen['resolution_height'])
            screen_flags = 0
            if screen.getboolean('fullscreen'):
                screen_flags = pygame.FULLSCREEN
            if screen.getboolean('scaled'):
                screen_flags = screen_flags | pygame.SCALED
            if screen.getboolean('noframe'):
                screen_flags = screen_flags | pygame.NOFRAME
            if screen.getboolean('opengl'):
                screen_flags = screen_flags | pygame.OPENGL
            display_index = int(screen['display_index'])
            vsync = int(screen['vsync'])
            return resolution_width, resolution_height, screen_flags, display_index, vsync
        except:
            print("Error reading local config. Loading default.")
            self.generate_default_config()
            return 1280, 720, pygame.SCALED, 0, 1 # 回傳預設 config

    def load_game_config(self):
        """
        載入 GAME 設定
        """
        try:
            game = self.config['GAME']
            self.skip_story = game.getboolean('skip_story')
        except:
            print("Error reading local config. Loading default.")
            self.generate_default_config()
            self.skip_story = False

    def save_config(self):
        with open('config.ini', 'w', encoding='utf-8') as config_file:
            self.config.write(config_file)
