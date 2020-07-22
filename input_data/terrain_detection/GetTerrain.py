# this code is used to determine the shape of the terrain from the screenshot
from PIL import Image
import numpy as np

def getTerrain (screenshot):
    # open the screenshot
    image = Image.open(screenshot)

    # resize the image
    image = image.resize((128, 80))
    box = (0, 10, 128, 80)
    image = image.crop(box)

    # now find the height of the grass every 64 pixels
    x = 0
    heights = []
    for i in range(128):
        y = 69
        while True:
            r, g, b, trash = (image.getpixel((x, y)))
            if (r < 180 and g > 200 and b < 100):  # if this pixel is green
                heights.append(69 - y)
                break
            if(y == 0): #if there is no ground in this position
                heights.append(0)
                break
            y -= 1
        x += 1

    # return the array containing the height information
    return heights

# example: terrainData = getTerrain("testImages/shot1OG.png")