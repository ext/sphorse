# -*- coding: utf-8; -*-
import pygame
from game import Game
from player import Player
from vector import Vector2i

import numpy
map = numpy.array([
        [-1, -1,  0, -1, -1],
        [-1, -1,  0,  0, -1],
        [-1, -1,  0,  0, -1],
        [ 1, -1, -1,  0, -1],
        [ 1, -1, -1,  0, -1],
        [ 1, -1, -1,  1, -1],
        [ 1, -1, -1,  0, -1],
        [ 1, -1, -1,  0, -1],
        [ 1, -1, -1,  0, -1],
        [ 1, -1,  1,  0, 22.53],
        [ 1,  1,  1,  0,  0],
        [ 1,  1, -1,  0,  0],
        [ 1, -1, -1, -1,  0],
        [ 1, -1, -1, -1,  0],
        [ 1, -1, -1, -1,  0],
        [ 1, -1, -1, -1,  0],
        [ 1, -1, -1, -1,  0],
        [ 1, -1, -1, -1,  0],
        [ 0, -1, -1, -1,  0],
        [ 0, -1, -1, -1,  0],
        [ 0, -1, -1, -1,  0],
        [ 0, -1, -1, -1, -1],
        [ 0, -1, -1, -1, -1],
        [ 0, -1, -1, -1, -1],
        [ 0, -1, -1, -1,  0],
        [ 0,  0, -1, -1,  0],
        [ 0,  0, -1, -1,  0],
        [ 0,  0, -1,  0,  0],
        [ 0,  0, -1,  0,  0],
        [ 0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0],
        [-1,  4,  0,  4, -1],
        [-1,  5,  0,  5, -1],
        [-1,  4,  0,  4, -1],
        [-1,  5,  0,  5, -1],
        [-1,  4,  0,  4, -1],
        [-1,  5,  0,  5, -1],
        [-1,  4,  0,  4, -1],
        [-1,  4,  0,  4, -1],
        [-1,  3,  0,  3, -1],
        [-1,  3,  0,  3, -1],
        [-1,  2,  0,  2, -1],
        [-1,  2,  0,  2, -1],
        [-1,  1,  0,  1, -1],
        [-1,  1,  0,  1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  0, -1, -1],
        [-1, -1,  1, -1, -1],
        [-1, -1,  1, -1, -1],
        [-1, -1,  1, -1, -1],
        [-1, -1,  1, -1, -1],
        [-1, -1,  1, -1, -1],
        [-1, -1,  1, -1, -1],
        [-1, -1,  1, -1, -1],
        [-1, -1,  1, -1, -1],
        [-1, -1,  2, -1, -1],
        [-1, -1,  2, -1, -1],
        [-1, -1,  2, -1, -1],
        [-1, -1,  2, -1, -1],
        [-1, -1,  2, -1, -1],
        [-1, -1,  2, -1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  1.35,  1.41,   1.45, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  1,  0,  0, -1],
        [-1,  1,  0,  0, -1],
        [-1,  1,  0,  0, -1],
        [-1,  1,  0,  0, -1],
        [-1,  1,  1,  0, -1],
        [-1,  1,  1,  0, -1],
        [-1,  1,  1,  0, -1],
        [-1,  1,  1,  0, -1],
        [-1,  0,  1,  1, -1],
        [-1,  0,  1,  1, -1],
        [-1,  0,  1,  1, -1],
        [-1,  0,  1,  1, -1],
        [-1,  0,  0,  1, -1],
        [-1,  0,  0,  1, -1],
        [-1,  0,  0,  1, -1],
        [-1,  0,  0,  1, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],


        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],
        [-1, -1,  0,  0,  0],

        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],

        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],
        [ 0,  0,  0, -1, -1],

        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],
        [ 0,  0,  1, -1, -1],

])

if __name__ == '__main__':
    pygame.display.init()
    
    game = Game(size=Vector2i(800,600), fullscreen=False)

    __builtins__.game = game
    __builtins__.player = Player()
    __builtins__.map = map

    game.do_stuff()
