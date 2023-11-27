from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt

classifier = Sequential()

classifier.add(Convolution2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

classifier.add(Convolution2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

classifier.add(Flatten())

classifier.add(Dense(units=128, activation='relu'))
classifier.add(Dense(units=4, activation='softmax'))

(classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']))

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1. / 255,      #pixels ranging 0 - 255 grey scale
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

training_set = train_datagen.flow_from_directory('Dataset/train',
                                                 target_size=(64, 64),
                                                 batch_size=32,
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory('Dataset/test',
                                            target_size=(64, 64),
                                            batch_size=32,
                                            class_mode='categorical')

csv_logger = tf.keras.callbacks.CSVLogger('metrics.csv')

classifier.fit(training_set,
                         steps_per_epoch=4,  # number of training images
                         epochs=100,
                         validation_data=test_set,
                         validation_steps=4,  # number of test images
                         callbacks=[csv_logger])
classifier.save('brain_model.h5')

