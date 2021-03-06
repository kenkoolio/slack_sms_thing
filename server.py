from flask import Flask, render_template, request, abort
from twilio.rest import Client
from auth import sid, twilio_token, slack_token
import json
import requests

app = Flask(__name__)
app.secret_key = 'secretsquirrel'

# Slack: The parameters included in a slash command request (with example values):
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
    username = request.form.get("user_name")
    incoming_message = request.form.get("text")

    #if user is asking for help
    is_help = incoming_message[:4]
    if is_help.lower() == 'help':
        resp_text = 'Make sure the phone number is in the form xxxxxxxxxx (no parentheses or dashes) followed by a space before your message. Example: "/smsout 5556667777 cheerio!"'
        resp = {"text": resp_text}
        return json.dumps(resp), 200, {"Content-Type": "application/json"}

    #message formatting
    out_number = incoming_message[:10]
    message_text = incoming_message[11:]
    out_message = '{}: {}'.format(username, message_text)

    #twilio API to send slack message to mobile phone
    twilio_number = "+14698047301"
    to = "+1"+out_number
    from_ = twilio_number
    body = out_message

    #twilio methods
    client = Client(sid, twilio_token)

    client.messages.create(
        to=to,
        from_=from_,
        body=body)

    resp_text = '{} to {}: {}'.format(username, out_number, message_text)
    resp = {"text": resp_text}
    return json.dumps(resp), 200, {"Content-Type": "application/json"}


#Twilio request parameters
#   MessageSid = unique identifier for the message. May be used to later retrieve this message from the REST API.
#   SmsSid = Same value as MessageSid. Deprecated and included for backward compatibility.
#   AccountSid = The 34 character id of the Account this message is associated with.
#   MessagingServiceSid = The 34 character id of the Messaging Service associated to the message.
#   From = The phone number that sent this message.
#   To = The phone number of the recipient.
#   Body = The text body of the message. Up to 1600 characters long.
#   NumMedia = The number of media items associated with your message

#when mobile phone sends a reply, use incoming_webhooks to send reply to slack channel
@app.route('/smsreply', methods=['POST'])
def reply_to_slack():
    webhook_url = "https://hooks.slack.com/services/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"
    request_body = request.form.to_dict()
    from_phone = request_body["From"]
    message_body = request_body["Body"]
    #print("from twilio:", from_phone, message_body)

    return_message = 'Reply from {}: {}'.format(from_phone, message_body)
    return_body = {"text": return_message}
    return_headers = {"Content-Type": "application/json"}
    r = requests.post(url = webhook_url, data = json.dumps(return_body), headers = return_headers)
    print("slack webhook status:", r.status_code)
    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
