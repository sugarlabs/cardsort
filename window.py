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

try:
    from sugar.graphics import style
    GRID_CELL_SIZE = style.GRID_CELL_SIZE
except:
    GRID_CELL_SIZE = 0

from grid import *
from card import *
from sprites import Sprites
from math import sqrt

CARD_DIM = 135

class taWindow: pass

#
# handle launch from both within and without of Sugar environment 
#
def new_window(canvas, path, parent=None):
    tw = taWindow()
    tw.path = path
    tw.activity = parent

    # starting from command line
    # we have to do all the work that was done in CardSortActivity.py
    if parent is None:
        tw.sugar = False
        tw.canvas = canvas

    # starting from Sugar
    else:
        tw.sugar = True
        tw.canvas = canvas
        parent.show_all()

    tw.canvas.set_flags(gtk.CAN_FOCUS)
    tw.canvas.add_events(gtk.gdk.BUTTON_PRESS_MASK)
    tw.canvas.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
    tw.canvas.connect("expose-event", _expose_cb, tw)
    tw.canvas.connect("button-press-event", _button_press_cb, tw)
    tw.canvas.connect("button-release-event", _button_release_cb, tw)
    tw.width = gtk.gdk.screen_width()
    tw.height = gtk.gdk.screen_height()-GRID_CELL_SIZE
    tw.card_dim = CARD_DIM
    tw.scale = 0.8 * tw.height/(tw.card_dim*3)

    # Initialize the sprite repository
    tw.sprites = Sprites(tw.canvas)

    # Initialize the grid
    tw.grid = Grid(tw)

    # Start solving the puzzle
    tw.press = -1
    tw.release = -1
    tw.start_drag = [0,0]

    return tw

#
# Button press
#
def _button_press_cb(win, event, tw):
    win.grab_focus()
    x, y = map(int, event.get_coords())
    tw.start_drag = [x,y]
    spr = tw.sprites.find_sprite((x,y))
    if spr is None:
        tw.press = -1
        tw.release = -1
        return True
    # take note of card under button press
    tw.press = int(spr.labels[0])
    return True

#
# Button release
#
def _button_release_cb(win, event, tw):
    win.grab_focus()
    x, y = map(int, event.get_coords())
    spr = tw.sprites.find_sprite((x,y))
    if spr is None:
        tw.press = -1
        tw.release = -1
        return True
    # take note of card under button release
    tw.release = int(spr.labels[0])
    # if the same card (click) then rotate
    if tw.press == tw.release:
        # check to see if it was an aborted move
        if distance(tw.start_drag,[x,y]) < 20:
            tw.grid.card_table[tw.press].rotate_ccw()
            # tw.grid.card_table[tw.press].print_card()
    # if different card (drag) then swap
    else:
        tw.grid.swap(tw.press,tw.release)
        # tw.grid.print_grid()
    tw.press = -1
    tw.release = -1
    if tw.test() == True:
        if tw.sugar is True:
            tw.activity.results_label.set_text(_("You solved the puzzle."))
            tw.activity.results_label.show()
        else:
            tw.win.set_title(_("CardSort") + ": " + \
                                _("You solved the puzzle."))
    else:
        if tw.sugar is True:
            tw.activity.results_label.set_text(_("Keep trying."))
            tw.activity.results_label.show()
        else:
            tw.win.set_title(_("CardSort") + ": " + _("Keep trying."))
    return True

#
# Measure length of drag between button press and button release
#
def distance(start,stop):
    dx = start[0]-stop[0]
    dy = start[1]-stop[1]
    return sqrt(dx*dx+dy*dy)


#
# Repaint
#
def _expose_cb(win, event, tw):
    tw.sprites.redraw_sprites()
    return True

#
# callbacks
#
def _destroy_cb(win, event, tw):
    gtk.main_quit()
