from __future__ import print_function
from datetime import datetime, timedelta
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


def Get_StarT_End_Time(Day):
    start_time = datetime(Day[0], Day[1], Day[2], 10, 0, 0)#.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = start_time + timedelta(hours = 4)
    
    return start_time.strftime("%Y-%m-%dT%H:%M:%S"), end_time.strftime("%Y-%m-%dT%H:%M:%S")
    

def Create_event (Event = 100, Location = 0, Day = [2020, 7, 18], timeZone = 'Asia/Brunei'):
    service, creds_id = Build_Google_Service()
    events_result = service.events().list(calendarId = creds_id).execute()
    
    # Get Day, Default start from 10 am, end at 2 pm
    start_time, end_time = Get_StarT_End_Time(Day)

    event = {
      'summary': Event,
      'location': Location,
      'start': {
        'dateTime': '2020-07-28T09:00:00-07:00',
        'timeZone': timeZone,
      },
      'end': {
        'dateTime': '2020-07-28T17:00:00-07:00',
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

    
    event = service.events().insert(calendarId = creds_id, body = event).execute()
    print (('Event created: {}').format(event.get('htmlLink')))
    

if __name__ == '__main__':
    Event = 'Cinnamon_AI'
    Location = 'Elephant Mountain'
    Day = [2020, 7, 28]
    Create_event(Event, Location, Day)
