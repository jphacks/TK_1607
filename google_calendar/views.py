from datetime import date
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
import apiclient


### 参考資料はこちら
# https://developers.google.com/google-apps/calendar/quickstart/python


### APIの認証を行う
# API用の認証JSON
json_file = 'client_secret.json'
# スコープ設定
scopes = ['https://www.googleapis.com/auth/calendar']
# 認証情報作成
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes=scopes)
http_auth = credentials.authorize(Http())
# API利用できる状態を作る
service = apiclient.discovery.build("calendar", "v3", http=http_auth)


### 祝日を取得する
# カレンダーIDには、日本の祝日カレンダーを指定
calendar_id = "ja.japanese#holiday@group.v.calendar.google.com"
# 2016年の祝日を取得する例
dtfrom = date(year=2016, month=1, day=1).isoformat() + "T00:00:00.000000Z"
dtto   = date(year=2016, month=12, day=31).isoformat() + "T00:00:00.000000Z"
# API実行
events_results = service.events().list(
        calendarId = calendar_id,
        timeMin = dtfrom,
        timeMax = dtto,
        maxResults = 50,
        singleEvents = True,
    ).execute()
# API結果から値を取り出す
events = events_results.get('items', [])
for event in events:
    print(event)
