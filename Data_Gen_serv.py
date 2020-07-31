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

# %%
# from transformers import BertTokenizer, AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2", use_fast=True)

# def get_tokenize(data):
#     return tokenizer(data)

# # Brute force
# def find_match(list1, list2):
#     l = len(list2)
#     for i in range(len(list1)-l + 1):
#         if list1[i:i+l] == list2:
#             return [i, i+l-1]
#     return [0,0]

# %%
greet = ['|Hey, how are you doing? |I’m good, and you? |I’m fine, thanks. |',
 '|Sup! |Sup. |',
 "|Yo, what's up? |Nothing much. |",
 '|Hey. ',
 '|Hey! ']

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

time = ['1 am',
 '2 am',
 '3 am',
 '4 am',
 '5 am',
 '6 am',
 '7 am',
 '8 am',
 '9 am',
 '10 am',
 '11 am',
 '12 pm',
 '1 pm',
 '2 pm',
 '3 pm',
 '4 pm',
 '5 pm',
 '6 pm',
 '7 pm',
 '8 pm',
 '9 pm',
 '10 pm',
 '11 pm',
 'midnight', 'noon']

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

yes = ['|Sure. ', '|Ok. ', '|Sure! ', '|OK! ', '|Great. ', '|Sounds good. ']
qa = ["Would you want to ", "Do you want to ", "Let's "]
qt = ["What time? ", "When should we meet? ", "What time should we meet? ","When? "]
rt = ["|How about ", "|Let's do ", "|", "|You free ", "|Are you free at "]
rl = ["Let's do ", "I prefer "]
qd = ["You free ", "Are you free "] #, "You busy "
ql = ["|Where should we go? ","|Where do you want to go? ","|Where should we meet? ","|Where? "]
cu = [" there"," then"]
tno = [" have an appointment. ", " can't. ","'m busy. "]
dno = ["'m busy... "," have plans already. ","'ll be out of town. "]

# %%
# easy, success
def gen_simple(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.choice(time)
        l = random.choice(location)
        y = random.choices(yes, k=3)
        aska = random.choice(qa)
        askt = random.choice(qt)
        rept = random.choice(rt)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? "+ y[0] + askt+ rept + t + "? "+ y[1] + askl + "|How about " + l + "? "+ y[2] + "|See you"+ fin +"!"
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,t,l)]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data     

# %%
# easy, success
def gen_simple_flip(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.choice(time)
        l = random.choice(location)
        y = random.choices(yes, k=3)
        aska = random.choice(qa)
        askt = random.choice(qt)
        rept = random.choice(rt)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? "+ y[0]  + askl + "|How about " + l + "? "+ y[2] + askt + rept + t + "? "+ y[1] + "|See you"+ fin +"!"
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,t,l)]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%

# second time
def gen_t2(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.sample(time, k=2)
        l = random.choice(location)
        y = random.choices(yes, k=3)
        aska = random.choice(qa)
        askt = random.choice(qt)
        rept = random.choices(rt, k=2)
        dect = random.choice(tno)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? " + y[0] + askl + "|How about " + l + "? "+ y[1] + askt + rept[0] + t[0] + "? |Sorry, I" + dect + rept[1] + t[1] + "? "+y[2] + "|See you"+ fin +"!"
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,t[1],l)]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%
# second time
def gen_t2_flipsplit(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.sample(time, k=2)
        l = random.choice(location)
        y = random.choices(yes, k=4)
        aska = random.choice(qa)
        askt = random.choice(qt)
        rept = random.choices(rt, k=2)
        ct = random.choice(["|Actually, I", "|I forgot, I", "|Sorry, I"])
        dect = random.choice(tno)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? " + y[0] + askt + rept[0] + t[0] + "? " + y[3] + askl + "|How about " + l + "? "+ y[1] + ct + dect[0:-2] + " " + t[0] + ". " + rept[1] + t[1] + "? "+ y[2] + "|See you"+ fin +"!"
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,t[1],l)]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%
# two days, missing location
def gen_2d0l(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.sample(day, k=2)
        t = random.choice(time)
        l = random.choice(location)
        y = random.choices(yes, k=2)
        aska = random.choice(qa)
        askt = random.choice(qt)
        repd = random.choices(rt, k=2)
        dno = ["|I can't","|Sorry I'm busy"]
        dno2 = [". "]
        dno2_temp = copy.deepcopy(dno2)
        dno2_temp.append(" " + d[0] + ". ")
        decd = random.choice(dno)
        decd2 = random.choice(dno2_temp)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d[1])
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d[0] + "? " + decd + decd2 +  "|How about " + d[1] + "? "+ y[0] + askt +"|" + t + "? "  +y[1] + "|See you"+ fin +"!"
        example1 = example1.replace('|', '')
        if d[1][0:2] == "on":
            d[1] = d[1][3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d[1],t,'')]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%
# two locations (+ second time above)
def gen_t22l(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.sample(time, k=2)
        l = random.sample(location, k=2)
        l.append(random.choice(l))
        y = random.choices(yes, k=3)      
        aska = random.choice(qa)
        askt = random.choice(qt)
        rept = random.choices(rt, k=2)
        dect = random.choice(tno)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d[1])
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? " + y[0] + askl + "|I don't know. |How about " + l[0] + "? Or " + l[1] + "? "+ y[1] + "Let's do " + l[2] + ". " + askt + rept[0] + t[0] + "? |Sorry, I" + dect + rept[1] + t[1] + "? "+y[2] + "|See you"+ fin +"!"
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,t[1],l[2])]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 


# %%
# two locations (+ second time above) - flipped
def gen_t22l_flip(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.sample(time, k=2)
        l = random.sample(location, k=2)
        l.append(random.choice(l))
        y = random.choices(yes, k=3)      
        aska = random.choice(qa)
        askt = random.choice(qt)
        rept = random.choices(rt, k=2)
        repl = random.choice(rl)
        dect = random.choice(tno)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? " + y[0] + askt + rept[0] + t[0] + "? |Sorry, I" + dect + rept[1] + t[1] + "? "+y[1] + askl + "|I don't know. |How about " + l[0] + " or " + l[1] + "? "+ y[1] + repl + l[2] + ". " + y[2] + "|See you" + fin +"!"
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,t[1],l[2])]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

#%%

# null: unsuccessful
def gen_un(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        d = random.sample(day, k=2)
        y = random.choice(yes)      
        askd = random.choice(qd)
        decd = random.choice(dno)
        example1 = g + askd + d[0] + "? " + "|Sorry, I" + decd + "|How about " + d[1] + "? "+ "|I'm busy on " + d[1] +" too. "+ "|That's fine, next time then. " + y 
        example1 = example1.replace('|', '')
        label = [{'text': text, 'answer_start': example1.index(text)} for text in ('','','','')]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data

# %%

# simple, but no time
def gen_0t(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        l = random.choice(location)
        y = random.choices(yes, k=3) 
        askd = random.choice(qd)
        aska = random.choice(qa)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d)
        fin = random.choice(cu_temp)
        example1 = g + askd + d + "? " + "|Yes. " + "|"+ aska + a + "? " + y[1] + askl + "|How about " + l + "? "+ y[2] + "|See you"+ fin +"!"
        example1 = example1.replace('|', '') 
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,"",l)]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%
# 7/28
# *two days, 1 location*
def gen_2d1l(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.sample(day, k=2)
        t = random.choice(time)
        l = random.choice(location)
        y = random.choices(yes, k=3)
        aska = random.choice(qa)
        askt = random.choice(qt)
        repd = random.choices(rt, k=2)
        dno = ["|I can't","|Sorry I'm busy"]
        dno2 = [". "]
        dno2_temp = copy.deepcopy(dno2)
        dno2_temp.append(" " + d[0] + ". ")
        decd = random.choice(dno)
        decd2 = random.choice(dno2_temp)
        askl = random.choice(ql)
        repl = random.choice(["|Maybe ","|How about ","|"])
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d[1])
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d[0] + "? " + decd + decd2 +  "|How about " + d[1] + "? "+ y[0] + askt +"|" + t + "? " + y[1] + askl + repl + l +"? "+ y[2] + "|See you"+ fin +"!"
        example1 = example1.replace('|', '')
        if d[1][0:2] == "on":
            d[1] = d[1][3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d[1],t,l)]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%
# 7/28
# *multi-location*
# %%
# *multi-location*
def gen_ml(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        l = random.sample(location, k=3)
        l.append(random.choice(l[1:3]))
        y = random.choices(yes, k=2)
        ye = random.choice(af)
        askd = random.choice(qd)
        aska = random.choice(qa)
        repl = random.choice(rl)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d)
        fin = random.choice(cu_temp)
        example1 = g + askd + d + "? " + ye + "|" + aska + a +"? " + y[0] + askl + "|" + repl + l[0] + "? " + random.choice(["|Why not ", "|How about "]) + l[1] + "? Or " + l[2] + "? |" + random.choice(["I've never been to ", "I prefer ","I like ","I'd like to visit ", "I think it'd be cool to go to "])  + l[3] + ", let's " + random.choice(["go there", "do that", "meet there"]) + random.choice([" instead. ", ". ", " then. "]) + y[1] + "|See you" + fin +"!"
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,'',l[3])]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 



# %% 
import sys

if __name__ == '__main__':
    
    simp = 200
    simpf = 200 
    t0 = 500
    t2 = 300
    t2f = 300
    t22l = 350
    t22lf = 350
    un = 500
    d20l = 500

    outpath = "./data/new_data.json"
    # outpath = sys.argv[1]

    data_simp = gen_simple(simp)
    data_simpf = gen_simple_flip(simpf)
    data_t0 = gen_0t(t0)
    data_t2 = gen_t2(t2)
    data_t2f = gen_t2_flipsplit(t2f)
    data_t22l = gen_t22l(t22l)
    data_t22lf = gen_t22l_flip(t22lf)
    data_un = gen_un(un)
    data_d20l = gen_2d0l(d20l)
    data = dict()
    
    for key in data_simp.keys():
        data[key] = data_simp[key]+data_simpf[key]+data_t0[key]+data_t2[key]+data_t2f[key]+data_t22l[key]+data_t22lf[key]+data_un[key]+data_d20l[key]
    
    temp = list(zip(data["train_data"], data["label"])) 
    random.shuffle(temp) 
    res1, res2 = zip(*temp) 
    data = {"train_data": list(res1), "label":list(res2)}

    """
    with open(outpath, 'wb') as f:
        pickle.dump(data, f)

    """
    
    gen2json(data, outpath)
