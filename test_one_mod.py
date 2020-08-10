
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

#one_str = "Hey. Are you free Tuesday afternoon? Yup! Do you want to go rock climbing? Sure! Where should we meet? How about the theme park? Why not Daan Park? Or Elephant Mountain? I've never been to Daan Park. Let's go there instead. OK. See you there!"
#one_str = "Hey. Would you want to get dinner on Sunday? No problem. Where? Let's do Daan Park? Okay. Wait! Sorry! I forgot. I can't on Sunday, I'm busy. Oh ok. That's fine."
#one_str = "Hi March! I’m Jamie. Would you like to meet up and have a chat sometime? Probably easier (and more casual) to get to know each other and ask some questions. Look forward to meeting you! Hi Jamie, That would be nice! I’ll be around the campus next Thursday. How about meeting up at some café on the campus next Thursday afternoon. I’m currently doing this bootcamp program (10am-6pm). Think my only free day would be Wednesday next week. Would that work? If not, the week following may be better? (I’ll be in Kaohsiung next weekend and in currently in Hualien) Sorry about that. Both next Wednesday and the week following work for me, except for 8/12. We can meet up at a time that we both feel comfortable. You don’t have too rush back from Hualien or to Kaohsiung. That would be too exhausting. OK, great. I’ll let you know after this weekend? Sure! Cheers. Hey March! Would you prefer to meet in the afternoon or for lunch Wednesday? Would around Nanjing Fuxing work? Let’s meet for lunch tomorrow. And yes, around Nanjing Fuxing works. Do you have any restaurant on mind? If not, I know a brunch restaurant near Nanjing Fuxing. Sure, sounds good! Let me know. The brunch restaurant I was talking about. do you think it'll be really busy? It’s probably really busy during summer vacation. We might have to wait about 10 minutes before entering the restaurant. Alright. No problem. Just saw this that’s why It says “usually no wait”. I guess we’ll be fine. wait sorry, i just realized i have a meeting 11-11:30, will likely be able to get there at 12. is that fine with you? sure, 12 then. thanks!"

one_str = "Me: Sup : yoo Me: Was gonna ask u free for lunch? 🙈 boted : i’m going soemwhere with my parents : u free other days? Me: Oh nice Me: Um Me: Starting my bootcamp tmr so.. Me: That’s why may be busier : wait lemme ask : ye i can meet for lunch : where u wanna eat Me: wait today? Me: um Me: any ideas? : LOl u only free today right : or else i’d say we can meet another day Me: think im free wednesday as well : wanna do we instead? Me: but busy tues/thurs/fri : wed* : i’m free wed Me: u going somewhere with ur parents right? Me: sure : yeah this expo thing apparently Me: oh nice okk Me: Me: wed then Me: just downloaded pokemon cus im so bored.. : pokémon go? Me: nah Me: laptop Me: acutal pokemon Me: 😆 Me: what have u been up to : learning photoshop lmaoo : wanna pick one of your many saved spots for tmr? Me: 😆 Me: What food do we want tho bro Me: Ideas?! Me: Curry, beef noodle.. small stuff? And what do we do after! We shud hike again but so hot :/ Me: Ratchet street.. breakfast foods.. idk mann need a “topic” or “feeeeel” : u don’t crave anything in particular? : don’t need anything too heavy ya know hahaha Me: Yaaa same Me: Ideas bro Me: Yo Me: I crave like Me: When it’s Me: Now. (Like I just had ice 🙈) Me: Full. Don’t crave anything Me: What’s lightttt : i don’t mind like food hopping or smth : so we can try a little bit of different things Me: Oh my uh.. name a couple stuff we could hop. Cus gotta think.. small enough for us to hop 😆 : u got any on your list? : i don’t really have an idea rn ahahh : i mean we don’t have to hop : could just eat a meal at one place Me: Hmmm Me: To be honest.. my list is composed of a lot of 早餐店 咖啡廳 有的沒有的 Me: I can just shoot u some ideas I guess Me: Cus no cravin rn : no craving for me too cause i just ate ahha : maybe feeling smth a lil western : been having taiwanese a lot lately Me: Ooh ok um.. (just came back to chat) Me: Yo, youre the one coming all the way to town :/ wanna find something u wanna try? Me: There’s a western brunch. On the pricy side tho. Called sugar pea : ohhh i heard of it : really expensive tho? : u been? : i mean i’m down for that Me: I haven’t Me: Not “really” Me: But I think by tpe standards Me: 400-500 I believe? Me: So.. we cool with sugar pea? : let’s do it : wanna do 12? Me: Seems to be popular... 12:30 then? : 🏼 Me: Down. Me: *done. "

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

for i in range(num_q):
    
    print(question_type[i])
    print('text:', answer[0][i]['answer'][:3])
    print('prob:', answer[1][i]['probability'][:3])
    print('---------------------------------------------------\n')

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
            final_str += ' on'
        final_str += ' ' + output['Day']
    if output['Time']:
        final_str += ' at ' + output['Time']
    print(final_str + '?')

man_output(init_str)
