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

# 検索条件（キーワード: Python）
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
