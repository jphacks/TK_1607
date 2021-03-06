from django.http.response import HttpResponse
from django.shortcuts import render
import os
import json
import random
import requests
from django.http import *
from django.views.generic import View
import urllib
from analyse.views import *
from google_calendar.views import *
from rest_framework.views import APIView
from rest_framework.response import Response

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'


def post_text(reply_token, text):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 689NcGvXZTVd5e5mLiPasDV+AtCb+tF9PqbmrSQa7Cd5rfJbuK0XuzU8jIPtgCtY0GhQWmOBa4jpFbf5ehLWdj9IW8xgy2rfTrBvDrqaSN8ZbLjyMbuliHM31MVMJLV9wdh3tuB2Cdp1SfLDNHCzUQdB04t89/1O/w1cDnyilFU="
    }
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text":docomo_api(text),
                }
            ]
    }
    requests.post(REPLY_ENDPOINT, headers=header, data=json.dumps(payload))


def dispose(events):
    print(events)
    for event in events:
        text = event['message']['text']
        reply_token = event['replyToken']
        event_type = event['type']
        user_id = event['source']['userId']
        post_text(reply_token, text)

def google(code):
    get_access_token(code)
    print(code)


class ViewSet(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        code = request.GET['code']
        google(code)
        return HttpResponse("認証に成功しました。この画面を閉じてください。")

    def post(self, request, *args, **kwargs):
        dispose(json.loads(request.body.decode("utf-8"))['events'])
        return JsonResponse({'': ''})
