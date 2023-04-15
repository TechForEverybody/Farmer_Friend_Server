import joblib
from .Variables import *


class ModelProcessor:
    def __init__(self):
        print("🚀🚀🚀Crop Suggestion Model Processor is Initialized🚀🚀")
    def setModel(self,ModelPath):
        self.model=joblib.load(ModelPath)
        print("Model is Connected")
    def predictCropClass(self,inputArray):
        prediction=self.model.predict([inputArray])
        return prediction[0],image_urls[prediction[0]]
