# from https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

import os 
import time 

from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
READ_WEBSOCKET_DELAY = 1

# instantiate Slack and Twilio clients 
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client.api_call(
    "chat.postMessage",
    channel = "#test",
    text = "Hello world",
    as_user = True )

def hasNumbers(string):
    # from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    return any(char.isdigit() for char in string)

def handle_command(command, channel):
    # recieves commands and determines if they are valid, then acts on them. 
    # if not valid, asks for clarification and returns back what it needs
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
        "* command with numbers, delimited by spaces."
    
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel,
                                      text=response, as_user=True)

def check_illuminati(command, channel):
    print command
    slack_client.api_call("chat.postMessage", channel=channel, 
                                    text = 'ILLUMINATI', as_user = True)

def parse_slack_output(slack_rtm_output):
    # The Slack Real Time Messaging API is an events firehouse 
    output_list = slack_rtm_output
    if len(output_list) > 0:
        for output in output_list:
            if 'text' in output and AT_BOT in output["text"]:
                print output['text'].split(AT_BOT)[1].strip().lower()
                return output["text"].split(AT_BOT)[1].strip().lower(), \
                    output["channel"]

    return None, None 

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("yoshi_bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                print command.encode('ascii','ignonre')
                if hasNumbers(command.encode('ascii')):
                    check_illuminati(command, channel)
                else:
                    handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
            command = ''
    else:
        print("Connection failed. Invalid Slack token or bot ID?")