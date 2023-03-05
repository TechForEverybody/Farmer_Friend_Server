from App import *

@app.route("/authenticate_user",methods=["POST","GET"])
def authenticateUser():
    if isPostMethod():
        request_measure=stats.find({"ip_address":request.remote_addr},{"_id":0,"ip_address":0})
        request_measure=[i for i in request_measure]
        if len(request_measure)==0:
            stats.insert_one({"ip_address":request.remote_addr,"visit_count":1})
            stats.update_one({"_id":bson.objectid.ObjectId("64042f655a893bec111c047a")},{"$inc":{"requests_day":1}})
            stats.update_one({"_id":bson.objectid.ObjectId("64042f655a893bec111c047a")},{"$inc":{"visits_day":1}})
        else:
            stats.update_one({"ip_address":request.remote_addr},{"$inc":{"visit_count":1}})
            stats.update_one({"_id":bson.objectid.ObjectId("64042f655a893bec111c047a")},{"$inc":{"visits_day":1}})
        if isLoggedIn():
            return jsonify({
                "response":{
                    "name":session['name'],
                    "id":session['id'],
                    "detection_chances":session['detection_chances']
                }
            })
        else: return jsonify({
            "response":"Authentication Required"
        }),401
    else:
        return jsonify({"response":"Request not allowed"}),403

@app.route("/login",methods=["POST","GET"])
def login():
    if isPostMethod():
        email=request.json['email']
        password=request.json['password']
        user=users.find_one({"email":email,"password":getHashValue(password)},{"password":0})
        if user:
            session['name']=user['name']
            session['id']=str(user['_id'])
            session['is_login']=True
            session['detection_chances']=5
            return jsonify({"response":{
                "name":session['name'],
                "id":session['id'],
                "detection_chances":session['detection_chances']
            }})
        return jsonify({"response":"Invalid Credentials"}),404
    else:
        return jsonify({"response":"Request not allowed"}),403

@app.route("/register",methods=["POST","GET"])
def register():
    if isPostMethod():
        name=request.json['name']
        number=request.json['phone']
        email=request.json['email']
        password=request.json['password']
        user=users.find_one({"$or":[{"email":email},{"number":number}]},{"password":0})
        if user:
            return jsonify({"response":"User Already Exists"}),400
        password=getHashValue(password)
        new_user={
            "name":name,
            "number":number,
            "email":email,
            "password":password,
            "sensors_count":0,
            "created_at":datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "last_login_ip":request.remote_addr
        }
        user=users.insert_one(new_user)
        session['name']=new_user['name']
        session['id']=str(user.inserted_id)
        session['is_login']=True
        session['detection_chances']=5
        stats.update_one({"_id":bson.objectid.ObjectId("64042f655a893bec111c047a")},{"$inc":{"users_count":1}})
        return jsonify({"response":{
            "name":session['name'],
            "id":session['id'],
            "detection_chances":session['detection_chances']
        }})
    else:
        return jsonify({"response":"Request not allowed"}),403

@app.route("/logout",methods=["POST","GET"])
def logout():
    if isPostMethod():
        if isLoggedIn():
            session.pop("is_login")
            session.clear()
            return jsonify({
                "response":"Done, successfully logged out"
            })
    return jsonify({"response":"Request not allowed"}),403