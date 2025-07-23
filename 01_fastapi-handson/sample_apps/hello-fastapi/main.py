from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/hello")
async def say_hello():
    return {"message": "こんにちは、FastAPI！"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # ダミーのユーザーリスト
    user_list = [
        {"user_id": 1, "name": "安藤"},
        {"user_id": 2, "name": "伊藤"},
        {"user_id": 3, "name": "遠藤"},
        {"user_id": 4, "name": "加藤"},
        {"user_id": 5, "name": "武藤"}
    ]
    # ユーザーIDに一致するユーザーを検索
    for user in user_list:
        if user["user_id"] == user_id:
            # ユーザーが見つかった場合、ユーザーデータを返す
            return user

    # ユーザーが見つからない場合
    return {"error": "User not found"}


@app.get("/search")
async def search(keyword: str = "default"):
    # 例として、クエリパラメータのキーワードをそのまま返す
    return {"keyword": keyword}


class Item(BaseModel):
    """
    アイテムのモデル
    """
    name: str
    price: float


@app.post("/items/")
async def create_item(item: Item):
    # 例として、受け取ったアイテムのデータをそのまま返す
    return {"name": item.name, "price": item.price}
