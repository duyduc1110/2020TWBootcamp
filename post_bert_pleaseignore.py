import json
import os
import sys

input_json = open(sys.argv[1])
#mod_output = sys.argv[2]

bert_input = json.load(input_json)

def clean(bert_dict):
    return bert_dict

# Clean the output
mod_output = clean(bert_input)

print(mod_output.keys())

"""
# Evaluate the model. (Being lazy and evaluating on the train data itself)
#result, text = model.eval_model("data/train.json")
result, text = model.eval_model(train_path)
with open('result.json','w') as f:
    json.dump(result, f)
with open('text.json', 'w') as f:
    json.dump(text, f)
print(result)
print(text)

print("-------------------")
"""

input_json.close()

