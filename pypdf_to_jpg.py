#!/usr/bin/python
"""
Problem:
  How to Convert PDF to Image with Python Script ?

Installation:
  I use ubuntu OS 14.04
  We use wrapper for ImageMagick [http://www.imagemagick.org/script/index.php] to Convert The PDF file
  in Python do:

  $ sudo apt-get install libmagickwand-dev
  $ pip install Wand

  now install PIL
  $ pip install Pillow

  More Installation http://sorry-wand.readthedocs.org/en/latest/guide/install.html
  more about wand https://pypi.python.org/pypi/Wand
"""

from PIL import Image as Img
from wand.image import Image
import uuid
import numpy as np
import glob
import os
import sys
import getopt
import re

from ConvertPdf import ConvertPdf, DeleteJpg
from Slideshow import Slideshow

def usage(pname):
    print("Usage:")
    print("\t%s [-v|-V] -D <DIR> -Q <QUALITY> -R <RESOLUTION> -T <MILLISECONDS> -x <SIZE> -y <SIZE> -X <POS> -Y <POS> <FILE>" % (pname))
    print("where:")
    print("\t-D <DIR> \t\t Output directory")
    print("\t-Q <QUALITY> \t\t Quality as percentage")
    print("\t-R <RESOLUTION> \t Resolution in dpi")
    print("\t-T <MILLISECONDS> \t Delay between slides")
    print("\t-x <SIZE> \t\t Horizontal size")
    print("\t-y <SIZE> \t\t Vertical size")
    print("\t-X <POS> \t\t Horizontal offset")
    print("\t-Y <POS> \t\t Vertical offset")
    print("\t<FILE> \t\t\t Input file")
    sys.exit("")

# Pythonic entry point
def main(pname, argv):
    fname = None
    combine = False
    resolution = 200
    compression_quality = 90
    compression_dir = "temp"
    delay = 3500
    xpos = 300
    ypos = 50
    xdim = 630
    ydim = 900
    fforce = False

    try:
        opts, fnames  = getopt.gnu_getopt(argv,"cfhvD:Q:R:T:x:X:y:Y:", \
                                   ["help","dir=","qual=","res="])
    except getopt.GetoptError:
        print("Error in options")
        # usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage(pname)
        elif opt == '-c':
            combine = True
        elif opt == '-f':
            fforce = True
        elif opt == '-D' or opt == '--dir':
            compression_dir = arg
        elif opt == '-Q' or opt == '--qual':
            compression_quality = int(arg)
            #if compression_quality > 100:
                #compression_quality = 100
        elif opt == '-R' or opt == '--res':
            resolution = int(arg)
        elif opt == '-T':
            delay = int(arg)
        elif opt == '-x':
            xdim = int(arg)
        elif opt == '-y':
            ydim = int(arg)
        elif opt == '-X':
            xpos = int(arg)
        elif opt == '-Y':
            ypos = int(arg)
        else:
            print("Something is wrong here")

    fname = fnames[0]
    if fname is None:
        print("No input file name")
        sys.exit(1)

    # DeleteJpg(fname, compression_dir)

    print("Convert file %s" % fname)
    result, image_files = ConvertPdf(fname, resolution, compression_quality, compression_dir, combine, fforce)
    if not result:
        print("Could not convert %s" % (fname))
    elif len(image_files) == 0:
        print("No image files produced")
        sys.exit(1)
    elif not combine:
        print("Succcesfully converted %s" % fname)
    elif result:
        print("Succcesfully converted %s and saved it to %s" % (fname, result))
    else:
        print("Something went wrong")
        sys.exit(1)

    try:
        print("Run %dx%d slide show at %d,%d with delay %dms" % (xdim, ydim, xpos, ypos, delay))
        app = Slideshow(result, image_files, xdim, ydim, xpos, ypos, delay)
        app.show_slides()
        app.run()
    except KeyboardInterrupt:
        print("\nStop")
        DeleteJpg(fname, compression_dir)
        print("Done")


# Entry point
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        usage(sys.argv[0])
    main(sys.argv[0], sys.argv[1:])
