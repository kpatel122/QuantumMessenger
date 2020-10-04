from __future__ import print_function
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import slixmpp
from XMPP_Interface import *

from flask import Flask, request, request

import socket

app = Flask(__name__)

xmppaddress_dev = "http://fcm-xmpp.googleapis.com:5236"
xmppaddress_pro = "http://fcm-xmpp.googleapis.com:5235"

xmppaddress = xmppaddress_dev

linkbase= "http://127.0.0.1:5000/"

configparams = {} #holds all config and sensitive values, app keys, api keys etc...
CONFIGFILE = "config.txt" #make sure this file is in git ignore
CONFIGSEPERATOR = ":"


def get_config_params(filename, outparams):
    
    with open(filename) as paramsfile:
        for line in paramsfile:
            name, val = line.partition(CONFIGSEPERATOR)[::2] #::2 is every 2nd element
            outparams[name] = str(val.strip('\n'))



def make_link(destination, linebreak = True):
    breakhtml = "<br>"
    if linebreak == False:
        breakhtml = ""

    return "<a href=\'" +linkbase+destination + "\'>" + destination + "</a>" + breakhtml

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    outhtml = make_link('fcmxmpp') + make_link('sendadminsdk') + make_link('messagereceipt') \
        +make_link('test')
    
    return 'Default path <br>' + outhtml

# This is just one of your other valid routes:
@app.route('/fcmxmpp')
def fcmxmpp():
    #TODO: will throw a thread error currently

    print("sending fcm xmpp")

    xp = XMPP_Client(FCM_JID,FCM_SENDER_ID,configparams) 
   
    return 'sending to google XMPP <br> res is ' + make_link('home')

@app.route("/sendadminsdk")
def sendadminsdk():
    print("Sending admin sdk...")
  
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.    
    registration_token = configparams['registration_token']

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_token]

    return ""+response + "<br>" + make_link('home')

 
@app.route('/messagereceipt', methods=['POST'])
def messagereceipt():
    id = request.form['id']
    value = request.form['value']
    
    html = "id=" + id + " value=" + value + " "

    return html


if __name__ == "__main__":
    
    get_config_params(CONFIGFILE,configparams)
    
    cred = credentials.Certificate(configparams['adminsdkcredentialsfile'])
    firebase_admin.initialize_app(cred)

    app.run(host='0.0.0.0', debug=True)
