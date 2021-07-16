from flask import json, url_for, redirect, Flask, jsonify, request, abort
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from werkzeug.security import safe_str_cmp
from flask_jwt import JWT, jwt_required, current_identity
import datetime
from flask_restx import Resource, Api, fields
# region configs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asranmitionsintios123s'
# envio instancia app a pymongo

app.config['MONGO_URI'] = 'mongodb://localhost/pythonreactTest' # pythonreactTest va a ser la db
mongo = PyMongo(app)
CORS(app) # para interactuar con el sever de react
# creamos react app con el comando npx create-react-app frontend
# vamos a instalar dos aplicaciones npm i react-router-dom bootswatch
db = mongo.db

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id



users = [User(str(ObjectId(u["_id"])), u["name"], u["password"]) for u in db.users.find()]
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

jwt = JWT(app, authenticate, identity)

# endregion

# region routes

# #Authorizations
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

# Create swagger version 2.0
api = Api(
    app, 
    version='1.0',
    title='API get robotStatus', 
    description='This API obtains the robot status',
    doc='/swagger',
    default='Methods',
    default_label='',
    authorizations=authorizations)

body_auth_post = api.model('BodyAuthPost', {
    "username": fields.String('string'),
    "password": fields.String('string')
})



@api.route('/')
class inicio(Resource):
    @api.doc(responses={
        200: '(OK) The request was generated successfully',
        401: '(Unauthorized) Token is invalid or missing',
        404: '(NotFound) The requested exchange  rate has no content',
    },security='apikey')
    def get(self):
        return jsonify("Welcome to robotStatus")

@app.route("/protected", methods=["GET"])
# @jwt_required()
def protected():
    """
    Test conecction.
    :returns: Return a string message
    """
    return "method protected"
    


@app.route("/ping", methods=["GET"])
def ping():
    """
    Test conecction.
    :returns: Return a string message
    """
    api.doc(responses={
        200: '(OK) The request was generated successfully',
        401: '(Unauthorized) Token is invalid or missing',
        404: '(NotFound) The requested exchange  rate has no content',
    },security='apikey')
    return "pong"

@app.route("/process", methods=["POST"])
# @jwt_required()
def set_process():
    """
    set the items in mongo db called process.
    :returns: Return a json with Object id
    """
    now = datetime.datetime.now()
    actual_date = now.strftime("%Y-%m-%d")
    id = db.process.insert(
        {
        "name" : request.json["name"],
        "status" : request.json["status"],
        "time_execution" : actual_date
        }
    )
    return jsonify({"ID": str(ObjectId(id))})

@app.route("/process/<id>", methods=["GET"])
# @jwt_required()
def get_one_process(id):
    """
    send one process.
    :returns: Return a json with the field of de document in collection process
    """
    try:
        process = db.process.find_one({"_id": ObjectId(id)})

        dict_process = {
            "name" : process["name"],
            "status" : process["status"],
            "time_execution": process["time_execution"]
        }
        return jsonify(dict_process)
    except:
        abort(404, description="Process not found")

@app.route("/processes", methods=["GET"])
# @jwt_required()
def get_all_processes():
    """
    get all process.
    :returns: Return a json with the field of de document in collection process
    """
    processes = db.process.find()
    list_process = []
    for doc in processes:
        list_process.append(
            {   
                "id" : str(ObjectId(doc["_id"])),
                "name" : doc["name"],
                "status" : doc["status"],
                "time_execution": doc["time_execution"]
            }
        )
    return jsonify(list_process)



@app.route("/process/<id>", methods=["PUT"])
# @jwt_required()
def update_process(id):
    """
    Update the users.
    :returns: Return a json with the field of de document in collection process
    """
    try:
        now = datetime.datetime.now()
        actual_date = now.strftime("%Y-%m-%d")
        proc = db.process.update_one({"_id":ObjectId(id)},{"$set": {"name": request.json["name"],
        "status": request.json["status"],"time_execution": actual_date
        }})

        proc = db.process.find_one({"_id":ObjectId(id)})
        dic_user = {
            "id": str(ObjectId(proc["_id"])),
            "name": proc["name"],
            "status": proc["status"],
            "time_execution": actual_date
        }
        return jsonify({"User Updated" : dic_user})
    except:
        abort(404, description="Process not found")

@app.route("/process/<id>", methods=["DELETE"])
# @jwt_required()
def delete_process(id):
    """
    Delete process.
    :returns: Return a json with the field of de document in collection process
    """
    try:
        proc = db.process.find_one({"_id":ObjectId(id)})
        dic_user = {
            "id": str(ObjectId(proc["_id"])),
            "name": proc["name"],
            "status": proc["status"],
            "time_execution": proc["time_execution"]
        }
        db.process.delete_one({"_id":ObjectId(id)})
        return jsonify({"User deleted" : dic_user})
    except:
        abort(404, description="Process not found")
# endregion


@app.errorhandler(404)
def process_not_found(e):
    """
    Error handler.
    :returns: Return a json message with error
    """
    return jsonify(error=str(e)), 404





if __name__ == "__main__":
    app.run(debug=True,port=5000)