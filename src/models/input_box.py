import pygame
import assets
import json
from datetime import datetime
import time
import getpass

class Input_box():
    def __init__(self, x, y, w, h, text=""):

        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color("lightskyblue3")
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
        self.active = False
        self.word = "init"

        self.category = text

    def enter(self, press, key):
        if press != None:
            if self.rect.collidepoint(press):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pygame.Color("blue") if self.active else pygame.Color("lightskyblue3")
        if self.active:
            if key == pygame.K_RETURN:
                print("Input is: " + self.text)
                self.word = self.text

                self.record(self.category, self.word, True)

            elif key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif key!= None:
                try:
                    self.text += chr(key)
                except:
                    pass
        # Re-render the text.
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def record(self, category="Name", content="unknown", cache=True):

        if cache == True:
            with open(r"src/record.json", "r") as jsonFile1:
                record = json.load(jsonFile1)

            # record["CACHE2"] = {}
            if category == "Name":
                record["CACHE"]["Name"] = str(content)
            elif category == "Brand":
                record["CACHE"]["Brand"] = str(content)
            elif category == "Pounds":
                record["CACHE"]["Pounds"] = str(content)
            elif category == "Code":
                record["CACHE"]["Code"] = str(content)
            elif category == "Type":
                record["CACHE"]["Type"] = str(content)

            with open("src/record.json", "w", encoding='utf-8') as jsonFile2:
                json.dump(record, jsonFile2, indent=4)

            jsonFile1.close()
            jsonFile2.close()

        else:
            with open("src/record.json", "r") as jsonFile1:
                record = json.load(jsonFile1)

            user =  getpass.getuser()
            date = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
            now = str(user + " at " + date)
            record[str(now)] = {}
            record[str(now)]["Name"] = record["CACHE"]["Name"]
            record[str(now)]["Brand"] = record["CACHE"]["Brand"]
            record[str(now)]["Pounds"] = record["CACHE"]["Pounds"]
            record[str(now)]["Code"] = record["CACHE"]["Code"]
            record[str(now)]["Type"] = record["CACHE"]["Type"]

            now_list = [i for i in record]

            if len(now_list) > 12:
                for item in now_list[1:len(now_list)-12]:
                    record.pop(item)



            with open("src/record.json", "w", encoding='utf-8') as jsonFile2:
                json.dump(record, jsonFile2, indent=4)

            jsonFile1.close()
            jsonFile2.close()

    def clear_cache(self):
        with open(r"src/record.json", "r") as jsonFile1:
            record = json.load(jsonFile1)

        for item in record["CACHE"]:
            record["CACHE"][item] = "unknown"
        with open("src/record.json", "w", encoding='utf-8') as jsonFile2:
            json.dump(record, jsonFile2, indent=4)

        jsonFile1.close()
        jsonFile2.close()
