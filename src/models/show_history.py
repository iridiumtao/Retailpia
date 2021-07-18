import pygame
import assets
import json
from datetime import datetime
import time
import getpass

class Show_history():

    def __init__(self, category):

        self.jason = "src/record.json"
        self.category = category

        self.items = []
        self.text = ""
        self.x = 100

        xs = [400, 520, 640, 760, 880]
        categorys = ["Name", "Brand", "Pounds", "Code", "Type"]
        for i in range(len(categorys)):
            if categorys[i] == self.category:
                self.x = xs[i]

    def read_data(self):
        with open(self.jason, "r") as jsonFile1:
            record = json.load(jsonFile1)

        self.items = [record[purchase][self.category] for purchase in record if purchase != "CACHE"]  #i must be god
        jsonFile1.close()


    def draw(self, screen):
        self.read_data()
        screen.blit(pygame.font.Font(None, 40).render(self.category, True, pygame.Color("blue")), (self.x, 100))
        for i in range(len(self.items)):
            self.txt = pygame.font.Font(None, 32).render(self.items[i], True, pygame.Color("blue"))
            screen.blit(self.txt, (self.x, 150+i*40))

    def get_last(self):
        self.read_data()
        next_list = ["next"]
        boba_list = ["boba", "bubble tea", "tea"]

        if self.items[-1] in next_list:
            return 1
        elif self.items[-1] in boba_list:
            return 2
        return 0
        
