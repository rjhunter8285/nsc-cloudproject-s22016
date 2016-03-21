#file serves as a bridge between the api and backend services
#the backend services include oatuh, documentdb, and Azure storage
#this file includes methods that handle backend services method calls for
#POSR, PUT, GET, and DELETE
from storage_methods import uploadBlob, deleteBlob
from documentdb_methods import createRecord, getRecords, deleteRecord, updateRecord
from verify_oauth import verifyOauth
from static.app_json import *

#method calls backend services methods for uploading an image
#parameters are given by the api/init flask file
def uploadImageJSON(username, blob, filename, token, secret, tags):
    #checks given oauth credentials
    oauth_verify_code = verifyOauth(token, secret)
    #checks if methods gave an error
    # if there is an error, returns an oauth error json
    if oauth_verify_code != 200:
        return oauth_error_json

    #calls method to upload blob to storage        
    rtnBlobList = uploadBlob(username, blob, filename)
    #checks if an array with a timestamp and blob url were returned
    if len(rtnBlobList) < 2:
        #reurns error json is the array doesn't contain the blob url or timestamp
        return upload_image_blob_error_json

    #calls method to create a meta data document in documentdb
    rtnDocumentdbMsg = createRecord(username, filename, tags, rtnBlobList[0], rtnBlobList[1])  
    #checks if there was an error
    if rtnDocumentdbMsg  == 'error':
        #returns error json
        return upload_image_db_error_json

    #return success json       
    return upload_image_success_json


#method calls backend services methods for deleting an image
#parameters are given by the api/init flask file
def deleteImageJSON(blobURL, token, secret):
    #checks given oauth credentials
    oauth_verify_code = verifyOauth(token, secret)
    #checks if methods gave an error
    # if there is an error, returns an oauth error json
    if oauth_verify_code != 200:
        return oauth_error_json

    #calls method to delete blob for Azure storage
    rtnBlobList = deleteBlob(blobURL)
    if rtnBlobList == 'error':
        #returns error json if there was an error
        #deleting the image
        return delete_image_blob_error_json

    #calls method to delete metadata from documentdb
    rtnDbMsg = deleteRecord(blobURL)
    if rtnDbMsg == 'error':
        #returns error json if there was an error
        #deleting the metadata
        return delete_image_db_error_json

    #return success json 
    return delete_image_success_json


#method calls backend services methods for getting image metadata
#parameters are given by the api/init flask file
def getImagesJSON(timestamp, prev, tags, username, token, secret):
    #checks given oauth credentials
    oauth_verify_code = verifyOauth(token, secret)
    #checks if methods gave an error
    # if there is an error, returns an oauth error json
    if oauth_verify_code != 200:
        return oauth_error_json

    #calls method to get json array from documentdb based
    #on query parameters
    rec_json = getRecords(username, timestamp, prev, tags)
    if rec_json == 'error':
        #returns error json if there was an error
        #gettin the metadata
        return get_image_error_json

    #formats sucess json
    rtn_json = {'status': 'success', 'imgs': rec_json}         
    #return success json 
    return rtn_json


#method calls backend services methods for updating tags in the metadata
#parameters are given by the api/init flask file
def updateTagsJSON(blobURL, tags, token, secret):
    #checks given oauth credentials
    oauth_verify_code = verifyOauth(token, secret)
    #checks if methods gave an error
    # if there is an error, returns an oauth error json
    if oauth_verify_code != 200:
        return oauth_error_json

    #calls method to update tags in a given record in documentdb
    rtnDbMsg = updateRecord(blobURL,tags)
    if rtnDbMsg == 'error':
        #returns error json if there was an error
        #updating the metadata
        return update_tags_error_json

    #return success json 
    return update_tags_success_json

