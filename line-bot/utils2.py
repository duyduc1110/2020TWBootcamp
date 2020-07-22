from config import train_args, question_list

import json
import os
import sys
from simpletransformers.question_answering import QuestionAnsweringModel


def CreateModel(model_type = 'bert', model_path = "outputs/"):
    
    model = QuestionAnsweringModel(
        model_type,
        model_path,
        args = train_args
    )
    
    return model

def get_to_predict(context, question_type):
    to_predict =  [
                    {
                        "context": context, 
                        "qas": [{"question": question_type[i], "id": str(i)}],
                    }
                        for i in range(len(question_type)) ]
    return to_predict

def get_qa(context, question_list, model=None):
    """
    Parameters
    ----------
    context : Str.
    question_list : List
    model :simpletransformer's model

    Returns
    -------
    First Ans list
    """
    if not model:
        model = CreateModel()
        
    to_predict = get_to_predict(context, question_list)
    answer = model.predict(to_predict)
    
    text = []
    prob = []
    for i in range(len(question_list)):
        temp_t = answer[0][i]['answer'][0]
        temp_p = answer[1][i]['probability'][0]
        
        text.append(temp_t)
        prob.append(temp_p)
        
    return text


if __name__ == "__main__":
    
    model = CreateModel()
    
    print("-------------------")
    print('hello worldn')
    msg = ["Hey. Are you free on Wednesday? Sorry, I'll be out of town. How about on Tuesday? I'm busy on on Tuesday too. That's fine, next time then. Sure."]
    
    # Making predictions using the model.
    
    to_predict = get_to_predict(msg[0], question_list)
    answer = model.predict(to_predict)
    print('-----------------------------------------------------\n')
    
    for i in range(len(question_list)):
        
        print(question_list[i])
        print('text:', answer[0][i]['answer'][:3])
        print('prob:', answer[1][i]['probability'][:3])
        print('---------------------------------------------------\n')
