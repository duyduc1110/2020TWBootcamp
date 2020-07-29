
class model:
    """
    need to be completed
    
    """
    def __init__(self):
        #self.model = CreatModel()
        pass
    
    def predict(self):
        # to do
        # return (bool of createvent, kv_dict )
        # kv_dict: {'activaity':None, 'day':None, 'place':None, 'logic': None if any}
        pass

class event:
    nid = 0
    def __init__(self):
        
        self.data = {'activaity':[], 'day':[], 'place':[]}
        self.current_sentence = None
        self.challenge = {'activaity':None, 'day':None, 'place':None}
        self.current_ans = {'activaity':None, 'day':None, 'place':None}
        
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
        temp_set = {}
        for key in ADPL_dict.keys():
            if key == 'logic':
                continue
            
            self.data[key].append(ADPL_dict[key])      
            self.challenge[key] = ADPL_dict[key]
            self.current_ans[key] = None
            
            temp_set.union(key)
        self.current_sentence = temp_set
    
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
        if creat_event:
            self.CreatEvent()
            
        for key in ADPL_dict.keys():
            if key == 'logic':
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
                    self.SwapEvent()
                    

        
    def CreatEvent(self):
        self.current_event = event()
        self.events.append(self.current_event)
    
    def SwapEvent(self, ADP_dict):
        if None == ADP_dict.get('logic', None):
            raise "model error >>> logic when Swapevent!!"
        
        event = self.FindEvent(ADP_dict)
        if event:
            self.current_event = event
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
            
            
        
        
         
