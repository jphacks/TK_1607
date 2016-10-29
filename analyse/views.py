# coding: utf8
import os
import json
import random
import requests
import urllib
import re


CHRONO_ENDPOINT = 'https://labs.goo.ne.jp/api/chrono'
goo_app_id = 'c22ffb5d21ac50aef26f11a851acd86724b17225e750aa273d0c3c2be9b2a8b5'

USERLOCAL_ENDPOINT = 'https://chatbot-api.userlocal.jp/api/chat'
userlocal_api_key = '97e9f233f7b9e0051657'

docomo_api_key = "4a795447764c4d70632e552f594350714c7875634f4b57596f75675049612f73422f55774b69356b346139"
DOCOMOAPI_ENDPOINT = "https://api.apigw.smt.docomo.ne.jp/sentenceUnderstanding/v1/task?APIKEY=" + docomo_api_key

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



def userlocal_chat(text):
    message = ""
    header = {
        "content-type": "application/json",
    }
    payload = {
         "key": userlocal_api_key,
         "message": text,
    }
    response = requests.post(
        USERLOCAL_ENDPOINT,
        data=json.dumps(payload),
        headers=header)
    chat = response.json()['result']
    return chat

def docomo_api(text):
    header = {
        "content-type": "application/x-www-form-urlencoded",
    }

    payload = {
        "projectKey": " Ypteikun",
         "appInfo": {
             "appName": "yoteikun_bot",
             "appKey": "yoteikun_bot"},
         "clientVer": "1.0.0", "dialogMode": "off",
         "language": "ja",
        # "userId": "12 123456 123456 0", "location": {
        # "lat": "139.766084",
        # "lon": "35.681382" },
        "userUtterance": {
        "utteranceText": text
        } }

    response = requests.post(
        DOCOMOAPI_ENDPOINT,
        data=json.dumps(payload),
        headers=header)

    if response.json()["dialogStatus"]["command"]["commandId"] == "BT01301":  # スケジュール登録
        message = 'スケジュールを登録しました。'
        return message
    elif response.json()["dialogStatus"]["command"]["commandId"] == "BT01302":  # スケジュール参照
        post_message_date = post_message_hour = post_message_day = japan_day = japan_date = japan_hour =  ""
        print(response.json())
        for date in response.json()['dialogStatus']['slotStatus']:
            print(date)
            if date['valueType'] == 'datePnoun':
                date = date['slotValue']
                post_message_day += get_time(date)
                japan_day = re.sub('-','年',post_message_day,1)
                japan_day = re.sub('-','月',japan_day,1)
                japan_day += '日'
            elif date['valueType'] == 'timeHour':
                hour = date['slotValue']
                post_message_hour += get_time(hour)
                hour_date = re.sub(post_message_day,'',post_message_hour)
                japan_hour = re.sub("T",'',hour_date,1)
                japan_hour += '時'
            elif date['valueType'] == 'time':
                day = date['slotValue']
                post_message_date += get_time(day)
                day_date = re.sub(post_message_day,'',post_message_date)
                japan_date = re.sub(':','時',day_date,1)
                japan_date = re.sub("T",'',japan_date,1)
                japan_date += '分'
                
        post_messages = japan_day + japan_date + japan_hour + 'のスケジュールはこちらです。'
        return post_messages

    else:
        return userlocal_chat(text)
