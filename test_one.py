

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
model = QuestionAnsweringModel(
    "bert",
    #"outputs/",
    "Bert_QA2/",
    args = train_args
)
#rain_path = sys.argv[1]

# Train the model
#model.train_model(train_path)

# Evaluate the model. (Being lazy and evaluating on the train data itself)
#result, text = model.eval_model("data/train.json")
#result, text = model.eval_model(train_path)
#with open('result.json','w') as f:
#    json.dump(result, f)
#with open('text.json', 'w') as f:
#    json.dump(text, f)
#print(result)
#print(text)

print("-------------------")
print('hello world2')

# DST-test format (?)
# msg = ["Let's have lunch tomorrow.", "where should we meet?", "How about xinyi?", "Sure.", "Can we meet the day after tomorrow?", "Sure."]
# m = ["Let's have lunch tomorrow.", 'Sure', "where should we meet?", "How about xinyi?", "Sure.", "Can we meet two days later?", "Sorry, I cant go."]
# string =  ""
# for i in m:
#     string += ' ' + i 

one_str = "Hey. Are you free on Tuesday? Yes. Do you want to go rock climbing? Sure! Where should we meet? How about the theme park? Why not Daan Park? Or Elephant Mountain? I've never been to Daan Park. Let's go there instead. OK. See you there!"
# Making predictions using the model.
question_type = ['what are we going to do?', 'what day?', 'what time?', 'where are we going?' ]

def get_to_predict(num):
    to_predict =  [
    {
        "context": one_str, 
        "qas": [{"question": question_type[i], "id": str(i)}],
    }
    for i in range(num)
    ]
    return to_predict

to_predict = get_to_predict(len(question_type))
answer = model.predict(to_predict)
print('-----------------------------------------------------\n')

for i in range(len(question_type)):
    
    print(question_type[i])
    print('text:', answer[0][i]['answer'][:3])
    print('prob:', answer[1][i]['probability'][:3])
    print('---------------------------------------------------\n')
