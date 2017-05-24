Slack sms app 

Description
  - An app that opens a bi-directional channel of communication between Slack and mobile phones through the use of Slack's API and Twilio's API.
  
Limitations
  - Currently hooked up to a specific Slack Team.
  - Due to the nature of Twilio API's free trial, to test the APP I must add your mobile number to a list of approved phone numbers.
  
How to use
  - Join my Slack team kenkooliokorp.slack.com via invitation
  - Email me with a mobile phone number you wish to add to the approved phone numbers list, it will send you a confirmation code that I will ask for to complete registration.
  
  - In the #general channel of the slack team:
    - Send messages to mobile phone using the slash command "/smsout" followed by 10-digit phone number (excluding parentheses and dashes) followed by your message (spaces in between of course).
    - The mobile phone user can simply send a reply and it will appear on the Slack #general channel
    - Structure: "/smsout [phone number] [message]"
    - Example: "/smsout 5555555555 cheerio!" 
    
  - Type "/smsout help" for tips
