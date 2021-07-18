import pygame

class Message():

    def __init__(self, x, y, text, size = 50):
        self.font_obj = pygame.font.Font("assets/ShadowsIntoLightTwo-Regular.ttf", size)

        self.font_x = x
        self.font_y = y
        self.text = text
        self.color = (255, 255, 255)
        self.font_surface = self.font_obj.render(self.text, True, self.color)        

    def draw(self, screen):
        '''
        繪製
        '''
        screen.blit(self.font_surface, (self.font_x, self.font_y))