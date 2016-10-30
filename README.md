# LINE SERVANT
## 製品概要
###  ServanTech

### 開発のきっかけ
スマートフォンでスケジュール管理をするとき，予定の日時の設定を,カレンダーアプリのドラムロールUIで行うのが面倒だった。
### 製品説明
国内だけで5200万人が利用しているLINE。その累計起動回数は，他のアプリを圧倒している。
そんなLINEを使って，決まった予定をサッと，簡単に記録できるのがLINE SERVANTだ。
LINE SERVANTは，話し言葉でスケジュールの追加，編集，削除ができるスケジュール管理bot。
天気予報を聞くこともできる。
### 特長
####1.話し言葉でスケジュールの追加，編集，削除ができる
####2.カレンダー専用のアプリを使う必要がなく，メッセージアプリ(Line)のみで完結している
####3.今日と明日の天気予報が聞ける
####4.適当に話しかけても，猫の執事が返事をしてくれる！


### 解決出来ること
素早く予定が作成できるので，あらゆるシチュエーションで予定の管理ができる。
### 今後の展望
botを公開して誰でも使えるようにする。
### 注力したこと（こだわり等）
* 毎日指定された時刻に今日の予定，明日の予定を画像で送信されるようにしたこと。

## 開発技術
### 活用した外部技術
#### API・データ
* Line Messaging API
* Google Calendar API
* NTT docomo 発話理解API
* NTTレゾナント 時刻表現正規化API
* Userlocal チャットボットAPI
* Weather hacks お天気WebサービスAPI

#### フレームワーク・ライブラリ・モジュール
* virtualenv
* gunicorn
* requests
* djangorestframework
* oauth2client
* oauthlib
* httplib2
* google
* google-api-python-client
* Python
* Django
* gunicorn
* requests

#### デバイス
* LINEが使えるスマートフォン，パソコン

### 独自技術
#### 期間中に開発した独自機能・技術
* POSTでデータを送るとそのデータを整形して画像データとして送り返すAPI
