import pymongo

# with open("../../Utils/Database/Database_Config.env") as file:
#     connection_url=file.read()
connection_url="mongodb+srv://server:0987654321qwertyuiop@farmer-friend-sever.t17fn.mongodb.net/?retryWrites=true&w=majority"
mongodb_connection=pymongo.MongoClient(connection_url)
print(mongodb_connection)