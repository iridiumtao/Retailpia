import pygame
import random

class Code():

    def __init__(self, size = 50, length = 4, window_width = 1280, window_height = 720):
        self.font_obj = pygame.font.Font(None, size)
        self.color = (255, 255, 255)
        self.length = length # code長度
        self.code_text = None
        self.font_surface = None
        self.society_num = None
        self.update() # 更新一次code

        self.font_x = int((window_width - self.font_surface.get_width()) / 2)
        self.font_y = int((window_height - self.font_surface.get_height()) / 2)

    def update(self, society_num = None):
        '''
        更新code
        '''
        self.society_num = society_num
        code = random.randint(0, (10 ** self.length) - 1)
        self.code_text = str(code).zfill(self.length)
        self.font_surface = self.font_obj.render('Code: ' + self.code_text, True, self.color)

    def draw(self, screen):
        '''
        繪製
        '''
        screen.blit(self.font_surface, (self.font_x, self.font_y))
