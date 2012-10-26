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
from gi.repository import Gtk, Gdk
import pygtk
pygtk.require('2.0')
from gettext import gettext as _

from sugar3.graphics import style
GRID_CELL_SIZE = style.GRID_CELL_SIZE

from grid import Grid
from sprites import Sprites
from math import sqrt

CARD_DIM = 135

#
# handle launch from both within and without of Sugar environment 
#
class Game():

    def __init__(self, canvas, path, parent=None):
        self.activity = parent
        self.path = path
    
        # starting from command line
        # we have to do all the work that was done in CardSortActivity.py
        if parent is None:
            self.sugar = False
            self.canvas = canvas
    
        # starting from Sugar
        else:
            self.sugar = True
            self.canvas = canvas
            parent.show_all()
    
        self.canvas.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.canvas.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.canvas.connect("draw", self.__draw_cb)
        self.canvas.connect("button-press-event", self._button_press_cb)
        self.canvas.connect("button-release-event", self._button_release_cb)
        self.width = Gdk.Screen.width()
        self.height = Gdk.Screen.height()-GRID_CELL_SIZE
        self.card_dim = CARD_DIM
        self.scale = 0.8 * self.height / (self.card_dim * 3)
    
        # Initialize the sprite repository
        self.sprites = Sprites(self.canvas)
    
        # Initialize the grid
        self.grid = Grid(self)
    
        # Start solving the puzzle
        self.press = -1
        self.release = -1
        self.start_drag = [0, 0]
    
    #
    # Button press
    #
    def _button_press_cb(self, win, event):
        win.grab_focus()
        x, y = map(int, event.get_coords())
        self.start_drag = [x, y]
        self.grid.hide_masks()
        spr = self.sprites.find_sprite((x,y))
        if spr is None:
            self.press = -1
            self.release = -1
            return True
        # take note of card under button press
        self.press = int(spr.labels[0])
        return True
    
    #
    # Button release
    #
    def _button_release_cb(self, win, event):
        win.grab_focus()
        self.grid.hide_masks()
        x, y = map(int, event.get_coords())
        spr = self.sprites.find_sprite((x, y))
        if spr is None:
            self.press = -1
            self.release = -1
            return True
        # take note of card under button release
        self.release = int(spr.labels[0])
        # if the same card (click) then rotate
        if self.press == self.release:
            # check to see if it was an aborted move
            if self.distance(self.start_drag, [x, y]) < 20:
                self.grid.card_table[self.press].rotate_ccw()
                # self.grid.card_table[self.press].print_card()
        # if different card (drag) then swap
        else:
            self.grid.swap(self.press,self.release)
            # self.grid.print_grid()
        self.press = -1
        self.release = -1
        if self.test() == True:
            if self.sugar is True:
                self.activity.results_label.set_text(
                    _("You solved the puzzle."))
                self.activity.results_label.show()
            else:
                self.win.set_title(_("CardSort") + ": " + \
                                    _("You solved the puzzle."))
        else:
            if self.sugar is True:
                self.activity.results_label.set_text(_("Keep trying."))
                self.activity.results_label.show()
            else:
                self.win.set_title(_("CardSort") + ": " + _("Keep trying."))
        return True
    
    #
    # Measure length of drag between button press and button release
    #
    def distance(self, start, stop):
        dx = start[0] - stop[0]
        dy = start[1] - stop[1]
        return sqrt(dx * dx + dy * dy)

    #
    # Repaint
    #
    def __draw_cb(self, canvas, cr):
		self.sprites.redraw_sprites(cr=cr)
    
    def do_expose_event(self, event):
        ''' Handle the expose-event by drawing '''
        # Restrict Cairo to the exposed area
        cr = self.canvas.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                     event.area.width, event.area.height)
        cr.clip()
        # Refresh sprite list
        self.sprites.redraw_sprites(cr=cr)
    
    #
    # callbacks
    #
    def _destroy_cb(self, win, event):
        Gtk.main_quit()
