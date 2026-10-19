/* ★M-APP-20261019：Service Worker（PWA 安装 + 弱网可打开）
   原则：
   1) /api/ 与所有非 GET 请求【绝不缓存】——业务数据必须实时，缓存会造成"看到旧数据"。
   2) 页面导航走 network-first，断网时回退到缓存的 /lite 外壳。
   3) 静态资源（js/svg/png/json/字体）cache-first，后台顺带更新。
   4) 版本号改动即整体换缓存，避免旧外壳卡住新代码。 */
const CACHE = 'choice-shell-v1';
const SHELL = ['/lite', '/manifest.json', '/favicon.svg', '/icon-192.png', '/icon-512.png', '/icon-512-maskable.png', '/apple-touch-icon.png'];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return Promise.all(SHELL.map(function (u) {
        return c.add(new Request(u, { cache: 'reload' })).catch(function () {});
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.indexOf('/api/') === 0) return;       // 接口一律走网络

  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).catch(function () {
        return caches.match('/lite').then(function (hit) { return hit || caches.match(req); });
      })
    );
    return;
  }

  const ext = (url.pathname.split('.').pop() || '').toLowerCase();
  if (['js', 'css', 'svg', 'png', 'jpg', 'jpeg', 'webp', 'woff', 'woff2', 'json'].indexOf(ext) < 0) return;

  e.respondWith(
    caches.match(req).then(function (hit) {
      const net = fetch(req).then(function (res) {
        if (res && res.ok) {
          const cp = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, cp); });
        }
        return res;
      }).catch(function () { return hit; });
      return hit || net;
    })
  );
});
