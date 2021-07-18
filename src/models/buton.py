import pygame
import assets

class Button(pygame.sprite.Sprite):
    def __init__(self, x = 100, y = 100, w = 100, h = 100, image = "help_button.png", lock_aspect_ratio = False, visual_effect = True):
        pygame.sprite.Sprite.__init__(self)

        # 設定圖片大小、長寬比、效果
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.lock_aspect_ratio = lock_aspect_ratio

        # 放大效果參數
        self.visual_effect = visual_effect # 是否啟用
        self.effect_ratio = 1.1 # 放大倍數
        self.x_offset = 0
        self.y_offset = 0

        # 載入圖片
        self.images = []
        self.image = pygame.image.load(image).convert_alpha()
        self.aspect_ratio()

        # 設定rect屬性（圖片座標、大小）
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def aspect_ratio(self):
        '''
        鎖定長寬比
        '''
        if self.lock_aspect_ratio:
            # 鎖定長寬比，參考長、寬數值較大者進行縮放
            rew_width, raw_height = self.image.get_size()
            if self.width >= self.height:
                self.height = int(self.width * raw_height / rew_width)
            else:
                self.width = int(self.height * rew_width / raw_height)

        self.image = pygame.transform.scale(self.image, (self.width ,self.height))  
        if self.visual_effect:
            # 製作效果圖
            e_width = int(self.width * self.effect_ratio)
            e_height = int(self.height * self.effect_ratio)
            self.x_offset = int((e_width - self.width) / 2)
            self.y_offset = int((e_height - self.height) / 2)

            self.images.append(self.image.copy())
            self.images.append(pygame.transform.scale(self.image, (e_width, e_height)))        

    def set_focus(self, focus):
        '''
        是否選取按鈕
        '''
        if self.visual_effect:
            if focus:
                self.image = self.images[1]
                self.rect = self.image.get_rect()
                self.rect.x = self.x - self.x_offset
                self.rect.y = self.y - self.y_offset
            else:
                self.image = self.images[0]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y