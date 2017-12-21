from keras.models import Sequential

from keras.models import model_from_json

class NNModelSaver(object):
    """description of class"""

    @staticmethod
    def saveModel(model, fileName):
        if not (type(model) == Sequential):
            return None

        # serialize model to JSON
        model_json = model.to_json()
        with open(fileName, "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(fileName)
 
    @staticmethod
    def loadModel(fileName):
        # load json and create model
        json_file = open(fileName, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        return loaded_model

