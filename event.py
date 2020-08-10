from simpletransformers.classification import MultiLabelClassificationModel
from simpletransformers.classification import ClassificationModel
from simpletransformers.question_answering import QuestionAnsweringModel
from DST_model import DST_predict, DSTout2dict

class DSTModel:
    
    def __init__(self, path='outputs/'):
        self.Domain_classifier = MultiLabelClassificationModel('roberta', 'Domain_classifier_outputs/')
        self.YN_classifier = ClassificationModel('roberta', 'YN_classifier_outputs/')
        self.Day_classifier = ClassificationModel('bert', 'Day_classifier_outputs/')
        self.QA_model = QuestionAnsweringModel('bert', 'outputs/')

        print()
        print('issue')
        print()
    
    def predict(self, scentence):
        """
        return (bool of createvent, kv_dict )
        kv_dict: {'activaity':None, 'day':None, 'place':None, 'logic': None if any}
        """
        ans = DST_predict(self.Domain_classifier, self.YN_classifier, self.Day_classifier, self.QA_model, [scentence])
        creat_event, kv_dict, chat = DSTout2dict(ans)
        return creat_event, kv_dict

class event:
    nid = 0
    def __init__(self):
        
        self.data = {'Activity':[], 'Day':[], 'Place':[]}
        self.current_sentence = []
        self.challenge = {'Activity':None, 'Day':None, 'Place':None}
        self.current_ans = {'Activity':None, 'Day':None, 'Place':None}
        
        # will use in the future
        self.id = event.nid
        event.nid += 1
    
    def add_logic(self, bool_, question_mark=''):
        for key in self.current_sentence:
            if self.data[key][-1] == question_mark:
                continue
            self.data[key].append(bool_)
            
            if bool_==True:
                self.current_ans[key] = self.challenge[key]
            
            self.challenge[key] = None
            
    
    def add_ADP(self, ADPL_dict):
        #print(ADPL_dict)
        temp = []
        for key in ADPL_dict.keys():
            if key == 'logic':
                continue
            
            self.data[key].append(ADPL_dict[key])      
            self.challenge[key] = ADPL_dict[key]
            self.current_ans[key] = None
            
            temp.append(key)
            
        self.current_sentence = temp
    
    def check_preS(self):
        """
        check whether pre sentence is ADP question and val is ''

        """
        flag = True
        for k in self.current_sentence:
            flag = True if self.data[k][-1]=='' else False
            
        return flag
    
    def check_ans(self):
        for val in self.current_ans.values():
            if val == None:
                return None
        return self.current_ans
    
    def show(self):
        print('Challenge:', self.challenge)
        print('Ans:', self.current_ans)
        challenge = 'Challenge-->>  Activity: %s, Day: %s, Place: %s'\
            %(self.challenge['Activity'], self.challenge['Day'], self.challenge['Place'])
        
        ans = 'Ans-->>  Activity: %s, Day: %s, Place: %s'\
            %(self.current_ans['Activity'], self.current_ans['Day'], self.current_ans['Place'])
        
        return challenge, ans
                
        
        
            
            
            
            
        
class person:
    def __init__(self, name='cinnamon', model=None):
        self.name = name
        self.dst_model = model
        self.events = []
        self.current_event = None
        self.now_date = 1200
        self.calender = []
    
    def next(self, s: str):
        """
        input one sentence 
        """
        creat_event, ADPL_dict = self.dst_model.predict(s)
        if creat_event or self.current_event == None:
            self.CreatEvent()
            
        for key in ADPL_dict.keys():
            if key == 'Logic':
                self.current_event.add_logic(ADPL_dict[key])
                
                plan = self.current_event.check_ans()
                if plan:
                    self.calender.append(plan)
            
            elif s[-1]=='?':
                self.current_event.add_ADP(ADPL_dict)
            
            else:
                if self.current_event.check_preS():
                    self.current_event.add_ADP(ADPL_dict)
                else:
                    self.SwapEvent(ADPL_dict)
                    

        
    def CreatEvent(self):
        self.current_event = event()
        self.events.append(self.current_event)
    
    def SwapEvent(self, ADP_dict):
        if None == ADP_dict.get('logic', None):
            print("model error >>> logic when Swapevent!!")
            #raise "model error >>> logic when Swapevent!!"
        
        event = self.FindEvent(ADP_dict)
        if event:
            self.current_event = event
            print("SWAP!!!!!!")
        else:
            print("Swap event but not match! Check model")
            # raise "Swap event but not match! Check model"
            
            
    def FindEvent(self, ADP_dict):
        for event in self.events:
            
            # compare
            flag = True
            for val in ADP_dict.values():
                if val not in event.challenge.values() and val not in event.current_ans.values():
                        
                    flag = False
                    continue
                
            if flag:
                return event
            
        return False
    
    def clean(self):
        self.events = []
        self.current_event = None
        self.calender = []
    
    def ShowEvent(self):
        """
        
        Returns Tuple List
        -------
        [(challenge, ans), ... ]
        """
        if self.current_event == None:
            return [(None,'Ans-->>  Activity: %s, Day: %s, Place: %s'%('none', 'none', 'none'))]
        temp = []
        for idx, event in enumerate(self.events):
            print('EVENT %2s'%idx)
            challenge, ans = event.show()
            temp.append((challenge, ans))
        return temp
        
            
            
if __name__ == '__main__':
    net = DSTModel()

    hank = person('hank', net)
    chats = "do you want to see a movie tomorrow? | sorry, I'm busy tomorrow. | How about five days later? | Sure."
    chats = chats.split(' | ')    
    for s in chats:
        hank.next(s)
    
    
    
