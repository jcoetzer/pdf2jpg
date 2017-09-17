
import tkinter as tk
from PIL import Image, ImageTk
from itertools import cycle

class Slideshow(tk.Tk):

    def __init__(self, stitle, image_files, xs, ys, xp, yp, delay):
        tk.Tk.__init__(self)
        self.geometry('+{}+{}'.format(xp, yp))
        self.xsize = xs
        self.ysize = ys
        self.delay = delay
        self.title(stitle)
        #self.pictures = cycle((ImageTk.PhotoImage(file=image), image) for image in image_files)
        self.pictures = cycle(image for image in image_files)
        self.pictures = self.pictures
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
        self.images = [] # to keep references to images.

    def show_slides(self):
        img_name = next(self.pictures)
        image_pil = Image.open(img_name).resize((self.xsize, self.ysize)) #<-- resize images here
        self.images.append(ImageTk.PhotoImage(image_pil))
        self.picture_display.config(image=self.images[-1])
        #self.title("Something or other")
        self.after(self.delay, self.show_slides)

    def run(self):
        self.mainloop()