import pygame
import random
import time
from src.event_manager import *
from src.local_config import LocalConfig
import src.model as model
from src.models import story
from src.models import society
from src.models import button
from src.models import input_box
from src.models import island
from src.models import code
from src.models import show_history
from src.models import instruction
from src.models import interface
from src.models import message
from src import save

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, ev_mgr, model):
        """
        ev_mgr (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        """

        self.ev_mgr = ev_mgr
        ev_mgr.register_listener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.mouse_pos = (0, 0)

        self.local_config = None
        self.line_index = 0
        self.key = 0

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, InitializeEvent):
            self.initialize()
            self.create_all_objects()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_INTRO:
                self.render_intro()
            if currentstate == model.STATE_STORY:
                self.render_story()
            if currentstate == model.STATE_INSTRUCTION:
                self.render_instruction()
            if currentstate == model.STATE_ISLAND:
                self.render_island()
            if currentstate == model.STATE_ADD:
                self.render_add()
            if currentstate == model.STATE_BUILD:
                self.render_build()
            if currentstate == model.STATE_HISTORY:
                self.render_history()
            if currentstate == model.STATE_CODE:
                self.render_code()
            self.clock.tick(60)
        elif isinstance(event, InputEvent):
            currentstate = self.model.state.peek()
            if event.click_pos is not None:
                self.mouse_pos = event.click_pos
            if currentstate == model.STATE_ISLAND:
                if event.char == pygame.K_q:
                    self.delete_house(3)
                if event.char == pygame.K_w:
                    self.delete_house(1)
                if event.char == pygame.K_e:
                    self.delete_house(0)
                if event.char == pygame.K_a:
                    self.delete_house(6)
                if event.char == pygame.K_s:
                    self.delete_house(4)
                if event.char == pygame.K_d:
                    self.delete_house(2)
                if event.char == pygame.K_z:
                    self.delete_house(8)
                if event.char == pygame.K_x:
                    self.delete_house(7)
                if event.char == pygame.K_c:
                    self.delete_house(5)
            if currentstate == model.STATE_STORY:
                if not(self.story.isDone()):
                    # 跳過逐一印文字，直接印整行文字
                    self.story.text_pointer = len(self.story.line)
                elif self.line_index < len(self.story.lines) - 1:
                    # 下一行文字
                    self.story.select_line(self.line_index + 1)
                    self.line_index += 1
                elif self.line_index == len(self.story.lines) - 1:
                    # 對話結束自動換State
                    self.line_index = 0
                    self.skip_story_sub()
            if currentstate == model.STATE_ADD:
                self.key = event.char
            if currentstate == model.STATE_CODE:
                pass
            print('self.mouse_pos:' + str(self.mouse_pos))


    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        self.local_config = LocalConfig()
        resolution_width, resolution_height, screen_flags, display_index, vsync = self.local_config.load_screen_config()

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('RETAILPIA')
        self.screen = pygame.display.set_mode(size = (resolution_width, resolution_height),
                                              flags = screen_flags,
                                              display = display_index,
                                              vsync = vsync)
        self.window_width, self.window_height = pygame.display.get_window_size()
        self.clock = pygame.time.Clock()
        self.isinitialized = True

        # background
        self.background_image = pygame.image.load("assets/background.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.window_width, self.window_height))
        self.island_image = pygame.image.load("assets/3x3island.png").convert_alpha()
        self.island_image = self.scale_keep_aspect_ratio(self.island_image, height = self.window_height * 0.8)

    def scale_keep_aspect_ratio(self, image, width = 100000, height = 100000):

        ref_width, ref_height = image.get_size()
        # 鎖定長寬比，參考長、寬數值較大者進行縮放
        if width <= height:
            height = int(width * ref_height / ref_width)
        else:
            width = int(height * ref_width / ref_height)
        image = pygame.transform.scale(image, (int(width), int(height)))
        return image

    def create_all_objects(self):
        '''
        建立每種畫面需要的物件
        '''

        self.create_share_objects()
        # intro page
        self.create_intro_objects()
        # story page
        self.create_story_objects()
        # instruction page
        self.create_instruction_objects()
        # island page
        self.create_island_objects()
        # add page
        self.create_add_objects()
        # build page
        self.create_build_objects()
        # history page
        self.create_history_objects()

        # code page
        self.create_code_objects()

    def create_share_objects(self):
        # share
        self.help_btn = button.Button(1120, 50, 100, 0, "assets/help_button.png", True)  # used by island, add, history, code
        self.return_btn = button.Button(50, 50, 100, 0, "assets/return_button.png", True)  # used by add, history, code

    def create_intro_objects(self):
        self.intro_objs = pygame.sprite.Group()

        self.start_btn = button.Button(1040, 540, 200, 0, "assets/start_button.png", True)
        self.intro_objs.add(self.start_btn)

    def create_story_objects(self):
        self.story_objs = pygame.sprite.Group()
        self.skip_btn = button.Button(1040, 50, 180, 0, "assets/skip_button.png", True)
        self.story_objs.add(self.skip_btn)

        self.story = story.Story(100, 620, 1280, 720)

    def create_instruction_objects(self):
        self.instruction_objs = pygame.sprite.Group()

        self.instruction_objs.add(self.return_btn)

        self.story_btn = button.Button(1040, 50, 180, 0, "assets/story_button.png", True)
        self.instruction_objs.add(self.story_btn)
        self.small_add_btn = button.Button(705, 320, 70, 0, "assets/add_button.png", True)
        self.instruction_objs.add(self.small_add_btn)
        self.small_history_btn = button.Button(880, 440, 70, 0, "assets/history_button.png", True)
        self.instruction_objs.add(self.small_history_btn)

        self.instruction = instruction.Instruction(90, 200)
        self.instruction_interface = interface.Interface(1220, 540, "assets/help_box.png", height_offset = 75)

        self.ori_island = island.Island()

    def create_island_objects(self):
        self.island_objs = pygame.sprite.Group()

        self.island_objs.add(self.help_btn)
        self.history_btn = button.Button(1120, 500, 100, 0, "assets/history_button.png", True)
        self.island_objs.add(self.history_btn)
        self.add_btn = button.Button(1120, 600, 100, 0, "assets/add_button.png", True)
        self.island_objs.add(self.add_btn)

        self.lands = []
        self.societies = []
        self.societies_2nd_floor = []
        self.societies_3rd_floor = []

        # for 3x3
        society_positions = [(583, 144), (479, 210), (686, 204), (375, 272), (582, 271), (793, 266), (477, 334), (690, 330), (580, 392)]

        self.society_num = len(society_positions)

        self.society_objs = pygame.sprite.LayeredUpdates()

        for i in range(self.society_num):
            x, y = society_positions[i][0], society_positions[i][1]

            # 載入所有預設建築
            self.lands.append(society.Society(x-7, y+30, w=125, h=85, layer=0))
            self.lands[i].set_type(society.Society.LAND)
            self.lands[i].show()
            self.societies.append(society.Society(x, y, layer=i*10))
            self.societies_2nd_floor.append(society.Society(x, y-38, floor=1, layer=10*i+1))
            self.societies_3rd_floor.append(society.Society(x, y-76, floor=2, layer=10*i+2))
            # print(f"({x}, {y})")


        society_dict = {
            "society_0" : self.societies,
            "society_1" : self.societies_2nd_floor,
            "society_2" : self.societies_3rd_floor,
        }
        society_dict = save.restore(society_dict)


        self.society_objs.add(self.lands)

        if society_dict is not None:
            print("society json is not None")
            for society_key, society_value in society_dict.items():
                self.society_objs.add(society_value)
        else:
            # 自動將所有房子加入
            print("society json is None")
            self.society_objs.add(self.societies)
            self.society_objs.add(self.societies_2nd_floor)
            self.society_objs.add(self.societies_3rd_floor)
            self.save_society()

        # 作為測試用，自動長出一個房子
        # self.societies[0].show()

    def create_add_objects(self):
        self.add_objs = pygame.sprite.Group()

        self.input_name = input_box.Input_box(int((1280-200)/2), 244, 140, 32, "Name")
        self.input_brand = input_box.Input_box(int((1280-200)/2), 294, 140, 32, "Brand")
        self.input_money = input_box.Input_box(int((1280-200)/2), 344, 140, 32, "Pounds")  # let's go British!
        self.input_code = input_box.Input_box(int((1280-200)/2), 394, 140, 32, "Code")
        self.input_type = input_box.Input_box(int((1280-200)/2), 444, 140, 32, "Type")

        self.add_objs.add(self.return_btn)
        self.add_objs.add(self.help_btn)
        self.submit_btn = button.Button(1120, 600, 100, 0, "assets/submit_button.png", True)
        self.add_objs.add(self.submit_btn)

        self.add_interface = interface.Interface(300, 350, "assets/ui_box.png")

    def create_build_objects(self):
        self.build_objs = pygame.sprite.Group()

        self.build_message = message.Message(50, 40, "Choose a land or building to upgrade!")

    def create_history_objects(self):
        self.history_objs = pygame.sprite.Group()

        self.history_name = show_history.Show_history("Name")
        self.history_name.read_data()
        self.history_brand = show_history.Show_history("Brand")
        self.history_brand.read_data()
        self.history_Pounds = show_history.Show_history("Pounds")
        self.history_Pounds.read_data()
        self.history_code = show_history.Show_history("Code")
        self.history_code.read_data()
        self.history_type = show_history.Show_history("Type")
        self.history_type.read_data()

        self.history_objs.add(self.return_btn)
        self.history_objs.add(self.help_btn)

        self.history_interface = interface.Interface(850, 600, "assets/ui_box.png")

    def create_code_objects(self):
        self.code_objs = pygame.sprite.Group()

        self.code_objs.add(self.return_btn)
        self.code_objs.add(self.help_btn)
        self.code_objs.add(self.submit_btn)

        self.code = code.Code()
        self.code_interface = interface.Interface(250, 100, "assets/ui_box.png")

    def render_intro(self):
        """
        Render the game intro.
        """

        self.start_btn.set_focus(self.start_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.start_btn.rect.collidepoint(self.mouse_pos):
            print("按下「enter按鈕」")
            # 首次遊玩自動進story
            if self.local_config.skip_story:
                self.ev_mgr.post(StateChangeEvent(model.STATE_ISLAND))
            else:
                self.line_index = 0
                self.story.select_line(self.line_index)
                self.ev_mgr.post(StateChangeEvent(model.STATE_STORY))

        self.draw_all(self.intro_objs)

    def render_story(self):
        """
        Render the game story.
        """

        self.skip_btn.set_focus(self.skip_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.skip_btn.rect.collidepoint(self.mouse_pos):
            print("按下「skip按鈕」")
            self.skip_story_sub()
        self.story.render_line()
        self.draw_all((self.story, self.story_objs))

    def render_instruction(self):
        """
        Render the game instruction.
        """

        self.story_btn.set_focus(self.story_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.story_btn.rect.collidepoint(self.mouse_pos):
            print("按下「Story again按鈕」")
            self.line_index = 0
            self.story.select_line(self.line_index)
            self.ev_mgr.post(StateChangeEvent(model.STATE_STORY))

        self.return_btn.set_focus(self.return_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.return_btn.rect.collidepoint(self.mouse_pos):
            print("按下「return按鈕」")
            self.ev_mgr.post(StateChangeEvent(None))

        self.draw_all((self.ori_island, self.instruction_interface, self.instruction, self.instruction_objs))

    def render_island(self):
        """
        Render the game island.
        """

        self.help_btn.set_focus(self.help_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.help_btn.rect.collidepoint(self.mouse_pos):
            print("按下「help按鈕」")
            self.ev_mgr.post(StateChangeEvent(model.STATE_INSTRUCTION))

        self.history_btn.set_focus(self.history_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.history_btn.rect.collidepoint(self.mouse_pos):
            print("按下「history按鈕」")
            self.ev_mgr.post(StateChangeEvent(model.STATE_HISTORY))

        self.add_btn.set_focus(self.add_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.add_btn.rect.collidepoint(self.mouse_pos):
            print("按下「add按鈕」")
            self.ev_mgr.post(StateChangeEvent(model.STATE_ADD))

        # 測試刪除房子
        # self.society_objs.remove(self.societies_3rd_floor[2])
        # self.society_objs.remove(self.societies_3rd_floor[6])
        # self.society_objs.remove(self.societies_2nd_floor[6])

        focused_societies = []
        selected_societies = []

        for i in range(self.society_num):
            # 建築物被 focus 的處理(建築物會放大)
            if self.societies[i].rect.collidepoint(pygame.mouse.get_pos()) or \
                    self.societies_2nd_floor[i].rect.collidepoint(pygame.mouse.get_pos()) or \
                    self.lands[i].rect.collidepoint(pygame.mouse.get_pos()):
                focused_societies.append(i)

            # 建築物被點擊的處理
            if self.societies[i].rect.collidepoint(self.mouse_pos) or \
                    self.societies_2nd_floor[i].rect.collidepoint(self.mouse_pos):
                print(f"Island按下「{i}號房子」, level = {self.societies[i].level}")
                self.mouse_pos = (0, 0)
                selected_societies.append(i)

            # 建築物被 focus 的處理(建築物會放大)
            self.lands[i].set_focused(False)
            self.societies[i].set_focused(False)
            self.societies_2nd_floor[i].set_focused(False)
            self.societies_3rd_floor[i].set_focused(False)

        # 選擇的建築，取ID最大的執行
        if selected_societies:
            i = max(selected_societies)
            # 顯示折扣碼
            if self.societies[i].level == 2 or \
                    self.societies_2nd_floor[i].level == 2 or \
                    self.societies_3rd_floor[i].level == 2:
                self.code.update(i)  # 更新code
                self.ev_mgr.post(StateChangeEvent(model.STATE_CODE))

        # print(focused_societies)
        if focused_societies:
            i = max(focused_societies)
            self.lands[i].set_focused(True)
            self.societies[i].set_focused(True)
            self.societies_2nd_floor[i].set_focused(True)
            self.societies_3rd_floor[i].set_focused(True)


        self.draw_all((self.society_objs, self.island_objs))

    def render_add(self):
        """
        Render the game add.
        """

        self.input_name.update()
        self.input_name.enter(self.mouse_pos, self.key)
        self.input_brand.update()
        self.input_brand.enter(self.mouse_pos, self.key)
        self.input_money.update()
        self.input_money.enter(self.mouse_pos, self.key)
        self.input_code.update()
        self.input_code.enter(self.mouse_pos, self.key)
        self.input_type.update()
        self.input_type.enter(self.mouse_pos, self.key)
        self.key = None  # prevent duplicate input

        self.return_btn.set_focus(self.return_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.return_btn.rect.collidepoint(self.mouse_pos):
            print("按下「return按鈕」")
            self.ev_mgr.post(StateChangeEvent(None))

        self.help_btn.set_focus(self.help_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.help_btn.rect.collidepoint(self.mouse_pos):
            print("按下「help按鈕」")
            self.ev_mgr.post(StateChangeEvent(model.STATE_INSTRUCTION))

        self.submit_btn.set_focus(self.submit_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.submit_btn.rect.collidepoint(self.mouse_pos):
            print("按下「submit按紐」")
            self.input_name.record(cache=False)
            self.input_name.clear_cache()
            self.ev_mgr.post(StateChangeEvent(model.STATE_BUILD))

        self.draw_all((self.society_objs, self.add_interface, self.add_objs, self.input_name, self.input_brand, self.input_money, self.input_code, self.input_type))

    def render_build(self):
        """
        Render the game build.
        """

        selected_societies = []
        focused_societies = []
        succeed = None

        self.return_btn.set_focus(self.return_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.return_btn.rect.collidepoint(self.mouse_pos):
            self.ev_mgr.post(StateChangeEvent(None))

        current_mouse_pos = pygame.mouse.get_pos()

        for i in range(self.society_num):
            # 建築物被 focus 的處理(建築物會放大)
            if self.societies[i].rect.collidepoint(current_mouse_pos) or \
                    self.societies_2nd_floor[i].rect.collidepoint(current_mouse_pos) or \
                    self.lands[i].rect.collidepoint(current_mouse_pos):
                focused_societies.append(i)

            # 建築物被點擊的處理
            # 新增建築物
            if self.societies[i].rect.collidepoint(self.mouse_pos) or \
                    self.societies_2nd_floor[i].rect.collidepoint(self.mouse_pos) or \
                    self.lands[i].rect.collidepoint(self.mouse_pos):
                print(f"Build按下「{i}號房子」")
                selected_societies.append(i)

            self.lands[i].set_focused(False)
            self.societies[i].set_focused(False)
            self.societies_2nd_floor[i].set_focused(False)
            self.societies_3rd_floor[i].set_focused(False)

        # 選擇的建築，取ID最大的執行
        if selected_societies:
            i = max(selected_societies)
            type = self.history_brand.get_last()
            succeed = self.society_upgrade(i, type)
            print(f"succeed = {succeed}")

        # focus 的建築，取ID最大的執行
        if focused_societies:
            i = max(focused_societies)
            self.lands[i].set_focused(True)
            self.societies[i].set_focused(True)
            self.societies_2nd_floor[i].set_focused(True)
            self.societies_3rd_floor[i].set_focused(True)

        self.mouse_pos = (0, 0)

        if succeed:
            self.save_society()
            # 狀態機 pop 兩次
            self.ev_mgr.post(StateChangeEvent(None))
            self.ev_mgr.post(StateChangeEvent(None))

        self.draw_all((self.build_objs, self.society_objs, self.build_message))

    def society_upgrade(self, i, type):
        """
        建築升級處理
        判斷現在幾樓

        如果是與該建築下方的建築是「不同」種類的
        蓋一棟新的1級建築

        如果是與該建築下方的建築是「相同」種類的
        升級一棟建築

        詳細訊息見print()資訊

        以下註解樓層數為 0, 1, 2，變數為societies, 2nd_floor, 3rd_floor
        """
        succeed = False

        # 三個樓層都 show 的話直接 FALSE
        if (self.societies[i].isshow
            and self.societies_2nd_floor[i].isshow
                and self.societies_3rd_floor[i].isshow):
            return False

        if (self.societies_2nd_floor[i].isshow
            and self.societies_2nd_floor[i].level == 0
                and self.societies_2nd_floor[i].type != type):
            print(f"{i}號房子1樓，建造2樓，類型為：{type}")
            succeed = self.societies_3rd_floor[i].show(type)
            return succeed

        if (self.societies[i].isshow
            and self.societies[i].level == 1
                and self.societies[i].type != type):
            print(f"{i}號房子0樓，建造2樓，類型為：{type}")
            succeed = self.societies_3rd_floor[i].show(type)
            return succeed

        if (self.societies_2nd_floor[i].isshow
            and self.societies_2nd_floor[i].level == 0
                and self.societies_2nd_floor[i].type == type):
            print(f"{i}號房子1樓，升級，相同類型")
            succeed = self.societies_2nd_floor[i].level_up()
            return succeed

        if (self.societies[i].isshow
            and self.societies[i].level != 2
                and self.societies[i].type == type):
            print(f"{i}號房子0樓，升級，相同類型")
            succeed = self.societies[i].level_up()
            return succeed

        if (self.societies[i].isshow
            and self.societies[i].level == 0
                and self.societies[i].type != type):
            print(f"{i}號房子0樓，建造1樓，類型為：{type}")
            succeed = self.societies_2nd_floor[i].show(type)
            return succeed

        # 若無0樓，則加入0樓
        if not self.societies[i].isshow:
            succeed = self.societies[i].show(type)
            print(f"{i}號房子0樓加入，類型為{type}")
            return succeed

        return succeed

    def save_society(self):
        society_dict = {
            "society_0" : self.societies,
            "society_1" : self.societies_2nd_floor,
            "society_2" : self.societies_3rd_floor,
        }
        save.save(society_dict)

    def render_history(self):
        """
        Render the game history.
        """

        self.return_btn.set_focus(self.return_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.return_btn.rect.collidepoint(self.mouse_pos):
            print("按下「return按鈕」")
            self.ev_mgr.post(StateChangeEvent(None))

        self.help_btn.set_focus(self.help_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.help_btn.rect.collidepoint(self.mouse_pos):
            print("按下「help按鈕」")
            self.ev_mgr.post(StateChangeEvent(model.STATE_INSTRUCTION))

        self.draw_all((self.society_objs, self.history_interface, self.history_objs, self.history_name, self.history_brand, self.history_Pounds, self.history_code, self.history_type))

    def render_code(self):
        """
        Render the game code.
        """

        self.return_btn.set_focus(self.return_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.return_btn.rect.collidepoint(self.mouse_pos):
            print("按下「return按鈕」")
            self.ev_mgr.post(StateChangeEvent(None))

        self.help_btn.set_focus(self.help_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.help_btn.rect.collidepoint(self.mouse_pos):
            print("按下「help按鈕」")
            self.ev_mgr.post(StateChangeEvent(model.STATE_INSTRUCTION))

        self.submit_btn.set_focus(self.submit_btn.rect.collidepoint(pygame.mouse.get_pos()))
        if self.submit_btn.rect.collidepoint(self.mouse_pos):
            print("按下「submit按紐」")
            self.mouse_pos = (0, 0)
            code = input("Enter the code here: ")
            if code == self.code.code_text:
                print("success")
                # 刪除那棟房子
                self.ev_mgr.post(StateChangeEvent(None))
                self.delete_house(self.code.society_num)
            else:
                print("failure")

        self.draw_all((self.society_objs, self.code_objs, self.code_interface, self.code))

    def delete_house(self, num):
        self.societies[num].clear_society()
        self.societies_2nd_floor[num].clear_society()
        self.societies_3rd_floor[num].clear_society()
        self.save_society()

    def skip_story_sub(self):
        # 首次遊玩自動進story後，更新config.ini
        if self.local_config.skip_story:
            self.ev_mgr.post(StateChangeEvent(None))
        else:
            self.local_config.config['GAME']['skip_story'] = 'TRUE'
            self.local_config.save_config()
            self.local_config.load_game_config()
            self.ev_mgr.post(StateChangeEvent(None))
            self.ev_mgr.post(StateChangeEvent(model.STATE_ISLAND))

    def draw_all(self, objects):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (0, 0))
        x, y = self.window_width * 0.5, self.window_height * 0.6
        rect = self.island_image.get_rect(center=(x, y))
        self.screen.blit(self.island_image, rect)

        # 若輸入為list或tuple則逐一draw到螢幕上
        if isinstance(objects, tuple) or isinstance(objects, list):
            for object in objects:
                object.draw(self.screen)
        else:
            objects.draw(self.screen)

        pygame.display.flip()
