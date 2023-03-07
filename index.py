from App import *
from APIs.sensor import *
from APIs.user_authentication import *
from APIs.stats import *
from Admin.sensor_module import *








@app.errorhandler(404)
def not_found(error):
    return jsonify({'response': 'why are you here'}), 404



@app.route("/.well-known/pki-validation/8A9C09B54AC668091E8575B440EB2ECB.txt")
def letsencrypt():
    return send_from_directory(directory="./Data",path="8A9C09B54AC668091E8575B440EB2ECB.txt")




if __name__ == '__main__':
    # try:
        app.run(debug=True,host='0.0.0.0', port=80)
        mongodb_connection.close()
    # except:
    #     pass
    # finally:
    #     mongodb_connection.close()