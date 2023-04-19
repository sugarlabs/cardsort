# -*- coding: utf-8 -*-
# Copyright (C) 2009-11 Walter Bender
# Copyright (C) 2012 Ignacio Rodríguez
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os.path

from gi.repository import GdkPixbuf

from sprites import Sprite


def load_image(file, w, h):
    return GdkPixbuf.Pixbuf.new_from_file_at_size(file, int(w), int(h))


#
# class for defining individual cards
#
class Card:
    SUITS = {
        1: "Spade",
        -1: "Spade",
        2: "Heart",
        -2: "Heart",
        3: "Club",
        -3: "Club",
        4: "Diamond",
        -4: "Diamond"
    }
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
        self.suit = Card.SUITS[c.index(max(c))]
        self.value = max(c)
        self.face_up = False
    def flip(self):
        if self.face_up:
            self.set_face_down()
        else:
            self.set_face_up()
    def set_face_down(self):
        if self.face_up:
            self.face_up = False
            self.spr.set_shape(self.images[0])
            self.spr.hide_label()

    def set_face_up(self):
        if not self.face_up:
            self.face_up = True
            self.spr.set_shape(self.images[int(self.orientation / 90)])
            self.spr.show_label()

    def reset_image(self, game, i):
        while self.orientation != 0:
            self.rotate_ccw()

    def set_orientation(self, r, rotate_spr=True):
        while r != self.orientation:
            self.rotate_ccw(rotate_spr)

    def rotate_ccw(self, rotate_spr=True):
        # print "rotating card " + str(self.spr.label)
        tmp = self.north
        self.north = self.east
        self.east = self.south
        self.south = self.west
        self.west = tmp
        self.orientation += 90
        if self.orientation == 360:
            self.orientation = 0
        if rotate_spr:
            if self.face_up:
                self.spr.set_shape(self.images[int(self.orientation / 90)])
            else:
                self.spr.set_shape(self.images[0])

    def print_card(self):
        print(f"{self.value} of {self.suit} with orientation {self.orientation} at position ({self.spr.x}, {self.spr.y})")
       
