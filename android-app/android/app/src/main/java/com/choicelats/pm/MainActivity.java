package com.choicelats.pm;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.widget.Toast;

import com.getcapacitor.BridgeActivity;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;

/**
 * CHOICE SLATS 手机版外壳。
 *
 * ★M-APK-LAYOUT-20261108：手机端版式修复（只改 APK，网页端代码不动）
 *   1) assets/mobile-fix.css / mobile-fix.js 在页面每次加载后注入一次；
 *   2) 注入内容负责：横屏顶栏压成一行（不再把字号压到 8px）、
 *      宽表恢复桌面自然列宽（不再 table-layout:fixed 强压一屏）、
 *      被裁掉的横向内容改为可横滑、竖屏导航 5 列不再重叠；
 *   3) 用 600ms 轮询 + 版本号守卫实现「每次页面加载注入一次」，
 *      不接管 Capacitor 的 WebViewClient，避免破坏原生桥。
 */
public class MainActivity extends BridgeActivity {

    private static final String FIX_VER = "M-APK-LAYOUT-20261108c";
    private static final long POLL_MS = 600L;

    private long lastBackAt = 0L;
    private Handler mHandler;
    private Runnable mPoller;
    private String mCss = "";
    private String mJs = "";

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
                // 系统字体放大不要让表格跟着变形
                try {
                    wv.getSettings().setTextZoom(100);
                } catch (Exception ignore) {
                }
            }
        } catch (Exception ignore) {
        }
        mCss = readAsset("mobile-fix.css");
        mJs = readAsset("mobile-fix.js");
        startFixPoller();
    }

    private String readAsset(String name) {
        InputStream is = null;
        try {
            is = getAssets().open(name);
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            byte[] buf = new byte[8192];
            int n;
            while ((n = is.read(buf)) > 0) bos.write(buf, 0, n);
            return new String(bos.toByteArray(), "UTF-8");
        } catch (Exception e) {
            return "";
        } finally {
            try {
                if (is != null) is.close();
            } catch (Exception ignore) {
            }
        }
    }

    private void startFixPoller() {
        if (mCss.length() == 0 && mJs.length() == 0) return;
        mHandler = new Handler(Looper.getMainLooper());
        mPoller = new Runnable() {
            @Override
            public void run() {
                pollOnce();
                if (mHandler != null) mHandler.postDelayed(this, POLL_MS);
            }
        };
        mHandler.postDelayed(mPoller, 700);
    }

    /** 页面里已有本次版本的注入 → 什么都不做；否则注入一次。 */
    private void pollOnce() {
        try {
            final android.webkit.WebView wv = (getBridge() != null) ? getBridge().getWebView() : null;
            if (wv == null) return;
            if (wv.getUrl() == null) return;
            wv.evaluateJavascript(
                    "(function(){try{return (window.__mfixVer==='" + FIX_VER + "')?1:0}catch(e){return 0}})()",
                    new android.webkit.ValueCallback<String>() {
                        @Override
                        public void onReceiveValue(String value) {
                            if (value == null || value.indexOf('1') < 0) {
                                injectFix(wv);
                            }
                        }
                    });
        } catch (Exception ignore) {
        }
    }

    private void injectFix(android.webkit.WebView wv) {
        try {
            StringBuilder sb = new StringBuilder(12000);
            sb.append("(function(){try{");
            sb.append("if(!document.body) return 0;");
            sb.append("var s=document.getElementById('mfix-css');");
            sb.append("if(!s){s=document.createElement('style');s.id='mfix-css';document.body.appendChild(s);}");
            sb.append("s.textContent=").append(JSONObject.quote(mCss)).append(";");
            sb.append("window.__mfixVer='").append(FIX_VER).append("';");
            if (mJs.length() > 0) sb.append(mJs);
            sb.append(";return 1}catch(e){return -1}})()");
            wv.evaluateJavascript(sb.toString(), null);
        } catch (Exception ignore) {
        }
    }

    /* 说明：BridgeActivity 的 onResume/onPause/onDestroy 不是 public/protected，
       不能覆写；轮询常驻（600ms 一次极轻量的版本号检查）即可。 */

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
