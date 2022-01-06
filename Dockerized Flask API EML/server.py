from flask import Flask, jsonify,request, request
#from flask_cors import CORS,cross_origin
import json
import os
import base64
from database import getDatabaseInstance,insertEmailBody, findEmail, getEmailPhisingStatus, getAllEmails

DB_NAME = 'emaildb'
USER_NAME = "umerfarooq" #os.getenv('USER_NAME')
PASSWORD = "umerfarooq" #os.getenv('PASSWORD')
URL = "mongodb+srv://{}:{}@cluster0.rru4r.mongodb.net/{}?retryWrites=true&w=majority".format(USER_NAME,PASSWORD,DB_NAME)



app = Flask(__name__)

@app.route("/", methods=['GET'])
def welcome():
    return jsonify({'response': "Welcome To EML Flask API"})


@app.route("/checkServerStatus", methods=['GET'])
def pingServer():
    return jsonify({'response': "running"})

@app.route("/printAllEmails", methods=['GET'])
def printAllEmails():
    
    database = getDatabaseInstance(URL)
    response = getAllEmails(database)
       
    return jsonify(response)


@app.route("/sendEMLData", methods=['POST'])
def analyzingEmailHeader():

   if request.method == 'POST':
       request_data = request.data
       request_data = json.loads(request_data.decode('utf-8'))
       
       _id = request_data['id']
       
       data = request_data['data'] 
       data = base64.b64decode(data)
       data = str(data, "utf-8")
       
       payload = request_data['extra']
       

        
       database = getDatabaseInstance(URL)
       status = insertEmailBody(database,payload)
       
       if status is False:
           print("Analyzed Already.")
           response = jsonify({'response':"exist"})
       else:
           fileName = "{}_{}.eml".format(_id,payload[4]["From"]["emailAddress"])
           emlFile = open(fileName,"w+")
           emlFile.write(data)
           emlFile.close()
           response = jsonify({'response':"success"})
      
   else:
       response = jsonify({'response':"failed"})

   print(response)
   return response


@app.route("/checkIfEmailAnalyzed", methods=['POST'])
def checkIfEmailAnalyzedAlready():

   if request.method == 'POST':
       request_data = request.data
       request_data = json.loads(request_data.decode('utf-8'))
       
       Body = request_data['Body']
    
   
       database = getDatabaseInstance(URL)
       status = findEmail(database,Body)
       print(status)
       if status[0] is True:

           analyzer = status[1][0].split('@')
           analyzerFullname = analyzer[0].split('.')
           analyzerFullname = " ".join(analyzerFullname).capitalize()
           response = jsonify({'response':analyzerFullname})
       else:
           response = jsonify({'response':"new"})
      
   else:
       response = jsonify({'response':"failed"})

   print(response)
   return response


@app.route("/getEmailPhishingReport", methods=['POST'])
def fetchEmailReport():

   if request.method == 'POST':
       request_data = request.data
       request_data = json.loads(request_data.decode('utf-8'))
       
       Body = request_data['Body']
    
       
       database = getDatabaseInstance(URL)
       status = findEmail(database,Body)
       
       if status[0] is True:
           response =  jsonify(getEmailPhisingStatus(database,Body))
       else:
           response = jsonify({
               "DKIM" : "No Analysis.", 
               "SPF" : "No Analysis.",
               "DMARC" : "No Analysis."
           })
      
   else:
       response = jsonify({'response':"failed"})

   return response

if __name__ == "__main__":
    ssl_context='adhoc'
    app.run(host = '0.0.0.0', port = 5000)



    
     