# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 14:50:22 2022

@author: rob
"""

import time

def add_metadata(entry):
    metadata = {}
    metadata["content"] = entry
    metadata["date"] = str(int(time.time()))
    return metadata

def strip_metadata(entry):
    content = entry["content"]
    return content