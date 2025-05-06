const { exec } = require('child_process');
const chokidar = require('chokidar');

// 監視対象のディレクトリとファイル
const watcher = chokidar.watch([
  'docs/**/*',
  'mkdocs.yml',
  'package*.json',
  '!**/node_modules/**',
  '!**/.git/**',
  '!**/.DS_Store'
], {
  ignored: /(^|[\/\\])\../, // ドットファイルを無視
  persistent: true,
  ignoreInitial: true
});

let timeoutId;
let isProcessing = false;

// 変更を検知したときの処理
const handleChange = (path, stats) => {
  console.log(`Detected change in: ${path}`);
  
  // すでに処理中の場合は何もしない
  if (isProcessing) {
    console.log('Already processing changes...');
    return;
  }

  
  // 前回のタイマーをクリア
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
  
  // 新しいタイマーをセット（1秒後に実行）
  timeoutId = setTimeout(async () => {
    try {
      isProcessing = true;
      console.log('Processing changes...');
      
      // Gitコマンドを実行
      await execPromise('git add .');
      const commitMsg = `Auto-commit: ${new Date().toISOString()}`;
      await execPromise(`git commit -m "${commitMsg}"`);
      await execPromise('git push origin main');
      
      console.log('Changes pushed successfully!');
    } catch (error) {
      console.error('Error pushing changes:', error.message);
    } finally {
      isProcessing = false;
    }
  }, 1000); // 1秒のディレイ
};

// Promiseを返すexecラッパー
const execPromise = (command) => {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing command: ${command}`, error);
        return reject(error);
      }
      if (stderr) {
        console.error(`stderr: ${stderr}`);
      }
      console.log(`stdout: ${stdout}`);
      resolve(stdout);
    });
  });
};

// イベントリスナーを設定
watcher
  .on('add', path => handleChange(path))
  .on('change', path => handleChange(path))
  .on('unlink', path => handleChange(path));

console.log('Watching for file changes... (Press Ctrl+C to stop)');

// エラーハンドリング
watcher.on('error', error => console.error('Watcher error:', error));

// クリーンアップ
process.on('SIGINT', () => {
  watcher.close();
  console.log('Stopped watching for changes');
  process.exit();
});
