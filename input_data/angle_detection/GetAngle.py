# this code is used to determine the car's angle from the screenshot
from tensorflow import keras
from PIL import Image
import numpy as np

def getAngle (screenshot):
    # open the screenshot
    image = Image.open(screenshot)

    # open the trained angle detection neural model
    model = keras.models.load_model('angleModel.h5')

    # crop the image
    box = (20, 250, 420, 650)
    image = image.crop(box)

    # now we need to downscale the image
    image = image.resize((50, 50))

    # loop over all pixels in the new image to isolate the car
    layer = []
    imgArray = []
    for x in range(50):
        for y in range(50):
            r, g, b, trash = (image.getpixel((x, y)))
            if (r > 160 and g < 80 and b < 80):  # if this pixel is the right shade of red add it to the array as a 1
                layer.append(1)
            else:
                layer.append(0)
        imgArray.append(layer)
        layer = []

    # turn the array into a numpy array and resize it
    imgArray = np.array(imgArray)
    imgArray = imgArray.reshape((1, 50, 50, 1))

    # use the model to predict the angle
    prediction = model.predict(imgArray)

    # find the most probable prediction and return that angle
    angle = np.argmax(prediction)
    angle = angle * 10
    angle = 360 - angle
    if(angle == 360):
        angle = 0

    return(angle)

# example: angle = getAngle("trainingData/shot5OG.png")