

from PIL import Image as Img
from wand.image import Image
import uuid
import numpy as np
import glob
import os
import sys
import getopt
import re

from hashlib import md5

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


def DeleteJpg(filepdf, cdir):
    file_set = os.path.basename(filepdf)
    file_set = os.path.splitext(file_set)[0]
    list_im = glob.glob("%s\\temp-%s*.jpg" % (cdir, file_set))
    list_im.sort(key=alphanum_key)
    for imf in list_im:
        print( "Delete %s" % imf )
        os.remove(imf)
    fname = "%s/%s.md5" % (cdir, file_set)
    print( "Delete %s" % fname )
    try:
        os.remove(fname)
    except OSError:
        print( "Could not delete %s" % fname )



def md5sum(filename):
    hash = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(128 * hash.block_size), b""):
            hash.update(chunk)
    return hash.hexdigest()


def md5write(cdir, cfile, csum):
    fname = "%s\\%s.md5" % (cdir, cfile)
    print( "Write MD5 %s to file %s" % (fname, csum) )
    md5f = open(fname, "w")
    md5f.write("%s" % csum)
    md5f.close()


def md5read(cdir, cfile, csum):
    fname = "%s\\%s.md5" % (cdir, cfile)
    try:
        md5f = open(fname, "r")
        csum = str(md5f.read())
        md5f.close()
        print( "Read MD5 %s from file %s" % (csum, fname) )
    except IOError:
        print( "Could not read MD5 from file %s" % (fname) )
        csum = ''
    return csum


def ConvertPdf(filepdf, cres, cqual, cdir, combine, force=False):
    file_set = os.path.basename(filepdf)
    file_set = os.path.splitext(file_set)[0]
    md5pdf = str(md5sum(filepdf))
    if force:
        DeleteJpg(filepdf, cdir)
    else:
        print( "Process file %s (%s)" % (filepdf, md5pdf) )
        md5prev = md5read(cdir, file_set, None)
        if md5pdf == md5prev:
            print( "File %s is unchanged" % filepdf )
            fnames = []
            list_im = glob.glob("%s\\temp-%s*.jpg" % (cdir, file_set))
            list_im.sort(key=alphanum_key) #sort the file before joining it
            for imf in list_im:
                print( "\t%s" % imf )
                fnames.append(imf)
            if len(fnames) > 0:
                print( "Use existing images" )
                return file_set, fnames
    filenames = []
    try:
        print( "Convert PDF to image with resolution %d quality %d%%" % (cres, cqual) )
        with Image(filename=filepdf, resolution=cres) as img:
            # keep good quality
            img.compression_quality = cqual
            # save it to tmp dir
            ifilename="%s\\temp-%s.jpg" % (cdir, file_set)
            print( "Create image %s" % ifilename )
            img.save(filename=ifilename)
    except Exception as err:
        # keep track of the error until the code is clean
        print( err )
        return False, filenames
    else:
        pathsave = []
        try:
            # search all images in temp path for file name ending with set value
            list_im = glob.glob("%s\\temp-%s*.jpg" % (cdir, file_set))
            list_im.sort(key=alphanum_key) #sort the file before joining it
            if combine:
                """
                converted pdf to image(s)
                merge all files into one large image
                """
                imgs = [Img.open(i) for i in list_im]
                # now lets Combine several images vertically with Python
                min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
                imgs_comb = np.vstack(
                    (np.asarray(i.resize(min_shape)) for i in imgs))
                # for horizontally  change the vstack to hstack
                imgs_comb = Img.fromarray(imgs_comb)
                pathsave = "MyPdf%s.jpg" % file_set
                # now save the image
                imgs_comb.save(pathsave)
            else:
                pathsave.append(file_set)
            # and then remove all temp image
            for imf in list_im:
                print( "\t%s" % imf )
                filenames.append(imf)
                #os.remove(i)
        except Exception as err:
            print( err )
            return False, filenames
        md5write(cdir, file_set, md5pdf)
        return pathsave, filenames
