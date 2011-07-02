# -*- coding: utf-8; -*-

import pygame
import traceback
from pygame.locals import *
from OpenGL.GL import *

event_table = {}

def event(type):
    def wrapper(func):
        event_table[type] = func
        return func
    return wrapper

class Game(object):
    def __init__(self, size, fullscreen=False):
        pygame.display.set_mode(size.xy(), OPENGL|DOUBLEBUF)
        pygame.display.set_caption('sporse runner')
        self._running = True

        glClearColor(1,0,1,1)

    def do_stuff(self):
        while self._running:
            try:
                self.poll()
                self.logic()
                self.render()
            except:
                traceback.print_exc()

    def poll(self):
        global event_table
        for event in pygame.event.get():
            func = event_table.get(event.type, None)
            if func is None:
                continue
            func(self, event)

    def logic(self):
        pass

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        pygame.display.flip()

    @event(pygame.QUIT)
    def on_quit(self, event):
        self._running = False
