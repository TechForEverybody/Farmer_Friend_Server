from App import *

def increaseTrialsCount(type):
    if session['ip_address']!=request.remote_user:
        session[type]=1
        return
    try:
        session[type]=session[type]+1
    except:
        session[type]=1

def checkTrialsCount(type):
    try:
        if session[type]<5:
            return True
        else:
            return jsonify({"response":"Your Trial Count is exceeded","count":session[type]}),429
    except:
        return True



@app.route('/crop_suggestion',methods=['POST'])
def crop_suggestion():
    if isPostMethod():
        try:
            data=request.get_json()
            temperature=data['temperature']
            humidity=data['humidity']
            result=cropSuggestionSystemModelProcessor.predictCropClass([temperature,humidity])
            print(result)
            return jsonify({
                "response":{
                    "result":result[0],
                    "image_url":"http://localhost"+result[1]
                }
            })
        except Exception as e:
            return jsonify({
                "response":"Some Error Occurred"
            }),403
    else:
        return jsonify({"response":"Request not allowed"}),403

@app.route("/get_crop_prediction_result",methods=["POST"])
def get_crop_prediction_result():
    checkTrialsCount("crop_detection")
    if isPostMethod():
        try:
            increaseTrialsCount("crop_detection")
            print(session['file_name'])
            image_array=cropDiseaseDetectionInputProcessor.preprocessCropTypeInput("."+session['file_name'])
            # print(image_array)
            result=cropDiseaseDetectionModelProcessor.predictCropClass(image_array)
            return jsonify({
                "response":{
                    "result":result[0],
                    "confidence_value":str(result[1])
                }
            })
        except Exception as e:
            print(e)
            return jsonify({
                "response":"Some Error Occurred"
            }),403
    else:
        return jsonify({"response":"Request not allowed"}),403


@app.route("/get_crop_diseased_prediction_result",methods=["POST"])
def get_crop_diseased_prediction_result():
    checkTrialsCount("disease_detection")
    if isPostMethod():
        try:
            increaseTrialsCount("disease_detection")
            print(session['file_name'])
            crop_type=request.get_json()['crop_name']
            is_crop_type_known=request.get_json()['isCropTypeKnown']
            image_array=cropDiseaseDetectionInputProcessor.preprocessCropTypeInput("."+session['file_name'])
            crop_name=cropDiseaseDetectionModelProcessor.predictCropClass(image_array)
            crop_name=crop_name[0]
            image_array=cropDiseaseDetectionInputProcessor.preprocessCropDiseaseTypeInput("."+session['file_name'])
            result=cropDiseaseDetectionModelProcessor.predictDiseaseClass(image_array,crop_name if  is_crop_type_known=="false" else crop_type)
            return jsonify({
                "response":{
                    "crop_name":crop_name if  is_crop_type_known=="false" else crop_type,
                    "disease_name":result[0],
                    "confidence_value":str(result[1])
                }
            })
        except Exception as e:
            print(e)
            return jsonify({
                "response":"Some Error Occurred"
            }),403
    else:
        return jsonify({"response":"Request not allowed"}),403

@app.route('/upload_file',methods=['POST','GET'])
def upload():
    global file_name
    if request.method=='POST':
        try:
            print(request.files['file'])
            file=request.files['file']
            file_name=file.filename
            extension=file_name.split(".")[-1]
            print(extension)
            milliseconds_value=round(time.time()*1000)
            file_name=f"{milliseconds_value}.{extension}"
            print(file_name)
            file_path=f"/static/Images/data/{file_name}"
            file.filename=file_name
            session['file_name']=file_path
            print(file)
            file.save(f"static/Images/data/{file_name}")
            return jsonify({'response':"http://localhost"+file_path}),200
        except Exception as e:
            print(e)
            return jsonify({"response":"Some Error Occurred"}),403
    else:
        return jsonify({"response":"Request not allowed"}),403





