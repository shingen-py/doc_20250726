# 📘 第2章：FastAPI 環境の準備

## 🎯 この章の目的
この章では、FastAPI を使って API サーバーを構築するための準備を行います。

* FastAPI の基本構造を知る
* 作業用ディレクトリをセットアップする
* 仮想環境を作成して依存ライブラリを導入する
* FastAPI アプリを起動して、API が動く状態を確認する

## 📦 2-1. FastAPI とは？

FastAPI は、Python で Web API を素早く簡単に構築できるフレームワークです。\
以下のような特徴があります：

| 特徴 | 内容 |
| ---- | ---- |
| 高速 | 非同期対応（`async`）で高速 |
| 型ヒント対応 | Python の型ヒントを活かして自動でバリデーションが可能 |
| ドキュメント自動生成 | OpenAPI / Swagger に対応し、ブラウザ上でAPIを操作できる画面が生成される |
| 学習コストが低い | Python の基本文法がわかれば使い始められる |

## 🧰 2-2. 作業ディレクトリの準備
作業用のディレクトリを作成し、移動します：

```bash
mkdir my-fastapi-app
cd my-fastapi-app
```
この中で Python プロジェクトを構築していきます。

## 🐍 2-3. 仮想環境の作成
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

## 📦 2-4. ライブラリのインストール
FastAPI および API呼び出し用の httpx、開発用サーバー uvicorn をインストールします。

```bash
pip install fastapi httpx uvicorn
```
※ uvicorn は FastAPI アプリを起動するためのサーバーです。

## 📄 2-5. 最小の FastAPI アプリを作ってみよう
エディタ（VS Code など）で main.py というファイルを作成し、以下のコードを入力します。

📄 main.py
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def say_hello():
    return {"message": "こんにちは、FastAPI！"}
```
このコードは、/hello というURLにアクセスすると「こんにちは、FastAPI！」という JSON を返すだけの最小構成です。

## 🚀 2-6. FastAPI アプリを起動する
ターミナルで次のコマンドを実行して、FastAPI アプリを起動します。

```bash
uvicorn main:app --reload
```
起動に成功すると、以下のようなメッセージが表示されます：

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```
ブラウザで以下のURLにアクセスしてください：

* http://127.0.0.1:8000/hello
→ JSON で {"message": "こんにちは、FastAPI！"} が表示されれば成功です。

## 🧪 2-7. Swagger UI を試す
FastAPI は、自動的に API ドキュメントを生成してくれます。

ブラウザで以下のURLにアクセスしてみましょう：

+ http://127.0.0.1:8000/docs

このページでは、提供している API エンドポイントを確認したり、ボタンでリクエストを送って実行結果を見ることができます。

Swagger UI と呼ばれるこの画面は、API 開発・テストにとても便利です。

## ❓ よくあるトラブルと対処法

| 状況 | 対処法 |
| ---- | ---- |
| `uvicorn: command not found` | 仮想環境が有効になっていない可能性があります。`source .venv/bin/activate` を再確認してください。 |
| `ModuleNotFoundError: fastapi` | ライブラリが入っていない可能性があります。`pip install fastapi` を再実行してください。 |
| アプリが起動しない／ポートが重複 | 既に `uvicorn` が起動している場合があります。`Ctrl+C` で停止してから再実行してください。 |

## ✅ この章のまとめ

* FastAPI の基本構成と、起動手順を理解しました
* 最小の API エンドポイント /hello を動かすことができました
* Swagger UI によって、視覚的に API を確認する方法を学びました

次章では、いよいよ connpass API v2 を FastAPI アプリの中から呼び出し、自作の API サーバを完成させていきます！

👉 次に進む：[第3章：connpass API を活用した実用的 API の構築](3_build-api.md)