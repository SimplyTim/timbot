import random
import json
import pickle
import numpy as np 
import lookup
import os

import nltk
from nltk.stem import WordNetLemmatizer
nltk.data.path.append('./nltk_data/')

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('timbotmodel.h5')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def cleanUpSentence(sentence):
    sentenceWords = nltk.word_tokenize(sentence)
    sentenceWords = [lemmatizer.lemmatize(word) for word in sentenceWords]
    return sentenceWords

def getBagOfWords(sentence):
    sentenceWords = cleanUpSentence(sentence)
    bag = [0] * len(words)
    for word1 in sentenceWords:
        for i, word2 in enumerate(words):
            if word1 == word2:
                bag[i] = 1
    return np.array(bag)

def predictClass(sentence):
    bagOfWords = getBagOfWords(sentence)
    result = model.predict(np.array([bagOfWords]))[0]
    theta = 0.25
    results = [[i,r] for i, r in enumerate(result) if r > theta]

    results.sort(key=lambda x:x[1], reverse=True)
    returnList = []
    for r in results:
        returnList.append({"intent":classes[r[0]], "probability":str(r[1])})
    return returnList

def getResponse(intentsList, intentsJSON):
    tag = intentsList[0]['intent']
    listOfIntents = intentsJSON['intents']
    for i in listOfIntents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("TimBot active!")

'''
while True:
    message = input("")
    ints = predictClass(message)
    res = getResponse(ints, intents)

    if res == "1998199819981998":
        res = lookup.getAnswers(message)
    
    print(res)
'''

def timResponse(message):
    ints = predictClass(message)
    res = getResponse(ints, intents)

    if res == "1998199819981998":
        res = lookup.getAnswers(message)
    
    return res
