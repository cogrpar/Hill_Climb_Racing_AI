# make sure to extract the zip archive containing the training data folders (trainingData/rotations.zip) before executing this script

from PIL import Image
import random

images = ["trainingData/shot1OG.png", "trainingData/shot2OG.png", "trainingData/shot3OG.png", "trainingData/shot4OG.png", "trainingData/shot5OG.png"]
initCarAngles = [35, 135, 280, 5, 106]  # approximate initial rotation of the car in each shot

# create black image to fill rotated corners
black = Image.new('RGB', (50, 50), (0, 0, 0, 255))

for num in range(5):
    image = Image.open(images[num])

    # crop the image
    box = (20, 250, 420, 650)
    image = image.crop(box)

    # now we need to downscale the image
    image = image.resize((50, 50))

    # now rotate the image so that the angle is 0
    image = image.rotate(initCarAngles[num])

    # loop over all pixels in the new image to isolate the car
    for x in range(50):
        for y in range(50):
            r, g, b, trash = (image.getpixel((x, y)))
            if (not(r > 160 and g < 80 and b < 80)):  # if this pixel is not the right shade of red, set it to 0 (black)
                image.putpixel((x, y), (0, 0, 0, 255))

    image.show()

    # now rotate the images by 1 degree at a time, saving each image with the angle in it's name
    for i in range(35950):
        imgRotated = image.rotate(i/100)
        # remove all white pixels
        blackTemp = black
        blackTemp.paste(imgRotated, (0,0))
        # convert the image to greyscale
        blackTemp = blackTemp.convert('LA')
        # translate the image by some random amount
        a = 1
        b = 0
        c = random.randint(-10, 10) # left/right
        d = 0
        e = 1
        f = random.randint(-10, 10) # up/down
        blackTemp = blackTemp.transform(blackTemp.size, Image.AFFINE, (a, b, c, d, e, f))
        # remove all white pixels
        output = black
        output.paste(blackTemp, (0, 0))
        # save the image
        output.save("trainingData/rotations/p" + str(num) + "/p" + str(num) + "rot" + str(i/100) + ".png")