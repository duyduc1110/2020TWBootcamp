
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

import time

#!/usr/bin/env python
#coding=utf-8

# Create the QuestionAnsweringModel
model = QuestionAnsweringModel(
    "bert",
    #"outputs/",
    "Bert_QA2/",
    args = train_args
)

"""
train_path = sys.argv[1]

Evaluate the model. (Being lazy and evaluating on the train data itself)
result, text = model.eval_model("data/train.json")
result, text = model.eval_model(train_path)
with open('result.json','w') as f:
   json.dump(result, f)
with open('text.json', 'w') as f:
   json.dump(text, f)
print(result)
print(text)
"""

print("-------------------")
print('hello world')

#one_str = "Hey. Are you free Tuesday afternoon? What time? 2 pm? Yup! Do you want to go rock climbing? Sure! Where should we meet? How about the theme park? Why not Daan Park? Or Elephant Mountain? I've never been to Daan Park. Let's go there instead. OK. See you there!"
one_str = "Hey, long time no talk. Yea, how've you been? Good. Let's watch a movie on Wednesday? Ok. Where do you want to go? We can go to a coffee shop? OK! Wait! Sorry! I forgot. I can't on Wednesday. I have to babysit my cousin. Okay, have fun!"
question_type = ['what are we going to do?', 'what day?', 'what time?', 'where are we going?' ]

num_q = len(question_type)

# Making predictions using the model.
def get_to_predict(num):
    to_predict =  [
    {
        "context": one_str, 
        "qas": [{"question": question_type[i], "id": str(i)}],
    }
    for i in range(num)
    ]
    return to_predict

to_predict = get_to_predict(num_q)
answer = model.predict(to_predict)

print('-----------------------------------------------------\n')
print(one_str,'\n')

# for i in range(num_q):
    
#     print(question_type[i])
#     print('text:', answer[0][i]['answer'][:3])
#     print('prob:', answer[1][i]['probability'][:3])
#     print('---------------------------------------------------\n')

# init_str = [answer[0][0]['answer'][0], answer[0][1]['answer'][0], answer[0][2]['answer'][0], answer[0][3]['answer'][0]] #output = [answer[0][i]['answer'][0] for i in range(num_q)]
init_str = {'Activity': answer[0][0]['answer'][0], 'Day': answer[0][1]['answer'][0], 'Time': answer[0][2]['answer'][0], 'Location' : answer[0][3]['answer'][0]}
print(init_str)

def man_output(output):
    if not output['Day'] and not output['Time'] or not output['Activity']:
        print('No event was created.')
        return 
    else:
        print('Please confirm the event below: ')
        #print('Will you', output['Activity'],'at', output['Location'], 'on', output['Day'],'at', output['Time'], '?')
        final_str = 'Will you ' + output['Activity']
    if output['Location']:
        final_str += ' at ' + output['Location']
    if output['Day']:
        if output['Day'] in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
            final_str += ' on '
        final_str += output['Day']
    if output['Time']:
        final_str += ' at ' + output['Time']
    print(final_str + '?')

man_output(init_str)
