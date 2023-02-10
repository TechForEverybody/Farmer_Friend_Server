from flask import Flask,jsonify,request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'your_ip_address': request.remote_addr}), 200
@app.errorhandler(404)
def not_found(error):
    return jsonify({'response': 'why are you here'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)