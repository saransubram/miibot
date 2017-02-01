#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "customer.balance":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    product = parameters.get("product")
    
    balance = {'Lloyds':41, 'Santander':49, 'Barclays':37, 'Lloyds and Barclays':33, 'Barclays and Santander':27, 'Lloyds and Santander':32, 'Lloyds Barclays and Santander':59}

    speech = "The balance in " + product + " is " + str(balance[product])

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-cfds"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
