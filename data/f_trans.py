
import json
import pickle


def transfer_format(inp, outpath = './data_vx.json'):
    """
    inp: [contexts, label pairs]
    pairs: [[question, ans], ......]
    ans: {'text':'......', 'answer_start': idx}
    
    out: write file
    
    """
    now_id = 0

    data = list()
    for context, pairs in inp:
        
        ele = dict()
        ele['context'] = context
        
        qas = list()
        
        for question, ans in pairs:
            qas_ele = dict()
            
            qas_ele['id'] = now_id = now_id+1
            qas_ele['is_impossible'] = False if ans['text'] else True
            qas_ele['question'] = question
            qas_ele['answers'] = [ans]
            
            qas.append(qas_ele)
        
        ele['qas'] = qas
        data.append(ele)
    
    with open(outpath, "w") as f:
        json.dump(data, f)

def gen2json_(inpath, outpath = './data_vx.json', question_type = ['what are we going to do?', 'what day?', 'what time?', 'where are we going?' ]):
    
    with open(inpath, 'rb') as f:
        data = pickle.load(f)
        
    contexts = data['train_data']
    labels = data['label']
    
    for i in range(len(labels)):
        labels[i] = list(zip(question_type, labels[i]))
    
    data = list(zip(contexts, labels))
    transfer_format(data, outpath)
    
def gen2json(data, outpath = './data_vx.json', question_type = ['what are we going to do?', 'what day?', 'what time?', 'where are we going?' ]):
    
        
    contexts = data['train_data']
    labels = data['label']
    
    for i in range(len(labels)):
        labels[i] = list(zip(question_type, labels[i]))
    
    data = list(zip(contexts, labels))
    transfer_format(data, outpath)





import sys
if __name__ == '__main__':
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    
    #gen2json('train_v1.pkl', './data_v1.json')
    gen2json_(inpath, outpath)
    
    
    



