import GenerateInputArrays
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

# set all layers to float 64
tf.keras.backend.set_floatx('float64')

# generate the training data
print("fetching training data...")
trainingData, labelData = GenerateInputArrays.generateTraining()
trainingData = np.array(trainingData)
labelData = np.array(labelData)

# reshape the arrays
trainingData = trainingData.reshape((trainingData.shape[0], 50, 50, 1))

# Define Sequential model with 3 layers
model = Sequential(
    [
        Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding = 'same', input_shape=(50,50,1)),
        MaxPool2D(pool_size=(2, 2), strides=2),
        Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding = 'same'),
        MaxPool2D(pool_size=(2, 2), strides=2),
        Flatten(),
        Dense(units=36, activation='softmax')
    ]
)

# prepare the model to be trained
model.compile(optimizer=Adam(learning_rate=0.007), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# train the model
model.fit(x=trainingData, y=labelData, validation_split=0.1, batch_size=180, epochs=40, verbose=2)

print(model)
# save model
model.save('angleModel.h5')
