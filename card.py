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
from gi.repository import Gtk, Gdk, GObject, GdkPixbuf
import pygtk
pygtk.require('2.0')
import os.path

from sprites import Sprite

def load_image(file, w, h):
    return GdkPixbuf.Pixbuf.new_from_file_at_size(file, int(w), int(h))

#
# class for defining individual cards
#
class Card:
    # Spade   = 1,-1
    # Heart   = 2,-2
    # Club    = 3,-3
    # Diamond = 4,-4
    def __init__(self, game, c, i, x, y):
        self.north = c[0]
        self.east = c[1]
        self.south = c[2]
        self.west = c[3]
        self.orientation = 0
        self.images = []
        self.images.append(load_image(
                os.path.join(game.path, 'card%d.svg' % (i)),
                game.card_dim * game.scale, game.card_dim * game.scale))
        for j in range(3):
            self.images.append(self.images[j].rotate_simple(90))
        # create sprite from svg file
        self.spr = Sprite(game.sprites, x, y, self.images[0])
        self.spr.set_label(i)

    def reset_image(self, game, i):
        while self.orientation != 0:
            self.rotate_ccw()

    def set_orientation(self, r, rotate_spr=True):
        while r != self.orientation:
            self.rotate_ccw(rotate_spr)

    def rotate_ccw(self,rotate_spr=True):
        # print "rotating card " + str(self.spr.label)
        tmp = self.north
        self.north = self.east
        self.east = self.south
        self.south = self.west
        self.west = tmp
        self.orientation += 90
        if self.orientation == 360:
            self.orientation = 0
        if rotate_spr is True:
            self.spr.set_shape(self.images[int(self.orientation / 90)])

    def print_card(self):
        print "(" + str(self.north) + "," + str(self.east) + \
              "," + str(self.south) + "," + str(self.west) + \
              ") " + str(self.rotate) + "ccw" + \
              " x:" + str(self.spr.x) + " y:" + str(self.spr.y)

