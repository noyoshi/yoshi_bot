#!/usr/bin/env python2.7

__author__ = 'Noah Yoshida'

'''
This is a silly Slack bot that I am making to practice using APIs and 
JSON. 

Use it to brighten up your slack channel. ^_^

Help came from:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
Features:
    Detects illuminati WIP
    Borks  WIP
    Gives random numbers 
Future Features?
'''


import time 
import random 
import itertools as it 
import sys
from BOT_ID import return_id
from SLACK_BOT_TOKEN import return_token
from slackclient import SlackClient

# bot ID taken from a seperate file so ya'll don't steal my bot 
BOT_ID = return_id()

AT_BOT = "<@" + BOT_ID + ">" # the command tag 
RANDOM_COMMAND = "rand" # an example command 

# opens the client  
slack_client = SlackClient(return_token())
# stored my token as an enviorenment variable. Can also call a file with it?
slack_client.api_call(
    "chat.postMessage",
    channel = "#test",
    text = "yoshi_bot online!",
    as_user = True )

# ================================= Functions ================================


def hasNumbers(string):
    '''
    from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    determines whether a string contains any numbers in it
    '''
    return any(char.isdigit() for char in string)


def parse_slack_output(slack_rtm_output):
    # parses the slack output - returns the text and channel of messages 
    output_list = slack_rtm_output
    print output_list
    if len(output_list) > 0: # if there is an event  
        for output in output_list:
            if 'text' in output: # if the JSON data has 'text' field in it 
            # this logic makes the bot ignore its own output as input 
                if 'user' in output: 
                    if output['user'] != BOT_ID:
                        print output['text']
                        return output['text'], output['channel']
                else: 
                # should never happen? since text indicates a user sent a msg 
                    print output['text']
                    return output['text'], output['channel']

    return None, None # if there was no 'text' field in the JSON data or no JSON data

# ============================= Commands and Stuff ============================

def illuminati_numbers(line):
    for perm in map(list,list(it.permutations(line))): 
        for ops in map(list,list(it.product((0,1,2),repeat=len(perm)-1))):
            temp = list(perm)
            while len(temp) > 1:
                i = ops.pop()
                if i == 0:
                    temp.append(temp.pop() + temp.pop())
                elif i == 1:
                    temp.append(temp.pop() - temp.pop())
                else:
                    temp.append(temp.pop() * temp.pop())
            if temp[0] == 13:
                return True
    return False 


def handle_command(command, channel): 
    '''
    recieves commands and determines if they are valid, then acts on them. 
    if not valid, asks for clarification and returns back what it needs
    '''
    response = "give me a better command pls"
    
    if command.startswith(RANDOM_COMMAND):
        response = str(random.randint(0,10))
    elif command.startswith('stop'):
        if random.random() > 0.5:
            response = 'I shall never stop!'
        else:
            response = 'Only if master commands'
    slack_client.api_call("chat.postMessage", channel=channel,
                                      text=response, as_user=True)

    
def bork(string,channel):
    '''
    this makes the bot bork. 
    bork bork!
    '''
    for char in string:
        if not char.isalpha():
            string = string.replace(char,' ')
    string = string.strip().lower().split()
    borks = 0 
    found = False 
    for word in string: 
        if word == 'bork':
            borks += 1
            found = True 

    if found: 
        txt = 'bork ' * borks * 2 
        txt = txt + '\n' + 'Whomst''deved'' let the dogs out?' 
        slack_client.api_call("chat.postMessage", channel=channel, 
                                    text = txt, as_user = True)
        

def check_illuminati(string, channel): 
    '''
    right now this only determines if there are three '6's in a message
    '''
    nums = []
    concat = ''
    illum = False 
    txt = '13! Illuminati detected'
    bad_letter = 666
    for char in string: 
        if char == '6':
            concat += char # this step checks to see if we can just concatonate 666 together
        elif not char.isdigit():
            string = string.replace(char,' ')
    for letter in string.split(): 
        nums.append(int(letter)) # appends the numbers to a number list 

    if str(bad_letter) in concat:
        txt = '6 + 6 + 6 = 666! ILLUMINATI CONFIRMED'
        illum = True 
    elif illuminati_numbers(nums):
        illum = True 
 
    print nums
    if illum: # illuminati confirmed 0_0
        slack_client.api_call("chat.postMessage", channel=channel, 
                                    text = txt, as_user = True)

# ================================= Main ===============================

if __name__ == "__main__":
    if slack_client.rtm_connect(): 
        print("yoshi_bot connected and running!")
        repeats = 0 
        k = 0 
        while True:
            text, channel = parse_slack_output(slack_client.rtm_read())
            if text and channel: 
                print text
                string = text.encode('utf-8')
                # turns the text from unicode to a Python string 
                if hasNumbers(string) and AT_BOT not in text: # if nums in text
                    check_illuminati(string, channel)
                elif AT_BOT not in text and repeats < 4 and 'bork' in string.lower(): 
                    bork(string,channel)
                    repeats += 1 
                    print repeats
                elif AT_BOT in text: # if the bot call is in the text 
                    # strips the bot call off of the text 
                    command = text.split(AT_BOT)[1].strip().lower() 
                    # handles the text of the text 
                    handle_command(command, channel)
                if repeats >= 4:
                    k += 1 
                    slack_client.api_call("chat.postMessage", channel=channel, 
                                    text = 'I won''t stop until you stop!'
                                    , as_user = True)
                    if k >= 2: 
                        k = 0 
                        repeats = 0
            time.sleep(0.3) 

    else:
        print("Connection failed. Invalid Slack token or bot ID?")