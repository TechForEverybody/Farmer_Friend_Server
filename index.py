from flask import Flask,jsonify,request

app = Flask(__name__)
module_keys=["123456"]
current_data=[]
@app.route('/')
def index():
    return jsonify({'your_ip_address': request.remote_addr}), 200
@app.errorhandler(404)

@app.route('/save_sensor_data/<iot_module_key>/<float:temperature>/<float:humidity>')
def addition(iot_module_key,temperature,humidity):
    global current_data
    if iot_module_key in module_keys:
        current_data.append([temperature,humidity])
        return jsonify({"data":current_data})
    else:
        return jsonify({"result":"invalid module key"})

def not_found(error):
    return jsonify({'response': 'why are you here'}), 404
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8001)