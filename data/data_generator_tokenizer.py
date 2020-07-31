#!/usr/bin/env python
#coding=utf-8

import random
import pandas as pd
import numpy as np
from transformers import BertTokenizer
import pickle
from f_trans import gen2json

# Declare Tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")


greet = ["Hey, how are you doing? | I?�m good, and you? | I?�m fine, thanks. |", "Sup! | Sup | ", "Yo, what's up? | Nothing much. |", "Hey.", "Heyo!"]
location = "the Japanese place, a coffee shop, Daan Park, your place, my place, the theme park, a club, a bar, the Italian restaurant".split(', ')
day = "today, tomorrow, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday".split(', ')
time = "1 am; 2 am; 3 am; 4 am; 5 am; 6 am; 7 am; 8 am; 9 am; 10 am; 11 am; 12 pm; 1 pm; 2 pm; 3 pm; 4 pm; 5 pm; 6 pm; 7 pm; 8 pm; 9 pm; 10 pm; 11 pm; midnight, noon".split('; ')
#time = [x.strip() for x in "1 am; 2 am; 3 am; 4 am; 5 am; 6 am; 7 am; 8 am; 9 am; 10 am; 11 am; 12 pm; 1 pm; 2 pm; 3 pm; 4 pm; 5 pm; 6 pm; 7 pm; 8 pm; 9 pm; 10 pm; 11 pm".split('; ')]
activity = "catch up, go to a party, go bowling, grab lunch, grab coffee, ice skating, hang out, see a game, go to the park, see a concert, see a movie, see a play, watch a movie, go rafting, bake, go swimming".split(', ')

def get_tokenize(data):
    return tokenizer(data)

# Brute force
def find_match(list1, list2):
    for i in range(len(list1)-len(list2) + 1):
        if list1[i:i+len(list2)] == list2:
            return [i, i+len(list2)-1]
    


def generate_training_data(num):
    training_data_list = []
    training_label_list = []
    for i in range(num):
        g = random.choice(greet)

        # what
        a = random.choice(activity)
        # when(day)
        d = random.choice(day)
        # when(time)
        t = random.choice(time)
        # where
        l = random.choice(location)
        training_data = g + " Do you want to " + a + " on " + d + "? | Sure, what time? | How about " + t + "? | Sure, sounds good. | Where do you want to go? | How about " + l + "? | Sounds good. | See you then! |"

        # [what, when(day), when(time), where, what change, when(day) change, when(time) change, where change]
        #label = [find_match(get_tokenize(training_data)['input_ids'], get_tokenize(item)['input_ids'][1:-1]) for item in (a, d, t, l)]
        label = [{'text': text, 'answer_start': training_data.index(text)} for text in (a,d,t,l)]
        
        training_data_list.append(training_data)
        training_label_list.append(label)
    
    data = {"train_data" : training_data_list,  "label" : training_label_list}
    return data

def genone():
    data = generate_training_data(2000)
    with open('train_v0.pkl', 'wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    
    genone

#df = pd.DataFrame(generate_training_data(2000), columns= ['train_data', 'label'])
#df.to_csv('training_data.csv', sep='\t')

"""
with open('train.pkl', 'rb') as f:
    a =pickle.load(f)
"""


