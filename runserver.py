"""
This script runs the FlaskWebProject application using a development server.
"""

from os import environ
from FlaskWebProject import app
from flask import request, redirect
import twilio.twiml
import requests

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
 
@app.route("/twilio", methods=['GET', 'POST'])
def inTextOutStock():
    """Parse incoming texts and send JSON sell/buy order."""
    incomingBody = request.values.get('Body', None)
    parsedBody = inomingMessage.split(" ")
    if (parsedBody[0] == "B" || parsedBody[0] == "S") {
    	params = {
    		'order': parsedBody[0],
    		'sym' : parsedBody[1],
    		'val' : parsedBody[2]
    		}
		r = requests.post("http://crowdinvestor.azurewebsites.net/order", 
			data = params)
        return;
    } else {
    	#not valid buy/sell order
    	return;
    }
    return;
