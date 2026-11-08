(() => {
  if (window.__mfix) { window.__mfix.rescan(); return 'rescan'; }

  // 带 colgroup / 被硬锁的表格：保持原样（不动 table-layout）
  const KEEP_SEL = '#slatsSpecTable, .slats-report-table, .slats-spec-table, #slatsReportOverview';
  const SKIP_TAGS = { TD: 1, TH: 1, SPAN: 1, I: 1, B: 1, EM: 1, LABEL: 1, BUTTON: 1, INPUT: 1, SELECT: 1, TEXTAREA: 1, SVG: 1, PATH: 1, IMG: 1 };
  const CAND = '[class*="scroll"],[class*="wrap"],[class*="tab"],[class*="bar"],section,nav,article';
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
      t.classList.remove('mfix-keep');
      t.style.setProperty('table-layout', 'auto', 'important');
      t.style.setProperty('width', 'auto', 'important');
      t.style.setProperty('min-width', '100%', 'important');
      fixed++;
    }
    return { keep, fixed };
  }

  function scan(full) {
    const t0 = performance.now();
    const root = curRoot();
    const tb = markTables(root);
    const ae = document.activeElement;
    const typing = ae && /^(INPUT|TEXTAREA|SELECT)$/.test(ae.tagName);
    let n = 0;
    if (!typing) {
      const list = root.querySelectorAll(full ? 'div,section,ul,ol,nav,article,form' : CAND);
      for (const el of list) {
        if (SKIP_TAGS[el.tagName]) continue;
        if (el.__mfixOk) continue;
        const cw = el.clientWidth;
        if (cw < 60) continue;
        if (el.scrollWidth <= cw + 6) { el.__mfixOk = 1; continue; }
        const ox = getComputedStyle(el).overflowX;
        if (ox === 'visible' || ox === 'hidden') { el.classList.add('mfix-scroll'); n++; }
        else el.__mfixOk = 1;
      }
    }
    window.__mfixLast = { ms: Math.round(performance.now() - t0), scroll: n, keep: tb.keep, fixed: tb.fixed, full: !!full, root: root.id || 'body' };
    return window.__mfixLast;
  }

  function rescan(full) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => { timer = null; scan(!!full); }, 320);
  }

  window.__mfix = { scan, rescan };
  window.addEventListener('resize', () => rescan(true));
  window.addEventListener('orientationchange', () => rescan(true));
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
  scan(true);
  setTimeout(() => scan(false), 1500);
  return 'installed';
})()
