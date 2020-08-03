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

def DST_predict(Domain_classifier, YN_classifier, Day_classifier, QA_model, chat_history, Threshold = 0.4):

    Domain = ['Create_event', 'Activity', 'Day', 'Place', 'Logic']
    Day_kind = ['delay', 'early', 'change']
    Question_dict = {'Activity' : 'what are we going to do?', 'Day' : 'what day?', 'Place' : 'where are we going?'}

    sentance_to_analyse = []
    raws = []

    for chats in chat_history:
        Domain_predictions, Domain_raw_outputs = Domain_classifier.predict([chats])
        '''
            raw_outputs = [[0.9, 0.08...]]
        '''
        # Check the raw_outputs of a sentance is qualified to be used
        chat_DST = []
        raws.append([Domain_raw_outputs[0], Domain_predictions[0]])
        for i in range(len(Domain_raw_outputs[0])):
            # Over the Threshold then used.
            if Domain_raw_outputs[0][i] > Threshold:
                # Get the logic, 0 for Negative, 1 for Positive
                if Domain[i] == 'Logic':
                    YN_predictions, YN_raw_outputs = YN_classifier.predict([chats])
                    chat_DST.append((Domain[i], YN_predictions[0]))
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
                                    # Get the value of Creating event
                    if Domain[i] == 'Day':
                        Day_predictions, Day_raw_outputs = Day_classifier.predict([chats])
                        chat_DST.append((Domain[i], Day_kind[Day_predictions[0]], QA_model.predict(to_predict)[0][0]['answer'][0]))
                    else:
                        chat_DST.append((Domain[i], QA_model.predict(to_predict)[0][0]['answer'][0]))

        sentance_to_analyse += [(chats, chat_DST)]
    for raw, pred in zip(raws,sentance_to_analyse):
        print(raw[0], raw[1])
        print(pred)
        print()
        
    return sentance_to_analyse

if __name__ == "__main__":
    Domain_classifier = MultiLabelClassificationModel('roberta', 'Domain_classifier_outputs/')
    YN_classifier = ClassificationModel('roberta', 'YN_classifier_outputs/')
    Day_classifier = ClassificationModel('bert', 'Day_classifier_outputs/')
    QA_model = QuestionAnsweringModel('bert', 'outputs/')

    chat_history = ["Let's have lunch tomorrow.", "where should we meet?", "How about xinyi?", "Sure.", "Can we meet 3 days later?", "Sure."]
    #chat_history += [ "what day?", "tomorrow? ", "I can't.", "How about tomorrow?", "That's fine.", "See you there."]
    #chat_history = pd.read_csv("data/struture_Domain_classifier_test.csv")['text'].iloc[:10]
    DST_predict(Domain_classifier, YN_classifier, Day_classifier, QA_model, chat_history)



