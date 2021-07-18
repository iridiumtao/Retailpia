import pygame
import assets
import src.view as view
class Story():

    def __init__(self, x, y, w, h, chat_font_size = 25, character_font_size = 50):
        self.chat_pos = (x, y)
        self.window_width = w
        self.window_height = h
        self.foreground_x = 0
        self.foreground_y = 0
        self.chat_obj = pygame.font.Font("assets/ShadowsIntoLightTwo-Regular.ttf", chat_font_size)
        self.big_chat_obj = pygame.font.Font("assets/ShadowsIntoLightTwo-Regular.ttf", chat_font_size + 20)
        self.color = (255, 255, 255)

        self.line = ""
        self.line_sequence = ""
        self.text_pointer = 0
        self.chat_surface = None

        self.character_pos = (100, 520)
        self.character_obj = pygame.font.Font("assets/ShadowsIntoLightTwo-Regular.ttf", character_font_size)
        self.character_surface = None

        self.scale_keep_aspect_ratio = view.GraphicalView.scale_keep_aspect_ratio

        self.lines = ["One fine day in Retailpia when everyone was enjoying their late afternoon...", # Narrator
                    "The evil monster “Paypay” has landed on the top of Retailpia.", # Narrator
                    "Pay!!!!! Pay!!!!!!", # Paypay
                    "On that day, mankind received a grim reminder.", # Narrator
                    "We lived in fear of spendthrift", # Narrator
                    "And were disgraced to live in these cages we called debt.", # Narrator
                    "Paypay lured citizens into the nation of “Spentacy land”, where people never learned to save money.", # Narrator
                    "He even ate all the reward points and coupons they earn while shopping.", # Narrator
                    "The empire is collapsing, culture is fading, the civilization is crashing. Could things be even worse?", # Narrator
                    "Meanwhile...","","","","","",
                    "Who are you? All citizens should be in the shelter at this point!", # Vice minister
                    "Minister, listen, I have a plan.", # you
                    "Go ahead, I shell listen.", # Prime minister
                    "I once also was a slave of overspending, but then found self-discipline and survived till now.", # you
                    "Oh?", # Prime minister
                    "The only cure is expense tracking! This is the only chance for we humans to boost immunity against Paypay.", # you
                    "But how?", # Prime minister
                    "Let me lead the department of finance, and make civilization great again!", # you
                    "Then let’s do this! But dare you remember, there is no turning back.", # Prime minister
                    "I know. Failure was never an option!", # you
                    "So that’s how you become the chair of the department of finance. Now good luck saving Retailpia!"] # Narrator

        self.characters = ["Narrator", "Narrator", "Paypay", "Narrator", "Narrator", "Narrator", "Narrator", "Narrator", "Narrator", "Narrator","","","","","",
                        "Vice minister", "You", "Prime minister", "You", "Prime minister", "You", "Prime minister", "You", "Prime minister", "You", "Narrator"]

        self.foregrounds = ["assets/1px.png", "assets/scene_cactus.png", "assets/scene_cactus_yelling.png", "assets/1px.png", "assets/1px.png", "assets/1px.png", "assets/1px.png", "assets/1px.png", "assets/1px.png", "assets/1px.png",
                            "assets/scene_council_in_1.png", "assets/scene_council_in_2.png", "assets/scene_council_in_3.png", "assets/scene_council_in_4.png", "assets/scene_council_in_5.png",
                            "assets/scene_vice_mayor.png", "assets/1px.png", "assets/scene_mayor.png", "assets/scene_mayor.png", "assets/scene_mayor.png"
                            , "assets/scene_mayor.png", "assets/scene_mayor.png", "assets/scene_council_book.png", "assets/scene_mayor.png", "assets/scene_mayor.png", "assets/scene_finance.png"]

        self.backgrounds = ["assets/scene_town.png", "assets/scene_town.png", "assets/scene_town.png", "assets/scene_people_bad.png", "assets/scene_people_bad.png",
                            "assets/scene_people_bad.png", "assets/scene_people_bad.png", "assets/scene_people_bad.png", "assets/scene_town_bad.png", "assets/scene_council.png",
                            "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png",
                            "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png",
                            "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png", "assets/scene_council.png", "assets/background.png"]

    def select_line(self, index):
        self.background_image = pygame.image.load(self.backgrounds[index]).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))

        self.foreground_image = pygame.image.load(self.foregrounds[index]).convert_alpha()
        if index >= 10 and index <= 14:
            self.foreground_image = pygame.transform.scale(self.foreground_image, (self.window_width, self.window_height))
            self.foreground_x, self.foreground_y = self.window_width * 0.5, self.window_height * 0.5
            self.dialog_box = pygame.image.load("assets/1px.png").convert_alpha()
            self.dialog_box = pygame.transform.scale(self.dialog_box, (self.window_width, 300))
        else:
            self.foreground_image = self.scale_keep_aspect_ratio(self, image = self.foreground_image, height = self.window_height * 0.8)
            self.foreground_x, self.foreground_y = self.window_width * 0.5, self.window_height * 0.6
            self.dialog_box = pygame.image.load("assets/dialog_box.png").convert_alpha()
            self.dialog_box = pygame.transform.scale(self.dialog_box, (self.window_width, 300))

        self.line = self.lines[index]
        self.text_pointer = 0
        self.line_sequence = ""
        self.character = self.characters[index]
        self.character_surface = self.character_obj.render(self.character, True, self.color)

    def render_line(self):
        if self.text_pointer < len(self.line):
            self.line_sequence += self.line[self.text_pointer]
            self.text_pointer += 1
        else:
            self.line_sequence = self.line

        if self.character == "Paypay":
            self.chat_surface = self.big_chat_obj.render(self.line_sequence, True, self.color)
        else:
            self.chat_surface = self.chat_obj.render(self.line_sequence, True, self.color)

    def isDone(self):
        return self.line_sequence == self.line

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        rect = self.foreground_image.get_rect(center=(self.foreground_x, self.foreground_y))
        screen.blit(self.foreground_image, rect)
        screen.blit(self.dialog_box, (0, 490))
        screen.blit(self.character_surface, self.character_pos)
        screen.blit(self.chat_surface, self.chat_pos)