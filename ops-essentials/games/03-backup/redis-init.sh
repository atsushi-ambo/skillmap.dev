#!/bin/sh
# Redis 初期化スクリプト

# コンテナ起動時に実行されるスクリプト
# サンプルデータを挿入

# Redis が起動するのを待機
until redis-cli ping &> /dev/null; do
  echo "Waiting for Redis to start..."
  sleep 1
done

# サンプルデータを挿入
echo "Inserting sample data..."
redis-cli set welcome "Hello, Redis Backup Demo!"
redis-cli lpush colors red green blue yellow
redis-cli hset user:1000 name "John Doe" email "john@example.com"

# データをディスクに同期
echo "Saving data to disk..."
redis-cli save

echo "Redis initialization complete!"
