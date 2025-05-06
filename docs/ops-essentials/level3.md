# Level 3 — Scale & High Availability { #level3 }
![Scale Icon](../../img/icons/scale.svg){ .icon style="color:#F59E0B" }
:tags: [scaling, ha, load-balancing]

!!! abstract "学習ゴール"
    1. スケーリングの基本戦略を理解する  
    2. 高可用性の仕組みと設計を学ぶ  
    3. ロードバランサーの設定と運用を習得する

## スケーリング戦略の基本

### スケールアップ vs スケールアウト

| 特徴 | スケールアップ | スケールアウト |
|------|--------------|--------------|
| 定義 | サーバーのリソースを増強 | サーバー台数を増やして分散 |
| メリット | 実装が簡単 | 可用性が高い |
| デメリット | 単一障害点のリスク | アプリケーションの対応が必要 |
| コスト | 高価になりがち | 段階的な拡張が可能 |
| 適したケース | 単一サーバーで十分な場合 | 高可用性が求められる場合 |

### 水平スケーリングのメリット
1. **耐障害性の向上**: 1台が停止しても他がカバー
2. **柔軟なリソース配分**: 需要に応じた柔軟な拡張
3. **ローリングアップデート**: ダウンタイムなしでの更新が可能

## 高可用性（HA）の基本

### 高可用性を実現する3つの要素
1. **冗長化**
   - 複数のサーバーで同じサービスを提供
   - データセンターのマルチAZ構成

2. **フェイルオーバー**
   - 障害発生時に自動で予備システムに切り替え
   - ヘルスチェックによる自動検知

3. **負荷分散**
   - リクエストを複数サーバーに分散
   - スティッキーセッションのサポート

## ロードバランサーの基本

### ロードバランサーの種類
1. **L4（レイヤー4）**
   - TCP/UDPレベルで動作
   - 高速だが、アプリケーション層の情報は見れない

2. **L7（レイヤー7）**
   - HTTP/HTTPSレベルで動作
   - URLパスやヘッダーに基づいたルーティングが可能

### ロードバランシングアルゴリズム
- ラウンドロビン
- リーストコネクション
- ソースIPハッシュ
- 最小応答時間

## ハンズオン: HAProxy による負荷分散

!!! tip "Lab 03 - ロードバランサーを設定"
    HAProxy を使って複数のWebサーバーに負荷分散します。
    
    ```bash
    # 3つのWebサーバーインスタンスを起動
    docker compose up -d --scale app=3 haproxy
    
    # ステータス確認
    docker ps
    ```
    
    - HAProxy Stats: http://localhost:1936 (admin:admin)
    - アプリケーション: http://localhost:8080

## ケーススタディ: Netflixのスケーリング戦略

Netflixは、マイクロサービスアーキテクチャとクラウドネイティブな設計により、世界中の1億人以上のユーザーにサービスを提供しています。

**主な取り組み**:
- すべてのサービスをステートレスに設計
- リージョン間のレイテンシーを考慮したマルチリージョン展開
- カオスエンジニアリングによる耐障害性テスト

## まとめチェックリスト

- [ ] スケールアップとスケールアウトの違いを説明できる
- [ ] 高可用性を実現する3つの要素を理解している
- [ ] ロードバランサーの種類と特徴を説明できる
- [ ] HAProxyの基本的な設定ができる
- [ ] 障害発生時の対応フローを理解している

## 理解度チェック

<details class="quiz">
  <summary>クイズ: スケーリング戦略</summary>
  <p>スケールアウトのメリットとして正しいものは？</p>
  <ul class="quiz-options">
    <li data-correct="true">耐障害性が向上する</li>
    <li data-correct="false">サーバー1台あたりの処理能力が向上する</li>
    <li data-correct="false">初期コストが安い</li>
    <li data-correct="false">メンテナンスが簡単</li>
  </ul>
</details>

<details class="quiz">
  <summary>クイズ: ロードバランサー</summary>
  <p>L7ロードバランサーの特徴として正しいものは？</p>
  <ul class="quiz-options">
    <li data-correct="true">HTTPヘッダーに基づいたルーティングが可能</li>
    <li data-correct="false">TCPレベルでのみ動作する</li>
    <li data-correct="false">SSL終端ができない</li>
    <li data-correct="false">レイヤー4で動作する</li>
  </ul>
</details>
<details class="quiz">
  <summary>クイズ: 高可用性</summary>
  <p>高可用性を実現するための要素でないものは？</p>
  <ul class="quiz-options">
    <li data-correct="false">冗長化</li>
    <li data-correct="false">フェイルオーバー</li>
    <li data-correct="true">単一障害点の導入</li>
    <li data-correct="false">ヘルスチェック</li>
  </ul>
</details>
