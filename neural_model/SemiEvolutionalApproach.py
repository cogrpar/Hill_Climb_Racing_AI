# this was my second attempt at teaching an ANN to play hill climb racing
# it used a more Evolutionary like approach, where at first the model would learn to replicate my moves
# after that, it would record it's own movements and whenever it preformed well, it added that run to the dataset
# this caused all future iterations (or generations) to inherit some of the actions that helped that car preform

import ExtractTrainingData
import keyboard
from pynput.keyboard import Key, Controller
from time import sleep
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.utils import shuffle

keys = Controller()
print("starting...")

# start by loading the model and the training data
data = open("SEATrainingData.txt", "r")
dataStr = data.read()
dataStr = "data = " + dataStr
exec(dataStr)
print("fetched data")

model = keras.models.load_model('SEAModel.h5')
print("fetched model")

# declare a variable to store the distance traveled
distance = 0

# declare a new list to store the data from this run
currentData = [[], []]

# initialize the top score to be 600m
best = 600

sleep(5)

while True:
    # the fist thing is to take the screenshot
    ExtractTrainingData.screenshot.takeScreenshot()

    # check if we have died
    if (ExtractTrainingData.screenshot.death()):
        if (distance > best):
            # if we have a new top score
            best = distance
            print("new record: " + str(distance))
            for i in range(len(currentData[1])):
                data[0].append(currentData[0][i])
                data[1].append(currentData[1][i])
            # update the data file
            dataWrite = open("SEATrainingData.txt", "w")
            dataWrite.write(str(data))
            dataWrite.close()
            # train the model
            print("input lenght: " + str(len(data[0])))
            print("output lenght: " + str(len(data[1])))
            d1 = data[1]
            d0 = data[0]
            d1, d0 = shuffle(d1, d0)
            data[0] = d0
            data[1] = d1
            input = np.array(data[0])
            print(input.shape)
            input = input.reshape((len(data[1]), 130))
            output = np.array(data[1])
            output = output.reshape((len(data[1]), 1))
            print("input shape: " + str(input.shape))
            print("output shape: " + str(output.shape))
            print(output.shape)
            model.fit(x=input, y=output, validation_split=0.1, batch_size=20, epochs= 500, verbose=2)
            # save the trained model
            model.save('SEAModel.h5')
        currentData = [[], []]
        # restart the game by pressing space twice
        for i in range(2):
            keys.press(Key.space)
            sleep(1)
            keys.release(Key.space)
            sleep(1)

    # now extract the data from the image
    try:
        newDistance = ExtractTrainingData.screenshot.getDistance()
    except:
        newDistance = distance
    gameData = ExtractTrainingData.screenshot.extractData()
    gameData = gameData.reshape((1, 130))

    try: # update the distance if the read was successful
        distance = int(newDistance)
    except:
        pass

    pedal = model.predict(gameData)
    pedal = np.argmax(pedal)

    # add this iteration's move to the currentData list
    currentData[0].append(gameData.reshape(130).tolist())
    currentData[1].append(pedal)

    # execute the prediction
    if (pedal == 0):  # press brake (left arrow)
        print("brake")
        keys.release(Key.right)
        keys.release(Key.left)
        keys.press(Key.left)
    else:  # press gas (right arrow)
        print("gas")
        keys.release(Key.right)
        keys.release(Key.left)
        keys.press(Key.right)