from flask import Flask, render_template, request, redirect, jsonify, abort
from twilio.rest import Client
from auth import sid, token
import requests

app = Flask(__name__)
app.secret_key = 'secretsquirrel'

# The parameters included in a slash command request (with example values):
#   token=gIkuvaNzQIHg97ATvDxqgjtO
#   team_id=T0001
#   team_domain=example
#   channel_id=C2147483705
#   channel_name=test
#   user_id=U2147483697
#   user_name=Steve
#   command=/weather
#   text=94070
#   response_url=https://hooks.slack.com/commands/1234/5678

#index
@app.route('/')
def index():

    return render_template('index.html')

#relay sms from slack to phone
@app.route('/smsout', methods=['POST'])
def relay_sms():
    twilio_number = "+14698047301"
    #incoming_message = request.get_json(force=True)


    incoming_message = request.form.get("text")

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
    reply = "Here, have a reply"
    return jsonify(resp), 200, {"Content-Type": "application/json"}
    #return reply

if __name__ == "__main__":
    app.run(debug=True)
