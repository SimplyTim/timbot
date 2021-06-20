import random
import json
import numpy as np 
import lookup
import os

print("TimBot active!")

def timResponse(message):
    res = lookup.getAnswers(message)
    return res
