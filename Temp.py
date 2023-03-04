import pymongo
import pprint
from bson.objectid import ObjectId
connection_url="mongodb+srv://server:0987654321qwertyuiop@farmer-friend-sever.t17fn.mongodb.net/?retryWrites=true&w=majority"
mongodb_connection=pymongo.MongoClient(connection_url)
print(mongodb_connection)
realtime_data=mongodb_connection['realtime-data']
sensors_list=realtime_data['sensors']
sensors_data=realtime_data['sensors_data']


print(sensors_data.find_one())
data = sensors_data.find({"sensor_id":"6402bc824c6eac8bda2e1c38"},{"_id":0,"sensor_id":0}).sort("_id",-1)
print(list(data))

mongodb_connection.close()