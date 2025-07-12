# 📘 第3章：connpass API を活用した実用的 API の構築

## 🎯 この章の目的
この章では、外部API（connpass API v2）を FastAPI でラップすることで、

* 外部の複雑なAPIを「わかりやすい」形に変換する方法
* 条件によるフィルタ処理やデータ整形の実装
* パラメータの受け取り（クエリ／パス／ボディ）の違い

を学びます。

FastAPI の「API設計力」と「柔軟性」の両方を体験する章です。

## 🔧 実装方針
この章では、1つの main.py に複数のエンドポイントを定義し、connpass API v2 をベースにした次のAPIを構築します：

| エンドポイント | メソッド | 説明 |
| ---- | ---- | ---- |
| `/events` | `GET` | キーワード検索（整形/生データ切り替え） |
| `/events/pref/{pref_name}` | `GET` | 都道府県でフィルタ |
| `/events/count` | `GET` | イベント件数のみ取得 |
| `/events/filter`  | `POST` | 柔軟な複数条件での検索 |

## 📄 main.py（全体構成）
以下に、FastAPI アプリ全体を構成する main.py のコードを記載します。

### 🔐 前提：API キー設定

`.env` ファイルの作成

```ini
CONNPASS_API_KEY=あなたのAPIキー
```

### ✅ 共通関数
```python
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
import httpx
from dotenv import load_dotenv
import os
load_dotenv()  # .env ファイルを読み込む

app = FastAPI()

# CORSの設定（開発中は "*" でもOK）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番では限定推奨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIキーを環境変数から取得
API_KEY = os.getenv("CONNPASS_API_KEY")
if not API_KEY:
    raise ValueError("API Key is not set.")

API_URL = "https://connpass.com/api/v2/events/"

# 共通のイベント取得関数
async def fetch_events(params: dict):
    headers = {"X-API-Key": API_KEY}
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(API_URL, headers=headers, params=params, timeout=10)
            res.raise_for_status()
            return res.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"connpass API エラー: {e}")
```
CORS 対応をここで設定することで、HTML/JS や外部サービスからのAPI呼び出しが可能になります。

### ✅ 1. /events – イベント一覧（整形 or フル）
```python
@app.get("/events")
async def get_events(
    keyword: str = "Python",
    count: int = Query(5, le=100),
    view: Literal["simple", "full"] = "simple"
):
    data = await fetch_events({"keyword": keyword, "count": count})
    events = data.get("events", [])

    if view == "full":
        return data

    simplified = [
        {
            "title": e["title"],
            "started_at": e["started_at"],
            "place": e.get("place"),
            "url": e["event_url"]
        } for e in events
    ]
    return {"results": simplified}
```

### ✅ 2. /events/pref/{pref_name} – 都道府県でフィルタ
```python
@app.get("/events/pref/{pref_name}")
async def get_events_by_prefecture(
    pref_name: str = Path(..., description="都道府県名（例: 山梨）"),
    keyword: str = "Python",
    count: int = Query(10, le=100),
    view: Literal["simple", "full"] = "simple"
):
    data = await fetch_events({"keyword": keyword, "count": count})
    events = data.get("events", [])

    filtered = [e for e in events if e.get("place") and pref_name in e["place"]]

    if view == "full":
        return {"results": filtered}

    simplified = [
        {
            "title": e["title"],
            "started_at": e["started_at"],
            "place": e.get("place"),
            "url": e["event_url"]
        } for e in filtered
    ]
    return {"results": simplified}
```

### ✅ 3. /events/count – 件数のみを返す
```python
@app.get("/events/count")
async def get_event_count(keyword: str = "Python"):
    params = {"keyword": keyword, "count": 1}
    data = await fetch_events(params)
    return {"count": data.get("results_available", 0)}
```

### ✅ 4. /events/filter – POSTで柔軟に検索

📦 リクエストモデル（Pydantic）
```python
class EventFilter(BaseModel):
    keyword: str = "Python"
    prefecture: str | None = None
    count: int = 10
    view: Literal["simple", "full"] = "simple"
```

📡 実装
```python
@app.post("/events/filter")
async def filter_events(filter: EventFilter):
    data = await fetch_events({"keyword": filter.keyword, "count": filter.count})
    events = data.get("events", [])

    if filter.prefecture:
        events = [e for e in events if e.get("place") and filter.prefecture in e["place"]]

    if filter.view == "full":
        return {"results": events}

    simplified = [
        {
            "title": e["title"],
            "started_at": e["started_at"],
            "place": e.get("place"),
            "url": e["event_url"]
        } for e in events
    ]
    return {"results": simplified}
```

## ✅ この章で学ぶ FastAPI 機能

| 機能 | エンドポイントでの使用例 |
| ---- | ---- |
| クエリパラメータ | `/events`, `/events/count` |
| パスパラメータ | `/events/pref/{pref_name}` |
| ボディパラメータ（Pydantic） | `/events/filter` |
| JSONレスポンス整形 | `view=simple` の実装 |
| 条件分岐・データ抽出 | `place` に都道府県名を含むかの判定 |

## 🔒 補足：CORS（クロスオリジン）の話
今回の構成では CORS を意識する必要は基本的にありません

* HTMLとJavaScriptは localhost:3000 から配信（Express）
* API呼び出しも同じ localhost:3000 に向けて実施（Nodeサーバ内でFastAPIに転送）

→ ブラウザから見たオリジン（プロトコル＋ドメイン＋ポート）は一貫して同じため、CORSは発生しません。

### ただし、以下のような構成では CORS が必要になります

| 状況 | 対応 |
| ---- | ---- |
| フロント（localhost:3000） → FastAPI（localhost:8000）に**直接fetch** | CORS 必要 |
| フロントを Vite や React で別ポートで開発 | CORS 必要 |
| API を AWS や外部サーバにデプロイ | **CORS 対応必須**（← 次章で扱います） |

フロントエンドや他のWebアプリからこのAPIを利用する場合、
ブラウザがCORS制限をかけて通信をブロックしてしまいます

FastAPI 側で CORS Middleware を設定することで、
意図的に外部からのアクセスを許可する必要があります

次章以降で扱う「AWS LambdaでAPIを公開」する際にも、CORS設定は非常に重要になります

## ✅ この章のまとめ

* connpass API を FastAPI で「ラップ」して、自分専用のAPIを設計
* クエリやPOST、整形レスポンスなど 柔軟で使いやすいAPIを自分で構築
* 今後の応用に向けて、CORS対応も含めた基本設定を理解

次章では、このAPIを実際にWeb UIから使ってみる体験に進みます。
ここまでで構築した FastAPI アプリはそのまま活用していきます。

👉 次に進む：[第4章：APIを実際に使ってみる体験（Webフロント × Node.js）](4_use-api.md)