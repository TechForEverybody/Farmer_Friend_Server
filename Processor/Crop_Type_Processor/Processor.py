import numpy
import tensorflow
import cv2
from .Variables import *

class InputPropcessor:
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
    def preprocessInput(self,image_path,method='mean',range_=(60,200)):
        image_array=cv2.imread(image_path,cv2.IMREAD_COLOR)
        image_array=cv2.cvtColor(image_array,cv2.COLOR_BGR2RGB)
        image_array=cv2.resize(image_array,resize_dimension)
        image_array=InputPropcessor.getMaxMinMeanMethodBasedArray(image_array,method=method,range_=range_)
        image_array=numpy.expand_dims([image_array],axis=-1)
        return image_array

class ModelProcessor:
    def __init__(self):
        print("🚀🚀🚀Crop Detection Model Processor is Initialized🚀🚀")
    def setModel(self,ModelPath):
        self.model=tensorflow.keras.models.load_model(ModelPath)
        print("Model is Connected")
    def predictClass(self,image_array):
        print(image_array.shape)
        prediction=self.model.predict(image_array)
        return class_list[numpy.argmax(prediction[0])]

