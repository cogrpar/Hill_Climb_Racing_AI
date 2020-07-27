# this was my first attempt at teaching an ANN to play hill climb racing
# it used a punishment/reward approach
# it was slightly successful, as the car learned basic actions like slowing down at the tops of hills to avoid toppling over, but nothing too complex

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
data = open("RAPATrainingData.txt", "r")
dataStr = data.read()
dataStr = "data = " + dataStr

exec(dataStr)

print("fetched data")

try:
    model = keras.models.load_model('RAPAModel.h5')
except:
    model = Sequential(
        [
        Input(shape=(130,)),
        Dense(units=8, activation='relu'),
        Dense(units=16, activation='relu'),
        Dense(units=2, activation='softmax')
        ]
    )

print("fetched model")

# initalize the value of n, which is the delay interval
n = 1
# initalize the correct percentage as 0 percent
p = 0
success = 0
iterations = 1

sleep(5) # delay for 5 seconds

while True:

    print("predicted:")
    iterations += 1

    # the fist thing is to take the screenshot
    ExtractTrainingData.screenshot.takeScreenshot()

    # now extract the data from the image
    distance = ExtractTrainingData.screenshot.getDistance()
    gameData = ExtractTrainingData.screenshot.extractData()

    # now arrange the training data and make a prediction
    gameData = gameData.reshape((1, 130))
    pedal = model.predict(gameData) # 0 is brake 1 is gas
    pedal = np.argmax(pedal)
    gameData = gameData.reshape((130))

    # execute the prediction
    if (pedal == 0): # press brake (left arrow)
        print("brake")
        keys.press(Key.left)
        sleep(n)
        keys.release(Key.left)
    else: # press gas (right arrow)
        print("gas")
        keys.press(Key.right)
        sleep(n)
        keys.release(Key.right)

    # now wait n seconds to see what the car does
    ExtractTrainingData.screenshot.takeScreenshot()

    # check to see if the car has died or not moved forward
    dead = ExtractTrainingData.screenshot.death()
    newDistance = ExtractTrainingData.screenshot.getDistance()
    try:
        start = int(distance)
        stop = int(newDistance)
        read = True
    except:
        start = 0
        stop = 0
        print("could not read distance")
        read = False

    if (read == True):
        if (not dead):
            if (stop - start > 1):
                data[0].append(gameData.tolist())
                progress = True
                print("right")
                success += 1
            else:
                data[0].append(gameData.tolist())
                progress = False
                print("wrong")
        else:
            data[0].append(gameData.tolist())
            progress = False
            print("wrong")

        # use that information to set the training answer to the correct state
        if (progress):
            correctPrediction = pedal
        else:
            correctPrediction = not(pedal)

        # append that state to the data array
        data[1].append(int(correctPrediction))

    if (dead):
        # now that we have died, we should pause to train the network a bit, and then restart
        # go back to the event that caused us to die and reverse it
        steps = int(3/n) + 2
        steps = len(data[1]) - 1 - steps
        for i in range(3):
            data[1][steps] = int(not(data[1][steps]))
            steps += 1
        # prepare the model to be trained
        model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        # train the model
        d1 = data[1]
        d0 = data[0]
        d1, d0 = shuffle(d1, d0)
        data[0] = d0
        data[1] = d1
        input = np.array(data[0])
        input = input.reshape((len(data[1]), 130))
        output = np.array(data[1])
        output = output.reshape((len(data[1]), 1))
        print(output.shape)
        if (len(data[1]) < 100):
            batchSize = int(len(data[1]) / 5)
        else:
            batchSize = 30
        model.fit(x=input, y=output, batch_size=batchSize, epochs=400, verbose=2)
        # save the model state
        model.save('RAPAModel.h5')
        # update the data file
        dataWrite = open("RAPATrainingData.txt", "w")
        dataWrite.write(str(data))
        dataWrite.close()
        # restart the game by pressing space twice
        for i in range(2):
            keys.press(Key.space)
            sleep(1)
            keys.release(Key.space)
            sleep(1)
        p = 0
        success = 0
        iterations = 1

    # calculate the success rate and print it
    p = success / iterations
    print("success rate: " + str(p*100) + "%")
