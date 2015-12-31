import os
from PIL import Image

def tif2other(dataFile, targetFile, targetFormat):
    # dataFile = '/home/joe/Pictures/t002c1.tif'
    if not os.path.isfile(dataFile):
        raise RuntimeError('could not find file "%s"' % dataFile)
    dataImg = Image.open(dataFile)
    # dataImg.save('t002c1.png', 'png')
    dataImg.save(targetFile, targetFormat)
