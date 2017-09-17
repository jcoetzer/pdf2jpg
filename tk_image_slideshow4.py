#!/usr/bin/python
import Tkinter as tk
from PIL import Image, ImageTk
from itertools import cycle
import glob
import os
import sys
import re

from Slideshow import Slideshow

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

#class App(tk.Tk):

    #def __init__(self, image_files, x, y, delay):
        #tk.Tk.__init__(self)
        #self.geometry('+{}+{}'.format(x,y))
        #self.delay = delay
        ##self.pictures = cycle((ImageTk.PhotoImage(file=image), image) for image in image_files)
        #self.pictures = cycle(image for image in image_files)
        #self.pictures = self.pictures
        #self.picture_display = tk.Label(self)
        #self.picture_display.pack()
        #self.images = [] # to keep references to images.

    #def show_slides(self):
        #img_name = next(self.pictures)
        #image_pil = Image.open(img_name).resize((700, 1000)) #<-- resize images here

        #self.images.append(ImageTk.PhotoImage(image_pil))

        #self.picture_display.config(image=self.images[-1])
        #self.title("Something or other")
        #self.after(self.delay, self.show_slides)

    #def run(self):
        #self.mainloop()

# Pythonic entry point
def main(pname, argv):
    delay = 3500

    image_files = glob.glob("temp/temp-%s*.jpg" % 'report')
    image_files.sort(key=alphanum_key)

    x = 200
    y = 150
    app = Slideshow(image_files,x,y,delay)
    app.show_slides()
    app.run()


# Entry point
if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])