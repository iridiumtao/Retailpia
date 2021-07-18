import pygame
import src.model as model
from src.event_manager import *


class Keyboard(object):
    """
    Handles keyboard input.
    """

    def __init__(self, ev_mgr, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_mgr = ev_mgr
        ev_mgr.register_listener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.ev_mgr.post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.ev_mgr.post(StateChangeEvent(None))
                    else:
                        currentstate = self.model.state.peek()
                        if currentstate == model.STATE_INTRO:
                            self.key_down_intro(event)
                        if currentstate == model.STATE_STORY:
                            self.key_down_story(event)
                        if currentstate == model.STATE_INSTRUCTION:
                            self.key_down_instruction(event)
                        if currentstate == model.STATE_ISLAND:
                            self.key_down_island(event)
                        if currentstate == model.STATE_ADD:
                            self.key_down_add(event)
                        if currentstate == model.STATE_BUILD:
                            self.key_down_build(event)
                        if currentstate == model.STATE_HISTORY:
                            self.key_down_history(event)
                        if currentstate == model.STATE_CODE:
                            self.key_down_code(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_left_button_up(event)



    def key_down_intro(self, event):
        """
        Handles intro key events.
        """
        pass
        # if event.key == pygame.K_SPACE:
        #     self.ev_mgr.post(StateChangeEvent(model.STATE_INSTRUCTION))

    def key_down_story(self, event):
        """
        Handles story key events.
        """
        pass
        # if event.key == pygame.K_SPACE:
        #     self.ev_mgr.post(StateChangeEvent(model.STATE_INSTRUCTION))

    def key_down_instruction(self, event):
        """
        Handles instruction key events.
        """
        pass
        # if event.key == pygame.K_SPACE:
        #     self.ev_mgr.post(StateChangeEvent(model.STATE_ISLAND))

    def key_down_island(self, event):
        """
        Handles island key events.
        """

        self.ev_mgr.post(InputEvent(event.key, None))
        # if event.key == pygame.K_SPACE:
        #     self.ev_mgr.post(StateChangeEvent(model.STATE_ADD))

    def key_down_add(self, event):
        """
        Handles add key events.
        """

        # if event.key == pygame.K_SPACE:
        #     self.ev_mgr.post(StateChangeEvent(model.STATE_BUILD))
        self.ev_mgr.post(InputEvent(event.key, None))

    def key_down_build(self, event):
        """
        Handles build key events.
        """
        pass
        # if event.key == pygame.K_SPACE:
        #     self.ev_mgr.post(StateChangeEvent(model.STATE_HISTORY))

    def key_down_history(self, event):
        """
        Handles history key events.
        """
        pass
        # if event.key == pygame.K_SPACE:
        #     self.ev_mgr.post(StateChangeEvent(model.STATE_CODE))

    def key_down_code(self, event):
        """
        Handles code key events.
        """
        pass

    def mouse_left_button_up(self, event):
        """
        放開滑鼠傳送游標位置
        """
        self.ev_mgr.post(InputEvent(None, event.pos))

