# this code is used to determine the cars height from the screenshot
from PIL import Image

def getHeight (screenshot):
    # open the screenshot
    image = Image.open(screenshot)

    # crop to area containing the car
    box = (20, 100, 420, 900)
    image = image.crop(box)

    # resize the image
    image = image.resize((40, 80))

    # now we need to find the coordinates of the left/right-most red pixels
    rx = ry = 0
    lx = ly = 0
    brk = False
    for x in range(40):
        for y in range(80):
            r, g, b, trash = (image.getpixel((x, y)))
            if (r > 160 and g < 80 and b < 80): # if this pixel is red
                rx = x
                ry = y
                brk = True
                break
        if brk: # break if we have found the pixel
           break
    brk = False
    x = 39
    while (x > 0):
        for y in range(80):
            r, g, b, trash = (image.getpixel((x, y)))
            if (r > 160 and g < 80 and b < 80): # if this pixel is red
                lx = x
                ly = y
                brk = True
                break
        if brk: # break if we have found the pixel
            break
        x = x - 1

    # handle the situation where the car was not detected
    if (lx == 0 and ly == 0):
        ly = 60
        lx = 10
    if (rx == 0 and ry == 0):
        ry = 60
        rx = 30

    print (str(lx) + ", " + str(ly) + ", " + str(rx) + ", " + str(ry))

    # now find the center point coordinates
    cx = int((lx + rx) / 2)
    cy = int((ly + ry) / 2)

    # get the y coordinate of the grass beneath this center point
    gy = 0
    for y in range(80):
        r, g, b, trash = (image.getpixel((cx, y)))
        if (r < 180 and g > 200 and b < 100):  # if this pixel is red
            gy = y
            break

    # get the height of the car by subtracting it's center y value from the y value of the grass
    height = abs(cy - gy)
    print(height)

    return(height)

# example: height = getHeight("testImages/shot2OG.png")