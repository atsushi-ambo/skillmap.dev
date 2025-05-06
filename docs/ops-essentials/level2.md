# Level 2 — Ops Routine { #level2 }
![Monitor Icon](../img/icons/monitor.svg){ .icon style="color:#10B981" }

!!! abstract "学習ゴール"
    1. システム監視の基本を理解する  
    2. ログ管理の重要性を学ぶ  
    3. バックアップ戦略を設計できる

## 監視の基本

### 監視の4つの観点
1. **リソース監視** (CPU, メモリ, ディスク)
2. **サービス監視** (HTTP, TCP)
3. **ログ監視** (エラーログ, アクセスログ)
4. **ビジネスKPI** (リクエスト数, エラー率)

## ハンズオン: 監視システムの構築

!!! warning "Lab 02 - 監視システムを構築しよう"
    Prometheus と Grafana をセットアップします。

```bash
docker compose up -d prometheus grafana
```

Grafana にログインして、ダッシュボードを確認しましょう。

## 理解度チェック

<details class="quiz">
  <summary>クイズ: 監視の基本</summary>
  <p>システム監視において、リソース監視に含まれないものは？</p>
  <ul class="quiz-options">
    <li data-correct="false">CPU使用率</li>
    <li data-correct="false">メモリ使用量</li>
    <li data-correct="true">HTTPステータスコード</li>
    <li data-correct="false">ディスク使用量</li>
  </ul>
</details>

<details class="quiz">
  <summary>クイズ: ログ管理</summary>
  <p>ログ管理で重要な「3-2-1ルール」とは？</p>
  <ul class="quiz-options">
    <li data-correct="false">3つのログレベル、2つの保存先、1つのバックアップ</li>
    <li data-correct="true">3つのコピー、2つのメディア、1つはオフサイト</li>
    <li data-correct="false">3時間ごとのログ取得、2時間の保持、1週間のアーカイブ</li>
    <li data-correct="false">3つの監視項目、2つのアラート、1つのダッシュボード</li>
  </ul>
</details>

<details class="quiz">
  <summary>クイズ: バックアップ戦略</summary>
  <p>バックアップ戦略を立てる際に考慮すべきでない要素は？</p>
  <ul class="quiz-options">
    <li data-correct="false">RPO (目標復旧時点)</li>
    <li data-correct="false">RTO (目標復旧時間)</li>
    <li data-correct="true">CPUのクロック速度</li>
    <li data-correct="false">バックアップの保存期間</li>
  </ul>
</details>

[次のレベルへ →](../ops-essentials/level3.md){ .md-button }
