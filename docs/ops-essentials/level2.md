# Level 2 — Ops Routine & Monitoring { #level2 }
![icon](../../img/icons/monitor.svg){ .icon style="color:#10B981" }
:tags: [cron, monitoring, linux]

!!! abstract "学習ゴール"
    1. 定期的なタスクの管理方法を理解する  
    2. 効果的な監視戦略を設計できるようになる  
    3. ログ収集・分析のベストプラクティスを学ぶ

## ジョブスケジューリングの比較

| 機能 | Cron | at | systemd-timer |
|------|------|----|--------------|
| 実行タイミング | 定期的に繰り返し | 1回のみ | 複雑なスケジュール可能 |
| 設定方法 | crontab -e | at コマンド | .timer ユニットファイル |
| ログ管理 | 個別設定が必要 | 個別設定が必要 | journaldと統合 |
| 依存関係 | なし | なし | 他のユニットと連携可能 |
| 使用例 | 定期的なバックアップ | メンテナンス通知 | 依存関係のあるタスク |

### 異常通知の設定例 (Cron)
```bash
0 2 * * * /path/to/backup.sh || curl -X POST -H 'Content-type: application/json' --data '{"text":"バックアップに失敗しました"}' $SLACK_WEBHOOK_URL
```

### systemd-timer の設定例
```ini
# backup.timer
[Unit]
Description=Run backup daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

## 監視の3つの視点

### 1. 死活監視
**目的**: サービスが正しく動作しているかどうかを確認
- ポートの応答確認
- HTTPステータスコードのチェック
- プロセスの生存確認

### 2. リソース監視
**目的**: システムリソースの使用状況を把握
- CPU使用率
- メモリ使用量
- ディスクI/O
- ネットワーク帯域

### 3. ログ監視
**目的**: 問題の早期発見と分析
- エラーログの検出
- アクセスログの分析
- セキュリティイベントの監視

## 監視フローの詳細

### Prometheus メトリクス収集フロー

```mermaid
sequenceDiagram
    participant App as アプリケーション
    participant Exp as Exporter
    participant Prom as Prometheus
    participant Graf as Grafana
    participant Alert as Alertmanager

    App->>Exp: /metrics エンドポイント公開
    Prom->>Exp: 15秒ごとにスクレイプ
    Prom->>Prom: ルール評価
    Prom->>Alert: アラート発行
    Alert->>Slack: 通知送信
    Prom->>Graf: メトリクス提供
    Graf->>User: ダッシュボード表示
```

### 監視アーキテクチャ

```mermaid
graph LR
    subgraph ターゲット
        A[アプリケーション]
        B[Node Exporter]
        C[Database]
    end
    
    subgraph Prometheus
        D[Prometheus Server]
    end
    
    subgraph 可視化
        E[Grafana]
    end
    
    subgraph アラート
        F[Alertmanager]
        G[Email/Slack]
    end
    
    A -->|メトリクス| D
    B -->|システムメトリクス| D
    C -->|DBメトリクス| D
    D -->|クエリ| E
    D -->|アラートルール| F
    F -->|通知| G
```

## ハンズオン: 監視システム構築

!!! tip "Lab 02 - 監視システムを構築"
    PrometheusとGrafanaを使用して監視システムを構築します。
    
    ```bash
    # 監視システムの起動
    docker compose up -d prometheus grafana
    
    # 起動確認
    docker ps
    ```
    
    - Prometheus: http://localhost:9090
    - Grafana: http://localhost:3000 (admin/admin)

## ケーススタディ: Airbnbの監視戦略

Airbnbは、初期段階ではcronを多用していましたが、スケーラビリティの問題に直面しました。タスクの依存関係の管理や、失敗したジョブの再実行が困難だったためです。

2014年、AirbnbはAirflowを開発し、cronから移行しました。これにより：

- ワークフローの視覚化
- 依存関係の管理
- 失敗時の自動リトライ
- 実行履歴の追跡

が可能になり、データパイプラインの信頼性が大幅に向上しました。

## まとめチェックリスト

- [ ] cronとatの違いを説明できる
- [ ] 監視の3つの視点を説明できる
- [ ] Prometheusの基本的なアーキテクチャを理解している
- [ ] 監視システムの構築手順を理解している
- [ ] ログ管理のベストプラクティスを説明できる

## 理解度チェック

<details class="quiz">
  <summary>クイズ: Cronの特徴</summary>
  <p>Cronの特徴として正しいものは？</p>
  <ul class="quiz-options">
    <li data-correct="true">定期的なタスクの実行に適している</li>
    <li data-correct="false">1回限りのタスクに最適</li>
    <li data-correct="false">GUIでのみ設定可能</li>
    <li data-correct="false">Windows専用のツール</li>
  </ul>
</details>

<details class="quiz">
  <summary>クイズ: 監視の基本</summary>
  <p>システム監視において、リソース監視に含まれるのは？</p>
  <ul class="quiz-options">
    <li data-correct="true" data-explain="CPU使用率はシステムの処理能力を計測する重要なリソース監視項目です。ボトルネックの特定やキャパシティプランニングに役立ちます。">CPU使用率</li>
    <li data-correct="true" data-explain="メモリ使用量はシステムのパフォーマンスに直結する重要なリソース指標で、メモリリークの検出にも役立ちます。">メモリ使用量</li>
    <li data-correct="false" data-explain="HTTPステータスコードはアプリケーション監視の項目で、リソース監視には含まれません。">HTTPステータスコード</li>
    <li data-correct="true" data-explain="ディスクI/Oはストレージのパフォーマンスを計測する重要なリソース監視項目です。">ディスクI/O</li>
  </ul>
</details>

<details class="quiz">
  <summary>クイズ: ログ管理</summary>
  <p>ログ管理で重要な「3-2-1ルール」とは？</p>
  <ul class="quiz-options">
    <li data-correct="false" data-explain="ログレベルの数や保存先の数は、3-2-1ルールとは関係ありません。">3つのログレベル、2つの保存先、1つのバックアップ</li>
    <li data-correct="true" data-explain="3-2-1ルールとは、データ保護のベストプラクティスで、3つのコピーを2つの異なるメディアに保存し、そのうち1つはオフサイトに保管するというものです。これにより、災害時やシステム障害時のデータ損失リスクを最小限に抑えられます。">3つのコピー、2つのメディア、1つはオフサイト</li>
    <li data-correct="false" data-explain="ログの取得間隔や保持期間は、3-2-1ルールとは異なる概念です。">3時間ごとのログ取得、2時間の保持、1週間のアーカイブ</li>
    <li data-correct="false" data-explain="監視項目やアラートの数は、3-2-1ルールとは無関係です。">3つの監視項目、2つのアラート、1つのダッシュボード</li>
  </ul>
</details>

[次のレベルへ →](../ops-essentials/level3.md){ .md-button }
