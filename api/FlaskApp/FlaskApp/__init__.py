#AD 440
#Cloud Practicum
# 
#File contains methods for all api routing calls.
#This includes methods for GET,PUT,POST,DELETE
# 
# 
from flask import Flask
from flask import make_response
from flask import request
from flask import jsonify
from azure_components import static
from azure_components.api_methods import *
from flask.ext.cors import CORS

#declare flask app
app = Flask(__name__)
#calls CORS method and gives the app Cross-Origin Resource Sharing
#for all domains
CORS(app)


#route for get images call, GET METHOD
@app.route("/getImages", methods=['GET'])
def getImages():
    #header variables for get api method
    username = request.headers.get('username')
    token = request.headers.get('token')
    secret = request.headers.get('secret')
    #checks if the mandatory headers are null
    if not all((username, token, secret)):
        #returns json error for null header parameters
        rtn_error = jsonify(request=static.app_json.api_parameters_error_json)
        return  rtn_error
    #gets then checks if timestamp is null
    #timestamp is an optional header 
    timestamp = request.headers.get('timestamp')
    if timestamp is None:
        #assigns 0 for null timestamp
        #the timestamp doesn't need to be used for the first page of
        #results
        timestamp = 0
    tags = request.headers.get('tags')
    #checks is tags were given
    if tags is None:
        #assigns empty array
        tags_new = []
    else:
        #splits tags by comma delimeter into an array
        tags_new = tags.split(',')

    prev = request.headers.get('prev')
    #checks if prev variable is set
    if prev is None:
        # updates variable to false
        prev = 'false'
    #calls get image method to get JSON from api method (get)
    rtn_json = getImagesJSON(timestamp, prev, tags_new, username, token, secret)

    #converts to json and returns json request
    rtn_body = jsonify(request=rtn_json)
    return rtn_body

#route for uploading images, POST METHOD
@app.route("/uploadImage", methods=['POST'])
def uploadImage():
    #header variables for post api method
    username = request.headers.get('username')
    blob = request.data
    filename = request.headers.get('filename')
    token = request.headers.get('token')
    secret = request.headers.get('secret')
    #checks if the mandatory headers are null
    if not all((username, blob, filename, token, secret)):
        #returns json error for null header parameters
        rtn_error = jsonify(request=static.app_json.api_parameters_error_json)
        return  rtn_error
    
    tags = request.headers.get('tags')
    #checks is tags were given
    if tags is None:
        #assigns empty array
        tags_new = []
    else:
        #splits tags by comma delimeter into an array
        tags_new = tags.split(',')

    #calls upload image method (post)
    rtn_json = uploadImageJSON(username, blob, filename, token, secret, tags_new)

    #converts to json and returns json request
    rtn_body = jsonify(request=rtn_json)
    return rtn_body

#route for deleting images, DELETE METHOD
@app.route("/deleteImage", methods=['DELETE'])
def deleteImage():
    #header variables for delete api method
    blobURL = request.headers.get('blobURL')
    token = request.headers.get('token')
    secret = request.headers.get('secret')
    #checks if the mandatory headers are null
    if not all((blobURL, token, secret)):
        #returns json error for null header parameters
        rtn_error = jsonify(request=static.app_json.api_parameters_error_json)
        return  rtn_error
    
    #calls delete image method (delete)
    rtn_json = deleteImageJSON(blobURL, token, secret)

    #converts to json and returns json request
    rtn_body = jsonify(request=rtn_json)
    return rtn_body

#route for updating tags, PUT METHOD
@app.route("/updateTags", methods=['PUT'])
def updateTags():
    #header variables for put api method
    blobURL = request.headers.get('blobURL')
    token = request.headers.get('token')
    secret = request.headers.get('secret')
    #checks if the mandatory headers are null
    if not all((blobURL, token, secret)):
        #returns json error for null header parameters
        rtn_error = jsonify(request=static.app_json.api_parameters_error_json)
        return  rtn_error
    
    tags = request.headers.get('tags')
    #checks is tags were given
    if tags is None:
        #assigns empty array
        tags_new = []
    else:
        #splits tags by comma delimeter into an array
        tags_new = tags.split(',')

    #calls update tags method (put)
    rtn_json = updateTagsJSON(blobURL, tags_new, token, secret)

    #converts to json and returns json request
    rtn_body = jsonify(request=rtn_json)
    return rtn_body

#initializes app and runs debug
if __name__ == "__main__":
    app.debug=True 
    app.run()



