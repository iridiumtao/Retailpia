import pygame

class Instruction():
    def __init__(self, x, y, font_size = 30):
        self.x = x
        self.y = y
        self.line_size = font_size + 30 # 行距
        self.color = (255, 255, 255)
        self.font_obj = pygame.font.Font("assets/ShadowsIntoLightTwo-Regular.ttf", font_size)

        # 為每行文字創建surface
        self.font_surfaces = []
        with open("assets/instructions.txt", 'r', encoding='utf8') as text:
            for line in text.readlines():
                self.font_surfaces.append(self.font_obj.render(line, True, self.color))
    
    def draw(self, screen):
        # draw所有text line，含行距運算
        for index, surface in enumerate(self.font_surfaces):
            screen.blit(surface, (self.x, self.y + self.line_size * index))