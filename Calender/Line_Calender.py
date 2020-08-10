from __future__ import print_function
from datetime import datetime, timedelta
from dateutil.parser import parse
from word2number import w2n
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def Get_OAth():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


def Build_Google_Service():
    # Prepare credential first
    Get_OAth()
    
    # Get service object
    creds = pickle.load(open('token.pickle', 'rb'))
    service = build('calendar', 'v3', credentials=creds)
    result = service.calendarList().list().execute()
    creds_id = result['items'][0]['id']
    
    return service, creds_id


def time_handler(Time):
    Time = Time.strip()
    non_exist_word = [None, '/', '', ' ']  
    date_word = 'January,February,March,April,May,June,July,August,September,October,November,December'.lower().split(',')
    # error time
    for t in non_exist_word:
        for d in date_word:
            if t == Time :
                return '10am'
            if d in Time:
                return '10am'

    # Normal one
    if 'pm' in Time or 'am' in Time:
        return Time

    # extract correct time
    Time_ = Time.split()
    key_word = ["o'clock"]
    Prepositions = ['on', 'in', 'at']
    return_time = []
    for t in Time_:
        if t in Prepositions:
            return_time.append(t)
        else:
            try:
                return_time.append(str(w2n.word_to_num(t)))
                return ''.join(return_time) +':00'
            except:
                return '10am'




def Get_Start_End_Time(Date, Time):
    Base_time = Date[0]
    Time = time_handler(Time)
    # split the confusing word
    key_word_change = {'next':7}
    with_key = False
    for key_change in key_word_change.keys():
        if key_change in Base_time.lower():
            Base_time = ''.join(re.split(key_change, Base_time))
            with_key = True
            break

    # Specific time
    key_word = {'weekend':['Saturday', 0], 'today' : ['today', 0], 'tomorrow': ['today', 1], 'the day after tomorrow':['today', 2]}
    key_word_to_remove = ['this', 'that']
    for key in key_word.keys():
        for rm_key in key_word_to_remove:
            if key in Base_time.lower():
                Base_time = ''.join(re.split(key, Base_time)) + key_word[key][0]
            Base_time = ''.join(re.split(rm_key, Base_time))
            break

    if with_key:
        start_time = parse(Base_time + ' ' + Time) + timedelta(days = key_word_change[key_change])
    else:
        if 'today' in Base_time:
            start_time = datetime.now() + timedelta(days = key_word[key][1])
        else:
            start_time = parse(Base_time + ' ' + Time) + timedelta(days = key_word[key][1])
    
    # Change time if needed
    if Date[1] is None or Date[2] is None:
        day_unit = {'day': 1, 'week' : 7}

        delay = True if Date[1] else False
        early = True if Date[2] else False

        if delay:
            for key in day_unit:
                if key in Date[1][1].lower():
                  start_time += timedelta(days = Date[1][0] * day_unit[key])
                  break

        elif early:
            for key in day_unit:
                if key in Date[2][1].lower():
                    start_time -= timedelta(days = Date[2][0] * day_unit[key])
                    break

    # expect every event last for 4 hours
    end_time = start_time + timedelta(hours = 4)
    
    return start_time.strftime("%Y-%m-%dT%H:%M:%S"), end_time.strftime("%Y-%m-%dT%H:%M:%S")
    

def Create_event (Event, timeZone = 'Asia/Brunei'):
    '''
      Event : dict
      Event['Activity'] = 'study'
      Event['Day'] = tuple(('on this friday', (3,'days'), None ))
      Event['Time'] = '  '
      Event['Place'] = 'Elephant Mountain'
    '''
    service, creds_id = Build_Google_Service()
    events_result = service.events().list(calendarId = creds_id).execute()
    
    # Get Day, Default start from 10 am, end at 2 pm
    start_time, end_time = Get_Start_End_Time(Event['Day'], Event['Time'])

    print(start_time)

    if Event['Activity'] is None:
        Event['Activity'] = 'Unkonwn'

    if Event['Place'] is None:
        Event['Place'] = 'Unkonwn'

    event = {
      'summary': Event['Activity'],
      'location': Event['Place'],
      'start': {
        'dateTime': start_time,
        'timeZone': timeZone,
      },
      'end': {
        'dateTime': end_time,
        'timeZone': timeZone,
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    
    #event = service.events().insert(calendarId = creds_id, body = event).execute()
    #print (('Event created: {}').format(event.get('htmlLink')))
    

if __name__ == '__main__':
    Event = dict()
    Event['Activity'] = 'study'
    Event['Day'] = tuple(('tomorrow', (3,'days'), None ))
    Event['Time'] = '  '
    Event['Place'] = 'Elephant Mountain'

    Create_event(Event)