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

from sprites import *
from card import *

CARD_DEFS = ((1,3,-2,-3),(2,3,-3,-2),(2,3,-4,-4),\
             (2,1,-1,-4),(3,4,-4,-3),(4,2,-1,-2),\
             (1,1,-2,-4),(4,2,-3,-4),(1,3,-1,-2),\
             (0,0,0,0))


#
# class for defining 3x3 matrix of cards
#
class Grid:
    # 123
    # 456
    # 789
    def __init__(self,tw):
        self.grid = [0,1,2,3,4,5,6,7,8,9]
        self.card_table = {}
        # Initialize the cards
        i = 0
        x = int((tw.width-(tw.card_dim*3*tw.scale))/2)
        y = int((tw.height-(tw.card_dim*3*tw.scale))/2)
        for c in CARD_DEFS:
            self.card_table[i] = Card(tw,c,i,x,y)
            self.card_table[i].draw_card()
            x += int(tw.card_dim*tw.scale)
            if x > (tw.width+(tw.card_dim*2*tw.scale))/2:
                x = int((tw.width-(tw.card_dim*3*tw.scale))/2)
                y += int(tw.card_dim*tw.scale)
            i += 1
            if i == 9: # put the extra (blank) card off the screen
                y = tw.height

    def toggle_blank(self):
        self.swap(6,9)

    def swap(self,a,b):
        # swap grid elements and x,y positions of sprites
        # print "swapping cards " + str(a) + " and " + str(b)
        ai = self.grid.index(a)
        bi = self.grid.index(b)
        self.grid[bi] = a
        self.grid[ai] = b
        x = self.card_table[a].spr.x
        y = self.card_table[a].spr.y
        self.card_table[a].spr.x = self.card_table[b].spr.x
        self.card_table[a].spr.y = self.card_table[b].spr.y
        self.card_table[b].spr.x = x
        self.card_table[b].spr.y = y

    def print_grid(self):
        print self.grid
        return

    def test(self):
        # self.print_grid()
        for i in (0,1,3,4,6,7):
            if self.card_table[self.grid[i]].east != 0 and \
               self.card_table[self.grid[i+1]].west != 0 and \
               self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i+1]].west != 0:
                return False
        for i in (0,1,2,3,4,5):
            if self.card_table[self.grid[i]].south != 0 and \
               self.card_table[self.grid[i+3]].north != 0 and \
               self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i+3]].north != 0:
                return False
        return True

