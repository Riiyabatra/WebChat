import train_chatbot
import subprocess
import pickle
import nltk
import os
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import texttospeech

import speechtotext 



lemmatizer = WordNetLemmatizer()
import numpy as np
from keras.models import load_model
model = load_model('/Users/ar-riya.batra/Documents/FinalYearProject/final/chatbot_model.h5')
import json
import random
intents = json.loads( open('/Users/ar-riya.batra/Documents/FinalYearProject/final/intents.json').read())
words = pickle.load(open('/Users/ar-riya.batra/Documents/FinalYearProject/final/words.pkl', 'rb'))
classes = pickle.load(open('/Users/ar-riya.batra/Documents/FinalYearProject/final/classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == 'noanswer'):
            texttospeech.tts('Any prticular brand')
            print('bot: Any particular brand?: ')
            
            ans = speechtotext.sst()
            print('user:'+ans)
            if(ans=='yes'):
                texttospeech.tts('bot: enter the brand')
                print('bot: enter the brand: ')
                
                brand = speechtotext.sst()
                print('user:'+brand)
                file1 = open('/Applications/XAMPP/htdocs/brand.txt', 'w')
                file1.write(brand)
                file1.close()
                file1 = open('/Applications/XAMPP/htdocs/answer.txt', 'w')
                file1.write(ans)
                file1.close()
            else: 
                file1 = open('/Applications/XAMPP/htdocs/answer.txt', 'w')
                file1.write(ans)
                file1.close()
            # texttospeech.tts('enter the minimum price')
            # print('bot: enter the minimum price\nuser: ')
            
            # minPrice = speechtotext.sst()
            # print('user:'+maxPrice)
            # texttospeech.tts('enter the maximum price')
            # print('bot: enter the maximum price')
            
            # maxPrice = speechtotext.sst()
            # print('user:'+maxPrice)
            # file1 = open('/Applications/XAMPP/htdocs/price.txt', 'w')
            # file1.write(minPrice + ' ' + maxPrice)
            # file1.close()
            # texttospeech.tts('enter the minimum feeback score')
            # print('bot: enter the minimum feeback score\nuser: ')
            
            # feedback = speechtotext.sst()
            # print('user:'+feedback)
            # file1 = open('/Applications/XAMPP/htdoc/feedback.txt', 'w')
            # file1.write(feedback)
            # file1.close()
            # ebay.py calls php
            proc = subprocess.Popen("python /Users/ar-riya.batra/Documents/FinalYearProject/final/ebay1.py", shell=True, stdout=subprocess.PIPE)
            script_response = proc.stdout.read()
            result = script_response.strip().decode('utf-8')
            break
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model) # ints contains intent and probability
    res = getResponse(ints, intents)
    return res

def send():
    
    message = []
    texttospeech.tts("user")
    print('user: ')
    msg = speechtotext.sst()
    print('user: ' + msg)
    stop_words = set(stopwords.words('english'))
    newStopWords = ['the','The','then','to','etc.','This','It', 'Our', 'buy', 'i', 'I', 'want', 'a', 'to']
    stopWordsList = stop_words.union(newStopWords)
    for word in msg.split():
        if word not in stopWordsList:
            message.append(word)
    msg = ""
    for word in message:
        msg = msg + word
    #msg = input('user: ')
    file1 = open('/Applications/XAMPP/htdocs/msg.txt', 'w')
    file1.write(msg)
    file1.close()
    if msg == 'quit':
        exit()
    res = chatbot_response(msg)
    texttospeech.tts(res)########################################
    print('bot: ' + res)
    send()
texttospeech.tts(" We can start the conversation now")
print(" We can start the conversation now")
send()
