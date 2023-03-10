import numpy
import tensorflow
import cv2
from .Variables import *

class InputProcessor:
    def __init__(self):
        print("🚀🚀Crop Detection Image Processor is connected🚀🚀")
    @staticmethod
    def getMaxMinMeanMethodBasedArray(image_array,method='mean',range_=(0,255)):
        temp_array=[]
        for x in image_array:
            rows=[]
            for y in x:
                value=0
                if method=='mean':
                    value=sum(y)/len(y)
                elif method=='max':
                    value=max(y)
                elif method=='min':
                    value=min(y)
                if value<range_[0] or value>range_[1]:
                    value=0
                rows.append(value)
            temp_array.append(rows)
        temp_array=numpy.array(temp_array)
        return temp_array
    def preprocessCropTypeInput(self,image_path,method='mean',range_=(60,200)):
        image_array=cv2.imread(image_path,cv2.IMREAD_COLOR)
        image_array=cv2.cvtColor(image_array,cv2.COLOR_BGR2RGB)
        image_array=cv2.resize(image_array,resize_dimension)
        image_array=InputProcessor.getMaxMinMeanMethodBasedArray(image_array,method=method,range_=range_)
        image_array=numpy.expand_dims([image_array],axis=-1)
        return image_array
    def preprocessCropDiseaseTypeInput(self,image_path):
        image_array=cv2.imread(image_path,cv2.IMREAD_COLOR)
        image_array=cv2.cvtColor(image_array,cv2.COLOR_BGR2RGB)
        image_array=cv2.resize(image_array,resize_dimension)
        image_array=numpy.array([image_array])
        return image_array

class ModelProcessor:
    def __init__(self):
        self.ClassMapper={
            "Cotton":Cotton_class_list,
            "Sugarcane":Sugarcane_class_list,
            "Wheat":Wheat_class_list
        }
        print("🚀🚀🚀Crop Detection Model Processor is Initialized🚀🚀")
    def setCropDetectionModel(self,ModelPath):
        self.model=tensorflow.keras.models.load_model(ModelPath)
        print("Model is Connected")
    def predictCropClass(self,image_array):
        print(image_array.shape)
        prediction=self.model.predict(image_array)
        return class_list[numpy.argmax(prediction[0])],prediction[0][numpy.argmax(prediction[0])]
    def predictDiseaseClass(self,image_array,model_path,crop_type):
        print(image_array.shape)
        model=tensorflow.keras.models.load_model(model_path)
        prediction=model.predict(image_array)
        return self.ClassMapper[crop_type][numpy.argmax(prediction[0])],prediction[0][numpy.argmax(prediction[0])]

