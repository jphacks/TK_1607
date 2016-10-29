from django.http.response import HttpResponse
from django.shortcuts import render
import os
import json
import random
import requests
from django.http import JsonResponse
from django.views.generic import View
import urllib
from analyse.views import *

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

def google(request):
    print(request)


class ViewSet(View):
    http_method_names = ['get', 'post']

    def get(self, *args, **kwargs):
        return JsonResponse({'Successfully': 'Connected!'})

    def post(self, request, *args, **kwargs):
        dispose(json.loads(request.body.decode("utf-8"))['events'])
        return JsonResponse({'': ''})
