import random
import pandas as pd
import numpy as np
from transformers import BertTokenizer, AutoTokenizer
# Code borrow from Jamie
from Generater_v4 import gendatl

# Declare Tokenizer
tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2", use_fast=True)

def get_tokenize(data):
    return tokenizer(data)

# Brute force to match
def find_match(list1, list2):
    for i in range(len(list1)-len(list2) + 1):
        if list1[i:i+len(list2)] == list2:
            return [i, i+len(list2)-1]

def generate_training_data(num):
    data = []
    training_data_frame = gendatl(num)

    for index, row in training_data_frame.iterrows():
        text = [row['Text']]
        # text get tokenized for each item
        label = [find_match( get_tokenize(row['Text'])['input_ids'], get_tokenize(row[col])['input_ids'][1:-1] ) for col in training_data_frame.columns[1:]]
        
        data.append([text, label])
    
    # Idea from Jamie's code
    training_data_to_saved = pd.DataFrame(data, columns =['Text', 'Label'])    
    training_data_to_saved.to_csv('data/training_data.csv', sep='\t', index=False)
    return data 


if __name__ == '__main__':
    generate_training_data(2000)
    data = pd.read_csv('data/training_data.csv', sep='\t')
    print(data)





