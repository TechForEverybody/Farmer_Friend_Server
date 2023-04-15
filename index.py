from App import *
from APIs.sensor import *
from APIs.user_authentication import *
from APIs.stats import *
from APIs.user_data import *
from APIs.pump import *
from Admin.sensor_module import *
from Products.products_data import *
# from ML_and_DL_Requests_APIS.detection_and_suggestion import *
# from ML_and_DL_Requests_APIS.feedback import *




@app.errorhandler(404)
def not_found(error):
    return jsonify({'response': 'why are you here'}), 404



if __name__ == '__main__':
    # try:
        app.run(debug=True,host='0.0.0.0', port=80)
        mongodb_connection.close()
    # except:
    #     pass
    # finally:
    #     mongodb_connection.close()