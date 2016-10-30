from datetime import date
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
import apiclient
import requests
import json
import requests
import json
import re
from datetime import datetime as dts
from analyse.views import *


CHRONO_ENDPOINT = 'https://labs.goo.ne.jp/api/chrono'
goo_app_id = 'c22ffb5d21ac50aef26f11a851acd86724b17225e750aa273d0c3c2be9b2a8b5'

def get_time(text):
    message = ""
    header = {
        "content-type": "application/json",
    }
    payload = {
          "app_id": goo_app_id,
          "sentence": text,
    }
    response = requests.post(
        CHRONO_ENDPOINT,
        data=json.dumps(payload),
        headers=header
        )
    for datetime in response.json()["datetime_list"]:
        return datetime[1]

client_id = '723758082242-d2ce0mh1jvrfrnicgb6k8ds1j7o91ite.apps.googleusercontent.com'
client_secret = '_dC6GVvnDa7Fx-hH2G7yYr3D'
authorization_code='4/0clQDihNdWSoGnV14OBze2ijDWVOMMlsd0CF8ZKMHHA'
redirect_uri = 'https://yoteikun.herokuapp.com/callback'
TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
def get_access_token(auth_token):
    header = {
        "content-type": "application/x-www-form-urlencoded",
    }
    payload = {
        'client_id': client_id,
         'grant_type':"authorization_code",
         'client_secret': client_secret,
         'redirect_uri': redirect_uri,
         'code': auth_token,
         'approval_prompt':'force',
    }
    response = requests.post(TOKEN_ENDPOINT,headers=header,data=payload)
    print(response.json())
    return response.json()['access_token']

def check_schedule(key,datevalue):
    schedule_id = 'CoralGift.N.H@gmail.com'
    SCHEDULE_ENDPOINT = 'https://www.googleapis.com/calendar/v3/calendars/' + schedule_id + '/events'
    schedule_date_min = get_time(datevalue) + 'T00:00:00Z'
    schedule_date_max = get_time(datevalue) + 'T23:59:59Z'
    print(schedule_date_max)
    print(schedule_date_min)
    payload = {
        'access_token':key,
        'timeMax':schedule_date_max,
        'timeMin':schedule_date_min,
        'orderBy':'startTime',
        'singleEvents':'true',
    }

#    CHECK_URL = SCHEDULE_ENDPOINT + schedule_id + '/events/?access_token=' + key + '&maxResults=1'
#    response = requests.get(CHECK_URL)
    response = requests.get(SCHEDULE_ENDPOINT,params=payload)
    print(response)
    for i in range(len(response.json()['items'])):
        postage = ''
        summary = '【予定】' + response.json()['items'][i]['summary']
        start_time =  '\n【開始時刻】' + response.json()['items'][i]['start']['dateTime'][0:17] + 'から'
        end_time = '\n【終了時刻】' + response.json()['items'][i]['end']['dateTime'][0:17] + 'まで\n'
        postage = summary + start_time + end_time
        for i in range(2):
            postage = re.sub('-','年',postage,1)
            postage = re.sub('-','月',postage,1)
            postage = re.sub('T','日',postage,1)
            postage = re.sub(':','時',postage,1)
            postage = re.sub(":",'分',postage,1)

#    return response.json()
        return postage

def add_schedule(key,schedule_body,apo_date):
    print(key)
    schedule_id = 'CoralGift.N.H@gmail.com'
    SCHEDULE_ENDPOINT = 'https://www.googleapis.com/calendar/v3/calendars/' + schedule_id + '/events?key=' + key
    header = {
    "Authorization":"Bearer " + key
    }
    payload = {
        'client_id': client_id,
         'grant_type':"authorization_code",
         'client_secret': client_secret,
         'code': auth_token,
        'access_token':key,
        'start':apo_date,
        'summary':schedule_body,
    }
    response = requests.post(SCHEDULE_ENDPOINT,data=payload)
    print(response)
    print(response.json())
    return response
