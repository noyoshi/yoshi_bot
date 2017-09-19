#!/usr/bin/env python2.7

__author__ = 'Noah Yoshida'

'''
This is a silly Slack bot that I am making to practice using APIs and 
JSON. 

Help came from:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
'''

import os 
import time 
from slackclient import SlackClient
import random 
import itertools

BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">" # the command tag 
EXAMPLE_COMMAND = "random" # an example command 
READ_WEBSOCKET_DELAY = 0.5 # pauses it for a second 

# instantiate Slack and Twilio clients 
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client.api_call(
    "chat.postMessage",
    channel = "#test",
    text = "Hello world",
    as_user = True )
# ================================= Functions ================================

def hasNumbers(string):
    # from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    return any(char.isdigit() for char in string)


def parse_slack_output(slack_rtm_output):
    # The Slack Real Time Messaging API is an events firehouse 
    output_list = slack_rtm_output
    print output_list
    if len(output_list) > 0:
        for output in output_list:
            if 'text' in output: # outputs everything in 'text' json section
            # this logic makes the bot ignore its own output as input 
                if 'user' in output: 
                    if output['user'] == BOT_ID:
                        pass 
                    else:
                        print output['text']
                        return output['text'], output['channel']
                else:
                    print output['text']
                    return output['text'], output['channel']

    return None, None 

# ============================= Commands and Stuff ============================

def handle_command(command, channel): # handles commands properly! 
    # recieves commands and determines if they are valid, then acts on them. 
    # if not valid, asks for clarification and returns back what it needs
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
        "* command with numbers, delimited by spaces."
    
    if command.startswith(EXAMPLE_COMMAND):
        response = str(random.randint(0,10))
    slack_client.api_call("chat.postMessage", channel=channel,
                                      text=response, as_user=True)

def check_illuminati(string, channel): # string works! 
    # will be implemeting the algorithm I make for Programming Challenges
    nums = []
    concat = ''
    illum = False 
    for letter in string: 
        if letter.isdigit():
            concat += letter
            nums.append(int(letter))
    bad_letter = 666
    if concat == str(bad_letter):
        illum = True 
    else:
        result = 0 
        for num in nums: 
            if sum(nums) == bad_letter: 
                illum = True 
    print nums
    if illum:
        slack_client.api_call("chat.postMessage", channel=channel, 
                                    text = '666 ILLUMINATI CONFIRMED', as_user = True)

# ================================= Main ===============================
if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("yoshi_bot connected and running!")
        while True:
            text, channel = parse_slack_output(slack_client.rtm_read())
            if text and channel: 
                print text
                com = text 
                string = text.encode('utf-8')
                # turns the text from unicode to a Python string 
                if hasNumbers(string) and AT_BOT not in text: # if nums in text
                    check_illuminati(string, channel)
                elif AT_BOT in text: # if the bot call is in the text 
                    # strips the bot call off of the text 
                    command = text.split(AT_BOT)[1].strip().lower() 
                    # handles the text of the text 
                    handle_command(command, channel)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")