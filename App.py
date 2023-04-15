from flask import Flask,jsonify,request,session,send_from_directory
from Database.schema import *
import hashlib
import datetime
import time
import os
import bson.json_util
from Modules.validate_id import *
# from flask_cors import CORS
import uuid
# from Processor.Crop_Suggestion_System_Processor.Processor import ModelProcessor as CropSuggestionSystemModelProcessor
# from Processor.Crop_Disease_Detection_Processor.Processor import ModelProcessor as CropDiseaseDetectionModelProcessor, InputProcessor as CropDiseaseDetectionInputProcessor
# cropDiseaseDetectionModelProcessor=CropDiseaseDetectionModelProcessor()
# cropDiseaseDetectionInputProcessor=CropDiseaseDetectionInputProcessor()
# cropDiseaseDetectionModelProcessor.setCropDetectionModel("./Models/Crop_Type_Detection/DefinedModel_2.h5")

# cropSuggestionSystemModelProcessor=CropSuggestionSystemModelProcessor()
# cropSuggestionSystemModelProcessor.setModel("./Models/Crop_Suggestion/Model.joblib")


app = Flask(__name__)
app.secret_key="SHIVKUMAR_CHAUHAN"
# CORS(app)
def alterPumpStatus(iot_module_id,pump_status):
    iot_modules.update_one({"_id":bson.objectid.ObjectId(iot_module_id)},{"$set":{"pump_status":pump_status}})

start_limit=700
start_trails=0
def isPostMethod():
    if request.method=="POST":return True
    else:return False

def isLoggedIn():
    if "is_login" in session:return True
    else:return False

def getHashValue(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()



@app.route('/')
def index():
    session['ip']=request.remote_addr
    return jsonify({'your_ip_address': request.remote_addr}), 200