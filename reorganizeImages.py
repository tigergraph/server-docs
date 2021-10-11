import re
import os
from pathlib import Path
from shutil import copyfile
import urllib.parse
import fileinput

imagesFolder = r'assets/'
modulesFolder = r'modules/'

# got through modules
for subdir in os.scandir(modulesFolder):
    # make images folder if it doesn't already exist
    try:
        newImagesFolder = os.path.join(subdir, "images")
        os.mkdir(newImagesFolder)
    except:
        print(newImagesFolder, "already exists")

    # make sure it's a module folder and not a file
    if not subdir.is_file() and subdir != r'modules/.idea/':
        pagesFolder = os.path.join(subdir, "pages")
        # go through each page in the pages folder
        for page in os.listdir(pagesFolder):
            # get the path of each page
            pagePath = os.path.join(subdir,"pages",page)
            if os.path.isfile(pagePath):
                for line in fileinput.input(pagePath, inplace=True):
                    image = re.search(r'image::(.*)\[(.*)]', line)
                    iimage = re.search(r'image:(.*)\[(.*)]', line)
                    if image:
                        # get the relative path
                        imagePath = image.group(1)
                        imageName = re.search('/assets/(.*\..*)', imagePath)
                        if imageName:
                            imageName = imageName.group(1)
                            line = (re.sub(r'image::(.*)\[(.*)]', r'image::'+imageName+r'[\2]', line))
                        
                    elif iimage:
                        imagePath = iimage.group(1)
                        imageName = re.search('/assets/(.*\..*)', imagePath)
                        if imageName:
                            imageName = imageName.group(1)
                            line = (re.sub(r'image:(.*)\[(.*)]', r'image:'+imageName+r'[\2]', line))

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
