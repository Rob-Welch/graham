# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:49:39 2020

@author: Robert|
"""

import re
import random

def create_random(story_string):
    #num_randoms = story_string.count('<')
    story_split = re.split('<|>', story_string)
    for curr_string in range(len(story_split)):
        if '|' in story_split[curr_string]:
            story_split[curr_string] = story_split[curr_string].split('|')
    return story_split

def respond_random(story_split):
    reponse = ""
    for item in story_split:
        if type(item) == str:
            reponse += item
        elif type(item) == list:
            reponse += random.choice(item)
    return reponse