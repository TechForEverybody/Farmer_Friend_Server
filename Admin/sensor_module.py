from App import *

@app.route("/add_module",methods=["POST","GET"])
def addModule():
    if isPostMethod():
        number_of_sensors=request.json['number_of_sensors']
        iot_module_details={
            "pump_status":"OFF",
            "number_of_sensors":number_of_sensors,
        }
        iot_module_id=iot_modules.insert_one(iot_module_details).inserted_id
        return jsonify({"response":str(iot_module_id)})
    else:
        return jsonify({"response":"Request not allowed"}),403

@app.route("/connect_owner",methods=["POST","GET"])
def connectOwner():
    if isPostMethod():
        owner_id=request.json['owner_id']
        if not validate_id(owner_id):
            return jsonify({"response":"Invalid keys"}),404
        owner=users.find({"_id":bson.objectid.ObjectId(owner_id)},{"_id":0})
        owner=[i for i in owner]
        print(owner)
        if  len(owner)>0:
            number_of_sensors=request.json['number_of_sensors']
            iot_module_details={
                "owner_id":owner_id,
                "pump_status":"OFF",
                "number_of_sensors":number_of_sensors,
            }
            iot_module_id=iot_modules.insert_one(iot_module_details).inserted_id
            return jsonify({"response":str(iot_module_id)})
        return jsonify({"response":"Invalid keys"}),404
    else:
        return jsonify({"response":"Request not allowed"}),403