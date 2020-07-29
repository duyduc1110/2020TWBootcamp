class model:
    def __init__(self):
        #self.model = CreatModel()
        pass
    
    def predict(self):
        # to do
        # return bool of createvent, kv_dict
        pass

class event:
    def __init__(self):
        
        self.data = {'activaity':[], 'day':[], 'place':[]}
        self.current_sentence = None
        self.challenge = {'activaity':None, 'day':None, 'place':None}
        self.current_ans = {'activaity':None, 'day':None, 'place':None}
    
    def add_logic(self, bool_, question_mark=''):
        for key in self.current_sentence:
            if self.data[key][-1] == question_mark:
                continue
            self.data[key].append(bool_)
            
            if bool_==True:
                self.current_ans[key] = self.challenge[key]
            
            self.challenge[key] = None
            
    
    def add_ADP(self, ADPL_dict):
        temp_set = {}
        for key in ADPL_dict.keys():
            if key == 'logic':
                continue
            
            self.data[key].append(ADPL_dict[key])      
            self.challenge[key] = ADPL_dict[key]
            temp_set.union(key)
        self.current_sentence = temp_set
    
    def check_preS(self):
        flag = True
        for k in self.current_sentence:
            flag = True if self.data[k][-1]=='' else False
            
        return flag
    
    def check(self):
        
        
        
            
            
            
            
        
class person:
    def __init__(self, name='cinnamon', model=None):
        self.name = name
        self.dst_model = model
        self.events = []
        self.current_event = None
        self.now_date = 1200
        self.calender = []
    
    def next(self, s: str):
        creat_event, ADPL_dict = self.dst_model.predict(s)
        if creat_event:
            self.CreatEvent()
            
        for key in ADPL_dict.keys():
            if key == 'logic':
                self.current_event.add_logic(ADPL_dict[key])
            
            elif s[-1]=='?':
                self.current_event.add_ADP(ADPL_dict)
            
            else:
                if self.current_event.check_preS():
                    self.current_event.add_ADP(ADPL_dict)
                else:
                    self.CreatEvent()
                    

        
    def CreatEvent(self):
        self.current_event = event()
        self.events.append(self.current_event)
    
    def SwapEvent
            
        
        
        
         
