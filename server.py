from flask import Flask, render_template, request, redirect, jsonify, abort
from twilio.rest import Client
from auth import sid, token
import requests

app = Flask(__name__)
app.secret_key = 'secretsquirrel'

#index
@app.route('/')
def index():

    return render_template('index.html')

#relay sms from slack to phone
@app.route('/smsout', methods=['POST'])
def relay_sms():
    twilio_number = "+14698047301"
    incoming_message = request.get_json(force=True)

    # to = "+1"+incoming_message["to"]
    # from_ = twilio_number
    # body = incoming_message["body"]
    # #todo callback URL
    #
    # client = Client(sid, token)
    #
    # client.messages.create(
    #     to=to,
    #     from_=from_,
    #     body=body)

    print("look here", incoming_message)
    # return render_template('index.html', message_data=incoming_message)
    resp = {"text": "have a reply"}
    return jsonify(resp), 200, {"Content-Type": "application/json"}
    #return {'text':'response number red'}

if __name__ == "__main__":
    app.run(debug=True)
