import pandas as pd
import numpy as np
import sklearn
import torch
import torch.nn as nn
import ast
import tqdm

from transformers import AutoConfig, AutoTokenizer, BertForQuestionAnswering
from torch.utils.data import DataLoader, Dataset


class SashimiDataset(Dataset):
    def __init__(self, data):
        super(SashimiDataset, self).__init__()
        self.text = data.Text
        self.label = data.Label
        
    def __len__(self):
        return self.text.shape[0]*4
    
    def __getitem__(self, idx):
        text = self.text[idx // len(QUESTIONS)]
        qs_idx = idx % len(QUESTIONS)
        label = self.label[idx // len(QUESTIONS)][qs_idx]
        question = QUESTIONS[qs_idx]
        
        inputs = tokenizer(question, text, padding='max_length', truncation=True, max_length=128, return_tensors='pt')
        label = torch.LongTensor(label)
        
        plus_idx = (inputs['input_ids'] == 102).nonzero()[0,1]
        if label.tolist() != [0,0]:
            label += plus_idx
        
        return inputs, label
        
        
def get_data(path, sep=',', index_col=None):
    data = pd.read_csv(path, sep=sep, index_col=index_col)
    #data['Text'] = [ast.literal_eval(data.Text[i])[0] for i in range(data.shape[0])]
    data['Label'] = [ast.literal_eval(data.Label[i]) for i in range(data.shape[0])]
    return data

if __name__ == '__main__':
    
    config = AutoConfig.from_pretrained("deepset/bert-base-cased-squad2")
    model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
    tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2", use_fast=True)
    
    QUESTIONS = [
        'What activity?',
        'What date?',
        'What time?',
        'Where to go?'
    ]

    data = get_data('./data/updated3500s.csv', sep='\t')
    dataset = SashimiDataset(data)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=2)
    
    
    loss_fn = nn.CrossEntropyLoss()
    num_epoch = 5
    lr = 1e-5
    optimizer = torch.optim.AdamW(model.parameters(), lr)
    
    model.cuda()
    model.train()

    for epoch in range(num_epoch):
        total_loss = 0
        
        for inputs, label in tqdm.tqdm(dataloader):
            # Reform the inputs
            for k in inputs.keys():
                inputs[k] = inputs[k].squeeze(1).cuda()

            optimizer.zero_grad()
            outputs = model(**inputs)
            predict = torch.stack(outputs, -1)

            loss = loss_fn(predict, label.cuda())
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        print(f'Train loss {total_loss}')

torch.save(model.state_dict(), 'e3lr2e5.pth')
        
    torch.save(model.state_dict(), f'e{num_epoch}lr{lr}.pth')
