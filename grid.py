# -*- coding: utf-8 -*-
# Copyright (c) 2009-11 Walter Bender
# Copyright (c) 2012 Ignacio Rodríguez
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

import pygtk
pygtk.require('2.0')
from gi.repository import Gtk, Gdk, GObject
import os.path

from random import uniform
from sprites import Sprite
from card import Card, load_image

CARD_DEFS = ((1, 3, -2, -3), (2, 3, -3, -2), (2, 3, -4, -4), 
             (2, 1, -1, -4), (3, 4, -4, -3), (4, 2, -1, -2), 
             (1, 1, -2, -4), (4, 2, -3, -4), (1, 3, -1, -2))


#
# Class for defining 3x3 matrix of cards
#
class Grid:
    """
    Grid positions correspond to one of:
    012  01x  012  01x
    345  34x  345  34x
    678  xxx  xxx  67x
    """
    def __init__(self, game):
        self.grid = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.card_table = []
        self.mask_table = []
        # Stuff to keep around for the graphics
        self.w = int(game.width)
        self.h = int(game.height)
        self.d = int(game.card_dim * game.scale)
        self.s = game.scale
        # Initialize the cards
        i = 0 # i is used as a label on the sprite
        for c in CARD_DEFS:
            x, y = self.i_to_xy(i)
            self.card_table.append(Card(game, c, i, x, y))
            i += 1
        # Initialize the masks (We need up to 6 of each one.)
        for i in range(4):
            bitmap = load_image(
                os.path.join(game.path, 'mask%dh.svg' % (i)),
                120 * game.scale, 48 * game.scale)
            for j in range(6):
                x, y = self.mh_to_xy(j)
                self.mask_table.append(Sprite(game.sprites, x, y, bitmap))
            bitmap = load_image(
                os.path.join(game.path, 'mask%dv.svg' % (i)),
                48 * game.scale, 120 * game.scale)
            for j in range(6):
                x, y = self.mv_to_xy(j)
                self.mask_table.append(Sprite(game.sprites, x, y, bitmap))
        self.hide_masks()

    # Utility functions
    def i_to_xy(self, i):
        return int((self.w - (self.d * 3)) / 2) + (i % 3) * self.d, \
               int((self.h - (self.d * 3)) / 2) + int(i / 3) * self.d

    def mh_to_xy(self, i):
        return int((self.w - (self.d * 3)) / 2 + \
                       ((i % 2) + 1) * self.d - 60 * self.s), \
               int((self.h - (self.d * 3)) / 2 + \
                       (int(i / 2) + .5) * self.d - 24 * self.s)

    def mv_to_xy(self, i):
        return int((self.w - (self.d * 3)) / 2 + \
                       ((i % 3) + .5) * self.d - 24 * self.s), \
               int((self.h - (self.d * 3)) / 2 + \
                       (int(i / 3) + 1) * self.d - 60 * self.s)

    def xy_to_i(self, x, y):
        return (x - int((self.w - (self.d * 3)) / 2)) / self.d  + \
               ((y - int((self.h - (self.d * 3)) / 2)) / self.d) * 3

    def set_orientation(self, neworientation, draw_card=True):
        for c in range(9):
            self.card_table[c].set_orientation(neworientation[c], draw_card)

    def randomize_orientation(self, draw_card=True):
        olist = [0, 90, 180, 270]
        for c in range(9):
            o = int(uniform(0, 4))
            self.card_table[c].set_orientation(olist[o], draw_card)

    def set_grid(self, newgrid):
        for i, c in enumerate(newgrid):
            x, y = self.i_to_xy(i)
            self.card_table[c].spr.move((x, y))
            self.grid[i] = c

    def show_all(self):
        for i in range(9):
            self.card_table[i].spr.set_layer(100)

    def hide_list(self, list):
        for i in list:
            self.card_table[i].spr.hide()

    def hide_masks(self):
        for i in self.mask_table:
            i.hide()

    # Reset everything to initial layout
    def reset3x3(self, game):
        self.show_all()
        self.hide_masks()
        self.set_grid([0, 1, 2, 3, 4, 5, 6, 7, 8])
        self.randomize_orientation()
        self.hide_masks()
        self.test3x3()

    # Two by two = ((7, 5, 0, 3), (7, 4, 5, 2), (1, 3, 5, 8), (4, 5, 6, 1))
    def reset2x2(self, game):
        self.show_all()
        self.hide_masks()
        self.randomize_orientation()
        r = int(uniform(0, 4))
        if r == 0:
            self.set_grid([7, 5, 1, 0, 3, 2, 4, 6, 8])
            self.hide_list([1, 2, 4, 6, 8])
        elif r == 1:
            self.set_grid([7, 4, 1, 5, 2, 3, 0, 6, 8])
            self.hide_list([0, 1, 3, 6, 8])
        elif r == 2:
            self.set_grid([1, 3, 2, 5, 8, 4, 6, 7, 0])
            self.hide_list([2, 4, 6, 7, 0])
        else:
            self.set_grid([4, 5, 0, 6, 1, 2, 3, 7, 8])
            self.hide_list([0, 2, 3, 7, 8])
        self.hide_masks()
        self.test2x2()

    # Three by two = ((7, 5, 0, 2, 4, 3), (5, 6, 1, 4, 3, 8))
    def reset3x2(self, game):
        self.show_all()
        self.hide_masks()
        self.randomize_orientation()
        r = int(uniform(0, 2))
        if r == 0:
            self.set_grid([7, 5, 0, 2, 4, 3, 1, 6, 8])
            self.hide_list([1, 6, 8])
        else:
            self.set_grid([5, 6, 1, 4, 3, 8, 0, 2, 7])
            self.hide_list([0, 2, 7])
        self.hide_masks()
        self.test3x2()

    # Two by three = ((5, 2, 4, 6, 1, 7), (7, 1, 2, 5, 8, 0))
    # reset everything to initial layout
    def reset2x3(self, game):
        self.show_all()
        self.hide_masks()
        self.randomize_orientation()
        r = int(uniform(0, 2))
        if r == 0:
            self.set_grid([5, 2, 0, 4, 6, 3, 1, 7, 8])
            self.hide_list([0, 3, 8])
        else:
            self.set_grid([7, 1, 3, 2, 5, 4, 8, 0, 6])
            self.hide_list([3, 4, 6])
        self.hide_masks()
        self.test2x3()

    # swap card a and card b
    # swap their entries in the grid and the position of their sprites
    def swap(self, a, b):
        # swap grid elements and x, y positions of sprites
        # print "swapping cards " + str(a) + " and " + str(b)
        ai = self.grid.index(a)
        bi = self.grid.index(b)
        self.grid[bi] = a
        self.grid[ai] = b
        ax, ay = self.card_table[a].spr.get_xy()
        bx, by = self.card_table[b].spr.get_xy()
        self.card_table[a].spr.move((bx, by))
        self.card_table[b].spr.move((ax, ay))

    # print the grid
    def print_grid(self):
        print self.grid[0:3]
        print self.grid[3:6]
        print self.grid[6:9]
        return

    # print the grid orientations
    def print_orientations(self):
        print self.card_table[self.grid[0]].orientation, \
              self.card_table[self.grid[1]].orientation, \
              self.card_table[self.grid[2]].orientation 
        print self.card_table[self.grid[3]].orientation, \
              self.card_table[self.grid[4]].orientation, \
              self.card_table[self.grid[5]].orientation 
        print self.card_table[self.grid[6]].orientation, \
              self.card_table[self.grid[7]].orientation, \
              self.card_table[self.grid[8]].orientation 
        return

    # Test all relevant borders, ignoring edges
    # Highlight matches.
    def test3x3(self):
        for m, i in enumerate([0, 1, 3, 4, 6, 7]):
            offset = abs(self.card_table[self.grid[i]].east)
            offset = (offset - 1) * 12
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i + 1]].west == 0:
                self.mask_table[m + offset].set_layer(2000)
            else:
                self.mask_table[m + offset].hide()
        for m, i in enumerate([0, 1, 2, 3, 4, 5]):
            offset = abs(self.card_table[self.grid[i]].south)
            offset = (offset - 1) * 12 + 6
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i + 3]].north == 0:
                self.mask_table[m + offset].set_layer(2000)
            else:
                self.mask_table[m + offset].hide()
        for i in (0, 1, 3, 4, 6, 7):
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i + 1]].west != 0:
                return False
        for i in (0, 1, 2, 3, 4, 5):
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i + 3]].north != 0:
                return False
        return True

    def test2x3(self):
        for m, i in enumerate([0, 3, 6]):
            offset = abs(self.card_table[self.grid[i]].east)
            offset = (offset - 1) * 12
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i + 1]].west == 0:
                self.mask_table[m * 2 + offset].set_layer(2000)
            else:
                self.mask_table[m * 2 + offset].hide()
        for m, i in enumerate([0, 1, 3, 4]):
            offset = abs(self.card_table[self.grid[i]].south)
            offset = (offset - 1) * 12 + 6
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i + 3]].north == 0:
                self.mask_table[i + offset].set_layer(2000)
            else:
                self.mask_table[i + offset].hide()
        for i in (0, 3, 6):
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i + 1]].west != 0:
                return False
        for i in (0, 1, 3, 4):
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i + 3]].north != 0:
                return False
        return True

    def test3x2(self):
        for m, i in enumerate([0, 1, 3, 4]):
            offset = abs(self.card_table[self.grid[i]].east)
            offset = (offset - 1) * 12
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i + 1]].west == 0:
                self.mask_table[m + offset].set_layer(2000)
            else:
                self.mask_table[m + offset].hide()
        for m, i in enumerate([0, 1, 2]):
            offset = abs(self.card_table[self.grid[i]].south)
            offset = (offset - 1) * 12 + 6
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i + 3]].north == 0:
                self.mask_table[m + offset].set_layer(2000)
            else:
                self.mask_table[m + offset].hide()
        for i in (0, 1, 3, 4):
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i + 1]].west != 0:
                return False
        for i in (0, 1, 2):
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i + 3]].north != 0:
                return False
        return True

    def test2x2(self):
        for m, i in enumerate([0, 3]):
            offset = abs(self.card_table[self.grid[i]].east)
            offset = (offset - 1) * 12
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i + 1]].west == 0:
                self.mask_table[m * 2 + offset].set_layer(2000)
            else:
                self.mask_table[m * 2 + offset].hide()
        for m, i in enumerate([0, 1]):
            offset = abs(self.card_table[self.grid[i]].south)
            offset = (offset - 1) * 12 + 6
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i + 3]].north == 0:
                self.mask_table[m + offset].set_layer(2000)
            else:
                self.mask_table[m + offset].hide()
        for i in (0, 3):
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i + 1]].west != 0:
                return False
        for i in (0, 1):
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i + 3]].north != 0:
                return False
        return True

