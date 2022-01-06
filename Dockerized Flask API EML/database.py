from pymongo import MongoClient
from bson import json_util
import uuid
from datetime import datetime
from bson.json_util import dumps
import json
import random
import os



###############################################################################
###############################################################################

DB_NAME = 'emaildb'
EML_COLLECTION = "payload"

#URL = "mongodb+srv://umerfarooq:{}@cluster0.rru4r.mongodb.net/{}?retryWrites=true&w=majority".format("umerfarooq",DB_NAME)
def getDatabaseInstance(URL):
    #print("GETTING DATABSE INSTANCE")

    client = MongoClient(URL)
    database = client[DB_NAME]

    return database
      

###################################################################
###################################################################
###################################################################



def insertEmailBody(database,payload):

    email_collection = database[EML_COLLECTION]
    
    
    #print(json.dumps(payload, indent=4))
    

    _id = hash(payload[8]["Body"])

    email_template = {
        "_id": _id,
        "Conversation ID": payload[0]["Conversation ID"],
        "Internet Message ID": payload[1]["Internet Message ID"],
        "Date Time Created": payload[2]["Date Time Created"],
        "Date Time Modified": payload[3]["Date Time Modified"],
        "Display Name:": payload[4]["From"]["displayName"],
        "Sender Email Address": payload[4]["From"]["emailAddress"],
        "Subject" : payload[5]["Subject"],
        "Receiver Emaiil Address" : payload[6]["To"],
        "Total Email Count" : payload[7]["Count"],
        "Body":payload[8]["Body"],
        "Extra Information":payload[9]["Extra Information"]
        }
    
    #email = email_collection.find_one({"_id":hash(Body)})
    email = email_collection.find_one({"Body":payload[8]["Body"]})
    
    if email is None:
        email_collection.insert_one(email_template)
        return True
    
    return False
   

     
def findEmail(database, Body):

  email_collection = database[EML_COLLECTION]
  
  #email = email_collection.find_one({"_id":hash(Body)})
  email = email_collection.find_one({"Body":Body})
  if email is None:
      return False, None
  return True, email['Receiver Emaiil Address']

def getEmailPhisingStatus(database,Body):
    
    testNum = random.randint(0,100)
    
    authentication = {
        "DKIM" : "Failed with 100 vulnerabilities." if testNum > 50 and testNum%2 == 0 else "Authorized Domain.", 
        "SPF" : "Failed in stage B." if testNum%2 != 0 else "Authorized Domain.",
        "DMARC" : "Passed"  if testNum > 20 and testNum%2 == 0 else "Failed"
    }
    
    return authentication

# =============================================================================
def getAllEmails(database):
    email_collection = database[EML_COLLECTION]
#   
# 
    EmailList = []
    cursor = email_collection.find({})
    if cursor is None:
        return None
#   
# 
    for c in cursor:
        EmailList.append(c)
# 
# 
    return EmailList
# 
# 
# def deleteAll(database):
#   eml_collection = database[EML_COLLECTION]
#   eml_collection.delete_many({})
#   
# =============================================================================
  
#for email in getAllEmails():
#    print(email)
