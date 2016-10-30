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

### 参考資料はこちら
# https://developers.google.com/google-apps/calendar/quickstart/python
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
    }
    response = requests.post(TOKEN_ENDPOINT,headers=header,data=payload)
    print(response.json())
    return response.json()['access_token']

def check_schedule(key,datevalue):
    schedule_id = 'CoralGift.N.H@gmail.com'
    SCHEDULE_ENDPOINT = 'https://www.googleapis.com/calendar/v3/calendars/' + schedule_id + '/events'
    schedule_date_min = '2016-10-27T00:00:00Z'
    schedule_data_max = '2016-10-31T00:00:00Z'
    payload = {
        'access_token':key,
        'timeMax':schedule_data_max,
        'timeMin':schedule_date_max,
        'orderBy':'startTime',
        'singleEvents':'true',
    }

#    CHECK_URL = SCHEDULE_ENDPOINT + schedule_id + '/events/?access_token=' + key + '&maxResults=1'
#    response = requests.get(CHECK_URL)
    response = requests.get(SCHEDULE_ENDPOINT,params=payload)
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
