#!/usr/bin/env python3
"""
Skillmap CLI - Ops Essentials 演習用ツール

使い方:
  python3 tools/cli/game.py play <game_id>

利用可能なゲーム:
  01-network: ネットワーク設定のデバッグ演習
"""
import subprocess
import sys
import argparse
import time
from pathlib import Path
from typing import Optional

def print_header():
    """Print the tool header."""
    print("""
    ____  _ _       _ __  __       _   _             
   / ___|(_) | __ _|  \\/  | __ _| |_| |    ___  ___
   \\___ \\| | |/ _` | |\\/| |/ _` | __| |   / _ \\/ __|
    ___) | | | (_| | |  | | (_| | |_| |__|  __/\\__ \\
   |____/|_|_|\\__,_|_|  |_|\\__,_|\\__|_____\\___||___/
   
   Ops Essentials - ネットワーク演習ツール
   """)

def get_available_games() -> list:
    """Get list of available games."""
    games_dir = Path(__file__).parent.parent.parent / "ops-essentials" / "games"
    if not games_dir.exists():
        return []
    return [d.name for d in games_dir.iterdir() if d.is_dir()]

def play_game(game_id: str) -> bool:
    """Play a specific game.
    
    Args:
        game_id: ID of the game to play
        
    Returns:
        bool: True if the game was completed successfully
    """
    game_dir = Path(__file__).parent.parent.parent / "ops-essentials" / "games" / game_id
    checker = game_dir / "checker.py"
    
    if not checker.exists():
        print(f"❌ エラー: ゲーム '{game_id}' が見つからないか、checker.py が存在しません")
        return False
    
    print(f"\n🎮 ゲームを開始します: {game_id}")
    print("-" * 50)
    
    # Check if the game has a quest file
    quest_file = game_dir / "quest.md"
    if quest_file.exists():
        with open(quest_file, 'r', encoding='utf-8') as f:
            print("\n📜 ミッション概要:")
            print("-" * 30)
            print(f.read())
    
    print("\n🔍 チェックを開始します...")
    print("-" * 50)
    
    try:
        # Run the checker with a timeout of 30 seconds
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, str(checker)],
            cwd=game_dir,
            check=False,
            text=True,
            capture_output=True
        )
        elapsed_time = time.time() - start_time
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            print("\n" + "=" * 50)
            print("🎉 おめでとうございます！ クリアです！")
            print(f"⏱️  かかった時間: {elapsed_time:.1f}秒")
            print("=" * 50)
            return True
        else:
            print("\n" + "=" * 50)
            print("❌ もう一度挑戦してください")
            print("=" * 50)
            return False
            
    except subprocess.TimeoutExpired:
        print("\n🕒 チェックがタイムアウトしました。時間がかかりすぎています。")
        return False
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        return False

def main():
    """Main entry point for the CLI."""
    print_header()
    
    parser = argparse.ArgumentParser(description='Skillmap CLI tool for Ops Essentials')
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')
    
    # Play command
    play_parser = subparsers.add_parser('play', help='ゲームをプレイする')
    play_parser.add_argument('game_id', help='プレイするゲームのID')
    
    args = parser.parse_args()
    
    if args.command == 'play':
        available_games = get_available_games()
        if args.game_id not in available_games:
            print(f"\n❌ エラー: ゲーム '{args.game_id}' は存在しません")
            print("\n利用可能なゲーム:")
            for game in available_games:
                print(f"  - {game}")
            sys.exit(1)
            
        success = play_game(args.game_id)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        print("\n利用可能なゲーム:")
        for game in get_available_games():
            print(f"  - {game}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 プログラムを終了します")
        sys.exit(0)
