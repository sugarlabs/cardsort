#!/usr/bin/env python

#Copyright (c) 2009,10 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

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

        menu_items = gtk.MenuItem(_("2x2"))
        menu.append(menu_items)
        menu_items.connect("activate", self._grid2x2_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("2x3"))
        menu.append(menu_items)
        menu_items.connect("activate", self._grid2x3_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("3x2"))
        menu.append(menu_items)
        menu_items.connect("activate", self._grid3x2_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("3x3"))
        menu.append(menu_items)
        menu_items.connect("activate", self._grid3x3_cb)
        menu_items.show()

        """
        menu_items = gtk.MenuItem(_("Solve it"))
        menu.append(menu_items)
        menu_items.connect("activate", self._solve_cb)
        menu_items.show()
        """

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

        # Start the activity
        self.tw = window.new_window(canvas, \
                               os.path.join(os.path.abspath('.'), \
                                            'images/card'))
        self.tw.win = self.win
        self.tw.test = self.tw.grid.test2x2
        self.tw.grid.reset2x2(self.tw)

    def set_title(self, title):
        self.win.set_title(title)

    #
    # Grid resize callbacks
    #
    def _grid2x2_cb(self, button):
        self.tw.test = self.tw.grid.test2x2
        self.tw.grid.reset2x2(self.tw)

    def _grid3x2_cb(self, button):
        self.tw.test = self.tw.grid.test3x2
        self.tw.grid.reset3x2(self.tw)

    def _grid2x3_cb(self, button):
        self.tw.test = self.tw.grid.test2x3
        self.tw.grid.reset2x3(self.tw)

    def _grid3x3_cb(self, button):
        self.tw.test = self.tw.grid.test3x3
        self.tw.grid.reset3x3(self.tw)

    def _solve_cb(self, widget):
        self.show_all()
        self.set_grid([0,1,2,3,4,5,6,7,8])
        self.set_orientations([0,0,0,0,0,0,0,0,0])
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
            if self.tw.test() is True:
                print _("You solved the puzzle.")
                self.tw.grid.print_grid()
                self.tw.grid.print_orientations()
                self.tw.win.set_title(_("CardSort") + ": " + \
                                      _("You solved the puzzle."))
                self.tw.grid.reset3x3(self.tw)
                self.tw.grid.set_grid(g)
                for r in range(9):
                    self.tw.grid.card_table[self.tw.grid.grid.index(r)]\
                        .set_orientation(self.rotation_sets[o][r],True)
                self.tw.grid.print_grid()
                self.tw.grid.print_orientations()
                self.tw.sprites.redraw_sprites()
                return True
        return False

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
