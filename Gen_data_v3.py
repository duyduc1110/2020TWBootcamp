#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
import pandas as pd
import numpy as np
import copy


# In[3]:


from sklearn.utils import shuffle


# In[4]:


from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

def get_tokenize(data):
    return tokenizer(data)


# In[24]:


greet = ['|Hey, how are you doing? |I’m good, and you? |I’m fine, thanks. |',
 '|Sup! |Sup. |',
 "|Yo, what's up? |Nothing much. |",
 '|Hey. ',
 '|Heyo! ']

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
 'the Italian restaurant']

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
 'ice skating',
 'hang out',
 'see a game',
 'see a concert',
 'see a movie',
 'see a play',
 'watch a movie',
 'go rafting',
 'bake',
 'go swimming']

yes = ['|Sure. ', '|Ok. ', '|Sure! ', '|OK! ', '|Great. ', '|Sounds good. ']
qa = ["Would you want to ", "Do you want to ", "Let's "]
qt = ["What time? ", "When should we meet? ", "What time should we meet? ","When? "]
rt = ["|How about ", "|Let's do ", "|", "|You free ", "|Are you free at "]
qd = ["You free ", "Are you free "] #, "You busy "
ql = ["|Where should we go? ","|Where do you want to go? ","|Where should we meet? ","|Where? "]
cu = ["there","then",""]
tno = [" have an appointment... ", " can't. ","'m busy. "]
dno = ["'m busy... "," have plans already. ","'ll be out of town. "]


# In[6]:


#Brute force
def find_match(list1, list2):
    l = len(list2)
    for i in range(len(list1)-l + 1):
        if list1[i:i+l] == list2:
            return [i, i+l-1]
    return [0,0]
    
# def find_match(text, key): # two lists! (only for substring)
#     try:
#         a = text.index(key)
#     except ValueError:
#         return [0,0]
#     return [a, a+len(key)]


# In[7]:


# easy, success
def gen_simple(rows):
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
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? "+ y[0] + askt+ rept + t + "? "+ y[1] + askl + "|How about " + l + "? "+ y[2] + "|See you "+ fin +"!"
        example1 = example1.replace('|', '')
        label = [find_match(get_tokenize(example1)['input_ids'], get_tokenize(item)['input_ids'][1:-1]) for item in (a, d, t, l)]
        data.append((example1,label))        
    return pd.DataFrame(data, columns =['Text','Label'])#.drop_duplicates()
 


# In[8]:


temp = gen_simple(10)


# In[9]:


display(temp['Text'][0])
display(temp['Label'][0])


# In[10]:


# second time
def gen_t2(rows):
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
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? " + y[0] + askl + "|How about " + l + "? "+ y[1] + askt + rept[0] + t[0] + "? |Sorry, I" + dect + rept[1] + t[1] + "? "+y[2] + "|See you "+ fin +"!"
        example1 = example1.replace('|', '')
        label = [find_match(get_tokenize(example1)['input_ids'], get_tokenize(item)['input_ids'][1:-1]) for item in (a, d, t[1], l)]
        data.append((example1,label))        
    return pd.DataFrame(data, columns =['Text','Label'])#.drop_duplicates()


# In[11]:


temp = gen_t2(10)


# In[12]:


display(temp['Text'][0])
display(temp['Label'][0])


# In[ ]:





# In[13]:


# two locations (+ second time above)
def gen_t22l(rows):
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
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? " + y[0] + askl + "|I don't know. |How about " + l[0] + "? Or " + l[1] + "? "+ y[1] + "Let's do " + l[2] + ". " + askt + rept[0] + t[0] + "? |Sorry, I" + dect + rept[1] + t[1] + "? "+y[2] + "|See you "+ fin +"!"
        example1 = example1.replace('|', '')
        label = [find_match(get_tokenize(example1)['input_ids'], get_tokenize(item)['input_ids'][1:-1]) for item in (a, d, t[1], l[2])]
        data.append((example1,label))        
    return pd.DataFrame(data, columns =['Text','Label'])#.drop_duplicates()


# In[14]:


temp = gen_t22l(10)


# In[15]:


display(temp['Text'][0])
display(temp['Label'][0])


# In[ ]:





# In[16]:


# null: unsuccessful
def gen_un(rows):
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        d = random.sample(day, k=2)
        y = random.choice(yes)      
        askd = random.choice(qd)
        decd = random.choice(dno)
        example1 = g + askd + d[0] + "? " + "|Sorry, I" + decd + "|How about " + d[1] + "? "+ "|I'm busy on " + d[1] +" too. "+ "|That's fine, next time then. " + y 
        example1 = example1.replace('|', '')
        data.append((example1,[[0,0],[0,0],[0,0],[0,0]])) # fail        
    return pd.DataFrame(data, columns =['Text','Label'])#.drop_duplicates()


# In[17]:


temp = gen_un(10)


# In[18]:


display(temp['Text'][0])
display(temp['Label'][0])


# In[19]:


# easy, success
def gen_simple(rows):
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
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? "+ y[0] + askt+ rept + t + "? "+ y[1] + askl + "|How about " + l + "? "+ y[2] + "|See you "+ fin +"!"
        example1 = example1.replace('|', '')
        label = [find_match(get_tokenize(example1)['input_ids'], get_tokenize(item)['input_ids'][1:-1]) for item in (a, d, t, l)]
        data.append((example1,label))        
    return pd.DataFrame(data, columns =['Text','Label'])#.drop_duplicates()
 


# In[20]:


# simple, but no time
def gen_0t(rows):
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
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        example1 = g + askd + d + "? " + "|Yes. " + "|"+ aska + a + "? " + y[1] + askl + "|How about " + l + "? "+ y[2] + "|See you "+ fin +"!"
        example1 = example1.replace('|', '') 
        label = [find_match(get_tokenize(example1)['input_ids'], get_tokenize(item)['input_ids'][1:-1]) for item in (a, d, 'missing', l)]
        data.append((example1,label))        
    return pd.DataFrame(data, columns =['Text','Label'])


# In[21]:


temp = gen_0t(10)


# In[22]:


display(temp['Text'][0])
display(temp['Label'][0])


# In[ ]:





# In[307]:


df0t = gen_0t(500)
dft2 = gen_t2(500)
dft22l = gen_t22l(1000)
dfun = gen_un(500)
dfsimple = gen_simple(500)


# In[308]:


frames = [df0t, dft2, dft22l, dfun, dfsimple]
final3000 = pd.concat(frames)


# In[309]:


final3000.head()


# In[320]:


final3000s = shuffle(final3000)
final3000s.reset_index(inplace=True, drop=True)


# In[321]:


final3000s.head()


# In[322]:


final3000s.to_csv('final3000s.csv')


# In[ ]:





# In[23]:


df0t_s = gen_0t(50)
dft2_s = gen_t2(50)
dft22l_s = gen_t22l(100)
dfun_s = gen_un(50)
dfsimple_s = gen_simple(50)
frames_s = [df0t_s, dft2_s, dft22l_s, dfun_s, dfsimple_s]
test300 = pd.concat(frames_s)
test300s = shuffle(test300)
test300s.reset_index(inplace=True, drop=True)
test300s.to_csv('test300s.csv')


# In[ ]:





# In[ ]:


#"Sup! Sup. Do you want to bake on Saturday? I have to ask my parents. Sounds good. I can. Where do you want to go? I don't know. How about a coffee shop? Or your place? Sure! Let's do a coffee shop. What time should we meet? How about 9 pm? Are you free at midnight? Sorry, I'm busy. That's fine, let's do 9 pm then. Sure. See you on Saturday!"


# In[ ]:




ARCHIVE BELOW--
# In[134]:


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
        aska = random.choice(qa)
        askt = random.choice(qt)
        rept = random.choice(rt)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? "+ y[0] + askt+ rept + t + "? "+ y[1] + askl + "|How about " + l + "? "+ y[2] + "|See you "+ fin +"!"
        data.append((example1,a,d,t,l)) # only one of each       
    return pd.DataFrame(data, columns =['Text', 'Activity','Day','Time',"Location"]).drop_duplicates()
 


# In[135]:


data1 = gendat1(10)
data1['Text'][0]


# In[56]:


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
        aska = random.choice(qa)
        askt = random.choice(qt)
        rept = random.choices(rt, k=2)
        dect = random.choice(tno)
        askl = random.choice(ql)
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? " + y[0] + askl + "|How about " + l + "? "+ y[1] + askt + rept[0] + t[0] + "? |Sorry, I" + dect + rept[1] + t[1] + "? "+y[2] + "|See you "+ fin +"!"
        data.append((example1,a,d,t[1],l)) # always the second time
    return pd.DataFrame(data, columns =['Text', 'Activity','Day','Time',"Location"]).drop_duplicates() 
# didn't remove "on" because grammatical when reassemble


# In[110]:


secondt = gendatt(500)
secondt["Text"][0]


# In[ ]:





# In[63]:


# two locations (+ two times)
def gendatl(rows):
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
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        example1 = g + aska + a + " " + d + "? " + y[0] + askl + "|I don't know. |How about " + l[0] + "? Or " + l[1] + "? "+ y[1] + "Let's do " + l[2] + ". " + askt + rept[0] + t[0] + "? |Sorry, I" + dect + rept[1] + t[1] + "? "+y[2] + "|See you "+ fin +"!"
        data.append((example1,a,d,t[1],l[2])) # random choice location, always the second time
    return pd.DataFrame(data, columns =['Text', 'Activity','Day','Time',"Location"]).drop_duplicates()
# didn't remove "on" because grammatical when reassemble


# In[64]:


twolsecondt = gendatl(500)
twolsecondt["Text"][0]


# In[93]:


twolsecondt.describe()


# In[94]:


twolsecondt.to_csv('twolsecondt500.csv')


# In[ ]:





# In[105]:


# null: unsuccessful
def gendatun(rows):
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        d = random.sample(day, k=2)
        y = random.choice(yes)      
        askd = random.choice(qd)
        decd = random.choice(dno)
        example1 = g + askd + d[0] + "? " + "|Sorry, I" + decd + "|How about " + d[1] + "? "+ "|I'm busy on " + d[1] +" too. "+ "|That's fine, next time then. " + y 
        data.append((example1,[[0,0],[0,0],[0,0],[0,0]])) # only one of each 
        #data.append(example1)
    return pd.DataFrame(data, columns =['training_data', 'label']).drop_duplicates(subset='training_data')
    #return data


# In[109]:


notfree = gendatun(200)
notfree.to_csv('none200.csv', sep='\t')


# In[ ]:





# In[ ]:





# In[ ]:


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
 

