from flask import Flask,jsonify,request
import pymongo
import pprint
connection_url="mongodb+srv://server:0987654321qwertyuiop@farmer-friend-sever.t17fn.mongodb.net/?retryWrites=true&w=majority"
mongodb_connection=pymongo.MongoClient(connection_url)
print(mongodb_connection)
realtime_data=mongodb_connection['realtime-data']
sensors_list=realtime_data['sensors']
sensors_data=realtime_data['sensors_data']
app = Flask(__name__)
module_keys=["93a77eb3-856c-49fc-8a6d-44a7e822f25f"]
current_data=[]




@app.route('/')
def index():
    return jsonify({'your_ip_address': request.remote_addr}), 200

@app.route('/save_sensor_data/<iot_module_key>/<float:temperature>/<float:humidity>/<float:moisture>')
def save_sensor_data(iot_module_key,temperature,humidity,moisture):
    global current_data
    if iot_module_key in module_keys:
        sensors_data_instance={
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": moisture,
            "sensor_id": "6402bc824c6eac8bda2e1c38"
        }
        sensors_data.insert_one(sensors_data_instance)
        return jsonify({"data":sensors_data_instance})
    else:
        return jsonify({"data":"Invalid key"})


@app.route('/get_sensor_data/<id>')
def get_sensor_data(id):
    global current_data
    data = sensors_data.find({"sensor_id":id},{"_id":0,"sensor_id":0}).sort("_id",-1)
    data=[i for i in data]
    print(len(list(data)))
    if len(list(data))>0:
        return jsonify({"data":[i for i in data]})    
    return jsonify({"data":"No data Found"})

@app.route('/get_recent_sensor_data/<id>')
def get_recent_sensor_data(id):
    global current_data
    data = sensors_data.find_one({"sensor_id":id},{"_id":0,"sensor_id":0})
    return jsonify({"data":data if data else "Why are you here"})    


@app.errorhandler(404)
def not_found(error):
    return jsonify({'response': 'why are you here'}), 404
if __name__ == '__main__':
    try:
        app.run(debug=True,host='0.0.0.0', port=8001)
    except:
        pass
    finally:
        mongodb_connection.close()