import pygame

class Interface():

    def __init__(self, width, height, image, width_offset = 0, height_offset = 0, window_width = 1280, window_height = 720):

        self.interface_surface = pygame.image.load(image).convert_alpha()
        self.interface_surface = pygame.transform.scale(self.interface_surface, (width, height))
        self.interface_x = int((window_width - width) / 2) + width_offset
        self.interface_y = int((window_height - height) / 2) + height_offset

    def draw(self, screen):
        screen.blit(self.interface_surface, (self.interface_x, self.interface_y))