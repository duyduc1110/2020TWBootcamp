
from simpletransformers.classification import MultiLabelClassificationModel
from simpletransformers.classification import ClassificationModel
from simpletransformers.question_answering import QuestionAnsweringModel

import pandas as pd
import logging


'''
    Domain_classifier, MultiLabel classifier
    YN_classifier, binary classifier
    QA_model, QA based model
    chat_history is a list of string, ['fudwfjls', 'fkdsklf']
'''

def DST_predict(Domain_classifier, YN_classifier, QA_model, chat_history, Threshold = 0.5):

    Domain = ['Create_event', 'Activity', 'Day', 'Place', 'Logic']
    Question_dict = {'Activity' : 'what are we going to do?', 'Day' : 'what day?', 'Place' : 'where are we going?'}

    sentance_to_analyse = []

    for chats in chat_history:
        predictions, raw_outputs = Domain_classifier.predict([chats])
        '''
            raw_outputs = [[0.9, 0.08...]]
        '''
        # Check the raw_outputs of a sentance is qualified to be used
        chat_DST = []
        for i in range(len(raw_outputs[0])):

            # Over the Threshold then used.
            if raw_outputs[0][i] > Threshold:
                # Get the logic, 0 for Negative, 1 for Positive
                if Domain[i] == 'Logic':
                    predictions, raw_outputs = YN_classifier.predict([chats])
                    chat_DST.append((Domain[i], predictions[0]))
                    #sentance_to_analyse += [(chats, Domain[i], predictions[0])]

                # Get the value of Creating event
                elif Domain[i] == 'Create_event':
                    chat_DST.append((Domain[i], 'create event'))
                    #sentance_to_analyse += [(chats, Domain[i], 'create event')]

                # Else Go to QA model for searching the Value of it.
                else :
                    to_predict = [{
                    "context": chats,
                    "qas": [{"question":Question_dict[Domain[i]] , "id": "0"}]}]
                    chat_DST.append((Domain[i], QA_model.predict(to_predict)[0][0]['answer'][0]))
                    #sentance_to_analyse += [(chats, Domain[i], QA_model.predict(to_predict)[0][0]['answer'][0])]

        sentance_to_analyse += [(chats, chat_DST)]

    for s in sentance_to_analyse:
        print(s)
    return sentance_to_analyse

if __name__ == "__main__":
    Domain_classifier = MultiLabelClassificationModel('roberta', 'Domain_classifier_outputs/')
    YN_classifier = ClassificationModel('roberta', 'YN_classifier_outputs/')
    QA_model = QuestionAnsweringModel('bert', 'outputs/')

    chat_history = ["No ","yes",""]
    sen = [ "what day?", "tomorrow? ", "I can't.", "How about tomorrow?", "That's fine.", "See you there."]
    chat_history = ["Let's have lunch tomorrow.", "where should we meet?", "How about xinyi?", "Sure.", "Can we meet two days later?", "Sorry, I cant.", 'How about Friday?', "See you then."]
    #chat_history = ["Let's have lunch tomorrow."]
    DST_predict(Domain_classifier, YN_classifier, QA_model, chat_history)
