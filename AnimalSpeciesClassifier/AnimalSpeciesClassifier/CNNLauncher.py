#omport required packages
from keras.preprocessing.image import ImageDataGenerator
from CNNClassifier import CNNClassifier
from NNModelSaver import NNModelSaver
import os
import sys

numImageChannels    = 3
kernelSize          = 3
imageHeight         = 100
imageWidth          = 100
numConvFilters      = 32
maxPoolingPoolSize  = (2, 2)

print('Would you like to load the model from a .h5 file? Y/N')
loadFileAnswer = input()

if loadFileAnswer.upper() == 'Y':

    fileToLoad = input()
    if os.path.isfile(fileToLoad):
        model = NNModelSaver.loadModel(fileToLoad )

else:
    model = CNNClassifier()

    model.createConvLayers()    #Creates the layers following the CNN architecture: Conv -> ReLu -> Pooling 
    model.createFlatLayer()     #Flattens the last pooling layer
    model.createDenseLayer(2)   #Creates the dense layers before the output layer. Also applies dropout
    model.createOutputLayer(3)
    model.compile()
    
    train_datagen = ImageDataGenerator(rescale = 1./255,
                                       shear_range = 0.2,
                                       zoom_range = 0.2,
                                       horizontal_flip = True)
    
    test_datagen = ImageDataGenerator(rescale = 1./255)
    
    print('Please specify the directory for the training set:')
    trainingSetDir = input()
    training_set = train_datagen.flow_from_directory(trainingSetDir,
                                                     target_size = (100, 100),
                                                     batch_size = 32,
                                                     class_mode = 'categorical') #to make multi-class change binary to categorical
    
    print('Please specify the directory for the test set:')
    testSetDir = input()
    test_set = test_datagen.flow_from_directory(testSetDir,
                                                target_size = (100, 100),
                                                batch_size = 32,
                                                class_mode = 'categorical') #to make multi-class change binary to categorical
    
    model.cnnModel.fit_generator(training_set,
                             steps_per_epoch = 150,
                             epochs = 2,
                             validation_data = test_set,
                             validation_steps = 150)

#print('Where should the file be saved to?')
#fileToSaveModel = input()
#NNModelSaver.saveModel(model.cnnModel, fileToSaveModel)

while True:
    print('Please enter file path to an image that you would like to classify:')
    fileToClassify = input()
    model.makeModelPrediction(fileToClassify, training_set)
    sys.stdout.flush()