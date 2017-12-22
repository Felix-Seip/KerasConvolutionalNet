#omport required packages
from keras.preprocessing.image import ImageDataGenerator
from CNNClassifier import CNNClassifier
from NNModelSaver import NNModelSaver
import _winapi as winAPI
import os
import sys

numImageChannels    = 3         #To be handled from interface
kernelSize          = 3         #To be handled from interface
imageHeight         = 100       #To be handled from interface
imageWidth          = 100       #To be handled from interface
numConvFilters      = 32        #To be handled from interface
maxPoolingPoolSize  = (2, 2)    #To be handled from interface

fileHandle = winAPI.CreateFile("\\\\.\\pipe\\Demo", winAPI.GENERIC_READ | winAPI.GENERIC_WRITE, 0, 0, winAPI.OPEN_EXISTING, 0, 0)


#print('Would you like to load the model from a .h5 file? Y/N') #To be handled from interface
loadFileAnswer = sys.argv[1] #input()

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
    
    #print('Please specify the directory for the training set:')#To be handled from interface
    trainingSetDir = sys.argv[2] #input()
    training_set = train_datagen.flow_from_directory(trainingSetDir,
                                                     target_size = (100, 100),
                                                     batch_size = 32,
                                                     class_mode = 'categorical') #to make multi-class change binary to categorical
    
    #print('Please specify the directory for the test set:')#To be handled from interface
    testSetDir = sys.argv[3] #input()
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
    data = winAPI.ReadFile(fileHandle, 4096)
    print(data)
    #if os.path.exists(data):
    #    model.makeModelPrediction(data, training_set)
    #    winAPI.WriteFile(fileHandle, bytes(data), 0)
    #else:
    winAPI.WriteFile(fileHandle, b'Hello World', 0)