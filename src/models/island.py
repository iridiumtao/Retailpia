import pygame

class Island(pygame.sprite.Sprite):
    """
    非常糟糕的寫法，勿用
    """
    def __init__(self, window_width = 1280, window_height= 720):
        pygame.sprite.Sprite.__init__(self)

        self.island_image = pygame.image.load("assets/island.png").convert_alpha()
        self.island_image = self.scale_keep_aspect_ratio(self.island_image, height = window_height * 0.8)

        x, y = window_width * 0.5, window_height * 0.6
        self.rect = self.island_image.get_rect(center=(x, y))

    def scale_keep_aspect_ratio(self, image, width = 100000, height = 100000):

        ref_width, ref_height = image.get_size()
        # 鎖定長寬比，參考長、寬數值較大者進行縮放
        if width <= height:
            height = int(width * ref_height / ref_width)
        else:
            width = int(height * ref_width / ref_height)
        image = pygame.transform.scale(image, (int(width), int(height)))
        return image

    def draw(self, screen):
        screen.blit(self.island_image, self.rect)
