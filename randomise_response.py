# -*- coding: utf-8 -*-

import re
import random

def create_random(story_string):
    """
    For a story string delimited by <|>, generate a story, which is a list of
    lists of strings. For example, the story string
    "graham likes <cars|automobiles|motor vehicles>" will become
    ['graham likes ', ['cars', 'automobiles', 'motor vehicles'], '']
    Params:
        story_string - the input, a string
    Returns:
        story_split, the split version of the story
    """
    story_split = re.split('<|>', story_string) 
    for curr_string in range(len(story_split)):
        if '|' in story_split[curr_string]:
            story_split[curr_string] = story_split[curr_string].split('|')
    return story_split

def respond_random(story_split):
    """
    For a given story_split made with create_random, return that story_split
    with strings selected from the list at random.
    Params:
        story_split - list made with create_random
    Returns:
        response - string, story_split with random elements chosen
    """
    reponse = ""
    for item in story_split:
        if type(item) == str:
            reponse += item
        elif type(item) == list:
            reponse += random.choice(item)
    return reponse