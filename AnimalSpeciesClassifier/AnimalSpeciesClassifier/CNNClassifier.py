from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Dense

from keras.preprocessing import image

import os
import numpy as np


class CNNClassifier(object):
    """description of class"""
    
    cnnModel = None

    def __init__(self):
        self.cnnModel = Sequential()    #Creates a sequential model


    #classifier.add(Conv2D(numConvFilters, kernelSize, input_shape = (imageWidth, imageHeight, numImageChannels), activation = 'relu'))
    def createConvLayers(self, numConvLayers = 2, numConvFilters = 32, kernelSize = 3, input_shape = (100, 100, 3), poolingSize = (2, 2), activationFunction = 'relu'):
        if not (type(self.cnnModel) == Sequential):
            return None

        for i in range(numConvLayers):
            self.cnnModel.add(Conv2D(numConvFilters, kernelSize, input_shape = input_shape, activation = activationFunction))
            self.cnnModel.add(MaxPooling2D(poolingSize))


    def createFlatLayer(self):
        if not (type(self.cnnModel) == Sequential):
            return None

        self.cnnModel.add(Flatten())


    def createDenseLayer(self, numDenseLayers, dropout = 0.75,  neuronCount = 200, activationFunction = 'sigmoid'):
        '''
        Creates the given amount of dense layers
            numDenseLayers: The amount of layers to be created
            unitCount: The amount of inputs for the dense layer
            activationFunction: The activation function to be used
        '''

        if not (type(self.cnnModel) == Sequential):
            return None

        for i in range(numDenseLayers):
            self.cnnModel.add(Dense(units = neuronCount, activation = activationFunction))

        if int(dropout) == 0:
            return None

        self.cnnModel.add(Dropout(rate = dropout))


    def createOutputLayer(self, outputNeurons = 1, activationFunction = 'softmax'):
        self.cnnModel.add(Dense(units = outputNeurons, activation = activationFunction))


    def compile(self, modelOptimizer = 'adam', lossFunction = 'categorical_crossentropy'):
        self.cnnModel.compile(optimizer = modelOptimizer, loss = lossFunction, metrics = ['accuracy']) #change binary_crossentropy to categorical_crossentropy


    def makeModelPrediction(self, fileName, training_set, targetImageSize = (100, 100)):
        
        test_image = image.load_img(fileName, target_size = targetImageSize)
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = self.cnnModel.predict(test_image)
        training_set.class_indices

        print(result[0])



