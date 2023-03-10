from App import *

@app.route("/check_pump_status/<iot_module_id>")
def checkPumpStatus(iot_module_id):
    if not validate_id(iot_module_id):
        return jsonify({"response":"Invalid keys"}),404
    pre_check_data=iot_modules.find({"_id":bson.objectid.ObjectId(iot_module_id)})
    pre_check_data=[i for i in pre_check_data]
    if len(pre_check_data)>0:
        if pre_check_data[0]['pump_status']=="ON":
            return jsonify({"response":"ON"}),201
        else:
            return jsonify({"response":"OFF"}),202
    else:
        return jsonify({"response":"Invalid keys"}),404

@app.route("/change_pump_status",methods=["POST","GET"])
def changePumpStatus():
    if isPostMethod():
        if isLoggedIn():
            iot_module_id=request.json['module_id']
            pump_status=request.json['current_status']
            pump_status = "ON" if pump_status=="OFF" else "OFF"
            if not validate_id(iot_module_id):
                return jsonify({"response":"Invalid keys"}),404
            pre_check_data=iot_modules.find({"_id":bson.objectid.ObjectId(iot_module_id),"owner_id":session['id']})
            pre_check_data=[i for i in pre_check_data]
            if len(pre_check_data)>0:
                iot_modules.update_one({"_id":bson.objectid.ObjectId(iot_module_id)},{"$set":{"pump_status":pump_status}})
                return jsonify({"response":"Pump status changed"})
            else:
                return jsonify({"response":"Invalid keys"}),404
        else:
            return jsonify({
                "response":"Authentication Required"
            })
    return jsonify({"response":"Request not allowed"}),403