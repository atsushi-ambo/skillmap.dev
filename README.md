# Skillmap.dev - Ops Essentials

## 概要

Skillmap.dev は、ITインフラエンジニア向けの実践的な演習環境を提供するプロジェクトです。
このリポジトリには、ネットワークやシステム運用の基本を学ぶためのドキュメントと演習コンテンツが含まれています。

## 機能

- **インタラクティブなドキュメント**: 概念を学ぶためのマークダウンベースのドキュメント
- **ハンズオン演習**: 実際の環境で試しながら学べる実践的な課題
- **Mermaid 図解**: 概念を視覚的に理解するためのダイアグラム

## クイックスタート

### 前提条件

- Docker と Docker Compose がインストールされていること

### ローカルでの実行

1. リポジトリをクローン:
   ```bash
   git clone https://github.com/atsushi-ambo/skillmap.dev.git
   cd skillmap.dev
   ```

2. ドキュメントサーバーを起動:
   ```bash
   docker compose up docs
   ```

3. ブラウザで [http://localhost:8000](http://localhost:8000) にアクセス

## ドキュメントの構成

- **Ops Essentials**: インフラ運用の基礎からコスト設計まで
  - Level 1: 基礎知識とネットワーク
  - Level 2: 運用業務の基本
  - Level 3: スケーリングと高可用性
  - Level 4: 設計とコスト最適化

2. スライドを表示:
   ```bash
   docker compose --profile slides up
   ```
   ブラウザで http://localhost:1948 を開きます

3. 演習を開始:
   ```bash
   # ゲーム環境を起動
   docker compose --profile game up -d
   
   # 演習を開始
   python3 tools/cli/game.py play 01-network
   ```

## 利用可能な演習

### 1. ネットワーク設定のデバッグ

- **目的**: Docker のネットワーク設定とポートマッピングを学ぶ
- **学習内容**:
  - コンテナのポートマッピング
  - Nginx の基本的な設定
  - ネットワークトラブルシューティング

## トラブルシューティング

- コンテナが起動しない場合:
  ```bash
  # ログを確認
  docker logs skillmapdev-network_lab-1
  
  # コンテナを再起動
  docker compose --profile game down
  docker compose --profile game up -d
  ```

- ポートが競合する場合:
  ```bash
  # 使用中のポートを確認
  lsof -i :8080
  
  # 別のポートを使用する場合は、docker-compose.yml を編集
  ```

## ライセンス

MIT License