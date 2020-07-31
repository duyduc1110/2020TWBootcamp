#!/usr/bin/env python
#coding=utf-8

print('Hello')

import json
import os
import torch

from simpletransformers.question_answering import QuestionAnsweringModel

train_args = {
    'num_train_epochs': 1,
    'overwrite_output_dir': True,
    'reprocess_input_data': True,
}

# Create the QuestionAnsweringModel
model = QuestionAnsweringModel(
            "bert",
            "deepset/bert-large-uncased-whole-word-masking-squad2",
            args=train_args
             )
             
# Train the model
model.train_model('data_v1.json')

print("-------------------")

# Making predictions using the model.
to_predict = [
            {
                "context": "This is the context used for demonstrating predictions.",
                "qas": [{"question": "What is this context?", "id": "0"}],
            }]

print(model.predict(to_predict))
