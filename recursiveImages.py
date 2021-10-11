import re
import os
from pathlib import Path
from shutil import copyfile
import urllib.parse
import fileinput

imagesFolder = r'assets/'
modulesFolder = r'modules/'

for dirpath, dirs, files in os.walk(modulesFolder):
    # print(dirpath)
    for f in files:
        fname = os.path.join(dirpath,f)
        if fname.endswith('.adoc'):
            print(fname)
            parentFolder = os.path.dirname(os.path.dirname(fname))
            # we don't need to create an images folder in the modules folder
            if not parentFolder.endswith('modules'):
                # see if the images folder already exists and create it if not
                try:
                    newImagesFolder = os.path.join(parentFolder, "images")
                    os.mkdir(newImagesFolder)
                except:
                    # print(newImagesFolder, "already exists")
                    pass
            # actual text replacement and image moving
            with fileinput.input(fname, inplace=True) as f:
                for line in f:
                    image = re.search(r'image::(.*)\[(.*)]', line)
                    iimage = re.search(r'image:(.*)\[(.*)]', line)
                    if image:
                        # get the relative path
                        imagePath = image.group(1)
                        imageName = re.search(r'/assets/(.*\..*)', imagePath)
                        if imageName:
                            imageName = imageName.group(1)
                            line = (re.sub(r'image::(.*)\[(.*)]', r'image::'+imageName+r'[\2]', line))
                        
                    elif iimage:
                        imagePath = iimage.group(1)
                        imageName = re.search(r'/assets/(.*\..*)', imagePath)
                        if imageName:
                            imageName = imageName.group(1)
                            line = (re.sub(r'image:(.*)\[(.*)]', r' image:'+imageName+r'[\2] ', line))

                    if image or iimage:
                        if imageName:
                            # find the image in the 'assets' folder
                            sourceImage = os.path.join("assets", imageName)
                            # strip special characters
                            sourceImage = urllib.parse.unquote(sourceImage)
                            destinationImage = os.path.join(newImagesFolder, imageName)
                            destinationImage = urllib.parse.unquote(destinationImage)
                            copyfile(sourceImage, destinationImage)
                    print('{}'.format(line), end='')
