from config import train_args, question_type

import json
import os
import sys
from simpletransformers.question_answering import QuestionAnsweringModel

#!/usr/bin/env python
#coding=utf-8

# Create the QuestionAnsweringModel

def CreateModel(model_type = 'bert', model_path = "outputs/"):
    
    model = QuestionAnsweringModel(
        model_type,
        model_path,
        args = train_args
    )
    
    return model

def get_to_predict(num):
    to_predict =  [
                    {
                        "context": msg[0], 
                        "qas": [{"question": question_type[i], "id": str(i)}],
                    }
                        for i in range(num) ]
    return to_predict

if __name__ == "__main__":
    
    model = CreateModel()
    
    print("-------------------")
    print('hello worldn')
    msg = ["Hey. Are you free on Wednesday? Sorry, I'll be out of town. How about on Tuesday? I'm busy on on Tuesday too. That's fine, next time then. Sure."]
    # Making predictions using the model.
    

    
    to_predict = get_to_predict(len(question_type))
    answer = model.predict(to_predict)
    print('-----------------------------------------------------\n')
    
    for i in range(len(question_type)):
        
        print(question_type[i])
        print('text:', answer[0][i]['answer'][:3])
        print('prob:', answer[1][i]['probability'][:3])
        print('---------------------------------------------------\n')
