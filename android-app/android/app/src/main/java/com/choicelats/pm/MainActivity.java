package com.choicelats.pm;

import android.os.Bundle;
import android.os.SystemClock;
import android.widget.Toast;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    private long lastBackAt = 0L;

    /** ★APP-CACHE-20261025：每次冷启动清一次 WebView 的 HTTP 磁盘缓存，
     *  保证打开 App 就是服务器上的最新页面（前端已改为加载线上 /lite）。
     *  注意：只清 HTTP 缓存，绝不动 localStorage / Cookie，避免丢登录态与本地数据。 */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            android.webkit.WebView wv = (getBridge() != null) ? getBridge().getWebView() : null;
            if (wv != null) {
                wv.clearCache(true);
            }
        } catch (Exception ignore) {
        }
    }

    /** ★M-APP-20261019：返回键行为 ——
     *  1) 页面还能后退（打开过弹窗/子页）→ 后退一页，不退出；
     *  2) 已在最上层 → 1.5 秒内再按一次才退出（防止现场误触直接退出 App）。 */
    @Override
    public void onBackPressed() {
        try {
            android.webkit.WebView wv = (getBridge() != null) ? getBridge().getWebView() : null;
            if (wv != null && wv.canGoBack()) {
                wv.goBack();
                return;
            }
        } catch (Exception ignore) {
        }
        long now = SystemClock.elapsedRealtime();
        if (now - lastBackAt < 1500) {
            super.onBackPressed();
            return;
        }
        lastBackAt = now;
        Toast.makeText(this, "再按一次退出 / Nhấn lần nữa để thoát", Toast.LENGTH_SHORT).show();
    }
}
