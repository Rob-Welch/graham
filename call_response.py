# -*- coding: utf-8 -*-
"""
call_response is a python backend for chatbots that will recite canned phrases.
author: rob w

usage:
    1) create an instance of call_respose (only one!) e.g. cr = call_response()
    2) pass it messages with a string identifying the server
       e.g. cr.parse("hello", "server_id")
    3) add responses to it by sending messages with the following syntax
       for responses:   ~graham-respond "come" "also arrive"
       for corrections: ~graham-permute "egg" "dippy egg"
"""

import os
import json
import randomise_response
import random
import modules as load_module

class call_response:

    def __init__(self, profile_path="call_response_index.json", decay_in=100, help_msg=""):
        """
        Will load in call_response_index.json if it exists. Otherwise it
        initialises an empty call response index. The index file is only saved
        when an entry is added to it (see self.add_response).
        """

        if os.path.exists(profile_path):
            self.index = json.load(open(profile_path, "r"))
        else:
            self.index = {}

        self.decay_in = decay_in
        self.help_msg=help_msg
        self.profile_path = profile_path
        self.modules = load_module.load()
        
        if len(self.modules) > 0:
            self.help_msg += ("\nCommands from modules:")
            for module in self.modules:
                try:
                    self.help_msg += ("\n"+module.help_str)
                except:
                    self.help_msg += ("\nModule "+module.__name__+"has no help string!")
        

    def parse(self, message, server):
        """
        If you've created an instance of call_response, use this method to
        talk to it. It will return an appropriate response, or an empty string
        if none of the response criteria are met.
        Params:
            message - the message, a string
            server - a string identifying the server the message is from
        """
        response = ""
        if message.startswith("~"):
            response = self.add_response(message, server)
        else:
            response = self.get_response(message, server)

        return response


    def get_response(self, message, server):
        """
        Query the response index and return the appropriate response. If there
        is none, return an empty string.
        Params:
            message - the message, a string
            server - a string identifying the server the message is from
        """

        if server not in self.index.keys():
            return ""

        stripgrammar = lambda string: string.lower().replace(",", "").replace(".", "").replace(":", "").replace("... ", "").replace("'", "").split(" ")
        split_msg = stripgrammar(message) # ignore grammar

        # first priority: permutations
        for original, replacement in self.index[server]["permute"].items():
            # if original in split_msg:
            if set(stripgrammar(original)).issubset(set(split_msg)):
                if replacement not in split_msg:
                    self.decay_response(server,"permute",original)
                    return message.lower().replace(original, replacement)

        # second priority: call/response
        for call, response in self.index[server]["respond"].items():
            #if call in split_msg:
            if set(stripgrammar(call)).issubset(set(split_msg)):
                self.decay_response(server,"respond",call)
                return response

        # randomize
        for call, response in self.index[server]["generate"].items():
            #if call in split_msg:
            if set(stripgrammar(call)).issubset(set(split_msg)):
                self.decay_response(server,"generate",call)
                return randomise_response.respond_random(response)

        # final: custom graham modules
        for module in self.modules:
            for call, response in self.index[server][module.__name__].items():
                if set(stripgrammar(call)).issubset(set(split_msg)):
                    self.decay_response(server,module.__name__,call)
                    return module.get_response(message.lower(), call, response)
            
        return ""


    def decay_response(self, server, category, entry):
        """
        Chance to remove a response from the response index. Called when the
        reponse is said, so more-used responses have a higher chance of being
        removed.
        Params:
            response - the dictionary entry corresponding to the call/original.
        """
        rand_decay = random.randint(0, self.decay_in)
        if rand_decay == 0:
            del self.index[server][category][entry]
            with open(self.profile_path, "w") as write_file:
                json.dump(self.index, write_file)


    def add_response(self, message, server):
        '''
        Append a response to the index. The syntax is as follows:
        ~respond "call" "response"
        ~permute "original" "corrected"
        Saves the updated index to the file "call_response_index.json", "w" as
        well as updating self.index.
        Params:
            message - the message, a string
            server - a string identifying the server the message is from
        '''
        # note: normally a generic try\except is bad but it's better for this
        # to respond with the error than to just crash or whatever
        
        return_msg = "did nothing"

        if message.split(" ")[0] == "~graham-help":
            return 'Curent server name: "'+server+'"\n\n'+self.help_msg

        stripgrammar = lambda string: string.lower().replace(",", "").replace(".", "").replace(":", "").replace("... ", "")

        # handle errors
        num_delimiters = 4

        if server == "":
            server = message.split('"')[5]
            num_delimiters += 2

        if message.count('"') != num_delimiters and not message.startswith("~graham-help"):
            return 'Error: got too many " marks or " in the wrong place. Note: as " are part of the graham syntax, they are forbidden in messages.'

        if len(stripgrammar(message.split('"')[1])) < 3:
            return "Error: call phrase is less than three characters long. Make it longer!"

        #formulate response

        try:

            if server not in self.index.keys(): # create new server
                self.index[server] = {"respond":{}, "permute":{}, "generate":{}}

            if message.split(" ")[0] == "~graham-respond":
                self.index[server]["respond"][stripgrammar(message.split('"')[1])] = message.split('"')[3]
                return_msg = "added reponse :)"

            if message.split(" ")[0] == "~graham-permute":
                self.index[server]["permute"][stripgrammar(message.split('"')[1])] = message.split('"')[3]
                return_msg = "added pemute"

            if message.split(" ")[0] == "~graham-generate":
                self.index[server]["generate"][stripgrammar(message.split('"')[1])] = randomise_response.create_random(message.split('"')[3])
                return_msg = "added generte"
            
            for module in self.modules:
                if message.split(" ")[0] == "~"+module.add_response_syntax:
                    call, response, = module.add_response( '"'.join(message.split('"')[:-1] ) )
                    if module.__name__ not in self.index[server]:
                        self.index[server][module.__name__] = {}
                    self.index[server][module.__name__][call] = response
                    return_msg = module.return_msg
                
        except Exception as e:
            return "could not parse request. errror: "+repr((e))

        #update index on hdd
        with open(self.profile_path, "w") as write_file:
            json.dump(self.index, write_file)

        return return_msg