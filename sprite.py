# -*- coding: utf-8; -*-

import pygame
from OpenGL.GL import *
from os.path import join

class Sprite(object):
    def __init__(self, filename, frames):
        self.filename = filename
        self.frames = frames

        self.load_texture()

    def load_texture(self):
        fp = open(join('textures', self.filename), 'rb')
        surface = pygame.image.load(fp).convert_alpha()
        data = pygame.image.tostring(surface, "RGBA", 0)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data );
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        self.texture = texture

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    def index(self, i):
        x = i % self.frames;
        y = i / self.frames;

        w = 1.0 / self.frames;
        h = 1.0

        a = (x * w,   y * h)
        b = (x * w,   y * h + h)
        c = (x * w+w, y * h +h)
        d = (x * w+w, y * h)
        return a,b,c,d
