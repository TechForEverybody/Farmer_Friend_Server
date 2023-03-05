from App import *

@app.route('/save_sensor_data/<iot_module_id>/<float:temperature>/<float:humidity>/<float:moisture>')
def save_sensor_data(iot_module_id,temperature,humidity,moisture):
    if not validate_id(iot_module_id):
        return jsonify({"response":"Invalid keys"}),404
    pre_check_data=iot_modules.find({"_id":bson.objectid.ObjectId(iot_module_id)})
    pre_check_data=[i for i in pre_check_data]
    if len(pre_check_data)>0:
        sensors_data_instance={
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": moisture,
            "iot_module_id": iot_module_id,
            "timestamp":str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        }
        sensors_data.insert_one(sensors_data_instance)
        sensors_data_instance.pop("_id")
        sensors_data_instance.pop("iot_module_id")
        stats.update_one({"_id":bson.objectid.ObjectId("64042f655a893bec111c047a")},{"$inc":{"sensor_hits":1}})
        return jsonify({"response":sensors_data_instance})
    else:
        return jsonify({"response":"Invalid keys"}),404

@app.route('/get_sensor_data/<iot_module_id>')
def get_sensor_data(iot_module_id):
    if not validate_id(iot_module_id):
        return jsonify({"response":"Invalid keys"}),404
    pre_check_data=iot_modules.find({"_id":bson.objectid.ObjectId(iot_module_id)})
    pre_check_data=[i for i in pre_check_data]
    if len(pre_check_data)>0:
        data=sensors_data.find({"iot_module_id":iot_module_id},{"_id":0,"iot_module_id":0}).limit(20).sort("_id",-1)
        return jsonify({"response":[i for i in data]})    
    return jsonify({"response":"No data Found"})

@app.route('/get_recent_sensor_data/<iot_module_id>')
def get_recent_sensor_data(owner_id,iot_module_id):
    if not validate_id(iot_module_id):
        return jsonify({"response":"Invalid keys"}),404
    pre_check_data=iot_modules.find({"_id":bson.objectid.ObjectId(iot_module_id),"owner_id":owner_id})
    pre_check_data=[i for i in pre_check_data]
    if len(pre_check_data)>0:
        data=sensors_data.find({"iot_module_id":iot_module_id},{"_id":0}).limit(1).sort("_id",-1)
        data=[i for i in data]
        return jsonify({"response":data[0] if len(data)>0 else []})    
    return jsonify({"response":"No data Found"})
