#!/usr/bin/python


''' tk_image_slideshow3.py
create a Tkinter image repeating slide show
tested with Python27/33  by  vegaseat  03dec2013
'''

from itertools import cycle
from PIL import Image, ImageTk
import glob
import os
import sys
import re

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class App(tk.Tk):
    '''Tk window/label adjusts to size of image'''
    def __init__(self, image_files, x, y, delay):
        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        self.geometry('+{}+{}'.format(x, y))
        self.delay = delay
        # allows repeat cycling through the pictures
        # store as (img_object, img_name) tuple
        self.pictures = cycle((ImageTk.PhotoImage(file=image), image)
                                for image in image_files)
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
    def show_slides(self):
        '''cycle through the images and show them'''
        # next works with Python26 or higher
        img_object, img_name = next(self.pictures)
        self.picture_display.config(image=img_object)
        # shows the image filename, but could be expanded
        # to show an associated description of the image
        self.title("Do very little")
        self.maxsize(800, 1000)
        self.after(self.delay, self.show_slides)
    def run(self):
        self.mainloop()

# set milliseconds time between slides
delay = 3500
# get a series of gif images you have in the working folder
# or use full path, or set directory to where the images are

image_files = glob.glob("temp/temp-%s*.jpg" % 'report')
image_files.sort(key=alphanum_key) #sort the file before joining it

# upper left corner coordinates of app window
x = 100
y = 50
app = App(image_files, x, y, delay)
app.show_slides()
app.run()

