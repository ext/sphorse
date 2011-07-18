# -*- coding: utf-8; -*-

import pygame
import traceback
import math
import sys
import json
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from vector import Vector2i
from sprite import Sprite
from hiscore import Hiscore

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
        (1.0, 0.0, 0.0, 1),
        (1.0, 0.3, 0.0, 1),
        (1.0, 0.5, 0.0, 1),
        (1.0, 0.8, 0.0, 1),
        (1.0, 1.0, 0.0, 1),
        (0.5, 1.0, 0.0, 1),
        (0.0, 1.0, 0.0, 1),
        (0.0, 1.0, 0.5, 1),
        (0.0, 1.0, 1.0, 1),
        (0.0, 0.5, 1.0, 1),
        (0.0, 0.0, 1.0, 1),
    ]

    def __init__(self, size, fullscreen=False):
        if len(sys.argv) < 2:
            print 'specify name as argument',
            sys.exit(1)

        for x in sys.argv:
            if x == '--score':
                self.print_hiscore()
                sys.exit(0)

        # Get name as unicode string
        self.name = sys.argv[1].decode(sys.getfilesystemencoding())

        flags = OPENGL|DOUBLEBUF
        if '--fullscreen' in sys.argv:
            flags |= FULLSCREEN

        pygame.display.set_mode(size.xy(), flags)
        pygame.display.set_caption('sporse runner')
        self._running = True

        glClearColor(0,0,0,1)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, (0,0,0,1))
        glFogf(GL_FOG_DENSITY, 1.0)
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogf(GL_FOG_START, 30.0)
        glFogf(GL_FOG_END, 45.0)
        glEnable(GL_FOG)

        # Play background "music" if audio was initialized properly.
        if pygame.mixer.get_init() is not None:
            self.music = pygame.mixer.Sound('nyan.wav')
            self.music.play(loops=-1)

        self.goal = Sprite('goal.png', 1)

        self.on_resize(size=size)

    def stop(self):
        self._running = False

    def do_stuff(self):
        clock = pygame.time.Clock()
        timer = pygame.time.get_ticks()
        while self._running:
            try:
                self.poll()
                self.logic()
                self.render()
            except Lost, e:
                print e
                break
            except GLError:
                traceback.print_exc()
                self.stop()
            except:
                traceback.print_exc()

            clock.tick_busy_loop(Game.framerate)

        t = ((pygame.time.get_ticks() - timer) / 1000)
        d = math.floor(player.z)
        self.hiscore(self.name, t,d)

    def hiscore(self, name, t, d):
        score = Hiscore('.score', '')
        score.add(name, distance=d, time=t)
        score.store()

        print 'Total time: %ds' % t
        print 'Total distance: %dm' % d
        if score.placement > 0 and score.placement < 10:
            print 'Placement: %d' % (score.placement+1)
        print
        score.print_local()

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
            player.left()
        if keys[K_d] or keys[K_e]:
            player.right()
        if keys[K_w] or keys[K_COMMA]:
            player.inc()
        if keys[K_s] or keys[K_o]:
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

        glPushAttrib(GL_ENABLE_BIT)
        glDisable(GL_TEXTURE_2D)
        h,w = map.shape
        my =  max(int(player.z)-10, 0)

        if int(player.z) > h:
            self.stop()
            return

        glPushAttrib(GL_ENABLE_BIT)
        glDisable(GL_DEPTH_TEST)
        glColor4f(1,1,1,1)
        glBegin(GL_POINTS)
        for seed in range(my, int(player.z) + 200):
            random.seed(seed)
            x = (random.random() - 0.5) * 25.0
            y = (random.random() - 0.5) * 25.0
            glVertex3f(x, y, seed)

        glEnd()
        glPopAttrib()

        # goal
        glPushAttrib(GL_ENABLE_BIT)
        glEnable(GL_TEXTURE_2D)
        self.goal.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(1,0)
        glVertex3f(-3.0, 3.5, 999)

        glTexCoord2f(0,0)
        glVertex3f( 3.0, 3.5, 999)

        glTexCoord2f(0,1)
        glVertex3f( 3.0,   0, 999)

        glTexCoord2f(1,1)
        glVertex3f(-3.0,   0, 999)
        glEnd()
        glPopAttrib()

        # load map region
        region = map[my:my+50]
        
        # Take region, enumerate it (so it knows which part it is currently
        # rendering) and reverse it so it can be rendered back-to-front for
        #  - Performance
        #  - Reduces artifacts on poor GPUs which might render black artifacts
        #    on the edges.
        tmp = reversed(list(enumerate(region)))
        
        for z, row in tmp:
            z += my
            for i, x in enumerate([-2, -1, 0, 1, 2]):
                if row[i] < 0.0:
                    continue

                tmp = [math.floor(row[i])]
                if row[i] - math.floor(row[i]) > 0:
                    tmp.append((row[i] - math.floor(row[i])) * 100)

                for y in tmp:
                    hs = int(y) / 10 - 1
                    he = int(y) % 10 + (hs+1)

                    p0 = (-0.5 + x, he, 0 + z)
                    p1 = (-0.5 + x, he, 1 + z)
                    p2 = ( 0.5 + x, he, 1 + z)
                    p3 = ( 0.5 + x, he, 0 + z)
                    p4 = ( 0.5 + x, hs, 0 + z)
                    p5 = (-0.5 + x, hs, 0 + z)
                    p6 = (-0.5 + x, hs, 1 + z)
                    p7 = ( 0.5 + x, hs, 1 + z)
                    
                    lcolor = game.colors[z%len(game.colors)]
                    dcolor = [i < 3 and c*0.3 or c for i,c in enumerate(lcolor)]
                    
                    glBegin(GL_QUADS)
                    glColor4f(*lcolor)
                    
                    # Top face
                    glVertex3f(*p0)
                    glVertex3f(*p1)
                    glVertex3f(*p2)
                    glVertex3f(*p3)

                    # Bottom face
                    glVertex3f(*p6)
                    glVertex3f(*p5)
                    glVertex3f(*p4)
                    glVertex3f(*p7)
                    
                    glColor4f(*dcolor)
                    
                    # Front face
                    glVertex3f(*p0)
                    glVertex3f(*p3)
                    glVertex3f(*p4)
                    glVertex3f(*p5)
                    
                    # Right face
                    glVertex3f(*p0)
                    glVertex3f(*p5)
                    glVertex3f(*p6)
                    glVertex3f(*p1)

                    # Left face
                    glVertex3f(*p3)
                    glVertex3f(*p2)
                    glVertex3f(*p7)
                    glVertex3f(*p4)
                    
                    glEnd()
        glPopAttrib()

        player.render()

        pygame.display.flip()

    @event(pygame.KEYDOWN)
    def on_keydown(self, event):
        if event.key == K_ESCAPE:
            self.stop()

    @event(pygame.KEYUP)
    def on_keyup(self, event):
        if event.key == K_SPACE:
            player.unjump()

    @event(pygame.VIDEORESIZE)
    def on_resize(self, event=None, size=None):
        if event is not None:
            size = Vector2i(event.w, event.h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, size.ratio(), 0.1, 200)

    @event(pygame.QUIT)
    def on_quit(self, event):
        self.stop()
