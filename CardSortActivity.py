#Copyright (c) 2009-11 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import sugar
from sugar.activity import activity
try: # 0.86+ toolbar widgets
    from sugar.bundle.activitybundle import ActivityBundle
    from sugar.activity.widgets import ActivityToolbarButton
    from sugar.activity.widgets import StopButton
    from sugar.graphics.toolbarbox import ToolbarBox
    from sugar.graphics.toolbarbox import ToolbarButton
except ImportError:
    pass
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.graphics.icon import Icon
from sugar.datastore import datastore

from gettext import gettext as _
import locale
import os.path

from sprites import *
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

        try:
            # Use 0.86 toolbar design
            toolbar_box = ToolbarBox()

            # Buttons added to the Activity toolbar
            activity_button = ActivityToolbarButton(self)
            toolbar_box.toolbar.insert(activity_button, 0)
            activity_button.show()

            # 2x2 Button
            self.grid2x2 = ToolButton( "2x2on" )
            self.grid2x2.set_tooltip(_('2x2'))
            self.grid2x2.props.sensitive = True
            self.grid2x2.connect('clicked', self._grid2x2_cb)
            toolbar_box.toolbar.insert(self.grid2x2, -1)
            self.grid2x2.show()

            # 3x2 Button
            self.grid3x2 = ToolButton( "3x2off" )
            self.grid3x2.set_tooltip(_('3x2'))
            self.grid3x2.props.sensitive = True
            self.grid3x2.connect('clicked', self._grid3x2_cb)
            toolbar_box.toolbar.insert(self.grid3x2, -1)
            self.grid3x2.show()

            # 2x3 Button
            self.grid2x3 = ToolButton( "2x3off" )
            self.grid2x3.set_tooltip(_('2x3'))
            self.grid2x3.props.sensitive = True
            self.grid2x3.connect('clicked', self._grid2x3_cb)
            toolbar_box.toolbar.insert(self.grid2x3, -1)
            self.grid2x3.show()

            # 3x3 Button
            self.grid3x3 = ToolButton( "3x3off" )
            self.grid3x3.set_tooltip(_('3x3'))
            self.grid3x3.props.sensitive = True
            self.grid3x3.connect('clicked', self._grid3x3_cb)
            toolbar_box.toolbar.insert(self.grid3x3, -1)
            self.grid3x3.show()

            separator = gtk.SeparatorToolItem()
            separator.show()
            toolbar_box.toolbar.insert(separator, -1)

            # Label for showing status
            self.results_label = gtk.Label(_("click to rotate; drag to swap"))
            self.results_label.show()
            results_toolitem = gtk.ToolItem()
            results_toolitem.add(self.results_label)
            toolbar_box.toolbar.insert(results_toolitem,-1)

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            separator.show()
            toolbar_box.toolbar.insert(separator, -1)

            # The ever-present Stop Button
            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>Q'
            toolbar_box.toolbar.insert(stop_button, -1)
            stop_button.show()

            self.set_toolbar_box(toolbar_box)
            toolbar_box.show()

        except NameError:
            # Use pre-0.86 toolbar design
            self.toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(self.toolbox)

            self.projectToolbar = ProjectToolbar(self)
            self.toolbox.add_toolbar( _('Project'), self.projectToolbar )

            self.toolbox.show()

        # Create a canvas
        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width(),
                                gtk.gdk.screen_height())
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
        self.grid2x2.set_icon("2x2on")
        self.grid3x2.set_icon("3x2off")
        self.grid2x3.set_icon("2x3off")
        self.grid3x3.set_icon("3x3off")
        self.game.test = self.game.grid.test2x2
        self.game.grid.reset2x2(self.game)
        self.metadata['grid'] = "2x2"

    def _grid3x2_cb(self, button):
        self.show_grid3x2()
        return True

    def show_grid3x2(self):
        self.grid2x2.set_icon("2x2off")
        self.grid3x2.set_icon("3x2on")
        self.grid2x3.set_icon("2x3off")
        self.grid3x3.set_icon("3x3off")
        self.game.test = self.game.grid.test3x2
        self.game.grid.reset3x2(self.game)
        self.metadata['grid'] = "3x2"

    def _grid2x3_cb(self, button):
        self.show_grid2x3()
        return True

    def show_grid2x3(self):
        self.grid2x2.set_icon("2x2off")
        self.grid3x2.set_icon("3x2off")
        self.grid2x3.set_icon("2x3on")
        self.grid3x3.set_icon("3x3off")
        self.game.test = self.game.grid.test2x3
        self.game.grid.reset2x3(self.game)
        self.metadata['grid'] = "2x3"

    def _grid3x3_cb(self, button):
        self.show_grid3x3()
        return True

    def show_grid3x3(self):
        self.grid2x2.set_icon("2x2off")
        self.grid3x2.set_icon("3x2off")
        self.grid2x3.set_icon("2x3off")
        self.grid3x3.set_icon("3x3on")
        self.game.test = self.game.grid.test3x3
        self.game.grid.reset3x3(self.game)
        self.metadata['grid'] = "3x3"

    """
    Write the grid status to the Journal
    """
    def write_file(self, file_path):
        pass

#
# Project toolbar for pre-0.86 toolbars
#
class ProjectToolbar(gtk.Toolbar):

    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # 2x2 Button
        self.activity.grid2x2 = ToolButton( "2x2on" )
        self.activity.grid2x2.set_tooltip(_('2x2'))
        self.activity.grid2x2.props.sensitive = True
        self.activity.grid2x2.connect('clicked', self.activity._grid2x2_cb)
        self.insert(self.activity.grid2x2, -1)
        self.activity.grid2x2.show()

        # 3x2 Button
        self.activity.grid3x2 = ToolButton( "3x2off" )
        self.activity.grid3x2.set_tooltip(_('3x2'))
        self.activity.grid3x2.props.sensitive = True
        self.activity.grid3x2.connect('clicked', self.activity._grid3x2_cb)
        self.insert(self.activity.grid3x2, -1)
        self.activity.grid3x2.show()

        # 2x3 Button
        self.activity.grid2x3 = ToolButton( "2x3off" )
        self.activity.grid2x3.set_tooltip(_('2x3'))
        self.activity.grid2x3.props.sensitive = True
        self.activity.grid2x3.connect('clicked', self.activity._grid2x3_cb)
        self.insert(self.activity.grid2x3, -1)
        self.activity.grid2x3.show()

        # 3x3 Button
        self.activity.grid3x3 = ToolButton( "3x3off" )
        self.activity.grid3x3.set_tooltip(_('3x3'))
        self.activity.grid3x3.props.sensitive = True
        self.activity.grid3x3.connect('clicked', self.activity._grid3x3_cb)
        self.insert(self.activity.grid3x3, -1)
        self.activity.grid3x3.show()

        separator = gtk.SeparatorToolItem()
        separator.set_draw(True)
        self.insert(separator, -1)
        separator.show()

        # Label for showing status
        self.activity.results_label = gtk.Label(\
            _("click to rotate; drag to swap"))
        self.activity.results_label.show()
        self.activity.results_toolitem = gtk.ToolItem()
        self.activity.results_toolitem.add(self.activity.results_label)
        self.insert(self.activity.results_toolitem, -1)
        self.activity.results_toolitem.show()
