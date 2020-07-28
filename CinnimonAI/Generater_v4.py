#!/usr/bin/env python
# coding: utf-8

# In[52]:


import random
import pandas as pd
import numpy as np


# In[53]:


#df = pd.DataFrame(columns=['Text', 'Output'])


# In[54]:


greet = ["Hey, how are you doing? |I’m good, and you? |I’m fine, thanks. |", "Sup! |Sup. |", "Yo, what's up? |Nothing much. |", "Hey. ", "Heyo! "]
location = "the Japanese place, a coffee shop, Daan Park, the mall, the train station, your place, my place, the theme park, a club, a bar, the Italian restaurant".split(', ')
day = "today, tomorrow, on Sunday, on Monday, on Tuesday, on Wednesday, on Thursday, on Friday, on Saturday".split(', ')
time = "1 am; 2 am; 3 am; 4 am; 5 am; 6 am; 7 am; 8 am; 9 am; 10 am; 11 am; 12 pm; 1 pm; 2 pm; 3 pm; 4 pm; 5 pm; 6 pm; 7 pm; 8 pm; 9 pm; 10 pm; 11 pm; midnight, noon".split('; ')
#time = [x.strip() for x in "1 am; 2 am; 3 am; 4 am; 5 am; 6 am; 7 am; 8 am; 9 am; 10 am; 11 am; 12 pm; 1 pm; 2 pm; 3 pm; 4 pm; 5 pm; 6 pm; 7 pm; 8 pm; 9 pm; 10 pm; 11 pm".split('; ')]
activity = "catch up, do something, go to a party, go bowling, go somewhere, grab lunch, grab coffee, ice skating, hang out, see a game, see a concert, see a movie, see a play, watch a movie, go rafting, bake, go swimming".split(', ')
yes = "|Sure. , |Ok. , |Sure! , |OK! , |Great. , |Sounds good. ".split(', ')


# In[55]:


# easy, success
def gendat1(rows):
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.choice(time)
        l = random.choice(location)
        y = random.choices(yes, k=3)
        example1 = g + "Do you want to " + a + " " + d + "? "+ y[0] + "What time? |How about " + t + "? "+ y[1] + "|Where do you want to go? |How about " + l + "? "+ y[2] + "|See you then!"
        data.append(example1)
    return list(set(data)) # ensure unique
 


# In[56]:


data1 = gendat1(100)
len(data1)
data1


# In[76]:


# second time
def gendatt(rows):
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.sample(time, k=2)
        l = random.choice(location)
        y = random.choices(yes, k=3)
        aska = random.choice(["Would you want to ", "Do you want to ", "Let's "])
        askt = random.choice(["What time? ", "When should we meet? ", "When? "])
        rept = random.choices(["|How about ", "|Let's do ", "|", "|You free "], k=2)
        askl = random.choice(["|Where should we go? ","|Where do you want to go? ","|Where should we meet? ","|Where? "])
        example1 = g + aska + a + " " + d + "? " + y[0] + askl + "|How about " + l + "? "+ y[1] + askt + rept[0] + t[0] + "? |Sorry, I can't. " + rept[1] + t[1] + "? "+y[2]+ "|See you then!"
        data.append((example1,a,d,t[1],l))
    return pd.DataFrame(data, columns =['Text', 'Activity','Day','Time',"Location"]) # always the second time
# didn't remove "on" because grammatical when reassemble


secondt = gendatt(500).drop_duplicates()
secondt["Text"][0]


#secondt.to_csv('secondt.csv')


# where I currently using ... Hank
# more complex (location)
def gendatl(rows):
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.sample(time, k=2)
        l = random.choice(location)
        y = random.choices(yes, k=3)
        aska = random.choice(["Would you want to ", "Do you want to ", "Let's "])
        askt = random.choice(["What time? ", "When should we meet? ", "When? "])
        rept = random.choices(["|How about ", "|Let's do ", "|", "|You free "], k=2)
        askl = random.choice(["|Where should we go? ","|Where do you want to go? ","|Where should we meet? ","|Where? "])
        example1 = g + aska + a + " " + d + "? " + y[0] + askl + "|I don't know. |How about " + l + "? "+ y[1] + askt + rept[0] + t[0] + "? |Sorry, I can't. " + rept[1] + t[1] + "? "+y[2]+ "|See you then!"
        data.append((example1.replace('|', ''),a,d,t[1],l))
    return pd.DataFrame(data, columns =['Text', 'Activity','Day','Time',"Location"]) # always the second time
# didn't remove "on" because grammatical when reassemble


manyl = gendatl(1)

manyl["Text"][0]



# easy, success; with human indexing
def gendatans1():
    data = []
    for i in range(100):
        g = random.choice(greet)
        a = random.choice(activity)
        d = random.choice(day)
        t = random.choice(time)
        l = random.choice(location)
        example1 = g + "Do you want to " + a + " " + d + "? |Sure, what time? |How about " + t + "? |Sure, sounds good. |Where do you want to go? |How about " + l + "? |Sounds good. |See you then!"
        # [what, when(day), when(time), where, what change, when(day) change, when(time) change, where change]
        answer1 = []
        answer1.append([len(g.split())+4])
        answer1[0].append(answer1[0][0]+len(a.split())-1)
        answer1.append([answer1[0][1]+1])
        answer1[1].append(answer1[1][0]+len(d.split())-1)
        answer1.append([answer1[1][1]+6])
        answer1[2].append(answer1[2][0]+len(t.split())-1)
        answer1.append([answer1[2][1]+12])
        answer1[3].append(answer1[3][0]+len(l.split())-1)
        answer1.extend([[-1,-1],[-1,-1],[-1,-1],[-1,-1]])
        data.append((example1,answer1))
    return data
 


# In[42]:


data1 = gendatans1()
#data1


# In[ ]:




