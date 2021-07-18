import pygame
from src.event_manager import *


class GameEngine(object):
    """
    Tracks the game state.
    """

    def __init__(self, ev_mgr):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """

        self.ev_mgr = ev_mgr
        ev_mgr.register_listener(self)
        self.running = False
        self.state = StateMachine()

    def notify(self, event):
        """
        Called by an event in the message queue.
        """

        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, StateChangeEvent):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.ev_mgr.post(QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        self.ev_mgr.post(InitializeEvent())
        self.state.push(STATE_INTRO)
        while self.running:
            newTick = TickEvent()
            self.ev_mgr.post(newTick)

STATE_INTRO = 1
STATE_STORY = 2
STATE_INSTRUCTION = 3
STATE_ISLAND = 4
STATE_ADD = 5
STATE_BUILD = 6
STATE_HISTORY = 7
STATE_CODE = 8

class StateMachine(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """

    def __init__ (self):
        self.statestack = []

    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.statestack[-1]
        except IndexError:
            # empty stack
            return None

    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.statestack.pop()
            return len(self.statestack) > 0
        except IndexError:
            # empty stack
            return None

    def push(self, state):
        """
        Push a new state onto the stack.
        Returns the pushed value.
        """
        self.statestack.append(state)
        return state
