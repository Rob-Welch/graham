# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'..')
import process_text

help_str = '~graham-permute - I will replace words with other words. For example: ~graham-permute "egg" "dippy egg" "server name"'
add_response_syntax = "graham-permute"
return_msg = "added permute"

def add_response(input_str):
    call = process_text.stripgrammar(input_str.split('"')[1])
    response = input_str.split('"')[3]
    return call, response

def get_response(message, call, response):
    output = message.lower().replace(call, response)
    return output