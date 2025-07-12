# 📘 第4章：APIを実際に使ってみる体験（Webフロント × Node.js）

## 🎯 この章の目的
これまでに構築した FastAPI API が、実際の Web アプリケーションからどのように利用されるのかを体験します。\
今回は、HTML+JavaScript（fetch）で構築した Web フロントエンドを、Node.js + Express サーバーで配信し、FastAPI の API を呼び出す構成で進めます。

### この章で得られること

* **Web アプリケーションから API を使う流れ**を体験
* **Node.js を使った軽量なローカル Web サーバー構成**を知る
* **ユーザー操作（都道府県選択＋検索）→ API 呼び出し → 結果表示**の流れを学ぶ

## 🧭 システム構成図

```plaintext
[ブラウザ]
   |
   | fetch /api/search
   v
[Node.js + Express (http://localhost:3000)]
   |
   | fetch /events/filter
   v
[FastAPI (http://localhost:8000)]
```

## 🧱 ディレクトリ構成

```plaintext
node-client/
├── index.js          ← Node.js サーバー
└── public/
    └── index.html    ← HTML + JavaScript
```

## 🛠 セットアップ

```bash
mkdir node-client
cd node-client
npm init -y
npm install express node-fetch
```

## 📄 index.js（Node.js + Express サーバー）

```js
const express = require('express');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const PORT = 3000;
const FASTAPI = 'http://localhost:8000';

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// POST /api/search → FastAPI の /events/filter に転送
app.post('/api/search', async (req, res) => {
  try {
    const response = await fetch(`${FASTAPI}/events/filter`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error('API呼び出し失敗:', err);
    res.status(500).send('検索に失敗しました');
  }
});

app.listen(PORT, () => {
  console.log(`✅ Webサーバー起動：http://localhost:${PORT}`);
});
```

## 📄 public/index.html（都道府県選択付き検索UI）
```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <title>イベント検索</title>
</head>
<body>
  <h1>イベント検索（都道府県付き）</h1>

  <label>
    キーワード:
    <input id="kw" placeholder="例: Python" />
  </label>

  <label>
    都道府県:
    <select id="pref">
      <option value="">--選択してください--</option>
      <option value="山梨">山梨</option>
      <option value="東京">東京</option>
      <option value="大阪">大阪</option>
      <!-- 必要に応じて他の県も追加 -->
    </select>
  </label>

  <button onclick="search()">検索</button>

  <ul id="results"></ul>

  <script>
    async function search() {
      const kw = document.getElementById('kw').value;
      const pref = document.getElementById('pref').value;

      const res = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keyword: kw,
          prefecture: pref,
          count: 10,
          view: 'simple'
        })
      });

      const data = await res.json();
      const ul = document.getElementById('results');
      ul.innerHTML = "";
      data.results.forEach((e) => {
        const li = document.createElement("li");
        li.innerHTML = `<a href="${e.url}" target="_blank">${e.title}</a>（${e.place ?? '場所未定'}）`;
        ul.appendChild(li);
      });
    }
  </script>
</body>
</html>
```

## ✅ 動作手順

FastAPI サーバーを起動
```bash
vicorn main:app --reload
```

Node.js サーバーを起動
```bash
node index.js
```

ブラウザでアクセス
```
http://localhost:3000
```

## ✅ この章のまとめ

* Web フロントからの API 利用方法を体験しました
* UI操作（キーワード + 都道府県選択）と API を連携させた検索機能を実装しました
* Node.js の役割（静的ファイルの配信と API プロキシ）を理解しました
* 「API を作るだけでなく、使ってもらう設計」が重要であることを学びました

次章では、ここまでのハンズオンの振り返りと、FastAPIやAPI構築を今後どのように活かしていくかを考えます。

👉 次に進む：[第5章：振り返りと今後のステップ）](5_summary.md)
