from App import *

@app.route("/check_pump_status/<iot_module_id>")
def checkPumpStatus(iot_module_id):
    if not validate_id(iot_module_id):
        return jsonify({"response":"Invalid keys"}),404
    pre_check_data=iot_modules.find({"_id":bson.objectid.ObjectId(iot_module_id)})
    pre_check_data=[i for i in pre_check_data]
    if len(pre_check_data)>0:
        return jsonify({"response":pre_check_data[0]['pump_status']})
    else:
        return jsonify({"response":"Invalid keys"}),404

@app.route("/change_pump_status/<iot_module_id>/<pump_status>")
def changePumpStatus(iot_module_id,pump_status):
    if not validate_id(iot_module_id):
        return jsonify({"response":"Invalid keys"}),404
    pre_check_data=iot_modules.find({"_id":bson.objectid.ObjectId(iot_module_id)})
    pre_check_data=[i for i in pre_check_data]
    if len(pre_check_data)>0:
        iot_modules.update_one({"_id":bson.objectid.ObjectId(iot_module_id)},{"$set":{"pump_status":pump_status}})
        return jsonify({"response":"Pump status changed"})
    else:
        return jsonify({"response":"Invalid keys"}),404