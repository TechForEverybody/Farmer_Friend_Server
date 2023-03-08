from App import *


@app.route("/get_dashboard_data",methods=["POST","GET"])
def getDashboardData():
    if isPostMethod():
        if isLoggedIn():
            initial_data=iot_modules.find({"owner_id":session['id']},{"senor_key":0})
            initial_data=[i for i in initial_data]
            number_of_sensors=sum([i['number_of_sensors'] for i in initial_data])
            iot_modules_list=[str(i['_id']) for i in initial_data]
            [ i.pop("_id") for i in initial_data]            
            temperature_data=[]
            humidity_data=[]
            moisture_data=[]
            for module_id in iot_modules_list:
                data=sensors_data.find({"iot_module_id":module_id},{"temperature":1,"humidity":1,"soil_moisture":1}).limit(25).sort("_id",-1)
                data=[i for i in data]
                print(data)
                temperature_data.append([i['temperature'] for i in data])
                humidity_data.append([i['humidity'] for i in data])
                moisture_data.append([i['soil_moisture'] for i in data])
            final_data={
                "number_of_modules":len(initial_data),
                "module_ids":iot_modules_list,
                "number_of_sensors":number_of_sensors,
                "initial_data": initial_data,
                "temperature_data":temperature_data,
                "humidity_data":humidity_data,
                "moisture_data":moisture_data
            }
            print(final_data)
            return jsonify({
                "response":final_data
            })
        else:
            return jsonify({
                "response":"Authentication Required"
            })
    return jsonify({"response":"Request not allowed"}),403


@app.route("/get_irrigation_data",methods=["POST","GET"])
def getIrrigationData():
    if isPostMethod():
        if isLoggedIn():
            iot_module_id=request.json["module_id"]
            irrigation_data=sensors_data.find({"iot_module_id":iot_module_id,"owner_id":session['id']},{"temperature":1,"humidity":1,"soil_moisture":1,"_id":0,"timestamp":1}).limit(25).sort("_id",-1)
            irrigation_data=[i for i in irrigation_data]
            module_data=iot_modules.find({"_id":bson.objectid.ObjectId(iot_module_id)},{"_id":0,"owner_id":0,"sensor_key":0})
            module_data=[i for i in module_data]
            temperature_data=[i['temperature'] for i in irrigation_data]
            temperature_data.reverse()
            humidity_data=[i['humidity'] for i in irrigation_data]
            humidity_data.reverse()
            soil_moisture_data=[i['soil_moisture'] for i in irrigation_data]
            soil_moisture_data.reverse()
            time_stamp=[i['timestamp'] for i in irrigation_data]
            time_stamp.reverse()
            data=sensors_data.find({"iot_module_id":iot_module_id},{"_id":0,"iot_module_id":0}).limit(1).sort("_id",-1)
            data=[i for i in data]
            final_data={
                "module_data":module_data,
                "recent_data":data[0] if len(data)>0 else "No data",
                "irrigation_data":{
                    "temperature_data":temperature_data,
                    "humidity_data":humidity_data,
                    "soil_moisture_data":soil_moisture_data,
                    "time_stamps":time_stamp
                }
            }
            print(final_data)
            return jsonify({
                "response":final_data
            })
        else:
            return jsonify({
                "response":"Authentication Required"
            })
    return jsonify({"response":"Request not allowed"}),403