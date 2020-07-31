#!/usr/bin/env python
# coding: utf-8
# %%
import random
import pandas as pd
import numpy as np
import copy

from sklearn.utils import shuffle

import pickle
from f_trans import gen2json

greet = ['Hey, how are you doing?',
 'Sup!',
 "Yo, what's up?",
 'Hey! ']

greet_response = ['I’m good, and you?','I’m fine, thanks.', 'Sup.', 'Nothing much.', 'Hey.']

location = ['the Japanese place',
 'a coffee shop',
 'Daan Park',
 'Xinyi',
 'the zoo',
 'the mall',
 'the train station',
 'your place',
 'my place',
 'the theme park',
 'a club',
 'a bar',
 'the Italian restaurant', 
 "school"]

day = ['today',
 'tomorrow',
 'on Sunday',
 'on Monday',
 'on Tuesday',
 'on Wednesday',
 'on Thursday',
 'on Friday',
 'on Saturday']


activity = ['catch up',
 'do something',
 'go to a party',
 'go bowling',
 'go somewhere',
 'grab lunch',
 'grab coffee',
 'go ice skating',
 'hang out',
 'see a game',
 'see a concert',
 'see a movie',
 'see a play',
 'watch a movie',
 'go rafting',
 'bake',
 'go swimming',
 'go surfing']

yes = ['Sure. ', 'Ok. ', 'Sure! ', 'OK! ', 'Great. ', 'Sounds good. ']
qa = ["Would you want to ", "Do you want to ", "Let's "]

create_event = ["Would you want to ", "Do you want to ", "Let's "]

qt = ["What time? ", "When should we meet? ", "What time should we meet? ","When? "]
rt = ["How about ", "Let's do ", "You free ", "Are you free at "]
rl = ["Let's do ", "I prefer "]
qd = ["You free ", "Are you free "] #, "You busy "
ql = ["Where should we go? ","Where do you want to go? ","Where should we meet? ","Where? "]
cu = [" there"," then"]
tno = [" have an appointment. ", " can't. ","'m busy. "]
dno = ["'m busy... "," have plans already. ","'ll be out of town. "]

def chat_to_sentance(chat):
    return list(filter(None, chat.split('|')))

# null: unsuccessful
def gen_unnes(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        get_greet = random.choice(greet)
        get_activity = random.choice(activity)
        get_day = random.choice(day)
        get_day_ = random.sample(day, k=2)
        get_day_location = random.sample(location, k=2)
        get_day_location.append(random.choice(get_day_location))
        get_yes = random.choices(yes, k=3)      
        get_location = random.sample(location, k=2)
        get_quest_activity = random.choice(qa)
        get_quest_day = random.choice(qd)
        get_quest_location = random.choice(ql)
        get_respon_time = random.choices(rt, k=2)
        get_respon_location = random.choice(rl)
        dect = random.choice(tno)
        
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + get_day)
        fin = random.choice(cu_temp)


      # C  A  D  P  L
        train_data = []

      #[0, 0, 0, 0, 0]  
        train_data.append([[get_greet], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]) 
      #[1, 1, 0, 0, 0]  
        train_data.append([]) 
      #[0, 1, 0, 0, 0]  
        train_data.append([]) 
      #[0, 0, 1, 0, 0]  
        train_data.append([]) 
      #[0, 0, 0, 1, 0]  
        train_data.append([]) 
      #[1, 1, 1, 0, 0]  
        train_data.append([]) 
      #[1, 1, 0, 0, 0]  
        train_data.append([]) 
      #[1, 1, 1, 1, 0]  
        train_data.append([]) 
      #[0, 0, 0, 0, 1]  
        train_data.append([]) 

        print('[A, D, P, L]')
        for i in train_data:
            
            print(i)

    #print(data)
    return data

# %% 
import sys

if __name__ == '__main__':
    print('Gen 109')
    gen_unnes(1)
    print('dome-0')