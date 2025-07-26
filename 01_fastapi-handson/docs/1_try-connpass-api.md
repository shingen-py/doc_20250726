# 📘 第1章：connpass API v2 の仕組みと体験
🕒本章の作業時間：15分

## 🎯 この章の目的
この章では、以下のことを体験します。

* connpass API v2 がどのような仕組みで動いているのかを知る
* 実際に HTTP リクエストを使って connpass からイベントデータを取得する
* 今後作る FastAPI アプリの「土台になる部分」を理解する

## 🔍 1-1. API とは何か？

**API（Application Programming Interface）** とは、他のアプリケーションとプログラムでやり取りをするための「窓口」です。

たとえば、connpass というサービスの中にある「イベント情報を検索する機能」を、他のアプリからも利用できるようにしたものが connpass API です。

## 🧾 1-2. connpass API v2 の特徴
* URL：`https://connpass.com/api/v2`
* 認証：APIキーが必要（X-API-Keyヘッダーで送信）
* データ形式：JSON
* 利用制限：1秒に1回までのリクエスト（Rate limit）

APIの利用申請方法は公式ページに案内があります（ https://connpass.com/about/api/v2/ ）

### connpass API で取得できるデータ

| エンドポイント | 説明 | 取得できる情報 |
| ---- | ---- | ---- |
| `/events/` | イベント情報 | タイトル、日時、場所、主催者、参加者数など |
| `/events/{id}/presentations/` | 資料情報 | タイトル、発表者、URLなど |
| `/groups/` | グループ情報 | タイトル、概要、主催者など |
| `/users/` | ユーザー情報 | 表示名、画像URL、参加イベント数など |
| `/users/{nickname}/groups/` | ユーザーが所属するグループ情報 | グループ名、概要、主催者など |
| `/users/{nickname}/attended_events/` | ユーザーが参加したイベント情報 | イベント名、日時、場所など |
| `/users/{nickname}/presenter_events/` | ユーザーが発表したイベント情報 | イ   ベント名、日時、場所など |

### 本日の勉強会での利用環境について
* 本日の勉強会では、事前に Shingen.py で connpass に申請済みのAPIキーを使用して connpass API を実行します。
* APIキーの第三者への漏洩を防ぐため、本日の勉強会のために用意した**APIプロキシサーバー** を介して connpass API を呼び出します。
  * APIプロキシサーバー：`https://proxy01.yamanashi.dev`
  * APIプロキシサーバーのソースコードは[こちら](https://github.com/yuukis/connpass-api-proxy)で公開しています
* 多くのリクエストに対応するため、プロキシサーバーではAPIのレスポンスをキャッシュしており、connpass API への呼び出し回数を減らしています。

```plaintext
[クライアント]
   |
   | プロキシサーバー用のAPIキーを指定してリクエスト
   v
[APIプロキシサーバー (https://proxy01.yamanashi.dev)]
   |
   | connpass API 用のAPIキーを指定してリクエスト
   v
[connpass API v2 (https://connpass.com/api/v2)]
```

## 🖥 1-3. ターミナルからAPIを直接呼び出す方法
### 🎯 目的
Pythonでプログラムを書く前に、まずは 「手動でAPIを叩いてみる」 ことで、

* HTTPリクエストの構造
* APIキーの必要性
* ヘッダーやクエリパラメータの使い方

を体験的に理解しましょう。

### 🖥 curl を使ってAPIを呼び出す
curl はほとんどの OS に標準で入っているコマンドラインツールです。

✅ 基本構文
```bash
curl -H "X-API-Key: あなたのAPIキー" "URL"
```
✅ 実行例①：イベントを取得（APIキーを仮に `abcd1234` とした場合）
```bash
curl -H "X-API-Key: abcd1234" "https://proxy01.yamanashi.dev/events/?keyword=Python&count=1"
```
📌 うまくいくと…
```text
{"results_start":1,"results_returned":1,"results_available":1234,"events":[{"event_id":...}]}
```
❗失敗例（APIキーなし）
```bash
curl "https://proxy01.yamanashi.dev/events/?keyword=Python"
```
```json
{"error":"Unauthorized"}
```
X-API-Key ヘッダーを付けないと、401 Unauthorized（認証エラー）になります。

✅ 実行例②：特定のユーザーが参加しているイベントを取得（APIキーを仮に `abcd1234` とした場合）
```bash
curl -H "X-API-Key: abcd1234" "https://proxy01.yamanashi.dev/users/yuukis/attended_events/"
```
📌 うまくいくと…
```text
{"results_returned":10,"results_available":312,"results_start":1,"events":[{"id":354581,"title":"出張版！甲斐国もくもく会 in 北杜市 (清里/オンライン)","catch":"北杜市民の方大歓迎！廃校の小学校の教室でもくもく作業しながらの交流会","description":"<p>山梨開催のもくもく会、 <strong>甲斐国（かいのくに）もくもく会</strong> です！</p>\n<p>「もくもく会」とは、複数の人が集ま
...
```


## 📦 1-4. PythonでAPIを呼び出す

### 1-4-1. 仮想環境の作成
仮想環境を作成し、他のプロジェクトと依存パッケージが混ざらないようにします。

✅ macOS / Linux の場合
```bash
python3 -m venv .venv
source .venv/bin/activate
```
✅ Windows の場合（PowerShell）
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 1-4-2. 作業ディレクトリの準備
作業用のディレクトリを作成し、移動します：

```bash
mkdir try-connpass-api
cd try-connpass-api
```
この中で Python プロジェクトを構築していきます。

### 1-4-3. 必要なライブラリをインストール
まずはAPIを呼び出すために、Pythonのライブラリ httpx、`.env` ファイルを読み込むためのライブラリ python-dotenv をインストールします。

```bash
pip install httpx python-dotenv
```

### 1-4-4. APIキーの安全な管理：`.env` ファイルを使おう

APIキーは直接コードに書くのではなく、`.env` ファイルを使って管理しましょう。  
これにより、**キーの流出防止**や **コード共有時の安全性向上**が図れます。

`.env` ファイルの作成

```ini
CONNPASS_API_KEY=あなたのAPIキー
```
🔐 注意：APIキーを、配布されたものに置き換えてください

以下のコードで、`.env` ファイルから API キーを読み込むことができます。

```python
from dotenv import load_dotenv
import os
load_dotenv()  # .env ファイルを読み込む

# APIキーを環境変数から取得
API_KEY = os.getenv("CONNPASS_API_KEY")
```

### 1-4-5. connpass API を叩いてみよう（サンプルコード）
以下のコードを main.py という名前で保存して、実行してみましょう。

```python
import httpx
from dotenv import load_dotenv
import os
import pprint  # 見やすく出力するためのモジュール

load_dotenv()  # .env ファイルを読み込む

# APIキーを環境変数から取得
API_KEY = os.getenv("CONNPASS_API_KEY")

# connpass API v2 の URL
# url = "https://connpass.com/api/v2/events/"
url = "https://proxy01.yamanashi.dev/events/"

# 検索条件（キーワード: 山梨県立図書館）
params = {
    "keyword": "山梨県立図書館",
    "count": 3  # 取得件数
}

# APIキーを指定したヘッダー
headers = {
    "X-API-Key": API_KEY
}

# リクエスト送信
response = httpx.get(url, params=params, headers=headers)

# レスポンスの JSON を整形して出力
if response.status_code == 200:
    data = response.json()
    pprint.pprint(data)
else:
    print("エラーが発生しました:", response.text)
```

実行方法
```bash
python main.py
```

### 1-4-6. 実行結果の見方
実行すると、以下のような出力が得られます（一部抜粋）：

```text
{'events': [{'accepted': 7,
             'address': '山梨県甲府市北口２丁目８−１ 山梨県立図書館',
             'catch': '毎月最終日曜日に開催している山梨のもくもく会！',
             'description': '<p>山梨開催のもくもく会、 <strong>甲斐国（かいのくに）もくもく会</strong> '
                            'です！\n'
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
* connpass API v2 は、イベント情報などを取得できる便利な Web API
* API を呼び出すには、URL・クエリパラメータ・HTTPヘッダーの3つが重要
* Python の httpx を使って簡単に API を呼び出せる

次章では、ここで取得した connpass API の情報を使って、自分の Web API（FastAPI）を作ってみましょう！

👉 次に進む：[第2章： FastAPI 環境の準備](2_setup-fastapi.md)