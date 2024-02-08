import slack
from slackeventsapi import SlackEventAdapter
from flask import Flask, Response, request

SLACK_TOKEN = 'your token'
SIGNING_SECRET = 'your secret'

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET,"/slack/action", app)

client = slack.WebClient(token = SLACK_TOKEN)
BOT_ID = client.api_call("auth.test")['user_id']

@slack_event_adapter.on('message')
def message(payLoad):
    print(payLoad)
    event = payLoad.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        client.chat_postMessage(channel = channel_id, text = text)

joke_text = "I was going to tell you a joke about boxing but I forgot the punch line!"

@app.route('/joke', methods = ['POST'])
def joke():
    data = request.form
    print(data)
    channel_id = data.get('channel_id')

    return client.chat_postMessage(channel = channel_id, text = joke_text)

if __name__  == "__main__":
    app.run(debug = "True")