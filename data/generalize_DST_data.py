#!/usr/bin/env python
# coding: utf-8
# %%
import random
import pandas as pd
import numpy as np
import copy
from sklearn.utils import shuffle
import pickle
#from f_trans import gen2json_DST
import sys


##### Redefine the word #####

##### Opening of a Question #####
create_event = ["Would you", "Do you want", "Let's ", "Want to", "Shall we", 'Let us']# + ["Let's grab lunch your place on Sunday?"]
opening_word = ["Are you busy ", "You free", "Are you free ", "How about ", "You free ", "Are you free at", 'Why not', 'Why not']

# What, Where, When
opening_word_when = ["When should we meet", "What day should we meet", "What time should we meet", 'When ', 'what time', 'what day']
opening_word_where = ["Where we", "Where do you want", "Where we meet", 'Where', 'go where', 'What place', 'What location', 'Where should']

# for the activity, place
useful_data = pd.read_csv('DST_data.csv')

##### Activity #####
to_Buy = useful_data['Food'].values.tolist() + useful_data['Drink'].values.tolist() + useful_data['Clothes'].values.tolist() + useful_data['Products'].values.tolist()
activity = ['go buy ' + item for item in to_Buy] + ['see ' + item for item in useful_data['Movie'].values.tolist()] + ['go get ' + item for item in to_Buy]
activity += ['catch up',
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


##### Day #####
day = ['today',
 'tomorrow',
 'the day after tomorrow',
 'on Sunday',
 'on Monday',
 'on Tuesday',
 'on Wednesday',
 'on Thursday',
 'on Friday',
 'on Saturday']

day_unit = ['day', 'month', ' week', 'year']
day_list = [str(i+1) + ' ' + unit for unit in day_unit for i in range(10)]
day_list += [i + ' ' + unit for unit in day_unit for i in ['one, two, three, four, five, six, seven, eihgt, nine, ten, eleven, twelve']]

delay_head = [ 'later', 'after']

delay_behind = [ 'delay for ',
'late for',
'postpone',
'move to',
'hold up for',
'suspend',
'defer'
]

early_head = [ 'pirior.',
'before.',
'earlier.',
'ahead.',
'in advance.',
'early',
'advance.'
]

early_behind = [
  'to advance'
]


delay = [d + ' ' + item  for item in delay_head for d in day_list] + [item + ' ' + d  for item in delay_behind for d in day_list]
early = [d + ' ' + item  for item in early_head for d in day_list] + [item + ' ' + d  for item in early_behind for d in day_list]
change = day


##### Place #####
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
 "school",
 'train station']
 
location += useful_data['City'].values.tolist() + useful_data['City'].values.tolist()

place = ['go ' + item for item in location]


##### Logic #####

refuse = ["Sorry", "No..., I", 'No. ', 'Sorry. ','can\'t', 'don\'t', 'Nah ', 'No.'] + 'nope/not/reject/no/no way/of course not/'.split('/') 
tno = [" I have an appointment. ", "I can't. ","I'm busy. ", "I'm busy... "," I have plans already. "," I'll be out of town.", 'I dont have time']

no = [refuse_ + ' ' + tno_ for refuse_ in refuse for tno_ in tno]
yes = ['Sure. ', 'Ok. ', 'Sure! ', 'OK! ', 'Great. ', 'Sounds good. ', 'Of course', 'Good', 'Yes', 'Nice', 'Yeah...'] + 'exactly/That\'s right/True dat/OK/agree/yeah/can\'t wait/Yep/Yup/okay/k/alright/of course'.split('/')

##### Meaningless, from machine translation dataset (Stanford NLP) -> negative sampling #####
with open("meaningless_sentence.txt", "r") as f:
    meaningless = f.read().split('\n')

greet = ['Hey, how are you doing?',
 'Sup!',
 "Yo, what's up?",
 'Hey! ']

greet_response = ['I\'m good, and you?','I\'m fine, thanks.', 'Sup.', 'Nothing much.', 'Hey.']

meaningless += greet + greet_response

##### End of Generating data #####



# In general data to used will be save in this dict (key, value) = (string, list)
Sentence_dict = {'create event':create_event, 'other opening': opening_word, 'opening where': opening_word_where, 'opening when': opening_word_when, 'activity':activity, 'delay':delay, 'early': early, 'change': change, 'place': place, 'yes': yes, 'no': no, 'meaningless': meaningless}



# Get Sample from dict
def get_sample_component():
  create_event_ = random.choice(Sentence_dict['create event'])
  other_opening_ = random.choice(Sentence_dict['other opening'])
  opening＿where_ = random.choice(Sentence_dict['opening where'])
  opening_when_ = random.choice(Sentence_dict['opening when'])
  activity_ = random.choice(Sentence_dict['activity'])
  delay_ = random.choice(Sentence_dict['delay'])
  early_ = random.choice(Sentence_dict['early'])
  change_ = random.choice(Sentence_dict['change'])
  place_ = random.choice(Sentence_dict['place'])
  yes_ = random.choice(Sentence_dict['yes'])
  no_ = random.choice(Sentence_dict['no'])
  meaningless_ = random.choice(Sentence_dict['meaningless'])

  return create_event_ , other_opening_, opening＿where_, opening＿when_, activity_, delay_, early_, change_, place_ , yes_ , no_ , meaningless_ 

def get_opening_label():
  # C  A  D  P  L
  create_event_label = [1, 0, 0, 0, 0]
  other_opening_label = [0, 0, 0, 0, 0]
  opening＿where_label = [0, 0, 0, 1, 0]
  opening＿when_label = [0, 0, 1, 0, 0]
  yes_label = [0, 0, 0, 0, 1]
  no_label = [0, 0, 0, 0, 1]

  opening_label_list = [create_event_label, other_opening_label, opening＿where_label, opening＿when_label, yes_label, no_label]

  return opening_label_list

   

# Build comb of activity, place, Day
# return with [(component, label)]
def construct_end_component(activity_, delay_, early_, change_, place_): 
  to_sample = [activity_, [delay_, early_, change_], place_]
 # C  A  D  P  L
  build_list = [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 1, 1, 1, 0]]

  end_component_list = []
  end_component_label_list = []

  for build in build_list:
    sub_list = []
    sub_build = [0, 0, 0, 0, 0]
    if build[1]:
      sub_list.append(to_sample[0])
      sub_build[1] = 1

    if build[3]:
      sub_list.append(to_sample[2])
      sub_build[3] = 1

    if build[2]:
      return_list = []
      sub_build[2] = 1
      for item in to_sample[1]:
        return_list.append(sub_list + [item])
        end_component_label_list.append(sub_build)
      sub_list = return_list
    
    else:
      end_component_label_list.append(sub_build)
    end_component_list.append(sub_list)

  temp_list = []
  for i in range(len(end_component_list)):
    # Shuffle first
    random.shuffle(end_component_list[i])

    # contain day
    if len(end_component_list[i]) == 3:
      for item in end_component_list[i]:
        string = ''
        for sub_item in item:
          string += sub_item + ' '
        temp_list.append(string)

    # Not contain delay
    else:
      string = ''
      for n in end_component_list[i]:
        string += n + ' '
      temp_list.append(string)
  end_component_list = temp_list

  # format like ('go buy Kool-Aid go Garland to advance 1  week ', [0, 1, 1, 1, 0])
  return list(zip(end_component_list, end_component_label_list))

# null: unsuccessful
def Gen_Classfier_Data(rows):
    if rows == 0: return  {"train_data" : [],  "label" : []}
    data = []
    train_data_classifier = []
    train_data_YN_classifier = []
    train_data_Day_classifier = []
    train_data_QA = []
    Question_dict = {'Activity' : 'what are we going to do?', 'Day' : 'what day?', 'Place' : 'where are we going?', 'Logic' : 'Yes or No?'}
    
    for _ in range(rows):
      # Sample from data
      create_event_ , other_opening_, opening_where_, opening_when_, activity_, delay_, early_, change_, place_ , yes_ , no_ , meaningless_  = get_sample_component()
      
      # format like ('go buy Kool-Aid go Garland to advance 1  week ', [0, 1, 1, 1, 0]) 
      end_component = construct_end_component(activity_, delay_, early_, change_, place_)
      
      # Get the label with the opening
      opening_label_list = get_opening_label()

      # make opening to [(text, label)..] pair to open_component
      open_component = list(zip([create_event_ , other_opening_, opening_where_, opening_when_, yes_ , no_], opening_label_list))

      # meaningless data
      train_data_classifier.append([meaningless_, [0, 0, 0, 0, 0]])

      # C  A  D  P  L
      # Make combination
      for open_text, open_label in open_component:
        # Add sentence when only 
        if open_text == opening_where_:
          train_data_classifier.append([open_text + ' ?', [0, 0, 0, 1, 0]])
        elif open_text == opening_when_:
          train_data_classifier.append([open_text + ' ?', [0, 0, 1, 0, 0]])
          train_data_Day_classifier.append([open_text + ' ?', 2])

        for end_text, end_label in end_component:  
          # if yes/no, no Q
          if yes_ in open_text or no_ in open_text: 
            train_text = open_text + ' ' + end_text
          else:
            train_text = open_text + ' ' + end_text + ' ?'

          train_label = []
          for index in range(len(open_label)):
            train_label.append(open_label[index] or end_label[index])

          # append to Day classifier
          # 0 -> delay, 1 -> early, 2 -> change
          if delay_ in end_text:
            train_data_Day_classifier.append([train_text, 0])
            # append to data classifier
            train_data_classifier.append([train_text, train_label])
            continue
          
          if early_ in end_text:
            train_data_Day_classifier.append([train_text, 1])
            # append to data classifier
            train_data_classifier.append([train_text, train_label])
            continue

          if change_ in end_text:
            train_data_Day_classifier.append([train_text, 2])
            # append to data classifier
            train_data_classifier.append([train_text, train_label])
            continue

          # append to YN classifier
          # 1 -> yes, 0 -> no
          if open_text == yes_:
            train_data_YN_classifier.append([train_text, 1])
            # append to data classifier
            train_data_classifier.append([train_text, train_label])            
            continue

          if open_text == no_:
            train_data_YN_classifier.append([train_text, 0])
            # append to data classifier
            train_data_classifier.append([train_text, train_label])
            continue

          # if non of the above, still append to data classifier
          train_data_classifier.append([train_text, train_label])

    # shuffle the dataframe then split into trainset, testset                                                                 
    Domain_classifier = shuffle(pd.DataFrame(train_data_classifier, columns = ['text', 'labels']))
    YN_classifier = shuffle(pd.DataFrame(train_data_YN_classifier, columns = ['text', 'labels']))
    Day_classifier = shuffle(pd.DataFrame(train_data_Day_classifier, columns = ['text', 'labels']))

    # Drop Duplicates
    Domain_classifier.drop_duplicates(subset ="text", inplace = True) 
    YN_classifier.drop_duplicates(subset ="text", inplace = True) 
    Day_classifier.drop_duplicates(subset ="text", inplace = True) 

    # Split it into training data, test data
    row_end_for_Domain_training = int(0.8*Domain_classifier.shape[0])
    row_end_for_YN_training = int(0.8*YN_classifier.shape[0])
    row_end_for_Day_training = int(0.8*Day_classifier.shape[0])
    print(row_end_for_Domain_training, row_end_for_YN_training, row_end_for_Day_training)

    # 80% training data, 20% test data
    # Domain lassifier
    #Domain_classifier.iloc[:row_end_for_Domain_training].to_csv('Domain_classifier_train.csv', index=False)
    #Domain_classifier.iloc[row_end_for_Domain_training:].to_csv('Domain_classifier_test.csv', index=False)
    # Yes No 
    #YN_classifier.iloc[:row_end_for_YN_training].to_csv('YN_classifier_train.csv', index=False)
    #YN_classifier.iloc[row_end_for_YN_training:].to_csv('YN_classifier_test.csv', index=False)
    # Day 
    Day_classifier.iloc[:row_end_for_Day_training].to_csv('Day_classifier_train.csv', index=False)
    Day_classifier.iloc[row_end_for_Day_training:].to_csv('Day_classifier_test.csv', index=False)



if __name__ == '__main__':
  #300
  Gen_Classfier_Data(1000)
  print('done')


