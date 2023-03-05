from App import *

@app.route("/get_stats",methods=["POST","GET"])
def getStats():
    if isPostMethod():
        stats_data=stats.find_one({"_id":bson.objectid.ObjectId("64042f655a893bec111c047a")},{"_id":0})
        return jsonify({"response":stats_data})
    else:
        return jsonify({"response":"Request not allowed"}),403