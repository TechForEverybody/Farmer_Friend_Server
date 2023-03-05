from flask import Flask,jsonify,request,session
from Database.schema import *
import hashlib
import datetime
import bson.json_util
import bson.objectid

app = Flask(__name__)
module_keys=["93a77eb3-856c-49fc-8a6d-44a7e822f25f"]
app.secret_key="SHIVKUMAR_CHAUHAN"


def isPostMethod():
    if request.method=="POST":return True
    else:return False

def isLoggedIn():
    if "is_login" in session:return True
    else:return False

def getHashValue(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()




@app.route('/')
def index():
    session['ip']=request.remote_addr
    return jsonify({'your_ip_address': request.remote_addr}), 200