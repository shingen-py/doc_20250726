from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()  # .env ファイルを読み込む

app = FastAPI()

app.title = "Event API"
app.description = "connpass からイベント情報を取得する API"
app.version = "1.0.0"

# CORS(Cross-Origin Resource Sharing) 設定
app.add_middleware(
    CORSMiddleware,
    # 許可するオリジンを指定(本番では適切なオリジンに制限すること)
    allow_origins=["*"],
    # 認証情報を含むリクエストを許可
    allow_credentials=True,
    # 許可するHTTPメソッドを指定
    allow_methods=["*"],
    # 許可するHTTPヘッダーを指定
    allow_headers=["*"],
)

# APIキーを環境変数から取得
API_KEY = os.getenv("CONNPASS_API_KEY")

# connpass API の URL
# BASE_URL = "https://connpass.com/api/v2"  # 公式の connpass API
BASE_URL = "https://proxy01.yamanashi.dev"  # 勉強会用のプロキシサーバー


# ---- 共通のイベント取得関数 ----
async def fetch_events(
    event_id: int | None = None,    # イベントIDでの絞り込み
    keyword: str | None = None,     # キーワードでの絞り込み
    subdomain: str | None = None,   # サブドメイン(グループ)での絞り込み
    prefecture: str | None = None,  # 都道府県での絞り込み
    order: int = 2,                 # 検索結果の表示順(2: 開始日時の降順)
    count: int = 10,                # 取得件数
):
    """
    connpass API からイベント情報を取得する共通関数
    """
    url = f"{BASE_URL}/events/"
    headers = {"X-API-Key": API_KEY}
    params = {
        "event_id": event_id,
        "keyword": keyword,
        "subdomain": subdomain,
        "prefecture": prefecture,
        "order": order,
        "count": count,
    }
    print(f"Fetching events with params: {params}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            raise HTTPException(status_code=500,
                                detail=f"connpass API エラー: {e}")


# ---- イベント一覧取得エンドポイント ----
@app.get("/events")
async def get_events(
    keyword: str = "",
    limit: int = 10
):
    """
    イベントの一覧を取得するエンドポイント
    """
    data = await fetch_events(
        keyword=keyword,
        count=limit
    )
    events = data.get("events", [])

    return [
        {
            "id": event["id"],                  # イベントID
            "title": event["title"],            # イベント名
            "url": event["url"],                # connpass.com上のURL
            "started_at": event["started_at"],  # イベント開始日時
            "place": event.get("place"),        # 開催会場
        } for event in events
    ]


# ---- イベント詳細取得エンドポイント ----
@app.get("/events/{event_id}/detail")
async def get_event_detail(event_id: int):
    """
    イベントの詳細情報を取得するエンドポイント
    """
    data = await fetch_events(event_id)

    if not data or "events" not in data or len(data["events"]) == 0:
        raise HTTPException(status_code=404, detail="イベントが見つかりません")

    event = data["events"][0]

    return {
        "id": event["id"],                              # イベントID
        "title": event["title"],                        # イベント名
        "catch": event.get("catch"),                    # キャッチ
        "description": event.get("description"),        # 概要
        "url": event["url"],                            # connpass.com上のURL
        "started_at": event["started_at"],              # イベント開始日時
        "ended_at": event.get("ended_at"),              # イベント終了日時
        "group": event.get("group", {}).get("title"),   # グループ名
        "address": event.get("address"),                # 開催場所
        "place": event.get("place"),                    # 開催会場
    }


# ---- 都道府県別イベント取得エンドポイント ----
@app.get("/events/pref/{prefecture}")
async def get_events_by_prefecture(
    prefecture: str = Path(..., description="都道府県（例: yamanashi）"),
    keyword: str = "",
    limit: int = 10
):
    """
    都道府県別のイベントを取得するエンドポイント
    """
    data = await fetch_events(
        keyword=keyword,
        prefecture=prefecture,
        count=limit
    )
    events = data.get("events", [])

    return [
        {
            "id": event["id"],                  # イベントID
            "title": event["title"],            # イベント名
            "url": event["url"],                # connpass.com上のURL
            "started_at": event["started_at"],  # イベント開始日時
            "place": event.get("place"),        # 開催会場
        } for event in events
    ]


# ---- グループ別イベント取得エンドポイント ----
@app.get("/events/group/{subdomain}")
async def get_events_by_group(
    subdomain: str = Path(..., description="グループのサブドメイン（例: shingenpy, jaws-ug-yamanashi）"),
    keyword: str = "",
    limit: int = 10
):
    """
    グループ別のイベントを取得するエンドポイント
    """
    data = await fetch_events(
        keyword=keyword,
        subdomain=subdomain,
        count=limit
    )
    events = data.get("events", [])

    return [
        {
            "id": event["id"],                  # イベントID
            "title": event["title"],            # イベント名
            "url": event["url"],                # connpass.com上のURL
            "started_at": event["started_at"],  # イベント開始日時
            "place": event.get("place"),        # 開催会場
        } for event in events
    ]


# ---- イベント数取得エンドポイント ----
@app.get("/events/count")
async def get_event_count(keyword: str = ""):
    """
    イベントの総件数を取得するエンドポイント
    """
    data = await fetch_events(
        keyword=keyword,
        count=1
    )
    count = data.get("results_available", 0)    # 検索結果の総件数

    return {"count": count}


class EventFilter(BaseModel):
    """
    イベント検索リクエストのモデル
    """
    keyword: str = ""
    prefecture: str | None = None
    subdomain: str | None = None
    limit: int = 10


# ---- イベント検索エンドポイント ----
@app.post("/events/filter")
async def filter_events(filter: EventFilter):
    """
    イベントをキーワード、都道府県、グループで検索するエンドポイント
    """
    data = await fetch_events(
        keyword=filter.keyword,
        prefecture=filter.prefecture,
        subdomain=filter.subdomain,
        count=filter.limit
    )
    events = data.get("events", [])

    return [
        {
            "id": event["id"],                  # イベントID
            "title": event["title"],            # イベント名
            "url": event["url"],                # connpass.com上のURL
            "started_at": event["started_at"],  # イベント開始日時
            "place": event.get("place"),        # 開催会場
        } for event in events
    ]
