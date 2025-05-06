#!/usr/bin/env python3
"""
Prometheus ターゲットチェッカー

このスクリプトは、Prometheus のターゲットが正しく設定され、
アプリケーションのメトリクスが収集されているかを確認します。
"""

import json
import sys
import urllib.request
import urllib.error
import socket
from typing import Dict, Any, List, Optional

def get_prometheus_targets() -> Dict[str, Any]:
    """Prometheus のターゲット情報を取得する"""
    try:
        url = "http://prometheus:9090/api/v1/targets"
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP Error: {e.code} - {e.reason}"}
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            return {"error": "Request timed out. Is Prometheus running?"}
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def check_flask_target(targets_data: Dict[str, Any]) -> bool:
    """Flask アプリケーションのターゲットが正しく設定されているか確認"""
    if "data" not in targets_data or "activeTargets" not in targets_data["data"]:
        print("❌ ターゲット情報を取得できませんでした")
        return False
    
    active_targets = targets_data["data"]["activeTargets"]
    flask_targets = [t for t in active_targets if t["scrapePool"] == "flask_app"]
    
    print("\n🔍 現在の Prometheus ターゲット状態:")
    print("-" * 50)
    
    if not flask_targets:
        print("❌ flask_app のターゲットが見つかりません")
        return False
    
    all_healthy = True
    for target in flask_targets:
        status = "✅ UP" if target["health"] == "up" else "❌ DOWN"
        print(f"{status} - {target['scrapeUrl']} (Job: {target['scrapePool']})")
        
        if target["health"] != "up":
            print(f"   エラー: {target.get('lastError', 'No error details')}")
            all_healthy = False
    
    return all_healthy

def check_metrics_are_being_collected() -> bool:
    """メトリクスが収集されているか確認"""
    try:
        # メトリクスが収集されているか確認
        url = "http://prometheus:9090/api/v1/query?query=http_requests_total"
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data["status"] != "success":
                print("❌ メトリクスクエリが失敗しました")
                return False
                
            if not data["data"]["result"]:
                print("❌ メトリクスが収集されていません")
                return False
                
            print("\n📊 メトリクス収集状況:")
            print("-" * 30)
            print(f"✅ メトリクスが正常に収集されています")
            for result in data["data"]["result"][:3]:  # 最初の3件のみ表示
                print(f"  - {result['metric'].get('job', 'unknown')}: {result['value'][1]} (at {result['value'][0]})")
            
            return True
            
    except Exception as e:
        print(f"❌ メトリクスの確認中にエラーが発生しました: {str(e)}")
        return False

def main() -> None:
    """メイン処理"""
    print("🚀 Prometheus ターゲットチェックを開始します...")
    
    # 1. Prometheus からターゲット情報を取得
    print("\n🔍 Prometheus からターゲット情報を取得中...")
    targets_data = get_prometheus_targets()
    
    if "error" in targets_data:
        print(f"❌ エラー: {targets_data['error']}")
        print("\n💡 トラブルシューティングのヒント:")
        print("1. Prometheus が起動しているか確認: docker ps | grep prometheus")
        print("2. Prometheus のログを確認: docker compose logs prometheus")
        print("3. ネットワーク設定を確認: docker network ls と docker network inspect")
        sys.exit(1)
    
    # 2. Flask アプリケーションのターゲットを確認
    print("\n🔍 Flask アプリケーションのターゲットを確認中...")
    if not check_flask_target(targets_data):
        print("\n❌ ターゲットの設定に問題があります")
        print("\n💡 修正のヒント:")
        print("1. prometheus.yml の targets が正しいか確認")
        print("   - 現在: ['localhost:9999']")
        print("   - 期待: ['flask_app:5000']")
        print("2. 修正後、docker compose restart prometheus で再起動")
        sys.exit(1)
    
    # 3. メトリクスが収集されているか確認
    print("\n🔍 メトリクスの収集状況を確認中...")
    if not check_metrics_are_being_collected():
        print("\n❌ メトリクスが正しく収集されていません")
        print("\n💡 トラブルシューティングのヒント:")
        print("1. Flask アプリケーションが起動しているか確認: docker ps | grep flask")
        print("2. Flask アプリケーションのログを確認: docker compose logs flask_app")
        print("3. http://localhost:5000/metrics にアクセスしてメトリクスが表示されるか確認")
        sys.exit(1)
    
    # すべてのチェックに成功
    print("\n" + "=" * 50)
    print("✅ おめでとうございます！すべてのチェックに成功しました！")
    print("=" * 50)
    print("\n🎯 学習のポイント:")
    print("- Prometheus のターゲット設定を理解しました")
    print("- メトリクスの収集方法を学びました")
    print("- 監視システムの設定とデバッグ方法を実践しました")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
