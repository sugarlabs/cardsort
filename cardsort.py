#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os.path

import window

def main():
    # All PyGTK applications must have a gtk.main(). Control ends here
    # and waits for an event to occur (like a key press or mouse event).
    tw = window.new_window(None, \
                           os.path.join(os.path.abspath('.'), \
                                        'images/card'))
    gtk.main()


if __name__ == "__main__":
    main()
    
