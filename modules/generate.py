# -*- coding: utf-8 -*-
import re
import random
import sys
sys.path.insert(0,'..')
import process_text

help_str = '~graham-generate - I will pick words from a random pool. For example: ~graham-generate "fortune" "your fortune is <good|bad|mediocre|full of eggs>" "server name"'
add_response_syntax = "graham-generate"
return_msg = "added generate"

def add_response(input_str):
    call = process_text.stripgrammar(input_str.split('"')[1])
    story_split = input_str.split('"')[3]
    story_split = re.split('<|>', story_split)
    for curr_string in range(len(story_split)):
        if '|' in story_split[curr_string]:
            story_split[curr_string] = story_split[curr_string].split('|')
    return call, story_split

def get_response(message, call, response): #formerly respond_random
    output = ""
    for item in response:
        if type(item) == str:
            output += item
        elif type(item) == list:
            output += random.choice(item)
    return output