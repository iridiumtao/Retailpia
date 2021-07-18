import pygame

class Society(pygame.sprite.Sprite):
    LEVEL_MULTIPLIER = 34
    NORMAL_HOUSE = 0
    NEXT_HOUSE = 1
    BOBA_HOUSE = 2
    LAND = 3

    def __init__(self, x=100, y=100, w=112, h=112, floor=0, type=0, layer=0):
        pygame.sprite.Sprite.__init__(self)
        self.hidden_image = pygame.transform.scale(pygame.image.load("assets/1px.png").convert_alpha(), (1, 1))

        self.initialize(x, y, w, h, floor, type, layer)

    def initialize(self, x=100, y=100, w=112, h=112, floor=0, type=0, layer=0):
        self.w = w
        self.h = h

        self._w = w
        self._h = h

        self.image = self.hidden_image
        self.images = []
        self.images_focused = []

        self.floor = floor
        self.level = 0
        self.type = type
        self.rect = self.image.get_rect()

        # original x and y
        self._x = x
        self._y = y

        self.rect.x = x
        self.rect.y = y
        self.isshow = False
        self.isfocused = False
        self._layer = layer

    def show(self, type = None):
        if self.isshow:
            print("已經show過了")
            return False

        if self.type == self.LAND:
            self.show_land()
            return True

        self.isshow = True

        self.init_images(type)
        return True

    def init_images(self, type = None):
        if type is not None:
            image_path = self.get_image_path(type)
            print(image_path)
        else:
            image_path = self.get_image_path(self.type)
        w = self.w
        h = self.h

        self.images = []
        self.images_focused = []
        # self.images.append(pygame.transform.scale(pygame.image.load(image_path+".png").convert_alpha(), (int(w), int(h))))
        # self.images.append(pygame.transform.scale(pygame.image.load(image_path+".png").convert_alpha(), (int(w), int(h) * 2)))
        # self.images.append(pygame.transform.scale(pygame.image.load(image_path+".png").convert_alpha(), (int(w), int(h) * 3)))
        # self.images_focused.append(pygame.transform.scale(pygame.image.load(image_path+".png").convert_alpha(), (int(w)+8, int(h) + 8)))
        # self.images_focused.append(pygame.transform.scale(pygame.image.load(image_path+".png").convert_alpha(), (int(w)+4, int(h) * 2 + 4)))
        # self.images_focused.append(pygame.transform.scale(pygame.image.load(image_path+".png").convert_alpha(), (int(w)+4, int(h) * 3 + 4)))
        self.images.append(pygame.transform.scale(pygame.image.load(image_path+".png").convert_alpha(), (int(w), int(h))))
        self.images.append(pygame.transform.scale(pygame.image.load(image_path+"_1.png").convert_alpha(), (int(w), int(h * 1.298))))
        self.images.append(pygame.transform.scale(pygame.image.load(image_path+"_2.png").convert_alpha(), (int(w), int(h * 1.596))))
        self.images_focused.append(pygame.transform.scale(pygame.image.load(image_path+".png").convert_alpha(), (int(w)+8, int(h) + 8)))
        self.images_focused.append(pygame.transform.scale(pygame.image.load(image_path+"_1.png").convert_alpha(), (int(w)+7, int(h * 1.298 + 6))))
        self.images_focused.append(pygame.transform.scale(pygame.image.load(image_path+"_2.png").convert_alpha(), (int(w)+4, int(h * 1.596 + 4))))
        if self.isshow:
            self.image = self.images[self.level]
        else:
            self.image = pygame.transform.scale(pygame.image.load("assets/1px.png").convert_alpha(), (1, 1))
        self.rect = self.image.get_rect()
        self.rect.x = self._x
        self.rect.y = self._y

    def set_type(self, type):
        self.type = type

    def get_image_path(self, type):
        if type == self.NORMAL_HOUSE:
            image_path = "assets/normal_house"
        elif type == self.NEXT_HOUSE:
            image_path = "assets/next_house"
        elif type == self.BOBA_HOUSE:
            image_path = "assets/bubble_tea_house"
        elif type == self.LAND:
            image_path = "assets/soil"
        self.type = type
        return image_path

    def show_land(self):
        if not self.type == self.LAND:
            return

        self.images.append(pygame.transform.scale(pygame.image.load("assets/1px.png").convert_alpha(), (int(self.w), int(self.h))))
        self.images_focused.append(pygame.transform.scale(pygame.image.load("assets/soil.png").convert_alpha(), (int(self.w)+8, int(self.h) + 8)))
        self.image = self.images[0]

        self.rect = self.images_focused[0].get_rect()
        self.rect.x = self._x
        self.rect.y = self._y
        self.isshow = True

    def level_up(self):
        """
        Make the society level up.
        """
        if not self.isshow:
            return False

        if self.type == self.LAND:
            print("ERROR: LAND 無法升級")
            return False

        if self.level >= 2:
            print("ERROR: 樓層數大於3")
            return False

        self.level += 1
        self.image = self.images[self.level]
        self.rect = self.image.get_rect()
        self.rect.x = self._x
        self.rect.y = self._y - (self.level * self.LEVEL_MULTIPLIER)
        print(f"房子升至{self.level}級")
        return True

    def set_focused(self, isfocused):
        if not self.isshow:
            return

        if isfocused:
            self.isfocused = True
            self.rect.x = self._x - 2
            self.rect.y = self._y - 4 - (self.floor*2) - (self.level * self.LEVEL_MULTIPLIER)
            self.image = self.images_focused[self.level]

        else:
            self.isfocused = True
            self.rect.x = self._x
            self.rect.y = self._y - (self.level * self.LEVEL_MULTIPLIER)
            self.image = self.images[self.level]

    def level_down(self):
        if not self.isshow:
            return False

        if self.level <= 0:
            print("ERROR: 樓層數小於0")
            return False

        if self.type == self.LAND:
            print("ERROR: LAND 無法降級")
            return False

        self.level -= 1
        self.image = self.images[self.level]
        self.rect = self.image.get_rect()
        self.rect.x = self._x
        self.rect.y = self._y
        print(f"房子降至{self.level}級")
        return True

    def redeemed(self):
        if self.level != 2:
            return
        self.clear_society()

    def clear_society(self):
        print("clear")
        self.initialize(x=self._x, y=self._y, w=self._w, h=self._h)
