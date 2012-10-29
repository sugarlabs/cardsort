#!/usr/bin/env python
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
from gi.repository import Gdk, Gtk, GdkPixbuf, GObject
import pygtk
pygtk.require('2.0')

from gettext import gettext as _
import os.path

from window import Game
from orientation import get_rotation_sets


class CardSortMain:
    def __init__(self):
        self.r = 0
        self.tw = None
        # create a new window
        self.win = Gtk.Window(Gdk.WindowType.TOPLEVEL)
        self.win.maximize()
        self.win.set_title(_("CardSort") + ": " + 
                           _("click to rotate; drag to swap"))
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())

        menu = Gtk.Menu()

        menu_items = Gtk.MenuItem(_("2x2"))
        menu.append(menu_items)
        menu_items.connect("activate", self._grid2x2_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("2x3"))
        menu.append(menu_items)
        menu_items.connect("activate", self._grid2x3_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("3x2"))
        menu.append(menu_items)
        menu_items.connect("activate", self._grid3x2_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("3x3"))
        menu.append(menu_items)
        menu_items.connect("activate", self._grid3x3_cb)
        menu_items.show()

        """
        menu_items = gtk.MenuItem(_("Solve it"))
        menu.append(menu_items)
        menu_items.connect("activate", self._solve_cb)
        menu_items.show()
        """

        root_menu = Gtk.MenuItem("Tools")
        root_menu.show()
        root_menu.set_submenu(menu)

        # A vbox to put a menu and the canvas in:
        vbox = Gtk.VBox(False, 0)
        self.win.add(vbox)
        vbox.show()

        menu_bar = Gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 2)
        menu_bar.show()

        canvas = Gtk.DrawingArea()
        vbox.pack_end(canvas, True, True, 3)
        canvas.show()

        menu_bar.append(root_menu)
        self.win.show_all()

        # Start the activity
        self.game = Game(canvas, os.path.join(os.path.abspath('.'), 'images'))
        self.game.win = self.win
        self.game.test = self.game.grid.test2x2
        self.game.grid.reset2x2(self.game)

    def set_title(self, title):
        self.win.set_title(title)

    #
    # Grid resize callbacks
    #
    def _grid2x2_cb(self, button):
        self.game.test = self.game.grid.test2x2
        self.game.grid.reset2x2(self.game)

    def _grid3x2_cb(self, button):
        self.game.test = self.game.grid.test3x2
        self.game.grid.reset3x2(self.game)

    def _grid2x3_cb(self, button):
        self.game.test = self.game.grid.test2x3
        self.game.grid.reset2x3(self.game)

    def _grid3x3_cb(self, button):
        self.game.test = self.game.grid.test3x3
        self.game.grid.reset3x3(self.game)

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
                print str(counter) + ": " + str(self.game.grid.grid)
        print "no solution found :("
        return True

    def test(self,g):
        self.game.grid.grid = g
        for o in range(64):
            for r in range(9):
                self.game.grid.card_table[self.game.grid.grid.index(r)]\
                    .set_orientation(self.rotation_sets[o][r],False)
            if self.game.test() is True:
                print _("You solved the puzzle.")
                self.game.grid.print_grid()
                self.game.grid.print_orientations()
                self.game.win.set_title(_("CardSort") + ": " + \
                                      _("You solved the puzzle."))
                self.game.grid.reset3x3(self.game)
                self.game.grid.set_grid(g)
                for r in range(9):
                    self.game.grid.card_table[self.game.grid.grid.index(r)]\
                        .set_orientation(self.rotation_sets[o][r],True)
                self.game.grid.print_grid()
                self.game.grid.print_orientations()
                self.game.sprites.redraw_sprites()
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
    Gtk.main()
    return 0

if __name__ == "__main__":
    CardSortMain()
    main()
