# -*- coding: utf-8; -*-

import pygame
import traceback
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from vector import Vector2i

event_table = {}

def event(type):
    def wrapper(func):
        event_table[type] = func
        return func
    return wrapper

class Lost(Exception):
    pass

class Game(object):
    camera_height = 2
    camera_distance = 10
    framerate = 30

    colors = [
        (1,1,1,1),
        (1,1,0,1),
        (0,0,1,1),
        (0,1,1,1),
        (0,1,0,1),
        (1,0,0,1),
    ]

    def __init__(self, size, fullscreen=False):
        pygame.display.set_mode(size.xy(), OPENGL|DOUBLEBUF)
        pygame.display.set_caption('sporse runner')
        self._running = True

        glClearColor(1,0,1,1)
        glEnable(GL_DEPTH_TEST)

        self.on_resize(size=size)

    def stop(self):
        self._running = False

    def do_stuff(self):
        clock = pygame.time.Clock()
        while self._running:
            try:
                self.poll()
                self.logic()
                self.render()
            except Lost, e:
                print e
                break
            except:
                traceback.print_exc()

            clock.tick_busy_loop(Game.framerate)

    def poll(self):
        global event_table
        for event in pygame.event.get():
            func = event_table.get(event.type, None)
            if func is None:
                continue
            func(self, event)

    def logic(self):
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            player.x += 0.1
        if keys[K_d]:
            player.x -= 0.1
        if keys[K_w]:
            player.inc()
        if keys[K_s]:
            player.dec()
        if keys[K_SPACE]:
            player.jump()

        player.update()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, Game.camera_height, player.z - Game.camera_distance,
                  0, 0, player.z + 15,
                  0, 1, 0)

        player.render()

        h,w = map.shape
        for z, row in enumerate(map):
            glColor4f(*game.colors[z%4])
            for i, x in enumerate([-2, -1, 0, 1, 2]):
                if row[i] < 0.0:
                    continue

                p0 = (-0.5 + x, row[i], 0 + z)
                p1 = (-0.5 + x, row[i], 1 + z)
                p2 = ( 0.5 + x, row[i], 1 + z)
                p3 = ( 0.5 + x, row[i], 0 + z)
                p4 = ( 0.5 + x, -1, 0 + z)
                p5 = (-0.5 + x, -1, 0 + z)
                p6 = (-0.5 + x, -1, 1 + z)
                p7 = ( 0.5 + x, -1, 1 + z)

                glBegin(GL_QUADS)
                glColor4f(*game.colors[z%6])
                glVertex3f(*p0)
                glVertex3f(*p1)
                glVertex3f(*p2)
                glVertex3f(*p3)

                glColor4f(*[_*0.3 for _ in game.colors[z%6]])
                glVertex3f(*p0)
                glVertex3f(*p3)
                glVertex3f(*p4)
                glVertex3f(*p5)

                glVertex3f(*p0)
                glVertex3f(*p5)
                glVertex3f(*p6)
                glVertex3f(*p1)

                glVertex3f(*p3)
                glVertex3f(*p2)
                glVertex3f(*p7)
                glVertex3f(*p4)

                glEnd()

        pygame.display.flip()

    @event(pygame.KEYDOWN)
    def on_keydown(self, event):
        if event.key == K_ESCAPE:
            self.quit()

    @event(pygame.VIDEORESIZE)
    def on_resize(self, event=None, size=None):
        if event is not None:
            size = Vector2i(event.w, event.h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, size.ratio(), 0.001, 100)

    @event(pygame.QUIT)
    def on_quit(self, event):
        self.stop()
