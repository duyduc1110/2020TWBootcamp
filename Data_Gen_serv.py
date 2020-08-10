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

greet = ['|Hey, how are you doing? |I’m good, and you? |I’m fine, thanks. |',
 '|Hey, how’s it going? |Not too bad... How about you? |Pretty good. |',
 '|Sup! |Sup. |',
 "|Yo, what's up? |Nothing much. |",
 '|Hey. ','|Hello. |Hi. |', '|Hi. |Hello! |',
 '|Hey! ','|Hello!. |Hi! |','|Hi! |Hello. |',
 '|Hey, long time no talk. |Yea, how’ve you been? |Good. ']

location = ['the Japanese place',
 'a coffee shop',
 'Daan Park',
 'Xinyi',
 'the zoo',
 'the mall', 'Sogo', '7-11', 'Family Mart', 'the department store', 'the thrift shop', 'the clubhouse', 'the gym',
 'the train station',
 'your place',
 'my place',
 'the theme park',
 'a club',
 'a bar',
 'the Italian restaurant', 
 'school',
 'a casino',
 'Times Square',
 'McDonalds',
 'Raohe Night Market',
 'Dunhua']

day = ['today',
 'tomorrow',
 'on Sunday',
 'on Monday',
 'on Tuesday',
 'on Wednesday',
 'on Thursday',
 'on Friday',
 'on Saturday']

time = ['12 am', '1 am',
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
 'grab brunch',
 'get breakfast',
 'get dinner',
 'grab coffee',
 'go ice skating',
 'hang out',
 'watch the game',
 'see a baseball match',
 'see a concert',
 'watch a movie',
 'see a play',
 'see a musical',
 'watch a movie',
 'go rafting',
 'bake', 
 'cook',
 'go swimming',
 'go surfing',
 'go waterboarding',
 'go rafting',
 'go camping',
 'go kayaking',
 'play basketball',
 'play tennis',
 'go for a jog',
 'go shopping']

yes = ['|Sure. ', '|Ok. ', '|Sure! ', '|OK! ', '|Great. ', '|Sounds good. ', '|No problem. ', '|Okay. ', '|Aight. ']
qa = ["Would you want to ", "Do you want to ", "Let's "]
qt = ["What time? ", "When should we meet? ", "What time should we meet? ","When? "]
rt = ["|How about ", "|Let's do ", "|", "|You free ", "|Are you free at "]
rl = ["Let's do ", "I prefer ", "How about ", "We can go to ", "What about "]
qd = ["You free ", "Are you free "] #, "You busy "
ql = ["|Where should we go? ","|Where do you want to go? ","|Where should we meet? ","|Where? "]
cu = [" there"," then"]
tno = [" have an appointment. ", " can't. ","'m busy. "]
dno = ["'m busy... "," have plans already. ","'ll be out of town. "]
af = ["Yes. ","Yea. ","Ya. ","Yup. ","Yep. ","Yeah. ","Yah. ","Uh huh. "]

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
# 7/28, 8/3 updated
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
        example1 = g + askd + d + "? " + ye + "|" + aska + a +"? " + y[0] + askl + "|" + repl + l[0] + "? " + random.choice(["|Why not ", "|How about ", "|What about "]) + l[1] + "? Or " + l[2] + "? |" + random.choice(["I've never been to ", "I prefer ","I like ","I'd like to visit ", "I think it'd be cool to go to ", "I'd rather go to "])  + l[3] + ". |Let's " + random.choice(["go there", "do that", "meet there"]) + random.choice([" instead. ", ". ", " then. "]) + y[1] + "|See you" + fin +"!"
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,'',l[3])]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%
# 8/3 updated
# *yes, then no*
def gen_yn(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        l = random.sample(location, k=3)
        l.append(random.choice(l[1:3]))
        ye = random.choices(af, k=2)
        y = random.choices(yes, k=2)
        askd = random.choice(qd)
        aska = random.choice(qa)
        repl = random.choice(rl)
        askl = random.choice(ql)
        exc = random.choice([", I have to babysit my cousin. Sad... ", ". I have to babysit my cousin. ", ", I'm busy. ", ", I have a meeting. ", ", I'm meeting up with someone. ", ", I have something else. "])
        end = ["|Oh... Ok then. Next time.", "|Oh ok. That's fine. ", "|Aight, let me know when you're free. ", "|That's fine, next time. ", "|Okay, have fun! "]
        fin = random.choice(end) #askd + d + "? " + ye + 
        example1 = g + aska + a + " " + d +"? " + y[0] + askl + repl + l[0] + "? " + y[1] +"|Wait! Sorry! I forgot. I can't " + d + exc + fin
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in ('','','','')]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%
# 8/3
# *yes, then no* 2
def gen_yn2(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.choice(time)
        ye = random.choices(af, k=2)
        y = random.choices(yes, k=2)
        askd = random.choice(qd)
        aska = random.choice(qa)
        rept = random.choice(rt)
        askt = random.choice(qt)
        exc = random.choice(["I have to babysit my cousin ", "I have to babysit my cousin ", "I'm busy ", "I have a meeting ", "I'm meeting up with someone ", "I have something else "])
        end = ["|Oh... Ok then. Next time.", "|Oh ok. That's fine. ", "|Aight, let me know when you're free. ", "|That's fine, next time. ", "|Okay, have fun! "]
        fin = random.choice(end) #askd + d + "? " + ye + 
        example1 = g + aska + a + " " + d +"? " + y[0] + askt + rept + t + "? " + y[1] + "|My bad... Actually " + exc + d +". "+ fin
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in ('','','','')]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 

# %%
# 8/3
# *not a (so b)*
def gen_nota(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        l = random.sample(location, k=2)
        t = random.choice(time)
        if random.choice([True, False]) == True:
            l.extend(l)
        else:
            l.extend([l[1],l[0]])
        y = random.choices(yes, k=4)
        ye = random.choice(af)
        askd = random.choice(qd)
        aska = random.choice(qa)
        repl = random.choice(rl)
        askl = random.choice(ql)
        rept = random.choice(rt)
        askt = random.choice(qt)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a +" " + d + "? " + y[0] + askl + "|" + repl + l[0] + " or " + l[1] + "? |" + random.choice(["Not ", "Anything but ","I don't really like ","Let's not go to ", "I think don't think it'll be that fun if we go to ", "I'd not rather go to "]) + l[2] + ". " + y[1] + askt + rept + t +"? " + y[2] + y[3]
        example1 = example1.replace('|', '')
        if d[0:2] == "on":
            d = d[3:]
        label = [{'text': text, 'answer_start': example1.index(text)} for text in (a,d,t,l[3])]
        data.append([example1,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data 


# %% 
import sys

if __name__ == '__main__':
    
    simp = 20
    simpf = 20 
    t0 = 45
    t2 = 30
    t2f = 30
    t22l = 35
    t22lf = 35
    un = 40
    d20l = 35

    d21l = 35
    ml = 45
    yn = 32
    yn2 = 32
    nota = 45 # causing bigggggg issues

    # outpath = "./data/new_data_4800.json"
    # outpath = "./data/new_data_470.json"
    outpath = sys.argv[1]

    # data_simp = gen_simple(simp)
    # data_simpf = gen_simple_flip(simpf)
    # data_t0 = gen_0t(t0)
    # data_t2 = gen_t2(t2)
    # data_t2f = gen_t2_flipsplit(t2f)
    # data_t22l = gen_t22l(t22l)
    # data_t22lf = gen_t22l_flip(t22lf)
    # data_un = gen_un(un)
    # data_d20l = gen_2d0l(d20l)

    # data_d21l = gen_2d1l(d21l)
    # data_ml = gen_ml(ml)
    # data_yn = gen_yn(yn)
    # data_yn2 = gen_yn2(yn2)
    # data_nota = gen_nota(nota)
    
    data_all = [gen_simple(simp), gen_simple_flip(simpf), gen_0t(t0), gen_t2(t2), gen_t2_flipsplit(t2f), gen_t22l(t22l), gen_t22l_flip(t22lf), gen_un(un), gen_2d0l(d20l), gen_2d1l(d21l), gen_ml(ml), gen_yn(yn), gen_yn2(yn2), gen_nota(nota)]

    data = {"train_data":[],"label":[]}
    
    for d in data_all:
        data["train_data"].extend(d["train_data"])
        data["label"].extend(d["label"])

    temp = list(zip(data["train_data"], data["label"])) 
    random.shuffle(temp) 
    res1, res2 = zip(*temp) 
    data = {"train_data": list(res1), "label":list(res2)}
    
    #data = gen_nota(100)

    """
    with open(outpath, 'wb') as f:
        pickle.dump(data, f)
    """
    
    gen2json(data, outpath)
