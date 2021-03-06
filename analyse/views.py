# coding: utf8
import os
import json
import random
import requests
import urllib
import re
from google_calendar.views import *

CHRONO_ENDPOINT = 'https://labs.goo.ne.jp/api/chrono'
goo_app_id = 'c22ffb5d21ac50aef26f11a851acd86724b17225e750aa273d0c3c2be9b2a8b5'

USERLOCAL_ENDPOINT = 'https://chatbot-api.userlocal.jp/api/chat'
userlocal_api_key = '97e9f233f7b9e0051657'

docomo_api_key = "4a795447764c4d70632e552f594350714c7875634f4b57596f75675049612f73422f55774b69356b346139"
DOCOMOAPI_ENDPOINT = "https://api.apigw.smt.docomo.ne.jp/sentenceUnderstanding/v1/task?APIKEY=" + docomo_api_key

key = 'ya29.CjCKAxerh0SNzrrhTv6KbMRbsmBlN2CL22F4sHvgcQ6b19kop5c14fhw61DtJPCzF9A'


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
        "content-type": "application/json",
    }

    payload = {
        "projectKey": "OSU",
         "appInfo": {
             "appName": "yoteikun_app",
             "appKey": "yoteikun_app01"
             },
         "clientVer": "1.0.0",
         "dialogMode": "off",
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
        apo_date = get_time(response.json()['dialogStatus']['slotStatus'][1]['slotValue'])
        schedule_body = response.json()['dialogStatus']['slotStatus'][2]['slotValue']
        print(response.json())
        res = add_schedule(key,schedule_body,apo_date)
        if res == '<Response [401]>':
            message = 'スケジュールを登録しました。'
            return message
        else:
            message = 'スケジュールの登録に失敗しました。'
            return message
    elif response.json()["dialogStatus"]["command"]["commandId"] == "BT01302":  # スケジュール参照
        post_message_date = post_message_hour = post_message_day = japan_day = japan_date = japan_hour =  ""
        for date in response.json()['dialogStatus']['slotStatus']:
            if 'valueType' in date and date['valueType'] == 'datePnoun':
                schedule_date = date = date['slotValue']
                post_message_day += get_time(date)
                japan_day = re.sub('-','年',post_message_day,1)
                japan_day = re.sub('-','月',japan_day,1)
                japan_day += '日'
            elif 'valueType' in date and date['valueType'] == 'timeHour':
                hour = date['slotValue']
                post_message_hour += get_time(hour)
                hour_date = re.sub(post_message_day,'',post_message_hour)
                japan_hour = re.sub("T",'',hour_date,1)
                japan_hour += '時'
            elif 'valueType' in date and date['valueType'] == 'time':
                day = date['slotValue']
                post_message_date += get_time(day)
                day_date = re.sub(post_message_day,'',post_message_date)
                japan_date = re.sub(':','時',day_date,1)
                japan_date = re.sub("T",'',japan_date,1)
                japan_date += '分'
        post_messages = japan_day + japan_date + japan_hour + 'のスケジュールはこちらです。'
        key = 'ya29.Ci-KA7YQvG-ze6J56ut15-_O6dwCU9vSHdKpbbIRfy7_srdG3ql8fPsEczRc2VOmgg'
        schedule_data = check_schedule(key,schedule_date)
        message = post_messages + '\n' + schedule_data
        print(schedule_data)
        return message
    elif response.json()["dialogStatus"]["command"]["commandId"] == "BT00301":  # 天気予報
        WEATHER_ENDPOINT_BETA = "http://weather.livedoor.com/forecast/webservice/json/v1?city="
        header = {"content-type": "application/json"}

        if 'valueType' in response.json()['dialogStatus']['slotStatus'][0]:  #地名を検出したか
            place = response.json()['dialogStatus']['slotStatus'][0]['slotValue']  # 地名が検出できて入れば，placeに代入

            FILEIN = 'chimei.json'  # jsonファイルから情報を取り出してdataに代入
            f = open(FILEIN, 'r')
            data = json.load(f)

            if place in data:  # ユーザからもらった地名がjsonデータにあるかをチェック。なければ東京の天気を返す
                WEATHER_ENDPOINT = WEATHER_ENDPOINT_BETA + data[place]
                response = requests.get(WEATHER_ENDPOINT)
                tenki = place + 'は' + response.json()['forecasts'][0]['telop'] + "だって！\n"
                kaisetsu = (response.json()['description']['text'])
                output = tenki + kaisetsu
                return output
            else:  #地名は取得できたけどjsonデータにない時
                WEATHER_ENDPOINT = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + "130010"
                response = requests.get(WEATHER_ENDPOINT)
                tenki = '地名が分からないので，東京の天気を表示します。県名には「県」を入れてください！東京は' + response.json()['forecasts'][0]['telop'] + "だって！\n"
                kaisetsu = (response.json()['description']['text'])
                output = tenki + kaisetsu
                return output

        else:  # 天気を聞きたいのはわかるけど地名がjsonデータにない時
            print("I'm in tenki_in_tokyo.")
            WEATHER_ENDPOINT = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + "130010"
            response = requests.get(WEATHER_ENDPOINT)
            tenki = '地名が分からないから，東京の天気を表示します。東京は' + response.json()['forecasts'][0]['telop'] + "だって！\n"
            kaisetsu = (response.json()['description']['text'])
            output = tenki + kaisetsu
            return output

    else:
        return userlocal_chat(text)
