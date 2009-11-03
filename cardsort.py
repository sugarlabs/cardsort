#!/usr/bin/env python

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

from gettext import gettext as _
import os.path

import window
import grid
import card
import sprites
from orientation import get_rotation_sets

class CardSortMain:
    def __init__(self):
        self.r = 0
        self.tw = None
        # create a new window
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.maximize()
        self.win.set_title(_("CardSort") + ": " + 
                           _("click to rotate; drag to swap"))
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())

        menu = gtk.Menu()
        menu_items = gtk.MenuItem(_("Toggle blank card"))
        menu.append(menu_items)
        menu_items.connect("activate", self._toggle_card_cb)
        menu_items = gtk.MenuItem(_("Apply rotation sets"))
        menu.append(menu_items)
        menu_items.connect("activate", self._apply_rotation_sets_cb)
        menu_items = gtk.MenuItem(_("Solve it"))
        menu.append(menu_items)
        menu_items.connect("activate", self._solve_cb)
        menu_items.show()
        root_menu = gtk.MenuItem("Tools")
        root_menu.show()
        root_menu.set_submenu(menu)

        # A vbox to put a menu and the canvas in:
        vbox = gtk.VBox(False, 0)
        self.win.add(vbox)
        vbox.show()

        menu_bar = gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 2)
        menu_bar.show()

        canvas = gtk.DrawingArea()
        vbox.pack_end(canvas, True, True)
        canvas.show()

        menu_bar.append(root_menu)
        self.win.show_all()

        # Join the activity
        self.tw = window.new_window(canvas, \
                               os.path.join(os.path.abspath('.'), \
                                            'images/card'))
        self.tw.win = self.win

    def set_title(self, title):
        self.win.set_title(title)

    # Print a string when a menu item is selected
    def _toggle_card_cb(self, widget):
        self.tw.grid.toggle_blank()
        sprites.redrawsprites(self.tw)

    def _apply_rotation_sets_cb(self, widget):
        self.rotation_sets = get_rotation_sets()
        i = self.r
        for j in range(9):
            # if the blank card (9) is in the grid,
            # then the index for the card it replaced will fail
            try: 
                self.tw.grid.card_table[self.tw.grid.grid.index(j)]\
                    .set_orientation(self.rotation_sets[i][j])
            except ValueError:
                pass
        sprites.redrawsprites(self.tw)
        self.r += 1
        if self.r == 64:
            self.r = 0

    def _solve_cb_x(self, widget):
        self.tw.grid.set_grid([8,7,6,5,4,3,2,1,0,9])
        self.tw.grid.print_grid()

        self.tw.grid.set_orientation([0,90,180,270,0,90,180,270,0,90])
        self.tw.grid.print_orientations()
        sprites.redrawsprites(self.tw)
        return True

    def _solve_cb(self, widget):
        self.rotation_sets = get_rotation_sets()
        counter = 0
        a = [0,1,2,3,4,5,6,7,8]
        for i in Permutation(a):
            if self.test(i) is True:
                return True
            counter += 1
            if (counter/1000)*1000 == counter:
                print str(counter) + ": " + str(self.tw.grid.grid)
        print "no solution found :("
        return True

    def test(self,g):
        self.tw.grid.grid = g
        for o in range(64):
            for r in range(9):
                self.tw.grid.card_table[self.tw.grid.grid.index(r)]\
                    .set_orientation(self.rotation_sets[o][r],False)
            if self.tw.grid.test() is True:
                print _("You solved the puzzle.")
                self.tw.grid.print_grid()
                self.tw.grid.print_orientations()
                self.tw.win.set_title(_("CardSort") + ": " + \
                                      _("You solved the puzzle."))
                self.tw.grid.reset(self.tw)
                self.tw.grid.set_grid(g)
                for r in range(9):
                    self.tw.grid.card_table[self.tw.grid.grid.index(r)]\
                        .set_orientation(self.rotation_sets[o][r],True)
                self.tw.grid.print_grid()
                self.tw.grid.print_orientations()
                sprites.redrawsprites(self.tw)
                return True
        return False
"""
def permute(inputData, outputSoFar): 
    for elem in inputData: 
        if elem not in outputSoFar: 
            outputSoFar.append(elem) 
            if len(outputSoFar) == len(inputData): 
                print outputSoFar 
            else: 
                permute(inputData, outputSoFar) # --- Recursion  
            outputSoFar.pop() 

permute([0,1,2,3,4,5,6,7,8], []) 
"""

class Permutation: 
    def __init__(self, justalist): 
        self._data = justalist[:] 
        self._sofar = [] 
    def __iter__(self): 
        return self.next() 
    def next(self): 
         for elem in self._data: 
             if elem not in self._sofar: 
                 self._sofar.append(elem) 
                 if len(self._sofar) == len(self._data): 
                     yield self._sofar[:] 
                 else: 
                     for v in self.next(): 
                         yield v 
                 self._sofar.pop() 


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    CardSortMain()
    main()
