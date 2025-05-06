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

[次のレベルへ →](../ops-essentials/level3.md){ .md-button }
