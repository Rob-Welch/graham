# -*- coding: utf-8 -*-

import sys
sys.path.insert(0,'..')
import process_text

help_str = '~graham-respond - I will respond to one phrase with another phrase. For example: ~graham-respond "come" "and also arrive" "server name"'
add_response_syntax = "graham-respond"
return_msg = "added response :)"

def add_response(input_str):
    call = process_text.stripgrammar(input_str.split('"')[1])
    response = input_str.split('"')[3]
    return call, response

def get_response(message, call, response):
    return response