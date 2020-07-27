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

# this script is part of the semi-evolutionary approach, and it watches me play and trains a network to replicate my actions

data = open("SEATrainingData.txt", "r")
dataStr = data.read()
dataStr = "data = " + dataStr

exec(dataStr)
play = True # set to true to record a run and set to false to train the network

if play:
    while True:
        ExtractTrainingData.screenshot.takeScreenshot()
        gameData = ExtractTrainingData.screenshot.extractData()

        if (ExtractTrainingData.screenshot.death()):
            # update the data file
            dataWrite = open("SEATrainingData.txt", "w")
            dataWrite.write(str(data))
            dataWrite.close()
            print("dataset length: " + str(len(data[1])))
            break

        if (keyboard.is_pressed("right arrow")):
            # print("right")
            data[1].append(1)
        else:
            # print("left")
            data[1].append(0)

        data[0].append(gameData.tolist())

if not(play):
    model = Sequential(
            [
            Input(shape=(130,)),
            Dense(units=32, activation='relu'),
            Dense(units=16, activation='relu'),
            Dense(units=2, activation='softmax')
            ]
    )

    model.compile(optimizer=Adam(learning_rate=0.005), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # train the model
    print("input lenght: " + str(len(data[0])))
    print("output lenght: " + str(len(data[1])))
    d1 = data[1]
    d0 = data[0]
    d1, d0 = shuffle(d1, d0)
    data[0] = d0
    data[1] = d1
    input = np.array(data[0])
    input = input.reshape((len(data[1]), 130))
    output = np.array(data[1])
    output = output.reshape((len(data[1]), 1))
    print("input shape: " + str(input.shape))
    print("output shape: " + str(output.shape))
    print(output.shape)
    model.fit(x=input, y=output, validation_split=0.1, batch_size=30, epochs=1000, verbose=2)
    # save the trained model
    model.save('SEAModel.h5')
