# Level 3 — Scale & HA { #level3 }
![Scale Icon](../img/icons/scale.svg){ .icon style="color:#F59E0B" }

!!! abstract "学習ゴール"
    1. スケーリングの基本を理解する  
    2. 高可用性の仕組みを学ぶ  
    3. ロードバランサーを設定できる

## スケーリング戦略

### スケールアップ vs スケールアウト
- **スケールアップ**: サーバーのリソースを増強
- **スケールアウト**: サーバー台数を増やして分散

## ハンズオン: ロードバランサー

!!! warning "Lab 03 - ロードバランサーを設定しよう"
    HAProxy を使って複数インスタンスに負荷分散します。

```bash
docker compose up -d --scale app=3 haproxy
```

[次のレベルへ →](../ops-essentials/level4.md){ .md-button }
