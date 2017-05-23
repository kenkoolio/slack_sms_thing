from flask import Flask, render_template, request, redirect, jsonify, abort
from twilio.rest import Client
from auth import sid, twilio_token, slack_token
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
#   command=/smsout
#   text="1234567890 message goes here"
#   response_url=https://hooks.slack.com/commands/1234/5678

#index
@app.route('/')
def index():

    return render_template('index.html')

#relay sms from slack to phone
@app.route('/smsout', methods=['POST'])
def relay_sms():
    #verify request is from slack
    slack_verify_token = request.form.get("token")
    if not slack_verify_token == slack_token:
        abort(400)

    #incoming slack data
    incoming_message = request.form.get("text")
    out_number = incoming_message[:10]
    out_message = incoming_message[11:]
    response_url = request.form.get("response_url")
    print("lookie here", response_url)

    #twilio API to send slack message to mobile phone
    twilio_number = "+14698047301"
    to = "+1"+out_number
    from_ = twilio_number
    body = out_message
    #todo callback URL

    client = Client(sid, twilio_token)

    client.messages.create(
        to=to,
        from_=from_,
        body=body)

    resp = {"text": "have a reply"}
    return jsonify(resp), 200, {"Content-Type": "application/json"}

#when mobile phone sends a reply, use incoming_webhooks to send reply to slack channel
@app.route('/smsreply', methods=['POST'])
def reply_to_slack():
    pass


if __name__ == "__main__":
    app.run(debug=True)
