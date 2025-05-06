# モニタリング設定のデバッグ

## 演習の目的
この演習では、Prometheus を使ったアプリケーションの監視設定を学びます。
間違った設定を正しく修正して、アプリケーションのメトリクスが正しく収集されるようにします。

## 現在の状況

- Flask アプリケーションが `http://flask_app:5000` で動作しています
- Prometheus が `http://localhost:9090` で動作しています
- しかし、Prometheus のターゲットがダウンした状態になっています

## 課題

1. Prometheus の設定ファイル (`prometheus.yml`) を修正して、Flask アプリケーションのメトリクスを収集できるようにしてください
2. 修正後、Prometheus のターゲットページで `flask_app` が `UP` 状態になっていることを確認してください

## ステップバイステップガイド

1. まず、現在の設定を確認してください:
   ```bash
   cat prometheus.yml
   ```

2. 問題点を特定してください:
   - Flask アプリケーションは `flask_app:5000` で動作しています
   - しかし、Prometheus は `localhost:9999` を監視しようとしています

3. `prometheus.yml` を編集して、正しいターゲットを設定してください:
   ```yaml
   - job_name: 'flask_app'
     static_configs:
       - targets: ['flask_app:5000']  # ここを修正
   ```

4. 変更を適用するために、Prometheus を再起動してください:
   ```bash
   docker compose restart prometheus
   ```

5. Prometheus の Web UI でステータスを確認:
   - http://localhost:9090/targets にアクセス
   - `flask_app` のステータスが `UP` になっていることを確認

6. メトリクスが収集されているか確認:
   - http://localhost:9090/graph にアクセス
   - クエリフィールドに `http_requests_total` と入力
   - グラフが表示されれば成功

## ヒント

- Prometheus はコンテナ間で通信するため、サービス名をホスト名として使用できます
- ポート番号は、アプリケーションが実際にリッスンしているポートと一致させる必要があります
- 変更後は必ず Prometheus を再起動してください

## 確認方法

演習が完了したら、以下のコマンドで正しく設定できたか確認できます:

```bash
python3 ../../../../tools/cli/game.py play 02-monitor
```

## 発展課題（余裕があれば挑戦してみてください）

- Prometheus のアラートルールを追加してみましょう
- Grafana を追加して、ダッ�ボードを作成してみましょう
- カスタムメトリクスを追加して、Prometheus で収集してみましょう
