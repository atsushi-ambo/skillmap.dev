#!/usr/bin/env python3
"""
Redis バックアップチェッカー

このスクリプトは、Redis のバックアップ設定が正しく行われているかを確認します。
"""

import subprocess
import json
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

def run_command(cmd: str) -> Tuple[bool, str]:
    """コマンドを実行して結果を返す"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"Command failed with error: {e.stderr}"

def check_redis_running() -> bool:
    """Redis が実行中か確認"""
    print("\n🔍 Redis の実行状態を確認中...")
    success, output = run_command("docker compose ps redis | grep Up")
    
    if not success or "redis" not in output:
        print("❌ Redis が実行されていません")
        print("💡 以下のコマンドで起動してください: docker compose up -d")
        return False
    
    print("✅ Redis が正常に実行されています")
    return True

def check_redis_config() -> Dict[str, Any]:
    """Redis の設定を確認"""
    print("\n🔍 Redis の設定を確認中...")
    
    # 設定ファイルの内容を取得
    success, output = run_command("docker compose exec redis cat /usr/local/etc/redis/redis.conf | grep -v '^#' | grep -v '^$'")
    
    if not success:
        print(f"❌ 設定ファイルの取得に失敗しました: {output}")
        return {}
    
    # 設定をパース
    config = {}
    for line in output.split('\n'):
        if ' ' in line:
            key, *value = line.split()
            config[key] = ' '.join(value) if len(value) > 1 else value[0]
    
    return config

def check_backup_settings(config: Dict[str, Any]) -> bool:
    """バックアップ設定を確認"""
    print("\n🔍 バックアップ設定を確認中...")
    
    # バックアップ設定を取得
    save_commands = [v for k, v in config.items() if k == 'save']
    
    if not save_commands:
        print("❌ バックアップ設定が見つかりません")
        return False
    
    # バックアップ設定を表示
    print("現在のバックアップ設定:")
    for i, save_cmd in enumerate(save_commands, 1):
        print(f"  {i}. {save_cmd}")
    
    # バックアップが有効かチェック
    if any(save_cmd == '\"\"' or save_cmd == "''" for save_cmd in save_commands):
        print("❌ バックアップが無効化されています (save \"\" が設定されています)")
        return False
    
    # 推奨されるバックアップ設定
    recommended = [
        '900 1',
        '300 10',
        '60 10000'
    ]
    
    # 推奨設定と比較
    missing = []
    for rec in recommended:
        if not any(rec in save_cmd for save_cmd in save_commands):
            missing.append(rec)
    
    if missing:
        print(f"❌ 推奨されるバックアップ設定が不足しています: {', '.join(missing)}")
        return False
    
    print("✅ バックアップ設定が正しく構成されています")
    return True

def check_backup_file() -> bool:
    """バックアップファイルを確認"""
    print("\n🔍 バックアップファイルを確認中...")
    
    # バックアップファイルの存在確認
    success, output = run_command("docker compose exec redis ls -la /data/ | grep dump.rdb")
    
    if not success or 'dump.rdb' not in output:
        print("❌ バックアップファイル (dump.rdb) が見つかりません")
        return False
    
    # ファイルサイズを取得
    success, size_output = run_command("docker compose exec redis du -h /data/dump.rdb | cut -f1")
    
    if not success:
        print("❌ バックアップファイルのサイズを取得できませんでした")
        return False
    
    # ファイルの最終更新日時を取得
    success, mtime_output = run_command("docker compose exec redis stat -c '%y' /data/dump.rdb")
    
    if not success:
        print("❌ バックアップファイルの最終更新日時を取得できませんでした")
        return False
    
    # コンテナの起動時間を取得
    success, start_time_output = run_command("docker inspect -f '{{.State.StartedAt}}' redis-backup-demo")
    
    if not success:
        print("❌ コンテナの起動時間を取得できませんでした")
        return False
    
    # 日時をパース
    try:
        file_mtime = datetime.fromisoformat(mtime_output.split('.')[0])
        container_start = datetime.fromisoformat(start_time_output.split('.')[0].replace('Z', '+00:00'))
        now = datetime.now(file_mtime.tzinfo)
        
        print(f"✅ バックアップファイルが見つかりました (サイズ: {size_output})")
        print(f"    最終更新: {file_mtime}")
        print(f"    コンテナ起動から: {now - container_start} 経過")
        
        # ファイルがコンテナ起動後に更新されているか確認
        if file_mtime < container_start:
            print("❌ バックアップファイルが古いです。コンテナ起動後に更新されていません")
            print("💡 SAVE コマンドを実行して、バックアップファイルを更新してください")
            return False
            
    except Exception as e:
        print(f"❌ 日時の処理中にエラーが発生しました: {str(e)}")
        return False
    
    return True

def main() -> None:
    """メイン処理"""
    print("🚀 Redis バックアップ設定チェックを開始します...")
    
    # 1. Redis が実行中か確認
    if not check_redis_running():
        sys.exit(1)
    
    # 2. Redis の設定を確認
    config = check_redis_config()
    if not config:
        print("❌ Redis の設定を取得できませんでした")
        sys.exit(1)
    
    # 3. バックアップ設定を確認
    if not check_backup_settings(config):
        print("\n💡 修正のヒント:")
        print("1. redis.conf を編集して、以下の設定を追加してください:")
        print("   save 900 1")
        print("   save 300 10")
        print("   save 60 10000")
        print("2. 以下のコマンドで Redis を再起動してください:")
        print("   docker compose restart redis")
        sys.exit(1)
    
    # 4. バックアップファイルを確認
    if not check_backup_file():
        print("\n💡 トラブルシューティングのヒント:")
        print("1. Redis CLI で SAVE コマンドを実行して、バックアップファイルを作成してください:")
        print("   docker compose exec redis redis-cli SAVE")
        print("2. バックアップファイルのパーミッションを確認してください:")
        print("   docker compose exec redis ls -la /data/")
        sys.exit(1)
    
    # すべてのチェックに成功
    print("\n" + "=" * 60)
    print("✅ おめでとうございます！すべてのチェックに成功しました！")
    print("=" * 60)
    print("\n🎯 学習のポイント:")
    print("- Redis のバックアップ設定を理解しました")
    print("- データの永続化の重要性を学びました")
    print("- バックアップファイルの管理方法を実践しました")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
