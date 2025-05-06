# Hands-on: ラボの遊び方

!!! tip "クイックスタート"
    ```bash
    # ラボ環境を起動
    docker compose --profile game up -d
    # ネットワーク演習を開始
    python3 tools/cli/game.py play 01-network
    ```

## ラボの特徴

- **実践的なシナリオ**: 実際のトラブルシューティングを想定した課題
- **段階的な学習**: 基礎から応用までステップバイステップで学べる
- **即時フィードバック**: 解答チェックで理解度を確認

## 収録ゲーム

| ID | テーマ | 学ぶこと | 想定時間 |
|----|--------|----------|----------|
| **01-network** | ポートマッピングデバッグ | Docker ネットワーク基礎・Nginx | 20分 |
| **02-monitor** | 監視入門 | Prometheus Exporter 追加 | 30分 |
| _Coming soon_ | ログ分析 | ELKスタック | - |

## 各ラボの進め方

### 1. ラボの開始

```bash
# 特定のラボを開始
python3 tools/cli/game.py play 01-network
```

### 2. 課題の確認

- 表示される問題文をよく読み、何を解決すべきか理解します
- 必要に応じて、ヒントを参照できます

### 3. 課題に取り組む

- 指示に従って環境を操作します
- 複数の方法で解決できる場合がありますので、自由に試してみてください

### 4. 解答チェック

```bash
# 解答をチェック
python3 tools/cli/game.py check
```

## トラブルシューティング

- **Dockerが起動しない場合**: `docker compose down` で一度クリーンアップしてから再起動
- **問題が表示されない場合**: ラボIDが正しいか確認してください
- **その他**: `python3 tools/cli/game.py --help` でヘルプを表示

## ラボの終了

```bash
# ラボ環境を停止
python3 tools/cli/game.py stop

# すべてのコンテナを削除
# docker compose down
```

## フィードバック

問題や改善点がありましたら、GitHubのIssueでお知らせください。

[新しいIssueを作成](https://github.com/your-username/skillmap.dev/issues/new)
