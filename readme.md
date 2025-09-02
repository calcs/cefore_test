# Cefore + cefpyco 開発環境メモ
Cefore（ICN/CCN実装？）とcefpyco（Pythonバインディング）をDocker上でサクッと動かす用。
producerの自動実行は行わないので、コンテナに入って手動起動してください。
とりあえずproducerはinterestを受け取ったら外部APIをたたいて結果を返す

## 前提
- Docker Desktop推奨(Windowsでの未確認している)
- 外のWebAPIをたたいているので、そこの通信許可

## ディレクトリ構成
```
cefore_test/  
├─ Dockerfile  
├─ docker-compose.yml  
└─ app/  
   ├─ producer.py   # ICN Interest を受けて REST を呼び、Data で返す  
   └─ consumer.py   # ICN Interest を送って Data を受け取る  
```

app/ は /workspace/app としてマウントされる

### 使い方
docker compose up -d
docker compose exec icn bash
python3 /workspace/app/producer.py

\# Consumer を実行（2つ目のシェルで）
docker compose exec icn bash -lc 'python3 /workspace/app/consumer.py'

\# 成功すると httpbin.org/get の JSON が表示されます。

## メモ
producer.pyはnohupとかでバックグラウンド起動させてもいいはず。
