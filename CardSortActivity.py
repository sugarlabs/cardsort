# -*- coding: utf-8 -*-
# Copyright (c) 2009-12 Walter Bender
# Copyright (c) 2012 Ignacio Rodríguez
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

from gi.repository import Gtk, Gdk, GObject
import pygtk
pygtk.require('2.0')

import sugar3
from sugar3.activity import activity
from sugar3.bundle.activitybundle import ActivityBundle
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.menuitem import MenuItem
from sugar3.graphics.icon import Icon
from sugar3.datastore import datastore

from gettext import gettext as _
import locale
import os.path

from sprites import *
from toolbar_utils import radio_factory, label_factory, separator_factory
from window import Game

SERVICE = 'org.sugarlabs.CardSortActivity'
IFACE = SERVICE
PATH = '/org/augarlabs/CardSortActivity'

#
# Sugar activity
#
class CardSortActivity(activity.Activity):

    def __init__(self, handle):
        super(CardSortActivity,self).__init__(handle)

	toolbar_box = ToolbarBox()
	activity_button = ActivityToolbarButton(self)
	toolbar_box.toolbar.insert(activity_button, 0)
	activity_button.show()

        self.grid2x2 = radio_factory('2x2on',
                                     toolbar_box.toolbar,
                                     self._grid2x2_cb,
                                     tooltip=_('2x2'),
                                     group = None)
        self.grid3x2 = radio_factory('3x2on',
                                     toolbar_box.toolbar,
                                     self._grid3x2_cb,
                                     tooltip=_('3x2'),
                                     group = self.grid2x2)
        self.grid2x3 = radio_factory('2x3on',
                                     toolbar_box.toolbar,
                                     self._grid2x3_cb,
                                     tooltip=_('2x3'),
                                     group = self.grid2x2)
        self.grid3x3 = radio_factory('3x3on',
                                     toolbar_box.toolbar,
                                     self._grid3x3_cb,
                                     tooltip=_('3x3'),
                                     group = self.grid2x2)

        separator_factory(toolbar_box.toolbar,
                          visible=False)

	self.results_label = label_factory(toolbar_box.toolbar,
                                           _("click to rotate; drag to swap"),
                                           width=300)

        separator_factory(toolbar_box.toolbar,
                          expand=True,
                          visible=False)

	# The ever-present Stop Button
	stop_button = StopButton(self)
	stop_button.props.accelerator = '<Ctrl>Q'
	toolbar_box.toolbar.insert(stop_button, -1)
	stop_button.show()

	self.set_toolbar_box(toolbar_box)
	toolbar_box.show()

         # Create a canvas
        canvas = Gtk.DrawingArea()
        canvas.set_size_request(Gdk.Screen.width(),
                                Gdk.Screen.height())
        self.set_canvas(canvas)
        canvas.show()
        self.show_all()

        # Initialize the canvas
        self.game = Game(canvas, os.path.join(
                activity.get_bundle_path(), 'images'), self)

        # Read the mode from the Journal
        try:
            if self.metadata['grid'] == '2x2':
                self.show_grid2x2()
            elif self.metadata['grid'] == '3x2':
                self.show_grid3x2()
            elif self.metadata['grid'] == '2x3':
                self.show_grid2x3()
            elif self.metadata['grid'] == '3x3':
                self.show_grid3x3()
        except:
            self.metadata['grid'] = "2x2"
            self.show_grid2x2()


    #
    # Grid resize callbacks
    #
    def _grid2x2_cb(self, button):
        self.show_grid2x2()
        return True

    def show_grid2x2(self):
        self.game.test = self.game.grid.test2x2
        self.game.grid.reset2x2(self.game)
        self.metadata['grid'] = "2x2"

    def _grid3x2_cb(self, button):
        self.show_grid3x2()
        return True

    def show_grid3x2(self):
        self.game.test = self.game.grid.test3x2
        self.game.grid.reset3x2(self.game)
        self.metadata['grid'] = "3x2"

    def _grid2x3_cb(self, button):
        self.show_grid2x3()
        return True

    def show_grid2x3(self):
        self.game.test = self.game.grid.test2x3
        self.game.grid.reset2x3(self.game)
        self.metadata['grid'] = "2x3"

    def _grid3x3_cb(self, button):
        self.show_grid3x3()
        return True

    def show_grid3x3(self):
        self.game.test = self.game.grid.test3x3
        self.game.grid.reset3x3(self.game)
        self.metadata['grid'] = "3x3"

    """
    Write the grid status to the Journal
    """
    def write_file(self, file_path):
        pass

