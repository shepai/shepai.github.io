from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datetime as dt
from datetime import datetime
from dateutil.parser import parse as dtparse

link="https://www.googleapis.com/auth/calendar"
scopes = [link,
         link+".readonly",
         link+".events",
         link+".events.readonly",
         link+".settings.readonly",
         link+".addons.execute"]

#flow = InstalledAppFlow.from_client_secrets_file("client_id.json",scopes=scopes)
class calendar:
    def __init__(self,token=""):
        c=""
        if token=="":
           c=pickle.load(open("token.pkl","rb"))
        self.service=build("calendar","v3",credentials=c)
    def getDay(self,dateWanted):
        result=self.service.calendarList().list().execute()
        calendarId=result['items'][0]['id']
        result=self.service.events().list(calendarId=calendarId,timeZone="Europe/London").execute()
        today=[]
        for i in result['items']:
            event=i['summary']
            date=i['start']
            time=""
            if 'date' in list(date.keys()):
                date=date['date']
                time="all day"
            else:
                date=date['dateTime'].replace("+01:00","Z")
                d1 = dt.datetime.strptime(date,"%Y-%m-%dT%H:%M:%SZ")
                date=d1.strftime("%d %m %Y")
                time=d1.strftime("%H:%M")
            if date==dateWanted:
                today.append([event,time])
        return today   
    def getEvents(self):
        result=self.service.calendarList().list().execute()
        calendarId=result['items'][0]['id']
        result=self.service.events().list(calendarId=calendarId,timeZone="Europe/London").execute()
        events=[]
        for i in result['items']:
            events.append(i['summary'])
        return events



