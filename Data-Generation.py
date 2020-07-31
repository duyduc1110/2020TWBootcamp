
import random
import pandas as pd
import numpy as np
import pickle
from f_trans import gen2json


greet = ["|Hey, how are you doing? |I'm good, and you? |I'm fine, thanks. |",
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



greet = ["Hey, how are you doing? |I'm good, and you? |I'm fine, thanks. |", "Sup! |Sup. |", "Yo, what's up? |Nothing much. |", "Hey. ", "Heyo! "]
location = "the Japanese place, a coffee shop, Daan Park, the mall, the train station, your place, my place, the theme park, a club, a bar, the Italian restaurant".split(', ')
day = "today, tomorrow, on Sunday, on Monday, on Tuesday, on Wednesday, on Thursday, on Friday, on Saturday".split(', ')
time = "1 am; 2 am; 3 am; 4 am; 5 am; 6 am; 7 am; 8 am; 9 am; 10 am; 11 am; 12 pm; 1 pm; 2 pm; 3 pm; 4 pm; 5 pm; 6 pm; 7 pm; 8 pm; 9 pm; 10 pm; 11 pm; midnight, noon".split('; ')
#time = [x.strip() for x in "1 am; 2 am; 3 am; 4 am; 5 am; 6 am; 7 am; 8 am; 9 am; 10 am; 11 am; 12 pm; 1 pm; 2 pm; 3 pm; 4 pm; 5 pm; 6 pm; 7 pm; 8 pm; 9 pm; 10 pm; 11 pm".split('; ')]
activity = "catch up, do something, go to a party, go bowling, go somewhere, grab lunch, grab coffee, ice skating, hang out, see a game, see a concert, see a movie, see a play, watch a movie, go rafting, bake, go swimming".split(', ')
yes = "|Sure. , |Ok. , |Sure! , |OK! , |Great. , |Sounds good. ".split(', ')


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
 



#print(len(data1), data1)




# second time
def gendatt(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
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
        
        context = g + aska + a + " " + d + "? " + y[0] + askl + "|How about " + l + "? "+ y[1] + askt + rept[0] + t[0] + "? |Sorry, I can't. " + rept[1] + t[1] + "? "+y[2]+ "|See you then!"
        label = [{'text': text, 'answer_start': context.index(text)} for text in (a,d,t[1],l)]
        
        data.append([context,label])
        
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data
    #return pd.DataFrame(data, columns =['Text', 'Activity','Day','Time',"Location"]) # always the second time
# didn't remove "on" because grammatical when reassemble



#secondt = gendatt(500).drop_duplicates()
#secondt["Text"][0]
#secondt.describe()
#secondt.to_csv('secondt.csv')





# more complex (location)
def gendatl(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
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
        
        context = g + aska + a + " " + d + "? " + y[0] + askl + "|I don't know. |How about " + l + "? "+ y[1] + askt + rept[0] + t[0] + "? |Sorry, I can't. " + rept[1] + t[1] + "? "+y[2]+ "|See you then!"
        label = [{'text': text, 'answer_start': context.index(text)} for text in (a,d,t[1],l)]
        
        data.append([context,label])
        
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data
    #return pd.DataFrame(data, columns =['Text', 'Activity','Day','Time',"Location"]) # always the second time
# didn't remove "on" because grammatical when reassemble



 

# two locations (+ two times) 
def gendatll(rows):
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
        cu_temp.append(d)
        fin = random.choice(cu_temp)
        context = g + aska + a + " " + d + "? " + y[0] + askl + "|I don't know. |How about " + l[0] + "? Or " + l[1] + "? "+ y[1] + "Let's do " + l[2] + ". " + askt + rept[0] + t[0] + "? |Sorry, I" + dect + rept[1] + t[1] + "? "+y[2] + "|See you "+ fin +"!"
        #data.append((example1,a,d,t[1],l[2])) # random choice location, always the second time
        
        label = [{'text': text, 'answer_start': context.index(text)} for text in (a,d,t[1],l[2])]
        data.append([context,label])
        
        
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data
    
# null: unsuccessful
def gendatun(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    for _ in range(rows):
        g = random.choice(greet)
        d = random.sample(day, k=2)
        y = random.choice(yes)      
        askd = random.choice(qd)
        decd = random.choice(dno)
        context = g + askd + d[0] + "? " + "|Sorry, I" + decd + "|How about " + d[1] + "? "+ "|I'm busy on " + d[1] +" too. "+ "|That's fine, next time then. " + y
        label = [{'text': text, 'answer_start': context.index(text)} for text in ('','','','')]
        data.append([context,label])
    data = np.array(data)
    data = {"train_data" : list(data[:,0]),  "label" : list(data[:,1])}
    return data
    #return pd.DataFrame(data, columns =['training_data', 'label']).drop_duplicates(subset='training_data')
    
    
    
    
    
import sys

if __name__ == '__main__':
    t_size = int(sys.argv[1])
    l_size = int(sys.argv[2])
    ll_size = int(sys.argv[3])
    un_size = int(sys.argv[4])
    outpath = sys.argv[5]

    data_t = gendatt(t_size)
    data_l = gendatl(l_size)
    data_ll = gendatl(ll_size)
    data_un = gendatun(un_size)
    data = dict()
    
    
    for key in data_t.keys():
        data[key] = data_t[key]+data_l[key]+data_ll[key]+data_un[key]
    
    """
    with open(outpath, 'wb') as f:
        pickle.dump(data, f)

    """
    gen2json(data, outpath)

