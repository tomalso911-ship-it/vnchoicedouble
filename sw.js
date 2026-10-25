/* ★FIX-20261025：Service Worker 之前会经 HTTP 缓存返回旧页面（旧页面照片仍是
   <a target="_blank"> → 点开新标签页、没有照片内关闭按钮）。
   这个版本只做"自我销毁"：清空所有缓存 → 注销自己 → 刷新所有已打开窗口到最新页面。
   注销后本页不再有 SW，之后每次都直接从服务器取最新 HTML。 */
self.addEventListener('install', function () { self.skipWaiting(); });

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (ks) {
      return Promise.all(ks.map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
      .then(function () { return self.clients.matchAll({ type: 'window' }); })
      .then(function (cs) {
        cs.forEach(function (c) { try { c.navigate(c.url); } catch (_) {} });
      })
      .then(function () { return self.registration.unregister(); })
  );
});

/* 不拦截任何请求：全部走网络（避免任何旧缓存） */
self.addEventListener('fetch', function () {});
