#!/usr/bin/env python
# coding: utf-8
# %%
import random
import pandas as pd
import numpy as np
import copy
from sklearn.utils import shuffle
import pickle
from f_trans import gen2json_DST
import sys


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

yes = ['Sure. ', 'Ok. ', 'Sure! ', 'OK! ', 'Great. ', 'Sounds good. ', 'Of course', 'Good']
qa = ["Would you want to ", "Do you want to ", "Let's "]
create_event = ["Would you want to ", "Do you want to ", "Let's "]

qd = ["Are you busy ", "You free ", "Are you free ", "What day? ", "When should we meet? ", "What time should we meet? ","When? ", "What time?" ]
rd = ["How about ", "Let's do ", "You free ", "Are you free at ", 'Why not ']

ql = ["Where should we go? ","Where do you want to go? ","Where should we meet? ","Where? "]
rl = ["Let's do ", "I prefer ", 'Why not ']

cu = [" there"," then"]
refuse = ["Sorry, I", "No..., I"]
tno = [" have an appointment. ", " can't. ","'m busy. "]
dno = ["'m busy... "," have plans already. ","'ll be out of town. "]
how_about = ["How about ",  'Why not', "Why don't we "]

def chat_to_sentance(chat):
    return list(filter(None, chat.split('|')))

# null: unsuccessful
def Gen_Classfier_Data(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    train_data_classifier = []
    train_data_YN_classifier = []
    train_data_QA = []
    Question_dict = {'Activity' : 'what are we going to do?', 'Day' : 'what day?', 'Place' : 'where are we going?', 'Logic' : 'Yes or No?'}
    for _ in range(rows):
        get_greet = random.choice(greet)
        get_activity = random.choice(activity)
        get_day = random.choice(day)
        get_day_ = random.sample(day, k=2)
        get_day_location = random.sample(location, k=2)
        get_day_location.append(random.choice(get_day_location))
        get_yes = random.choice(yes)
        get_location = random.choice(location)
        get_quest_activity = random.choice(qa)
        get_how_about = 'How about '
        get_quest_day = random.choice(qd)
        get_quest_location = random.choice(ql)
        get_respon_day = random.choice(rd)
        get_respon_location = random.choice(rl)
        get_tno = random.choice(tno)
        get_dno = random.choice(dno)
        get_refuse = random.choice(refuse)
        
        cu_temp = copy.deepcopy(cu)
        cu_temp.append(" " + get_day)
        fin = random.choice(cu_temp)

      # C  A  D  P  L
      #[0, 0, 0, 0, 0]
        train_data_classifier.append([get_greet, [0, 0, 0, 0, 0]])
      #[1, 1, 0, 0, 0]
        train_data_classifier.append([get_quest_activity + get_activity + '?', [1, 1, 0, 0, 0]])
        train_data_QA.append([get_quest_activity + get_activity + '?', Question_dict['Activity'], get_activity])
      #[0, 1, 0, 0, 0]
        train_data_classifier.append([get_how_about + get_activity + '?', [0, 1, 0, 0, 0]])
        train_data_QA.append([get_how_about + get_activity + '?', Question_dict['Activity'], get_activity])
      #[0, 0, 1, 0, 0]
        train_data_classifier.append([get_quest_day + get_day + '?', [0, 0, 1, 0, 0]])
        train_data_QA.append([get_quest_day + get_day + '?', Question_dict['Day'], get_day])
      #[0, 0, 1, 0, 0]
        train_data_classifier.append([get_respon_day + get_day + '?', [0, 0, 1, 0, 0]])
        train_data_QA.append([get_quest_day + get_day + '?', Question_dict['Day'], get_day])
      #[0, 0, 0, 1, 0]
        train_data_classifier.append([get_quest_location + get_location + '?', [0, 0, 0, 1, 0]])
        train_data_QA.append([get_quest_location + get_location + '?', Question_dict['Place'], get_location])
      #[0, 0, 0, 1, 0]
        train_data_classifier.append([get_respon_location + get_location + '?', [0, 0, 0, 1, 0]])
        train_data_QA.append([get_quest_location + get_location + '?', Question_dict['Place'], get_location])
      #[1, 1, 1, 0, 0]
        train_data_classifier.append([get_quest_activity + get_activity + ' ' + get_day + '?', [1, 1, 1, 0, 0]])
        train_data_QA.append([get_quest_activity + get_activity + ' ' + get_day + '?', Question_dict['Activity'], get_activity])
        train_data_QA.append([get_quest_activity + get_activity + ' ' + get_day + '?', Question_dict['Day'], get_day])
      #[1, 1, 0, 1, 0]
        train_data_classifier.append([get_quest_activity + get_activity + ' ' +  get_location + '?', [1, 1, 0, 1, 0]])
        train_data_QA.append([get_quest_activity + get_activity + ' ' +  get_location + '?', Question_dict['Activity'], get_activity])
        train_data_QA.append([get_quest_activity + get_activity + ' ' +  get_location + '?', Question_dict['Place'], get_location])
      #[1, 1, 1, 1, 0]
        train_data_classifier.append([get_quest_activity + get_activity + ' ' +  get_location + ' ' +  get_day + '?', [1, 1, 1, 1, 0]])
        train_data_QA.append([get_quest_activity + get_activity + ' ' +  get_location + ' ' +  get_day + '?', Question_dict['Activity'], get_activity])
        train_data_QA.append([get_quest_activity + get_activity + ' ' +  get_location + ' ' +  get_day + '?', Question_dict['Day'], get_day])
        train_data_QA.append([get_quest_activity + get_activity + ' ' +  get_location + ' ' +  get_day + '?', Question_dict['Place'], get_location])
      #[0, 0, 0, 0, 1]
        train_data_classifier.append([get_yes, [0, 0, 0, 0, 1]])
        train_data_YN_classifier.append([get_yes, 1])
        train_data_QA.append([get_yes, Question_dict['Logic'], 'Yes'])
      #[0, 0, 0, 0, 1]
        train_data_classifier.append([get_refuse + get_tno, [0, 0, 0, 0, 1]])
        train_data_YN_classifier.append([get_refuse + get_tno, 0])
        train_data_QA.append([get_refuse + get_tno, Question_dict['Logic'], 'No'])

        train_data_classifier.append([get_refuse + get_dno, [0, 0, 0, 0, 1]])
        train_data_YN_classifier.append([get_refuse + get_dno, 0])
        train_data_QA.append([get_refuse + get_dno, Question_dict['Logic'], 'No'])

    # shuffle the dataframe then split into trainset, testset                                                                 
    Domain_classifier = shuffle(pd.DataFrame(train_data_classifier, columns = ['text', 'labels']))
    YN_classifier = shuffle(pd.DataFrame(train_data_YN_classifier, columns = ['text', 'labels']))
    df_QA = pd.DataFrame(train_data_QA, columns = ['Text', 'Question', 'Label'])

    # Drop Duplicates
    Domain_classifier.drop_duplicates(subset ="text", inplace = True) 
    #YN_classifier.drop_duplicates(subset ="text", inplace = True) 

    # Split it into training data, test data
    row_end_for_Domain_training = int(0.8*Domain_classifier.shape[0])
    row_end_for_YN_training = int(0.8*YN_classifier.shape[0])

    # 80% training data, 20% test data
    # Domain lassifier
    Domain_classifier.iloc[:row_end_for_Domain_training].to_csv('Domain_classifier_train.csv', index=False)
    Domain_classifier.iloc[row_end_for_Domain_training:].to_csv('Domain_classifier_test.csv', index=False)
    # Yes No 
    YN_classifier.iloc[:row_end_for_YN_training].to_csv('YN_classifier_train.csv', index=False)
    YN_classifier.iloc[row_end_for_YN_training:].to_csv('YN_classifier_test.csv', index=False)

    return data

# %%
import sys

if __name__ == '__main__':
    Gen_Classfier_Data(10000)
    
