from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app.get("/hello")
async def say_hello():
    return {"message": "こんにちは、FastAPI！"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # 例として、パスパラメータのユーザIDをそのまま返す
    return {"user_id": user_id}


@app.get("/search")
async def search(keyword: str = "default"):
    # 例として、クエリパラメータのキーワードをそのまま返す
    return {"keyword": keyword}


@app.post("/items/")
async def create_item(item: Item):
    # 例として、受け取ったアイテムのデータをそのまま返す
    return {"name": item.name, "price": item.price}
