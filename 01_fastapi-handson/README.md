# 🚀 FastAPI を使った APIサーバー構築ハンズオン

このハンズオンでは、**connpass API v2 を題材に、FastAPI を使って API サーバを構築し、Web アプリケーションから利用するところまで**を体験します。

---

## 🎯 ハンズオンのゴール

- 公開 API（connpass API v2）を理解して使えるようになる
- FastAPI を使って独自の API を構築できるようになる
- 作成した API を Web アプリケーションから利用できる

---

## 🚀 サンプルコード

- [こちらからダウンロードください](https://github.com/shingen-py/doc_20250726/tree/main/01_fastapi-handson/sample_apps)

---


## 🗂 目次

### [第1章：connpass API v2 の仕組みと体験](docs/1_try-connpass-api.md)(15分)
- API の仕様とできることを把握
- キーワード検索などを使ってみる

### [第2章：FastAPI 環境の準備](docs/2_setup-fastapi.md)(15分)
- FastAPI + Uvicorn のインストールと初期設定
- 簡単な FastAPI アプリの作成
- Swagger UI による API 動作確認
- FastAPI のクエリパラメータ・パスパラメータの扱い

### [第3章：connpass API を活用した実用的 API の構築](docs/3_build-api.md)(30分)
- キーワード検索API
- 都道府県フィルター付きAPI

### [第4章：APIを実際に使ってみる（Webフロント）](docs/4_use-api.md)(15分)
- HTML + fetch による簡易 UI 作成
- 都道府県セレクトボックスによる検索条件操作
- 実際にAPIをフロントから呼び出して使ってみる

### [第5章：まとめと今後のステップ](docs/5_summary.md)(5分)
- 学んだことの整理
- 公開API化に向けた展望

---

## 🛠 使用技術・ツール

| 種類 | ツール |
|------|--------|
| 言語 | Python 3.12+, JavaScript |
| フレームワーク | FastAPI |
| API | [connpass API v2](https://connpass.com/about/api/v2/) |
| 実行ツール | uvicorn, httpx, pydantic |
| テスト用 | curl, ブラウザ, Swagger UI |

---

## 📦 セットアップ手順（ローカル実行）

### 1. Python 仮想環境作成

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):
```powershell
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

### 3. `.env` ファイルの作成

```ini
CONNPASS_API_KEY=あなたのAPIキー
```

### 4. FastAPI アプリ起動

```bash
cd /path/to/my-event-api
uvicorn main:app --reload
```

### 5. ローカルHTTPサーバ起動（別ターミナル）

```bash
cd /path/to/my-event-frontend
python -m http.server 3000
```

### 6. ブラウザでアクセス

http://localhost:3000

---

## 🔜 次のステップ：APIをインターネットに公開しよう

このハンズオンの続編として、**「AWS Lambda を使ったAPI公開ハンズオン」** も用意されています。  
作成した FastAPI アプリをサーバーレスで公開し、誰でも使えるようにする方法を体験できます。

## 📎 補足資料・リンク

* connpass API v2 ドキュメント: https://connpass.com/about/api/v2/
* FastAPI 公式: https://fastapi.tiangolo.com/
* Shingen.py: https://shingenpy.connpass.com/

