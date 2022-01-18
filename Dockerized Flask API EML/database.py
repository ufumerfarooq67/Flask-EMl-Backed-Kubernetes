from pymongo import MongoClient
from bson import json_util
import uuid
from datetime import datetime
from bson.json_util import dumps
import json
import random


###############################################################################
###############################################################################

DB_NAME = 'emaildb'
EML_COLLECTION = "payload"
USER_COLLECTION = "user"
URL = "mongodb+srv://umerfarooq:{}@cluster0.rru4r.mongodb.net/{}?retryWrites=true&w=majority".format("umerfarooq",DB_NAME)

def getDatabaseInstance():
    #print("GETTING DATABSE INSTANCE")

    client = MongoClient(URL)
    database = client[DB_NAME]

    return database
      

###################################################################
###################################################################
###################################################################



def insertEmailBody(database,payload):

    email_collection = database[EML_COLLECTION]
    
    email_template = {
        "_id": payload["InternetMessageID"],
        "Analyzer": payload["Analyzer"],
        "Conversation ID": payload["ConversationID"],
        "Date Time Created": payload["DateTimeCreated"],
        "Date Time Modified": payload["DateTimeModified"],
        "Display Name:": payload["From"]["displayName"],
        "Sender Email Address": payload["From"]["emailAddress"],
        "Subject" : payload["Subject"],
        "Receiver Emaiil Address" : payload["To"],
        "Total Email Count" : payload["Count"],
        "Body":payload["Body"],
        "Extra Information":payload["ExtraInformation"]
        }
    
    email = email_collection.find_one({"Subject":payload["Subject"]})#email_collection.find_one({"Body":payload["Body"]})
    
    if email is None:
        email_collection.insert_one(email_template)
        return True
    
    return False
   

     
def findEmail(database, Subject):

  email_collection = database[EML_COLLECTION]
  
  email = email_collection.find_one({"Subject":Subject})
  if email is None:
      return False, None
  return True, email['Analyzer']

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
