from datetime import date
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
import apiclient
import requests
import json

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

def check_schedule(key):
    SCHEDULE_ENDPOINT = 'https://www.googleapis.com/calendar/v3/calendars/'
    schedule_id = 'CoralGift.N.H@gmail.com'
    CHECK_URL = SCHEDULE_ENDPOINT + schedule_id + '/?access_token=' + key
    response = requests.get(CHECK_URL)
    print(response.json())
    return response.json()
