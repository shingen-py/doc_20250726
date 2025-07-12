# 📘 第1章：connpass API v2 の仕組みと体験

## 🎯 この章の目的
この章では、以下のことを体験します。

* connpass API v2 がどのような仕組みで動いているのかを知る
* 実際に HTTP リクエストを使って connpass からイベントデータを取得する
* JSON というデータ形式に慣れる
* 今後作る FastAPI アプリの「土台になる部分」を理解する

## 🔍 1-1. API とは何か？

**API（Application Programming Interface）** とは、他のアプリケーションとプログラムでやり取りをするための「窓口」です。

たとえば、connpass というサービスの中にある「イベント情報を検索する機能」を、他のアプリからも利用できるようにしたものが connpass API です。

## 🧾 1-2. connpass API v2 の特徴
* URL: https://connpass.com/api/v2/events/
* 認証：APIキーが必要（X-API-Keyヘッダーで送信）
* データ形式：JSON
* 利用制限：1秒に1回までのリクエスト（Rate limit）

APIの利用申請方法は公式ページに案内があります（ https://connpass.com/about/api/v2/ ）

## 🧪 1-3 ターミナルからAPIを直接呼び出す方法
### 🎯 目的
Pythonでプログラムを書く前に、まずは 「手動でAPIを叩いてみる」 ことで、

* HTTPリクエストの構造
* APIキーの必要性
* ヘッダーやクエリパラメータの使い方

を体験的に理解しましょう。

### 🖥 方法1：curl を使ってAPIを呼び出す
curl はほとんどの OS に標準で入っているコマンドラインツールです。

✅ 基本構文
```bash
curl -H "X-API-Key: あなたのAPIキー" "https://connpass.com/api/v2/events/?keyword=Python&count=1"
```
✅ 実行例（APIキーを仮に abcdefg12345 とした場合）
```bash
curl -H "X-API-Key: abcdefg12345" "https://connpass.com/api/v2/events/?keyword=Python&count=1"
```
📌 うまくいくと…
```json
{"results_start":1,"results_returned":1,"results_available":1234,"events":[{"event_id":...}]}
```
❗失敗例（APIキーなし）
```bash
curl "https://connpass.com/api/v2/events/?keyword=Python"
```
```json
{"error":"Unauthorized"}
```
X-API-Key ヘッダーを付けないと、401 Unauthorized（認証エラー）になります。

### 🧰 方法2：httpie を使って読みやすく表示（任意）
httpie は、curl よりも人に優しい出力をしてくれるコマンドラインツールです。

📥 インストール
```bash
pip install httpie
```
✅ 実行例
```bash
http GET https://connpass.com/api/v2/events/ keyword==Python count==1 "X-API-Key:abcdefg12345"
```
出力が整形されて見やすくなり、JSONの構造が理解しやすくなります。

## 📦 1-4. PythonでAPIを呼び出す

### 🔧 必要なライブラリをインストール
まずはAPIを呼び出すために、Pythonのライブラリ httpx をインストールします。

```bash
pip install httpx
pip install python-dotenv
```

### 🔐 APIキーの安全な管理：`.env` ファイルを使おう

APIキーは直接コードに書くのではなく、`.env` ファイルを使って管理しましょう。  
これにより、**キーの流出防止**や **コード共有時の安全性向上**が図れます。

`.env` ファイルの作成

```ini
CONNPASS_API_KEY=あなたのAPIキー
```

以下のコードで、`.env` ファイルから API キーを読み込むことができます。

```python
from dotenv import load_dotenv
import os
load_dotenv()  # .env ファイルを読み込む

# APIキーを環境変数から取得
API_KEY = os.getenv("CONNPASS_API_KEY")
```

### 🧪 connpass API を叩いてみよう（サンプルコード）
以下のコードを try_connpass_api.py という名前で保存して、実行してみましょう。

🔐 注意：APIキーを自分のものに置き換えてください
```python
import httpx
from dotenv import load_dotenv
import pprint  # 見やすく出力するためのモジュール

# APIキーを環境変数から取得
API_KEY = os.getenv("CONNPASS_API_KEY")

# connpass API v2 の URL
url = "https://connpass.com/api/v2/events/"

# 検索条件（キーワード: Python）
params = {
    "keyword": "Python",
    "count": 3  # 取得件数
}

# APIキーを指定したヘッダー
headers = {
    "X-API-Key": API_KEY
}

# リクエスト送信
response = httpx.get(url, params=params, headers=headers)

# 結果のステータスコードを表示
print("ステータスコード:", response.status_code)

# レスポンスの JSON を整形して出力
if response.status_code == 200:
    data = response.json()
    pprint.pprint(data)
else:
    print("エラーが発生しました:", response.text)
```

### 実行結果の見方
実行すると、以下のような出力が得られます（一部抜粋）：

```json
{
  'results_start': 1,
  'results_returned': 3,
  'events': [
    {
      'event_id': 123456,
      'title': 'Pythonもくもく会@甲府',
      'started_at': '2025-07-01T19:00:00+09:00',
      'place': '甲府市○○',
      'event_url': 'https://connpass.com/event/123456/',
      ...
    },
    ...
  ]
}
```
events の中にイベント情報が入っています。title や started_at を見ると、イベント名や開催日時が取れていることが分かります。

### よくあるエラーと対処法

| エラー | 原因 | 対処法 |
| ---- | ---- | ---- |
| `401 Unauthorized` | APIキーが間違っている、または指定していない | ヘッダーの `X-API-Key` を確認 |
| `429 Too Many Requests` | 短時間に連続してアクセスした | 1秒に1回まで、`time.sleep(1)` などで間隔を空ける |
| `ModuleNotFoundError: No module named 'httpx'` | httpx がインストールされていない | `pip install httpx` を実行 |

## ✅ この章のまとめ
* connpass API v2 は、イベント情報を取得できる便利な Web API
* API を呼び出すには、URL・クエリパラメータ・HTTPヘッダーの3つが重要
* Python の httpx を使って簡単に API を呼び出せる

次章では、ここで取得した connpass API の情報を使って、自分の Web API（FastAPI）を作ってみましょう！

👉 次に進む：[第2章： FastAPI 環境の準備](2_setup-fastapi.md)