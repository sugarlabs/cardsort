#Copyright (c) 2009, Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os.path

from sprites import *

#
# class for defining individual cards
#
class Card:
    # Spade   = 1,-1
    # Heart   = 2,-2
    # Club    = 3,-3
    # Diamond = 4,-4
    def __init__(self,tw,c,i,x,y):
        self.north = c[0]
        self.east = c[1]
        self.south = c[2]
        self.west = c[3]
        self.orientation = 0
        # create sprite from svg file
        self.spr = sprNew(tw, x, y,\
                          self.load_image(tw.path,i,tw.card_dim*tw.scale))
        self.spr.label = i

    def draw_card(self):
        setlayer(self.spr,2000)
        draw(self.spr)

    def load_image(self, file, i, wh):
        # print "loading " + os.path.join(file + str(i) + '.svg') + \
        #       " scale: " + str(wh)
        return gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(file + \
                                                         str(i) + "x" + \
                                                         '.svg'), \
                                                    int(wh), int(wh))

    def set_orientation(self,r):
        while r != self.orientation:
            self.rotate_ccw()

    def rotate_ccw(self):
        # print "rotating card " + str(self.spr.label)
        tmp = self.north
        self.north = self.east
        self.east = self.south
        self.south = self.west
        self.west = tmp
        self.orientation += 90
        if self.orientation > 359:
            self.orientation -= 360
        tmp = self.spr.image.rotate_simple(90)
        self.spr.image = tmp

    def print_card(self):
        print "(" + str(self.north) + "," + str(self.east) + \
              "," + str(self.south) + "," + str(self.west) + \
              ") " + str(self.rotate) + "ccw" + \
              " x:" + str(self.spr.x) + " y:" + str(self.spr.y)

