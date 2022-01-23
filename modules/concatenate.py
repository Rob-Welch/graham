stripgrammar = lambda string: string.lower().replace(",", "").replace(".", "").replace(":", "")

"""
This is an example module for graham. It concatenates words together. So,
weirdly, it has a call but no response, which makes it kind of a bad example
module.
You add stuff to it like this:
    
~graham-concatenate "thanks" "" 
    
Based on the 'thanks' trigger word, if someone says 'thanks graham' then he
will respond 'thaham', if they say 'thanks ants', he will respond 'thants'.

All graham modules must have the two functions 'add_response' and 'get_response.'
add_response is how stuff gets added to the database and get_response is what
graham uses to formulate a response to a message.

add_response has one parameter - the input string, e.g.

~graham-concatenate "thanks" "" 

It can be whatever you want, but if your message doesn't have a tilde in
it, it won't set graham into 'add' mode. It returns two values,

    call: the word/phrase that triggers graham to respond.
    
    response: how graham's response is stored. This can be anything, as long
    as it's serializable into json. The buillt-in graham modules use some
    combinations of strings and lists of strings. This is 
    
get_response has three parameters - message, call and response.

    message - the message in its raw state. The message will contain the
    'call' phrase, you don't need to check that.
    
    call - the call phrase
    
    response - the contents of the response that you defined in
    graham-concatenate.
    
It only has one return value, output, which is simply the message that graham
will post.

In addition to these two functions, your graham module should have the
variables help_str and add_response_syntax defined globally. The help_str
displays in ~graham-help. The add_response_syntax is the string that
initiates the add_response function of this module.

"""

help_str = '~graham-concatenate - I will combine together one word with the next. For example: ~graham-respond "thanks" "" "server name"'
add_response_syntax = "graham-concatenate"
return_msg = "concatenated"

def add_response(input_str):
    
    call = stripgrammar(input_str.split('"')[1])
    response = ""
    
    return call, response

def get_response(message, call, response):
    
    output = splice_word(message, call)
    
    return output

"""
All of the stuff below here  is specific to the functionality of this module,
so if you're just looking for how to make modules for graham, you can stop
here.
"""

def splice_word(message, call):
    
    vowels = ["a", "e", "i", "o", "u"]
    
    # for a given message, return a list of indices of vowels
    def get_vowel_index(message):
        vowel_indices = []
        for letter_i in range(len(message)):
            if message[letter_i] in vowels:
                vowel_indices.append(letter_i)
        return vowel_indices
    
    # check if word is in message
    word_index = -1
    message_stripped = stripgrammar(message).split(" ")
    for word in range(len(message_stripped)):
        if message_stripped[word] == call:
            word_index = word
    
    # return an empty string if not
    if (word_index == len(message_stripped)-1) or word_index == -1:
        return ""
    
    # cludge words together
    first_word = message_stripped[word_index]
    second_word = message_stripped[word_index+1]
    
    first_vowel_indices = get_vowel_index(first_word)
    second_vowel_indices = get_vowel_index(second_word)
    
    # if there are no vowels, do nothing
    if len(first_vowel_indices) == 0 or len(second_vowel_indices) == 0:
        return ""
        
    first_word_altered = first_word[:first_vowel_indices[0]]
    second_word_altered = second_word[second_vowel_indices[0]:]
    
    replacement = first_word_altered+second_word_altered
    
    return replacement