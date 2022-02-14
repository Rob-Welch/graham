# -*- coding: utf-8 -*-

grammar = [",", ".", ":", "!", "?", "\"", "~", "'", ";", "(", ")"]

def stripgrammar(string):
    for character in grammar:
        string = string.replace(character, "")
    return string
