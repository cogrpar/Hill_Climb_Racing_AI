import numpy
import os
from PIL import Image
from sklearn.utils import shuffle

# this function will generate two arrays that store the training images and the corresponding angle of the car in those images
def generateTraining():
    trainingData = []
    labelData = []

    track = 0 # an index int to select every nth image in each file
    n = 2 # this is the fraction of the dataset to be used (1/n), which can be adjusted to save memory

    # loop over all of the images and add them to the datasets
    for file in os.listdir("trainingData/rotations/p0"):
        image = Image.open("trainingData/rotations/p0/" + file)

        # create the array that will store the image pixel data
        pix_data = []

        for x in range(50):
            for y in range(50):
                pix = image.getpixel((x, y))
                if(pix[0] != 0):
                    pix_data.append(1) # add the pixel value to the array
                else:
                    pix_data.append(0) # add the pixel value to the array

        # get the angle of this image from the file name
        trash, angle = file.split("t")
        angle, trash = angle.split(".p")
        angle = round(float(angle) / 10)
        angle = int(angle)

        # set the angle to 0 if it is 360
        if(angle == 36):
            angle = 0

        # now add the image data and the angle to the arrays
        track += 1
        if (track % n == 0):
            trainingData.append(pix_data)
            labelData.append(angle)

    for file in os.listdir("trainingData/rotations/p1"):
        image = Image.open("trainingData/rotations/p1/" + file)

        # create the array that will store the image pixel data
        pix_data = []

        for x in range(50):
            for y in range(50):
                pix = image.getpixel((x, y))
                pix_data.append(pix[0]/100) # add the pixel value to the array

        # get the angle of this image from the file name
        trash, angle = file.split("t")
        angle, trash = angle.split(".p")
        angle = round(float(angle) / 10)
        angle = int(angle)

        # set the angle to 0 if it is 360
        if (angle == 36):
            angle = 0

        # now add the image data and the angle to the arrays
        track += 1
        if (track % n == 0):
            trainingData.append(pix_data)
            labelData.append(angle)

    for file in os.listdir("trainingData/rotations/p2"):
        image = Image.open("trainingData/rotations/p2/" + file)

        # create the array that will store the image pixel data
        pix_data = []

        for x in range(50):
            for y in range(50):
                pix = image.getpixel((x, y))
                pix_data.append(pix[0]/100) # add the pixel value to the array

        # get the angle of this image from the file name
        trash, angle = file.split("t")
        angle, trash = angle.split(".p")
        angle = round(float(angle) / 10)
        angle = int(angle)

        # set the angle to 0 if it is 360
        if (angle == 36):
            angle = 0

        # now add the image data and the angle to the arrays
        track += 1
        if (track % n == 0):
            trainingData.append(pix_data)
            labelData.append(angle)

    for file in os.listdir("trainingData/rotations/p3"):
        image = Image.open("trainingData/rotations/p3/" + file)

        # create the array that will store the image pixel data
        pix_data = []

        for x in range(50):
            for y in range(50):
                pix = image.getpixel((x, y))
                pix_data.append(pix[0]/100) # add the pixel value to the array

        # get the angle of this image from the file name
        trash, angle = file.split("t")
        angle, trash = angle.split(".p")
        angle = round(float(angle) / 10)
        angle = int(angle)

        # set the angle to 0 if it is 360
        if (angle == 36):
            angle = 0

        # now add the image data and the angle to the arrays
        track += 1
        if (track % n == 0):
            trainingData.append(pix_data)
            labelData.append(angle)

    for file in os.listdir("trainingData/rotations/p4"):
        image = Image.open("trainingData/rotations/p4/" + file)

        # create the array that will store the image pixel data
        pix_data = []

        for x in range(50):
            for y in range(50):
                pix = image.getpixel((x, y))
                pix_data.append(pix[0]/100) # add the pixel value to the array

        # get the angle of this image from the file name
        trash, angle = file.split("t")
        angle, trash = angle.split(".p")
        angle = round(float(angle) / 10)
        angle = int(angle)

        # set the angle to 0 if it is 360
        if (angle == 36):
            angle = 0

        # now add the image data and the angle to the arrays
        track += 1
        if (track % n == 0):
            trainingData.append(pix_data)
            labelData.append(angle)

    # shuffle the datasets randomly
    labelData, trainingData = shuffle(labelData, trainingData)

    return (trainingData, labelData)
