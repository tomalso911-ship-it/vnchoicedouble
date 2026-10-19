/* 切换 APK 打开的网址（Capacitor CLI 6 不支持 --config，统一用本脚本改配置）
   用法：
     node set-server.js https://pm2.你的域名.com/lite   ← 生产
     node set-server.js http://10.0.2.2:5050/lite       ← 模拟器连本机
     node set-server.js http://192.168.1.20:5050/lite   ← 真机连同一 WiFi 的电脑
   改完执行：npx cap sync android && cd android && gradlew.bat assembleDebug */
const fs = require('fs');
const path = require('path');

const cfgPath = path.join(__dirname, 'capacitor.config.json');
const url = (process.argv[2] || '').trim();
if (!/^https?:\/\//.test(url)) {
  console.log('usage: node set-server.js <http(s)://host:port/lite>');
  process.exit(1);
}

const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const isHttps = url.startsWith('https://');
cfg.server = cfg.server || {};
cfg.server.url = url;
cfg.server.cleartext = !isHttps;
cfg.server.androidScheme = isHttps ? 'https' : 'http';
if (cfg.android) {
  cfg.android.allowMixedContent = !isHttps;
  cfg.android.webContentsDebuggingEnabled = !isHttps;
}

fs.writeFileSync(cfgPath, JSON.stringify(cfg, null, 2) + '\n', 'utf8');
console.log('[OK] server.url =', url);
