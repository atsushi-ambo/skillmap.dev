# ネットワーク設定のデバッグ演習

## 演習の目的
この演習では、Docker のネットワーク設定とポートマッピングについて学びます。
コンテナ内で動作するアプリケーションに、ホストマシンからアクセスするための基本的な設定方法を理解します。

## 課題
Nginx ウェブサーバーが正しく動作するように、`docker-compose.yml` ファイルを修正してください。

## 現在の状態
- Nginx はコンテナ内の 8000 番ポートでリッスンするように設定されています
- しかし、`docker-compose.yml` のポートマッピングが正しく設定されていないため、ホストマシンからアクセスできません

## 目標
1. `docker-compose.yml` を編集して、ホストマシンの 8080 番ポートが Nginx コンテナの 8000 番ポートに正しくマッピングされるようにする
2. 修正後、以下のコマンドで動作確認する
   ```bash
   python3 tools/cli/game.py play 01-network
   ```

## ステップバイステップガイド

1. まず、`docker-compose.yml` ファイルを開いてください
   ```bash
   code ops-essentials/games/01-network/docker-compose.yml
   ```

2. `ports` セクションを確認します。現在は以下のようになっています：
   ```yaml
   ports:
     - "8080:8000"  # 意図的に間違ったマッピング
   ```

3. ポートマッピングのフォーマットは `ホストポート:コンテナポート` です。
   Nginx はデフォルトで 80 番ポートでリッスンするため、コンテナポートを 80 に変更します。

4. 以下のように修正してください：
   ```yaml
   ports:
     - "8080:80"  # ホストの8080 → コンテナの80
   ```

5. 変更を保存したら、以下のコマンドでコンテナを再起動します：
   ```bash
   docker compose --profile game down
   docker compose --profile game up -d
   ```

6. 最後に、以下のコマンドで正しく修正できたか確認します：
   ```bash
   python3 tools/cli/game.py play 01-network
   ```

## ヒント
- `docker ps` コマンドで、コンテナのポートマッピングを確認できます
- `curl -v http://localhost:8080` で、Nginx の応答を直接確認できます
- 問題が解決しない場合は、Nginx のログを確認してみてください：
  ```bash
  docker logs skillmapdev-network_lab-1
  ```

## 発展課題（余裕があれば挑戦してみてください）
- ホストマシンの異なるポート（例: 8081）で Nginx にアクセスできるように設定を変更してみてください
- Nginx の設定ファイル (`nginx.conf`) を編集して、カスタムのウェルカムメッセージを表示するように変更してみてください
