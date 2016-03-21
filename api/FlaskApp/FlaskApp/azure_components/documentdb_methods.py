#file contains all of the methods of our api that interact with documentdb
#the methods include creating, getting, deleting and updating the metadata documents
import pydocumentdb.document_client as document_client
import verify_oauth
import datetime
from datetime import timedelta
from static.app_keys import db_client, db_client_key, db_name, db_collection
import json	

#creates metadata record based on the parameters given to the api via http request
def createRecord(user, originalFilename, tags, time, url):
    #tries updloading metadata to documentdb
    try:
        #creates epoc based on the date 2/23/2016 (arbitrary date)
        epoc = datetime.datetime(2016, 2, 23, 3, 0, 00, 000000);
        #converts timestamp to value
        #this value is needed for searcing documentdb based on timestamp
        val = (time - epoc).total_seconds()*1000000;
        #connects to documentdb               
        client = document_client.DocumentClient(db_client, {'masterKey': db_client_key});
        #gets instance of database based on the client id
        db = next((data for data in client.ReadDatabases() if data['id'] == db_name));
        #gets instance of coll based on the coll id and db path
        coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == db_collection));

        #create document. Tags is an array, as passed.
        document = client.CreateDocument(coll['_self'],
                        {   "user_id": user,
                                "file_name": originalFilename,
                                "photo_url": url,
                                "photo_id": val,
                                "tags": tags
                        });
        
        return "success"

    #returns error if the metadata wasn't uploaded        
    except Exception:
        return "error"

#gets json array of records based on parameters
def getRecords(user, lastID, prev, tags):
    #tries get request to documentdb
    try:
        #creates direction and order variables for query
        dir = ">"
        order = "ASC"

        #checks if previous is true
        #changes direction and order variables
        if prev != 'false':
            dir = "<"
            order = "DESC"


        #connects to documentdb               
        client = document_client.DocumentClient(db_client, {'masterKey': db_client_key});
        #gets instance of database based on the client id
        db = next((data for data in client.ReadDatabases() if data['id'] == db_name));
        #gets instance of coll based on the coll id and db path
        coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == db_collection));

        #queries documentdb for the next 20 images based on parameters
        queryString = 'SELECT TOP 20 ' + db_collection + '.photo_id, ' + \
                        db_collection +'.file_name, ' + db_collection + '.photo_url, ' + db_collection + \
                        '.tags FROM '+ db_collection + ' WHERE '+ db_collection + '.user_id = "' \
                        + user + '" AND ' + db_collection + '.photo_id ' + dir + ' ' + str(lastID)

        #checks is tags were given
        if len(tags) > 0:
            #loops through tag array and adds query parameters to search for images that include
            #the given tags
            for tag in tags:
                queryString += ' AND ARRAY_CONTAINS(' + db_collection + '.tags ,"' + tag + '")'

        #concats the order to the query
        queryString += ' ORDER BY '+ db_collection +'.photo_id '+ order
        
        #queries the collection
        itterResult =  client.QueryDocuments(coll['_self'], queryString)
        #converts returned iterable to list
        rtn_list = list(itterResult)
        #returns json if empty
        if len(rtn_list) == 0:
           return rtn_list

        #checks if previous is set to true
        if prev != 'false':
            #creates a return array
            rtn_list_new = []
            #loops backwards through list
            #reverses json
            for i in range(len(rtn_list)-1, -1, -1):
                rtn_list_new.append(rtn_list[i])
            return rtn_list_new

        #returns json array
        return rtn_list

    #returns error if method throws an exception
    except Exception:
        return "error"


#deleteRecords receives the blobURL to locate the document
#calls documentdb method to delete metadata document
def deleteRecord(blobURL):
    #tries delete reques to documentdb
    try:
        #connects to documentdb               
        client = document_client.DocumentClient(db_client, {'masterKey': db_client_key});
        #gets instance of database based on the client id
        db = next((data for data in client.ReadDatabases() if data['id'] == db_name));
        #gets instance of coll based on the coll id and db path
        coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == db_collection));

        #Read documents and take first since blobURL should not be duplicated.
        doc = next((doc for doc in client.ReadDocuments(coll['_self']) if doc['photo_url'] == blobURL))
        #calls documentdb delete function
        client.DeleteDocument(doc['_self'])
        return 'success'

    #returns error if method throws an exception
    except Exception:
        return 'error'

#updateRecord receives the blobURL to locate the document
#and tags which are to be used to replace the current tags in the document
def updateRecord(blobURL, tags):

    try:
        #these function calls are used to locate the db client, database, collection, then the actual document
        #based off the URL provided
        #connects to documentdb               
        client = document_client.DocumentClient(db_client, {'masterKey': db_client_key});
        #gets instance of database based on the client id
        db = next((data for data in client.ReadDatabases() if data['id'] == db_name));
        #gets instance of coll based on the coll id and db path
        coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == db_collection));       

        #Read documents and take first since blobURL should not be duplicated.
        doc = next((doc for doc in client.ReadDocuments(coll['_self']) if doc['photo_url'] == blobURL))

        #changes the tags field to the new one provided by the user
        doc['tags'] = tags 
        #replaces the current document with the new document, with updated tags
        replaced_document = client.ReplaceDocument(doc['_self'], doc)
        return "success"

    #returns error if method throws an exception    
    except Exception:
        return "error"
