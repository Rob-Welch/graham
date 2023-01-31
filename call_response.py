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
import random
import modules as load_module
import process_text
import meta
from cryptography.fernet import Fernet
import base64, hashlib

class call_response:

    def __init__(self, profile_path="call_response_index.json", decay_in=50,
                 help_msg="", gdpr_expiry=31536000, cryptokey=None):
        """
        Will load in call_response_index.json if it exists. Otherwise it
        initialises an empty call response index. The index file is only saved
        when an entry is added to it (see self.add_response).
        """
        
        if cryptokey is not None:
            hlib = hashlib.md5()
            hlib.update(cryptokey.encode("utf-8"))
            cryptokey = base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))
            self.fernet = Fernet(cryptokey)

        if os.path.exists(profile_path):
            with open(profile_path, "rb") as file:
                contents = file.read()
                if cryptokey is not None:
                    contents = self.fernet.decrypt(contents)
                self.index = json.loads(contents)
        else:
            self.index = {}
            self.index["_settings"] = {}
            self.index["_settings"]["last-cleanup"] = int(meta.time.time())

        self.decay_in = decay_in
        self.help_msg=help_msg
        self.profile_path = profile_path
        self.modules = load_module.load()
        self.gdpr_expiry = gdpr_expiry
        
        if len(self.modules) > 0:
            self.help_msg += ("\nCommands from modules:")
            for module in self.modules:
                try:
                    self.help_msg += ("\n"+module.help_str)
                except:
                    self.help_msg += ("\nModule "+module.__name__+"has no help string!")
        
    def export(self):
        with open(self.profile_path, "wb") as write_file:
            try:
                encrypted = self.fernet.encrypt(json.dumps(self.index).encode("utf-8"))
            except: 
                encrypted = json.dumps(self.index).encode("utf-8")
            write_file.write(encrypted)


    def parse(self, message, server, username=None):
        """
        If you've created an instance of call_response, use this method to
        talk to it. It will return an appropriate response, or an empty string
        if none of the response criteria are met.
        Params:
            message - the message, a string
            server - a string identifying the server the message is from
        """
        response = ""
        
        ignore = self.ignore(message, username)
        if ignore:
            return response
        
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

        split_msg = process_text.stripgrammar(message).split(" ") # ignore grammar
        
        # final: custom graham modules
        for module in self.modules:
            for call, response in self.index[server][module.__name__].items():
                response = meta.strip_metadata(response)
                if set(process_text.stripgrammar(call).split(" ")).issubset(set(split_msg)):
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
            self.export()

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

        # handle errors
        num_delimiters = 4

        if server == "":
            server = message.split('"')[5]
            num_delimiters += 2

        if message.count('"') != num_delimiters and not message.startswith("~graham-help"):
            return 'Error: got too many " marks or " in the wrong place. Note: as " are part of the graham syntax, they are forbidden in messages.'

        if len(process_text.stripgrammar(message.split('"')[1])) < 3:
            return "Error: call phrase is less than three characters long. Make it longer!"

        #formulate response

        try:

            if server not in self.index.keys(): # create new server
                self.index[server] = {"respond":{}, "permute":{}, "generate":{}}
                for module in self.modules:
                    self.index[server][module.add_response_syntax.split("-")[1]] = {}
            
            for module in self.modules:
                if message.split(" ")[0] == "~"+module.add_response_syntax:
                    call, response, = module.add_response( '"'.join(message.split('"')[:-1] ) )
                    if module.__name__ not in self.index[server]:
                        self.index[server][module.__name__] = {}
                    self.index[server][module.__name__][call] = meta.add_metadata(response)
                    return_msg = module.return_msg
                
        except Exception as e:
            return "could not parse request. errror: "+repr((e))

        #update index on hdd
        self.export()

        return return_msg
    
    def tidy(self):
        if meta.time.time() > int(self.index["_settings"]["last-cleanup"]) + 60*60:
            for servername, server in self.index.items():
                for modulename, module in server.items():
                    for entryname, entry in module.items():
                        if "date" in entry:
                            if int(entry.date)+self.gdpr_expiry > meta.time.time():
                                del self.index[servername][modulename][entryname]
                                self.export()
            self.index["_settings"]["last-cleanup"] = int(meta.time.time())

    def ignore(self, message, user):
        ignored = False
        if "ignored-users" not in self.index["_settings"]:
            self.index["_settings"]["ignored-users"] = []
        if message.split(" ")[0] == "~graham-ignore":
            ignored = True
            self.index["_settings"]["ignored-users"].append(user)
            self.export()
        else:
            if user in self.index["_settings"]["ignored-users"]:
                ignored = True
        return ignored