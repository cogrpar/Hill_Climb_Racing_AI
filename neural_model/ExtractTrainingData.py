from tensorflow import keras
from PIL import Image
import numpy as np
import pyautogui
import pytesseract
from PIL import ImageFilter

class dataExtractor: # class containing the methods for extracting the data from an image

    def getAngle(screenshot): # this code is used to determine the car's angle from the screenshot
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
                r, g, b = (image.getpixel((x, y)))
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
        if (angle == 360):
            angle = 0

        return (angle)

    def getHeight(screenshot): # this code is used to determine the car's height from the screenshot
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
                r, g, b = (image.getpixel((x, y)))
                if (r > 160 and g < 80 and b < 80):  # if this pixel is red
                    rx = x
                    ry = y
                    brk = True
                    break
            if brk:  # break if we have found the pixel
                break
        brk = False
        x = 39
        while (x > 0):
            for y in range(80):
                r, g, b = (image.getpixel((x, y)))
                if (r > 160 and g < 80 and b < 80):  # if this pixel is red
                    lx = x
                    ly = y
                    brk = True
                    break
            if brk:  # break if we have found the pixel
                break
            x = x - 1

        # handle the situation where the car was not detected
        if (lx == 0 and ly == 0):
            ly = 60
            lx = 10
        if (rx == 0 and ry == 0):
            ry = 60
            rx = 30

        #print(str(lx) + ", " + str(ly) + ", " + str(rx) + ", " + str(ry))

        # now find the center point coordinates
        cx = int((lx + rx) / 2)
        cy = int((ly + ry) / 2)

        # get the y coordinate of the grass beneath this center point
        gy = 0
        for y in range(80):
            r, g, b = (image.getpixel((cx, y)))
            if (r < 180 and g > 200 and b < 100):  # if this pixel is green
                gy = y
                break

        # get the height of the car by subtracting it's center y value from the y value of the grass
        height = abs(cy - gy)
        #print(height)

        return (height)

    def getTerrain(screenshot): # this code is used to determine the shape of the terrain from the screenshot
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
                r, g, b = (image.getpixel((x, y)))
                if (r < 180 and g > 200 and b < 100):  # if this pixel is green
                    heights.append(69 - y)
                    break
                if (y == 0):  # if there is no ground in this position
                    heights.append(0)
                    break
                y -= 1
            x += 1

        # return the array containing the height information
        return heights

class screenshot: # class containing methods for taking screenshots and call methods of the dataExtractor class

    def takeScreenshot(): # method to take the screenshot that is going to be used
        pyautogui.screenshot().save("screenshot.png")

    def extractData(): # method to extract the data from the screenshot that was taken
        angle = dataExtractor.getAngle("screenshot.png")
        height = dataExtractor.getHeight("screenshot.png")
        terrain = dataExtractor.getTerrain("screenshot.png")

        # concentrate all of the data to a single array
        data = [angle, height]
        for i in terrain:
            data.append(i)

        #return the array
        data = np.array(data)
        return data

    def getDistance(): # this method takes the screenshot and extracts the distance that the car has traveled
        # open the screenshot and crop to just show the distance meter
        image = Image.open("screenshot.png")
        box = (320, 35, 450, 95)
        image = image.crop(box)
        for x in range(130): # convert the image to all black or all white
            for y in range(60):
                r, g, b = image.getpixel((x, y))
                if (r > 250 and g > 250 and b > 250):
                    image.putpixel((x, y), (0, 0, 0, 255))
                else:
                    image.putpixel((x, y), (255, 255, 255, 255))
        image = image.filter(ImageFilter.SMOOTH)

        # set up pytesseract (you need to install it from here first: https://github.com/UB-Mannheim/tesseract/wiki)
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        text = str(pytesseract.image_to_string(image))
        # remove all non numbers
        text = text.replace("m", "")
        # print("distance: " + text)

        return text

    def death(): # method to determine if the player has died
        image = Image.open("screenshot.png")
        pix = image.getpixel((500, 550))
        if(pix == (255, 255, 255)): # if there is a white pixel in this position, then the user is dead
            return True
        else: # the user is not dead
            return False
