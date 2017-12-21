#omport required packages
from keras.preprocessing.image import ImageDataGenerator
from CNNClassifier import CNNClassifier
from NNModelSaver import NNModelSaver
import os

numImageChannels    = 3
kernelSize          = 3
imageHeight         = 100
imageWidth          = 100
numConvFilters      = 32
maxPoolingPoolSize  = (2, 2)

if os.path.isfile('testfile.txt'):
    model = NNModelSaver.loadModel('testfile.txt')

else:
    model = CNNClassifier()

    model.createConvLayers()    #Creates the layers following the CNN architecture: Conv -> ReLu -> Pooling 
    model.createFlatLayer()     #Flattens the last pooling layer
    model.createDenseLayer(2)   #Creates the dense layers before the output layer. Also applies dropout
    model.createOutputLayer()
    model.compile()
    
    
    
    train_datagen = ImageDataGenerator(rescale = 1./255,
                                       shear_range = 0.2,
                                       zoom_range = 0.2,
                                       horizontal_flip = True)
    
    test_datagen = ImageDataGenerator(rescale = 1./255)
    
    training_set = train_datagen.flow_from_directory('training_set',
                                                     target_size = (100, 100),
                                                     batch_size = 32,
                                                     class_mode = 'binary') #to make multi-class change binary to categorical
    
    test_set = test_datagen.flow_from_directory('test_set',
                                                target_size = (100, 100),
                                                batch_size = 32,
                                                class_mode = 'binary') #to make multi-class change binary to categorical
    
    model.cnnModel.fit_generator(training_set,
                             steps_per_epoch = 50,
                             epochs = 10,
                             validation_data = test_set,
                             validation_steps = 50)

model.makeModelPrediction('C:\\Users\\SeipF\\source\\repos\\AnimalSpeciesClassifier\\AnimalSpeciesClassifier\\dataset\\single_prediction\\cat_or_dog_1.jpg', training_set)

NNModelSaver.saveModel(model.cnnModel, 'testfile.txt')