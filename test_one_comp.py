
train_args = {
    'learning_rate': 3e-5,
    'num_train_epochs': 1,
    'max_seq_length': 384,
    'doc_stride': 128,
    'overwrite_output_dir': True,
    'reprocess_input_data': True,
    'train_batch_size': 2,
    'gradient_accumulation_steps': 8,
    "attention_probs_dropout_prob": 0.1,
  "finetuning_task": "squad2",
  "hidden_act": "gelu",
  "hidden_dropout_prob": 0.1,
  "hidden_size": 1024,
  "initializer_range": 0.02,
  "intermediate_size": 4096,
  "language": "english",
  "layer_norm_eps": 1e-12,
  "max_position_embeddings": 512,
  "model_type": "bert",
  "name": "Bert",
  "num_attention_heads": 16,
  "num_hidden_layers": 24,
  "output_past": True,
  "pad_token_id": 0,
  "type_vocab_size": 2,
  "vocab_size": 30522
}

import json
import os
import sys
from simpletransformers.question_answering import QuestionAnsweringModel

#!/usr/bin/env python
#coding=utf-8

# Create the QuestionAnsweringModel
model1 = QuestionAnsweringModel(
    "bert",
    "outputs/",
    args = train_args
)

model2 = QuestionAnsweringModel(
    "bert",
    "Bert_QA2/",
    args = train_args
)

print("-------------------")
print('hello worldj')


# "Yo, what's up? Nothing much. Do you want to see a musical on Friday? Sounds good. Where do you want to go? We can go to a casino? Ok. Wait! Sorry! I forgot. I can't on Friday, I have to babysit my cousin. Sad... Aight, let me know when you're free. "

some = ["Yo, what's up? Nothing much. Do you want to see a musical on Friday? Sounds good. Where do you want to go? We can go to a casino? Ok. Wait! Sorry! I forgot. I can't on Friday, I have to babysit my cousin. Sad... Aight, let me know when you're free. ",
"Hey! Want to see a concert next Saturday? OK! Where should we meet? School? Sure. Wait! I forgot. I can't next Saturday, I have to babysit my cousin. Sad... sorry. Oh... Ok then. Next time."
#, "Sup! Want to go bowling? When? Sunday? Sure! Wait, never mind. I won't be here on Sunday. Is Saturday ok? Yes, that's fine. Let's do 5 pm then. At the bowling alley? Yea. OK. Excited!"
 ]

question_type = ['what are we going to do?', 'what day?', 'what time?', 'where are we going?' ]
num_q = len(question_type)

def get_to_predict(num):
    to_predict =  [
    {
        "context": one_str, 
        "qas": [{"question": question_type[i], "id": str(i)}],
    }
    for i in range(num)
    ]
    return to_predict

for j in range(len(some)): #range(1): 
    #one_str = "Hi March! I’m Jamie. Would you like to meet up and have a chat sometime? Probably easier (and more casual) to get to know each other and ask some questions. Look forward to meeting you! Hi Jamie, That would be nice! I’ll be around the campus next Thursday. How about meeting up at some café on the campus next Thursday afternoon. I’m currently doing this bootcamp program (10am-6pm). Think my only free day would be Wednesday next week. Would that work? If not, the week following may be better? (I’ll be in Kaohsiung next weekend and in currently in Hualien) Sorry about that. Both next Wednesday and the week following work for me, except for 8/12. We can meet up at a time that we both feel comfortable. You don’t have too rush back from Hualien or to Kaohsiung. That would be too exhausting. OK, great. I’ll let you know after this weekend? Sure! Cheers. Hey March! Would you prefer to meet in the afternoon or for lunch Wednesday? Would around Nanjing Fuxing work? Let’s meet for lunch tomorrow. And yes, around Nanjing Fuxing works. Do you have any restaurant on mind? If not, I know a brunch restaurant near Nanjing Fuxing. Sure, sounds good! Let me know. The brunch restaurant I was talking about. do you think it'll be really busy? It’s probably really busy during summer vacation. We might have to wait about 10 minutes before entering the restaurant. Alright. No problem. Just saw this that’s why It says “usually no wait”. I guess we’ll be fine. wait sorry, i just realized i have a meeting 11-11:30, will likely be able to get there at 12. is that fine with you? sure, 12 then. thanks!"
    #one_str = "Hey, long time no talk. Yea, how’ve you been? Good. Do you want to grab coffee on Saturday? Okay. Where should we go? How about your place or the theme park? Let's not go to your place. OK! What time? Let's do 12 pm? Sure! Sounds good. "
    one_str = some[j]
    to_predict = get_to_predict(num_q)
    answer1 = model1.predict(to_predict)
    answer2 = model2.predict(to_predict)
    print('-----------------------------------------------------\n')

    for i in range(num_q):
        
        print(question_type[i])
        print('V1---------------------------------------------------')
        print('text:', answer1[0][i]['answer'][:3])
        print('prob:', answer1[1][i]['probability'][:3])
        print('\nV2---------------------------------------------------')
        print('text:', answer2[0][i]['answer'][:3])
        print('prob:', answer2[1][i]['probability'][:3])
        print('-')
    


    
