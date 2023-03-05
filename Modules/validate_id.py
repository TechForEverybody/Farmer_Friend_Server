import bson.objectid
def validate_id(id):
    try:
        bson.objectid.ObjectId(id)
        return True
    except:
        return False
    
def validate_ids(*ids):
    for id in ids:
        if not validate_id(id):
            return False
    return True