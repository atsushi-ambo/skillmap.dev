#!/usr/bin/env python3
import sys
import urllib.request
import urllib.error
import socket
import json
from typing import Tuple, Dict, Any

def check_ports() -> bool:
    """Check if the port mapping is correct by inspecting the container."""
    import subprocess
    try:
        # Get the container's port mapping
        cmd = [
            'docker', 'inspect',
            '--format', '{{range $p, $conf := .NetworkSettings.Ports}}{{$p}} -> {{(index $conf 0).HostPort}}{{"\n"}}{{end}}',
            'skillmapdev-network_lab-1'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("\n🔍 現在のポートマッピングを確認中...")
        print(result.stdout.strip())
        
        # Check if port 80 is mapped to 8080
        if '80/tcp -> 8080' in result.stdout:
            print("✅ ポートマッピングが正しく設定されています (80/tcp -> 8080)")
            return True
        else:
            print("❌ ポートマッピングが正しく設定されていません")
            print("   期待されるマッピング: 80/tcp -> 8080")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ コンテナ情報の取得に失敗しました: {e}")
        return False
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False

def check_nginx() -> Tuple[bool, Dict[str, Any]]:
    """Check if Nginx is responding correctly."""
    try:
        # Check if nginx is accessible on port 8080
        req = urllib.request.Request(
            'http://localhost:8080',
            headers={'User-Agent': 'Skillmap Exercise Checker'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            headers = dict(response.getheaders())
            
            return True, {
                'status': response.status,
                'content': content,
                'headers': headers
            }
            
    except urllib.error.HTTPError as e:
        return False, {'error': f'HTTP Error: {e.code} - {e.reason}'}
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            return False, {'error': 'Request timed out. Is Nginx running?'}
        return False, {'error': f'URL Error: {e.reason}'}
    except Exception as e:
        return False, {'error': f'An error occurred: {str(e)}'}

def check_network() -> bool:
    """Check if the network setup is correct."""
    print("🚀 ネットワーク設定を確認中...\n")
    
    # First check the port mapping
    if not check_ports():
        print("\n❌ ポートマッピングを確認してください。")
        print("   docker-compose.yml の ports 設定を確認し、正しいマッピングに修正してください。")
        print("   例: \"8080:80\" (ホスト:コンテナ)")
        return False
    
    # Then check Nginx response
    success, result = check_nginx()
    
    if success:
        print("\n🔄 Nginx の応答を確認中...")
        print(f"   Status: {result['status']}")
        print(f"   Content-Type: {result['headers'].get('Content-Type', 'N/A')}")
        print(f"   X-Network-Exercise: {result['headers'].get('X-Network-Exercise', 'N/A')}")
        
        if 'おめでとう' in result['content']:
            print("\n🎉 おめでとうございます！Nginx が正しく設定されました！")
            print("✅ 演習は成功です！")
            return True
        else:
            print("\n❌ Nginx の応答が期待と異なります。")
            print("   nginx.conf の設定を確認してください。")
            return False
    else:
        print("\n❌ Nginx への接続に失敗しました。")
        print(f"   エラー: {result['error']}")
        print("\nトラブルシューティングのヒント:")
        print("1. コンテナが起動しているか確認: docker ps")
        print("2. Nginx のログを確認: docker logs skillmapdev-network_lab-1")
        print("3. ポートが使用中でないか確認: lsof -i :8080")
        return False

if __name__ == "__main__":
    success = check_network()
    sys.exit(0 if success else 1)
