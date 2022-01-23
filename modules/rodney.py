stripgrammar = lambda string: string.lower().replace(",", "").replace(".", "").replace(":", "")

help_str = '~graham-rodney - I will take a word and use the word before or after it in a phrase. For example: ~graham-rodney "work" "I sure hope <before> works" "server name"'
add_response_syntax = "graham-rodney"
return_msg = "rodneyed"

def add_response(input_str):
    spl = input_str.split('"')
    call = stripgrammar(spl[1])
    response = spl[3]
    return call, response

def get_response(message, call, response):
    output = create_response(message, call, response)
    
    return output

def create_response(message, call, response):
    arr = message.split(" ")
    ind = arr.index(call)
    try:
        if "<after>" in response:
            response = response.replace("<after>", find_word(arr, ind, 1))
        if "<before>" in response:
            response = response.replace("<before>", find_word(arr, ind, -1))
        return response
    except IndexError:
        return ""

def find_word(arr, ind, num):
    skipWords = ["a", "an", "the"]
    while(True):
        
        if(arr[ind + num] not in skipWords):
            return arr[ind+num]
        if num < 0:
            num -= 1
        else:
            num+=1