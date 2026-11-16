/* CHOICE SLATS 手机版修复脚本 v6（仅 APK 注入，不改网页源码）
   职责：
   1) 给网页"自己没做横向滚动"的宽容器补 .mfix-scroll（CSS 里统一 overflow-x:auto）；
   2) 给网页已经做过横滑/固定列的桌子打 .mfix-keep，防止被通用表格规则改坏；
   3) 切页 / 换语言 / 旋转后重扫。
   注意：不再往 table 上写 inline style（inline !important 会压过 CSS !important）。 */
(() => {
  // ★注意：不要在这里写 window.__mfixVer —— 那是 MainActivity 的注入版本守卫，
  //   被 JS 覆盖会让守卫永远不匹配，导致 600ms 一次无限重复注入。
  const VER = 'M-APK-PORTRAIT-GANTT-20261116i';
  if (window.__mfix) { window.__mfix.rescan(true); return 'rescan'; }

  // 网页已经做过横滑 / 固定列 / 带 colgroup 的表：保持原样
  const KEEP_SEL = '#slatsSpecTable, .slats-report-table, .slats-spec-table, #slatsReportOverview,' +
    '.won-scroll-container > table, .receipt-card .prod-table, .usr-diff-box .prod-table';
  // 已经是横向滚动容器的，不要再判一次（它们本来就能滑）
  const OK_SEL = '.mfix-scroll, .won-scroll-container, .appr-table-wrap, .users-table-wrap, .rc-body, .rc-list-scroll';
  let timer = null, last = 0;

  function curRoot() {
    for (const v of document.querySelectorAll('[id^="view-"]')) {
      if (v.offsetParent !== null) return v;
    }
    return document.body;
  }

  function markTables(root) {
    let keep = 0, fixed = 0;
    for (const t of root.querySelectorAll('table')) {
      let isKeep = false;
      try { isKeep = t.matches(KEEP_SEL); } catch (e) { isKeep = false; }
      if (!isKeep && t.querySelector('colgroup')) isKeep = true;
      if (!isKeep && t.closest('.receipt-card, .usr-diff-box')) isKeep = true;
      if (isKeep) {
        if (!t.classList.contains('mfix-keep')) t.classList.add('mfix-keep');
        keep++;
        continue;
      }
      if (t.classList.contains('mfix-keep')) t.classList.remove('mfix-keep');
      fixed++;
    }
    return { keep, fixed };
  }

  /* ★性能：不要遍历所有 div。原先是 root.querySelectorAll('div,section,...')，
     这个页面 8 万多节点，每读一次 clientWidth/scrollWidth 都强制同步布局，
     低端机/模拟器上足以卡到 ANR。现在只从 <table> 往上走 3 层找容器，代价与表数量同阶。 */
  function markTableScrollers(root, n) {
    let hit = n;
    for (const t of root.querySelectorAll('table')) {
      if (t.classList.contains('mfix-keep')) continue;
      let el = t.parentElement, depth = 0;
      while (el && depth < 3 && el !== document.body && el !== document.documentElement) {
        if (el.classList) {
          if (el.classList.contains('mfix-scroll')) break;
          let skip = false;
          try { skip = el.matches(OK_SEL); } catch (e) { }
          if (skip) break;
        }
        const cw = el.clientWidth;
        if (cw > 60 && el.scrollWidth > cw + 6) {
          const ox = getComputedStyle(el).overflowX;
          if (ox === 'visible' || ox === 'hidden') { el.classList.add('mfix-scroll'); hit++; }
          break;
        }
        el = el.parentElement; depth++;
      }
    }
    return hit;
  }

  function scan(full) {
    const t0 = performance.now();
    const root = curRoot();
    const tb = markTables(root);
    const ae = document.activeElement;
    const typing = ae && /^(INPUT|TEXTAREA|SELECT)$/.test(ae.tagName);
    let n = 0;
    if (!typing) n = markTableScrollers(root, 0);
    window.__mfixLast = { ver: VER, ms: Math.round(performance.now() - t0), scroll: n, keep: tb.keep, fixed: tb.fixed, full: !!full, root: root.id || 'body' };
    return window.__mfixLast;
  }

  function rescan(full) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => { timer = null; scan(!!full); }, 320);
  }

  /* ★M-CELLFIT-20261116：单元格越界检查/修复（按需调用，不进轮询，避免大表卡顿）
     用法：window.__mfixFitCells()          → 修（给越界单元格加 white-space:normal）
           window.__mfixFitCells({reportOnly:1}) → 只体检不改            */
  window.__mfixFitCells = function (opts) {
    const reportOnly = !!(opts && opts.reportOnly);
    const rep = { cells: 0, over: 0, list: [] };
    const tables = document.querySelectorAll('table');
    for (const t of tables) {
      if (!t.getClientRects().length) continue;
      const tid = t.id || (t.className || '').toString().slice(0, 40);
      const cells = t.querySelectorAll('td,th');
      for (const c of cells) {
        rep.cells++;
        const cw = c.clientWidth, sw = c.scrollWidth;
        let childOver = false;
        const cr = c.getBoundingClientRect();
        for (const ch of c.children) {
          const b = ch.getBoundingClientRect();
          if (b.width > 0 && (b.right > cr.right + 1.5 || b.left < cr.left - 1.5)) { childOver = true; break; }
        }
        if (sw <= cw + 1 && !childOver) { c.classList.remove('mfix-cell-over'); continue; }
        rep.over++;
        c.classList.add('mfix-cell-over');
        if (rep.list.length < 30) {
          rep.list.push({ table: tid, text: (c.textContent || '').trim().slice(0, 24), cw: cw, sw: sw, childOver: childOver });
        }
        if (!reportOnly && sw > cw + 1) c.style.setProperty('white-space', 'normal', 'important');
      }
    }
    window.__mfixLastFit = rep;
    return rep;
  };

  window.__mfix = { scan, rescan, ver: VER };
  window.addEventListener('resize', () => rescan(true));
  window.addEventListener('orientationchange', () => { rescan(true); setTimeout(() => rescan(true), 350); });
  document.addEventListener('app:langchange', () => rescan(true));

  if (typeof window.switchView === 'function') {
    const sv = window.switchView;
    window.switchView = function () {
      const r = sv.apply(this, arguments);
      setTimeout(() => rescan(true), 120);
      setTimeout(() => rescan(true), 900);
      return r;
    };
  }
  const mo = new MutationObserver(() => {
    const now = Date.now();
    if (now - last < 900) return;
    last = now;
    rescan(false);
  });
  mo.observe(document.body, { childList: true, subtree: true });

  /* =====================================================================
     ★M-BACK-20261116：安卓返回键（◁ / 手势返回）
     MainActivity.onBackPressed 先问 window.__mfixBack()：
       返回 1 → 页面已经处理（关掉了弹窗/预览），Java 什么都不做；
       返回 0 → Java 继续走 canGoBack()（回上一页）/ 双击退出。
     顺序：PDF 预览 → 图片灯箱 → 最上层弹窗（按 z-index 从高到低）。
     ===================================================================== */
  function isVisible(el) {
    if (!el || !el.getClientRects) return false;
    if (!el.getClientRects().length) return false;
    const c = getComputedStyle(el);
    return c.display !== 'none' && c.visibility !== 'hidden' && c.opacity !== '0';
  }

  function layerZ(el) {
    let z = 0, n = el;
    while (n && n !== document.body) {
      const v = parseInt(getComputedStyle(n).zIndex, 10);
      if (!isNaN(v)) z = Math.max(z, v);
      n = n.parentElement;
    }
    return z;
  }

  // 永远不参与"返回键关闭"的元素（顶栏/登录页/视图容器/提示气泡）
  const BACK_BLACK = '#topbar, #loginPage, .app-body, #tbMenu, nav, #view-dashboard, #view-won, ' +
    '#view-worklog, #view-production, #view-install, #view-finance, #view-library, #view-equity, #view-approvals, #view-users';

  function visibleLayers() {
    const out = [];
    const sel = '[class*="overlay"], [class*="Overlay"], [class*="Modal"], [class*="modal"], [class*="Drawer"],' +
      '[class*="drawer"], [class*="popup"], [class*="lightbox"], .show';
    let nodes;
    try { nodes = document.querySelectorAll(sel); } catch (e) { return out; }
    for (const el of nodes) {
      if (el === document.body || el === document.documentElement) continue;
      try { if (el.matches(BACK_BLACK)) continue; } catch (e) { }
      if (!isVisible(el)) continue;
      const c = getComputedStyle(el);
      if (c.position !== 'fixed' && c.position !== 'absolute') continue;
      const z = layerZ(el);
      if (z < 800) continue;                       // 弹窗层一般 1100+，避免误伤普通浮层
      out.push({ el, z });
    }
    out.sort((a, b) => a.z - b.z);                 // 后面的更靠上
    return out.map((o) => o.el);
  }

  function closeLayer(el) {
    try {
      if (el.id === 'mfix-pdf-ov') { closePdf(); return true; }
      if (el.classList.contains('img-lightbox-20261025')) { el.remove(); return true; }
      // 优先点网页自己的关闭按钮：走原生关闭逻辑，不会留下半关闭状态
      const btn = el.querySelector('.close, button[title="关闭"], button[aria-label="关闭"], [onclick*="Close"], [onclick*="close"]');
      if (btn && btn !== el && isVisible(btn)) { btn.click(); if (!isVisible(el)) return true; }
      if (el.classList.contains('show')) { el.classList.remove('show'); if (!isVisible(el)) return true; }
      el.click();                                   // 兜底：点遮罩本身（有的弹窗 target===this 才关）
      return !isVisible(el);
    } catch (e) { return false; }
  }

  window.__mfixBack = function () {
    try {
      const pdf = document.getElementById('mfix-pdf-ov');
      if (pdf && isVisible(pdf)) { closePdf(); return 1; }
      const layers = visibleLayers();
      for (let i = layers.length - 1; i >= 0; i--) {
        if (closeLayer(layers[i])) return 1;
      }
      /* ★M-BACK-VIEW-20261116（用户要求）：没有弹窗可关时，交给网页自己的
         「返回上一层视图」逻辑（switchView 历史 / gotoPrevView）。
         返回 1 = 网页已经退了一层，Java 不再 goBack 也不退出 App。 */
      if (typeof window.__handleBack === 'function') {
        const consumed = window.__handleBack();
        if (consumed) return 1;
      }
    } catch (e) { }
    return 0;
  };

  /* =====================================================================
     ★M-CLOSEBTN-20261116（用户要求）：模态框【自带的顶部关闭按钮】点了必须能关。
     失败原因（手机上很常见）：
       ① 按钮被内容层/遮罩盖住，tap 落到了别人身上（pointer-events / z-index 问题）；
       ② 按钮 onclick 里调的函数不存在或抛错，视觉上"点了没反应"；
       ③ 弹窗只把自己 display:none，overlay 还留着。
     这里做三件事：
       A) 捕获阶段识别"关闭按钮"（class 含 close / 文本 ×✕✗ / title|aria-label 含关闭·close·đóng），
          点完 350ms 后若弹窗还在，就强制关掉它（closeLayer 兜底）；
       B) 把按钮的命中区域放大到至少 34×34（CSS 侧配合 pointer-events:auto）；
       C) 关不掉时给出明确提示，不再让用户"点了没反应"。
     ===================================================================== */
  const CLOSE_TXT_RE = /^[×✕✗✖╳xX]$/;
  const CLOSE_ATTR_RE = /(关闭|關閉|close|đóng|dong|hủy|huy)/i;

  function looksCloseBtn(el) {
    if (!el || el.nodeType !== 1) return false;
    const cls = (el.className || '').toString();
    if (/close/i.test(cls)) return true;
    const t = (el.textContent || '').trim();
    if (CLOSE_TXT_RE.test(t)) return true;
    const at = (el.getAttribute('title') || '') + ' ' + (el.getAttribute('aria-label') || '');
    if (at.trim() && CLOSE_ATTR_RE.test(at)) return true;
    const oc = el.getAttribute('onclick') || '';
    if (/close/i.test(oc)) return true;
    return false;
  }

  function layerOf(el) {
    let n = el, best = null;
    while (n && n !== document.body) {
      try {
        if (n.matches && n.matches('[class*="overlay"],[class*="Overlay"],[class*="modal"],[class*="Modal"]')) {
          const cs = getComputedStyle(n);
          if (cs.position === 'fixed' || cs.position === 'absolute') best = n;
        }
      } catch (e) { }
      n = n.parentElement;
    }
    return best;
  }

  document.addEventListener('click', function (e) {
    const tgt = e.target;
    const btn = (tgt && tgt.closest) ? tgt.closest('button, .close, .mmax-close, [onclick], [role="button"]') : null;
    if (!btn || !looksCloseBtn(btn)) return;
    const layer = layerOf(btn);
    if (!layer) return;
    setTimeout(function () {
      try {
        if (isVisible(layer)) closeLayer(layer);
      } catch (err) { }
    }, 350);
  }, true);

  /* =====================================================================
     ★M-CLOSEFAB-20261116：顶栏高度 → CSS 变量；有弹窗时给一个永远点得到的 ✕
     网页自己的 × 是 absolute，手机上一滚就滚没了 → 用户"根本关不掉"。
     ===================================================================== */
  function syncTopbarHeight() {
    const tb = document.getElementById('topbar');
    let h = 0;
    try {
      if (tb && tb.getClientRects().length) {
        const c = getComputedStyle(tb);
        if (c.display !== 'none' && c.visibility !== 'hidden') h = tb.getBoundingClientRect().height || 0;
      }
    } catch (e) { }
    document.documentElement.style.setProperty('--mfix-topbar-h', Math.round(h) + 'px');
    return Math.round(h);
  }

  function anyLayerShown() {
    const nodes = document.querySelectorAll('.show');
    for (const el of nodes) {
      if (el === document.body) continue;
      if (!isVisible(el)) continue;
      const z = parseInt(getComputedStyle(el).zIndex, 10) || 0;
      if (z >= 800) return true;
    }
    return false;
  }

  function syncCloseFab() {
    syncTopbarHeight();
    const need = anyLayerShown();
    const fab = document.getElementById('mfix-close-fab');
    if (!need) { if (fab) fab.remove(); return; }
    if (fab) return;
    const b = document.createElement('button');
    b.id = 'mfix-close-fab';
    b.type = 'button';
    b.setAttribute('aria-label', '关闭');
    b.textContent = '✕';
    b.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      try { window.__mfixBack(); } catch (err) { }
    });
    document.body.appendChild(b);
  }

  setInterval(function () { try { syncCloseFab(); } catch (e) { } }, 700);

  /* =====================================================================
     ★M-GANTT-PORTRAIT-20261116（用户 2026-11-16 竖屏截图）：
     「安装管理 → 安装计划详细安排」整页跑在 #instGanttFrame 这个 iframe 里，
     父页面的 mobile-fix.css 完全管不到它 —— 竖屏下：排程参数 8 个字段被
     flex:1 1 auto 压成一条条竖字、标题两行挤在一起、表格列被裁在右边。
     这里往 iframe 文档里补一份窄屏样式（网页源码不动）。
     ===================================================================== */
  const GANTT_CSS = [
    "@media (max-width:900px){",
    "html .page{padding:6px 8px 16px}",
    "html .hdr{display:block;margin-bottom:4px}",
    "html .hdr h1{font-size:14px;line-height:1.3;overflow-wrap:break-word;word-break:normal}",
    "html .hdr .sub{display:block;font-size:11px;margin-top:2px}",
    "html .hdr-btns{margin-left:0 !important;margin-top:6px !important;display:flex !important;gap:8px !important}",
    "html .hdr-btns .btn{flex:1 1 auto !important;padding:8px 10px !important}",
    "html .card{padding:10px !important;margin-top:10px !important}",
    "html .card h2{font-size:12px !important;flex-wrap:wrap !important;line-height:1.45 !important}",
    "html .row.params-row{flex-wrap:wrap !important;gap:8px !important;align-items:flex-end !important}",
    "html .params-row .fld{flex:1 1 calc(50% - 8px) !important;min-width:130px !important}",
    "html .params-row .fld label{white-space:normal !important;overflow:visible !important;text-overflow:clip !important;text-align:left !important;font-size:10.5px !important;line-height:1.25 !important}",
    "html .params-row .fld input,html .params-row .fld select{width:100% !important;min-width:0 !important}",
    "html .params-row .btn{flex:1 1 calc(50% - 8px) !important;white-space:normal !important;padding:8px 6px !important}",
    "html .layout{height:auto !important;flex-direction:column !important}",
    "html .splitter{display:none !important}",
    "html .tbl-wrap{width:100% !important;max-height:38vh !important;overflow:auto !important;border-right:0 !important;border-bottom:1px solid #cfd8dc !important;-webkit-overflow-scrolling:touch !important}",
    "html .chart-wrap{min-height:280px !important;max-height:60vh !important;overflow:auto !important;-webkit-overflow-scrolling:touch !important}",
    /* 表格/甘特都比屏幕宽：给一条看得见的细横滑条，提示"这里能左右滑" */
    "html .tbl-wrap,html .chart-wrap{touch-action:pan-x pan-y}",
    "html .tbl-wrap::-webkit-scrollbar,html .chart-wrap::-webkit-scrollbar{height:8px;width:8px}",
    "html .tbl-wrap::-webkit-scrollbar-thumb,html .chart-wrap::-webkit-scrollbar-thumb{background:rgba(0,0,0,.35);border-radius:4px}",
    "html .tbl-wrap::-webkit-scrollbar-track,html .chart-wrap::-webkit-scrollbar-track{background:rgba(0,0,0,.06)}",
    "html .cfg.open{width:100% !important}",
    "html .cards-wrap{overflow-x:auto !important;-webkit-overflow-scrolling:touch !important}",
    "html .loadgrid{grid-template-columns:1fr !important}",
    "html table.zt{font-size:11px !important}",
    "html .delivery-label{flex:0 0 96px !important}",
    "}"
  ].join("\n");

  function injectGanttCss() {
    const fr = document.getElementById('instGanttFrame');
    if (!fr) return 0;
    let doc = null;
    try { doc = fr.contentDocument || (fr.contentWindow && fr.contentWindow.document); } catch (e) { doc = null; }
    if (!doc || !doc.head) return 0;
    if (doc.getElementById('mfix-gantt-css')) return 0;
    const st = doc.createElement('style');
    st.id = 'mfix-gantt-css';
    st.textContent = GANTT_CSS;
    doc.head.appendChild(st);
    return 1;
  }
  window.__mfixGantt = injectGanttCss;
  setInterval(function () { try { injectGanttCss(); } catch (e) { } }, 700);
  document.addEventListener('load', function (e) {
    try {
      const t = e.target;
      if (t && t.id === 'instGanttFrame') injectGanttCss();
    } catch (err) { }
  }, true);
  window.addEventListener('resize', syncTopbarHeight);
  document.addEventListener('app:langchange', syncTopbarHeight);

  /* =====================================================================
     ★M-PDF-20261116：附件预览
     网页里 window.openPdfPreview 只有调用、从未定义，安卓 WebView 的 window.open
     也不会弹新窗口 → 表现就是"点开附件毫无反应"。
     这里用站点自带的 /vendor/pdf.min.js 在页内渲染（无需外部 PDF 阅读器），
     同时接管 window.open 与 <a href="...pdf"> 点击。
     ===================================================================== */
  let pdfDoc = null, pdfPage = 1;

  function closePdf() {
    const ov = document.getElementById('mfix-pdf-ov');
    if (ov) ov.remove();
    pdfDoc = null; pdfPage = 1;
  }

  function ensurePdfOverlay() {
    let ov = document.getElementById('mfix-pdf-ov');
    if (ov) return ov;
    ov = document.createElement('div');
    ov.id = 'mfix-pdf-ov';
    ov.className = 'mfix-pdf-ov';
    ov.innerHTML =
      '<div class="mfix-pdf-head">' +
      '<button type="button" class="mfix-pdf-btn" data-act="close" aria-label="关闭">✕</button>' +
      '<div class="mfix-pdf-name"></div>' +
      '<button type="button" class="mfix-pdf-btn" data-act="prev" aria-label="上一页">‹</button>' +
      '<div class="mfix-pdf-page">1 / 1</div>' +
      '<button type="button" class="mfix-pdf-btn" data-act="next" aria-label="下一页">›</button>' +
      '</div>' +
      '<div class="mfix-pdf-body"><div class="mfix-pdf-msg">…</div></div>';
    ov.addEventListener('click', function (e) {
      const b = e.target && e.target.closest ? e.target.closest('[data-act]') : null;
      if (!b) return;
      const act = b.getAttribute('data-act');
      if (act === 'close') closePdf();
      else if (act === 'prev') gotoPdfPage(pdfPage - 1);
      else if (act === 'next') gotoPdfPage(pdfPage + 1);
    });
    document.body.appendChild(ov);
    return ov;
  }

  function loadPdfLib() {
    return new Promise(function (resolve, reject) {
      if (window.pdfjsLib) return resolve(window.pdfjsLib);
      const s = document.createElement('script');
      s.src = '/vendor/pdf.min.js';
      s.onload = function () {
        if (!window.pdfjsLib) return reject(new Error('pdfjs 未就绪'));
        try { window.pdfjsLib.GlobalWorkerOptions.workerSrc = '/vendor/pdf.worker.min.js'; } catch (e) { }
        resolve(window.pdfjsLib);
      };
      s.onerror = function () { reject(new Error('pdf.js 加载失败')); };
      document.head.appendChild(s);
    });
  }

  function gotoPdfPage(n) {
    if (!pdfDoc) return;
    const total = pdfDoc.numPages || 1;
    pdfPage = Math.min(Math.max(1, n), total);
    const ov = document.getElementById('mfix-pdf-ov');
    if (ov) ov.querySelector('.mfix-pdf-page').textContent = pdfPage + ' / ' + total;
    renderPdfPage();
  }

  function renderPdfPage() {
    const ov = document.getElementById('mfix-pdf-ov');
    if (!ov || !pdfDoc) return;
    const body = ov.querySelector('.mfix-pdf-body');
    pdfDoc.getPage(pdfPage).then(function (page) {
      const vw = Math.max(200, (body.clientWidth || window.innerWidth) - 16);
      const base = page.getViewport({ scale: 1 });
      const vp = page.getViewport({ scale: vw / base.width });
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      let cv = body.querySelector('canvas.mfix-pdf-cv');
      if (!cv) { body.innerHTML = ''; cv = document.createElement('canvas'); cv.className = 'mfix-pdf-cv'; body.appendChild(cv); }
      cv.width = Math.floor(vp.width * dpr);
      cv.height = Math.floor(vp.height * dpr);
      cv.style.width = Math.floor(vp.width) + 'px';
      cv.style.height = Math.floor(vp.height) + 'px';
      const ctx = cv.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      page.render({ canvasContext: ctx, viewport: vp }).promise.then(function () { body.scrollTop = 0; });
    }).catch(function (e) {
      const b = ov.querySelector('.mfix-pdf-body');
      if (b && !b.querySelector('canvas')) b.innerHTML = '<div class="mfix-pdf-msg">渲染失败</div>';
    });
  }

  function openPdf(url, name) {
    const ov = ensurePdfOverlay();
    ov.querySelector('.mfix-pdf-name').textContent = name || '';
    const body = ov.querySelector('.mfix-pdf-body');
    body.innerHTML = '<div class="mfix-pdf-msg">加载中…</div>';
    pdfDoc = null; pdfPage = 1;
    loadPdfLib().then(function (pdfjs) {
      return fetch(url, { credentials: 'same-origin' }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.arrayBuffer();
      }).then(function (buf) { return pdfjs.getDocument({ data: buf }).promise; });
    }).then(function (doc) {
      pdfDoc = doc;
      gotoPdfPage(1);
    }).catch(function (e) {
      body.innerHTML = '<div class="mfix-pdf-msg">无法预览：' + ((e && e.message) || '未知错误') + '</div>';
    });
  }

  window.openPdfPreview = openPdf;
  window.__mfixOpenPdf = openPdf;
  window.__mfixClosePdf = closePdf;

  // 接管 window.open（网页里 3 处附件预览在没有 openPdfPreview 时走这里）
  try {
    const _open = window.open;
    window.open = function (u) {
      const url = String(u || '');
      if (/\.pdf(\?|#|$)/i.test(url) || /\/api\/files\//i.test(url) ||
        /\/api\/won-projects\/[^/]+\/documents\//i.test(url)) {
        openPdf(url, '');
        return null;
      }
      return _open.apply(window, arguments);
    };
  } catch (e) { }

  // 接管附件链接（<a href="...pdf"> 未被 preventDefault 的情况）
  document.addEventListener('click', function (e) {
    const a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    if (a.hasAttribute('download')) return;                       // 下载链接不动
    if (a.closest && a.closest('.mfix-pdf-ov')) return;
    const href = a.getAttribute('href') || '';
    const isFile = /\.pdf(\?|#|$)/i.test(href) || /\/api\/files\//i.test(href) ||
      /\/api\/won-projects\/[^/]+\/documents\//i.test(href);
    if (!isFile) return;
    e.preventDefault();
    e.stopPropagation();
    openPdf(a.href || href, a.getAttribute('title') || '');
  }, true);

  scan(true);
  setTimeout(() => scan(false), 1500);
  return 'installed';
})()
