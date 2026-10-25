var Fa = Object.defineProperty;
var Ha = (n, e, t) => e in n ? Fa(n, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : n[e] = t;
var x = (n, e, t) => Ha(n, typeof e != "symbol" ? e + "" : e, t);
import { Inject as z, Disposable as ue, toDisposable as Zn, UniverInstanceType as _, BuildTextUtils as Ce, IUniverInstanceService as Q, JSONX as k, ObjectRelativeFromH as $n, ObjectRelativeFromV as ot, useDependency as $, ICommandService as y, generateRandomId as pt, DisposableCollection as Dn, CommandType as N, debounce as fi, Tools as X, IUndoRedoService as eo, TextX as me, TextXActionType as W, DOC_RANGE_TYPE as Ge, RANGE_DIRECTION as xe, COLORS as tn, BooleanNumber as L, Rectangle as ka, RxDisposable as At, DataStreamTreeTokenType as U, ILogService as fs, isInternalEditorID as to, createIdentifier as ps, EDITOR_ACTIVATED as wn, FOCUSING_EDITOR_STANDALONE as lr, DEFAULT_EMPTY_DOCUMENT_VALUE as pi, VerticalAlign as Va, HorizontalAlign as _e, IContextService as ms, Direction as se, createInternalEditorID as ja, useObservable as Nn, LocaleService as Ze, DocumentFlavor as ye, PresetListType as Oe, sequenceExecuteAsync as Es, FOCUSING_DOC as hn, FOCUSING_UNIVER_EDITOR as Ss, FOCUSING_COMMON_DRAWINGS as mi, MemoryCursor as St, BaselineOffset as Ne, getBodySlice as Ei, PRESET_LIST_TYPE as Wa, GridType as za, sortRulesFactory as Ga, UpdateDocsAttributeType as no, TableRowHeightRule as Ya, TableSizeType as Si, TableAlignmentType as qa, TableTextWrapType as Ka, SHEET_EDITOR_UNITS as Is, PositionedObjectLayoutType as oo, LRUMap as Xa, ColorKit as dr, DrawingTypeEnum as Cs, skipParseTagNames as Ja, CustomRangeType as Ii, DataStreamTreeNodeType as qt, SliceBodyType as ur, DOCS_NORMAL_EDITOR_UNIT_ID_KEY as vs, normalizeBody as Za, SpacingRule as Bt, DEFAULT_STYLES as Ci, ThemeService as vi, DOCS_ZEN_EDITOR_UNIT_ID_KEY as $e, Injector as so, connectInjector as $a, IConfigService as Rs, QuickListTypeMap as bo, fromEventSubject as nn, DOCS_FORMULA_BAR_EDITOR_UNIT_ID_KEY as ec, checkForSubstrings as tc, UndoCommandId as hr, RedoCommandId as gr, DependentOn as nc, Plugin as oc, merge as sc, touchDependencies as fr, mergeOverrideWithDependencies as rc } from "@univerjs/core";
import { DocSelectionManagerService as G, RichTextEditingMutation as J, DocSkeletonManagerService as ie, SetTextSelectionsOperation as De, DocStateEmitService as ic, DocInterceptorService as ac } from "@univerjs/docs";
import { DeviceInputEventType as Ri, ScrollBar as Vo, IRenderManagerService as fe, Liquid as bi, GlyphType as xi, DocumentSkeletonPageType as Ie, getPageFromPath as jo, getTableIdAndSliceIndex as pr, NORMAL_TEXT_SELECTION_PLUGIN_STYLE as sn, getColor as on, RegularPolygon as Oi, Rect as yn, getOffsetRectForDom as cc, ScrollTimer as Ac, CURSOR_TYPE as mt, getSystemHighlightColor as lc, Vector2 as rn, PageLayoutType as an, DocumentEditArea as ge, Shape as dc, Path as mr, getCharSpaceApply as uc, getNumberUnitValue as ze, hasListGlyph as hc, isIndentByGlyph as gc, isFirstGlyph as fc, getParagraphByGlyph as pc, pixelToPt as mc, ptToPixel as Er, parseDataStreamToTree as Ec, Viewport as Sc, Layer as Sr, Documents as Ic, DocBackground as Cc, lineIterator as vc, getLastColumn as Rc, getLastLine as bc, pxToNum as Ti, TRANSFORM_CHANGE_OBSERVABLE_TYPE as yi, UniverRenderEnginePlugin as xc } from "@univerjs/engine-render";
import { IShortcutService as ro, KeyCode as j, ILayoutService as bs, MetaKeys as K, useEvent as xo, ComponentManager as io, ISidebarService as Bi, IClipboardInterfaceService as Mi, FILE_PNG_CLIPBOARD_MIME_TYPE as _i, FILE__WEBP_CLIPBOARD_MIME_TYPE as Pi, FILE__JPEG_CLIPBOARD_MIME_TYPE as Di, FILE__BMP_CLIPBOARD_MIME_TYPE as wi, HTML_CLIPBOARD_MIME_TYPE as Ni, PLAIN_TEXT_CLIPBOARD_MIME_TYPE as Qi, CopyCommand as Oc, CutCommand as Tc, PasteCommand as yc, IConfirmService as Bc, MenuItemType as Z, getMenuHiddenObservable as ee, FONT_FAMILY_LIST as Mc, FONT_SIZE_LIST as _c, RibbonStartGroup as Ir, ContextMenuPosition as Ui, ContextMenuGroup as Cr, FontFamily as Pc, FontFamilyItem as Dc, FontSize as wc, BuiltInUIPart as Nc, IMenuManagerService as Qc, IUIPartsService as Uc, ICanvasPopupService as Lc, IContextMenuService as Fc } from "@univerjs/ui";
import * as Hc from "react";
import Wo, { useMemo as Fe, useEffect as Re, useCallback as Li, useState as ve, useLayoutEffect as kc, useRef as cn, forwardRef as It, useImperativeHandle as Vc, createElement as Ft } from "react";
import { Subject as Ee, BehaviorSubject as Le, merge as Fi, filter as Qn, takeUntil as st, fromEvent as Ue, combineLatest as ao, Observable as pe, map as gn, distinctUntilChanged as vr, throttleTime as Hi, switchMap as jc, take as Wc, animationFrameScheduler as zc } from "rxjs";
import { filter as zo, bufferTime as Gc, map as Yc } from "rxjs/operators";
import { Checkbox as Rr, InputNumber as An, Button as qc, Slider as Kc, Tooltip as Xc, Select as Jc, ColorPicker as Zc } from "@univerjs/design";
import { ImageSourceType as xs } from "@univerjs/drawing";
var $c = Object.defineProperty, eA = Object.getOwnPropertyDescriptor, tA = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? eA(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && $c(e, t, s), s;
}, br = (n, e) => (t, o) => e(t, o, n);
function nA(n, e) {
  var i, a;
  const { startOffset: t, endOffset: o } = n, s = [];
  let r = -1;
  for (let c = 0; c < e.length; c++) {
    const A = e[c], l = e[c - 1], { startIndex: d } = A;
    t > r && t <= d || o > r && o <= d ? s.push({
      ...A,
      paragraphStart: ((i = l == null ? void 0 : l.startIndex) != null ? i : -1) + 1,
      paragraphEnd: A.startIndex
    }) : d >= t && d <= o && s.push({
      ...A,
      paragraphStart: ((a = l == null ? void 0 : l.startIndex) != null ? a : -1) + 1,
      paragraphEnd: A.startIndex
    }), r = d;
  }
  return s;
}
let Et = class extends ue {
  constructor(e, t) {
    super();
    x(this, "_matches", /* @__PURE__ */ new Map());
    this._univerInstanceService = e, this._textSelectionManagerService = t;
  }
  registerAutoFormat(e) {
    const t = this._matches.get(e.id);
    return t ? (t.push(e), t.sort((o, s) => {
      var r, i;
      return ((r = s.priority) != null ? r : 0) - ((i = o.priority) != null ? i : 0);
    })) : this._matches.set(e.id, [e]), Zn(() => {
      const o = this._matches.get(e.id);
      if (o) {
        const s = o.findIndex((r) => r === e);
        s >= 0 && o.splice(s, 1);
      }
    });
  }
  onAutoFormat(e, t) {
    var a, c, A, l, d, h, u;
    const o = (a = this._matches.get(e)) != null ? a : [], s = this._univerInstanceService.getCurrentUnitForType(_.UNIVER_DOC), r = this._textSelectionManagerService.getDocRanges(), i = (c = r.find((g) => g.isActive)) != null ? c : r[0];
    if (s && i) {
      const g = s.getSelfOrHeaderFooterModel(i.segmentId), f = {
        unit: g,
        selection: i,
        isBody: !i.segmentId,
        paragraphs: nA(i, (l = (A = g.getBody()) == null ? void 0 : A.paragraphs) != null ? l : []),
        customRanges: Ce.customRange.getCustomRangesInterestsWithSelection(i, (h = (d = g.getBody()) == null ? void 0 : d.customRanges) != null ? h : []),
        commandId: e,
        commandParams: t
      }, p = o.find((m) => m.match(f));
      return (u = p == null ? void 0 : p.getMutations(f)) != null ? u : [];
    }
    return [];
  }
};
Et = tA([
  br(0, Q),
  br(1, z(G))
], Et);
const oA = {
  undo: !0,
  redo: !0,
  // Undo redo
  font: !0,
  // 'font'
  fontSize: !0,
  // 'Font size'
  bold: !0,
  // 'Bold (Ctrl+B)'
  italic: !0,
  // 'Italic (Ctrl+I)'
  strikethrough: !0,
  // 'Strikethrough (Alt+Shift+5)'
  underline: !0,
  // 'Underline (Alt+Shift+6)'
  textColor: !0,
  // 'Text color'
  fillColor: !0,
  // 'Cell color'
  horizontalAlignMode: !0,
  // 'Horizontal alignment'
  verticalAlignMode: !0,
  // 'Vertical alignment'
  textWrapMode: !0,
  // 'Wrap mode'
  textRotateMode: !0
  // 'Text Rotation Mode'
}, sA = {
  outerLeft: !1,
  outerRight: !1,
  header: !0,
  footer: !0,
  innerLeft: !1,
  innerRight: !1,
  frozenHeaderLT: !1,
  frozenHeaderRT: !1,
  frozenHeaderLM: !1,
  frozenContent: !1,
  infoBar: !0,
  toolbar: !0
}, rA = "DOC_UI_PLUGIN";
var We = /* @__PURE__ */ ((n) => (n.MAIN = "__Document_Render_Main__", n.BACKGROUND = "__Document_Render_Background__", n))(We || {}), Xe = /* @__PURE__ */ ((n) => (n.VIEW_MAIN = "viewMain", n.VIEW_TOP = "viewTop", n.VIEW_LEFT = "viewLeft", n.VIEW_LEFT_TOP = "viewLeftTop", n))(Xe || {});
const iA = 0, Oo = 2, aA = 4, xr = 10, ef = "normalTextSelectionPluginName";
function rt(n) {
  const { mainComponent: e, scene: t, engine: o, components: s } = n, r = e, i = s.get(We.BACKGROUND);
  return {
    document: r,
    docBackground: i,
    scene: t,
    engine: o
  };
}
function cA(n, e) {
  const t = n.getCurrentUnitForType(_.UNIVER_DOC);
  if (!t)
    return null;
  const o = t.getUnitId(), s = e.getRenderById(o);
  if (s == null)
    return;
  const { mainComponent: r, scene: i, engine: a, components: c } = s, A = r, l = c.get(We.BACKGROUND);
  return {
    document: A,
    docBackground: l,
    scene: i,
    engine: a
  };
}
function tf(n, e) {
  const t = e.getRenderById(n);
  if (t == null)
    return;
  const { mainComponent: o, scene: s, engine: r, components: i } = t, a = o, c = i.get(We.BACKGROUND);
  return {
    document: a,
    docBackground: c,
    scene: s,
    engine: r
  };
}
function AA(n) {
  const { unitId: e, ranges: t, id: o, type: s, segmentId: r } = n, i = {
    id: J.id,
    params: {
      unitId: e,
      actions: [],
      textRanges: void 0,
      // noHistory: true,
      segmentId: r
    }
  }, a = k.getInstance(), c = Ce.customDecoration.add({ ranges: t, id: o, type: s });
  return i.params.actions = a.editOp(c.serialize()), i;
}
function nf(n, e) {
  const { segmentId: t, id: o, type: s, unitId: r } = e, i = n.get(G), a = n.get(Q), c = r ? a.getUnit(r, _.UNIVER_DOC) : a.getCurrentUnitForType(_.UNIVER_DOC);
  if (!c)
    return !1;
  const A = c.getUnitId(), l = i.getTextRanges({ unitId: A, subUnitId: A });
  return !l || !c.getBody() ? !1 : AA(
    {
      unitId: A,
      ranges: l,
      id: o,
      type: s,
      segmentId: t
    }
  );
}
function of(n, e) {
  const { unitId: t, id: o, segmentId: s } = e, i = n.get(Q).getUnit(t);
  if (!i)
    return !1;
  const a = {
    id: J.id,
    params: {
      unitId: t,
      actions: [],
      textRanges: void 0,
      // noHistory: true,
      segmentId: s
    }
  }, c = Ce.customDecoration.delete({ id: o, segmentId: s, documentDataModel: i });
  if (!c)
    return !1;
  const A = k.getInstance();
  return a.params.actions = A.editOp(c.serialize()), a;
}
function sf(n, e) {
  return e.some((t) => n.startIndex > t.startIndex && n.startIndex < t.endIndex);
}
function co(n, e, t, o) {
  const s = {
    st: 0,
    ed: 0,
    ts: t
  };
  for (let r = n.length - 1; r >= 0; r--) {
    const i = n[r], { st: a, ed: c } = i;
    e > a && e <= c && (s.st = a, s.ed = c, s.ts = {
      ...s.ts,
      ...i.ts
    });
  }
  if (e === 0) {
    const r = n == null ? void 0 : n[0];
    r && r.st === 0 && (s.ts = {
      ...s.ts,
      ...r.ts
    });
  }
  return o && (s.ts = {
    ...s.ts,
    ...o
  }), s;
}
function Os(n, e, t) {
  if (t) {
    const s = n.find((r) => e >= r.startIndex && e <= r.endIndex + 1);
    return s != null && s.wholeEntity ? null : s;
  }
  const o = n.find((s) => e > s.startIndex && e <= s.endIndex);
  return o != null && o.wholeEntity ? null : o;
}
function Ts(n, e) {
  return n.filter((t) => e > t.startIndex && e <= t.endIndex);
}
function rf(n) {
  return {
    left: n.positionH.posOffset,
    top: n.positionV.posOffset,
    width: n.size.width,
    height: n.size.height
  };
}
function af(n, e = 0, t = 0) {
  return {
    size: {
      width: n.width,
      height: n.height
    },
    positionH: {
      relativeFrom: $n.MARGIN,
      posOffset: (n.left || 0) - e
    },
    positionV: {
      relativeFrom: ot.PAGE,
      posOffset: (n.top || 0) - t
    },
    angle: n.angle || 0
  };
}
function lA(n, e, t) {
  const o = $(y), s = $(ro), r = Fe(() => pt(4), []);
  Re(() => {
    if (!t || !n || !e)
      return;
    const a = `sheet.operation.editor-${t.getEditorId()}-keyboard-${r}`, c = new Dn();
    return c.add(o.registerCommand({
      id: a,
      type: N.OPERATION,
      handler(A, l) {
        const { keyCode: d, metaKey: h } = l;
        e.handler(d, h);
      }
    })), e.keyCodes.map((A) => ({
      id: a,
      binding: A.metaKey ? A.keyCode | A.metaKey : A.keyCode,
      preconditions: () => !0,
      priority: 901,
      staticParameters: {
        eventType: Ri.Keyboard,
        keyCode: A.keyCode,
        metaKey: A.metaKey
      }
    })).forEach((A) => {
      c.add(s.registerShortcut(A));
    }), () => {
      c.dispose();
    };
  }, [o, e, t, n, r, s]);
}
const dA = (n, e = !0, t, o) => {
  const s = Li(() => {
    if (n) {
      const { scene: i, mainComponent: a } = n.render, c = n.render.with(ie), { width: A, height: l } = n.getBoundingClientRect();
      c.getViewModel().getDataModel().updateDocumentDataPageSize(e ? 1 / 0 : A, 1 / 0), i.transformByState({
        width: A,
        height: l
      }), a == null || a.resize(A, l);
    }
  }, [n, e]), r = Fe(() => fi(() => {
    var E, I;
    if (!t || !n || !t)
      return;
    const a = n.render.with(ie).getSkeleton(), { scene: c, mainComponent: A } = n.render, l = c.getViewport(Xe.VIEW_MAIN), { actualWidth: d, actualHeight: h } = a.getActualSize(), { width: u, height: g } = n.getBoundingClientRect();
    let f = l == null ? void 0 : l.getScrollBar();
    const p = Math.max(d, u), m = Math.max(h, g);
    c.transformByState({
      width: p,
      height: m
    }), A == null || A.resize(p, m), e ? d > u ? (f == null ? l && new Vo(l, {
      barSize: 8,
      enableVertical: !1,
      enableHorizontal: !0,
      minThumbSizeV: 8
    }) : l == null || l.resetCanvasSizeAndUpdateScroll(), o && (l == null || l.scrollToBarPos({ x: 1 / 0, y: 0 }))) : (f = null, l == null || l.scrollToBarPos({ x: 0, y: 0 }), (I = l == null ? void 0 : l.getScrollBar()) == null || I.dispose()) : h > g ? (f == null ? l && (f = new Vo(l, {
      enableHorizontal: !1,
      enableVertical: !0,
      barSize: 8,
      minThumbSizeV: 8
    })) : l == null || l.resetCanvasSizeAndUpdateScroll(), o && (l == null || l.scrollToBarPos({ x: 0, y: 1 / 0 }))) : (f = null, l == null || l.scrollToBarPos({ x: 0, y: 0 }), (E = l == null ? void 0 : l.getScrollBar()) == null || E.dispose());
  }, 30), [n, t, e, o]);
  return Re(() => {
    if (t && n) {
      const i = setTimeout(() => {
        s(), r();
      }, 500);
      return () => {
        clearTimeout(i);
      };
    }
  }, [n, t, s, r]), Re(() => {
    if (t && n) {
      const i = n.input$.subscribe(() => {
        r();
      });
      return () => {
        i.unsubscribe();
      };
    }
  }, [n, t, r]), { resize: s, checkScrollBar: r };
};
var To = { exports: {} }, Kt = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Or;
function uA() {
  if (Or) return Kt;
  Or = 1;
  var n = Wo, e = Symbol.for("react.element"), t = Symbol.for("react.fragment"), o = Object.prototype.hasOwnProperty, s = n.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, r = { key: !0, ref: !0, __self: !0, __source: !0 };
  function i(a, c, A) {
    var l, d = {}, h = null, u = null;
    A !== void 0 && (h = "" + A), c.key !== void 0 && (h = "" + c.key), c.ref !== void 0 && (u = c.ref);
    for (l in c) o.call(c, l) && !r.hasOwnProperty(l) && (d[l] = c[l]);
    if (a && a.defaultProps) for (l in c = a.defaultProps, c) d[l] === void 0 && (d[l] = c[l]);
    return { $$typeof: e, type: a, key: h, ref: u, props: d, _owner: s.current };
  }
  return Kt.Fragment = t, Kt.jsx = i, Kt.jsxs = i, Kt;
}
var Tr;
function hA() {
  return Tr || (Tr = 1, To.exports = uA()), To.exports;
}
var w = hA();
function ki(n) {
  var e, t, o = "";
  if (typeof n == "string" || typeof n == "number") o += n;
  else if (typeof n == "object") if (Array.isArray(n)) {
    var s = n.length;
    for (e = 0; e < s; e++) n[e] && (t = ki(n[e])) && (o && (o += " "), o += t);
  } else for (t in n) n[t] && (o && (o += " "), o += t);
  return o;
}
function Un() {
  for (var n, e, t = 0, o = "", s = arguments.length; t < s; t++) (n = arguments[t]) && (e = ki(n)) && (o && (o += " "), o += e);
  return o;
}
function ke(n, e) {
  var o;
  return (o = n.get(fe).getRenderById(e)) == null ? void 0 : o.with(ie);
}
function le(n, e = "") {
  if (!e)
    return ["body"];
  const { headers: t, footers: o } = n.getSnapshot();
  if (t == null && o == null)
    throw new Error("Document data model must have headers or footers when update by segment id");
  if ((t == null ? void 0 : t[e]) != null)
    return ["headers", e, "body"];
  if ((o == null ? void 0 : o[e]) != null)
    return ["footers", e, "body"];
  throw new Error("Segment id not found in headers or footers");
}
const Vi = {
  id: "doc.command-replace-snapshot",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function, complexity
  handler: (n, e) => {
    const { unitId: t, snapshot: o, textRanges: s, segmentId: r = "", options: i } = e, a = n.get(Q), c = n.get(y), A = n.get(G), l = a.getUnit(t, _.UNIVER_DOC), d = l == null ? void 0 : l.getSelfOrHeaderFooterModel(r).getSnapshot();
    if (l == null || d == null)
      return !1;
    const { body: h, tableSource: u, footers: g, headers: f, lists: p, drawings: m, drawingsOrder: E, documentStyle: I } = X.deepClone(o), {
      body: v,
      tableSource: R,
      footers: S,
      headers: C,
      lists: T,
      drawings: O,
      drawingsOrder: P,
      documentStyle: b
    } = d;
    if (h == null || v == null)
      return !1;
    if (X.diffValue(h, v) && s)
      return A.replaceDocRanges(s, {
        unitId: t,
        subUnitId: t
      }, !1), !0;
    const B = {
      id: J.id,
      params: {
        unitId: t,
        actions: [],
        textRanges: s
      }
    };
    i && (B.params.options = i);
    const M = [], H = k.getInstance();
    if (!X.diffValue(b, I)) {
      const D = H.replaceOp(["documentStyle"], b, I);
      D != null && M.push(D);
    }
    if (!X.diffValue(h, v)) {
      const D = H.replaceOp(["body"], v, h);
      D != null && M.push(D);
    }
    if (!X.diffValue(u, R)) {
      const D = H.replaceOp(["tableSource"], R, u);
      D != null && M.push(D);
    }
    if (!X.diffValue(g, S)) {
      const D = H.replaceOp(["footers"], S, g);
      D != null && M.push(D);
    }
    if (!X.diffValue(f, C)) {
      const D = H.replaceOp(["headers"], C, f);
      D != null && M.push(D);
    }
    if (!X.diffValue(p, T)) {
      const D = H.replaceOp(["lists"], T, p);
      D != null && M.push(D);
    }
    if (!X.diffValue(m, O)) {
      const D = H.replaceOp(["drawings"], O, m);
      D != null && M.push(D);
    }
    if (!X.diffValue(E, P)) {
      const D = H.replaceOp(["drawingsOrder"], P, E);
      D != null && M.push(D);
    }
    return B.params.actions = M.reduce((D, te) => k.compose(D, te), null), !!c.syncExecuteCommand(B.id, B.params);
  }
}, gA = {
  id: "doc.command-replace-content",
  type: N.COMMAND,
  handler: async (n, e) => {
    const { unitId: t, body: o, textRanges: s, segmentId: r = "", options: i } = e, a = n.get(Q), c = n.get(y), A = n.get(G), l = a.getUnit(t, _.UNIVER_DOC), d = l == null ? void 0 : l.getSelfOrHeaderFooterModel(r).getSnapshot().body;
    if (l == null || d == null)
      return !1;
    const h = ji(t, r, l, d, o);
    return h.params.textRanges = s, i && (h.params.options = i), h.params.actions == null && s ? (A.replaceDocRanges(s, {
      unitId: t,
      subUnitId: t
    }, !1), !0) : !!c.syncExecuteCommand(h.id, h.params);
  }
}, fA = {
  id: "doc.command-cover-content",
  type: N.COMMAND,
  handler: async (n, e) => {
    const { unitId: t, body: o, segmentId: s = "" } = e, r = n.get(Q), i = n.get(y), a = n.get(eo), c = r.getUniverDocInstance(t), A = c == null ? void 0 : c.getSnapshot().body;
    if (c == null || A == null)
      return !1;
    const l = ji(t, s, c, A, o);
    return l.params.noNeedSetTextRange = !0, l.params.noHistory = !0, i.syncExecuteCommand(
      l.id,
      l.params
    ), a.clearUndoRedo(t), !0;
  }
};
function pA(n, e, t, o) {
  const s = new me(), r = k.getInstance(), i = (t == null ? void 0 : t.dataStream.length) - 2;
  i > 0 && s.push({
    t: W.DELETE,
    len: i
  }), o.dataStream.length > 0 && s.push({
    t: W.INSERT,
    body: o,
    len: o.dataStream.length
  });
  const a = le(e, n);
  return r.editOp(s.serialize(), a);
}
function ji(n, e, t, o, s) {
  const r = {
    id: J.id,
    params: {
      unitId: n,
      actions: [],
      textRanges: []
    }
  }, i = pA(e, t, o, s);
  return r.params.actions = i, r;
}
N.COMMAND;
const mA = {
  id: "doc.command.replace-text-runs",
  type: N.COMMAND,
  handler: (n, e) => {
    const { unitId: t, body: o, textRanges: s, segmentId: r = "", options: i } = e, a = n.get(Q), c = n.get(y), A = a.getUnit(t, _.UNIVER_DOC), l = A == null ? void 0 : A.getSelfOrHeaderFooterModel(r).getSnapshot().body;
    if (A == null || l == null)
      return !1;
    const d = Ce.selection.replaceTextRuns({
      doc: A,
      body: o,
      selection: {
        startOffset: 0,
        endOffset: l.dataStream.length - 2,
        collapsed: !1
      }
    });
    if (!d)
      return !1;
    const h = {
      id: J.id,
      params: {
        unitId: t,
        actions: [],
        textRanges: s,
        noHistory: !0
      }
    }, u = k.getInstance(), g = le(A, r);
    return h.params.actions = u.editOp(d.serialize(), g), h.params.textRanges = s, i && (h.params.options = i), !!c.syncExecuteCommand(h.id, h.params);
  }
};
var Bn = /* @__PURE__ */ ((n) => (n[n.page = 0] = "page", n[n.section = 1] = "section", n[n.column = 2] = "column", n[n.line = 3] = "line", n[n.divide = 4] = "divide", n[n.glyph = 5] = "glyph", n))(Bn || {});
const Tt = {
  page: 0,
  section: 1,
  column: 2,
  line: 3,
  divide: 4,
  glyph: 5
};
function ys(n, e) {
  return n.page > e.page ? !1 : n.page < e.page ? !0 : n.section > e.section ? !1 : n.section < e.section ? !0 : n.column > e.column ? !1 : n.column < e.column ? !0 : n.line > e.line ? !1 : n.line < e.line ? !0 : n.divide > e.divide ? !1 : n.divide < e.divide ? !0 : n.glyph > e.glyph ? !1 : (n.glyph < e.glyph, !0);
}
function Go(n, e) {
  return ys(n, e) ? {
    start: n,
    end: e
  } : {
    start: e,
    end: n
  };
}
function yr(n) {
  const e = n.length;
  if (e === 0)
    return;
  const t = n[0], o = n[e - 1], s = n.length === 1 && t.collapsed;
  return {
    startOffset: t.startOffset,
    endOffset: o.endOffset,
    collapsed: s
  };
}
function EA(n, e, t, o) {
  let s = o, r = o;
  for (let i = 0; i < n.length; i++) {
    const c = n[i].count;
    i < e && (s += c), i < t && (r += c);
  }
  return {
    startOffset: s,
    endOffset: r
  };
}
function Yo(n) {
  const { startX: e, startY: t, endX: o, endY: s } = n, r = [];
  return r.push({
    x: e,
    y: t
  }), r.push({
    x: o,
    y: t
  }), r.push({
    x: o,
    y: s
  }), r.push({
    x: e,
    y: s
  }), r.push({
    x: e,
    y: t
  }), r;
}
class it {
  constructor(e, t) {
    x(this, "_liquid", new bi());
    x(this, "_currentStartState", {
      page: 0,
      section: 0,
      column: 0,
      line: 0,
      divide: 0,
      glyph: 0
      /* NORMAL */
    });
    x(this, "_currentEndState", {
      page: 0,
      section: 0,
      column: 0,
      line: 0,
      divide: 0,
      glyph: 0
      /* NORMAL */
    });
    this._documentOffsetConfig = e, this._docSkeleton = t;
  }
  // eslint-disable-next-line max-lines-per-function
  getRangePointData(e, t) {
    const o = [], s = [], r = [];
    if (e == null || t == null)
      return {
        borderBoxPointGroup: o,
        contentBoxPointGroup: s,
        cursorList: r
      };
    if (!this._isValidPosition(e, t))
      throw new Error(
        `
                Invalid positions in NodePositionConvertToCursor,
                they are not in the same segment page when in header or footer.`
      );
    const { start: a, end: c } = Go(e, t);
    return this._selectionIterator(a, c, (A, l, d, h, u, g) => {
      const { lineHeight: f, asc: p, paddingTop: m, marginTop: E, marginBottom: I } = g, { glyphGroup: v, st: R } = u;
      if (v.length === 0)
        return;
      const { x: S, y: C } = this._liquid;
      let T, O;
      const P = v[A], b = v[l], B = v[A - 1], M = (P == null ? void 0 : P.left) || 0, H = (P == null ? void 0 : P.width) || 0, F = (b == null ? void 0 : b.left) || 0, D = (b == null ? void 0 : b.width) || 0, te = (P == null ? void 0 : P.glyphType) === xi.LIST, { startOffset: q, endOffset: V } = EA(v, A, l, R), Y = a.glyph === A && d ? a.isBack : !0, oe = c.glyph === l && h ? c.isBack : !1, ce = a === c, he = Y && B != null ? B : P;
      if (A === 0 && l === v.length - 1)
        T = {
          startX: S + M + (te ? H : 0),
          startY: C,
          endX: S + F + (oe ? 0 : D),
          endY: C + f - E - I
        }, O = {
          startX: S + M + (te ? H : 0),
          startY: C + m + p - he.bBox.ba,
          endX: S + F + (oe ? 0 : D),
          endY: C + m + p + he.bBox.bd
        };
      else {
        const Ae = Y && !te;
        T = {
          startX: S + M + (Ae ? 0 : H),
          startY: C,
          endX: S + F + (oe ? 0 : D),
          endY: C + f - E - I
        }, O = {
          startX: S + M + (Ae ? 0 : H),
          startY: C + m + p - he.bBox.ba,
          endX: S + F + (oe ? 0 : D),
          endY: C + m + p + he.bBox.bd
        };
      }
      o.push(Yo(T)), s.push(Yo(O)), r.push({
        startOffset: Y ? q : q + P.count,
        endOffset: oe ? V : V + b.count,
        collapsed: ce
      });
    }), {
      borderBoxPointGroup: o,
      contentBoxPointGroup: s,
      cursorList: r
    };
  }
  _isValidPosition(e, t) {
    const { segmentPage: o, pageType: s } = e, { segmentPage: r, pageType: i } = t;
    return s !== i ? !1 : s === Ie.HEADER || s === Ie.FOOTER ? o === r : !0;
  }
  _resetCurrentNodePositionState() {
    this._currentStartState = {
      page: 0,
      section: 0,
      column: 0,
      line: 0,
      divide: 0,
      glyph: 0
      /* NORMAL */
    }, this._currentEndState = {
      page: 0,
      section: 0,
      column: 0,
      line: 0,
      divide: 0,
      glyph: 0
      /* NORMAL */
    };
  }
  _setNodePositionState(e = 0, t, o, s) {
    s === t ? this._currentStartState[e] = 1 : this._currentStartState[e] = 0, s === o ? this._currentEndState[e] = 2 : this._currentEndState[e] = 0;
  }
  _checkPreviousNodePositionState(e, t = !0) {
    let o = e, s;
    for (; o >= 0; ) {
      const r = Bn[o];
      let i;
      if (t ? i = this._currentStartState[r] : i = this._currentEndState[r], i === void 0)
        return;
      if (s === void 0 && (s = i), i !== s)
        return 0;
      o--;
    }
    return s;
  }
  _getSelectionRuler(e, t, o, s, r) {
    let i = 0, a = s;
    const c = Bn[e], A = Bn[e + 1];
    if (A === null || c === null)
      return {
        start_next: i,
        end_next: a
      };
    const l = t[c], d = o[c];
    this._setNodePositionState(c, l, d, r);
    const h = this._checkPreviousNodePositionState(e), u = this._checkPreviousNodePositionState(e, !1);
    return h === 1 && (i = t[A]), u === 2 && (a = o[A]), {
      start_next: i,
      end_next: a
    };
  }
  // eslint-disable-next-line max-lines-per-function, complexity
  _selectionIterator(e, t, o) {
    var v, R;
    const s = this._docSkeleton;
    if (!s)
      return [];
    const { pageType: r, path: i } = e;
    this._liquid.reset();
    const a = s.getSkeletonData();
    if (a == null)
      return [];
    const { pages: c, skeHeaders: A, skeFooters: l } = a, { page: d, segmentPage: h } = e, { page: u, segmentPage: g } = t;
    if (this._resetCurrentNodePositionState(), this._documentOffsetConfig == null)
      return [];
    const { pageLayoutType: f, pageMarginLeft: p, pageMarginTop: m } = this._documentOffsetConfig, E = r === Ie.BODY || r === Ie.CELL ? d : h;
    for (let S = 0; S < E; S++) {
      const C = c[S];
      this._liquid.translatePage(C, f, p, m);
    }
    const I = r === Ie.BODY || r === Ie.CELL ? u : g;
    for (let S = E; S <= I; S++) {
      const C = c[S], { headerId: T, footerId: O, pageWidth: P } = C;
      let b = C;
      if (r === Ie.HEADER ? b = (v = A.get(T)) == null ? void 0 : v.get(P) : r === Ie.FOOTER ? b = (R = l.get(O)) == null ? void 0 : R.get(P) : r === Ie.CELL && (b = jo(a, i)), b == null) {
        this._liquid.translatePage(C, f, p, m);
        continue;
      }
      const B = b.sections, { start_next: M, end_next: H } = this._getSelectionRuler(
        Tt.page,
        e,
        t,
        B.length - 1,
        r === Ie.BODY || r === Ie.CELL ? S : 0
      );
      switch (this._liquid.translateSave(), r) {
        case Ie.HEADER:
          this._liquid.translatePagePadding({
            ...b,
            marginLeft: C.marginLeft
            // Because header or footer margin Left is 0.
          });
          break;
        case Ie.FOOTER: {
          const F = C.pageHeight - b.height - b.marginBottom;
          this._liquid.translate(C.marginLeft, F);
          break;
        }
        case Ie.CELL: {
          this._liquid.translatePagePadding(C);
          const F = b.parent, D = F.parent, { left: te } = b, { top: q, left: V } = D, { top: Y } = F;
          this._liquid.translate(V + te, q + Y), this._liquid.translatePagePadding(b);
          break;
        }
        default:
          this._liquid.translatePagePadding(C);
          break;
      }
      for (let F = M; F <= H; F++) {
        const D = B[F], te = D.columns, { start_next: q, end_next: V } = this._getSelectionRuler(
          Tt.section,
          e,
          t,
          te.length - 1,
          F
        );
        this._liquid.translateSection(D);
        for (let Y = q; Y <= V; Y++) {
          const oe = te[Y], ce = oe.lines, { start_next: he, end_next: Ae } = this._getSelectionRuler(
            Tt.column,
            e,
            t,
            ce.length - 1,
            Y
          );
          this._liquid.translateColumn(oe);
          for (let ne = he; ne <= Ae; ne++) {
            const ae = ce[ne], { divides: Te } = ae, { start_next: je, end_next: ut } = this._getSelectionRuler(
              Tt.line,
              e,
              t,
              Te.length - 1,
              ne
            );
            this._liquid.translateSave(), this._liquid.translateLine(ae, !0, !1);
            for (let we = je; we <= ut; we++) {
              const Yt = Te[we];
              this._liquid.translateSave(), this._liquid.translateDivide(Yt);
              const { glyphGroup: Qa } = Yt, { start_next: Ua, end_next: La } = this._getSelectionRuler(
                Tt.divide,
                e,
                t,
                Qa.length - 1,
                we
              );
              let cr = !1, Ar = !1;
              S === E && F === M && Y === q && ne === he && we === je && (cr = !0), S === I && F === H && Y === V && ne === Ae && we === ut && (Ar = !0), o && o(Ua, La, cr, Ar, Yt, ae, oe, D, b), this._liquid.translateRestore();
            }
            this._liquid.translateRestore();
          }
        }
      }
      this._liquid.translateRestore(), this._liquid.translatePage(C, f, p, m);
    }
  }
}
function SA(n, e) {
  const { path: t } = n, { path: o } = e;
  if (t.length !== o.length || t.indexOf("cells") === -1)
    return !1;
  const s = t.indexOf("skeTables") + 1, r = t.indexOf("rows") + 1, i = t.indexOf("cells") + 1, { tableId: a, sliceIndex: c } = pr(t[s]), { tableId: A, sliceIndex: l } = pr(o[s]);
  if (a !== A)
    return !1;
  const d = t[r], h = o[r], u = t[i], g = o[i];
  return !(d === h && u === g && c === l);
}
function Wi(n, e) {
  const { path: t } = n, { path: o } = e;
  return t.indexOf("cells") === -1 || o.indexOf("cells") === -1 || t.length !== o.length ? !1 : X.diffValue(t, o);
}
function zi(n, e, t) {
  var u, g, f, p, m, E, I, v;
  const { path: o } = e, { path: s } = t;
  if (o.indexOf("cells") === -1 || s.indexOf("cells") === -1)
    return !1;
  const r = n.findGlyphByPosition(e), i = n.findGlyphByPosition(t), a = (p = (f = (g = (u = r == null ? void 0 : r.parent) == null ? void 0 : u.parent) == null ? void 0 : g.parent) == null ? void 0 : f.parent) == null ? void 0 : p.parent, c = (v = (I = (E = (m = i == null ? void 0 : i.parent) == null ? void 0 : m.parent) == null ? void 0 : E.parent) == null ? void 0 : I.parent) == null ? void 0 : v.parent;
  if (a == null || c == null)
    return !1;
  const A = a.parent, l = c.parent, d = A.cells.indexOf(a), h = l.cells.indexOf(c);
  return d === h && A.index === l.index;
}
function yo(n, e) {
  if (Wi(n, e))
    return ys(n, e);
  const { path: t } = n, { path: o } = e, s = t[t.length - 5], r = o[o.length - 5];
  if (s !== r && typeof s == "string" && typeof r == "string") {
    const l = s.split("#-#")[1], d = r.split("#-#")[1];
    return +l < +d;
  }
  const i = t[t.length - 3], a = o[o.length - 3], c = t[t.length - 1], A = o[o.length - 1];
  return i < a ? !0 : i > a ? !1 : c <= A;
}
function vt(n) {
  return n.sections[0].columns[0].lines.length === 0;
}
function IA(n, e, t) {
  let o = e, s = t, r = n[o], i = n[s];
  for (; o < s && (vt(r) || vt(i)); )
    vt(r) ? (o++, r = n[o]) : vt(i) && (s--, i = n[s]);
  if (!vt(r) && !vt(i))
    return [r, i];
}
class Gi {
  constructor(e, t) {
    x(this, "_liquid", new bi());
    this._documentOffsetConfig = e, this._docSkeleton = t;
  }
  // eslint-disable-next-line max-lines-per-function
  getRangePointData(e, t) {
    const o = [], r = this._docSkeleton.getSkeletonData();
    if (r == null)
      return;
    const { pages: i } = r, { segmentPage: a, page: c, pageType: A } = e, l = this._getTableRectRangeInfo(e, t);
    if (l == null)
      return;
    const {
      tableId: d,
      startRowIndex: h,
      startColumnIndex: u,
      endRowIndex: g,
      endColumnIndex: f
    } = l;
    this._liquid.reset();
    const { pageLayoutType: p, pageMarginLeft: m, pageMarginTop: E } = this._documentOffsetConfig, I = A === Ie.BODY || A === Ie.CELL ? c : a;
    for (let v = 0; v < I; v++) {
      const R = i[v];
      this._liquid.translatePage(R, p, m, E);
    }
    for (let v = I; v < i.length; v++) {
      const R = i[v];
      this._liquid.translatePagePadding(R);
      const { skeTables: S } = R;
      let C = null;
      for (const [b, B] of S.entries())
        b.startsWith(d) && (C = B);
      if (C == null) {
        this._liquid.restorePagePadding(R), this._liquid.translatePage(R, p, m, E);
        continue;
      }
      this._liquid.translateSave(), this._liquid.translate(0, C.top);
      const { x: T, y: O } = this._liquid, { left: P } = C;
      for (const b of C.rows)
        if (b.index >= h && b.index <= g) {
          const B = IA(b.cells, u, f);
          if (B == null)
            continue;
          const [M, H] = B, F = {
            startX: T + M.left + P,
            startY: O + b.top,
            endX: T + H.left + H.pageWidth + P,
            endY: O + b.top + b.height
          };
          o.push(Yo(F));
        }
      this._liquid.translateRestore(), this._liquid.restorePagePadding(R), this._liquid.translatePage(R, p, m, E);
    }
    return {
      pointGroup: o,
      startRow: h,
      startColumn: u,
      endRow: g,
      endColumn: f,
      tableId: d
    };
  }
  getNodePositionGroup(e, t) {
    const o = [], s = this._docSkeleton.findCharIndexByPosition(e), r = this._docSkeleton.findCharIndexByPosition(t);
    if (s == null || r == null)
      return;
    const i = s < r, a = this._getTableRectRangeInfo(e, t);
    if (a == null)
      return;
    const { tableId: c, startRowIndex: A, startColumnIndex: l, endRowIndex: d, endColumnIndex: h } = a, u = this._docSkeleton.getViewModel().findTableNodeById(c);
    if (u == null)
      return;
    const g = u.children[0].children.length;
    if (l === 0 && h === g - 1) {
      const p = u.children[A].children[l], m = this._docSkeleton.findNodePositionByCharIndex(p.startIndex + 1), E = u.children[d].children[h], I = this._docSkeleton.findNodePositionByCharIndex(E.endIndex - 2);
      if (m == null || I == null)
        return;
      o.push({
        anchor: i ? m : I,
        focus: i ? I : m
      });
    } else
      for (let p = A; p <= d; p++) {
        const m = u.children[p], E = m.children[l], I = m.children[h], v = this._docSkeleton.findNodePositionByCharIndex(E.startIndex + 1), R = this._docSkeleton.findNodePositionByCharIndex(I.endIndex - 2);
        if (v == null || R == null)
          return;
        o.push({
          anchor: i ? v : R,
          focus: i ? R : v
        });
      }
    return o;
  }
  _getTableRectRangeInfo(e, t) {
    const s = this._docSkeleton.getSkeletonData();
    if (s == null)
      return;
    const { pages: r } = s, { path: i } = e, { path: a } = t, c = jo(s, i), A = jo(s, a);
    if (c == null || A == null)
      return;
    const l = c.segmentId, d = c.parent.index, h = c.parent.cells.indexOf(c), u = (A == null ? void 0 : A.parent).index, g = (A == null ? void 0 : A.parent).cells.indexOf(A), f = Math.min(d, u), p = Math.max(d, u), m = Math.min(h, g), E = Math.max(h, g);
    return {
      pages: r,
      tableId: l,
      startRowIndex: f,
      startColumnIndex: m,
      endRowIndex: p,
      endColumnIndex: E
    };
  }
}
const CA = "__TestSelectionRange__", vA = "__TestSelectionAnchor__", Br = 6, Bo = 500, RA = 500, qo = 3;
function Mn(n) {
  const e = n[0], t = e[0], o = e[2], { x: s, y: r } = t, { x: i, y: a } = o;
  return {
    left: s,
    top: r,
    width: i - s,
    height: a - r
  };
}
function Bs(n) {
  return n.map((e) => {
    let t = 1 / 0, o = -1 / 0, s = 1 / 0, r = -1 / 0;
    return e.forEach((i) => {
      t = Math.min(i.x, t), o = Math.max(i.x, o), r = Math.max(i.y, r), s = Math.min(i.y, s);
    }), {
      left: t,
      right: o,
      top: s,
      bottom: r
    };
  });
}
class Mt {
  constructor(e, t, o, s, r, i = sn, a = "", c = -1) {
    x(this, "rangeType", Ge.TEXT);
    // Identifies whether the range is the current one, most of which is the last range.
    x(this, "_current", !1);
    // The rendered range graphic when collapsed is false
    x(this, "_rangeShape");
    // The rendered range graphic when collapsed is true
    x(this, "_anchorShape");
    x(this, "_cursorList", []);
    x(this, "_anchorBlinkTimer", null);
    this._scene = e, this._document = t, this._docSkeleton = o, this.anchorNodePosition = s, this.focusNodePosition = r, this.style = i, this._segmentId = a, this._segmentPage = c, this._anchorBlink(), this.refresh();
  }
  _anchorBlink() {
    setTimeout(() => {
      this._anchorShape && this._anchorShape.visible && this.deactivateStatic();
    }, Bo), this._anchorBlinkTimer = setInterval(() => {
      this._anchorShape && this._anchorShape.visible && (this.activeStatic(), setTimeout(() => {
        this.deactivateStatic();
      }, Bo));
    }, RA + Bo);
  }
  // The start position of the range
  get startOffset() {
    var s;
    const { startOffset: e } = (s = yr(this._cursorList)) != null ? s : {}, t = this._docSkeleton.getViewModel().getDataModel().getSelfOrHeaderFooterModel(this._segmentId).getBody();
    if (e == null || t == null)
      return e;
    const o = t.dataStream.length - 2;
    return Math.min(o, e);
  }
  // The end position of the range
  get endOffset() {
    var s;
    const { endOffset: e } = (s = yr(this._cursorList)) != null ? s : {}, t = this._docSkeleton.getViewModel().getDataModel().getSelfOrHeaderFooterModel(this._segmentId).getBody();
    if (e == null || t == null)
      return e;
    const o = t.dataStream.length - 2;
    return Math.min(e, o);
  }
  get collapsed() {
    const { startOffset: e, endOffset: t } = this;
    return e != null && e === t;
  }
  get startNodePosition() {
    if (this.anchorNodePosition == null)
      return null;
    if (this.focusNodePosition == null)
      return this.anchorNodePosition;
    const { start: e } = Go(this.anchorNodePosition, this.focusNodePosition);
    return e;
  }
  get endNodePosition() {
    if (this.anchorNodePosition == null)
      return this.focusNodePosition;
    if (this.focusNodePosition == null)
      return null;
    const { end: e } = Go(this.anchorNodePosition, this.focusNodePosition);
    return e;
  }
  get direction() {
    const { collapsed: e, anchorNodePosition: t, focusNodePosition: o } = this;
    return e || t == null || o == null ? xe.NONE : ys(t, o) ? xe.FORWARD : xe.BACKWARD;
  }
  get segmentId() {
    return this._segmentId;
  }
  get segmentPage() {
    return this._segmentPage;
  }
  getAbsolutePosition() {
    const e = this.anchorNodePosition, t = this.focusNodePosition;
    if (this._isEmpty())
      return;
    const o = this._document.getOffsetConfig(), { docsLeft: s, docsTop: r } = o, i = new it(o, this._docSkeleton);
    if (this._isCollapsed()) {
      const { contentBoxPointGroup: l, cursorList: d } = i.getRangePointData(e, e);
      if (this._setCursorList(d), l.length === 0)
        return;
      const h = Mn(l);
      return {
        ...h,
        left: h.left + s,
        top: h.top + r
      };
    }
    const { borderBoxPointGroup: a, cursorList: c } = i.getRangePointData(e, t);
    if (this._setCursorList(c), a.length === 0)
      return;
    const A = Mn(a);
    return {
      ...A,
      left: A.left + s,
      top: A.top + r
    };
  }
  getAnchor() {
    return this._anchorShape;
  }
  activeStatic() {
    var e, t;
    (t = this._anchorShape) == null || t.setProps({
      stroke: ((e = this.style) == null ? void 0 : e.strokeActive) || on(tn.black, 1)
    });
  }
  deactivateStatic() {
    var e, t;
    (t = this._anchorShape) == null || t.setProps({
      stroke: ((e = this.style) == null ? void 0 : e.stroke) || on(tn.black, 0)
    });
  }
  isActive() {
    return this._current === !0;
  }
  activate() {
    this._current = !0;
  }
  deactivate() {
    this._current = !1;
  }
  dispose() {
    var e, t;
    (e = this._rangeShape) == null || e.dispose(), this._rangeShape = null, (t = this._anchorShape) == null || t.dispose(), this._anchorShape = null, this._anchorBlinkTimer && (clearInterval(this._anchorBlinkTimer), this._anchorBlinkTimer = null);
  }
  isIntersection(e) {
    const { startOffset: t, endOffset: o } = this, { startOffset: s, endOffset: r } = e;
    return t == null || o == null || s == null || r == null ? !1 : t <= r && o >= s;
  }
  // render cursor and selection.
  refresh() {
    var d, h;
    const { _document: e, _docSkeleton: t } = this, o = this.anchorNodePosition, s = this.focusNodePosition;
    if ((d = this._anchorShape) == null || d.hide(), (h = this._rangeShape) == null || h.hide(), this._isEmpty())
      return;
    const r = e.getOffsetConfig(), { docsLeft: i, docsTop: a } = r, c = new it(r, t);
    if (this._isCollapsed()) {
      const { contentBoxPointGroup: u, cursorList: g } = c.getRangePointData(o, o);
      if (this._setCursorList(g), u.length > 0) {
        const f = t.findGlyphByPosition(o);
        this._createOrUpdateAnchor(u, i, a, f);
      }
      return;
    }
    const { borderBoxPointGroup: A, cursorList: l } = c.getRangePointData(o, s);
    this._setCursorList(l), A.length > 0 && this._createOrUpdateRange(A, i, a);
  }
  _isEmpty() {
    return this.anchorNodePosition == null && this.focusNodePosition == null;
  }
  _isCollapsed() {
    const e = this.anchorNodePosition, t = this.focusNodePosition;
    if (e != null && t == null)
      return !0;
    if (e == null || t == null)
      return !1;
    const o = Object.keys(Tt);
    for (const s of o) {
      const r = e[s], i = t[s];
      if (r !== i)
        return !1;
    }
    return e.isBack === t.isBack;
  }
  _createOrUpdateRange(e, t, o) {
    var i;
    if (this._rangeShape) {
      this._rangeShape.translate(t, o), this._rangeShape.updatePointGroup(e), this._rangeShape.show();
      return;
    }
    const s = 0.3, r = new Oi(CA + X.generateRandomId(Br), {
      pointsGroup: e,
      fill: ((i = this.style) == null ? void 0 : i.fill) || on(tn.black, s),
      left: t,
      top: o,
      evented: !1,
      debounceParentDirty: !1
    });
    this._rangeShape = r, this._scene.addObject(r, qo);
  }
  _createOrUpdateAnchor(e, t, o, s) {
    var f, p, m;
    const r = Mn(e), { left: i } = r;
    let { top: a, height: c } = r;
    const A = 14;
    c < A && (a -= A - c, c = A);
    const l = 12;
    let d = i + t;
    const h = a + o, u = ((f = s == null ? void 0 : s.ts) == null ? void 0 : f.it) === L.TRUE;
    if (u && (d += c * Math.tan(l * Math.PI / 180) / 2), this._anchorShape) {
      this._anchorShape.transformByState({ left: d, top: h, height: c }), this._anchorShape.show(), u ? this._anchorShape.skew(-12, 0) : this._anchorShape.skew(0, 0);
      return;
    }
    const g = new yn(vA + X.generateRandomId(Br), {
      left: d,
      top: h,
      height: c,
      strokeWidth: ((p = this.style) == null ? void 0 : p.strokeWidth) || 1.5,
      stroke: ((m = this.style) == null ? void 0 : m.strokeActive) || on(tn.black, 1),
      evented: !1
    });
    u && g.skew(-12, 0), this._anchorShape = g, this._scene.addObject(g, qo), this.activeStatic();
  }
  _setCursorList(e) {
    e.length !== 0 && (this._cursorList = e);
  }
}
const bA = "__DocTableRectRange__", xA = 6;
function Mo(n, e, t, o, s, r = sn, i = "", a = -1) {
  const c = e.getOffsetConfig(), l = new Gi(c, t).getNodePositionGroup(o, s);
  return (l != null ? l : []).map((d) => new Yi(
    n,
    e,
    t,
    d.anchor,
    d.focus,
    r,
    i,
    a
  ));
}
class Yi {
  constructor(e, t, o, s, r, i = sn, a = "", c = -1) {
    x(this, "rangeType", Ge.RECT);
    // The rendered rect range
    x(this, "_rangeShape");
    // Identifies whether the range is the current one, most of which is the last range.
    x(this, "_current", !1);
    // Rect Range start row.
    x(this, "_startRow");
    // Rect Range start column.
    x(this, "_startCol");
    // Rect Range end row.
    x(this, "_endRow");
    // Rect Range end column.
    x(this, "_endCol");
    // table id in view model.
    x(this, "_tableId");
    this._scene = e, this._document = t, this._docSkeleton = o, this.anchorNodePosition = s, this.focusNodePosition = r, this.style = i, this._segmentId = a, this._segmentPage = c, this.refresh();
  }
  get startOffset() {
    const { startNodePosition: e } = this;
    return this._docSkeleton.findCharIndexByPosition(e);
  }
  get endOffset() {
    const { endNodePosition: e } = this;
    return this._docSkeleton.findCharIndexByPosition(e);
  }
  get collapsed() {
    return !1;
  }
  get startRow() {
    return this._startRow;
  }
  get startColumn() {
    return this._startCol;
  }
  get endRow() {
    return this._endRow;
  }
  get endColumn() {
    return this._endCol;
  }
  get tableId() {
    return this._tableId;
  }
  get segmentId() {
    return this._segmentId;
  }
  get segmentPage() {
    return this._segmentPage;
  }
  get spanEntireRow() {
    var i;
    const t = (i = this._docSkeleton.getViewModel().getSnapshot().tableSource) == null ? void 0 : i[this._tableId], { _startCol: o, _endCol: s } = this;
    if (t == null)
      throw new Error("Table is not found.");
    const { tableColumns: r } = t;
    return o === 0 && s === r.length - 1;
  }
  get spanEntireColumn() {
    var i;
    const t = (i = this._docSkeleton.getViewModel().getSnapshot().tableSource) == null ? void 0 : i[this._tableId], { _startRow: o, _endRow: s } = this;
    if (t == null)
      throw new Error("Table is not found.");
    const { tableRows: r } = t;
    return o === 0 && s === r.length - 1;
  }
  get spanEntireTable() {
    return this.spanEntireRow && this.spanEntireColumn;
  }
  get startNodePosition() {
    const { anchorNodePosition: e, focusNodePosition: t } = this;
    return yo(e, t) ? e : t;
  }
  get endNodePosition() {
    const { anchorNodePosition: e, focusNodePosition: t } = this;
    return yo(e, t) ? t : e;
  }
  get direction() {
    const { anchorNodePosition: e, focusNodePosition: t } = this;
    return yo(e, t) ? xe.FORWARD : xe.BACKWARD;
  }
  isActive() {
    return this._current === !0;
  }
  activate() {
    this._current = !0;
  }
  deactivate() {
    this._current = !1;
  }
  dispose() {
    var e;
    (e = this._rangeShape) == null || e.dispose(), this._rangeShape = null;
  }
  isIntersection(e) {
    const { startRow: t, startColumn: o, endRow: s, endColumn: r } = this, { startRow: i, startColumn: a, endRow: c, endColumn: A } = e, l = {
      left: o,
      top: t,
      right: r,
      bottom: s
    }, d = {
      left: a,
      top: i,
      right: A,
      bottom: c
    };
    return ka.hasIntersectionBetweenTwoRect(l, d);
  }
  refresh() {
    var p;
    (p = this._rangeShape) == null || p.hide();
    const { startNodePosition: e, endNodePosition: t, _document: o, _docSkeleton: s } = this, r = o.getOffsetConfig(), { docsLeft: i, docsTop: a } = r, A = new Gi(r, s).getRangePointData(e, t);
    if (A == null)
      return;
    const { pointGroup: l = [], startRow: d, endRow: h, startColumn: u, endColumn: g, tableId: f } = A;
    (l == null ? void 0 : l.length) > 0 && this._createOrUpdateRange(l, i, a), this._updateTableInfo(d, h, u, g, f);
  }
  _updateTableInfo(e, t, o, s, r) {
    this._startRow = e, this._endRow = t, this._startCol = o, this._endCol = s, this._tableId = r;
  }
  _createOrUpdateRange(e, t, o) {
    var i;
    if (this._rangeShape) {
      this._rangeShape.translate(t, o), this._rangeShape.updatePointGroup(e), this._rangeShape.show();
      return;
    }
    const s = 0.3, r = new Oi(bA + X.generateRandomId(xA), {
      pointsGroup: e,
      fill: ((i = this.style) == null ? void 0 : i.fill) || on(tn.black, s),
      left: t,
      top: o,
      evented: !1,
      debounceParentDirty: !1
    });
    this._rangeShape = r, this._scene.addObject(r, qo);
  }
}
function Mr(n, e, t, o, s, r, i, a, c = !0, A = !0) {
  const l = s.findNodePositionByCharIndex(n, c, i, a), d = s.findNodePositionByCharIndex(e, A, i, a);
  if (!(l == null || d == null))
    return new Mt(t, o, s, l, d, r, i, a);
}
function OA(n, e, t, o, s, r, i, a) {
  const c = s.findNodePositionByCharIndex(n, !0, i, a), A = s.findNodePositionByCharIndex(e, !0, i, a);
  if (!(c == null || A == null))
    return new Yi(t, o, s, c, A, r, i, a);
}
function TA(n, e, t, o, s, r, i, a) {
  const c = s.findNodePositionByCharIndex(n, !0, i, a), A = s.findNodePositionByCharIndex(e, !0, i, a);
  if (!(c == null || A == null))
    return Ko(
      c,
      A,
      t,
      o,
      s,
      r,
      i,
      a
    );
}
function Ko(n, e, t, o, s, r, i, a) {
  const c = [], A = [], l = [t, o, s, n, e, r, i, a];
  if (zi(s, n, e)) {
    if (Wi(n, e))
      return c.push(new Mt(...l)), {
        textRanges: c,
        rectRanges: A
      };
    {
      const I = Mo(
        ...l
      );
      return A.push(...I), {
        textRanges: c,
        rectRanges: A
      };
    }
  }
  if (SA(n, e)) {
    const I = Mo(
      ...l
    );
    return A.push(...I), {
      textRanges: c,
      rectRanges: A
    };
  }
  const d = s.getViewModel().getSelfOrHeaderFooterViewModel(i), h = s.findCharIndexByPosition(n), u = s.findCharIndexByPosition(e);
  if (h == null || u == null)
    return;
  const g = h <= u ? xe.FORWARD : xe.BACKWARD, f = Math.min(h, u), p = Math.max(h, u);
  let m = f, E = p;
  for (const I of d.getChildren())
    for (const v of I.children) {
      const { startIndex: R, endIndex: S, children: C } = v, T = I.children.indexOf(v), O = I.children[T + 1], P = C[0];
      let b = !1;
      if (P) {
        const { startIndex: B, endIndex: M, children: H } = P;
        let F = null, D = null;
        const te = H.find((V) => V.startIndex <= f && V.endIndex >= f), q = H.find((V) => V.startIndex <= p && V.endIndex >= p);
        if (f > B && f < M)
          F = s.findNodePositionByCharIndex(te.startIndex + 2, !0, i, a), D = s.findNodePositionByCharIndex(M - 4, !0, i, a), m = M + 1;
        else if (p > B && p < M)
          F = s.findNodePositionByCharIndex(B + 3, !0, i, a), D = s.findNodePositionByCharIndex(q.endIndex - 3, !0, i, a), E = B - 1, b = !0;
        else if (B > f && M < p) {
          if (F = s.findNodePositionByCharIndex(B + 3, !0, i, a), D = s.findNodePositionByCharIndex(M - 4, !0, i, a), m <= B - 1) {
            const V = s.findNodePositionByCharIndex(m, !0, i, a), Y = s.findNodePositionByCharIndex(B - 1, !1, i, a), oe = g === xe.FORWARD ? V : Y, ce = g === xe.FORWARD ? Y : V;
            c.push(new Mt(t, o, s, oe, ce, r, i, a));
          }
          m = M + 1;
        }
        if (F && D) {
          const V = g === xe.FORWARD ? F : D, Y = g === xe.FORWARD ? D : F;
          A.push(...Mo(
            t,
            o,
            s,
            V,
            Y,
            r,
            i,
            a
          ));
        }
      }
      if (E === S + 1 && !b && O && O.children.length && (E = S, b = !0), E >= R && E <= S || b) {
        const B = s.findNodePositionByCharIndex(m, !0, i, a), M = s.findNodePositionByCharIndex(E, !b, i, a), H = g === xe.FORWARD ? B : M, F = g === xe.FORWARD ? M : B;
        if (A.length && X.diffValue(H, F))
          continue;
        c.push(new Mt(t, o, s, H, F, r, i, a));
      }
    }
  return {
    textRanges: c,
    rectRanges: A
  };
}
function yA(n) {
  const e = n == null ? void 0 : n.getCanvasElement();
  if (!e)
    return {
      left: 0,
      top: 0
    };
  const { top: t, left: o } = cc(e);
  return {
    left: o,
    top: t
  };
}
function _r(n) {
  var c;
  const e = (c = n.parent) == null ? void 0 : c.parent, t = e == null ? void 0 : e.parent;
  if (e == null || t == null)
    return;
  const { paragraphIndex: o } = e, s = t.lines.filter((A) => A.paragraphIndex === o);
  let r = -1, i = "", a = !1;
  for (const A of s)
    for (const l of A.divides)
      for (const d of l.glyphGroup)
        a || (r += d.count), d === n && (a = !0), i += d.count > 0 ? d.content : "";
  return {
    st: s[0].st,
    ed: o,
    content: i,
    nodeIndex: r
  };
}
function Xo(n) {
  const { startOffset: e, endOffset: t, collapsed: o, rangeType: s, startNodePosition: r, endNodePosition: i, direction: a, segmentId: c, segmentPage: A } = n;
  return {
    startOffset: e,
    endOffset: t,
    collapsed: o,
    rangeType: s,
    startNodePosition: r,
    endNodePosition: i,
    direction: a,
    segmentId: c,
    segmentPage: A,
    isActive: n.isActive()
  };
}
function BA(n) {
  const e = Xo(n), {
    startRow: t,
    startColumn: o,
    endRow: s,
    endColumn: r,
    tableId: i,
    spanEntireRow: a,
    spanEntireColumn: c,
    spanEntireTable: A
  } = n;
  return {
    ...e,
    startRow: t,
    startColumn: o,
    endRow: s,
    endColumn: r,
    tableId: i,
    spanEntireRow: a,
    spanEntireColumn: c,
    spanEntireTable: A
  };
}
var MA = Object.defineProperty, _A = Object.getOwnPropertyDescriptor, PA = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? _A(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && MA(e, t, s), s;
}, Cn = (n, e) => (t, o) => e(t, o, n);
let Se = class extends At {
  constructor(e, t, o, s, r) {
    super();
    x(this, "_onInputBefore$", new Ee());
    x(this, "onInputBefore$", this._onInputBefore$.asObservable());
    x(this, "_onKeydown$", new Ee());
    x(this, "onKeydown$", this._onKeydown$.asObservable());
    x(this, "_onInput$", new Ee());
    x(this, "onInput$", this._onInput$.asObservable());
    x(this, "_onCompositionstart$", new Le(null));
    x(this, "onCompositionstart$", this._onCompositionstart$.asObservable());
    x(this, "_onCompositionupdate$", new Le(null));
    x(this, "onCompositionupdate$", this._onCompositionupdate$.asObservable());
    x(this, "_onCompositionend$", new Le(null));
    x(this, "onCompositionend$", this._onCompositionend$.asObservable());
    x(this, "_onSelectionStart$", new Le(null));
    x(this, "onSelectionStart$", this._onSelectionStart$.asObservable());
    x(this, "onChangeByEvent$", Fi(
      this._onInput$,
      this._onKeydown$.pipe(Qn((e) => e.event.keyCode === j.BACKSPACE)),
      this._onCompositionend$
    ));
    x(this, "_onPaste$", new Ee());
    x(this, "onPaste$", this._onPaste$.asObservable());
    x(this, "_textSelectionInner$", new Le(null));
    x(this, "textSelectionInner$", this._textSelectionInner$.asObservable());
    x(this, "_onFocus$", new Ee());
    x(this, "onFocus$", this._onFocus$.asObservable());
    x(this, "_onBlur$", new Ee());
    x(this, "onBlur$", this._onBlur$.asObservable());
    x(this, "_onPointerDown$", new Ee());
    x(this, "onPointerDown$", this._onPointerDown$.asObservable());
    x(this, "_container");
    x(this, "_inputParent");
    x(this, "_input");
    x(this, "_scrollTimers", []);
    x(this, "_rangeList", []);
    // Use to cache range list in moving.
    x(this, "_rangeListCache", []);
    // Rect range list.
    x(this, "_rectRangeList", []);
    // Use to cache rect range list in moving.
    x(this, "_rectRangeListCache", []);
    x(this, "_anchorNodePosition", null);
    x(this, "_focusNodePosition", null);
    x(this, "_currentSegmentId", "");
    x(this, "_currentSegmentPage", -1);
    x(this, "_selectionStyle", sn);
    x(this, "_onPointerEvent", !1);
    x(this, "_viewPortObserverMap", /* @__PURE__ */ new Map());
    x(this, "_isIMEInputApply", !1);
    x(this, "_scenePointerMoveSubs", []);
    x(this, "_scenePointerUpSubs", []);
    // When the user switches editors, whether to clear the doc ranges.
    x(this, "_reserveRanges", !1);
    this._context = e, this._layoutService = t, this._logService = o, this._univerInstanceService = s, this._docSkeletonManagerService = r, this._initDOM(), this._registerContainer(), this._setSystemHighlightColorToStyle(), this._listenCurrentUnitChange();
  }
  get isOnPointerEvent() {
    return this._onPointerEvent;
  }
  get isFocusing() {
    return this._input === document.activeElement;
  }
  get canFocusing() {
    return this.isFocusing || document.activeElement === document.body || document.activeElement === null;
  }
  _listenCurrentUnitChange() {
    this._univerInstanceService.getCurrentTypeOfUnit$(_.UNIVER_DOC).pipe(st(this.dispose$)).subscribe((e) => {
      if (e == null)
        return;
      e.getUnitId() !== this._context.unitId && !this._reserveRanges && this.removeAllRanges();
    });
  }
  get activeViewPort() {
    return this._context.scene.getViewports()[0];
  }
  setSegment(e) {
    this._currentSegmentId = e;
  }
  getSegment() {
    return this._currentSegmentId;
  }
  setSegmentPage(e) {
    this._currentSegmentPage = e;
  }
  getSegmentPage() {
    return this._currentSegmentPage;
  }
  setReserveRangesStatus(e) {
    this._reserveRanges = e;
  }
  _setRangeStyle(e = sn) {
    this._selectionStyle = e;
  }
  // eslint-disable-next-line max-lines-per-function
  addDocRanges(e, t = !0, o) {
    const {
      _currentSegmentId: s,
      _currentSegmentPage: r,
      _selectionStyle: i
    } = this, { scene: a, mainComponent: c } = this._context, A = c, l = this._docSkeletonManagerService.getSkeleton(), d = (h, u) => {
      const g = TA(
        h,
        u,
        a,
        A,
        l,
        i,
        s,
        r
      );
      if (g == null)
        return;
      const { textRanges: f, rectRanges: p } = g;
      for (const m of f)
        this._addTextRange(m);
      this._addRectRanges(p);
    };
    for (const h of e) {
      const { startOffset: u, endOffset: g, rangeType: f, startNodePosition: p, endNodePosition: m } = h;
      if (f === Ge.RECT) {
        const E = OA(
          u,
          g,
          a,
          A,
          l,
          i,
          s,
          r
        );
        E && this._addRectRanges([E]);
      } else if (f === Ge.TEXT)
        try {
          let E = null;
          p && m ? E = Mr(
            p.isBack ? u : u - 1,
            m.isBack ? g : g - 1,
            a,
            A,
            l,
            i,
            s,
            r,
            p.isBack,
            m.isBack
          ) : E = Mr(
            u,
            g,
            a,
            A,
            l,
            i,
            s,
            r
          ), E && this._addTextRange(E);
        } catch {
          d(u, g);
        }
      else
        d(u, g);
    }
    this._textSelectionInner$.next({
      textRanges: this._getAllTextRanges(),
      rectRanges: this._getAllRectRanges(),
      segmentId: s,
      segmentPage: r,
      style: i,
      isEditing: t,
      options: o
    }), this._updateInputPosition(o == null ? void 0 : o.forceFocus);
  }
  setCursorManually(e, t) {
    const o = this._findNodeByCoord(e, t, {
      strict: !0,
      segmentId: this._currentSegmentId,
      segmentPage: this._currentSegmentPage
    }), s = this._getNodePosition(o);
    if (s == null) {
      this._removeAllRanges();
      return;
    }
    (o == null ? void 0 : o.node.streamType) === U.PARAGRAPH && (s.isBack = !0), this._createTextRangeByAnchorPosition(s), this._textSelectionInner$.next({
      textRanges: this._getAllTextRanges(),
      rectRanges: this._getAllRectRanges(),
      segmentId: this._currentSegmentId,
      segmentPage: this._currentSegmentPage,
      style: this._selectionStyle,
      isEditing: !1
    });
  }
  // Sync canvas selection to dom selection.
  sync() {
    this._updateInputPosition();
  }
  /**
   * @deprecated
   */
  activate(e, t, o = !1) {
    this._container.style.left = `${e}px`, this._container.style.top = `${t}px`, this._container.style.zIndex = "1000", (this.canFocusing || o) && this.focus();
  }
  hasFocus() {
    return document.activeElement === this._input;
  }
  focus() {
    this._input.focus();
  }
  blur() {
    this._input.blur();
  }
  // FIXME: for editor cell editor we don't need to blur the input element
  /**
   * @deprecated
   */
  deactivate() {
    this._container.style.left = "0px", this._container.style.top = "0px";
  }
  // Handler double click.
  __handleDblClick(e) {
    const { offsetX: t, offsetY: o } = e, s = this._findNodeByCoord(t, o, {
      strict: !1,
      segmentId: this._currentSegmentId,
      segmentPage: this._currentSegmentPage
    });
    if (s == null || s.node == null)
      return;
    const r = _r(s.node);
    if (r == null)
      return;
    const { content: i, st: a, nodeIndex: c } = r;
    if (c === -1 || Intl.Segmenter == null)
      return;
    const l = new Intl.Segmenter(void 0, { granularity: "word" }).segment(i);
    let d = Number.NEGATIVE_INFINITY, h = Number.NEGATIVE_INFINITY;
    for (const { segment: u, index: g, isWordLike: f } of l)
      if (g <= c && c < g + u.length && f) {
        d = g + a, h = g + a + u.length;
        break;
      }
    if (Number.isFinite(d) && Number.isFinite(h)) {
      this.removeAllRanges();
      const u = [
        {
          startOffset: d,
          endOffset: h
        }
      ];
      this.addDocRanges(u, !1, { forceFocus: !0 });
    }
  }
  __handleTripleClick(e) {
    const { offsetX: t, offsetY: o } = e, s = this._findNodeByCoord(t, o, {
      strict: !1,
      segmentId: this._currentSegmentId,
      segmentPage: this._currentSegmentPage
    });
    if (s == null || s.node == null)
      return;
    const r = _r(s.node);
    if (r == null)
      return;
    this.removeAllRanges();
    const { st: i, ed: a } = r, c = [
      {
        startOffset: i,
        endOffset: a
      }
    ];
    this.addDocRanges(c, !1, { forceFocus: !0 });
  }
  // Handle pointer down.
  // eslint-disable-next-line max-lines-per-function, complexity
  __onPointDown(e) {
    var f, p;
    const { scene: t, mainComponent: o } = this._context, s = this._docSkeletonManagerService.getSkeleton(), { offsetX: r, offsetY: i } = e, a = this._findNodeByCoord(r, i, {
      strict: !1,
      segmentId: this._currentSegmentId,
      segmentPage: this._currentSegmentPage
    }), c = this._getNodePosition(a);
    if (c == null || a == null) {
      this._removeAllRanges();
      return;
    }
    (a == null ? void 0 : a.node.streamType) === U.PARAGRAPH && (c.isBack = !0);
    const A = this._textSelectionInner$.value;
    if (a && e.button === 2 && A) {
      const m = s.findCharIndexByPosition(c);
      if (typeof m == "number" && A.textRanges.some((E) => E.startOffset <= m && E.endOffset > m) || typeof m == "number" && A.rectRanges.some((E) => E.startOffset <= m && E.endOffset >= m))
        return;
    }
    const { segmentId: l, segmentPage: d } = a;
    l && this._currentSegmentId && l !== this._currentSegmentId && this.setSegment(l), l && d !== this._currentSegmentPage && this.setSegmentPage(d), this._anchorNodePosition = c, e.shiftKey && this._getActiveRangeInstance() ? this._updateActiveRangePosition(c) : e.ctrlKey ? this._removeAllCollapsedTextRanges() : this._isEmpty() || this._removeAllRanges(), t.disableObjectsEvent();
    const h = Ac.create(t);
    this._scrollTimers.push(h), h.startScroll(r, i), this._onSelectionStart$.next((f = this._getActiveRangeInstance()) == null ? void 0 : f.startNodePosition), (p = t.getTransformer()) == null || p.clearSelectedObjects();
    let u = r, g = i;
    this._onPointerEvent = !0, this._scenePointerMoveSubs.push(t.onPointerMove$.subscribeEvent((m) => {
      const { offsetX: E, offsetY: I } = m;
      t.setCursor(mt.TEXT), !(Math.sqrt((E - u) ** 2 + (I - g) ** 2) < 3) && (this._moving(E, I), h.scrolling(E, I, () => {
        this._moving(E, I);
      }), u = E, g = I);
    })), this._scenePointerUpSubs.push(t.onPointerUp$.subscribeEvent(() => {
      if ([...this._scenePointerMoveSubs, ...this._scenePointerUpSubs].forEach((E) => {
        E.unsubscribe();
      }), this._onPointerEvent = !1, t.enableObjectsEvent(), this._anchorNodePosition && !this._focusNodePosition) {
        if (e.ctrlKey) {
          this._disposeScrollTimers();
          return;
        }
        const E = new Mt(t, o, s, this._anchorNodePosition, void 0, this._selectionStyle, this._currentSegmentId, this._currentSegmentPage);
        this._addTextRange(E);
      } else if (this._anchorNodePosition && this._focusNodePosition) {
        for (const E of this._rangeListCache)
          e.ctrlKey ? E.collapsed ? E.dispose() : this._addTextRange(E) : this._addTextRange(E);
        this._addRectRanges(this._rectRangeListCache), this._rangeListCache = [], this._rectRangeListCache = [];
      }
      this._anchorNodePosition = null, this._focusNodePosition = null;
      const m = {
        textRanges: this._getAllTextRanges(),
        rectRanges: this._getAllRectRanges(),
        segmentId: this._currentSegmentId,
        segmentPage: this._currentSegmentPage,
        style: this._selectionStyle,
        isEditing: !1
      };
      this._textSelectionInner$.next(m), this._disposeScrollTimers(), this._updateInputPosition(!0);
    }));
  }
  removeAllRanges() {
    this._removeAllRanges(), this.deactivate();
  }
  getActiveTextRange() {
    return this._getActiveRangeInstance();
  }
  _disposeScrollTimers() {
    this._scrollTimers.forEach((e) => {
      e == null || e.dispose();
    }), this._scrollTimers = [];
  }
  _setSystemHighlightColorToStyle() {
    const { r: e, g: t, b: o, a: s } = lc(), r = {
      strokeWidth: 1.5,
      stroke: "rgba(0, 0, 0, 0)",
      strokeActive: "rgba(0, 0, 0, 1)",
      fill: `rgba(${e}, ${t}, ${o}, ${s != null ? s : 0.3})`
    };
    this._setRangeStyle(r);
  }
  _getAllTextRanges() {
    return this._rangeList.map(Xo);
  }
  _getAllRectRanges() {
    return this._rectRangeList.map(BA);
  }
  getAllTextRanges() {
    return this._getAllTextRanges();
  }
  getAllRectRanges() {
    return this._getAllRectRanges();
  }
  _getActiveRange() {
    const e = this._rangeList.find((s) => s.isActive());
    if (e == null)
      return null;
    const { startOffset: t, endOffset: o } = e;
    return t == null || o == null ? null : Xo(e);
  }
  _getActiveRangeInstance() {
    return this._rangeList.find((e) => e.isActive());
  }
  dispose() {
    super.dispose(), this._detachEvent(), this._removeAllRanges(), this._container.remove();
  }
  _initDOM() {
    const { unitId: e } = this._context, t = document.createElement("div");
    t.style.position = "fixed", t.style.left = "0px", t.style.top = "0px", t.id = `univer-doc-selection-container-${e}`;
    const o = document.createElement("div"), s = document.createElement("div");
    o.appendChild(s), t.appendChild(o), this._container = t, this._inputParent = o, this._input = s, this._initInput(), this._initInputEvents(), document.body.appendChild(t);
  }
  _registerContainer() {
    this.disposeWithMe(
      // the content editable div should be regarded as part of the applications container
      this._layoutService.registerContainerElement(this._container)
    );
  }
  _initInput() {
    this._inputParent.style.cssText = `
            position:absolute;
            height:1px;
            width:1px;
            overflow: hidden;
        `, this._input.contentEditable = "true", this._input.classList.add("univer-editor"), this._input.id = `__editor_${this._context.unitId}`, this._input.style.cssText = `
            position: absolute;
            overflow: hidden;
            opacity: 1;
            background: #000;
            color: transparent;
            outline: none;
            z-index: -2;
            caret-color: transparent;
            white-space: pre-wrap;
            user-select: text;
        `;
  }
  _getNodePosition(e) {
    if (e == null)
      return;
    const { node: t, ratioX: o, segmentPage: s } = e, i = this._docSkeletonManagerService.getSkeleton().findPositionByGlyph(t, s);
    if (i == null)
      return;
    let c = o < 0.5;
    return t.glyphType === xi.LIST && (c = !0), {
      ...i,
      isBack: c
    };
  }
  _interactTextRanges(e) {
    const t = [];
    for (const o of this._rangeList) {
      if (e.some((s) => s.isIntersection(o))) {
        o.dispose();
        continue;
      }
      t.push(o);
    }
    this._rangeList = t;
  }
  _interactRectRanges(e) {
    const t = [];
    for (const o of this._rectRangeList) {
      if (e.some((s) => s.isIntersection(o))) {
        o.dispose();
        continue;
      }
      t.push(o);
    }
    this._rectRangeList = t;
  }
  _removeAllRanges() {
    this._removeAllTextRanges(), this._removeAllRectRanges();
  }
  _removeAllCacheRanges() {
    this._rangeListCache.forEach((e) => {
      e.dispose();
    }), this._rectRangeListCache.forEach((e) => {
      e.dispose();
    }), this._rangeListCache = [], this._rectRangeListCache = [];
  }
  _removeAllTextRanges() {
    this._rangeList.forEach((e) => {
      e.dispose();
    }), this._rangeList = [];
  }
  _removeAllRectRanges() {
    this._rectRangeList.forEach((e) => {
      e.dispose();
    }), this._rectRangeList = [];
  }
  _removeAllCollapsedTextRanges() {
    for (const e of this._rangeList)
      e.collapsed && e.dispose();
  }
  _deactivateAllTextRanges() {
    this._rangeList.forEach((e) => {
      e.deactivate();
    });
  }
  _deactivateAllRectRanges() {
    this._rectRangeList.forEach((e) => {
      e.deactivate();
    });
  }
  _addTextRangesToCache(e) {
    this._rangeListCache.push(...e);
  }
  _addTextRange(e) {
    this._deactivateAllTextRanges(), e.activate(), this._rangeList.push(e);
  }
  _addRectRangesToCache(e) {
    this._rectRangeListCache.push(...e);
  }
  _addRectRanges(e) {
    e.length !== 0 && (this._deactivateAllRectRanges(), e[e.length - 1].activate(), this._rectRangeList.push(...e));
  }
  _createTextRangeByAnchorPosition(e) {
    this._removeAllRanges();
    const { scene: t, mainComponent: o } = this._context, s = this._docSkeletonManagerService.getSkeleton(), r = new Mt(t, o, s, e, void 0, this._selectionStyle, this._currentSegmentId, this._currentSegmentPage);
    this._addTextRange(r);
  }
  _updateActiveRangePosition(e) {
    const t = this._getActiveRangeInstance();
    if (t == null || t.anchorNodePosition == null) {
      this._logService.error(
        "[DocSelectionRenderService] _updateActiveRangeFocusPosition: active range has no anchor"
      );
      return;
    }
    this._removeAllRanges(), this._anchorNodePosition = t.anchorNodePosition, this._focusNodePosition = e;
    const { scene: o, mainComponent: s } = this._context, r = this._docSkeletonManagerService.getSkeleton(), { _anchorNodePosition: i, _focusNodePosition: a, _selectionStyle: c, _currentSegmentId: A, _currentSegmentPage: l } = this;
    if (i == null || a == null || s == null)
      return;
    const d = Ko(
      i,
      a,
      o,
      s,
      r,
      c,
      A,
      l
    );
    if (d == null)
      return;
    const { textRanges: h, rectRanges: u } = d;
    this._addTextRangesToCache(h), this._addRectRangesToCache(u), this.deactivate();
  }
  _isEmpty() {
    return this._rangeList.length === 0 && this._rectRangeList.length === 0;
  }
  _getCanvasOffset() {
    var t;
    const e = (t = this._context.scene) == null ? void 0 : t.getEngine();
    return yA(e);
  }
  _updateInputPosition(e = !1) {
    const t = this._getActiveRangeInstance(), o = t == null ? void 0 : t.getAnchor();
    if (!o || o && !o.visible || this.activeViewPort == null) {
      this.focus();
      return;
    }
    const { left: s, top: r } = o, i = this.activeViewPort.getAbsoluteVector(rn.FromArray([s, r])), { x: a, y: c } = i;
    let { left: A, top: l } = this._getCanvasOffset();
    A += a, l += c, this.activate(A, l, e);
  }
  _moving(e, t) {
    var m, E;
    const { _currentSegmentId: o, _currentSegmentPage: s } = this, r = this._findNodeByCoord(e, t, {
      strict: !0,
      segmentId: o,
      segmentPage: s
    }), i = this._getNodePosition(r);
    if (i == null || r == null)
      return;
    const a = r == null ? void 0 : r.node.parent, c = a == null ? void 0 : a.glyphGroup[a.glyphGroup.indexOf(r.node) + 1];
    (r == null ? void 0 : r.node.streamType) === U.PARAGRAPH && (c == null ? void 0 : c.streamType) === U.SECTION_BREAK && (i.isBack = !0), this._focusNodePosition = i, this._removeAllCacheRanges();
    const { _anchorNodePosition: A, _selectionStyle: l } = this, { scene: d, mainComponent: h } = this._context, u = this._docSkeletonManagerService.getSkeleton();
    if (A == null || h == null)
      return;
    const g = Ko(
      A,
      i,
      d,
      h,
      u,
      l,
      o,
      s
    );
    if (g == null)
      return;
    const { textRanges: f, rectRanges: p } = g;
    this._rangeList.length > 0 && f.length > 0 && this._interactTextRanges(f), this._rectRangeList.length > 0 && p.length > 0 && this._interactRectRanges(p), this._addTextRangesToCache(f), this._addRectRangesToCache(p), this.deactivate(), (E = (m = this._context.scene) == null ? void 0 : m.getEngine()) == null || E.setCapture();
  }
  __attachScrollEvent() {
    const e = this.activeViewPort;
    if (!e)
      return;
    const { unitId: t } = this._context;
    if (this._viewPortObserverMap.has(t))
      return;
    const o = e.onScrollAfter$.subscribeEvent((r) => {
      if (!r.viewport)
        return;
      const a = this._getActiveRangeInstance();
      a == null || a.activeStatic();
    }), s = e.onScrollEnd$.subscribeEvent((r) => {
      const i = r.viewport;
      if (!i)
        return;
      const a = i.getBounding(), c = this._getActiveRangeInstance(), A = c == null ? void 0 : c.getAnchor();
      if (!(!A || A && !A.visible)) {
        if (a) {
          const { left: l, top: d, right: h, bottom: u } = a.viewBound;
          if (A.left < l || A.left > h || A.top < d || A.top > u) {
            c == null || c.deactivateStatic();
            return;
          }
        }
        this._updateInputPosition();
      }
    });
    this._viewPortObserverMap.set(t, {
      scrollBefore: o,
      scrollStop: s
    });
  }
  // FIXME: listeners here are not correctly disposed
  // eslint-disable-next-line max-lines-per-function
  _initInputEvents() {
    this.disposeWithMe(
      Ue(this._input, "keydown").subscribe((e) => {
        this._isIMEInputApply || this._eventHandle(e, (t) => {
          this._onKeydown$.next(t);
        });
      })
    ), this.disposeWithMe(
      Ue(this._input, "input").subscribe((e) => {
        if (!(e.inputType === "historyUndo" || e.inputType === "historyRedo")) {
          if (this._rectRangeList.length > 0)
            return e.stopPropagation(), e.preventDefault();
          this._isIMEInputApply || this._eventHandle(e, (t) => {
            this._onInputBefore$.next(t), this._onInput$.next(t);
          });
        }
      })
    ), this.disposeWithMe(
      Ue(this._input, "compositionstart").subscribe((e) => {
        if (this._rectRangeList.length > 0)
          return e.stopPropagation(), e.preventDefault();
        this._isIMEInputApply = !0, this._eventHandle(e, (t) => {
          this._onCompositionstart$.next(t);
        });
      })
    ), this.disposeWithMe(
      Ue(this._input, "compositionend").subscribe((e) => {
        this._isIMEInputApply = !1, this._eventHandle(e, (t) => {
          this._onCompositionend$.next(t);
        });
      })
    ), this.disposeWithMe(
      Ue(this._input, "compositionupdate").subscribe((e) => {
        this._eventHandle(e, (t) => {
          this._onInputBefore$.next(t), this._onCompositionupdate$.next(t);
        });
      })
    ), this.disposeWithMe(
      Ue(this._input, "paste").subscribe((e) => {
        this._eventHandle(e, (t) => {
          this._onPaste$.next(t);
        });
      })
    ), this.disposeWithMe(
      Ue(this._input, "focus").subscribe((e) => {
        this._eventHandle(e, (t) => {
          this._onFocus$.next(t);
        });
      })
    ), this.disposeWithMe(
      Ue(this._input, "blur").subscribe((e) => {
        this._eventHandle(e, (t) => {
          this._onBlur$.next(t);
        });
      })
    );
  }
  _eventHandle(e, t) {
    const o = this._input.textContent || "";
    this._input.innerHTML = "";
    const s = this._getActiveRange(), r = this._getAllTextRanges();
    t({
      event: e,
      content: o,
      activeRange: s,
      rangeList: r
    });
  }
  _getTransformCoordForDocumentOffset(e, t) {
    const o = this._context.mainComponent, { documentTransform: s } = o.getOffsetConfig();
    if (this.activeViewPort == null || s == null)
      return;
    const r = this.activeViewPort.transformVector2SceneCoord(rn.FromArray([e, t]));
    if (r)
      return s.clone().invert().applyPoint(r);
  }
  _findNodeByCoord(e, t, o) {
    const s = this._getTransformCoordForDocumentOffset(e, t);
    if (s == null)
      return;
    const r = this._context.mainComponent, i = this._docSkeletonManagerService.getSkeleton(), {
      pageLayoutType: a = an.VERTICAL,
      pageMarginLeft: c,
      pageMarginTop: A
    } = r.getOffsetConfig();
    return i.findNodeByCoord(
      s,
      a,
      c,
      A,
      o
    );
  }
  _detachEvent() {
    this._onInputBefore$.complete(), this._onKeydown$.complete(), this._onInput$.complete(), this._onCompositionstart$.complete(), this._onCompositionupdate$.complete(), this._onCompositionend$.complete(), this._onSelectionStart$.complete(), this._textSelectionInner$.complete(), this._onPaste$.complete(), this._onFocus$.complete(), this._onBlur$.complete(), this._onPointerDown$.complete();
  }
};
Se = PA([
  Cn(1, bs),
  Cn(2, fs),
  Cn(3, Q),
  Cn(4, z(ie))
], Se);
class DA extends ue {
  constructor(t, o, s, r, i) {
    super();
    // Emit change event when editor lose focus.
    x(this, "_change$", new Ee());
    x(this, "change$", this._change$.asObservable());
    // The input event fires when the value of a editor has been changed as a direct result of a user action.
    x(this, "_input$", new Ee());
    x(this, "input$", this._input$.asObservable());
    // paste event.
    x(this, "_paste$", new Ee());
    x(this, "paste$", this._paste$.asObservable());
    // Editor get focus.
    x(this, "_focus$", new Ee());
    x(this, "focus$", this._focus$.asObservable());
    // Editor lose focus.
    x(this, "_blur$", new Ee());
    x(this, "blur$", this._blur$.asObservable());
    // Emit when doc selection changed.
    x(this, "_selectionChange$", new Ee());
    x(this, "selectionChange$", this._selectionChange$.asObservable());
    this._param = t, this._univerInstanceService = o, this._docSelectionManagerService = s, this._commandService = r, this._undoRedoService = i, this._listenSelection();
  }
  get docSelectionRenderService() {
    return this._param.render.with(Se);
  }
  _listenSelection() {
    const t = this._param.render.with(Se);
    this.disposeWithMe(
      t.onBlur$.subscribe((o) => {
        this._blur$.next(o);
        const s = this.getDocumentData();
        this._change$.next({
          target: this,
          data: s
        });
      })
    ), this.disposeWithMe(
      t.onFocus$.subscribe((o) => {
        this._focus$.next(o);
      })
    ), this.disposeWithMe(
      t.onPaste$.subscribe((o) => {
        this._paste$.next(o);
      })
    ), this.disposeWithMe(
      Fi(
        t.onInput$,
        t.onKeydown$.pipe(zo((o) => {
          const s = o.event;
          return s.ctrlKey || s.metaKey ? [j.X, j.V].includes(s.keyCode) : [j.BACKSPACE].includes(s.keyCode);
        })),
        t.onCompositionupdate$,
        t.onCompositionend$,
        t.onPaste$
      ).subscribe((o) => {
        if (o == null)
          return;
        const { content: s = "" } = o, r = this.getDocumentData();
        this._input$.next({
          target: this,
          content: s,
          data: r,
          isComposing: o.event.type === "compositionupdate"
        });
      })
    ), this.disposeWithMe(
      this._docSelectionManagerService.textSelection$.subscribe((o) => {
        if (o == null)
          return;
        const { unitId: s, subUnitId: r, ...i } = o, a = this.getEditorId();
        s === a && this._selectionChange$.next(i);
      })
    );
  }
  isFocus() {
    const t = this._param.render.with(Se);
    return t.isFocusing && !!t.getActiveTextRange();
  }
  /**
   * @deprecated use `IEditorService.focus` as instead. this is for internal usage.
   */
  focus() {
    const t = this._univerInstanceService.getCurrentUnitForType(_.UNIVER_DOC), o = this.getEditorId();
    (t == null || t.getUnitId() !== o) && this._univerInstanceService.setCurrentUnitForType(o), this._param.render.with(Se).focus();
  }
  /**
   * @deprecated use `IEditorService.blur` as instead. this is for internal usage.
   */
  blur() {
    this._param.render.with(Se).blur();
  }
  // Selects the entire content of the editor.
  // Calling editor.select() will not necessarily focus the editor, so it is often used with Editor.focus
  select() {
    const t = this.getDocumentData();
    return this.setSelectionRanges([{
      startOffset: 0,
      endOffset: t.body ? t.body.dataStream.length - 2 : 0
    }]);
  }
  // Selects the specified range of characters within editor.
  setSelectionRanges(t) {
    const o = this.getEditorId(), s = {
      unitId: o,
      subUnitId: o
    };
    return this._docSelectionManagerService.replaceDocRanges(t, s, !1);
  }
  // Get current doc ranges. include text range and rect range.
  getSelectionRanges() {
    const t = this.getEditorId(), o = {
      unitId: t,
      subUnitId: t
    };
    return this._docSelectionManagerService.getDocRanges(o);
  }
  getCursorPosition() {
    var o, s;
    return (s = (o = this.getSelectionRanges().find((r) => r.collapsed)) == null ? void 0 : o.startOffset) != null ? s : -1;
  }
  // get editor id.
  getEditorId() {
    return this._getEditorId();
  }
  // get document data.
  getDocumentData() {
    return this._getDocDataModel().getSnapshot();
  }
  getDocumentDataModel() {
    return this._getDocDataModel();
  }
  // Set the new document data.
  setDocumentData(t, o) {
    const { id: s } = t;
    this._commandService.syncExecuteCommand(Vi.id, {
      unitId: s,
      snapshot: t,
      textRanges: o
    });
  }
  replaceText(t, o = !0) {
    const s = this.getDocumentData();
    this.setDocumentData(
      {
        ...s,
        body: {
          dataStream: `${t}\r
`,
          paragraphs: [{
            startIndex: 0
          }],
          customRanges: [],
          sectionBreaks: [],
          tables: [],
          textRuns: []
        }
      },
      o ? [{
        startOffset: t.length,
        endOffset: t.length,
        collapsed: !0
      }] : null
    );
  }
  // Clear the undo redo history of this editor.
  clearUndoRedoHistory() {
    const t = this.getEditorId();
    return this._undoRedoService.clearUndoRedo(t);
  }
  dispose() {
    this._getDocDataModel().dispose();
  }
  /**
   * @deprecated use getEditorId.
   */
  get editorUnitId() {
    return this._param.editorUnitId;
  }
  /**
   * @deprecated @TODO: @JOCS remove this in the future.
   */
  get params() {
    return this._param;
  }
  get cancelDefaultResizeListener() {
    return this._param.cancelDefaultResizeListener;
  }
  get render() {
    return this._param.render;
  }
  isReadOnly() {
    return this._param.readonly === !0;
  }
  getBoundingClientRect() {
    return this._param.editorDom.getBoundingClientRect();
  }
  get editorDOM() {
    return this._param.editorDom;
  }
  isVisible() {
    return this._param.visible;
  }
  isSheetEditor() {
    return to(this._getEditorId());
  }
  /**
   * @deprecated use getDocumentData.
   */
  getValue() {
    var s;
    return (((s = this._getDocDataModel().getBody()) == null ? void 0 : s.dataStream) || "").replace(/\r\n/g, "").replace(/\n/g, "").replace(/\n/g, "");
  }
  /**
   * @deprecated use getDocumentData.
   */
  getBody() {
    return this._getDocDataModel().getBody();
  }
  /**
   * @deprecated.
   */
  update(t) {
    this._param = {
      ...this._param,
      ...t
    };
  }
  /**
   * @deprecated.
   */
  updateCanvasStyle() {
    var s;
    const t = this._getDocDataModel();
    if (t == null)
      return;
    const o = {};
    (s = this._param.canvasStyle) != null && s.fontSize && (o.textStyle == null && (o.textStyle = {}), o.textStyle.fs = this._param.canvasStyle.fontSize), t.updateDocumentStyle(o);
  }
  _getDocDataModel() {
    const t = this._getEditorId();
    return this._univerInstanceService.getUnit(t, _.UNIVER_DOC);
  }
  _getEditorId() {
    var t;
    return ((t = this._param.initialSnapshot) == null ? void 0 : t.id) || this._param.editorUnitId || "";
  }
}
var wA = Object.defineProperty, NA = Object.getOwnPropertyDescriptor, QA = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? NA(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && wA(e, t, s), s;
}, Rt = (n, e) => (t, o) => e(t, o, n);
const UA = [
  "univer-editor",
  "univer-range-selector",
  "univer-range-selector-editor",
  "univer-render-canvas",
  "univer-text-editor-container-placeholder"
];
let Jo = class extends ue {
  constructor(e, t, o, s, r, i) {
    super();
    x(this, "_editors", /* @__PURE__ */ new Map());
    x(this, "_focusEditorUnitId");
    x(this, "_blur$", new Ee());
    x(this, "blur$", this._blur$.asObservable());
    x(this, "_focus$", new Ee());
    x(this, "focus$", this._focus$.asObservable());
    this._univerInstanceService = e, this._renderManagerService = t, this._docSelectionManagerService = o, this._contextService = s, this._commandService = r, this._undoRedoService = i, this._initUniverFocusListener();
  }
  // REFACTOR: @Gggpound The specific business processing should not be placed here,
  // I moved from the layout service. https://github.com/dream-num/univer-pro/issues/1708
  _initUniverFocusListener() {
    this.disposeWithMe(
      Ue(window, "focusin").subscribe((e) => {
        const t = e.target;
        this._blurSheetEditor(t);
      })
    );
  }
  _blurSheetEditor(e) {
    if (UA.some((o) => e.classList.contains(o)))
      return;
    const t = this.getFocusEditor();
    t && t.isSheetEditor() !== !0 && this.blur();
  }
  _setFocusId(e) {
    this._focusEditorUnitId = e;
  }
  getFocusId() {
    return this._focusEditorUnitId;
  }
  getFocusEditor() {
    if (this._focusEditorUnitId)
      return this.getEditor(this._focusEditorUnitId);
  }
  isEditor(e) {
    return this._editors.has(e);
  }
  isSheetEditor(e) {
    const t = this._editors.get(e);
    return !!(t && t.isSheetEditor());
  }
  blur() {
    this._setFocusId(null), this._contextService.setContextValue(wn, !1), this._contextService.setContextValue(lr, !1);
    const e = this.getFocusEditor();
    e == null || e.blur(), this._blur$.next(null);
  }
  focus(e) {
    if (this._focusEditorUnitId && this.blur(), e == null)
      return;
    const t = this.getEditor(e);
    if (t == null)
      return;
    this._univerInstanceService.setCurrentUnitForType(e);
    const o = t.getValue().length;
    this._contextService.setContextValue(wn, !0), to(e) || this._contextService.setContextValue(lr, !0), t.focus(), this._setFocusId(e), this._focus$.next({
      startOffset: o,
      endOffset: o
    });
  }
  dispose() {
    this._editors.clear(), super.dispose();
  }
  getEditor(e = this._getCurrentEditorUnitId()) {
    return this._editors.get(e);
  }
  getAllEditor() {
    return this._editors;
  }
  register(e, t) {
    var c, A, l, d;
    const { initialSnapshot: o, canvasStyle: s = {} } = e, r = o.id;
    this._univerInstanceService.getUnit(r, _.UNIVER_DOC) == null && this._univerInstanceService.createUnit(
      _.UNIVER_DOC,
      o || this._getBlank(r),
      { makeCurrent: !1 }
    );
    let a = this._renderManagerService.getRenderById(r);
    if (a == null && (this._renderManagerService.create(r), a = this._renderManagerService.getRenderById(r)), a) {
      a.engine.setContainer(t);
      const h = new DA(
        { ...e, render: a, editorDom: t, canvasStyle: s },
        this._univerInstanceService,
        this._docSelectionManagerService,
        this._commandService,
        this._undoRedoService
      );
      this._editors.set(r, h), e.scrollBar || (d = (l = (A = (c = a.mainComponent) == null ? void 0 : c.getScene()) == null ? void 0 : A.getViewports()) == null ? void 0 : l[0].getScrollBar()) == null || d.dispose();
    }
    return Zn(() => {
      this._unRegister(r);
    });
  }
  _unRegister(e) {
    const t = this._editors.get(e);
    t != null && (this._renderManagerService.removeRender(e), t.dispose(), this._editors.delete(e), this._univerInstanceService.disposeUnit(e));
  }
  _getCurrentEditorUnitId() {
    return this._univerInstanceService.getCurrentUniverDocInstance().getUnitId();
  }
  _getBlank(e) {
    return {
      id: e,
      body: {
        dataStream: `${pi}`,
        textRuns: [],
        paragraphs: [
          {
            startIndex: 0
          }
        ]
      },
      documentStyle: {
        renderConfig: {
          verticalAlign: Va.TOP,
          horizontalAlign: _e.LEFT
        },
        marginLeft: 3,
        marginTop: 0,
        marginRight: 3
      }
    };
  }
};
Jo = QA([
  Rt(0, Q),
  Rt(1, fe),
  Rt(2, z(G)),
  Rt(3, ms),
  Rt(4, y),
  Rt(5, eo)
], Jo);
const He = ps("univer.editor.service");
function LA(n) {
  const { editorId: e, initialValue: t, container: o, autoFocus: s, isSingle: r } = n, i = Fe(() => s != null ? s : !1, []), [a, c] = ve(), A = $(He);
  return kc(() => {
    var l, d;
    if (o.current) {
      const h = {
        body: {
          dataStream: `\r
`,
          textRuns: [],
          customBlocks: [],
          customDecorations: [],
          customRanges: [],
          paragraphs: [{
            startIndex: 0
          }]
        },
        ...t,
        documentStyle: {
          ...t == null ? void 0 : t.documentStyle,
          pageSize: {
            width: r ? 1 / 0 : o.current.clientWidth,
            height: 1 / 0
          }
        },
        id: e
      }, u = A.register(
        {
          autofocus: !0,
          editorUnitId: e,
          initialSnapshot: h
        },
        o.current
      ), g = A.getEditor(e);
      if (c(g), i) {
        g.focus();
        const f = ((d = (l = h.body) == null ? void 0 : l.dataStream.length) != null ? d : 2) - 2;
        g.setSelectionRanges([{ startOffset: f, endOffset: f }]);
      }
      return () => {
        u == null || u.dispose();
      };
    }
  }, []), a;
}
const at = {
  id: "doc.operation.move-cursor",
  type: N.OPERATION,
  handler: (n, e) => !!e
}, ct = {
  id: "doc.operation.move-selection",
  type: N.OPERATION,
  handler: (n, e) => !!e
}, FA = (n, e, t, o) => {
  const s = $(y), r = $(ro), i = cn(e);
  i.current = e;
  const a = cn(o);
  a.current = o, Re(() => {
    if (!t || !n)
      return;
    const A = `sheet.formula-embedding-editor.${t.getEditorId()}`, l = new Dn(), d = (u, g) => {
      if (a.current) {
        a.current(u, g);
        return;
      }
      let f = se.LEFT;
      u === j.ARROW_DOWN ? f = se.DOWN : u === j.ARROW_UP ? f = se.UP : u === j.ARROW_RIGHT && (f = se.RIGHT), g === K.SHIFT ? s.executeCommand(ct.id, {
        direction: f
      }) : s.executeCommand(at.id, {
        direction: f
      });
    };
    return l.add(s.registerCommand({
      id: A,
      type: N.OPERATION,
      handler(u, g) {
        const { keyCode: f } = g;
        d(f);
      }
    })), [
      { keyCode: j.ARROW_DOWN },
      { keyCode: j.ARROW_LEFT },
      { keyCode: j.ARROW_RIGHT },
      { keyCode: j.ARROW_UP },
      { keyCode: j.ARROW_DOWN, metaKey: K.SHIFT },
      { keyCode: j.ARROW_LEFT, metaKey: K.SHIFT },
      { keyCode: j.ARROW_RIGHT, metaKey: K.SHIFT },
      { keyCode: j.ARROW_UP, metaKey: K.SHIFT },
      { keyCode: j.ARROW_DOWN, metaKey: K.CTRL_COMMAND },
      { keyCode: j.ARROW_LEFT, metaKey: K.CTRL_COMMAND },
      { keyCode: j.ARROW_RIGHT, metaKey: K.CTRL_COMMAND },
      { keyCode: j.ARROW_UP, metaKey: K.CTRL_COMMAND },
      { keyCode: j.ARROW_DOWN, metaKey: K.CTRL_COMMAND | K.SHIFT },
      { keyCode: j.ARROW_LEFT, metaKey: K.CTRL_COMMAND | K.SHIFT },
      { keyCode: j.ARROW_RIGHT, metaKey: K.CTRL_COMMAND | K.SHIFT },
      { keyCode: j.ARROW_UP, metaKey: K.CTRL_COMMAND | K.SHIFT }
    ].map(({ keyCode: u, metaKey: g }) => ({
      id: A,
      binding: g ? u | g : u,
      preconditions: () => !0,
      priority: 900,
      staticParameters: {
        eventType: Ri.Keyboard,
        keyCode: u
      }
    })).forEach((u) => {
      l.add(r.registerShortcut(u));
    }), () => {
      l.dispose();
    };
  }, [s, t, n, r]);
};
function HA(n, e) {
  const t = $(y);
  Re(() => {
    if (!n) return;
    const o = t.onCommandExecuted((s) => {
      if (s.id === J.id) {
        if (s.params.unitId !== n.getEditorId()) return;
        e(n.getDocumentData());
      }
    });
    return () => {
      o.dispose();
    };
  }, [n, e, t]);
}
const kA = "univer-rich-text-editor-active", VA = "univer-rich-text-editor-wrap", jA = "univer-rich-text-editor-text", WA = "univer-rich-text-editor-error-wrap", zA = "univer-rich-text-editor-placeholder", Xt = {
  richTextEditorActive: kA,
  richTextEditorWrap: VA,
  richTextEditorText: jA,
  richTextEditorErrorWrap: WA,
  richTextEditorPlaceholder: zA
}, cf = It((n, e) => {
  var te;
  const {
    className: t,
    autoFocus: o,
    onFocusChange: s,
    initialValue: r,
    onClickOutside: i,
    keyboardEventConfig: a,
    moveCursor: c = !0,
    style: A,
    isSingle: l,
    editorId: d,
    onHeightChange: h,
    onChange: u,
    defaultHeight: g = 32,
    maxHeight: f = 32
  } = n, p = $(He), m = xo(s), E = xo(i), [I, v] = ve(g), R = Wo.useRef(null), S = Fe(() => d != null ? d : ja(`RICH_TEXT_EDITOR-${pt(4)}`), [d]), C = LA({
    editorId: S,
    initialValue: r,
    container: R,
    autoFocus: o,
    isSingle: l
  }), O = $(fe).getRenderById(S), P = O == null ? void 0 : O.with(Se), b = (te = P == null ? void 0 : P.isFocusing) != null ? te : !1, B = Wo.useRef(null), [M, H] = ve(() => {
    var q, V;
    return !Ce.transform.getPlainText((V = (q = C == null ? void 0 : C.getDocumentData().body) == null ? void 0 : q.dataStream) != null ? V : "");
  }), { checkScrollBar: F } = dA(C, l, !0, !0), D = xo((q) => {
    const V = O == null ? void 0 : O.with(ie), Y = V == null ? void 0 : V.getSkeleton().getActualSize();
    Y && (h == null || h(Y.actualHeight), v(Math.max(g, Math.min(Y.actualHeight + 10, f)))), u == null || u(q), F();
  });
  return Re(() => {
    var V, Y;
    H(!Ce.transform.getPlainText((Y = (V = C == null ? void 0 : C.getDocumentData().body) == null ? void 0 : V.dataStream) != null ? Y : ""));
    const q = C == null ? void 0 : C.selectionChange$.subscribe(() => {
      var oe, ce;
      H(!Ce.transform.getPlainText((ce = (oe = C == null ? void 0 : C.getDocumentData().body) == null ? void 0 : oe.dataStream) != null ? ce : ""));
    });
    return () => q == null ? void 0 : q.unsubscribe();
  }, [C]), Nn(C == null ? void 0 : C.blur$), Nn(C == null ? void 0 : C.focus$), Re(() => {
    m == null || m(b);
  }, [b, m]), Re(() => {
    const q = (V) => {
      var oe, ce;
      p.getFocusId() !== S || ((ce = (oe = V.target) == null ? void 0 : oe.dataset) == null ? void 0 : ce.editorid) === S || B.current && !B.current.contains(V.target) && (E == null || E());
    };
    return setTimeout(() => {
      document.addEventListener("click", q);
    }, 100), () => {
      document.removeEventListener("click", q);
    };
  }, [C, S, p, E]), FA(b && c, !1, C), lA(b, a, C), Vc(e, () => C, [C]), HA(C, D), /* @__PURE__ */ w.jsx("div", { className: Un(Xt.richTextEditor, t), style: A, children: /* @__PURE__ */ w.jsxs(
    "div",
    {
      className: Un(Xt.richTextEditorWrap, {
        [Xt.richTextEditorActive]: b
      }),
      style: { height: I },
      ref: B,
      children: [
        /* @__PURE__ */ w.jsx(
          "div",
          {
            className: Xt.richTextEditorText,
            ref: R,
            onMouseUp: () => C == null ? void 0 : C.focus()
          }
        ),
        M ? /* @__PURE__ */ w.jsx("div", { className: Xt.richTextEditorPlaceholder, children: n.placeholder }) : null
      ]
    }
  ) });
});
var Qe = function() {
  return Qe = Object.assign || function(n) {
    for (var e, t = 1, o = arguments.length; t < o; t++) {
      e = arguments[t];
      for (var s in e) Object.prototype.hasOwnProperty.call(e, s) && (n[s] = e[s]);
    }
    return n;
  }, Qe.apply(this, arguments);
}, GA = function(n, e) {
  var t = {};
  for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && e.indexOf(o) < 0 && (t[o] = n[o]);
  if (n != null && typeof Object.getOwnPropertySymbols == "function")
    for (var s = 0, o = Object.getOwnPropertySymbols(n); s < o.length; s++)
      e.indexOf(o[s]) < 0 && Object.prototype.propertyIsEnumerable.call(n, o[s]) && (t[o[s]] = n[o[s]]);
  return t;
}, Ht = It(function(n, e) {
  var t = n.icon, o = n.id, s = n.className, r = n.extend, i = GA(n, ["icon", "id", "className", "extend"]), a = "univerjs-icon univerjs-icon-".concat(o, " ").concat(s || "").trim(), c = cn("_".concat(KA()));
  return qi(t, "".concat(o), { defIds: t.defIds, idSuffix: c.current }, Qe({ ref: e, className: a }, i), r);
});
function qi(n, e, t, o, s) {
  return Ft(n.tag, Qe(Qe({ key: e }, YA(n, t, s)), o), (qA(n, t).children || []).map(function(r, i) {
    return qi(r, "".concat(e, "-").concat(n.tag, "-").concat(i), t, void 0, s);
  }));
}
function YA(n, e, t) {
  var o = Qe({}, n.attrs);
  t != null && t.colorChannel1 && o.fill === "colorChannel1" && (o.fill = t.colorChannel1);
  var s = e.defIds;
  return !s || s.length === 0 || (n.tag === "use" && o["xlink:href"] && (o["xlink:href"] = o["xlink:href"] + e.idSuffix), Object.entries(o).forEach(function(r) {
    var i = r[0], a = r[1];
    typeof a == "string" && (o[i] = a.replace(/url\(#(.*)\)/, "url(#$1".concat(e.idSuffix, ")")));
  })), o;
}
function qA(n, e) {
  var t, o = e.defIds;
  return !o || o.length === 0 ? n : n.tag === "defs" && (!((t = n.children) === null || t === void 0) && t.length) ? Qe(Qe({}, n), { children: n.children.map(function(s) {
    return typeof s.attrs.id == "string" && o && o.indexOf(s.attrs.id) > -1 ? Qe(Qe({}, s), { attrs: Qe(Qe({}, s.attrs), { id: s.attrs.id + e.idSuffix }) }) : s;
  }) }) : n;
}
function KA() {
  return Math.random().toString(36).substring(2, 8);
}
Ht.displayName = "UniverIcon";
var XA = { tag: "svg", attrs: { fill: "none", viewBox: "0 0 16 16", width: "1em", height: "1em" }, children: [{ tag: "path", attrs: { fill: "currentColor", d: "M1.9999 1.89941C1.66853 1.89941 1.3999 2.16804 1.3999 2.49941 1.3999 2.83078 1.66853 3.09941 1.9999 3.09941H13.9999C14.3313 3.09941 14.5999 2.83078 14.5999 2.49941 14.5999 2.16804 14.3313 1.89941 13.9999 1.89941H1.9999zM1.9999 5.56641C1.66853 5.56641 1.3999 5.83504 1.3999 6.16641 1.3999 6.49778 1.66853 6.76641 1.9999 6.76641H13.9999C14.3313 6.76641 14.5999 6.49778 14.5999 6.16641 14.5999 5.83504 14.3313 5.56641 13.9999 5.56641H1.9999zM1.3999 9.8334C1.3999 9.50203 1.66853 9.2334 1.9999 9.2334H13.9999C14.3313 9.2334 14.5999 9.50203 14.5999 9.8334 14.5999 10.1648 14.3313 10.4334 13.9999 10.4334H1.9999C1.66853 10.4334 1.3999 10.1648 1.3999 9.8334zM1.9999 12.9004C1.66853 12.9004 1.3999 13.169 1.3999 13.5004 1.3999 13.8318 1.66853 14.1004 1.9999 14.1004H13.9999C14.3313 14.1004 14.5999 13.8318 14.5999 13.5004 14.5999 13.169 14.3313 12.9004 13.9999 12.9004H1.9999z" } }] }, Ki = It(function(n, e) {
  return Ft(Ht, Object.assign({}, n, {
    id: "align-text-both-single",
    ref: e,
    icon: XA
  }));
});
Ki.displayName = "AlignTextBothSingle";
var JA = { tag: "svg", attrs: { fill: "none", viewBox: "0 0 16 16", width: "1em", height: "1em" }, children: [{ tag: "path", attrs: { fill: "currentColor", d: "M1.9999 1.89941C1.66853 1.89941 1.3999 2.16804 1.3999 2.49941 1.3999 2.83078 1.66853 3.09941 1.9999 3.09941H13.9999C14.3313 3.09941 14.5999 2.83078 14.5999 2.49941 14.5999 2.16804 14.3313 1.89941 13.9999 1.89941H1.9999zM3.33315 5.56641C3.00178 5.56641 2.73315 5.83504 2.73315 6.16641 2.73315 6.49778 3.00178 6.76641 3.33315 6.76641H12.6665C12.9979 6.76641 13.2665 6.49778 13.2665 6.16641 13.2665 5.83504 12.9979 5.56641 12.6665 5.56641H3.33315zM1.3999 9.8334C1.3999 9.50203 1.66853 9.2334 1.9999 9.2334H13.9999C14.3313 9.2334 14.5999 9.50203 14.5999 9.8334 14.5999 10.1648 14.3313 10.4334 13.9999 10.4334H1.9999C1.66853 10.4334 1.3999 10.1648 1.3999 9.8334zM3.33315 12.9004C3.00178 12.9004 2.73315 13.169 2.73315 13.5004 2.73315 13.8318 3.00178 14.1004 3.33315 14.1004H12.6665C12.9979 14.1004 13.2665 13.8318 13.2665 13.5004 13.2665 13.169 12.9979 12.9004 12.6665 12.9004H3.33315z" } }] }, Xi = It(function(n, e) {
  return Ft(Ht, Object.assign({}, n, {
    id: "horizontally-single",
    ref: e,
    icon: JA
  }));
});
Xi.displayName = "HorizontallySingle";
var ZA = { tag: "svg", attrs: { fill: "none", viewBox: "0 0 16 16", width: "1em", height: "1em" }, children: [{ tag: "path", attrs: { fill: "currentColor", d: "M1.9999 1.89941C1.66853 1.89941 1.3999 2.16804 1.3999 2.49941 1.3999 2.83078 1.66853 3.09941 1.9999 3.09941H13.9999C14.3313 3.09941 14.5999 2.83078 14.5999 2.49941 14.5999 2.16804 14.3313 1.89941 13.9999 1.89941H1.9999zM1.9999 5.56641C1.66853 5.56641 1.3999 5.83504 1.3999 6.16641 1.3999 6.49778 1.66853 6.76641 1.9999 6.76641H11.3332C11.6646 6.76641 11.9332 6.49778 11.9332 6.16641 11.9332 5.83504 11.6646 5.56641 11.3332 5.56641H1.9999zM1.3999 9.8334C1.3999 9.50203 1.66853 9.2334 1.9999 9.2334H13.9999C14.3313 9.2334 14.5999 9.50203 14.5999 9.8334 14.5999 10.1648 14.3313 10.4334 13.9999 10.4334H1.9999C1.66853 10.4334 1.3999 10.1648 1.3999 9.8334zM1.9999 12.9004C1.66853 12.9004 1.3999 13.169 1.3999 13.5004 1.3999 13.8318 1.66853 14.1004 1.9999 14.1004H11.3332C11.6646 14.1004 11.9332 13.8318 11.9332 13.5004 11.9332 13.169 11.6646 12.9004 11.3332 12.9004H1.9999z" } }] }, Ji = It(function(n, e) {
  return Ft(Ht, Object.assign({}, n, {
    id: "left-justifying-single",
    ref: e,
    icon: ZA
  }));
});
Ji.displayName = "LeftJustifyingSingle";
var $A = { tag: "svg", attrs: { fill: "none", viewBox: "0 0 16 16", width: "1em", height: "1em" }, children: [{ tag: "path", attrs: { fill: "currentColor", d: "M1.9999 1.89941C1.66853 1.89941 1.3999 2.16804 1.3999 2.49941 1.3999 2.83078 1.66853 3.09941 1.9999 3.09941H13.9999C14.3313 3.09941 14.5999 2.83078 14.5999 2.49941 14.5999 2.16804 14.3313 1.89941 13.9999 1.89941H1.9999zM4.66665 5.56641C4.33528 5.56641 4.06665 5.83504 4.06665 6.16641 4.06665 6.49778 4.33528 6.76641 4.66665 6.76641H14C14.3314 6.76641 14.6 6.49778 14.6 6.16641 14.6 5.83504 14.3314 5.56641 14 5.56641H4.66665zM1.3999 9.8334C1.3999 9.50203 1.66853 9.2334 1.9999 9.2334H13.9999C14.3313 9.2334 14.5999 9.50203 14.5999 9.8334 14.5999 10.1648 14.3313 10.4334 13.9999 10.4334H1.9999C1.66853 10.4334 1.3999 10.1648 1.3999 9.8334zM4.66665 12.9004C4.33528 12.9004 4.06665 13.169 4.06665 13.5004 4.06665 13.8318 4.33528 14.1004 4.66665 14.1004H14C14.3314 14.1004 14.6 13.8318 14.6 13.5004 14.6 13.169 14.3314 12.9004 14 12.9004H4.66665z" } }] }, Zi = It(function(n, e) {
  return Ft(Ht, Object.assign({}, n, {
    id: "right-justifying-single",
    ref: e,
    icon: $A
  }));
});
Zi.displayName = "RightJustifyingSingle";
var el = { tag: "svg", attrs: { fill: "none", viewBox: "0 0 16 16", width: "1em", height: "1em" }, children: [{ tag: "path", attrs: { fill: "currentColor", d: "M4.96372 2.59116C5.19803 2.35684 5.19803 1.97695 4.96372 1.74263 4.7294 1.50832 4.3495 1.50832 4.11519 1.74263L2.53945 3.31837 1.96372 2.74263C1.7294 2.50832 1.3495 2.50832 1.11519 2.74263.880874 2.97695.880874 3.35684 1.11519 3.59116L2.11519 4.59116C2.3495 4.82547 2.7294 4.82547 2.96372 4.59116L4.96372 2.59116zM14.4605 2.56689H6.8981C6.56672 2.56689 6.2981 2.83552 6.2981 3.16689 6.2981 3.49827 6.56672 3.76689 6.8981 3.76689H14.4605C14.7918 3.76689 15.0605 3.49827 15.0605 3.16689 15.0605 2.83552 14.7918 2.56689 14.4605 2.56689zM6.8981 7.2334C6.56672 7.2334 6.2981 7.50203 6.2981 7.8334 6.2981 8.16477 6.56672 8.4334 6.8981 8.4334H14.4605C14.7918 8.4334 15.0605 8.16477 15.0605 7.8334 15.0605 7.50203 14.7918 7.2334 14.4605 7.2334H6.8981zM6.2981 12.4999C6.2981 12.1685 6.56672 11.8999 6.8981 11.8999H14.4605C14.7918 11.8999 15.0605 12.1685 15.0605 12.4999 15.0605 12.8313 14.7918 13.0999 14.4605 13.0999H6.8981C6.56672 13.0999 6.2981 12.8313 6.2981 12.4999z" } }, { tag: "path", attrs: { fill: "currentColor", d: "M2.87279 5.8999C1.80504 5.8999.939453 6.76549.939453 7.83324.939453 8.90099 1.80504 9.76657 2.87279 9.76657 3.94054 9.76657 4.80612 8.90099 4.80612 7.83324 4.80612 6.76549 3.94054 5.8999 2.87279 5.8999zM2.13945 7.83324C2.13945 7.42823 2.46778 7.0999 2.87279 7.0999 3.2778 7.0999 3.60612 7.42823 3.60612 7.83324 3.60612 8.23824 3.2778 8.56657 2.87279 8.56657 2.46778 8.56657 2.13945 8.23824 2.13945 7.83324zM.939453 12.5002C.939453 11.4325 1.80504 10.5669 2.87279 10.5669 3.94054 10.5669 4.80612 11.4325 4.80612 12.5002 4.80612 13.568 3.94054 14.4336 2.87279 14.4336 1.80504 14.4336.939453 13.568.939453 12.5002zM2.87279 11.7669C2.46778 11.7669 2.13945 12.0952 2.13945 12.5002 2.13945 12.9052 2.46778 13.2336 2.87279 13.2336 3.2778 13.2336 3.60612 12.9052 3.60612 12.5002 3.60612 12.0952 3.2778 11.7669 2.87279 11.7669z", fillRule: "evenodd", clipRule: "evenodd" } }] }, $i = It(function(n, e) {
  return Ft(Ht, Object.assign({}, n, {
    id: "todo-list",
    ref: e,
    icon: el
  }));
});
$i.displayName = "TodoList";
function ea(n) {
  var o;
  const { dataStream: e } = (o = n.body) != null ? o : {}, t = [
    U.TABLE_START,
    U.TABLE_CELL_END,
    U.TABLE_CELL_START,
    U.TABLE_END,
    U.TABLE_ROW_END,
    U.TABLE_ROW_START,
    U.COLUMN_BREAK,
    U.PAGE_BREAK,
    U.TAB,
    U.DOCS_END,
    U.CUSTOM_BLOCK
  ];
  if (typeof e == "string")
    for (let s = 0; s < e.length; s++) {
      const r = e[s];
      if (!t.includes(r))
        return s;
    }
  return 0;
}
const ta = "COMPONENT_DOC_HEADER_FOOTER_PANEL", tl = "univer-panel", nl = "univer-options-section", ol = "univer-options-form-item", sl = "univer-options-input", rl = "univer-options-margin-setting", Pe = {
  panel: tl,
  optionsSection: nl,
  optionsFormItem: ol,
  optionsInput: sl,
  optionsMarginSetting: rl
};
function il(n, e, t) {
  const { useFirstPageHeaderFooter: o, evenAndOddHeaders: s, defaultHeaderId: r, defaultFooterId: i, firstPageHeaderId: a, firstPageFooterId: c, evenPageHeaderId: A, evenPageFooterId: l } = n;
  return e === ge.HEADER ? o === L.TRUE ? t === 0 ? a : s === L.TRUE && t % 2 === 1 ? A : r : s === L.TRUE && t % 2 === 1 ? A : r : o === L.TRUE ? t === 0 ? c : s === L.TRUE && t % 2 === 1 ? l : i : s === L.TRUE && t % 2 === 1 ? l : i;
}
const al = (n) => {
  const e = $(Ze), t = $(Q), o = $(fe), s = $(y), r = $(bs), { unitId: i } = n, a = o.getRenderById(i).with(Se), [c, A] = ve({}), l = (u, g) => {
    var C;
    A((T) => ({
      ...T,
      [g]: u ? L.TRUE : L.FALSE
    }));
    const f = t.getUniverDocInstance(i), p = f == null ? void 0 : f.getSnapshot().documentStyle, m = (C = o.getRenderById(i)) == null ? void 0 : C.with(ie), E = m == null ? void 0 : m.getViewModel();
    if (p == null || E == null)
      return;
    const I = E.getEditArea();
    let v = !1;
    const R = a.getSegmentPage();
    let S = !1;
    if (g === "useFirstPageHeaderFooter" && u === !0 && ((I === ge.HEADER && !p.firstPageHeaderId || I === ge.FOOTER && !p.firstPageFooterId) && (v = !0), v && R === 0 && (S = !0)), g === "evenAndOddHeaders" && u === !0 && ((I === ge.HEADER && !p.evenPageHeaderId || I === ge.FOOTER && !p.evenPageFooterId) && (v = !0), v && R % 2 === 1 && (S = !0)), v) {
      const O = X.generateRandomId(6);
      S && a.setSegment(O), s.executeCommand(_n, {
        unitId: i,
        segmentId: O,
        headerFooterProps: {
          [g]: u ? L.TRUE : L.FALSE
        }
      });
    } else {
      const T = a.getSegmentPage(), O = a.getSegment(), P = il(
        {
          ...p,
          [g]: u ? L.TRUE : L.FALSE
        },
        I,
        T
      );
      P && P !== O && a.setSegment(P), s.executeCommand(_n, {
        unitId: i,
        headerFooterProps: {
          [g]: u ? L.TRUE : L.FALSE
        }
      });
    }
    r.focus();
  }, d = async (u, g) => {
    A((f) => ({
      ...f,
      [g]: u
    })), await s.executeCommand(_n, {
      unitId: i,
      headerFooterProps: {
        [g]: u
      }
    }), a.removeAllRanges(), a.blur();
  }, h = () => {
    s.executeCommand(Ps.id, {
      unitId: i
    });
  };
  return Re(() => {
    const u = t.getUniverDocInstance(i), g = u == null ? void 0 : u.getSnapshot().documentStyle;
    if (g) {
      const {
        marginHeader: f = 0,
        marginFooter: p = 0,
        useFirstPageHeaderFooter: m = L.FALSE,
        evenAndOddHeaders: E = L.FALSE
      } = g;
      A({
        marginHeader: f,
        marginFooter: p,
        useFirstPageHeaderFooter: m,
        evenAndOddHeaders: E
      });
    }
  }, [i]), /* @__PURE__ */ w.jsxs("div", { className: Pe.options, children: [
    /* @__PURE__ */ w.jsxs("div", { className: Pe.optionsSection, children: [
      /* @__PURE__ */ w.jsx("div", { className: Pe.optionsFormItem, children: /* @__PURE__ */ w.jsx(
        Rr,
        {
          checked: c.useFirstPageHeaderFooter === L.TRUE,
          onChange: (u) => {
            l(u, "useFirstPageHeaderFooter");
          },
          children: e.t("headerFooter.firstPageCheckBox")
        }
      ) }),
      /* @__PURE__ */ w.jsx("div", { className: Pe.optionsFormItem, children: /* @__PURE__ */ w.jsx(
        Rr,
        {
          checked: c.evenAndOddHeaders === L.TRUE,
          onChange: (u) => {
            l(u, "evenAndOddHeaders");
          },
          children: e.t("headerFooter.oddEvenCheckBox")
        }
      ) })
    ] }),
    /* @__PURE__ */ w.jsxs("div", { className: Un(Pe.optionsSection, Pe.optionsMarginSetting), children: [
      /* @__PURE__ */ w.jsxs("div", { className: Pe.optionsMarginItem, children: [
        /* @__PURE__ */ w.jsx("span", { children: e.t("headerFooter.headerTopMargin") }),
        /* @__PURE__ */ w.jsx(
          An,
          {
            min: 0,
            max: 200,
            precision: 1,
            value: c.marginHeader,
            onChange: (u) => {
              d(u, "marginHeader");
            },
            className: Pe.optionsInput
          }
        )
      ] }),
      /* @__PURE__ */ w.jsxs("div", { className: Pe.optionsMarginItem, children: [
        /* @__PURE__ */ w.jsx("span", { children: e.t("headerFooter.footerBottomMargin") }),
        /* @__PURE__ */ w.jsx(
          An,
          {
            min: 0,
            max: 200,
            precision: 1,
            value: c.marginFooter,
            onChange: (u) => {
              d(u, "marginFooter");
            },
            className: Pe.optionsInput
          }
        )
      ] })
    ] }),
    /* @__PURE__ */ w.jsx("div", { className: Pe.optionsSection, children: /* @__PURE__ */ w.jsx(qc, { onClick: h, children: e.t("headerFooter.closeHeaderFooter") }) })
  ] });
}, cl = () => {
  var A;
  const n = $(Ze), e = $(fe), s = $(Q).getCurrentUniverDocInstance().getUnitId(), i = ((A = e.getRenderById(s)) == null ? void 0 : A.with(ie)).getViewModel(), [a, c] = ve(!0);
  return Re(() => {
    const l = i.getEditArea();
    c(l !== ge.BODY);
    const d = i.editAreaChange$.subscribe((h) => {
      h != null && c(h !== ge.BODY);
    });
    return () => {
      d.unsubscribe();
    };
  }, []), /* @__PURE__ */ w.jsx("div", { className: Pe.panel, children: a ? /* @__PURE__ */ w.jsx(al, { unitId: s }) : /* @__PURE__ */ w.jsx("div", { className: Pe.panelDisableText, children: n.t("headerFooter.disableText") }) });
}, Pr = 18, Dr = 200, _o = 6, Al = 4;
function ll(n, e) {
  let { radius: t, width: o, height: s } = e;
  t = t != null ? t : 0, o = o != null ? o : 30, s = s != null ? s : 30;
  let r = 0;
  r = Math.min(t, o / 2, s / 2), n.beginPath(), n.moveTo(0, 0), n.lineTo(o, 0), n.lineTo(o, s - r), n.arc(o - r, s - r, r, 0, Math.PI / 2, !1), n.lineTo(0, s), n.lineTo(0, 0), n.closePath(), e.fill && (n.save(), n.fillStyle = e.fill, e.fillRule === "evenodd" ? n.fill("evenodd") : n.fill(), n.restore());
}
class Ln extends dc {
  constructor(t, o) {
    super(t, o);
    x(this, "color");
    x(this, "text");
    this.color = o == null ? void 0 : o.color, this.text = o == null ? void 0 : o.text;
  }
  static drawWith(t, o) {
    const { text: s, color: r } = o;
    t.save(), t.font = "13px Source Han Sans CN";
    const i = t.measureText(s).width, a = Math.min(
      i + 2 * _o,
      Dr
    );
    ll(t, {
      height: Pr,
      width: a,
      radius: 4,
      fill: r,
      evented: !1
    }), t.fillStyle = "rgba(58, 96, 247, 1)";
    const c = _o, A = Pr - Al, l = Dr - 2 * _o;
    if (i > l) {
      let d = "", h = 0;
      for (const u of s) {
        const g = t.measureText(u).width;
        if (h + g <= l - t.measureText("...").width)
          d += u, h += g;
        else {
          d += "...";
          break;
        }
      }
      t.fillText(d, c, A);
    } else
      t.fillText(s, c, A);
    t.restore();
  }
  _draw(t) {
    Ln.drawWith(t, this);
  }
}
var dl = Object.defineProperty, ul = Object.getOwnPropertyDescriptor, hl = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? ul(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && dl(e, t, s), s;
}, nt = (n, e) => (t, o) => e(t, o, n);
const wr = "rgba(58, 96, 247, 1)", Nr = "rgba(58, 96, 247, 0.08)";
var Me = /* @__PURE__ */ ((n) => (n[n.FIRST_PAGE_HEADER = 0] = "FIRST_PAGE_HEADER", n[n.FIRST_PAGE_FOOTER = 1] = "FIRST_PAGE_FOOTER", n[n.DEFAULT_HEADER = 2] = "DEFAULT_HEADER", n[n.DEFAULT_FOOTER = 3] = "DEFAULT_FOOTER", n[n.EVEN_PAGE_HEADER = 4] = "EVEN_PAGE_HEADER", n[n.EVEN_PAGE_FOOTER = 5] = "EVEN_PAGE_FOOTER", n))(Me || {});
function gl(n, e, t) {
  const { documentStyle: o } = n.getDataModel().getSnapshot(), {
    defaultHeaderId: s,
    defaultFooterId: r,
    evenPageHeaderId: i,
    evenPageFooterId: a,
    firstPageHeaderId: c,
    firstPageFooterId: A,
    evenAndOddHeaders: l,
    useFirstPageHeaderFooter: d
  } = o;
  switch (e) {
    case ge.BODY:
      return {
        createType: null,
        headerFooterId: null
      };
    case ge.HEADER:
      return d === L.TRUE && !c ? {
        createType: 0,
        headerFooterId: null
      } : l === L.TRUE && t % 2 === 0 && !i ? {
        createType: 4,
        headerFooterId: null
      } : s ? {
        createType: null,
        headerFooterId: s
      } : {
        createType: 2,
        headerFooterId: null
      };
    case ge.FOOTER:
      return d === L.TRUE && !A ? {
        createType: 1,
        headerFooterId: null
      } : l === L.TRUE && t % 2 === 0 && !a ? {
        createType: 5,
        headerFooterId: null
      } : r ? {
        createType: null,
        headerFooterId: r
      } : {
        createType: 3,
        headerFooterId: null
      };
    default:
      throw new Error(`Invalid editArea: ${e}`);
  }
}
let Zo = class extends ue {
  constructor(e, t, o, s, r, i, a, c, A) {
    super();
    x(this, "_loadedMap", /* @__PURE__ */ new WeakSet());
    this._context = e, this._commandService = t, this._editorService = o, this._instanceSrv = s, this._renderManagerService = r, this._docSkeletonManagerService = i, this._docSelectionRenderService = a, this._localeService = c, this._componentManager = A, this._initialize();
  }
  _initialize() {
    this._init(), this._drawHeaderFooterLabel(), this._initCustomComponents(), this._listenSwitchMode();
  }
  // Close header footer panel when switch mode.
  _listenSwitchMode() {
    this.disposeWithMe(
      this._commandService.onCommandExecuted((e) => {
        if (J.id === e.id) {
          const t = this._context.unit, s = this._docSkeletonManagerService.getViewModel().getEditArea(), r = t.getSnapshot().documentStyle.documentFlavor;
          s !== ge.BODY && r === ye.MODERN && this._commandService.executeCommand(Ps.id, {
            unitId: this._context.unitId
          });
        }
      })
    );
  }
  _initCustomComponents() {
    const e = this._componentManager;
    this.disposeWithMe(e.register(ta, cl));
  }
  _init() {
    const { unitId: e } = this._context, t = rt(this._context);
    t == null || t.document == null || this._loadedMap.has(t.document) || (this._initialMain(e), this._loadedMap.add(t.document));
  }
  _initialMain(e) {
    const t = rt(this._context), { document: o } = t;
    this.disposeWithMe(o.onDblclick$.subscribeEvent(async (s) => {
      if (this._isEditorReadOnly(e) || !this._isTraditionalMode())
        return;
      const { offsetX: r, offsetY: i } = s, {
        pageLayoutType: a = an.VERTICAL,
        pageMarginLeft: c,
        pageMarginTop: A
      } = o.getOffsetConfig(), l = this._getTransformCoordForDocumentOffset(r, i);
      if (l == null)
        return;
      const d = this._docSkeletonManagerService.getViewModel(), h = this._docSkeletonManagerService.getSkeleton(), u = d.getEditArea(), { editArea: g, pageNumber: f } = h.findEditAreaByCoord(
        l,
        a,
        c,
        A
      );
      if (u === g)
        return;
      d.setEditArea(g);
      const { createType: p, headerFooterId: m } = gl(d, g, f);
      if (g === ge.BODY)
        this._docSelectionRenderService.setSegment(""), this._docSelectionRenderService.setSegmentPage(-1), this._docSelectionRenderService.setCursorManually(r, i);
      else if (p != null) {
        const I = X.generateRandomId(6);
        this._docSelectionRenderService.setSegment(I), this._docSelectionRenderService.setSegmentPage(f), await this._commandService.executeCommand(na.id, {
          unitId: e,
          createType: p,
          segmentId: I
        });
      } else m != null && (this._docSelectionRenderService.setSegment(m), this._docSelectionRenderService.setSegmentPage(f), this._docSelectionRenderService.setCursorManually(r, i));
    }));
  }
  _getTransformCoordForDocumentOffset(e, t) {
    const o = rt(this._context), { document: s, scene: r } = o, { documentTransform: i } = s.getOffsetConfig(), a = r.getViewports()[0];
    if (a == null)
      return;
    const c = a.transformVector2SceneCoord(rn.FromArray([e, t]));
    return i.clone().invert().applyPoint(c);
  }
  // eslint-disable-next-line max-lines-per-function
  _drawHeaderFooterLabel() {
    const e = this._localeService;
    this._renderManagerService.currentRender$.subscribe((t) => {
      if (t == null)
        return;
      const o = this._renderManagerService.getRenderById(t);
      if (this._editorService.isEditor(t) || this._instanceSrv.getUniverDocInstance(t) == null || o == null)
        return;
      const { mainComponent: s } = o, r = s;
      this.disposeWithMe(
        Zn(
          // eslint-disable-next-line max-lines-per-function
          r.pageRender$.subscribe((i) => {
            if (this._editorService.isEditor(t) || !this._isTraditionalMode())
              return;
            const A = this._docSkeletonManagerService.getViewModel().getEditArea() === ge.BODY, { page: l, pageLeft: d, pageTop: h, ctx: u } = i, { pageWidth: g, pageHeight: f, marginTop: p, marginBottom: m } = l;
            if (u.save(), u.translate(d - 0.5, h - 0.5), A ? (yn.drawWith(u, {
              left: 0,
              top: 0,
              width: g,
              height: p,
              fill: "rgba(255, 255, 255, 0.5)"
            }), u.save(), u.translate(0, f - m), yn.drawWith(u, {
              left: 0,
              top: 0,
              width: g,
              height: m,
              fill: "rgba(255, 255, 255, 0.5)"
            }), u.restore()) : (u.save(), u.translate(0, p), yn.drawWith(u, {
              left: 0,
              top: p,
              width: g,
              height: f - p - m,
              fill: "rgba(255, 255, 255, 0.5)"
            }), u.restore()), !A) {
              const E = {
                dataArray: [{
                  command: "M",
                  points: [0, p]
                }, {
                  command: "L",
                  points: [g, p]
                }],
                strokeWidth: 1,
                stroke: wr
              }, I = {
                dataArray: [{
                  command: "M",
                  points: [0, f - m]
                }, {
                  command: "L",
                  points: [g, f - m]
                }],
                strokeWidth: 1,
                stroke: wr
              };
              mr.drawWith(u, E), mr.drawWith(u, I), u.translate(0, p + 1), Ln.drawWith(u, {
                text: e.t("headerFooter.header"),
                color: Nr
              }), u.translate(0, f - p - m), Ln.drawWith(u, {
                text: e.t("headerFooter.footer"),
                color: Nr
              });
            }
            u.restore();
          })
        )
      );
    });
  }
  _isEditorReadOnly(e) {
    const t = this._editorService.getEditor(e);
    return t ? t.isReadOnly() : !1;
  }
  _isTraditionalMode() {
    return this._context.unit.getSnapshot().documentStyle.documentFlavor === ye.TRADITIONAL;
  }
};
Zo = hl([
  nt(1, y),
  nt(2, He),
  nt(3, Q),
  nt(4, fe),
  nt(5, z(ie)),
  nt(6, z(Se)),
  nt(7, z(Ze)),
  nt(8, z(io))
], Zo);
const Ms = {
  id: "sidebar.operation.doc-header-footer-panel",
  type: N.OPERATION,
  handler: async (n, e) => {
    const t = n.get(Bi), o = n.get(Ze);
    switch (e.value) {
      case "open":
        t.open({
          header: { title: o.t("headerFooter.panel") },
          children: { label: ta },
          onClose: () => {
          },
          width: 400
        });
        break;
      case "close":
      default:
        t.close();
        break;
    }
    return !0;
  }
};
function Qr() {
  return {
    dataStream: `\r
`,
    textRuns: [{
      st: 0,
      ed: 0,
      ts: {
        fs: 9
        // The default header footer text size.
      }
    }],
    customBlocks: [],
    paragraphs: [
      {
        startIndex: 0,
        paragraphStyle: {
          spaceAbove: { v: 0 },
          lineSpacing: 1.5,
          spaceBelow: { v: 0 }
        }
      }
    ],
    sectionBreaks: [
      {
        startIndex: 1
      }
    ]
  };
}
function Po(n, e, t, o) {
  const s = k.getInstance(), r = 6, i = n != null ? n : X.generateRandomId(r), a = e === Me.DEFAULT_HEADER || e === Me.FIRST_PAGE_HEADER || e === Me.EVEN_PAGE_HEADER, c = s.insertOp([a ? "headers" : "footers", i], {
    [a ? "headerId" : "footerId"]: i,
    body: Qr()
  });
  o.push(c);
  const A = X.generateRandomId(r), l = s.insertOp([a ? "footers" : "headers", A], {
    [a ? "footerId" : "headerId"]: A,
    body: Qr()
  });
  o.push(l);
  let d = "defaultHeaderId", h = "defaultFooterId";
  switch (e) {
    case Me.DEFAULT_HEADER:
      d = "defaultHeaderId", h = "defaultFooterId";
      break;
    case Me.DEFAULT_FOOTER:
      d = "defaultFooterId", h = "defaultHeaderId";
      break;
    case Me.FIRST_PAGE_HEADER:
      d = "firstPageHeaderId", h = "firstPageFooterId";
      break;
    case Me.FIRST_PAGE_FOOTER:
      d = "firstPageFooterId", h = "firstPageHeaderId";
      break;
    case Me.EVEN_PAGE_HEADER:
      d = "evenPageHeaderId", h = "evenPageFooterId";
      break;
    case Me.EVEN_PAGE_FOOTER:
      d = "evenPageFooterId", h = "evenPageHeaderId";
      break;
    default:
      throw new Error(`Unknown header footer type: ${e}`);
  }
  for (const [u, g] of [[d, i], [h, A]])
    if (t[u] != null) {
      const f = s.replaceOp(["documentStyle", u], t[u], g);
      o.push(f);
    } else {
      const f = s.insertOp(["documentStyle", u], g);
      o.push(f);
    }
  return o;
}
const _n = "doc.command.core-header-footer", na = {
  id: _n,
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n, e) => {
    var v;
    const t = n.get(y), o = n.get(Q), s = n.get(fe), { unitId: r, segmentId: i, createType: a, headerFooterProps: c } = e, A = (v = s.getRenderById(r)) == null ? void 0 : v.with(ie), l = o.getUniverDocInstance(r), d = A == null ? void 0 : A.getViewModel();
    if (l == null || d == null)
      return !1;
    const h = d.getEditArea(), { documentStyle: u } = l.getSnapshot(), g = (c == null ? void 0 : c.marginFooter) != null || (c == null ? void 0 : c.marginHeader) != null, f = [{
      startOffset: 0,
      endOffset: 0,
      collapsed: !0
    }], p = {
      id: J.id,
      params: {
        unitId: r,
        actions: [],
        textRanges: f,
        debounce: !0
      }
    };
    g && (p.params.noNeedSetTextRange = !0);
    const m = k.getInstance(), E = [];
    return a != null && Po(i, a, u, E), c != null && Object.keys(c).forEach((R) => {
      const S = c[R], C = u[R];
      if (S === C)
        return;
      let T;
      if (C === void 0 ? T = m.insertOp(["documentStyle", R], S) : T = m.replaceOp(["documentStyle", R], C, S), E.push(T), R === "useFirstPageHeaderFooter" && S === L.TRUE && !u.firstPageHeaderId) {
        const O = h === ge.HEADER ? Me.FIRST_PAGE_HEADER : Me.FIRST_PAGE_FOOTER;
        Po(i, O, u, E);
      } else if (R === "evenAndOddHeaders" && S === L.TRUE && !u.evenPageHeaderId) {
        const O = h === ge.HEADER ? Me.EVEN_PAGE_HEADER : Me.EVEN_PAGE_FOOTER;
        Po(i, O, u, E);
      }
    }), E.length === 0 ? !1 : (p.params.actions = E.reduce((R, S) => k.compose(R, S), null), !!t.syncExecuteCommand(p.id, p.params));
  }
}, _s = {
  id: "doc.command.open-header-footer-panel",
  type: N.COMMAND,
  handler: async (n, e) => n.get(y).executeCommand(Ms.id, { value: "open" })
}, Ps = {
  id: "doc.command.close-header-footer",
  type: N.COMMAND,
  handler: async (n, e) => {
    var g;
    const t = n.get(y), o = n.get(fe), s = n.get(G), r = n.get(Q), { unitId: i } = e, a = o.getRenderById(i);
    if (a == null)
      return !1;
    const { scene: c } = a, A = c.getTransformerByCreate(), l = a.with(ie), d = a.with(Se), h = l == null ? void 0 : l.getSkeleton(), u = l == null ? void 0 : l.getViewModel();
    return u == null || h == null ? !1 : (s.replaceDocRanges([]), A.clearSelectedObjects(), d.setSegment(""), d.setSegmentPage(-1), u.setEditArea(ge.BODY), h.calculate(), (g = a.mainComponent) == null || g.makeDirty(!0), queueMicrotask(() => {
      const f = r.getUnit(i), p = f == null ? void 0 : f.getSnapshot();
      if (p == null)
        return;
      const m = ea(p);
      s.replaceDocRanges([
        {
          startOffset: m,
          endOffset: m
        }
      ]);
    }), t.executeCommand(Ms.id, { value: "close" }), !0);
  }
}, kt = "UI_PLUGIN_DOCS", Ds = `${kt}_COLOR_PICKER_COMPONENT`, oa = `${kt}_FONT_FAMILY_COMPONENT`, sa = `${kt}_FONT_FAMILY_ITEM_COMPONENT`, ra = `${kt}_FONT_SIZE_COMPONENT`, fl = "univer-doc-list-type-picker", pl = "univer-doc-list-type-picker-item", ml = "univer-doc-list-type-picker-item-active", Do = {
  docListTypePicker: fl,
  docListTypePickerItem: pl,
  docListTypePickerItemActive: ml
}, ia = (n) => {
  const { value: e, onChange: t, options: o } = n;
  return /* @__PURE__ */ w.jsx("div", { className: Do.docListTypePicker, children: o.map((s) => /* @__PURE__ */ w.jsx(
    "img",
    {
      className: Do.docListTypePickerItem + (e === s.value ? `
                              ${Do.docListTypePickerItemActive}
                            ` : ""),
      onClick: () => {
        t(s.value);
      },
      src: s.img
    },
    s.value
  )) });
}, El = [
  {
    value: Oe.ORDER_LIST,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.ORDER_LIST_1,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.ORDER_LIST_2,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.ORDER_LIST_3,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.ORDER_LIST_4,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.ORDER_LIST_5,
    img: "data:image/jpeg;base64,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"
  }
], Sl = (n) => /* @__PURE__ */ w.jsx(
  ia,
  {
    ...n,
    options: El
  }
), Il = [
  {
    value: Oe.BULLET_LIST,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.BULLET_LIST_1,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.BULLET_LIST_2,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.BULLET_LIST_3,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.BULLET_LIST_4,
    img: "data:image/jpeg;base64,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"
  },
  {
    value: Oe.BULLET_LIST_5,
    img: "data:image/jpeg;base64,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"
  }
], Cl = (n) => /* @__PURE__ */ w.jsx(
  ia,
  {
    ...n,
    options: Il
  }
), aa = `${kt}_ORDER_LIST_TYPE_COMPONENT`, ca = `${kt}_BULLET_LIST_TYPE_COMPONENT`, vl = "doc.command.tab", _t = {
  id: vl,
  type: N.COMMAND,
  async handler(n, e) {
    const o = n.get(Et).onAutoFormat(_t.id, e);
    return (await Es(o, n.get(y))).result;
  }
}, Rl = "doc.command.after-space", Ao = {
  id: Rl,
  type: N.COMMAND,
  async handler(n) {
    const t = n.get(Et).onAutoFormat(Ao.id);
    return (await Es(t, n.get(y))).result;
  }
}, ln = {
  id: "doc.command.enter",
  type: N.COMMAND,
  async handler(n) {
    const t = n.get(Et).onAutoFormat(ln.id);
    return (await Es(t, n.get(y))).result;
  }
};
function de(n) {
  return n.getContextValue(hn) && n.getContextValue(Ss) && !n.getContextValue(mi);
}
function bl(n) {
  return n.getContextValue(hn) && n.getContextValue(Ss) && !n.getContextValue(mi);
}
const xl = {
  id: _t.id,
  binding: j.TAB,
  preconditions: de
}, Ol = {
  id: _t.id,
  binding: j.TAB | K.SHIFT,
  preconditions: de,
  staticParameters: {
    shift: !0
  }
};
var Tl = Object.defineProperty, yl = Object.getOwnPropertyDescriptor, Bl = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? yl(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Tl(e, t, s), s;
}, wo = (n, e) => (t, o) => e(t, o, n);
const Ml = 11, _l = 9, vn = {
  /**
   * fontFamily
   */
  ff: "Arial",
  /**
   * fontSize
   */
  fs: Ml
};
let Je = class extends ue {
  constructor(e, t, o) {
    super();
    x(this, "_cacheStyle", null);
    this._textSelectionManagerService = e, this._univerInstanceService = t, this._renderManagerService = o, this._init();
  }
  _init() {
    this._listenDocRangeChange();
  }
  _listenDocRangeChange() {
    this.disposeWithMe(
      this._textSelectionManagerService.textSelection$.subscribe(() => {
        this._clearStyleCache();
      })
    );
  }
  getStyleCache() {
    return this._cacheStyle;
  }
  getDefaultStyle() {
    var i;
    const e = this._univerInstanceService.getCurrentUnitForType(_.UNIVER_DOC);
    if (e == null)
      return {
        ...vn
      };
    const t = e == null ? void 0 : e.getUnitId(), o = (i = this._renderManagerService.getRenderById(t)) == null ? void 0 : i.with(ie), s = o == null ? void 0 : o.getViewModel();
    return s == null ? {
      ...vn
    } : s.getEditArea() === ge.BODY ? {
      ...vn
    } : {
      ...vn,
      fs: _l
    };
  }
  setStyleCache(e) {
    this._cacheStyle = {
      ...this._cacheStyle,
      ...e
    };
  }
  _clearStyleCache() {
    this._cacheStyle = null;
  }
};
Je = Bl([
  wo(0, z(G)),
  wo(1, Q),
  wo(2, fe)
], Je);
function Ve(n, e, t) {
  return t.executeCommand(lt.id, {
    preCommandId: n,
    ...e != null ? e : {}
  });
}
const Ur = "doc.command.set-inline-format-bold", Vt = {
  id: Ur,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      Ur,
      e,
      t
    );
  }
}, Lr = "doc.command.set-inline-format-italic", jt = {
  id: Lr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      Lr,
      e,
      t
    );
  }
}, Fr = "doc.command.set-inline-format-underline", Wt = {
  id: Fr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      Fr,
      e,
      t
    );
  }
}, Hr = "doc.command.set-inline-format-strikethrough", zt = {
  id: Hr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      Hr,
      e,
      t
    );
  }
}, kr = "doc.command.set-inline-format-subscript", Ct = {
  id: kr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      kr,
      e,
      t
    );
  }
}, Vr = "doc.command.set-inline-format-superscript", Gt = {
  id: Vr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      Vr,
      e,
      t
    );
  }
}, jr = "doc.command.set-inline-format-fontsize", Pt = {
  id: jr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      jr,
      e,
      t
    );
  }
}, Wr = "doc.command.set-inline-format-font-family", Dt = {
  id: Wr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      Wr,
      e,
      t
    );
  }
}, zr = "doc.command.set-inline-format-text-color", wt = {
  id: zr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      zr,
      e,
      t
    );
  }
}, Gr = "doc.command.set-inline-format-text-background-color", Nt = {
  id: Gr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      Gr,
      e,
      t
    );
  }
}, Yr = "doc.command.reset-inline-format-text-background-color", fn = {
  id: Yr,
  type: N.COMMAND,
  handler: async (n, e) => {
    const t = n.get(y);
    return Ve(
      Yr,
      e,
      t
    );
  }
}, $o = {
  [Vt.id]: "bl",
  [jt.id]: "it",
  [Wt.id]: "ul",
  [zt.id]: "st",
  [Pt.id]: "fs",
  [Dt.id]: "ff",
  [wt.id]: "cl",
  [Nt.id]: "bg",
  [fn.id]: "bg",
  [Ct.id]: "va",
  [Gt.id]: "va"
}, lt = {
  id: "doc.command.set-inline-format",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function, complexity
  handler: async (n, e) => {
    var R;
    const { value: t, preCommandId: o } = e, s = n.get(y), r = n.get(G), i = n.get(Q), a = n.get(Je), c = r.getDocRanges(), A = (R = c.find((S) => S.isActive)) != null ? R : c[0];
    if (c.length === 0)
      return !1;
    const { segmentId: l } = c[0], d = i.getCurrentUnitForType(_.UNIVER_DOC);
    if (d == null)
      return !1;
    const h = d.getSelfOrHeaderFooterModel(l).getBody();
    if (h == null)
      return !1;
    const u = d.getUnitId();
    let g;
    switch (o) {
      case Vt.id:
      // fallthrough
      case jt.id:
      // fallthrough
      case Wt.id:
      // fallthrough
      case zt.id:
      // fallthrough
      case Ct.id:
      // fallthrough
      case Gt.id: {
        const S = a.getDefaultStyle(), C = la(
          h,
          A,
          S
        );
        g = Dl(
          C,
          o
        );
        break;
      }
      case Pt.id:
      case Dt.id: {
        g = t;
        break;
      }
      case wt.id:
      case Nt.id: {
        g = {
          rgb: t
        };
        break;
      }
      case fn.id: {
        g = {
          rgb: null
        };
        break;
      }
      default:
        throw new Error(`Unknown command: ${o} in handleInlineFormat`);
    }
    const f = {
      id: J.id,
      params: {
        unitId: u,
        actions: [],
        textRanges: c
      }
    }, p = new me(), m = k.getInstance(), E = new St();
    E.reset();
    for (const S of c) {
      let { startOffset: C, endOffset: T, rangeType: O } = S;
      if (C == null || T == null)
        continue;
      if (O === Ge.RECT && (C = C - 1), C === T) {
        const B = a.getStyleCache(), M = $o[o];
        a.setStyleCache(
          {
            [M]: (B == null ? void 0 : B[M]) !== void 0 ? Aa(
              B,
              M,
              o
            ) : g
          }
        );
        continue;
      }
      const P = {
        dataStream: "",
        textRuns: [
          {
            st: 0,
            ed: T - C,
            ts: {
              [$o[o]]: g
            }
          }
        ]
      }, b = C - E.cursor;
      b !== 0 && p.push({
        t: W.RETAIN,
        len: b
      }), p.push({
        t: W.RETAIN,
        body: P,
        len: T - C
      }), E.reset(), E.moveCursor(T);
    }
    const I = le(d, l);
    return f.params.actions = m.editOp(p.serialize(), I), !!s.syncExecuteCommand(f.id, f.params);
  }
};
function Pl(n) {
  return n !== null && typeof n == "object";
}
function Aa(n, e, t) {
  if (/bl|it/.test(e))
    return (n == null ? void 0 : n[e]) === L.TRUE ? L.FALSE : L.TRUE;
  if (/ul|st/.test(e))
    return Pl(n == null ? void 0 : n[e]) && (n == null ? void 0 : n[e]).s === L.TRUE ? {
      s: L.FALSE
    } : {
      s: L.TRUE
    };
  if (/va/.test(e))
    return t === Ct.id ? (n == null ? void 0 : n[e]) === Ne.SUBSCRIPT ? Ne.NORMAL : Ne.SUBSCRIPT : (n == null ? void 0 : n[e]) === Ne.SUPERSCRIPT ? Ne.NORMAL : Ne.SUPERSCRIPT;
}
function la(n, e, t) {
  var A, l, d, h, u, g, f, p, m, E, I, v, R, S;
  const { startOffset: o, endOffset: s, collapsed: r } = e;
  if (r) {
    const C = (A = n.textRuns) != null ? A : [];
    let T = null;
    for (let O = C.length - 1; O >= 0; O--) {
      const P = C[O];
      if (P.st < o && o <= P.ed) {
        T = P;
        break;
      }
    }
    return T != null && T.ts ? { ...t, ...T.ts } : t;
  }
  const { textRuns: i = [] } = Ei(n, o, s), a = X.deepClone(t);
  a.fs = Math.max(a.fs, ...i.map((C) => {
    var T, O;
    return (O = (T = C == null ? void 0 : C.ts) == null ? void 0 : T.fs) != null ? O : a.fs;
  })), a.ff = (h = (d = (l = i.find((C) => {
    var T;
    return ((T = C.ts) == null ? void 0 : T.ff) != null;
  })) == null ? void 0 : l.ts) == null ? void 0 : d.ff) != null ? h : a.ff, a.it = i.length && i.every((C) => {
    var T;
    return ((T = C.ts) == null ? void 0 : T.it) === L.TRUE;
  }) ? L.TRUE : L.FALSE, a.bl = i.length && i.every((C) => {
    var T;
    return ((T = C.ts) == null ? void 0 : T.bl) === L.TRUE;
  }) ? L.TRUE : L.FALSE, a.ul = i.length && i.every((C) => {
    var T, O;
    return ((O = (T = C.ts) == null ? void 0 : T.ul) == null ? void 0 : O.s) === L.TRUE;
  }) ? (u = i[0].ts) == null ? void 0 : u.ul : a.ul, a.st = i.length && i.every((C) => {
    var T, O;
    return ((O = (T = C.ts) == null ? void 0 : T.st) == null ? void 0 : O.s) === L.TRUE;
  }) ? (g = i[0].ts) == null ? void 0 : g.st : a.st, a.bg = (m = (p = (f = i.find((C) => {
    var T;
    return ((T = C.ts) == null ? void 0 : T.bg) != null;
  })) == null ? void 0 : f.ts) == null ? void 0 : p.bg) != null ? m : a.bg, a.cl = (v = (I = (E = i.find((C) => {
    var T;
    return ((T = C.ts) == null ? void 0 : T.cl) != null;
  })) == null ? void 0 : E.ts) == null ? void 0 : I.cl) != null ? v : a.cl;
  const c = i.filter((C) => {
    var T;
    return ((T = C == null ? void 0 : C.ts) == null ? void 0 : T.va) != null;
  });
  if (c.length > 0 && c.length === i.length) {
    const C = (R = c[0].ts) == null ? void 0 : R.va;
    let T = !0;
    for (let O = 1; O < c.length; O++)
      if (((S = c[O].ts) == null ? void 0 : S.va) !== C) {
        T = !1;
        break;
      }
    T && (a.va = C);
  }
  return a;
}
function Dl(n, e) {
  const t = $o[e];
  return Aa(n, t, e);
}
const pn = {
  id: "doc.command.list-operation",
  type: N.COMMAND,
  handler: (n, e) => {
    var E, I;
    const t = n.get(G), o = n.get(Q), s = n.get(y), r = e.listType, i = o.getCurrentUnitForType(_.UNIVER_DOC), a = (E = t.getDocRanges()) != null ? E : [];
    if (i == null || a.length === 0)
      return !1;
    const c = a[0].segmentId, A = (I = i.getSelfOrHeaderFooterModel(c).getBody()) == null ? void 0 : I.paragraphs;
    if (A == null)
      return !1;
    const l = mn(a, A), d = i.getUnitId(), h = {
      id: J.id,
      params: {
        unitId: d,
        actions: [],
        textRanges: a,
        isEditing: !1
      }
    };
    new St().reset();
    const g = Ce.paragraph.bullet.switch({
      paragraphs: l,
      listType: r,
      document: i,
      segmentId: c
    }), f = k.getInstance(), p = le(i, c);
    return h.params.actions = f.editOp(g.serialize(), p), !!s.syncExecuteCommand(h.id, h.params);
  }
}, lo = {
  id: "doc.command.change-list-type",
  type: N.COMMAND,
  handler: (n, e) => {
    var E, I;
    const t = n.get(G), o = n.get(Q), s = n.get(y), { listType: r } = e, i = o.getCurrentUnitForType(_.UNIVER_DOC), a = t.getDocRanges();
    if (i == null || a == null || !a.length)
      return !1;
    const { segmentId: c } = a[0], A = (E = t.getDocRanges()) != null ? E : [], l = (I = i.getSelfOrHeaderFooterModel(c).getBody()) == null ? void 0 : I.paragraphs;
    if (l == null)
      return !1;
    const d = mn(A, l), h = i.getUnitId(), u = Ce.paragraph.bullet.set({
      paragraphs: d,
      listType: r,
      segmentId: c,
      document: i
    });
    if (!u)
      return !1;
    const g = k.getInstance(), f = {
      id: J.id,
      params: {
        unitId: h,
        actions: [],
        textRanges: A,
        isEditing: !1
      }
    }, p = le(i, c);
    return f.params.actions = g.editOp(u.serialize(), p), !!s.syncExecuteCommand(f.id, f.params);
  }
};
var Pn = /* @__PURE__ */ ((n) => (n[n.increase = 1] = "increase", n[n.decrease = -1] = "decrease", n))(Pn || {});
const es = {
  id: "doc.command.change-list-nesting-level",
  type: N.COMMAND,
  handler: (n, e) => {
    var E, I;
    if (!e)
      return !1;
    const { type: t } = e, o = n.get(G), s = n.get(Q), r = n.get(y), i = s.getCurrentUnitForType(_.UNIVER_DOC), a = o.getActiveTextRange();
    if (i == null || a == null)
      return !1;
    const { segmentId: c } = a, A = (E = o.getDocRanges()) != null ? E : [], l = (I = i.getSelfOrHeaderFooterModel(c).getBody()) == null ? void 0 : I.paragraphs;
    if (l == null)
      return !1;
    const d = Qs(a, l), h = i.getUnitId(), u = k.getInstance(), g = Ce.paragraph.bullet.changeNestLevel({
      paragraphs: d,
      type: t,
      segmentId: c,
      document: i
    }), f = {
      id: J.id,
      params: {
        unitId: h,
        actions: [],
        textRanges: A,
        isEditing: !1
      }
    }, p = le(i, c);
    return f.params.actions = u.editOp(g.serialize(), p), !!r.syncExecuteCommand(f.id, f.params);
  }
}, uo = {
  id: "doc.command.bullet-list",
  type: N.COMMAND,
  handler: (n, e) => {
    const t = n.get(y);
    return e != null && e.value ? t.syncExecuteCommand(lo.id, {
      listType: e.value
    }) : t.syncExecuteCommand(pn.id, {
      listType: Oe.BULLET_LIST
    });
  }
}, ws = {
  id: "doc.command.check-list",
  type: N.COMMAND,
  handler: (n, e) => {
    const t = n.get(y);
    return e != null && e.value ? t.syncExecuteCommand(lo.id, {
      listType: e.value
    }) : t.syncExecuteCommand(pn.id, {
      listType: Oe.CHECK_LIST
    });
  }
}, Ns = {
  id: "doc.command.toggle-check-list",
  type: N.COMMAND,
  handler: (n, e) => {
    var f;
    if (!e)
      return !1;
    const t = n.get(Q), o = n.get(y), { index: s, segmentId: r, textRanges: i } = e, a = t.getCurrentUnitForType(_.UNIVER_DOC);
    if (a == null || ((f = a.getSelfOrHeaderFooterModel(r).getBody()) == null ? void 0 : f.paragraphs) == null)
      return !1;
    const A = a.getUnitId(), l = {
      id: J.id,
      params: {
        unitId: A,
        actions: [],
        textRanges: i != null ? i : [],
        segmentId: r,
        isEditing: !1
      }
    }, d = Ce.paragraph.bullet.toggleChecklist({
      document: a,
      paragraphIndex: s,
      segmentId: r
    });
    if (!d)
      return !1;
    const h = k.getInstance(), u = le(a, r);
    return l.params.actions = h.editOp(d.serialize(), u), !!o.syncExecuteCommand(l.id, l.params);
  }
}, ho = {
  id: "doc.command.order-list",
  type: N.COMMAND,
  handler: (n, e) => {
    const t = n.get(y);
    return e != null && e.value ? t.syncExecuteCommand(lo.id, {
      listType: e.value
    }) : t.syncExecuteCommand(pn.id, {
      listType: Oe.ORDER_LIST
    });
  }
}, da = {
  id: "doc.command.quick-list",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler(n, e) {
    var oe, ce, he, Ae, ne;
    if (!e)
      return !1;
    const t = n.get(G), o = n.get(Q), s = n.get(y), r = o.getCurrentUnitForType(_.UNIVER_DOC), i = t.getActiveTextRange();
    if (r == null || i == null)
      return !1;
    const { segmentId: a } = i, { listType: c, paragraph: A } = e, { paragraphStart: l, paragraphEnd: d } = A, h = new me(), u = k.getInstance(), { defaultTabStop: g = 36 } = r.getSnapshot().documentStyle, f = (ce = (oe = r.getSelfOrHeaderFooterModel(a).getBody()) == null ? void 0 : oe.sectionBreaks) != null ? ce : [], { startIndex: p, paragraphStyle: m = {} } = A, { indentFirstLine: E, snapToGrid: I, indentStart: v } = m, R = Wa[c].nestingLevel[0].paragraphProperties || {}, { hanging: S, indentStart: C } = R, T = R.textStyle, { charSpace: O, gridType: P } = wl(p, f) || { charSpace: 0, gridType: za.LINES }, b = uc(O, g, P, I);
    let M = X.generateRandomId(6);
    const H = (Ae = (he = r.getBody()) == null ? void 0 : he.paragraphs) != null ? Ae : [], F = H.findIndex((ae) => ae.startIndex === A.startIndex), D = H[F - 1], te = H[F + 1];
    D && D.bullet && D.bullet.listType.indexOf(c) === 0 ? M = D.bullet.listId : te && te.bullet && te.bullet.listType.indexOf(c) === 0 && (M = te.bullet.listId);
    const q = {
      id: J.id,
      params: {
        unitId: r.getUnitId(),
        actions: [],
        textRanges: [{
          startOffset: l,
          endOffset: l,
          collapsed: !0
        }],
        isEditing: !1
      }
    };
    h.push({
      t: W.RETAIN,
      len: l
    }), h.push({
      t: W.DELETE,
      len: d - l
    }), h.push({
      t: W.RETAIN,
      len: 1,
      body: {
        dataStream: "",
        paragraphs: [
          {
            startIndex: 0,
            paragraphStyle: {
              ...m,
              textStyle: {
                ...m.textStyle,
                ...T
              },
              indentFirstLine: void 0,
              hanging: S,
              indentStart: { v: ze(C, b) - ze(S, b) + ze(E, b) + ze(v, b) }
            },
            bullet: {
              ...(ne = A.bullet) != null ? ne : {
                nestingLevel: 0,
                textStyle: {
                  fs: 20
                }
              },
              listType: c,
              listId: M
            }
          }
        ]
      }
    });
    const V = le(r, a);
    return q.params.actions = u.editOp(h.serialize(), V), !!s.syncExecuteCommand(q.id, q.params);
  }
};
function Qs(n, e) {
  const { startOffset: t, endOffset: o } = n, s = [];
  let r = -1;
  for (const i of e) {
    const { startIndex: a } = i;
    (t > r && t <= a || o > r && o <= a || a >= t && a <= o) && s.push(i), r = a;
  }
  return s;
}
function mn(n, e) {
  const t = [];
  for (const o of n) {
    const s = Qs(o, e);
    t.push(...s);
  }
  return t;
}
function wl(n, e) {
  const t = e.sort(Ga("startIndex"));
  for (let o = 0; o < t.length; o++) {
    const s = e[o];
    if (s.startIndex >= n)
      return s;
  }
}
const et = {
  id: "doc.command.align-action",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: (n, e) => {
    var I;
    const t = n.get(G), o = n.get(Q), s = n.get(y), { alignType: r } = e, i = o.getCurrentUniverDocInstance();
    if (i == null)
      return !1;
    const a = t.getDocRanges();
    if (a.length === 0)
      return !1;
    const c = a[0].segmentId, A = (I = i.getSelfOrHeaderFooterModel(c).getBody()) == null ? void 0 : I.paragraphs;
    if (A == null)
      return !1;
    const l = mn(a, A), d = i.getUnitId(), h = l.every((v) => {
      var R;
      return ((R = v.paragraphStyle) == null ? void 0 : R.horizontalAlign) === r;
    }), u = {
      id: J.id,
      params: {
        unitId: d,
        actions: [],
        textRanges: a
      }
    }, g = new St();
    g.reset();
    const f = new me(), p = k.getInstance();
    for (const v of l) {
      const { startIndex: R } = v;
      f.push({
        t: W.RETAIN,
        len: R - g.cursor
      });
      const S = {
        ...v.paragraphStyle,
        horizontalAlign: h ? _e.UNSPECIFIED : r
      };
      f.push({
        t: W.RETAIN,
        len: 1,
        body: {
          dataStream: "",
          paragraphs: [
            {
              ...v,
              paragraphStyle: S,
              startIndex: 0
            }
          ]
        },
        coverType: no.REPLACE
      }), g.moveCursorTo(R + 1);
    }
    const m = le(i, c);
    return u.params.actions = p.editOp(f.serialize(), m), !!s.syncExecuteCommand(u.id, u.params);
  }
}, go = {
  id: "doc.command.align-left",
  type: N.COMMAND,
  handler: (n) => n.get(y).syncExecuteCommand(et.id, {
    alignType: _e.LEFT
  })
}, fo = {
  id: "doc.command.align-center",
  type: N.COMMAND,
  handler: (n) => n.get(y).syncExecuteCommand(et.id, {
    alignType: _e.CENTER
  })
}, po = {
  id: "doc.command.align-right",
  type: N.COMMAND,
  handler: (n) => n.get(y).syncExecuteCommand(et.id, {
    alignType: _e.RIGHT
  })
}, mo = {
  id: "doc.command.align-justify",
  type: N.COMMAND,
  handler: (n) => n.get(y).syncExecuteCommand(et.id, {
    alignType: _e.JUSTIFIED
  })
}, Nl = {
  id: Vt.id,
  binding: j.B | K.CTRL_COMMAND,
  preconditions: de
}, Ql = {
  id: jt.id,
  binding: j.I | K.CTRL_COMMAND,
  preconditions: de
}, Ul = {
  id: Wt.id,
  binding: j.U | K.CTRL_COMMAND,
  preconditions: de
}, Ll = {
  id: zt.id,
  binding: j.X | K.SHIFT | K.CTRL_COMMAND,
  preconditions: de
}, Fl = {
  id: Ct.id,
  binding: j.COMMA | K.CTRL_COMMAND,
  preconditions: de
}, Hl = {
  id: Gt.id,
  binding: j.PERIOD | K.CTRL_COMMAND,
  preconditions: de
}, kl = {
  id: go.id,
  binding: j.L | K.CTRL_COMMAND | K.SHIFT,
  preconditions: de
}, Vl = {
  id: po.id,
  binding: j.R | K.CTRL_COMMAND | K.SHIFT,
  preconditions: de
}, jl = {
  id: fo.id,
  binding: j.E | K.CTRL_COMMAND | K.SHIFT,
  preconditions: de
}, Wl = {
  id: mo.id,
  binding: j.J | K.CTRL_COMMAND | K.SHIFT,
  preconditions: de
}, zl = {
  id: ho.id,
  binding: j.Digit7 | K.CTRL_COMMAND | K.SHIFT,
  preconditions: de
}, Gl = {
  id: uo.id,
  binding: j.Digit8 | K.CTRL_COMMAND | K.SHIFT,
  preconditions: de
}, Yl = "univer-doc-count-bar", ql = {
  docCountBar: Yl
}, Kl = (n, e) => {
  const t = n.get(Q).getUniverDocInstance(e.unitId), o = (t == null ? void 0 : t.zoomRatio) || 1;
  return {
    ...X.deepClone(e),
    zoomRatio: o
  };
}, Ye = {
  id: "doc.operation.set-zoom-ratio",
  type: N.OPERATION,
  handler: (n, e) => {
    const t = n.get(Q).getUniverDocInstance(e.unitId);
    if (!t)
      return !1;
    const o = t.getSnapshot();
    return o.settings == null ? o.settings = {
      zoomRatio: e.zoomRatio
    } : o.settings.zoomRatio = e.zoomRatio, !0;
  }
}, Xl = [50, 80, 100, 130, 150, 170, 200, 400], Jl = [10, 400];
function Zl() {
  const n = $(y), e = $(Q), t = Fe(() => e.getCurrentTypeOfUnit$(_.UNIVER_DOC), []), o = Nn(t), s = Li(() => {
    var A, l;
    if (!o) return 100;
    const c = ((l = (A = o.getSettings()) == null ? void 0 : A.zoomRatio) != null ? l : 1) * 100;
    return Math.round(c);
  }, [o]), [r, i] = ve(() => s());
  Re(() => (i(s()), n.onCommandExecuted((A) => {
    if (A.id === Ye.id) {
      const l = s();
      i(l);
    }
  }).dispose), [n, s]);
  function a(c) {
    if (i(c), o == null)
      return;
    const A = c / 100;
    n.executeCommand(Ye.id, {
      unitId: o.getUnitId(),
      zoomRatio: A
    });
  }
  return /* @__PURE__ */ w.jsx(
    Kc,
    {
      min: Jl[0],
      value: r,
      shortcuts: Xl,
      onChange: a
    }
  );
}
function $l(n) {
  return /* @__PURE__ */ w.jsx("section", { className: ql.docCountBar, children: /* @__PURE__ */ w.jsx(Zl, {}) });
}
const ed = "univer-doc-footer-container", td = {
  docFooterContainer: ed
}, nd = () => /* @__PURE__ */ w.jsxs("div", { className: td.docFooterContainer, children: [
  /* @__PURE__ */ w.jsx("div", {}),
  /* @__PURE__ */ w.jsx($l, {})
] }), Us = "docs-ui.config", qr = {
  layout: {
    docContainerConfig: sA,
    toolbarConfig: oA
  }
};
var Eo = /* @__PURE__ */ ((n) => (n[n.ABOVE = 0] = "ABOVE", n[n.BELLOW = 1] = "BELLOW", n))(Eo || {}), Ls = /* @__PURE__ */ ((n) => (n[n.LEFT = 0] = "LEFT", n[n.RIGHT = 1] = "RIGHT", n))(Ls || {});
function od(n, e) {
  let t = U.TABLE_START;
  const o = [], s = [];
  for (let r = 0; r < n; r++) {
    t += U.TABLE_ROW_START;
    for (let i = 0; i < e; i++)
      t += `${U.TABLE_CELL_START}\r
${U.TABLE_CELL_END}`, o.push({
        startIndex: t.length - 3,
        paragraphStyle: {
          spaceAbove: { v: 3 },
          lineSpacing: 2,
          spaceBelow: { v: 0 }
        }
      }), s.push({
        startIndex: t.length - 2
      });
    t += U.TABLE_ROW_END;
  }
  return t += U.TABLE_END, {
    dataStream: t,
    paragraphs: o,
    sectionBreaks: s
  };
}
function Fs() {
  return {
    margin: {
      start: {
        v: 10
      },
      end: {
        v: 10
      },
      top: {
        v: 5
      },
      bottom: {
        v: 5
      }
    }
  };
}
function Hs(n) {
  const e = Fs();
  return {
    tableCells: [...new Array(n).fill(null).map(() => X.deepClone(e))],
    trHeight: {
      val: { v: 30 },
      hRule: Ya.AUTO
    }
  };
}
function ks(n) {
  return {
    size: {
      type: Si.SPECIFIED,
      width: {
        v: n
      }
    }
  };
}
function ua(n, e, t) {
  const o = ks(t / e), s = Hs(e), r = [...new Array(n).fill(null).map(() => X.deepClone(s))], i = [...new Array(e).fill(null).map(() => X.deepClone(o))], a = pt(6);
  return {
    tableRows: r,
    tableColumns: i,
    tableId: a,
    align: qa.START,
    indent: {
      v: 0
    },
    textWrap: Ka.NONE,
    position: {
      positionH: {
        relativeFrom: $n.PAGE,
        posOffset: 0
      },
      positionV: {
        relativeFrom: ot.PAGE,
        posOffset: 0
      }
    },
    dist: {
      distB: 0,
      distL: 0,
      distR: 0,
      distT: 0
    },
    cellMargin: {
      start: {
        v: 10
      },
      end: {
        v: 10
      },
      top: {
        v: 5
      },
      bottom: {
        v: 5
      }
    },
    size: {
      type: Si.UNSPECIFIED,
      width: {
        v: t
      }
    }
  };
}
function En(n, e) {
  if (!n && !e)
    return null;
  if (e && e.length > 0) {
    let t = Number.POSITIVE_INFINITY, o = Number.NEGATIVE_INFINITY;
    const s = "";
    for (const r of e) {
      const { startOffset: i, endOffset: a, segmentId: c } = r;
      i == null || a == null || c == null || (t = Math.min(t, i), o = Math.max(o, a));
    }
    if (Number.isFinite(t) && Number.isFinite(o))
      return {
        startOffset: t,
        endOffset: o,
        segmentId: s
      };
  } else if (n) {
    const { startOffset: t, endOffset: o, segmentId: s } = n;
    return t == null || o == null || s == null ? null : {
      startOffset: t,
      endOffset: o,
      segmentId: s
    };
  }
}
function sd(n) {
  let e = U.TABLE_ROW_START;
  const t = [], o = [];
  for (let s = 0; s < n; s++)
    e += `${U.TABLE_CELL_START}\r
${U.TABLE_CELL_END}`, t.push({
      startIndex: e.length - 3,
      paragraphStyle: {
        spaceAbove: { v: 3 },
        lineSpacing: 2,
        spaceBelow: { v: 0 }
      }
    }), o.push({
      startIndex: e.length - 2
    });
  return e += U.TABLE_ROW_END, {
    dataStream: e,
    paragraphs: t,
    sectionBreaks: o
  };
}
function rd() {
  const n = `${U.TABLE_CELL_START}\r
${U.TABLE_CELL_END}`, e = [], t = [];
  return e.push({
    startIndex: 1,
    paragraphStyle: {
      spaceAbove: { v: 3 },
      lineSpacing: 2,
      spaceBelow: { v: 0 }
    }
  }), t.push({
    startIndex: 2
  }), {
    dataStream: n,
    paragraphs: e,
    sectionBreaks: t
  };
}
function id(n, e, t) {
  var d, h, u;
  const { startOffset: o, endOffset: s, segmentId: r } = n, i = t.getSelfOrHeaderFooterViewModel(r), a = e === 0 ? o : s;
  let c = null;
  const A = (u = (h = (d = t.getBody()) == null ? void 0 : d.tables) == null ? void 0 : h.find((g) => a >= g.startIndex && a <= g.endIndex)) == null ? void 0 : u.tableId;
  let l = 0;
  for (const g of i.getChildren()) {
    for (const f of g.children) {
      const { children: p } = f, m = p[0];
      if (m) {
        for (const E of m.children)
          if (E.startIndex <= a && a <= E.endIndex) {
            l = m.children.indexOf(E), c = E;
            break;
          }
      }
      if (c)
        break;
    }
    if (c)
      break;
  }
  return c == null || A == null ? null : {
    offset: e === 0 ? c.startIndex : c.endIndex + 1,
    colCount: c.children.length,
    tableId: A,
    insertRowIndex: e === 0 ? l : l + 1
  };
}
function ad(n, e, t) {
  var u, g, f;
  const { startOffset: o, endOffset: s, segmentId: r } = n, i = t.getSelfOrHeaderFooterViewModel(r), a = e === 0 ? o : s, c = (f = (g = (u = t.getBody()) == null ? void 0 : u.tables) == null ? void 0 : g.find((p) => a >= p.startIndex && a <= p.endIndex)) == null ? void 0 : f.tableId, A = [];
  let l = null, d = -1;
  for (const p of i.getChildren()) {
    for (const m of p.children) {
      const { children: E } = m, I = E[0];
      if (I) {
        if (a < I.startIndex || a > I.endIndex)
          continue;
        l = I;
        for (const v of I.children) {
          for (const R of v.children) {
            const S = v.children.indexOf(R);
            if (a >= R.startIndex && a <= R.endIndex) {
              d = S;
              break;
            }
          }
          if (d !== -1)
            break;
        }
      }
      if (l)
        break;
    }
    if (l)
      break;
  }
  if (l == null || c == null || d === -1)
    return null;
  let h = 0;
  for (const p of l.children) {
    const m = p.children[d], E = e === 0 ? m.startIndex : m.endIndex + 1;
    A.push(E - h), h = E;
  }
  return {
    offsets: A,
    tableId: c,
    columnIndex: d,
    rowCount: l.children.length
  };
}
function cd(n, e, t) {
  const o = [];
  let s = e[t].size.width.v, r = 0;
  for (let i = 0; i < e.length; i++)
    r += e[i].size.width.v;
  r += s;
  for (let i = 0; i < e.length; i++)
    o.push(e[i].size.width.v / r * n);
  return s = s / r * n, {
    widths: o,
    newColWidth: s
  };
}
function ha(n, e) {
  var h, u, g;
  const { startOffset: t, endOffset: o, segmentId: s } = n, r = e.getSelfOrHeaderFooterViewModel(s), i = (g = (u = (h = e.getBody()) == null ? void 0 : h.tables) == null ? void 0 : u.find((f) => t >= f.startIndex && o <= f.endIndex)) == null ? void 0 : g.tableId, a = [];
  let c = -1, A = 0, l = -1, d = !1;
  for (const f of r.getChildren()) {
    for (const p of f.children) {
      const { children: m } = p, E = m[0];
      if (E) {
        if (t < E.startIndex || o > E.endIndex)
          continue;
        l = E.startIndex + 3;
        for (const I of E.children) {
          const v = E.children.indexOf(I), { startIndex: R, endIndex: S } = I;
          t >= R && t <= S ? (c = R, a.push(v), A += S - R + 1) : (R > t && S < o || o >= R && o <= S) && (a.push(v), A += S - R + 1), a.length === E.children.length && (d = !0);
        }
      }
      if (a.length)
        break;
    }
    if (a.length)
      break;
  }
  return i == null || a.length === 0 ? null : {
    tableId: i,
    rowIndexes: a,
    offset: c,
    len: A,
    cursor: l,
    selectWholeTable: d
  };
}
function Ad(n, e) {
  var g, f, p;
  const { startOffset: t, endOffset: o, segmentId: s } = n, r = e.getSelfOrHeaderFooterViewModel(s), i = (p = (f = (g = e.getBody()) == null ? void 0 : g.tables) == null ? void 0 : f.find((m) => t >= m.startIndex && o <= m.endIndex)) == null ? void 0 : p.tableId, a = [];
  let c = null;
  const A = [];
  let l = -1, d = -1, h = -1;
  for (const m of r.getChildren()) {
    for (const E of m.children) {
      const { children: I } = E, v = I[0];
      if (v) {
        if (t < v.startIndex || o > v.endIndex)
          continue;
        c = v;
        for (const R of v.children)
          for (const S of R.children) {
            const C = R.children.indexOf(S);
            t >= S.startIndex && t <= S.endIndex && (d = C), o >= S.startIndex && o <= S.endIndex && (h = C);
          }
      }
      if (c)
        break;
    }
    if (c)
      break;
  }
  if (c == null || i == null)
    return null;
  for (let m = d; m <= h; m++)
    A.push(m);
  let u = 0;
  for (const m of c.children) {
    const E = m.children[d], I = m.children[h];
    a.push({
      retain: E.startIndex - u,
      delete: I.endIndex - E.startIndex + 1
    }), u = I.endIndex + 1;
  }
  return l = c.startIndex + 3, {
    offsets: a,
    tableId: i,
    columnIndexes: A,
    cursor: l,
    selectWholeTable: A.length === c.children[0].children.length,
    rowCount: c.children.length
  };
}
function ga(n, e) {
  var l, d, h;
  const { startOffset: t, endOffset: o, segmentId: s } = n, r = e.getSelfOrHeaderFooterViewModel(s), i = (h = (d = (l = e.getBody()) == null ? void 0 : l.tables) == null ? void 0 : d.find((u) => t >= u.startIndex && o <= u.endIndex)) == null ? void 0 : h.tableId;
  let a = -1, c = 0, A = -1;
  for (const u of r.getChildren()) {
    for (const g of u.children) {
      const { children: f } = g, p = f[0];
      if (p) {
        if (t < p.startIndex || o > p.endIndex)
          continue;
        a = p.startIndex, c = p.endIndex - p.startIndex + 1, A = p.startIndex;
      }
      if (p)
        break;
    }
    if (c > 0)
      break;
  }
  return i == null ? null : {
    tableId: i,
    offset: a,
    len: c,
    cursor: A
  };
}
function ld(n, e) {
  var g, f, p;
  const { startOffset: t, endOffset: o, segmentId: s } = n, r = e.getSelfOrHeaderFooterViewModel(s), i = (p = (f = (g = e.getBody()) == null ? void 0 : g.tables) == null ? void 0 : f.find((m) => t >= m.startIndex && o <= m.endIndex)) == null ? void 0 : p.tableId, a = [];
  let c = null, A = -1, l = -1, d = -1, h = -1;
  for (const m of r.getChildren()) {
    for (const E of m.children) {
      const { children: I } = E, v = I[0];
      if (v) {
        if (t < v.startIndex || o > v.endIndex)
          continue;
        c = v;
        for (const R of v.children) {
          const S = v.children.indexOf(R);
          for (const C of R.children) {
            const T = R.children.indexOf(C);
            t >= C.startIndex && t <= C.endIndex && (l = S, d = T), o >= C.startIndex && o <= C.endIndex && (h = T);
          }
        }
      }
      if (c)
        break;
    }
    if (c)
      break;
  }
  if (c == null || i == null || l === -1)
    return null;
  const u = c.children[l];
  for (let m = d; m <= h; m++) {
    const E = u.children[m];
    a.push({
      retain: E.startIndex + 1,
      delete: E.endIndex - E.startIndex - 3
    });
  }
  return A = c.startIndex + 3, {
    offsets: a,
    tableId: i,
    cursor: A,
    rowCount: c.children.length
  };
}
var ts = /* @__PURE__ */ ((n) => (n[n.NEXT = 0] = "NEXT", n[n.PREV = 1] = "PREV", n))(ts || {});
function Kr(n, e, t) {
  const { startOffset: o } = e;
  let s = null;
  for (const A of n.getChildren()) {
    for (const l of A.children) {
      const d = l.children[0];
      if (d && o > d.startIndex && o < d.endIndex) {
        s = d;
        break;
      }
    }
    if (s)
      break;
  }
  if (s == null)
    return null;
  let r = -1, i = -1, a = null;
  for (const A of s.children) {
    for (const l of A.children)
      if (o > l.startIndex && o < l.endIndex) {
        r = A.children.indexOf(l), i = s.children.indexOf(A), a = A;
        break;
      }
    if (r > -1)
      break;
  }
  if (r === -1 || i === -1 || a == null)
    return null;
  let c = null;
  if (t === 0) {
    if (c = a.children[r + 1], !c) {
      const A = s.children[i + 1];
      A && (c = A.children[0]);
    }
  } else if (c = a.children[r - 1], !c) {
    const A = s.children[i - 1];
    A && (c = A.children[A.children.length - 1]);
  }
  if (c) {
    const { startIndex: A, endIndex: l } = c;
    return {
      startOffset: A + 1,
      endOffset: l - 2
    };
  }
}
function dd(n, e) {
  const t = [], { customBlocks: o = [] } = n;
  for (const s of e) {
    const { startOffset: r, endOffset: i } = s;
    if (!(r == null || i == null))
      for (const a of o) {
        const { startIndex: c } = a;
        c >= r && c < i && t.push(a.blockId);
      }
  }
  return t;
}
function ud(n) {
  return n.some((e) => {
    const { startNodePosition: t } = e;
    return t ? (t == null ? void 0 : t.path.indexOf("cells")) > -1 : !1;
  });
}
const hd = Is, fa = {
  id: "doc.command.inner-paste",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function, complexity
  handler: async (n, e) => {
    var O, P, b, B, M, H;
    const { segmentId: t, textRanges: o, doc: s } = e, r = n.get(y), i = n.get(G), a = n.get(Q), c = i.getTextRanges(), A = i.getRectRanges(), { body: l, tableSource: d, drawings: h } = s;
    if (!Array.isArray(c) || c.length === 0 || l == null)
      return !1;
    const u = a.getCurrentUniverDocInstance(), g = u == null ? void 0 : u.getSelfOrHeaderFooterModel(t).getBody();
    if (u == null || g == null)
      return !1;
    const f = u.getUnitId(), p = {
      id: J.id,
      params: {
        unitId: f,
        actions: [],
        textRanges: o,
        segmentId: t
      }
    }, m = new St();
    m.reset();
    const E = new me(), I = k.getInstance(), v = [], R = !!((O = l.tables) != null && O.length), S = !!((P = l.customBlocks) != null && P.length);
    if (R && t || R && ud(c) || c.length && (A != null && A.length))
      return !1;
    for (let F = 0; F < c.length; F++) {
      const D = c[F], { startOffset: te, endOffset: q, collapsed: V } = D, Y = te - m.cursor, oe = X.deepClone(l);
      if (R)
        for (const Ae of oe.tables) {
          const { tableId: ne } = Ae, ae = X.generateRandomId(6);
          Ae.tableId = ae;
          const Te = X.deepClone(d[ne]);
          Te.tableId = ae;
          const je = I.insertOp(["tableSource", ae], Te);
          v.push(je);
        }
      if (S && h) {
        const Ae = (B = (b = u.getSnapshot().drawingsOrder) == null ? void 0 : b.length) != null ? B : 0;
        for (const ne of oe.customBlocks) {
          const { blockId: ae } = ne, Te = X.generateRandomId(6);
          ne.blockId = Te;
          const je = X.deepClone(h[ae]);
          je.drawingId = Te;
          const ut = I.insertOp(["drawings", Te], je), we = I.insertOp(["drawingsOrder", Ae], Te);
          v.push(ut), v.push(we);
        }
      }
      const ce = Os((M = g.customRanges) != null ? M : [], q, hd.includes(f)), he = Ts((H = g.customDecorations) != null ? H : [], q);
      if (ce && (oe.customRanges = [{
        ...ce,
        startIndex: 0,
        endIndex: l.dataStream.length - 1
      }]), he.length && (oe.customDecorations = he.map((Ae) => ({
        ...Ae,
        startIndex: 0,
        endIndex: l.dataStream.length - 1
      }))), V)
        E.push({
          t: W.RETAIN,
          len: Y
        }), E.push({
          t: W.INSERT,
          body: oe,
          len: l.dataStream.length
        });
      else {
        const Ae = Ce.selection.delete([D], l, m.cursor, oe, c.length === 1);
        E.push(...Ae);
      }
      m.reset(), m.moveCursor(q);
    }
    const C = le(u, t);
    return v.push(I.editOp(E.serialize(), C)), p.params.actions = v.reduce((F, D) => k.compose(F, D), null), !!r.syncExecuteCommand(p.id, p.params);
  }
};
function gd(n, e) {
  const { startOffset: t, endOffset: o } = n, s = e.some((i) => i.startIndex === o), r = Math.max(t, s ? o - 1 : o);
  return {
    ...n,
    endOffset: r,
    collapsed: t === r
  };
}
function fd(n, e, t) {
  var g, f;
  const o = e.getSelfOrHeaderFooterModel(t).getBody(), s = new me(), r = k.getInstance(), i = [];
  if (o == null)
    return i;
  const { tables: a = [] } = o, c = new St();
  c.reset();
  for (let p = 0; p < n.length; p++) {
    const m = gd(n[p], a), { startOffset: E, endOffset: I, collapsed: v } = m, R = E - c.cursor;
    v ? s.push({
      t: W.RETAIN,
      len: R
    }) : s.push(...Ce.selection.delete([m], o, c.cursor, null, !1)), c.reset(), c.moveCursor(I);
  }
  const A = le(e, t);
  i.push(r.editOp(s.serialize(), A));
  const l = dd(o, n), d = (g = e.getDrawings()) != null ? g : {}, h = (f = e.getDrawingsOrder()) != null ? f : [], u = l.sort((p, m) => h.indexOf(p) > h.indexOf(m) ? -1 : h.indexOf(p) < h.indexOf(m) ? 1 : 0);
  if (u.length > 0)
    for (const p of u) {
      const m = d[p], E = h.indexOf(p);
      if (m == null || E < 0)
        continue;
      const I = r.removeOp(["drawings", p], m), v = r.removeOp(["drawingsOrder", E], p);
      i.push(I), i.push(v);
    }
  return i.reduce((p, m) => k.compose(p, m), null);
}
function pd(n, e, t, o) {
  const s = [];
  if (e.getSelfOrHeaderFooterModel(o).getBody() == null)
    return s;
  const i = new me(), a = k.getInstance(), c = new St();
  c.reset();
  for (const l of n) {
    const { startOffset: d, endOffset: h, spanEntireRow: u, spanEntireTable: g } = l;
    if (!(d == null || h == null))
      if (g) {
        const f = ga({ startOffset: d, endOffset: h, segmentId: o }, t);
        if (f == null)
          continue;
        const { offset: p, len: m, tableId: E } = f;
        p - c.cursor > 0 && i.push({
          t: W.RETAIN,
          len: p - c.cursor
        }), i.push({
          t: W.DELETE,
          len: m
        });
        const I = a.removeOp(["tableSource", E]);
        s.push(I), c.moveCursorTo(p + m);
      } else if (u) {
        const f = ha({ startOffset: d, endOffset: h, segmentId: o }, t);
        if (f == null)
          continue;
        const { offset: p, rowIndexes: m, len: E, tableId: I } = f;
        p - c.cursor > 0 && i.push({
          t: W.RETAIN,
          len: p - c.cursor
        }), i.push({
          t: W.DELETE,
          len: E
        });
        for (const v of m.reverse()) {
          const R = a.removeOp(["tableSource", I, "tableRows", v]);
          s.push(R);
        }
        c.moveCursorTo(p + E);
      } else {
        const f = ld({ startOffset: d, endOffset: h, segmentId: o }, t);
        if (f == null)
          continue;
        const { offsets: p } = f;
        for (const m of p) {
          const { retain: E, delete: I } = m;
          E - c.cursor > 0 && i.push({
            t: W.RETAIN,
            len: E - c.cursor
          }), i.push({
            t: W.DELETE,
            len: I
          }), c.moveCursorTo(E + I);
        }
      }
  }
  const A = le(e, o);
  return s.push(a.editOp(i.serialize(), A)), s.reduce((l, d) => k.compose(l, d), null);
}
function md(n, e, t, o, s) {
  let r = [];
  if (Array.isArray(n) && (n == null ? void 0 : n.length) !== 0 && (r = fd(n, t, s)), Array.isArray(e) && (e == null ? void 0 : e.length) !== 0) {
    const i = pd(e, t, o, s);
    r == null || r.length === 0 ? r = i : r = k.compose(
      r,
      k.transform(i, r, "right")
    );
  }
  return r;
}
const Qt = {
  id: "doc.command.inner-cut",
  type: N.COMMAND,
  handler: async (n, e) => {
    var f, p;
    const { segmentId: t, textRanges: o } = e, s = n.get(y), r = n.get(G), i = n.get(Q), a = (f = e.selections) != null ? f : r.getTextRanges(), c = r.getRectRanges();
    if ((!Array.isArray(a) || a.length === 0) && (!Array.isArray(c) || c.length === 0))
      return !1;
    const A = (p = i.getCurrentUniverDocInstance()) == null ? void 0 : p.getUnitId();
    if (!A)
      return !1;
    const l = i.getUniverDocInstance(A);
    if (l == null)
      return !1;
    const d = ke(n, A);
    if (d == null)
      return !1;
    const h = d.getViewModel(), u = {
      id: J.id,
      params: {
        unitId: A,
        actions: [],
        textRanges: o
      }
    };
    return u.params.actions = md(a, c, l, h, t), !!s.syncExecuteCommand(u.id, u.params);
  }
};
var Be = /* @__PURE__ */ ((n) => (n[n.LEFT = 0] = "LEFT", n[n.RIGHT = 1] = "RIGHT", n))(Be || {});
const Ed = "doc.command.insert-text", Vs = {
  id: Ed,
  type: N.COMMAND,
  handler: async (n, e) => {
    var S;
    const t = n.get(y), { range: o, segmentId: s, body: r, unitId: i, cursorOffset: a } = e, c = n.get(G), l = n.get(Q).getUnit(i, _.UNIVER_DOC);
    if (l == null)
      return !1;
    const d = c.getActiveTextRange(), h = l.getSelfOrHeaderFooterModel((S = d == null ? void 0 : d.segmentId) != null ? S : "").getBody();
    if (h == null)
      return !1;
    const { startOffset: u, collapsed: g } = o, f = a != null ? a : r.dataStream.length, p = [
      {
        startOffset: u + f,
        endOffset: u + f,
        style: d == null ? void 0 : d.style,
        collapsed: g
      }
    ], m = {
      id: J.id,
      params: {
        unitId: i,
        actions: [],
        textRanges: p,
        debounce: !0
      }
    }, E = new me(), I = k.getInstance();
    if (g)
      u > 0 && E.push({
        t: W.RETAIN,
        len: u
      }), E.push({
        t: W.INSERT,
        body: r,
        len: r.dataStream.length
      });
    else {
      const C = Ce.selection.delete([o], h, 0, r);
      E.push(...C);
    }
    m.params.textRanges = [{
      startOffset: u + f,
      endOffset: u + f,
      collapsed: g
    }];
    const v = le(l, s);
    return m.params.actions = I.editOp(E.serialize(), v), !!t.syncExecuteCommand(m.id, m.params);
  }
}, dn = {
  id: "doc.command.delete-text",
  type: N.COMMAND,
  handler: async (n, e) => {
    var R;
    const t = n.get(y), o = n.get(Q), { range: s, segmentId: r, unitId: i, direction: a, len: c = 1 } = e, A = o.getUnit(i, _.UNIVER_DOC), l = A == null ? void 0 : A.getSelfOrHeaderFooterModel(r).getBody();
    if (A == null || l == null)
      return !1;
    const { startOffset: d } = s;
    let h = a === Be.LEFT ? d - c : d, u = a === Be.LEFT ? d - 1 : d + c - 1;
    const g = (R = l.customRanges) == null ? void 0 : R.find((S) => S.startIndex <= h && S.endIndex >= u);
    g != null && g.wholeEntity && (h = g.startIndex, u = Math.max(u, g.endIndex));
    const f = {
      id: J.id,
      params: {
        unitId: i,
        actions: [],
        textRanges: [{
          startOffset: h,
          endOffset: h,
          collapsed: !0
        }],
        debounce: !0
      }
    }, p = new me(), m = k.getInstance();
    p.push({
      t: W.RETAIN,
      len: h - 0
    }), p.push({
      t: W.DELETE,
      len: u - h + 1
    });
    const I = le(A, r);
    return f.params.actions = m.editOp(p.serialize(), I), !!t.syncExecuteCommand(f.id, f.params);
  }
}, pa = {
  id: "doc.command.update-text",
  type: N.COMMAND,
  handler: async (n, e) => {
    const { range: t, segmentId: o, updateBody: s, coverType: r, unitId: i, textRanges: a } = e, c = n.get(y), l = n.get(Q).getCurrentUniverDocInstance();
    if (l == null)
      return !1;
    const d = {
      id: J.id,
      params: {
        unitId: i,
        actions: [],
        textRanges: a
      }
    }, h = new me(), u = k.getInstance(), { startOffset: g, endOffset: f } = t;
    h.push({
      t: W.RETAIN,
      len: g
    }), h.push({
      t: W.RETAIN,
      body: s,
      len: f - g,
      coverType: r
    });
    const p = le(l, o);
    return d.params.actions = u.editOp(h.serialize(), p), !!c.syncExecuteCommand(d.id, d.params);
  }
}, js = {
  id: "doc.command.delete-custom-block",
  type: N.COMMAND,
  handler: async (n, e) => {
    var b;
    const t = n.get(G), o = n.get(Q), s = n.get(y), r = t.getActiveTextRange(), i = o.getCurrentUniverDocInstance();
    if (r == null || i == null)
      return !1;
    const { direction: a, range: c, unitId: A, drawingId: l } = e, { startOffset: d, segmentId: h, style: u } = r, g = a === Be.LEFT ? d - 1 : d, f = [
      {
        startOffset: g,
        endOffset: g,
        style: u
      }
    ], p = {
      id: J.id,
      params: {
        unitId: A,
        actions: [],
        textRanges: f,
        prevTextRanges: [c]
      }
    }, m = new me(), E = k.getInstance(), I = [];
    d > 0 && m.push({
      t: W.RETAIN,
      len: a === Be.LEFT ? d - 1 : d
    }), m.push({
      t: W.DELETE,
      len: 1
    });
    const v = le(i, h);
    I.push(E.editOp(m.serialize(), v));
    const R = ((b = i.getDrawings()) != null ? b : {})[l], C = i.getDrawingsOrder().indexOf(l), T = E.removeOp(["drawings", l], R), O = E.removeOp(["drawingsOrder", C], l);
    return I.push(T), I.push(O), p.params.actions = I.reduce((B, M) => k.compose(B, M), null), !!s.syncExecuteCommand(p.id, p.params);
  }
}, Ws = {
  id: "doc.command.merge-two-paragraph",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n, e) => {
    const t = n.get(G), o = n.get(Q), s = n.get(y), { direction: r, range: i } = e, a = t.getActiveTextRange(), c = t.getTextRanges();
    if (a == null || c == null)
      return !1;
    const { segmentId: A, style: l } = a, d = o.getCurrentUnitForType(_.UNIVER_DOC), h = d == null ? void 0 : d.getSelfOrHeaderFooterModel(A).getBody();
    if (d == null || h == null)
      return !1;
    const u = a, g = d.getUnitId(), { startOffset: f, collapsed: p } = u;
    if (!p)
      return !1;
    const m = r === Be.LEFT ? f : f + 1;
    let E, I;
    for (const b of h.paragraphs) {
      if (b.startIndex >= m) {
        I = b;
        break;
      }
      E = b;
    }
    if (E == null || I == null)
      return !1;
    const v = r === Be.LEFT ? f - 1 : f, R = [
      {
        startOffset: v,
        endOffset: v,
        style: l
      }
    ], S = {
      id: J.id,
      params: {
        unitId: g,
        actions: [],
        textRanges: R,
        prevTextRanges: [i]
      }
    }, C = new me(), T = k.getInstance();
    E.startIndex > 0 && C.push({
      t: W.RETAIN,
      len: E.startIndex
    }), C.push({
      t: W.DELETE,
      len: 1
    }), I.startIndex > E.startIndex + 1 && C.push({
      t: W.RETAIN,
      len: I.startIndex - E.startIndex - 1
    }), C.push({
      t: W.RETAIN,
      len: 1,
      coverType: no.REPLACE,
      body: {
        dataStream: "",
        paragraphs: [
          {
            ...X.deepClone(E),
            startIndex: 0
          }
        ]
      }
    });
    const O = le(d, A);
    return S.params.actions = T.editOp(C.serialize(), O), !!s.syncExecuteCommand(S.id, S.params);
  }
};
function zs(n, e) {
  let t = 0;
  if (n == null || n.length === 0) {
    if (typeof e[0].startOffset == "number") {
      const o = e[0], { spanEntireRow: s, spanEntireTable: r } = o;
      r ? t = o.startOffset - 3 : s ? o.startRow > 0 ? t = o.startOffset - 6 : t = o.startOffset : t = e[0].startOffset;
    }
  } else if (n.length > 0 && e.length > 0) {
    const o = n[0], s = e[0];
    if (o.startOffset != null && s.startOffset != null) {
      if (o.startOffset < s.startOffset)
        t = o.startOffset;
      else if (o.startOffset >= s.startOffset) {
        const { spanEntireRow: r, spanEntireTable: i } = s;
        i ? t = s.startOffset - 3 : r && (t = s.startOffset - 6);
      }
    }
  }
  return t;
}
const So = {
  id: "doc.command.delete-left",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function, complexity
  handler: async (n) => {
    var O, P;
    const e = n.get(G), t = n.get(Q), o = n.get(y);
    let s = !0;
    const r = t.getCurrentUniverDocInstance();
    if (r == null)
      return !1;
    const i = r.getUnitId(), a = ke(n, i), c = e.getActiveTextRange(), A = e.getRectRanges(), l = e.getTextRanges(), d = a == null ? void 0 : a.getSkeleton();
    if (d == null)
      return !1;
    if (A != null && A.length) {
      const b = zs(l, A), B = A[0].segmentId, M = [
        {
          startOffset: b,
          endOffset: b
        }
      ];
      return o.executeCommand(Qt.id, {
        segmentId: B,
        textRanges: M
      });
    }
    if (c == null || l == null)
      return !1;
    const { segmentId: h, style: u, segmentPage: g } = c, f = r.getSelfOrHeaderFooterModel(h).getBody();
    if (f == null)
      return !1;
    const p = c, { startOffset: m, collapsed: E } = p, I = d.findNodeByCharIndex(m, h, g), v = hc(I), R = gc(I, f);
    let S = m;
    const C = d.findNodeByCharIndex(m - 1, h, g);
    if (fc(I) && C !== I && (v === !0 || R === !0) && E) {
      const b = pc(I, f);
      if (b == null)
        return !1;
      const B = b == null ? void 0 : b.startIndex, M = { startIndex: 0 }, H = b.paragraphStyle;
      if (v === !0) {
        const D = b.paragraphStyle;
        if (D) {
          M.paragraphStyle = D;
          const { hanging: te } = D;
          te && (M.paragraphStyle.indentStart = te, M.paragraphStyle.hanging = void 0);
        }
      } else if (R === !0) {
        const D = b.bullet;
        D && (M.bullet = D), H != null && (M.paragraphStyle = { ...H }, delete M.paragraphStyle.hanging, delete M.paragraphStyle.indentStart);
      }
      const F = [
        {
          startOffset: S,
          endOffset: S,
          style: u
        }
      ];
      s = await o.executeCommand(pa.id, {
        unitId: r.getUnitId(),
        updateBody: {
          dataStream: "",
          paragraphs: [{ ...M }]
        },
        range: {
          startOffset: B,
          endOffset: B + 1
        },
        textRanges: F,
        coverType: no.REPLACE,
        segmentId: h
      });
    } else if (E === !0) {
      if (C == null)
        return !0;
      if (C.content === "\r")
        s = await o.executeCommand(Ws.id, {
          direction: Be.LEFT,
          range: p
        });
      else if (C.streamType === "\b") {
        const b = (P = r.getSnapshot().drawings) == null ? void 0 : P[(O = C.drawingId) != null ? O : ""];
        if (b == null)
          return !0;
        if (b.layoutType === oo.INLINE) {
          const M = r.getUnitId();
          s = await o.executeCommand(js.id, {
            direction: Be.LEFT,
            range: c,
            unitId: M,
            drawingId: C.drawingId
          });
        } else {
          const M = d.findNodeByCharIndex(m - 2);
          if (M == null)
            return !0;
          S -= C.count, S -= M.count;
          const H = [
            {
              startOffset: S,
              endOffset: S,
              style: u
            }
          ];
          s = await o.executeCommand(dn.id, {
            unitId: r.getUnitId(),
            range: {
              ...c,
              startOffset: c.startOffset - 1,
              endOffset: c.endOffset - 1
            },
            segmentId: h,
            direction: Be.LEFT,
            len: M.count,
            textRanges: H
          });
        }
      } else
        S -= C.count, s = await o.executeCommand(dn.id, {
          unitId: r.getUnitId(),
          range: p,
          segmentId: h,
          direction: Be.LEFT,
          len: C.count
        });
    } else {
      const b = Ea(p, [p]);
      s = await o.executeCommand(Qt.id, {
        segmentId: h,
        textRanges: b,
        selections: [p]
      });
    }
    return s;
  }
}, ma = {
  id: "doc.command.delete-right",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function, complexity
  handler: async (n) => {
    var I, v;
    const e = n.get(G), o = n.get(Q).getCurrentUniverDocInstance();
    if (!o)
      return !1;
    const s = ke(n, o.getUnitId()), r = n.get(y), i = e.getActiveTextRange(), a = e.getRectRanges(), c = e.getTextRanges(), A = s == null ? void 0 : s.getSkeleton();
    if (a != null && a.length) {
      const R = zs(c, a), S = a[0].segmentId, C = [
        {
          startOffset: R,
          endOffset: R
        }
      ];
      return r.executeCommand(Qt.id, {
        segmentId: S,
        textRanges: C
      });
    }
    if (i == null || A == null || c == null)
      return !1;
    const { segmentId: l, style: d, segmentPage: h } = i, u = o == null ? void 0 : o.getSelfOrHeaderFooterModel(l).getBody();
    if (!o || !u)
      return !1;
    const g = i, { startOffset: f, endOffset: p, collapsed: m } = g;
    if (f === u.dataStream.length - 2 && m)
      return !0;
    let E = !1;
    if (m === !0) {
      const R = A.findNodeByCharIndex(f, l, h), S = A.findNodeByCharIndex(f + 1);
      if (R.streamType === U.PARAGRAPH && (S == null ? void 0 : S.streamType) === U.SECTION_BREAK)
        return !1;
      if (R.content === "\r")
        E = await r.executeCommand(Ws.id, {
          direction: Be.RIGHT,
          range: i
        });
      else if (R.streamType === "\b") {
        const C = (v = o.getSnapshot().drawings) == null ? void 0 : v[(I = R.drawingId) != null ? I : ""];
        if (C == null)
          return !0;
        if (C.layoutType === oo.INLINE) {
          const O = o.getUnitId();
          E = await r.executeCommand(js.id, {
            direction: Be.RIGHT,
            range: i,
            unitId: O,
            drawingId: R.drawingId
          });
        } else {
          if (S == null)
            return !0;
          const O = [
            {
              startOffset: f + 1,
              endOffset: f + 1,
              style: d
            }
          ];
          E = await r.executeCommand(dn.id, {
            unitId: o.getUnitId(),
            range: {
              ...i,
              startOffset: f + 1,
              endOffset: p + 1
            },
            segmentId: l,
            direction: Be.RIGHT,
            textRanges: O,
            len: S.count
          });
        }
      } else {
        const C = [
          {
            startOffset: f,
            endOffset: f,
            style: d
          }
        ];
        E = await r.executeCommand(dn.id, {
          unitId: o.getUnitId(),
          range: g,
          segmentId: l,
          direction: Be.RIGHT,
          textRanges: C,
          len: R.count
        });
      }
    } else {
      const R = Ea(g, [g]);
      E = await r.executeCommand(Qt.id, {
        segmentId: l,
        textRanges: R,
        selections: [g]
      });
    }
    return E;
  }
};
function Ea(n, e) {
  let t = n.endOffset;
  for (const s of e) {
    const { startOffset: r, endOffset: i } = s;
    r == null || i == null || i <= n.endOffset && (t -= i - r);
  }
  return [
    {
      startOffset: t,
      endOffset: t,
      style: n.style
    }
  ];
}
const Sd = 10, Id = 6;
function Cd() {
  return X.generateRandomId(Id);
}
function vd(n) {
  const e = n.match(/data-copy-id="([^\s]+)"/);
  return e && e[1] ? e[1] : null;
}
class Rd {
  constructor() {
    x(this, "_cache", new Xa(Sd));
  }
  set(e, t) {
    this._cache.set(e, t);
  }
  get(e) {
    return this._cache.get(e);
  }
  clear() {
    this._cache.clear();
  }
}
const No = new Rd();
function Gs(n) {
  const e = n.style, t = {}, o = n.tagName.toLowerCase();
  switch (o) {
    case "b":
    case "em":
    case "strong": {
      t.bl = L.TRUE;
      break;
    }
    case "s": {
      t.st = {
        s: L.TRUE
      };
      break;
    }
    case "u": {
      t.ul = {
        s: L.TRUE
      };
      break;
    }
    case "i": {
      t.it = L.TRUE;
      break;
    }
    case "sub":
    case "sup": {
      t.va = o === "sup" ? Ne.SUPERSCRIPT : Ne.SUBSCRIPT;
      break;
    }
  }
  for (let s = 0; s < e.length; s++) {
    const r = e[s], i = e.getPropertyValue(r);
    switch (r) {
      case "font-family": {
        t.ff = i.replace(/^"/g, "").replace(/"$/g, "");
        break;
      }
      case "font-size": {
        const a = Number.parseInt(i);
        Number.isNaN(a) || (i.endsWith("pt") ? t.fs = a : i.endsWith("px") && (t.fs = mc(a)));
        break;
      }
      case "font-style": {
        i === "italic" && (t.it = L.TRUE);
        break;
      }
      case "font-weight": {
        (Number(i) > 400 || String(i) === "bold") && (t.bl = L.TRUE);
        break;
      }
      case "text-decoration": {
        /underline/.test(i) ? t.ul = {
          s: L.TRUE
        } : /overline/.test(i) ? t.ol = {
          s: L.TRUE
        } : /line-through/.test(i) && (t.st = {
          s: L.TRUE
        });
        break;
      }
      case "color": {
        try {
          const a = new dr(i);
          a.isValid && (t.cl = {
            rgb: a.toRgbString()
          });
        } catch {
        }
        break;
      }
      case "background-color": {
        const a = new dr(i);
        a.isValid && (t.bg = {
          rgb: a.toRgbString()
        });
        break;
      }
    }
  }
  return t;
}
function bd(n) {
  const e = new DOMParser(), t = `<x-univer id="univer-root">${n}</x-univer>`;
  return e.parseFromString(t, "text/html").querySelector("#univer-root");
}
function Xr(n, e) {
  const t = n.tagName.toLowerCase();
  return typeof e == "string" ? t === e : Array.isArray(e) ? e.some((o) => o === t) : e(n);
}
const Jr = 660, Jn = class Jn {
  constructor() {
    x(this, "_tableCache", []);
    x(this, "_styleCache", /* @__PURE__ */ new Map());
    x(this, "_styleRules", []);
    x(this, "_afterProcessRules", []);
  }
  static use(e) {
    if (this._pluginList.includes(e))
      throw new Error(`Univer paste plugin ${e.name} already added`);
    this._pluginList.push(e);
  }
  convert(e, t = {}) {
    var a;
    const o = Jn._pluginList.find((c) => c.checkPasteType(e)), s = bd(e), i = {
      body: {
        dataStream: "",
        paragraphs: [],
        sectionBreaks: [],
        tables: [],
        textRuns: [],
        customBlocks: []
      },
      tableSource: {},
      id: (a = t == null ? void 0 : t.unitId) != null ? a : ""
    };
    return o && (this._styleRules = [...o.stylesRules], this._afterProcessRules = [...o.afterProcessRules]), this._tableCache = [], this._styleCache.clear(), this._process(null, s.childNodes, i), this._styleCache.clear(), this._styleRules = [], this._afterProcessRules = [], i;
  }
  // eslint-disable-next-line max-lines-per-function, complexity
  _process(e, t, o) {
    var r, i, a, c;
    const s = o.body;
    for (const A of t)
      if (A.nodeType === Node.TEXT_NODE) {
        if (((r = A.nodeValue) == null ? void 0 : r.trim()) === "")
          continue;
        const l = (i = A.nodeValue) == null ? void 0 : i.replace(/[\r\n]/g, "");
        let d;
        e && this._styleCache.has(e) && (d = this._styleCache.get(e)), s.dataStream += l, d && Object.getOwnPropertyNames(d).length && s.textRuns.push({
          st: s.dataStream.length - l.length,
          ed: s.dataStream.length,
          ts: d
        });
      } else if (A.nodeName === "IMG") {
        const l = A, d = l.dataset.imageSourceType, h = d === xs.UUID ? l.dataset.source : l.src;
        if (h && d) {
          const u = Number(l.dataset.width || 100), g = Number(l.dataset.height || 100), f = Number(l.dataset.docTransformWidth || u), p = Number(l.dataset.docTransformHeight || g), m = X.generateRandomId(6);
          (c = (a = o.body) == null ? void 0 : a.customBlocks) == null || c.push({ startIndex: s.dataStream.length, blockId: m }), s.dataStream += "\b", o.drawings || (o.drawings = {}), o.drawings[m] = {
            drawingId: m,
            title: "",
            description: "",
            imageSourceType: d,
            source: h,
            transform: { width: u, height: g, left: 0 },
            docTransform: {
              size: { width: f, height: p },
              angle: 0,
              positionH: {
                relativeFrom: $n.PAGE,
                posOffset: 0
              },
              positionV: {
                relativeFrom: ot.PARAGRAPH,
                posOffset: 0
              }
            },
            layoutType: oo.INLINE,
            drawingType: Cs.DRAWING_IMAGE,
            unitId: o.id || "",
            subUnitId: o.id || ""
          };
        }
      } else {
        if (Ja.includes(A.nodeName.toLowerCase()))
          continue;
        if (A.nodeType === Node.ELEMENT_NODE) {
          const l = A, d = this._processBeforeLink(l, o), h = e ? this._styleCache.get(e) : {}, u = this._styleRules.find(({ filter: m }) => Xr(A, m)), g = u ? u.getStyle(A) : Gs(A);
          this._styleCache.set(A, { ...h, ...g });
          const { childNodes: f } = A;
          this._processBeforeTable(A, o), this._process(A, f, o), this._processAfterTable(A, o);
          const p = this._afterProcessRules.find(
            ({ filter: m }) => Xr(A, m)
          );
          p && p.handler(o, A), this._processAfterLink(l, o, d);
        }
      }
  }
  _processBeforeTable(e, t) {
    var r;
    const o = e.tagName.toUpperCase(), s = t.body;
    switch (o) {
      case "TABLE": {
        s.dataStream[s.dataStream.length - 1] !== "\r" && (s.dataStream += "\r", s.paragraphs == null && (s.paragraphs = []), (r = s.paragraphs) == null || r.push({
          startIndex: s.dataStream.length - 1
        }));
        const i = ua(0, 0, Jr);
        this._tableCache.push({
          table: i,
          startIndex: s.dataStream.length
        }), s.dataStream += U.TABLE_START;
        break;
      }
      case "TR": {
        const i = Hs(0);
        this._tableCache[this._tableCache.length - 1].table.tableRows.push(i), s.dataStream += U.TABLE_ROW_START;
        break;
      }
      case "TD": {
        const i = Fs(), a = this._tableCache[this._tableCache.length - 1].table;
        a.tableRows[a.tableRows.length - 1].tableCells.push(i), s.dataStream += U.TABLE_CELL_START;
        break;
      }
    }
  }
  _processAfterTable(e, t) {
    var i, a;
    const o = e.tagName.toUpperCase(), s = t.body;
    t.tableSource == null && (t.tableSource = {}), s.tables == null && (s.tables = []), s.sectionBreaks == null && (s.sectionBreaks = []);
    const { tableSource: r } = t;
    switch (o) {
      case "TABLE": {
        const c = this._tableCache.pop(), { startIndex: A, table: l } = c, d = l.tableRows[0].tableCells.length, h = ks(Jr / d), u = [...new Array(d).fill(null).map(() => X.deepClone(h))];
        l.tableColumns = u, r[l.tableId] = l, s.dataStream += U.TABLE_END, s.tables.push({
          startIndex: A,
          endIndex: s.dataStream.length,
          tableId: l.tableId
        });
        break;
      }
      case "TR": {
        s.dataStream += U.TABLE_ROW_END;
        break;
      }
      case "TD": {
        s.dataStream[s.dataStream.length - 1] !== "\r" && ((i = s.paragraphs) == null || i.push({
          startIndex: s.dataStream.length
        }), s.dataStream += "\r"), (a = s.sectionBreaks) == null || a.push({
          startIndex: s.dataStream.length
        }), s.dataStream += `
${U.TABLE_CELL_END}`;
        break;
      }
    }
  }
  _processBeforeLink(e, t) {
    return t.body.dataStream.length;
  }
  _processAfterLink(e, t, o) {
    var i, a;
    const s = t.body, r = e;
    r.tagName.toUpperCase() === "A" && (s.customRanges = (i = s.customRanges) != null ? i : [], s.customRanges.push({
      startIndex: o,
      endIndex: s.dataStream.length - 1,
      rangeId: (a = r.dataset.rangeid) != null ? a : pt(),
      rangeType: Ii.HYPERLINK,
      properties: { url: r.href }
    }));
  }
};
x(Jn, "_pluginList", []);
let Ut = Jn;
const xd = {
  name: "univer-doc-paste-plugin-lark",
  checkPasteType(n) {
    return /lark-record-clipboard/i.test(n);
  },
  // TODO: @JOCS, support inline code copy from lark.
  stylesRules: [
    {
      filter: ["s"],
      getStyle(n) {
        const e = Gs(n);
        return {
          st: {
            s: L.TRUE
          },
          ...e
        };
      }
    }
  ],
  afterProcessRules: [
    {
      filter(n) {
        return n.tagName === "DIV" && /ace-line/i.test(n.className);
      },
      handler(n) {
        const e = n.body;
        e.paragraphs == null && (e.paragraphs = []), e.paragraphs.push({
          startIndex: e.dataStream.length
        }), e.dataStream += "\r";
      }
    }
  ]
};
function Sa(n) {
  const e = n.style, t = {};
  for (let o = 0; o < e.length; o++) {
    const s = e[o], r = e.getPropertyValue(s);
    switch (s) {
      case "margin-top": {
        const i = Number.parseInt(r);
        t.spaceAbove = { v: /pt/.test(r) ? Er(i) : i };
        break;
      }
      case "margin-bottom": {
        const i = Number.parseInt(r);
        t.spaceBelow = { v: /pt/.test(r) ? Er(i) : i };
        break;
      }
      case "line-height": {
        let i = Number.parseFloat(r);
        r.endsWith("%") && (i /= 100), t.lineSpacing = i;
        break;
      }
    }
  }
  return Object.getOwnPropertyNames(t).length ? t : null;
}
const Od = {
  name: "univer-doc-paste-plugin-univer",
  checkPasteType(n) {
    return /UniverNormal/i.test(n);
  },
  stylesRules: [],
  afterProcessRules: [
    {
      filter(n) {
        return n.tagName === "P" && /UniverNormal/i.test(n.className);
      },
      handler(n, e) {
        const t = n.body;
        t.paragraphs == null && (t.paragraphs = []);
        const o = {
          startIndex: t.dataStream.length
        }, s = Sa(e);
        s && (o.paragraphStyle = s), t.paragraphs.push(o), t.dataStream += "\r";
      }
    }
  ]
}, Td = {
  name: "univer-doc-paste-plugin-word",
  checkPasteType(n) {
    return /word|mso/i.test(n);
  },
  stylesRules: [
    {
      filter: ["b"],
      getStyle(n) {
        const e = Gs(n);
        return { bl: L.TRUE, ...e };
      }
    }
  ],
  afterProcessRules: [
    {
      filter(n) {
        return n.tagName === "P";
      },
      handler(n, e) {
        const t = n.body;
        t.paragraphs == null && (t.paragraphs = []);
        const o = {
          startIndex: t.dataStream.length
        }, s = Sa(e);
        s && (o.paragraphStyle = s), t.paragraphs.push(o), t.dataStream += "\r";
      }
    }
  ]
};
function yd(n) {
  var o, s;
  const e = (r) => {
    let i = "";
    return Object.keys(r).forEach((a) => {
      r[a] !== void 0 && (i += ` ${a}=${r[a]}`);
    }), i;
  }, t = {
    "data-doc-transform-height": n.docTransform.size.height,
    "data-doc-transform-width": n.docTransform.size.width,
    "data-width": (o = n.transform) == null ? void 0 : o.width,
    "data-height": (s = n.transform) == null ? void 0 : s.height,
    "data-image-source-type": n.imageSourceType,
    "data-source": n.imageSourceType === xs.UUID ? n.source : void 0,
    src: n.source
  };
  return `<img  ${e(t)}></img>`;
}
function Zr(n, e) {
  const { st: t, ed: o, ts: s = {} } = e, { ff: r, fs: i, it: a, bl: c, ul: A, st: l, ol: d, bg: h, cl: u, va: g } = s;
  let f = n.slice(t, o);
  const p = [];
  return a === L.TRUE && (f = `<i>${f}</i>`), g === Ne.SUPERSCRIPT ? f = `<sup>${f}</sup>` : g === Ne.SUBSCRIPT && (f = `<sub>${f}</sub>`), (A == null ? void 0 : A.s) === L.TRUE && (f = `<u>${f}</u>`), (l == null ? void 0 : l.s) === L.TRUE && (f = `<s>${f}</s>`), c === L.TRUE && (f = `<strong>${f}</strong>`), r && p.push(`font-family: ${r}`), u && p.push(`color: ${u.rgb}`), i && p.push(`font-size: ${i}pt`), d && p.push("text-decoration: overline"), h && p.push(`background: ${h.rgb}`), p.length ? `<span style="${p.join("; ")};">${f}</span>` : f;
}
function Qo(n, e, t) {
  const { dataStream: o, textRuns: s = [] } = n;
  if (e === t)
    return "";
  let r = e;
  const i = [];
  for (const a of s) {
    const { st: c, ed: A } = a;
    X.hasIntersectionBetweenTwoRanges(e, t, c, A) && (c > r ? (i.push(o.slice(r, c)), i.push(Zr(o, {
      ...a,
      ed: Math.min(A, t)
    }))) : i.push(Zr(o, {
      ...a,
      st: r,
      ed: Math.min(A, t)
    }))), r = Math.max(e, Math.min(A, t));
  }
  return r !== t && i.push(o.slice(r, t)), i.join("");
}
function Bd(n, e, t) {
  const o = n.body, s = n.drawings || {}, { customRanges: r = [], customBlocks: i = [] } = o || {}, a = [...i], c = r.filter((u) => u.startIndex >= e && u.endIndex <= t);
  let A = e, l = "";
  const d = (u, g) => {
    let f = "", p = 0, m = u, E = a.findIndex((I) => u <= I.startIndex && g >= I.startIndex);
    if (E === -1)
      return f = Qo(o, u, g), { sliceHtml: f, customBlockLength: p };
    for (; E !== -1; ) {
      const I = a[E];
      a.splice(E, 1), f += Qo(o, m, I.startIndex);
      const v = s[I.blockId];
      if (v)
        switch (v.drawingType) {
          case Cs.DRAWING_IMAGE: {
            f += yd(v), p++;
            break;
          }
        }
      m = I.startIndex + 1, E = a.findIndex((R) => m <= R.startIndex && g >= R.startIndex);
    }
    return f = f + Qo(o, m, g + 1), { sliceHtml: f, customBlockLength: p };
  };
  c.forEach((u) => {
    var v, R;
    const { startIndex: g, endIndex: f, rangeType: p, rangeId: m } = u, E = d(A, g);
    l += E.sliceHtml;
    const I = d(g, f + 1);
    switch (p) {
      case Ii.HYPERLINK: {
        l += `<a data-rangeid="${m}" href="${(R = (v = u.properties) == null ? void 0 : v.url) != null ? R : ""}">${I.sliceHtml}</a>`;
        break;
      }
      default: {
        l += I.sliceHtml;
        break;
      }
    }
    A = f + 1 + (E.customBlockLength + I.customBlockLength);
  });
  const h = d(A, t);
  return l += h.sliceHtml, l;
}
function Md(n) {
  const e = n.body || {}, { paragraphs: t = [], sectionBreaks: o = [] } = e;
  let { dataStream: s = "" } = e;
  s.endsWith(`\r
`) || (s += `\r
`, t.push({
    startIndex: s.length - 2
  }), o.push({
    startIndex: s.length - 1
  }), e.dataStream = s, e.paragraphs = t, e.sectionBreaks = o);
  const r = { html: "" }, i = Ec(s).sectionList;
  for (const a of i)
    yt(a, n, r);
  return r.html;
}
function yt(n, e, t) {
  var o, s;
  switch (n.nodeType) {
    case qt.SECTION_BREAK: {
      for (const r of n.children)
        yt(r, e, t);
      break;
    }
    case qt.PARAGRAPH: {
      const { children: r, startIndex: i, endIndex: a } = n, c = (s = (o = e.body) == null ? void 0 : o.paragraphs.find((g) => g.startIndex === a)) != null ? s : {}, { paragraphStyle: A = {} } = c, { spaceAbove: l, spaceBelow: d, lineSpacing: h } = A, u = [];
      if (l != null && (typeof l == "number" ? u.push(`margin-top: ${l}px`) : u.push(`margin-top: ${l.v}px`)), d != null && (typeof d == "number" ? u.push(`margin-bottom: ${d}px`) : u.push(`margin-bottom: ${d.v}px`)), h != null && u.push(`line-height: ${h}`), t.html += `<p class="UniverNormal" ${u.length ? `style="${u.join("; ")};"` : ""}>`, r.length)
        for (const g of r)
          yt(g, e, t);
      t.html += `${Bd(e, i, a)}</p>`;
      break;
    }
    case qt.TABLE: {
      const { children: r } = n;
      t.html += '<table class="UniverTable" style="width: 100%; border-collapse: collapse;"><tbody>';
      for (const i of r)
        yt(i, e, t);
      t.html += "</tbody></table>";
      break;
    }
    case qt.TABLE_ROW: {
      const { children: r } = n;
      t.html += '<tr class="UniverTableRow">';
      for (const i of r)
        yt(i, e, t);
      t.html += "</tr>";
      break;
    }
    case qt.TABLE_CELL: {
      const { children: r } = n;
      t.html += '<td class="UniverTableCell">';
      for (const i of r)
        yt(i, e, t);
      t.html += "</td>";
      break;
    }
    default:
      throw new Error(`Unknown node type: ${n.nodeType}`);
  }
}
class _d {
  convert(e) {
    if (e.length === 0)
      throw new Error("The bodyList length at least to be 1");
    let t = "";
    for (const o of X.deepClone(e))
      t += Md(o);
    return t;
  }
}
var Pd = Object.defineProperty, Dd = Object.getOwnPropertyDescriptor, wd = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Dd(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Pd(e, t, s), s;
}, Jt = (n, e) => (t, o) => e(t, o, n);
Ut.use(Td);
Ut.use(xd);
Ut.use(Od);
function $r(n, e, t) {
  var r, i, a;
  const o = Ei(n, e, t + 2), s = U.TABLE_START + U.TABLE_ROW_START + U.TABLE_CELL_START + o.dataStream + U.TABLE_CELL_END + U.TABLE_ROW_END + U.TABLE_END;
  return o.dataStream = s, (r = o.textRuns) == null || r.forEach((c) => {
    const { st: A, ed: l } = c;
    c.st = A + 3, c.ed = l + 3;
  }), (i = o.tables) == null || i.forEach((c) => {
    const { startIndex: A, endIndex: l } = c;
    c.startIndex = A + 3, c.endIndex = l + 3;
  }), (a = o.paragraphs) == null || a.forEach((c) => {
    const { startIndex: A } = c;
    c.startIndex = A + 3;
  }), o;
}
const Sn = ps("doc.clipboard-service");
let ns = class extends ue {
  constructor(e, t, o, s, r) {
    super();
    x(this, "_clipboardHooks", []);
    x(this, "_htmlToUDM", new Ut());
    x(this, "_umdToHtml", new _d());
    this._univerInstanceService = e, this._logService = t, this._commandService = o, this._clipboardInterfaceService = s, this._docSelectionManagerService = r;
  }
  async copy(e = ur.copy) {
    var r;
    const { newSnapshotList: t = [], needCache: o = !1, snapshot: s } = (r = this._getDocumentBodyInRanges(e)) != null ? r : {};
    if (t.length === 0 || s == null)
      return !1;
    try {
      const i = this._docSelectionManagerService.getActiveTextRange(), a = !!(i != null && i.segmentId);
      this._setClipboardData(t, !a && o);
    } catch (i) {
      return this._logService.error("[DocClipboardService] copy failed", i), !1;
    }
    return !0;
  }
  async cut() {
    return this._cut();
  }
  async paste(e) {
    const t = await this._genDocDataFromClipboardItems(e);
    return this._paste(t);
  }
  async legacyPaste(e) {
    let { html: t, text: o, files: s } = e;
    const r = this._univerInstanceService.getCurrentUnitForType(_.UNIVER_DOC), i = (r == null ? void 0 : r.getUnitId()) || "";
    !t && !o && s.length && (t = await this._createImagePasteHtml(s));
    const a = this._genDocDataFromHtmlAndText(t, o, i);
    if (i === vs)
      if (o) {
        const c = Ce.transform.fromPlainText(o);
        return this._paste({ body: c });
      } else
        a.body.textRuns = [];
    return this._paste(a);
  }
  async _cut() {
    var i, a, c;
    const {
      segmentId: e,
      endOffset: t,
      style: o
    } = (i = this._docSelectionManagerService.getActiveTextRange()) != null ? i : {}, s = (a = this._docSelectionManagerService.getTextRanges()) != null ? a : [], r = (c = this._docSelectionManagerService.getRectRanges()) != null ? c : [];
    if (e == null && this._logService.error("[DocClipboardController] segmentId is not existed"), s.length === 0 && r.length === 0)
      return !1;
    this.copy(ur.cut);
    try {
      let A = 0;
      if (r.length > 0)
        A = zs(s, r);
      else if (t != null) {
        A = t;
        for (const d of s) {
          const { startOffset: h, endOffset: u } = d;
          h == null || u == null || u <= t && (A -= u - h);
        }
      }
      const l = [
        {
          startOffset: A,
          endOffset: A,
          style: o
        }
      ];
      return this._commandService.executeCommand(Qt.id, { segmentId: e, textRanges: l });
    } catch {
      return this._logService.error("[DocClipboardController] cut content failed"), !1;
    }
  }
  async _paste(e) {
    var l, d;
    const { body: t } = e;
    if (t == null)
      return !1;
    let o = Za(t);
    if (!((l = this._univerInstanceService.getCurrentUnitForType(_.UNIVER_DOC)) == null ? void 0 : l.getUnitId()))
      return !1;
    this._clipboardHooks.forEach((h) => {
      h.onBeforePaste && (o = h.onBeforePaste(o));
    }), o.customRanges = (d = o.customRanges) == null ? void 0 : d.map(Ce.customRange.copyCustomRange);
    const r = this._docSelectionManagerService.getActiveTextRange(), { segmentId: i, endOffset: a, style: c } = r || {}, A = this._docSelectionManagerService.getTextRanges();
    if (i == null && this._logService.error("[DocClipboardController] segmentId does not exist!"), a == null || A == null)
      return !1;
    try {
      let h = a;
      for (const g of A) {
        const { startOffset: f, endOffset: p } = g;
        f == null || p == null || p <= a && (h += o.dataStream.length - (p - f));
      }
      const u = [
        {
          startOffset: h,
          endOffset: h,
          style: c
        }
      ];
      return this._commandService.executeCommand(fa.id, {
        doc: {
          ...e,
          body: o
        },
        segmentId: i,
        textRanges: u
      });
    } catch {
      return this._logService.error("[DocClipboardController]", "clipboard is empty."), !1;
    }
  }
  async _setClipboardData(e, t = !0) {
    var i, a, c, A;
    const o = Cd(), s = (e.length > 1 ? e.map((l) => {
      var d;
      return ((d = l.body) == null ? void 0 : d.dataStream) || "";
    }).join(`
`) : ((i = e[0].body) == null ? void 0 : i.dataStream) || "").replaceAll(U.TABLE_START, "").replaceAll(U.TABLE_END, "").replaceAll(U.TABLE_ROW_START, "").replaceAll(U.TABLE_ROW_END, "").replaceAll(U.TABLE_CELL_START, "").replaceAll(U.TABLE_CELL_END, "").replaceAll(`\r
`, " ");
    let r = this._umdToHtml.convert(e);
    if (e.length === 1 && t) {
      r = r.replace(/(<[a-z]+)/, (h, u) => `${u} data-copy-id="${o}"`);
      const l = e[0], d = { body: l.body };
      if ((c = (a = l.body) == null ? void 0 : a.customBlocks) != null && c.length) {
        d.drawings = {};
        for (const h of l.body.customBlocks) {
          const { blockId: u } = h, g = (A = l.drawings) == null ? void 0 : A[u];
          if (g) {
            const f = X.generateRandomId(6);
            h.blockId = f, d.drawings[f] = {
              ...X.deepClone(g),
              drawingId: f
            };
          }
        }
      }
      No.set(o, d);
    }
    return this._clipboardInterfaceService.write(s, r);
  }
  addClipboardHook(e) {
    return this._clipboardHooks.push(e), Zn(() => {
      const t = this._clipboardHooks.indexOf(e);
      t > -1 && this._clipboardHooks.splice(t, 1);
    });
  }
  _getDocumentBodyInRanges(e) {
    var A;
    const t = this._univerInstanceService.getCurrentUniverDocInstance(), o = this._docSelectionManagerService.getDocRanges(), s = [];
    let r = !0;
    if (t == null || o.length === 0)
      return;
    const i = o[0].segmentId, a = (A = t == null ? void 0 : t.getSelfOrHeaderFooterModel(i)) == null ? void 0 : A.getBody(), c = t.getSnapshot();
    if (a != null) {
      for (const l of o) {
        const { startOffset: d, endOffset: h, collapsed: u, rangeType: g } = l;
        if (u || d == null || h == null)
          continue;
        if (g === Ge.RECT) {
          r = !1;
          const { spanEntireRow: m } = l;
          let E;
          E = $r(a, d, h), s.push(E);
          continue;
        }
        const f = { startOffset: d, endOffset: h, collapsed: u }, p = t.getSelfOrHeaderFooterModel(i).sliceBody(f.startOffset, f.endOffset, e);
        p != null && s.push(p);
      }
      return {
        newSnapshotList: s.map((l) => ({ ...c, body: l })),
        needCache: r,
        snapshot: c
      };
    }
  }
  async _genDocDataFromClipboardItems(e) {
    try {
      let t = "", o = "";
      const s = [];
      for (const r of e)
        for (const i of r.types)
          switch (i) {
            case Qi: {
              o = await r.getType(i).then((a) => a && a.text());
              break;
            }
            case Ni: {
              t = await r.getType(i).then((a) => a && a.text());
              break;
            }
            case wi:
            case Di:
            case Pi:
            case _i: {
              const a = await r.getType(i), c = new File([a], `pasted_image.${i.split("/")[1]}`, { type: i });
              s.push(c);
              break;
            }
          }
      return !t && !o && s.length && (t = await this._createImagePasteHtml(s)), this._genDocDataFromHtmlAndText(t, o);
    } catch (t) {
      return Promise.reject(t);
    }
  }
  _genDocDataFromHtmlAndText(e, t, o) {
    if (!e) {
      if (t)
        return { body: Ce.transform.fromPlainText(t) };
      throw new Error("[DocClipboardService] html and text cannot be both empty!");
    }
    const s = vd(e);
    if (s) {
      const i = No.get(s);
      if (i)
        return i;
    }
    if (!o) {
      const i = this._univerInstanceService.getCurrentUnitForType(_.UNIVER_DOC);
      o = (i == null ? void 0 : i.getUnitId()) || "";
    }
    const r = this._htmlToUDM.convert(e, { unitId: o });
    return s && No.set(s, r), r;
  }
  async _createImagePasteHtml(e) {
    var a, c;
    const t = {
      id: "",
      documentStyle: {},
      body: {
        dataStream: "",
        customBlocks: []
      },
      drawings: {}
    }, o = async (A) => {
      const l = new FileReader();
      return new Promise((d) => {
        l.onloadend = function() {
          d({
            source: l.result,
            imageSourceType: xs.BASE64
          });
        }, l.readAsDataURL(A);
      });
    }, s = (A) => {
      const l = new Image(), d = 500;
      return new Promise((h) => {
        l.src = typeof A == "string" ? A : URL.createObjectURL(A), l.onload = () => {
          const u = Math.min(d, l.naturalWidth), g = l.naturalHeight / l.naturalWidth;
          h({ width: u, height: u * g });
        };
      });
    }, r = (c = (a = this._clipboardHooks.find((A) => A.onBeforePasteImage)) == null ? void 0 : a.onBeforePasteImage) != null ? c : o;
    return await Promise.all(e.map(async (A, l) => {
      var m;
      const d = await r(A);
      if (!d)
        return Promise.resolve();
      const { width: h = 100, height: u = 100 } = await s(A), g = `paste_image_id_${l}`, f = t.body, p = t.drawings;
      f.dataStream += "\b", (m = f.customBlocks) == null || m.push({ startIndex: l, blockId: g }), p[g] = {
        drawingId: g,
        unitId: "",
        subUnitId: "",
        imageSourceType: d.imageSourceType,
        title: "",
        source: d.source,
        description: "",
        layoutType: oo.INLINE,
        drawingType: Cs.DRAWING_IMAGE,
        transform: {
          width: h,
          height: u,
          angle: 0
        },
        docTransform: {
          angle: 0,
          size: { width: h, height: u },
          positionH: { relativeFrom: $n.CHARACTER, posOffset: 0 },
          positionV: { relativeFrom: ot.LINE, posOffset: 0 }
        }
      };
    })), this._umdToHtml.convert([t]);
  }
};
ns = wd([
  Jt(0, Q),
  Jt(1, fs),
  Jt(2, y),
  Jt(3, Mi),
  Jt(4, z(G))
], ns);
function Io(n) {
  return n.getContextValue(hn) || n.getContextValue(wn);
}
const Ys = 999, Fn = {
  id: Oc.id,
  name: "doc.command.copy",
  type: N.COMMAND,
  multi: !0,
  priority: Ys,
  preconditions: Io,
  handler: async (n) => n.get(Sn).copy()
}, qs = {
  id: Tc.id,
  name: "doc.command.cut",
  type: N.COMMAND,
  multi: !0,
  priority: Ys,
  preconditions: Io,
  handler: async (n) => n.get(Sn).cut()
}, Ks = {
  id: yc.id,
  name: "doc.command.paste",
  type: N.COMMAND,
  multi: !0,
  priority: Ys,
  preconditions: Io,
  handler: async (n) => {
    const e = n.get(Sn), o = await n.get(Mi).read();
    return o.length === 0 ? !1 : e.paste(o);
  }
}, Co = {
  id: "doc.command.switch-mode",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function, complexity
  handler: async (n) => {
    var E, I, v, R, S;
    const e = n.get(y), t = n.get(fe), o = n.get(G), r = n.get(Q).getCurrentUniverDocInstance();
    if (r == null)
      return !1;
    const i = r.getUnitId(), a = (E = t.getRenderById(i)) == null ? void 0 : E.with(ie).getSkeleton(), c = (I = t.getRenderById(i)) == null ? void 0 : I.with(Se);
    if (a == null || c == null)
      return !1;
    const A = c == null ? void 0 : c.getSegment(), l = c == null ? void 0 : c.getSegmentPage(), d = r.getSnapshot().documentStyle.documentFlavor, h = o.getDocRanges(), u = {
      id: J.id,
      params: {
        unitId: i,
        actions: [],
        textRanges: d === ye.TRADITIONAL && A ? [] : h
      }
    }, g = k.getInstance(), f = [];
    let p;
    if (d === void 0 ? p = g.insertOp(["documentStyle", "documentFlavor"], ye.MODERN) : d === ye.MODERN ? p = g.replaceOp(["documentStyle", "documentFlavor"], d, ye.TRADITIONAL) : p = g.replaceOp(["documentStyle", "documentFlavor"], d, ye.MODERN), p)
      f.push(p);
    else
      return !1;
    if (d !== ye.MODERN) {
      const C = r.getSnapshot(), { drawings: T = {}, body: O } = C, P = (v = O == null ? void 0 : O.customBlocks) != null ? v : [];
      for (const b in T) {
        const B = T[b], M = P.find((ae) => ae.blockId === b);
        if (M == null)
          continue;
        const H = B.docTransform.positionV, { relativeFrom: F, posOffset: D } = H;
        if (F === ot.PARAGRAPH)
          continue;
        const { startIndex: te } = M, q = a.findNodeByCharIndex(te, A, l), V = (R = q == null ? void 0 : q.parent) == null ? void 0 : R.parent, Y = V == null ? void 0 : V.parent, oe = Y == null ? void 0 : Y.lines.find((ae) => ae.paragraphIndex === (V == null ? void 0 : V.paragraphIndex) && ae.paragraphStart), ce = (S = Y == null ? void 0 : Y.parent) == null ? void 0 : S.parent;
        if (q == null || V == null || oe == null || Y == null || ce == null)
          continue;
        let he = 0;
        F === ot.LINE ? he -= V.top : F === ot.PAGE && (he += ce.marginTop), he += oe.top;
        const Ae = {
          ...H,
          relativeFrom: ot.PARAGRAPH,
          posOffset: (D != null ? D : 0) - he
        }, ne = g.replaceOp(["drawings", b, "docTransform", "positionV"], H, Ae);
        ne && f.push(ne);
      }
    }
    return u.params.actions = f.reduce((C, T) => k.compose(C, T), null), !!e.syncExecuteCommand(u.id, u.params);
  }
}, Xs = {
  id: "doc.table.delete-rows",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n) => {
    const e = n.get(G), t = n.get(Q), o = n.get(y), s = e.getRectRanges(), r = e.getActiveTextRange(), i = En(r, s);
    if (i == null)
      return !1;
    const { segmentId: a } = i, c = t.getCurrentUniverDocInstance(), A = c == null ? void 0 : c.getSelfOrHeaderFooterModel(a).getBody();
    if (c == null || A == null)
      return !1;
    const l = ke(n, c.getUnitId());
    if (l == null)
      return !1;
    const d = l.getViewModel(), h = c == null ? void 0 : c.getUnitId(), u = new me(), g = k.getInstance(), f = ha(i, d);
    if (f == null)
      return !1;
    const { offset: p, rowIndexes: m, len: E, tableId: I, cursor: v, selectWholeTable: R } = f;
    if (R)
      return o.executeCommand(In.id);
    const S = [], C = [{
      startOffset: v,
      endOffset: v,
      collapsed: !0
    }], T = {
      id: J.id,
      params: {
        unitId: h,
        actions: [],
        textRanges: C
      }
    };
    p > 0 && u.push({
      t: W.RETAIN,
      len: p
    }), u.push({
      t: W.DELETE,
      len: E
    });
    const O = le(c, a);
    S.push(g.editOp(u.serialize(), O));
    for (const b of m.reverse()) {
      const B = g.removeOp(["tableSource", I, "tableRows", b]);
      S.push(B);
    }
    return T.params.actions = S.reduce((b, B) => k.compose(b, B), null), !!o.syncExecuteCommand(T.id, T.params);
  }
}, Js = {
  id: "doc.table.delete-columns",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n) => {
    const e = n.get(G), t = n.get(Q), o = n.get(y), s = e.getRectRanges(), r = e.getActiveTextRange(), i = En(r, s);
    if (i == null)
      return !1;
    const { segmentId: a } = i, c = t.getCurrentUniverDocInstance(), A = c == null ? void 0 : c.getSelfOrHeaderFooterModel(a).getBody();
    if (c == null || A == null)
      return !1;
    const l = ke(n, c.getUnitId());
    if (l == null)
      return !1;
    const d = l.getViewModel(), h = c == null ? void 0 : c.getUnitId(), u = new me(), g = k.getInstance(), f = Ad(i, d);
    if (f == null)
      return !1;
    const { offsets: p, columnIndexes: m, tableId: E, cursor: I, rowCount: v, selectWholeTable: R } = f;
    if (R)
      return o.executeCommand(In.id);
    const S = [], C = [{
      startOffset: I,
      endOffset: I,
      collapsed: !0
    }], T = {
      id: J.id,
      params: {
        unitId: h,
        actions: [],
        textRanges: C
      }
    };
    for (const b of p) {
      const { retain: B, delete: M } = b;
      B > 0 && u.push({
        t: W.RETAIN,
        len: B
      }), u.push({
        t: W.DELETE,
        len: M
      });
    }
    const O = le(c, a);
    S.push(g.editOp(u.serialize(), O)), m.reverse();
    for (let b = 0; b < v; b++)
      for (const B of m) {
        const M = g.removeOp(["tableSource", E, "tableRows", b, "tableCells", B]);
        S.push(M);
      }
    for (const b of m) {
      const B = g.removeOp(["tableSource", E, "tableColumns", b]);
      S.push(B);
    }
    return T.params.actions = S.reduce((b, B) => k.compose(b, B), null), !!o.syncExecuteCommand(T.id, T.params);
  }
}, In = {
  id: "doc.table.delete-table",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n) => {
    const e = n.get(G), t = n.get(Q), o = n.get(y), s = e.getRectRanges(), r = e.getActiveTextRange(), i = En(r, s);
    if (i == null)
      return !1;
    const { segmentId: a } = i, c = t.getCurrentUniverDocInstance(), A = c == null ? void 0 : c.getSelfOrHeaderFooterModel(a).getBody();
    if (c == null || A == null)
      return !1;
    const l = ke(n, c.getUnitId());
    if (l == null)
      return !1;
    const d = l.getViewModel(), h = c == null ? void 0 : c.getUnitId(), u = new me(), g = k.getInstance(), f = ga(i, d);
    if (f == null)
      return !1;
    const { offset: p, len: m, tableId: E, cursor: I } = f, v = [], R = [{
      startOffset: I,
      endOffset: I,
      collapsed: !0
    }], S = {
      id: J.id,
      params: {
        unitId: h,
        actions: [],
        textRanges: R
      }
    };
    p > 0 && u.push({
      t: W.RETAIN,
      len: p
    }), u.push({
      t: W.DELETE,
      len: m
    });
    const C = le(c, a);
    v.push(g.editOp(u.serialize(), C));
    const T = g.removeOp(["tableSource", E]);
    return v.push(T), S.params.actions = v.reduce((P, b) => k.compose(P, b), null), !!o.syncExecuteCommand(S.id, S.params);
  }
}, Zs = "doc.command.table-insert-row", $s = "doc.command.table-insert-column", Nd = "doc.command.table-insert-row-above", Qd = "doc.command.table-insert-row-bellow", Ud = "doc.command.table-insert-column-left", Ld = "doc.command.table-insert-column-right", er = {
  id: Nd,
  type: N.COMMAND,
  handler: async (n) => n.get(y).executeCommand(Zs, { position: Eo.ABOVE })
}, tr = {
  id: Qd,
  type: N.COMMAND,
  handler: async (n) => n.get(y).executeCommand(Zs, { position: Eo.BELLOW })
}, nr = {
  id: Ud,
  type: N.COMMAND,
  handler: async (n) => n.get(y).executeCommand($s, { position: Ls.LEFT })
}, or = {
  id: Ld,
  type: N.COMMAND,
  handler: async (n) => n.get(y).executeCommand($s, { position: Ls.RIGHT })
}, Ia = {
  id: Zs,
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n, e) => {
    const { position: t } = e, o = n.get(G), s = n.get(Q), r = n.get(y), i = o.getRectRanges(), a = o.getActiveTextRange(), c = En(a, i);
    if (c == null)
      return !1;
    const { segmentId: A } = c, l = s.getCurrentUnitForType(_.UNIVER_DOC), d = l == null ? void 0 : l.getSelfOrHeaderFooterModel(A).getBody();
    if (l == null || d == null)
      return !1;
    const h = ke(n, l.getUnitId());
    if (h == null)
      return !1;
    const u = h.getViewModel(), g = l == null ? void 0 : l.getUnitId(), f = new me(), p = k.getInstance(), m = id(c, t, u);
    if (m == null)
      return !1;
    const { offset: E, colCount: I, tableId: v, insertRowIndex: R } = m, S = [], C = E + 2, T = [{
      startOffset: C,
      endOffset: C,
      collapsed: !0
    }], O = {
      id: J.id,
      params: {
        unitId: g,
        actions: [],
        textRanges: T
      }
    };
    E > 0 && f.push({
      t: W.RETAIN,
      len: E
    });
    const P = sd(I);
    f.push({
      t: W.INSERT,
      body: P,
      len: P.dataStream.length
    });
    const b = le(l, A);
    S.push(p.editOp(f.serialize(), b));
    const B = Hs(I), M = p.insertOp(["tableSource", v, "tableRows", R], B);
    return S.push(M), O.params.actions = S.reduce((F, D) => k.compose(F, D), null), !!r.syncExecuteCommand(O.id, O.params);
  }
}, Fd = {
  id: $s,
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n, e) => {
    var ce, he, Ae;
    const { position: t } = e, o = n.get(G), s = n.get(Q), r = n.get(y), i = o.getRectRanges(), a = o.getActiveTextRange(), c = En(a, i);
    if (c == null)
      return !1;
    const { segmentId: A } = c, l = s.getCurrentUniverDocInstance(), d = l == null ? void 0 : l.getSelfOrHeaderFooterModel(A).getBody();
    if (l == null || d == null)
      return !1;
    const h = ke(n, l.getUnitId());
    if (h == null)
      return !1;
    const u = h.getViewModel(), g = l == null ? void 0 : l.getUnitId(), f = new me(), p = k.getInstance(), m = ad(c, t, u);
    if (m == null)
      return !1;
    const { offsets: E, columnIndex: I, tableId: v, rowCount: R } = m, S = [], C = E[0] + 1, T = [{
      startOffset: C,
      endOffset: C,
      collapsed: !0
    }], O = {
      id: J.id,
      params: {
        unitId: g,
        actions: [],
        textRanges: T
      }
    };
    for (const ne of E) {
      f.push({
        t: W.RETAIN,
        len: ne
      });
      const ae = rd();
      f.push({
        t: W.INSERT,
        body: ae,
        len: ae.dataStream.length
      });
    }
    const P = le(l, A);
    S.push(p.editOp(f.serialize(), P));
    for (let ne = 0; ne < R; ne++) {
      const ae = Fs(), Te = p.insertOp(["tableSource", v, "tableRows", ne, "tableCells", I], ae);
      S.push(Te);
    }
    const b = l.getSnapshot(), B = b.documentStyle, { marginLeft: M = 0, marginRight: H = 0 } = B, F = ((he = (ce = B.pageSize) == null ? void 0 : ce.width) != null ? he : 800) - M - H, D = (Ae = b == null ? void 0 : b.tableSource) == null ? void 0 : Ae[v].tableColumns, { newColWidth: te, widths: q } = cd(F, D, I);
    for (let ne = 0; ne < q.length; ne++) {
      const ae = p.replaceOp(["tableSource", v, "tableColumns", ne, "size", "width", "v"], D[ne].size.width.v, q[ne]);
      S.push(ae);
    }
    const V = ks(te), Y = p.insertOp(["tableSource", v, "tableColumns", I], V);
    return S.push(Y), O.params.actions = S.reduce((ne, ae) => k.compose(ne, ae), null), !!r.syncExecuteCommand(O.id, O.params);
  }
}, Ca = "COMPONENT_DOC_CREATE_TABLE_CONFIRM";
function va(n, e) {
  const t = [];
  for (let o = 0, s = n.length; o < s; o++)
    n[o] === U.PARAGRAPH && t.push({
      startIndex: o
    });
  if (e)
    for (const o of t)
      e.bullet && (o.bullet = X.deepClone(e.bullet)), e.paragraphStyle && (o.paragraphStyle = X.deepClone(e.paragraphStyle));
  return t;
}
const Ra = {
  id: "doc.command.break-line",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n) => {
    var S, C, T;
    const e = n.get(G), t = n.get(Q), o = n.get(y), s = n.get(Je), r = e.getActiveTextRange(), i = e.getRectRanges();
    if (r == null)
      return !1;
    if (i && i.length) {
      const { startOffset: O } = r;
      return e.replaceDocRanges([{
        startOffset: O,
        endOffset: O
      }]), !0;
    }
    const { segmentId: a } = r, c = t.getCurrentUnitForType(_.UNIVER_DOC), A = c == null ? void 0 : c.getSelfOrHeaderFooterModel(a != null ? a : "").getBody();
    if (c == null || A == null)
      return !1;
    const l = c.getUnitId(), { startOffset: d, endOffset: h } = r, g = ((S = A.paragraphs) != null ? S : []).find((O) => O.startIndex >= d);
    if (!g)
      return !1;
    const f = g.startIndex, p = s.getDefaultStyle(), m = s.getStyleCache(), E = co((C = A.textRuns) != null ? C : [], h, p, m), I = {
      dataStream: U.PARAGRAPH,
      paragraphs: va(U.PARAGRAPH, g),
      textRuns: [{
        st: 0,
        ed: 1,
        ts: {
          ...E.ts
        }
      }]
    }, v = {
      startOffset: d,
      endOffset: h,
      collapsed: d === h
    }, R = await o.executeCommand(Vs.id, {
      unitId: l,
      body: I,
      range: v,
      segmentId: a
    });
    if (((T = g.bullet) == null ? void 0 : T.listType) === Oe.CHECK_LIST_CHECKED) {
      const O = {
        index: f + 1 - (h - d),
        segmentId: a,
        textRanges: [{
          startOffset: d + 1,
          endOffset: d + 1
        }]
      };
      return !!await o.executeCommand(Ns.id, O) && R;
    }
    return R;
  }
}, Hd = "doc.command.create-table", ba = {
  id: Hd,
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n, e) => {
    var Ae, ne, ae, Te, je, ut;
    const { rowCount: t, colCount: o } = e, s = n.get(G), r = n.get(Q), i = n.get(y), a = n.get(Je), c = s.getActiveTextRange();
    if (c == null)
      return !1;
    const { segmentId: A, segmentPage: l } = c, d = r.getCurrentUniverDocInstance(), h = d == null ? void 0 : d.getSelfOrHeaderFooterModel(A).getBody();
    if (d == null || h == null)
      return !1;
    const u = d.getUnitId(), g = ke(n, u), f = g == null ? void 0 : g.getSkeleton();
    if (f == null)
      return !1;
    const { startOffset: p } = c, E = ((Ae = h.paragraphs) != null ? Ae : []).find((we) => we.startIndex >= p), I = f.findNodeByCharIndex(p, A, l);
    if (I == null)
      return !1;
    const v = new me(), R = k.getInstance(), S = [], C = p + 4, T = [{
      startOffset: C,
      endOffset: C,
      collapsed: !0
    }], O = {
      id: J.id,
      params: {
        unitId: u,
        actions: [],
        textRanges: T
      }
    };
    p > 0 && v.push({
      t: W.RETAIN,
      len: p
    }), v.push({
      t: W.INSERT,
      body: {
        dataStream: U.PARAGRAPH,
        paragraphs: va(U.PARAGRAPH, E)
      },
      len: 1
    });
    const P = a.getDefaultStyle(), b = a.getStyleCache(), B = co(
      (ne = h.textRuns) != null ? ne : [],
      p,
      P,
      b
    ), { dataStream: M, paragraphs: H, sectionBreaks: F } = od(t, o), D = (ut = (je = (Te = (ae = I.parent) == null ? void 0 : ae.parent) == null ? void 0 : Te.parent) == null ? void 0 : je.parent) == null ? void 0 : ut.parent;
    if (D == null)
      return !1;
    const { pageWidth: te, marginLeft: q, marginRight: V } = D, Y = ua(t, o, te - q - V);
    v.push({
      t: W.INSERT,
      body: {
        dataStream: M,
        paragraphs: H,
        sectionBreaks: F,
        textRuns: [{
          ...B,
          st: 0,
          ed: M.length
        }],
        tables: [
          {
            startIndex: 0,
            endIndex: M.length,
            tableId: Y.tableId
          }
        ]
      },
      len: M.length
    });
    const oe = le(d, A);
    S.push(R.editOp(v.serialize(), oe));
    const ce = R.insertOp(["tableSource", Y.tableId], Y);
    return S.push(ce), O.params.actions = S.reduce((we, Yt) => k.compose(we, Yt), null), !!i.syncExecuteCommand(O.id, O.params);
  }
}, Uo = "doc.component.create-table-confirm", sr = {
  id: "doc.operation.create-table",
  type: N.COMMAND,
  handler: async (n) => {
    const e = n.get(Ze), t = n.get(Bc), o = n.get(y), s = {
      rowCount: 3,
      colCount: 5
    }, r = (i, a) => {
      s.rowCount = i, s.colCount = a;
    };
    return await t.open({
      id: Uo,
      children: {
        label: {
          name: Ca,
          props: {
            handleRowColChange: r,
            tableCreateParams: s
          }
        }
      },
      width: 400,
      title: { title: e.t("toolbar.table.insert") },
      onConfirm: () => {
        o.executeCommand(ba.id, s), t.close(Uo);
      },
      onClose: () => {
        t.close(Uo);
      }
    }), !0;
  }
}, qe = {
  id: "doc-paragraph-setting.command",
  type: N.COMMAND,
  handler: async (n, e) => {
    var m, E;
    const t = n.get(G), o = n.get(Q), s = n.get(y), r = o.getCurrentUnitForType(_.UNIVER_DOC), i = t.getDocRanges();
    if (!r || i.length === 0 || !e)
      return !1;
    const a = i[0].segmentId, c = r.getUnitId(), A = (E = (m = r.getSelfOrHeaderFooterModel(a).getBody()) == null ? void 0 : m.paragraphs) != null ? E : [], l = mn(i, A), d = {
      id: J.id,
      params: {
        unitId: c,
        actions: [],
        textRanges: i
      }
    }, h = new St();
    h.reset();
    const u = new me(), g = k.getInstance();
    for (const I of l) {
      const { startIndex: v } = I;
      u.push({
        t: W.RETAIN,
        len: v - h.cursor
      });
      const R = {
        ...I.paragraphStyle,
        ...e.paragraph
      };
      u.push({
        t: W.RETAIN,
        len: 1,
        body: {
          dataStream: "",
          paragraphs: [
            {
              ...I,
              paragraphStyle: R,
              startIndex: 0
            }
          ]
        },
        coverType: no.REPLACE
      }), h.moveCursorTo(v + 1);
    }
    const f = le(r, a);
    return d.params.actions = g.editOp(u.serialize(), f), !!s.syncExecuteCommand(d.id, d.params);
  }
}, kd = () => {
  const n = $(G), e = $(Lt), t = Fe(() => n.getDocRanges(), []);
  return Re(() => {
    t.length || e.closePanel();
  }, [t]), t;
}, Vd = () => {
  var i, a;
  const e = $(Q).getCurrentUnitForType(_.UNIVER_DOC), t = kd();
  if (!e || t.length === 0)
    return [];
  const o = t[0].segmentId, s = (a = (i = e.getSelfOrHeaderFooterModel(o).getBody()) == null ? void 0 : i.paragraphs) != null ? a : [];
  return mn(t, s);
}, jd = (n, e) => {
  const t = $(y), [o, s] = ve(() => {
    var a, c;
    const i = n[0];
    return i ? String((c = (a = i.paragraphStyle) == null ? void 0 : a.horizontalAlign) != null ? c : e) : e;
  });
  return [o, (i) => (s(i), t.executeCommand(qe.id, {
    paragraph: { horizontalAlign: Number(i) }
  }))];
}, Wd = (n) => {
  const e = $(y), [t, o] = ve(() => {
    var i;
    const r = n[0];
    return r ? ze((i = r.paragraphStyle) == null ? void 0 : i.indentStart, 0) : 0;
  });
  return [t, (r) => (o(r), e.executeCommand(qe.id, {
    paragraph: { indentStart: { v: r } }
  }))];
}, zd = (n) => {
  const e = $(y), [t, o] = ve(() => {
    var i;
    const r = n[0];
    return r ? ze((i = r.paragraphStyle) == null ? void 0 : i.indentEnd, 0) : 0;
  });
  return [t, (r) => (o(r), e.executeCommand(qe.id, {
    paragraph: { indentEnd: { v: r } }
  }))];
}, Gd = (n) => {
  const e = $(y), [t, o] = ve(() => {
    var i;
    const r = n[0];
    return r ? ze((i = r.paragraphStyle) == null ? void 0 : i.indentFirstLine, 0) : 0;
  });
  return [t, (r) => (o(r), e.executeCommand(qe.id, {
    paragraph: { indentFirstLine: { v: r } }
  }))];
}, Yd = (n) => {
  const e = $(y), [t, o] = ve(() => {
    var i;
    const r = n[0];
    return r ? ze((i = r.paragraphStyle) == null ? void 0 : i.hanging, 0) : 0;
  });
  return [t, (r) => (o(r), e.executeCommand(qe.id, {
    paragraph: { hanging: { v: r } }
  }))];
}, qd = (n) => {
  const e = $(y), [t, o] = ve(() => {
    var i;
    const r = n[0];
    return r ? ze((i = r.paragraphStyle) == null ? void 0 : i.spaceAbove, 0) : 0;
  });
  return [t, (r) => (o(r), e.executeCommand(qe.id, {
    paragraph: { spaceAbove: { v: r } }
  }))];
}, Kd = (n) => {
  const e = $(y), [t, o] = ve(() => {
    var i;
    const r = n[0];
    return r ? ze((i = r.paragraphStyle) == null ? void 0 : i.spaceBelow, 0) : 0;
  });
  return [t, (r) => (o(r), e.executeCommand(qe.id, {
    paragraph: { spaceBelow: { v: r } }
  }))];
}, Xd = (n) => {
  const e = $(y), t = $(fe), o = $(Q), s = Fe(() => {
    var g;
    const u = o.getCurrentUnitForType(_.UNIVER_DOC);
    if (u)
      return (g = t.getRenderById(u == null ? void 0 : u.getUnitId())) == null ? void 0 : g.with(ie).getSkeleton();
  }, []), r = Fe(() => new Le({}), []), [i, a] = ve(() => {
    var g, f;
    const u = n[0];
    return u && (f = (g = u.paragraphStyle) == null ? void 0 : g.lineSpacing) != null ? f : 1;
  }), c = cn(i), [A, l] = ve(() => {
    var g, f;
    const u = n[0];
    return u ? (f = (g = u.paragraphStyle) == null ? void 0 : g.spacingRule) != null ? f : Bt.AUTO : Bt.AUTO;
  }), d = async (u) => {
    a(u), r.next({ lineSpacing: u, spacingRule: A });
  }, h = async (u) => {
    if (u !== A) {
      let g = c.current;
      if (u === Bt.AT_LEAST) {
        const f = s == null ? void 0 : s.findNodeByCharIndex(n[0].startIndex), p = f == null ? void 0 : f.parent, m = p == null ? void 0 : p.parent;
        (m == null ? void 0 : m.contentHeight) !== void 0 && (g = Math.max(m.contentHeight, g));
      } else
        g > 5 && (g = 2);
      c.current = i, d(g), l(u), r.next({ spacingRule: u });
    }
  };
  return Re(() => {
    const u = r.pipe(
      zo((g) => !!Object.keys(g).length),
      Gc(16),
      zo((g) => !!g.length),
      Yc((g) => g.reduce((f, p) => (Object.keys(p).forEach((m) => {
        f[m] = p[m];
      }), f), {}))
    ).subscribe((g) => e.executeCommand(qe.id, {
      paragraph: { ...g }
    }));
    return () => u.unsubscribe();
  }, []), {
    lineSpacing: [i, d],
    spacingRule: [A, h]
  };
}, Jd = "univer-paragraph-setting-icon-list", Zd = "univer-paragraph-setting-icon-list-item", $d = "univer-paragraph-setting-icon-list-active", eu = "univer-paragraph-setting-title", tu = "univer-paragraph-setting-label", nu = "univer-paragraph-setting-mt-base", ou = "univer-paragraph-setting-flex-col", su = "univer-paragraph-setting-space-line", re = {
  paragraphSettingIconList: Jd,
  paragraphSettingIconListItem: Zd,
  paragraphSettingIconListActive: $d,
  paragraphSettingTitle: eu,
  paragraphSettingLabel: tu,
  paragraphSettingMtBase: nu,
  paragraphSettingFlexCol: ou,
  paragraphSettingSpaceLine: su
}, ht = (n) => {
  const { value: e, onChange: t, className: o = "", min: s = 0, max: r = 100, step: i = 1 } = n, a = Hc.useRef(null);
  return /* @__PURE__ */ w.jsx(
    An,
    {
      step: i,
      ref: a,
      min: s,
      max: r,
      value: e,
      onChange: (c) => {
        t(c != null ? c : 0).finally(() => {
          setTimeout(() => {
            var A;
            (A = a.current) == null || A.focus();
          }, 30);
        });
      },
      className: o
    }
  );
};
function ru() {
  const n = $(Ze), e = Fe(
    () => [
      { label: n.t("toolbar.alignLeft"), value: String(_e.LEFT), icon: /* @__PURE__ */ w.jsx(Ji, {}) },
      { label: n.t("toolbar.alignCenter"), value: String(_e.CENTER), icon: /* @__PURE__ */ w.jsx(Xi, {}) },
      { label: n.t("toolbar.alignRight"), value: String(_e.RIGHT), icon: /* @__PURE__ */ w.jsx(Zi, {}) },
      { label: n.t("toolbar.alignJustify"), value: String(_e.JUSTIFIED), icon: /* @__PURE__ */ w.jsx(Ki, {}) }
    ],
    []
  ), t = Vd(), [o, s] = jd(t, e[0].value), [r, i] = Wd(t), [a, c] = zd(t), [A, l] = Gd(t), [d, h] = Yd(t), [u, g] = qd(t), [f, p] = Kd(t), { lineSpacing: [m, E], spacingRule: [I, v] } = Xd(t), R = Fe(() => I === Bt.AUTO ? { min: 1, max: 5, step: m < 2 ? 0.5 : 1 } : { min: 1, max: 100 }, [I, m]);
  return /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSetting, children: [
    /* @__PURE__ */ w.jsx("div", { className: re.paragraphSettingTitle, children: n.t("doc.paragraphSetting.alignment") }),
    /* @__PURE__ */ w.jsx(
      "div",
      {
        className: `
              ${re.paragraphSettingIconList}
              ${re.paragraphSettingMtBase}
            `,
        children: e.map((S) => /* @__PURE__ */ w.jsx(Xc, { title: S.label, placement: "bottom", children: /* @__PURE__ */ w.jsx(
          "span",
          {
            className: Un(
              re.paragraphSettingIconListItem,
              { [re.paragraphSettingIconListActive]: o === S.value }
            ),
            onClick: () => s(S.value),
            children: S.icon
          }
        ) }, S.value))
      }
    ),
    /* @__PURE__ */ w.jsx("div", { className: re.paragraphSettingTitle, children: n.t("doc.paragraphSetting.indentation") }),
    /* @__PURE__ */ w.jsxs("div", { children: [
      /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingFlexCol, children: [
        /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingLabel, children: [
          n.t("doc.paragraphSetting.left"),
          "(px)"
        ] }),
        /* @__PURE__ */ w.jsx(ht, { className: re.paragraphSettingMtBase, value: r, onChange: (S) => i(S != null ? S : 0) })
      ] }),
      /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingFlexCol, children: [
        /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingLabel, children: [
          n.t("doc.paragraphSetting.right"),
          "(px)"
        ] }),
        /* @__PURE__ */ w.jsx(ht, { className: re.paragraphSettingMtBase, value: a, onChange: (S) => c(S != null ? S : 0) })
      ] }),
      /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingFlexCol, children: [
        /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingLabel, children: [
          n.t("doc.paragraphSetting.firstLine"),
          "(px)"
        ] }),
        /* @__PURE__ */ w.jsx(ht, { className: re.paragraphSettingMtBase, value: A, onChange: (S) => l(S != null ? S : 0) })
      ] }),
      /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingFlexCol, children: [
        /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingLabel, children: [
          n.t("doc.paragraphSetting.hanging"),
          "(px)"
        ] }),
        /* @__PURE__ */ w.jsx(ht, { className: re.paragraphSettingMtBase, value: d, onChange: (S) => h(S != null ? S : 0) })
      ] })
    ] }),
    /* @__PURE__ */ w.jsx("div", { className: re.paragraphSettingTitle, children: n.t("doc.paragraphSetting.spacing") }),
    /* @__PURE__ */ w.jsxs("div", { children: [
      /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingFlexCol, children: [
        /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingLabel, children: [
          n.t("doc.paragraphSetting.before"),
          "(px)"
        ] }),
        /* @__PURE__ */ w.jsx(ht, { className: re.paragraphSettingMtBase, value: u, onChange: (S) => g(S != null ? S : 0) })
      ] }),
      /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingFlexCol, children: [
        /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingLabel, children: [
          n.t("doc.paragraphSetting.after"),
          "(px)"
        ] }),
        /* @__PURE__ */ w.jsx(ht, { className: re.paragraphSettingMtBase, value: f, onChange: (S) => p(S != null ? S : 0) })
      ] }),
      /* @__PURE__ */ w.jsxs("div", { className: re.paragraphSettingFlexCol, children: [
        /* @__PURE__ */ w.jsx("div", { className: re.paragraphSettingLabel, children: n.t("doc.paragraphSetting.lineSpace") }),
        /* @__PURE__ */ w.jsxs(
          "div",
          {
            className: `
                          ${re.paragraphSettingMtBase}
                          ${re.paragraphSettingSpaceLine}
                        `,
            style: { width: 162 },
            children: [
              /* @__PURE__ */ w.jsx(
                Jc,
                {
                  value: `${I}`,
                  options: [
                    { label: n.t("doc.paragraphSetting.multiSpace"), value: `${Bt.AUTO}` },
                    { label: n.t("doc.paragraphSetting.fixedValue"), value: `${Bt.AT_LEAST}` }
                  ],
                  onChange: (S) => v(Number(S))
                }
              ),
              /* @__PURE__ */ w.jsx(
                ht,
                {
                  ...R,
                  value: m,
                  onChange: (S) => E(S != null ? S : 0)
                }
              )
            ]
          }
        )
      ] })
    ] })
  ] });
}
const iu = (n, e) => e.length === n.length && n.some((t) => e.some((o) => o.startOffset === t.startOffset && o.endOffset === t.endOffset));
function au() {
  const n = $(y), e = $(Ze), t = Nn(e.currentLocale$), [o, s] = ve(""), r = Fe(() => fi(() => s(pt(4)), 300), []), i = cn([]);
  return Re(() => {
    const a = n.onCommandExecuted((c) => {
      if (De.id === c.id) {
        const A = c.params.ranges;
        iu(A, i.current) || s(pt(4)), i.current = A;
      }
      J.id === c.id && c.params.trigger !== qe.id && r();
    });
    return () => a.dispose();
  }, [r]), Re(() => {
    s(pt(4));
  }, [t]), Re(() => () => r.cancel(), [r]), /* @__PURE__ */ w.jsx(ru, {}, o);
}
var cu = Object.defineProperty, Au = Object.getOwnPropertyDescriptor, lu = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Au(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && cu(e, t, s), s;
}, Lo = (n, e) => (t, o) => e(t, o, n);
const ei = "doc_ui_paragraph-setting-panel";
let Lt = class extends ue {
  constructor(e, t, o) {
    super();
    x(this, "_id");
    this._commandService = e, this._componentManager = t, this._sidebarService = o, this._init();
  }
  _init() {
    this.disposeWithMe(this._componentManager.register(ei, au));
  }
  openPanel() {
    const e = {
      header: { title: "doc.slider.paragraphSetting" },
      id: this._id,
      children: {
        label: ei
      },
      width: 300
    };
    this._sidebarService.open(e);
  }
  closePanel() {
    this._sidebarService.close(this._id);
  }
};
Lt = lu([
  Lo(0, y),
  Lo(1, z(io)),
  Lo(2, z(Bi))
], Lt);
const rr = {
  id: "sidebar.operation.doc-paragraph-setting-panel",
  type: N.OPERATION,
  handler: (n) => (n.get(Lt).openPanel(), !0)
}, ir = (n) => {
  const e = n.get(G);
  return new pe((t) => {
    const o = e.textSelection$.subscribe(() => {
      e.getDocRanges().some((i) => i.collapsed === !1 || i.rangeType === Ge.RECT) ? t.next(!1) : t.next(!0);
    });
    return () => o.unsubscribe();
  });
};
function du(n) {
  if (n.length < 2)
    return !0;
  const e = n.map((t) => t.tableId);
  return e.every((t) => t === e[0]);
}
function ti(n, e, t) {
  var r;
  const o = e.getRectRanges(), s = e.getActiveTextRange();
  if (o && o.length && du(o) && s == null) {
    n.next(!1);
    return;
  }
  if (s && (o == null || o.length === 0)) {
    const { segmentId: i, startOffset: a, endOffset: c } = s, A = t.getCurrentUniverDocInstance(), l = (r = A == null ? void 0 : A.getSelfOrHeaderFooterModel(i).getBody()) == null ? void 0 : r.tables;
    if (l && l.length && l.some((d) => {
      const { startIndex: h, endIndex: u } = d;
      return a > h && a < u || c > h && c < u;
    })) {
      n.next(!1);
      return;
    }
  }
  n.next(!0);
}
const tt = (n) => {
  const e = n.get(G), t = n.get(Q);
  return new pe((o) => {
    const s = e.textSelection$.subscribe(() => {
      ti(o, e, t);
    });
    return ti(o, e, t), () => s.unsubscribe();
  });
}, uu = (n) => ({
  id: Fn.name,
  commandId: Fn.id,
  type: Z.BUTTON,
  icon: "Copy",
  title: "rightClick.copy",
  disabled$: ir(n),
  hidden$: ee(n, _.UNIVER_DOC)
}), hu = (n) => ({
  id: rr.id,
  type: Z.BUTTON,
  icon: "MenuSingle24",
  title: "doc.menu.paragraphSetting",
  hidden$: ee(n, _.UNIVER_DOC)
}), gu = (n) => ({
  id: qs.id,
  type: Z.BUTTON,
  icon: "Copy",
  title: "rightClick.cut",
  disabled$: ir(n),
  hidden$: ee(n, _.UNIVER_DOC)
}), fu = (n) => ({
  id: Ks.id,
  type: Z.BUTTON,
  icon: "PasteSpecial",
  title: "rightClick.paste",
  hidden$: ee(n, _.UNIVER_DOC)
}), pu = (n) => ({
  id: So.id,
  type: Z.BUTTON,
  icon: "PasteSpecial",
  title: "rightClick.delete",
  disabled$: ir(n),
  hidden$: ee(n, _.UNIVER_DOC)
}), xa = "doc.menu.table-insert";
function mu(n) {
  return {
    id: xa,
    type: Z.SUBITEMS,
    title: "table.insert",
    icon: "Insert",
    hidden$: ao(ee(n, _.UNIVER_DOC), tt(n), (e, t) => e || t)
  };
}
function Eu(n) {
  return {
    id: er.id,
    type: Z.BUTTON,
    title: "table.insertRowAbove",
    icon: "InsertRowAbove",
    disabled$: tt(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Su(n) {
  return {
    id: tr.id,
    type: Z.BUTTON,
    title: "table.insertRowBelow",
    icon: "InsertRowBelow",
    disabled$: tt(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Iu(n) {
  return {
    id: nr.id,
    type: Z.BUTTON,
    title: "table.insertColumnLeft",
    icon: "LeftInsertColumn",
    disabled$: tt(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Cu(n) {
  return {
    id: or.id,
    type: Z.BUTTON,
    title: "table.insertColumnRight",
    icon: "RightInsertColumn",
    disabled$: tt(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
const Oa = "doc.menu.table-delete";
function vu(n) {
  return {
    id: Oa,
    type: Z.SUBITEMS,
    title: "table.delete",
    icon: "Reduce",
    hidden$: ao(ee(n, _.UNIVER_DOC), tt(n), (e, t) => e || t)
  };
}
function Ru(n) {
  return {
    id: Xs.id,
    type: Z.BUTTON,
    title: "table.deleteRows",
    icon: "DeleteRow",
    disabled$: tt(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function bu(n) {
  return {
    id: Js.id,
    type: Z.BUTTON,
    title: "table.deleteColumns",
    icon: "DeleteColumn",
    disabled$: tt(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function xu(n) {
  return {
    id: In.id,
    type: Z.BUTTON,
    title: "table.deleteTable",
    icon: "GridSingle",
    disabled$: tt(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Ou(n) {
  const e = n.get(Q), t = n.get(fe);
  return new pe((o) => {
    const s = e.focused$.subscribe((a) => {
      if (a == null || e.getUnitType(a) !== _.UNIVER_DOC)
        return o.next(!0);
      const A = t.getRenderById(a);
      if (A == null)
        return o.next(!0);
      A.with(ie).getViewModel().editAreaChange$.subscribe((d) => {
        o.next(d === ge.HEADER || d === ge.FOOTER);
      });
    }), r = t.getCurrentTypeOfRenderer(_.UNIVER_DOC);
    if (r == null)
      return o.next(!0);
    const i = r.with(ie).getViewModel();
    return o.next(i.getEditArea() !== ge.BODY), () => s.unsubscribe();
  });
}
function Tu(n) {
  const e = n.get(Q), t = n.get(y);
  return new pe((o) => {
    const s = t.onCommandExecuted((c) => {
      if (c.id === J.id) {
        const { unitId: A } = c.params, l = e.getUnit(A);
        if (l == null) {
          o.next(!0);
          return;
        }
        const { documentStyle: d } = l.getSnapshot();
        o.next((d == null ? void 0 : d.documentFlavor) !== ye.TRADITIONAL);
      }
    }), r = e.focused$.subscribe((c) => {
      if (c == null)
        return o.next(!0);
      const A = e.getUniverDocInstance(c), l = A == null ? void 0 : A.getSnapshot().documentStyle.documentFlavor;
      o.next(l !== ye.TRADITIONAL);
    }), i = e.getCurrentUniverDocInstance();
    if (i == null)
      return o.next(!0);
    const a = i == null ? void 0 : i.getSnapshot().documentStyle.documentFlavor;
    return o.next(a !== ye.TRADITIONAL), () => {
      s.dispose(), r.unsubscribe();
    };
  });
}
function yu(n) {
  const e = n.get(G), t = n.get(Q);
  return new pe((o) => {
    const s = e.textSelection$.subscribe((r) => {
      if (r == null) {
        o.next(!0);
        return;
      }
      const { textRanges: i } = r;
      if (i.length !== 1) {
        o.next(!0);
        return;
      }
      const a = i[0], { collapsed: c, startNodePosition: A, startOffset: l } = a;
      if (!c || l == null) {
        o.next(!0);
        return;
      }
      const d = t.getCurrentUniverDocInstance();
      if (d == null) {
        o.next(!0);
        return;
      }
      const h = ke(n, d.getUnitId());
      if (h == null) {
        o.next(!0);
        return;
      }
      if (h.getViewModel().getCustomRangeRaw(l)) {
        o.next(!0);
        return;
      }
      if (A != null) {
        const { path: f } = A;
        if (f.indexOf("cells") !== -1) {
          o.next(!0);
          return;
        }
      }
      o.next(!1);
    });
    return () => s.unsubscribe();
  });
}
function be(n) {
  const e = n.get(G);
  return new pe((t) => {
    const o = e.textSelection$.subscribe((s) => {
      if (s == null) {
        t.next(!0);
        return;
      }
      const { textRanges: r, rectRanges: i } = s;
      if (r.length === 0 && i.length === 0) {
        t.next(!0);
        return;
      }
      t.next(!1);
    });
    return () => o.unsubscribe();
  });
}
function Bu(n) {
  const e = n.get(y);
  return {
    id: Vt.id,
    type: Z.BUTTON,
    icon: "BoldSingle",
    title: "Set bold",
    tooltip: "toolbar.bold",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === lt.id) {
          const a = dt(n);
          if (a == null) {
            t.next(!1);
            return;
          }
          const c = (i = a.ts) == null ? void 0 : i.bl;
          t.next(c === L.TRUE);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Mu(n) {
  const e = n.get(y);
  return {
    id: jt.id,
    type: Z.BUTTON,
    icon: "ItalicSingle",
    title: "Set italic",
    tooltip: "toolbar.italic",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === lt.id) {
          const a = dt(n);
          if (a == null) {
            t.next(!1);
            return;
          }
          const c = (i = a.ts) == null ? void 0 : i.it;
          t.next(c === L.TRUE);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function _u(n) {
  const e = n.get(y);
  return {
    id: Wt.id,
    type: Z.BUTTON,
    icon: "UnderlineSingle",
    title: "Set underline",
    tooltip: "toolbar.underline",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === lt.id) {
          const a = dt(n);
          if (a == null) {
            t.next(!1);
            return;
          }
          const c = (i = a.ts) == null ? void 0 : i.ul;
          t.next((c == null ? void 0 : c.s) === L.TRUE);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Pu(n) {
  const e = n.get(y);
  return {
    id: zt.id,
    type: Z.BUTTON,
    icon: "StrikethroughSingle",
    title: "Set strike through",
    tooltip: "toolbar.strikethrough",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === lt.id) {
          const a = dt(n);
          if (a == null) {
            t.next(!1);
            return;
          }
          const c = (i = a.ts) == null ? void 0 : i.st;
          t.next((c == null ? void 0 : c.s) === L.TRUE);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Du(n) {
  const e = n.get(y);
  return {
    id: Ct.id,
    type: Z.BUTTON,
    icon: "SubscriptSingle",
    tooltip: "toolbar.subscript",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === lt.id) {
          const a = dt(n);
          if (a == null) {
            t.next(!1);
            return;
          }
          const c = (i = a.ts) == null ? void 0 : i.va;
          t.next(c === Ne.SUBSCRIPT);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function wu(n) {
  const e = n.get(y);
  return {
    id: Gt.id,
    type: Z.BUTTON,
    icon: "SuperscriptSingle",
    tooltip: "toolbar.superscript",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === lt.id) {
          const a = dt(n);
          if (a == null) {
            t.next(!1);
            return;
          }
          const c = (i = a.ts) == null ? void 0 : i.va;
          t.next(c === Ne.SUPERSCRIPT);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Nu(n) {
  const e = n.get(y);
  return {
    id: Dt.id,
    tooltip: "toolbar.font",
    type: Z.SELECTOR,
    label: oa,
    selections: Mc.map((t) => ({
      label: {
        name: sa,
        hoverable: !0
      },
      value: t.value
    })),
    // disabled$: getCurrentSheetDisabled$(accessor),
    value$: new pe((t) => {
      const o = Ci.ff, s = e.onCommandExecuted((r) => {
        var a;
        const i = r.id;
        if (i === De.id || i === Dt.id) {
          const c = dt(n);
          if (c == null) {
            t.next(o);
            return;
          }
          const A = (a = c.ts) == null ? void 0 : a.ff;
          t.next(A != null ? A : o);
        }
      });
      return t.next(o), s.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Qu(n) {
  const e = n.get(y);
  return {
    id: Pt.id,
    type: Z.SELECTOR,
    tooltip: "toolbar.fontSize",
    label: {
      name: ra,
      props: {
        min: 1,
        max: 400
        // disabled$,
      }
    },
    selections: _c,
    // disabled$,
    value$: new pe((t) => {
      const o = Ci.fs, s = e.onCommandExecuted((r) => {
        var a;
        const i = r.id;
        if (i === De.id || i === Pt.id) {
          const c = dt(n);
          if (c == null) {
            t.next(o);
            return;
          }
          const A = (a = c.ts) == null ? void 0 : a.fs;
          t.next(A != null ? A : o);
        }
      });
      return t.next(o), s.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Uu(n) {
  const e = n.get(y), t = n.get(vi);
  return {
    id: wt.id,
    icon: "FontColor",
    tooltip: "toolbar.textColor.main",
    type: Z.BUTTON_SELECTOR,
    selections: [
      {
        label: {
          name: Ds,
          hoverable: !1
        }
      }
    ],
    value$: new pe((o) => {
      const s = t.getCurrentTheme().textColor, r = e.onCommandExecuted((i) => {
        if (i.id === wt.id) {
          const a = i.params.value;
          o.next(a != null ? a : s);
        }
      });
      return o.next(s), r.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
    // disabled$: getCurrentSheetDisabled$(accessor),
  };
}
function Lu(n) {
  return {
    id: _s.id,
    type: Z.BUTTON,
    icon: "HeaderFooterSingle",
    tooltip: "toolbar.headerFooter",
    hidden$: ao(ee(n, _.UNIVER_DOC, void 0, $e), Tu(n), (e, t) => e || t)
  };
}
const Fu = "GridSingle", Ta = "doc.menu.table";
function Hu(n) {
  return {
    id: Ta,
    type: Z.SUBITEMS,
    icon: Fu,
    tooltip: "toolbar.table.main",
    disabled$: yu(n),
    // Do not show header footer menu and insert table at zen mode.
    hidden$: ao(ee(n, _.UNIVER_DOC, void 0, $e), Ou(n), (e, t) => e || t)
  };
}
function ku(n) {
  return {
    id: sr.id,
    title: "toolbar.table.insert",
    type: Z.BUTTON,
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function Vu(n) {
  const e = n.get(y);
  return {
    id: go.id,
    type: Z.BUTTON,
    icon: "LeftJustifyingSingle",
    tooltip: "toolbar.alignLeft",
    disabled$: be(n),
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === et.id) {
          const a = vo(n);
          if (a == null)
            return;
          const c = (i = a.paragraphStyle) == null ? void 0 : i.horizontalAlign;
          t.next(c === _e.LEFT);
        }
      });
      return t.next(!1), o.dispose;
    }),
    hidden$: ee(n, _.UNIVER_DOC, void 0, $e)
  };
}
function ju(n) {
  const e = n.get(y);
  return {
    id: fo.id,
    type: Z.BUTTON,
    icon: "HorizontallySingle",
    tooltip: "toolbar.alignCenter",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === et.id) {
          const a = vo(n);
          if (a == null)
            return;
          const c = (i = a.paragraphStyle) == null ? void 0 : i.horizontalAlign;
          t.next(c === _e.CENTER);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC, void 0, $e)
  };
}
function Wu(n) {
  const e = n.get(y);
  return {
    id: po.id,
    type: Z.BUTTON,
    icon: "RightJustifyingSingle",
    tooltip: "toolbar.alignRight",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === et.id) {
          const a = vo(n);
          if (a == null)
            return;
          const c = (i = a.paragraphStyle) == null ? void 0 : i.horizontalAlign;
          t.next(c === _e.RIGHT);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC, void 0, $e)
  };
}
function zu(n) {
  const e = n.get(y);
  return {
    id: mo.id,
    type: Z.BUTTON,
    icon: "AlignTextBothSingle",
    tooltip: "toolbar.alignJustify",
    activated$: new pe((t) => {
      const o = e.onCommandExecuted((s) => {
        var i;
        const r = s.id;
        if (r === De.id || r === et.id) {
          const a = vo(n);
          if (a == null)
            return;
          const c = (i = a.paragraphStyle) == null ? void 0 : i.horizontalAlign;
          t.next(c === _e.JUSTIFIED);
        }
      });
      return t.next(!1), o.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC, void 0, $e)
  };
}
const un = (n) => new pe((e) => {
  const t = n.get(Q), o = n.get(G);
  let s;
  const r = t.focused$.subscribe((i) => {
    if (s == null || s.unsubscribe(), i == null)
      return;
    const a = t.getUniverDocInstance(i);
    a != null && (s = o.textSelection$.subscribe(() => {
      var l, d, h;
      const c = o.getDocRanges(), A = (l = c.find((u) => u.isActive)) != null ? l : c[0];
      if (A) {
        const u = a.getSelfOrHeaderFooterModel(A == null ? void 0 : A.segmentId), g = Qs(A, (h = (d = u.getBody()) == null ? void 0 : d.paragraphs) != null ? h : []);
        let f;
        if (g.every((p) => {
          var m;
          return f || (f = (m = p.bullet) == null ? void 0 : m.listType), p.bullet && p.bullet.listType === f;
        })) {
          e.next(f);
          return;
        }
      }
      e.next(void 0);
    }));
  });
  return () => {
    r.unsubscribe(), s == null || s.unsubscribe();
  };
});
function Gu(n) {
  return {
    id: ho.id,
    type: Z.BUTTON_SELECTOR,
    selections: [
      {
        label: {
          name: aa,
          hoverable: !1
        },
        value$: un(n)
      }
    ],
    icon: "OrderSingle",
    tooltip: "toolbar.order",
    hidden$: ee(n, _.UNIVER_DOC),
    disabled$: be(n),
    activated$: un(n).pipe(gn((e) => e && e.indexOf("ORDER_LIST") === 0))
  };
}
function Yu(n) {
  return {
    id: uo.id,
    type: Z.BUTTON_SELECTOR,
    selections: [
      {
        label: {
          name: ca,
          hoverable: !1
        },
        value$: un(n)
      }
    ],
    icon: "UnorderSingle",
    tooltip: "toolbar.unorder",
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC),
    activated$: un(n).pipe(gn((e) => e && e.indexOf("BULLET_LIST") === 0))
  };
}
function qu(n) {
  return {
    id: ws.id,
    type: Z.BUTTON,
    icon: "TodoList",
    tooltip: "toolbar.checklist",
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC),
    activated$: un(n).pipe(gn((e) => e && e.indexOf("CHECK_LIST") === 0))
  };
}
function Ku(n) {
  const e = n.get(y), t = n.get(Q);
  return {
    id: Co.id,
    type: Z.BUTTON,
    icon: "KeyboardSingle",
    tooltip: "toolbar.documentFlavor",
    hidden$: ee(n, _.UNIVER_DOC, void 0, $e),
    activated$: new pe((o) => {
      var i;
      const s = e.onCommandExecuted((a) => {
        var c;
        if (a.id === J.id) {
          const A = t.getCurrentUnitForType(_.UNIVER_DOC);
          o.next(((c = A == null ? void 0 : A.getSnapshot()) == null ? void 0 : c.documentStyle.documentFlavor) === ye.MODERN);
        }
      }), r = t.getCurrentUnitForType(_.UNIVER_DOC);
      return o.next(((i = r == null ? void 0 : r.getSnapshot()) == null ? void 0 : i.documentStyle.documentFlavor) === ye.MODERN), () => s.dispose();
    })
  };
}
function Xu(n) {
  return {
    id: fn.id,
    type: Z.BUTTON,
    title: "toolbar.resetColor",
    icon: "NoColor"
  };
}
function Ju(n) {
  const e = n.get(y), t = n.get(vi);
  return {
    id: Nt.id,
    tooltip: "toolbar.fillColor.main",
    type: Z.BUTTON_SELECTOR,
    icon: "PaintBucket",
    selections: [
      {
        label: {
          name: Ds,
          hoverable: !1
        }
      }
    ],
    value$: new pe((o) => {
      const s = t.getCurrentTheme().primaryColor, r = e.onCommandExecuted((i) => {
        if (i.id === Nt.id) {
          const a = i.params.value;
          o.next(a != null ? a : s);
        }
      });
      return o.next(s), r.dispose;
    }),
    disabled$: be(n),
    hidden$: ee(n, _.UNIVER_DOC)
  };
}
function dt(n) {
  var h, u;
  const e = n.get(Q), t = n.get(G), o = n.get(Je), s = e.getCurrentUnitForType(_.UNIVER_DOC), r = t.getDocRanges(), i = (h = r.find((g) => g.isActive)) != null ? h : r[0], a = o.getDefaultStyle(), c = (u = o.getStyleCache()) != null ? u : {};
  if (s == null || i == null)
    return {
      ts: {
        ...a,
        ...c
      }
    };
  const { segmentId: A } = i, l = s.getSelfOrHeaderFooterModel(A).getBody();
  return l == null ? {
    ts: {
      ...a,
      ...c
    }
  } : {
    ts: {
      ...la(l, i, a),
      ...c
    }
  };
}
function vo(n) {
  var l, d;
  const e = n.get(Q), t = n.get(G), o = e.getCurrentUniverDocInstance(), s = t.getDocRanges(), r = (l = s.find((h) => h.isActive)) != null ? l : s[0];
  if (o == null || r == null)
    return;
  const { startOffset: i, segmentId: a } = r, c = (d = o.getSelfOrHeaderFooterModel(a).getBody()) == null ? void 0 : d.paragraphs;
  if (c == null)
    return;
  let A = -1;
  for (const h of c) {
    const { startIndex: u } = h;
    if (i > A && i <= u)
      return h;
    A = u;
  }
  return null;
}
const Zu = {
  [Ir.FORMAT]: {
    [Vt.id]: {
      order: 0,
      menuItemFactory: Bu
    },
    [jt.id]: {
      order: 1,
      menuItemFactory: Mu
    },
    [Wt.id]: {
      order: 2,
      menuItemFactory: _u
    },
    [zt.id]: {
      order: 3,
      menuItemFactory: Pu
    },
    [Ct.id]: {
      order: 4,
      menuItemFactory: Du
    },
    [Gt.id]: {
      order: 5,
      menuItemFactory: wu
    },
    [Pt.id]: {
      order: 6,
      menuItemFactory: Qu
    },
    [Dt.id]: {
      order: 7,
      menuItemFactory: Nu
    },
    [wt.id]: {
      order: 8,
      menuItemFactory: Uu
    },
    [Nt.id]: {
      order: 9,
      menuItemFactory: Ju,
      [fn.id]: {
        order: 0,
        menuItemFactory: Xu
      }
    }
  },
  [Ir.LAYOUT]: {
    [Ta]: {
      order: 1,
      menuItemFactory: Hu,
      [sr.id]: {
        order: 0,
        menuItemFactory: ku
      }
    },
    [go.id]: {
      order: 2,
      menuItemFactory: Vu
    },
    [fo.id]: {
      order: 3,
      menuItemFactory: ju
    },
    [po.id]: {
      order: 4,
      menuItemFactory: Wu
    },
    [mo.id]: {
      order: 5,
      menuItemFactory: zu
    },
    [ho.id]: {
      order: 6,
      menuItemFactory: Gu
    },
    [uo.id]: {
      order: 7,
      menuItemFactory: Yu
    },
    [ws.id]: {
      order: 8,
      menuItemFactory: qu
    },
    [_s.id]: {
      order: 9,
      menuItemFactory: Lu
    },
    [Co.id]: {
      order: 10,
      menuItemFactory: Ku
    }
  },
  [Ui.MAIN_AREA]: {
    [Cr.FORMAT]: {
      [Fn.name]: {
        order: 0,
        menuItemFactory: uu
      },
      [qs.id]: {
        order: 1,
        menuItemFactory: gu
      },
      [Ks.id]: {
        order: 2,
        menuItemFactory: fu
      },
      [So.id]: {
        order: 3,
        menuItemFactory: pu
      }
    },
    [Cr.LAYOUT]: {
      [rr.id]: {
        order: 0,
        menuItemFactory: hu
      },
      [xa]: {
        order: 1,
        menuItemFactory: mu,
        [er.id]: {
          order: 1,
          menuItemFactory: Eu
        },
        [tr.id]: {
          order: 2,
          menuItemFactory: Su
        },
        [nr.id]: {
          order: 3,
          menuItemFactory: Iu
        },
        [or.id]: {
          order: 4,
          menuItemFactory: Cu
        }
      },
      [Oa]: {
        order: 2,
        menuItemFactory: vu,
        [Xs.id]: {
          order: 1,
          menuItemFactory: Ru
        },
        [Js.id]: {
          order: 2,
          menuItemFactory: bu
        },
        [In.id]: {
          order: 3,
          menuItemFactory: xu
        }
      }
    }
  }
};
var $u = Object.defineProperty, eh = Object.getOwnPropertyDescriptor, th = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? eh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && $u(e, t, s), s;
}, Ke = (n, e) => (t, o) => e(t, o, n);
let Hn = class extends ue {
  constructor(n, e, t, o, s, r, i, a, c) {
    super(), this._injector = n, this._componentManager = e, this._commandService = t, this._layoutService = o, this._menuManagerService = s, this._uiPartsService = r, this._univerInstanceService = i, this._shortcutService = a, this._configService = c, this._init();
  }
  _initCustomComponents() {
    const n = this._componentManager;
    this.disposeWithMe(n.register(Ds, Zc)), this.disposeWithMe(n.register(oa, Pc)), this.disposeWithMe(n.register(sa, Dc)), this.disposeWithMe(n.register(ra, wc)), this.disposeWithMe(n.register(ca, Cl)), this.disposeWithMe(n.register(aa, Sl)), this.disposeWithMe(n.register("TodoList", $i));
  }
  // TODO: @zhangwei, why add workbook to docs-ui?
  _initUiParts() {
    var t, o;
    const n = this._univerInstanceService.getCurrentUnitForType(_.UNIVER_SHEET), e = this._configService.getConfig(Us);
    (o = (t = e == null ? void 0 : e.layout) == null ? void 0 : t.docContainerConfig) != null && o.footer && !n && this.disposeWithMe(this._uiPartsService.registerComponent(Nc.FOOTER, () => $a(nd, this._injector)));
  }
  _initMenus() {
    this._menuManagerService.mergeMenu(Zu);
  }
  _initShortCut() {
    [
      Nl,
      Ql,
      Ul,
      Ll,
      Fl,
      Hl,
      jl,
      Wl,
      Vl,
      kl,
      zl,
      Gl,
      xl
    ].forEach((n) => {
      this.disposeWithMe(this._shortcutService.registerShortcut(n));
    });
  }
  _init() {
    this._initCustomComponents(), this._initMenus(), this._initFocusHandler(), this._initCommands(), this._initUiParts(), this._initShortCut();
  }
  _initCommands() {
    [
      na,
      _s,
      Ms
    ].forEach((n) => this.disposeWithMe(this._commandService.registerCommand(n)));
  }
  _initFocusHandler() {
    this.disposeWithMe(
      this._layoutService.registerFocusHandler(_.UNIVER_DOC, (n) => {
        this._injector.get(fe).getRenderById(n).with(Se).focus();
      })
    );
  }
};
Hn = th([
  Ke(0, z(so)),
  Ke(1, z(io)),
  Ke(2, y),
  Ke(3, bs),
  Ke(4, Qc),
  Ke(5, Uc),
  Ke(6, Q),
  Ke(7, ro),
  Ke(8, Rs)
], Hn);
var nh = Object.defineProperty, oh = Object.getOwnPropertyDescriptor, sh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? oh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && nh(e, t, s), s;
}, Fo = (n, e) => (t, o) => e(t, o, n);
const ni = 1.5;
let kn = class extends At {
  constructor(n, e, t, o) {
    super(), this._context = n, this._textSelectionManagerService = e, this._editorService = t, this._docSkeletonManagerService = o, this._init();
  }
  _init() {
    this._textSelectionManagerService.textSelection$.pipe(st(this.dispose$)).subscribe((n) => {
      if (n == null)
        return;
      const { isEditing: e, unitId: t } = n;
      t !== this._context.unitId || !e || this._context.unitId !== vs && this._scrollToSelection();
    });
  }
  scrollToRange(n) {
    const e = this._docSkeletonManagerService.getSkeleton();
    if (!e)
      return;
    const { startOffset: t } = n, o = e.findNodePositionByCharIndex(t);
    o && this.scrollToNode(o);
  }
  scrollToNode(n) {
    var O;
    const { unitId: e, scene: t, mainComponent: o } = this._context, s = this._docSkeletonManagerService.getSkeleton();
    if (o == null || s == null)
      return;
    const r = o.getOffsetConfig(), { docsLeft: i, docsTop: a } = r, c = new it(r, s), { contentBoxPointGroup: A } = c.getRangePointData(n, n), { left: l, top: d, height: h } = Mn(A), u = l + i, g = d + a, f = t.getViewport(Xe.VIEW_MAIN), p = this._editorService.getEditor(e);
    if (f == null)
      return;
    const {
      left: m,
      top: E,
      right: I,
      bottom: v
    } = f.getBounding().viewBound;
    let R = 0, S = 0;
    const C = p ? (O = p.params.backScrollOffset) != null ? O : 0 : 100;
    g < E ? R = g - E - C : g > v - h && (R = g - v + h + C), u < m ? S = u - m : u > I - ni && (S = u - I + ni);
    const T = f.transViewportScroll2ScrollValue(S, R);
    f.scrollByBarDeltaValue(T);
  }
  // Let the selection show on the current screen.
  _scrollToSelection() {
    const n = this._textSelectionManagerService.getActiveTextRange();
    if (n == null)
      return;
    const { collapsed: e, startNodePosition: t } = n;
    e && this.scrollToNode(t);
  }
};
kn = sh([
  Fo(1, z(G)),
  Fo(2, He),
  Fo(3, z(ie))
], kn);
var rh = Object.defineProperty, ih = Object.getOwnPropertyDescriptor, ah = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? ih(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && rh(e, t, s), s;
}, bt = (n, e) => (t, o) => e(t, o, n);
let os = class extends At {
  constructor(n, e, t, o, s, r, i) {
    super(), this._context = n, this._commandService = e, this._docSelectionRenderService = t, this._docSkeletonManagerService = o, this._editorService = s, this._renderManagerService = r, this._univerInstanceService = i, this._addNewRender(), this._initRenderRefresh(), this._initCommandListener();
  }
  reRender(n) {
    var r, i;
    const e = (r = this._renderManagerService.getRenderById(n)) == null ? void 0 : r.with(ie), t = e == null ? void 0 : e.getSkeleton();
    if (!t || !!t.getViewModel().getDataModel().getSnapshot().disabled)
      return;
    t.calculate();
    const s = this._editorService.getEditor(n);
    if (this._editorService.isEditor(n) && !(s != null && s.params.scrollBar)) {
      (i = this._context.mainComponent) == null || i.makeDirty();
      return;
    }
    this._recalculateSizeBySkeleton(t);
  }
  _addNewRender() {
    const { scene: n, engine: e } = this._context, t = new Sc(Xe.VIEW_MAIN, n, {
      left: 0,
      top: 0,
      bottom: 0,
      right: 0,
      isWheelPreventDefaultX: !0
    });
    n.attachControl(), n.onMouseWheel$.subscribeEvent((o, s) => {
      const r = this._univerInstanceService.getCurrentUnitForType(_.UNIVER_DOC);
      if ((r == null ? void 0 : r.getUnitId()) !== this._context.unitId)
        return;
      const i = o;
      if (i.ctrlKey) {
        const a = Math.abs(i.deltaX);
        let c = a < 40 ? 0.2 : a < 80 ? 0.4 : 0.2;
        c *= i.deltaY > 0 ? -1 : 1, n.scaleX < 1 && (c /= 2), n.scaleX + c > 4 ? n.scale(4, 4) : n.scaleX + c < 0.1 ? n.scale(0.1, 0.1) : i.preventDefault();
      } else
        t.onMouseWheel(i, s);
    }), new Vo(t), n.addLayer(
      new Sr(n, [], Oo),
      new Sr(n, [], aA)
    ), this._addComponent(), e.runRenderLoop(() => {
      n.render();
    }), this._docSelectionRenderService.__attachScrollEvent();
  }
  _addComponent() {
    const { scene: n, unit: e, components: t } = this._context, r = {
      pageMarginLeft: 20,
      pageMarginTop: 20
    }, i = new Ic(We.MAIN, void 0, r);
    i.zIndex = xr;
    const a = new Cc(We.BACKGROUND, void 0, r);
    a.zIndex = xr, this._context.mainComponent = i, t.set(We.MAIN, i), t.set(We.BACKGROUND, a), n.addObjects([i], Oo), n.addObjects([a], iA), this._editorService.getEditor(e.getUnitId()) == null && n.enableLayerCache(Oo);
  }
  _initRenderRefresh() {
    this._docSkeletonManagerService.currentSkeletonBefore$.pipe(st(this.dispose$)).subscribe((n) => {
      this._create(n);
    });
  }
  _create(n) {
    var a;
    if (!n)
      return;
    const { mainComponent: e, components: t } = this._context, o = e, s = t.get(We.BACKGROUND);
    o.changeSkeleton(n), s.changeSkeleton(n);
    const { unitId: r } = this._context, i = this._editorService.getEditor(r);
    if (this._editorService.isEditor(r) && !(i != null && i.params.scrollBar)) {
      (a = this._context.mainComponent) == null || a.makeDirty();
      return;
    }
    this._recalculateSizeBySkeleton(n);
  }
  _initCommandListener() {
    const n = [J.id];
    this.disposeWithMe(this._commandService.onCommandExecuted((e) => {
      if (n.includes(e.id)) {
        const t = e.params, { unitId: o } = t;
        this.reRender(o);
      }
    }));
  }
  _recalculateSizeBySkeleton(n) {
    var u;
    const { mainComponent: e, scene: t, unitId: o, components: s } = this._context, r = e, i = s.get(We.BACKGROUND), a = (u = n.getSkeletonData()) == null ? void 0 : u.pages;
    if (a == null)
      return;
    let c = 0, A = 0;
    const d = this._context.unit.getSnapshot().documentStyle.documentFlavor;
    for (let g = 0, f = a.length; g < f; g++) {
      const p = a[g];
      let { pageWidth: m, pageHeight: E } = p;
      if (d === ye.MODERN) {
        const I = ch(p);
        m = I.pageWidth, E = I.pageHeight;
      }
      r.pageLayoutType === an.VERTICAL ? (A += E, A += r.pageMarginTop, g === f - 1 && (A += r.pageMarginTop), c = Math.max(c, m)) : r.pageLayoutType === an.HORIZONTAL && (c += m, g !== f - 1 && (c += r.pageMarginLeft), A = Math.max(A, E));
    }
    r.resize(c, A), i.resize(c, A);
    const h = this._editorService.getEditor(o);
    (!this._editorService.isEditor(o) || h != null && h.params.scrollBar) && t.resize(c, A);
  }
};
os = ah([
  bt(1, y),
  bt(2, z(Se)),
  bt(3, z(ie)),
  bt(4, He),
  bt(5, fe),
  bt(6, Q)
], os);
function ch(n) {
  let { pageWidth: e, pageHeight: t } = n;
  const { marginLeft: o, marginRight: s, marginTop: r, marginBottom: i, skeDrawings: a, skeTables: c } = n;
  e === Number.POSITIVE_INFINITY && (e = n.width + o + s), t === Number.POSITIVE_INFINITY && (t = n.height + r + i);
  for (const A of a.values())
    e = Math.max(e, A.aLeft + A.width + o + s), t = Math.max(t, A.aTop + A.height + r + i);
  for (const A of c.values())
    e = Math.max(e, A.left + A.width + o + s), t = Math.max(t, A.top + A.height + r + i);
  return { pageWidth: e, pageHeight: t };
}
const ya = {
  id: "doc.command.select-all",
  type: N.COMMAND,
  handler: async (n) => {
    var h;
    const e = n.get(Q), t = n.get(G), o = e.getCurrentUnitForType(_.UNIVER_DOC), s = t.getDocRanges(), r = (h = s.find((u) => u.isActive)) != null ? h : s[0];
    if (o == null || r == null)
      return !1;
    const { segmentId: i } = r, a = o.getUnitId(), c = o.getSelfOrHeaderFooterModel(i).getSnapshot().body;
    if (c == null)
      return !1;
    const { tables: A = [] } = c, l = [];
    let d = 0;
    for (const u of A) {
      const { startIndex: g, endIndex: f } = u;
      d !== g && l.push({
        startOffset: d,
        endOffset: g - 1,
        rangeType: Ge.TEXT
      }), l.push({
        startOffset: g + 3,
        // 3 is TABLE_START, ROW_START, CELL_START.
        endOffset: f - 5,
        // 4 is CELL_END, ROW_END, TABLE_END AND \n.
        rangeType: Ge.RECT
      }), d = f;
    }
    return d !== c.dataStream.length - 2 && l.push({
      startOffset: d,
      endOffset: c.dataStream.length - 2,
      rangeType: Ge.TEXT
    }), t.replaceDocRanges(l, {
      unitId: a,
      subUnitId: a
    }, !1), !0;
  }
};
class Ro extends At {
  constructor(t) {
    super();
    x(this, "_previousActiveRange", null);
    x(this, "_undoMutationParamsCache", []);
    x(this, "_redoMutationParamsCache", []);
    this._context = t;
  }
  clearUndoRedoMutationParamsCache() {
    this._undoMutationParamsCache = [], this._redoMutationParamsCache = [];
  }
  getUndoRedoMutationParamsCache() {
    return {
      undoCache: this._undoMutationParamsCache,
      redoCache: this._redoMutationParamsCache
    };
  }
  setUndoRedoMutationParamsCache({ undoCache: t = [], redoCache: o = [] }) {
    this._undoMutationParamsCache = t, this._redoMutationParamsCache = o;
  }
  getActiveRange() {
    return this._previousActiveRange;
  }
  setActiveRange(t) {
    this._previousActiveRange = t;
  }
  pushUndoRedoMutationParams(t, o) {
    this._undoMutationParamsCache.push(t), this._redoMutationParamsCache.push(o);
  }
  fetchComposedUndoRedoMutationParams() {
    if (this._undoMutationParamsCache.length === 0 || this._previousActiveRange == null || this._redoMutationParamsCache.length === 0)
      return null;
    const { unitId: t } = this._undoMutationParamsCache[0], o = {
      unitId: t,
      actions: this._undoMutationParamsCache.reverse().reduce((r, i) => k.compose(r, i.actions), null),
      textRanges: []
      // Add empty array, will never use, just fix type error
    };
    return { redoMutationParams: {
      unitId: t,
      actions: this._redoMutationParamsCache.reduce((r, i) => k.compose(r, i.actions), null),
      textRanges: []
      // Add empty array, will never use, just fix type error
    }, undoMutationParams: o, previousActiveRange: this._previousActiveRange };
  }
  dispose() {
    this._undoMutationParamsCache = [], this._redoMutationParamsCache = [], this._previousActiveRange = null;
  }
}
const Ah = Is, Ba = {
  id: "doc.command.ime-input",
  type: N.COMMAND,
  // eslint-disable-next-line max-lines-per-function
  handler: async (n, e) => {
    var D, te, q, V;
    const { unitId: t, newText: o, oldTextLen: s, isCompositionEnd: r, isCompositionStart: i } = e, a = n.get(y), c = n.get(fe), A = n.get(Q), l = n.get(Je), d = (D = c.getRenderById(t)) == null ? void 0 : D.with(Ro), h = A.getUnit(t, _.UNIVER_DOC);
    if (h == null || d == null)
      return !1;
    const u = d.getActiveRange();
    if (u == null)
      return !1;
    const { style: g, segmentId: f } = u, p = h.getSelfOrHeaderFooterModel(f).getBody();
    if (p == null)
      return !1;
    Object.assign(u, u);
    const { startOffset: E, endOffset: I } = u, v = o.length, R = [
      {
        startOffset: E + v,
        endOffset: E + v,
        collapsed: !0,
        style: g
      }
    ], S = {
      id: J.id,
      params: {
        unitId: t,
        actions: [],
        textRanges: R
      }
    }, C = l.getDefaultStyle(), T = l.getStyleCache(), O = Os((te = p.customRanges) != null ? te : [], E + s, Ah.includes(t)), P = co(
      (q = p.textRuns) != null ? q : [],
      i ? I : E + s,
      C,
      T
    ), b = Ts((V = p.customDecorations) != null ? V : [], E + s), B = new me(), M = k.getInstance();
    if (!u.collapsed && i) {
      const Y = Ce.selection.delete([u], p, 0, null, !1);
      B.push(...Y), S.params.textRanges = [{
        startOffset: E + v,
        endOffset: E + v,
        collapsed: !0
      }];
    } else
      B.push({
        t: W.RETAIN,
        len: E
      });
    s > 0 && B.push({
      t: W.DELETE,
      len: s
    }), B.push({
      t: W.INSERT,
      body: {
        dataStream: o,
        textRuns: P ? [{
          ...P,
          st: 0,
          ed: o.length
        }] : [],
        customRanges: O ? [{
          ...O,
          startIndex: 0,
          endIndex: o.length - 1
        }] : [],
        customDecorations: b.map((Y) => ({
          ...Y,
          startIndex: 0,
          endIndex: o.length - 1
        }))
      },
      len: o.length
    });
    const H = le(h, f);
    S.params.actions = M.editOp(B.serialize(), H), S.params.noHistory = !r, S.params.isCompositionEnd = r;
    const F = a.syncExecuteCommand(S.id, S.params);
    return d.pushUndoRedoMutationParams(F, S.params), !!F;
  }
}, ss = {
  type: N.COMMAND,
  id: "doc.command.set-zoom-ratio",
  handler: async (n, e) => {
    var d, h, u;
    const t = n.get(y), o = n.get(eo), s = n.get(Q);
    let r = (d = s.getCurrentUniverDocInstance()) == null ? void 0 : d.getUnitId();
    if (!r) return !1;
    let i = 1;
    if (e && (r = (h = e.documentId) != null ? h : r, i = (u = e.zoomRatio) != null ? u : i), !s.getUniverDocInstance(r)) return !1;
    const c = {
      zoomRatio: i,
      unitId: r
    }, A = Kl(n, c);
    return t.syncExecuteCommand(Ye.id, c) ? (o.pushUndoRedo({
      unitID: r,
      undoMutations: [{ id: Ye.id, params: A }],
      redoMutations: [{ id: Ye.id, params: c }]
    }), !0) : !1;
  }
}, Ma = {
  id: "doc.table.tab-in-table",
  type: N.COMMAND,
  handler: async (n, e) => {
    var g;
    const { shift: t } = e, o = n.get(G), s = o.getDocRanges(), r = n.get(y), a = n.get(Q).getCurrentUniverDocInstance();
    if (!a)
      return !1;
    const c = (g = s.find((f) => f.isActive)) != null ? g : s[0], A = a.getUnitId(), l = ke(n, A), d = l == null ? void 0 : l.getSkeleton(), h = d == null ? void 0 : d.getViewModel().getSelfOrHeaderFooterViewModel(c == null ? void 0 : c.segmentId);
    if (h == null || c == null)
      return !1;
    let u = null;
    if (t ? u = Kr(h, c, ts.PREV) : u = Kr(h, c, ts.NEXT), u) {
      const { startOffset: f, endOffset: p } = u, m = [{
        startOffset: f,
        endOffset: p
      }];
      return o.replaceDocRanges(m), !0;
    }
    return t === !1 ? await r.executeCommand(Ia.id, {
      position: Eo.BELLOW
    }) : !0;
  }
};
var lh = Object.defineProperty, dh = Object.getOwnPropertyDescriptor, uh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? dh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && lh(e, t, s), s;
}, Ho = (n, e) => (t, o) => e(t, o, n);
let rs = class {
  constructor(n, e, t) {
    x(this, "_docContainer");
    // 获取SheetContainer组件
    x(this, "getComponent", (n) => {
      if (this._docContainer = n, !n.getContentRef().current)
        throw new Error("container is not ready");
    });
    /**
     * Change language
     * @param {string} lang new language
     *
     * e: {target: HTMLSelectElement } reference from  https://stackoverflow.com/a/48443771
     *
     */
    x(this, "changeLocale", (n) => {
      this._localeService.setLocale(n);
    });
    this._localeService = n, this._injector = e, this._configService = t;
  }
  getUIConfig() {
    return {
      injector: this._injector,
      config: this._configService.getConfig(Us),
      changeLocale: this.changeLocale,
      getComponent: this.getComponent
    };
  }
  getContentRef() {
    return this._docContainer.getContentRef();
  }
  UIDidMount(n) {
    if (this._docContainer)
      return n(this._docContainer);
  }
  getDocContainer() {
    return this._docContainer;
  }
};
rs = uh([
  Ho(0, z(Ze)),
  Ho(1, z(so)),
  Ho(2, Rs)
], rs);
var hh = Object.defineProperty, gh = Object.getOwnPropertyDescriptor, fh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? gh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && hh(e, t, s), s;
}, ph = (n, e) => (t, o) => e(t, o, n);
let Vn = class extends At {
  constructor(e) {
    super();
    x(this, "_docContainerController");
    this._injector = e, this._docContainerController = this._injector.createInstance(rs);
  }
};
Vn = fh([
  ph(0, z(so))
], Vn);
var mh = Object.defineProperty, Eh = Object.getOwnPropertyDescriptor, Sh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Eh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && mh(e, t, s), s;
}, oi = (n, e) => (t, o) => e(t, o, n);
let jn = class extends ue {
  constructor(n, e) {
    super(), this._docAutoFormatService = n, this._renderManagerService = e, this._initListTabAutoFormat(), this._initListSpaceAutoFormat(), this._initDefaultEnterFormat(), this._initExitListAutoFormat();
  }
  _initListTabAutoFormat() {
    this.disposeWithMe(
      this._docAutoFormatService.registerAutoFormat({
        id: _t.id,
        match: (n) => {
          var s;
          const { selection: e, paragraphs: t, unit: o } = n;
          if (t.length === 1 && e.startOffset === t[0].paragraphStart && t[0].bullet) {
            const r = (s = o.getBody()) == null ? void 0 : s.paragraphs, i = r == null ? void 0 : r.filter((a) => {
              var c;
              return ((c = a.bullet) == null ? void 0 : c.listId) === t[0].bullet.listId;
            });
            return (i == null ? void 0 : i.findIndex((a) => a.startIndex === t[0].startIndex)) !== 0;
          } else if (t.length > 1 && t.some((r) => r.bullet))
            return !0;
          return !1;
        },
        // traverse all paragraphs, set paragraph
        getMutations(n) {
          const e = n.commandParams;
          return [{
            id: es.id,
            params: {
              type: e != null && e.shift ? Pn.decrease : Pn.increase
            }
          }];
        },
        priority: 100
      })
    ), this.disposeWithMe(
      this._docAutoFormatService.registerAutoFormat({
        id: _t.id,
        match: (n) => {
          const { selection: e, unit: t } = n, { startNodePosition: o, endNodePosition: s } = e, r = this._renderManagerService.getRenderById(t.getUnitId()), i = r == null ? void 0 : r.with(ie).getSkeleton();
          return i == null ? !1 : !!(o && s && zi(i, o, s) || o && !s && o.path.indexOf("cells") > -1);
        },
        getMutations(n) {
          const e = n.commandParams;
          return [{
            id: Ma.id,
            params: {
              shift: !!(e != null && e.shift)
            }
          }];
        },
        priority: 99
      })
    );
  }
  _initListSpaceAutoFormat() {
    this.disposeWithMe(
      this._docAutoFormatService.registerAutoFormat({
        id: Ao.id,
        match: (n) => {
          var r;
          const { selection: e, paragraphs: t, unit: o } = n;
          if (!e.collapsed || t.length !== 1)
            return !1;
          const s = (r = o.getBody()) == null ? void 0 : r.dataStream.slice(t[0].paragraphStart, t[0].paragraphEnd - 1);
          return !!(s && Object.keys(bo).includes(s));
        },
        getMutations(n) {
          var s;
          const { paragraphs: e, unit: t } = n, o = (s = t.getBody()) == null ? void 0 : s.dataStream.slice(e[0].paragraphStart, e[0].paragraphEnd - 1);
          if (o && Object.keys(bo).includes(o)) {
            const r = bo[o];
            return [{
              id: da.id,
              params: {
                listType: r,
                paragraph: e[0]
              }
            }];
          }
          return [];
        }
      })
    );
  }
  _initExitListAutoFormat() {
    this.disposeWithMe(
      this._docAutoFormatService.registerAutoFormat({
        id: ln.id,
        match: (n) => {
          const { paragraphs: e } = n;
          return !!(e.length === 1 && e[0].bullet && e[0].paragraphStart === e[0].paragraphEnd);
        },
        getMutations: (n) => {
          const e = n.paragraphs[0].bullet;
          return e ? e.nestingLevel > 0 ? [{
            id: es.id,
            params: {
              type: Pn.decrease
            }
          }] : [{
            id: pn.id,
            params: {
              listType: n.paragraphs[0].bullet.listType
            }
          }] : [];
        }
      })
    );
  }
  _initDefaultEnterFormat() {
    this.disposeWithMe(
      this._docAutoFormatService.registerAutoFormat({
        id: ln.id,
        match: () => !0,
        getMutations() {
          return [{
            id: Ra.id
          }];
        },
        priority: -9999
      })
    );
  }
};
jn = Sh([
  oi(0, z(Et)),
  oi(1, fe)
], jn);
function Ih(n) {
  return n.rows[0].cells[0].sections[0].columns[0].lines[0];
}
function Ch(n) {
  const e = n.rows[n.rows.length - 1], t = e.cells[e.cells.length - 1];
  return bc(t);
}
function vh(n, e) {
  const { ed: t } = n, { skeTables: o } = e;
  let s = null;
  for (const r of o.values())
    if (r.st === t + 1) {
      s = r;
      break;
    }
  return s;
}
function si(n) {
  const e = n == null ? void 0 : n.parent;
  let t = null, o = null;
  if (n == null || e == null)
    return {
      lineBeforeTable: t,
      lineAfterTable: o
    };
  const { st: s, ed: r } = n, i = e.type === Ie.CELL ? [e] : e.parent.pages;
  return vc(i, (a) => {
    a.st === r + 1 ? o = a : a.ed === s - 1 && (t = a);
  }), {
    lineBeforeTable: t,
    lineAfterTable: o
  };
}
function _a(n) {
  return n.sections[0].columns[0].lines.length === 0;
}
function Pa(n) {
  var i, a;
  const e = n.parent, t = e == null ? void 0 : e.parent, o = t == null ? void 0 : t.tableId;
  if (e == null || t == null)
    return;
  const s = e.cells.indexOf(n);
  let r = t.rows[t.rows.indexOf(e) + 1];
  if (r == null && o.indexOf("#-#")) {
    const [c, A] = o.split("#-#"), l = (a = (i = t.parent) == null ? void 0 : i.parent) == null ? void 0 : a.pages, d = `${c}#-#${Number.parseInt(A) + 1}`;
    if (l)
      for (const h of l) {
        const { skeTables: u } = h;
        if (u.has(d)) {
          const g = u.get(d);
          if (g != null && g.rows.length) {
            r = g.rows.find((f) => !f.isRepeatRow);
            break;
          }
        }
      }
  }
  if (r != null) {
    const c = r.cells[s];
    return _a(c) ? Pa(c) : c;
  }
}
function Da(n) {
  var r, i;
  const e = n.parent, t = e == null ? void 0 : e.parent;
  if (e == null || t == null)
    return;
  let o = t.rows[t.rows.indexOf(e) - 1];
  const s = e.cells.indexOf(n);
  if ((o == null || o.isRepeatRow) && t.tableId.indexOf("#-#")) {
    const [a, c] = t.tableId.split("#-#"), A = (i = (r = t.parent) == null ? void 0 : r.parent) == null ? void 0 : i.pages, l = `${a}#-#${Number.parseInt(c) - 1}`;
    if (A)
      for (const d of A) {
        const { skeTables: h } = d;
        if (h.has(l)) {
          const u = h.get(l);
          if (u != null && u.rows.length) {
            o = u.rows[u.rows.length - 1];
            break;
          }
        }
      }
  }
  if (o != null) {
    const a = o.cells[s];
    return _a(a) ? Da(a) : a;
  }
}
function Rh(n, e) {
  const { st: t } = n, { skeTables: o } = e;
  let s = null;
  for (const r of o.values())
    if (r.ed === t - 1) {
      s = r;
      break;
    }
  return s;
}
function bh(n) {
  return n.sections[0].columns[0].lines[0];
}
function xh(n) {
  const e = Rc(n);
  return e.lines[e.lines.length - 1];
}
var Oh = Object.defineProperty, Th = Object.getOwnPropertyDescriptor, yh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Th(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Oh(e, t, s), s;
}, Rn = (n, e) => (t, o) => e(t, o, n);
let Wn = class extends ue {
  constructor(e, t, o, s) {
    super();
    x(this, "_onInputSubscription");
    this._univerInstanceService = e, this._renderManagerService = t, this._textSelectionManagerService = o, this._commandService = s, this._commandExecutedListener();
  }
  dispose() {
    var e;
    super.dispose(), (e = this._onInputSubscription) == null || e.unsubscribe();
  }
  _commandExecutedListener() {
    const e = [at.id, ct.id];
    this.disposeWithMe(
      this._commandService.onCommandExecuted((t) => {
        if (!e.includes(t.id))
          return;
        const o = t.params;
        switch (t.id) {
          case at.id:
            return this._handleMoveCursor(o.direction);
          case ct.id:
            return this._handleShiftMoveSelection(o.direction);
          default:
            throw new Error("Unknown command");
        }
      })
    );
  }
  // eslint-disable-next-line max-lines-per-function, complexity
  _handleShiftMoveSelection(e) {
    var I, v, R;
    const t = this._textSelectionManagerService.getActiveTextRange(), o = this._textSelectionManagerService.getTextRanges(), s = this._univerInstanceService.getCurrentUniverDocInstance();
    if (s == null)
      return;
    const r = (I = this._renderManagerService.getRenderById(s.getUnitId())) == null ? void 0 : I.with(ie).getSkeleton(), i = this._getDocObject();
    if (t == null || r == null || i == null)
      return;
    const {
      startOffset: a,
      endOffset: c,
      style: A,
      collapsed: l,
      direction: d,
      segmentId: h,
      startNodePosition: u,
      endNodePosition: g,
      segmentPage: f
    } = t;
    if (o.length > 1) {
      let S = Number.POSITIVE_INFINITY, C = Number.NEGATIVE_INFINITY;
      for (const T of o)
        S = Math.min(S, T.startOffset), C = Math.max(C, T.endOffset);
      this._textSelectionManagerService.replaceTextRanges([
        {
          startOffset: e === se.LEFT || e === se.UP ? C : S,
          endOffset: e === se.LEFT || e === se.UP ? S : C,
          style: A
        }
      ], !1);
      return;
    }
    const p = l || d === xe.FORWARD ? a : c;
    let m = l || d === xe.FORWARD ? c : a;
    const E = (v = s.getSelfOrHeaderFooterModel(h).getBody().dataStream.length) != null ? v : Number.POSITIVE_INFINITY;
    if (e === se.LEFT || e === se.RIGHT) {
      const S = r.findNodeByCharIndex(m - 1, h, f), C = r.findNodeByCharIndex(m, h, f);
      m = e === se.RIGHT ? m + C.count : m - ((R = S == null ? void 0 : S.count) != null ? R : 0), m = Math.min(E - 2, Math.max(0, m)), this._textSelectionManagerService.replaceTextRanges([
        {
          startOffset: p,
          endOffset: m,
          style: A
        }
      ], !1), this._scrollToFocusNodePosition(s.getUnitId(), m);
    } else {
      const S = r.findNodeByCharIndex(m, h, f), C = i.document.getOffsetConfig(), T = l ? u : d === xe.FORWARD ? g : u, O = this._getTopOrBottomPosition(r, S, T, e === se.DOWN, !0);
      if (O == null) {
        const b = e === se.UP ? 0 : E - 2;
        if (b === m)
          return;
        this._textSelectionManagerService.replaceTextRanges([
          {
            startOffset: p,
            endOffset: b,
            style: A
          }
        ], !1);
        return;
      }
      const P = new it(C, r).getRangePointData(
        O,
        O
      ).cursorList[0];
      this._textSelectionManagerService.replaceTextRanges([
        {
          startOffset: p,
          endOffset: P.endOffset,
          style: A
        }
      ], !1), this._scrollToFocusNodePosition(s.getUnitId(), P.endOffset);
    }
  }
  // eslint-disable-next-line max-lines-per-function, complexity
  _handleMoveCursor(e) {
    var E, I, v, R;
    const t = this._textSelectionManagerService.getActiveTextRange(), o = this._textSelectionManagerService.getTextRanges(), s = this._univerInstanceService.getCurrentUniverDocInstance();
    if (s == null)
      return !1;
    const r = (E = this._renderManagerService.getRenderById(s.getUnitId())) == null ? void 0 : E.with(ie).getSkeleton(), i = this._getDocObject();
    if (t == null || r == null || i == null || o == null)
      return;
    const { startOffset: a, endOffset: c, style: A, collapsed: l, segmentId: d, startNodePosition: h, endNodePosition: u, segmentPage: g } = t, f = s.getSelfOrHeaderFooterModel(d).getBody();
    if (f == null)
      return;
    const p = (I = f.dataStream.length) != null ? I : Number.POSITIVE_INFINITY, m = (v = s.getCustomRanges()) != null ? v : [];
    if (e === se.LEFT || e === se.RIGHT) {
      let S;
      if (!t.collapsed || o.length > 1) {
        let O = Number.POSITIVE_INFINITY, P = Number.NEGATIVE_INFINITY;
        for (const b of o)
          O = Math.min(O, b.startOffset), P = Math.max(P, b.endOffset);
        S = e === se.LEFT ? O : P;
      } else {
        const O = r.findNodeByCharIndex(a - 1, d, g), P = r.findNodeByCharIndex(a, d, g), b = r.findNodeByCharIndex(a + 1, d, g);
        e === se.LEFT ? S = Math.max(0, a - ((R = O == null ? void 0 : O.count) != null ? R : 1)) : S = Math.min(p - 2, c + P.count + ((b == null ? void 0 : b.streamType) === U.SECTION_BREAK ? 1 : 0));
      }
      const C = [
        U.TABLE_START,
        U.TABLE_END,
        U.TABLE_ROW_START,
        U.TABLE_ROW_END,
        U.TABLE_CELL_START,
        U.TABLE_CELL_END,
        U.SECTION_BREAK
      ];
      if (e === se.LEFT)
        for (; C.includes(f.dataStream[S]); )
          S--;
      else
        for (; C.includes(f.dataStream[S]); )
          S++;
      m.filter((O) => O.wholeEntity && O.startIndex < S && O.endIndex >= S).forEach((O) => {
        e === se.LEFT ? S = Math.min(O.startIndex, S) : S = Math.max(O.endIndex + 1, S);
      }), this._textSelectionManagerService.replaceTextRanges([
        {
          startOffset: Math.max(0, S),
          endOffset: Math.max(0, S),
          style: A
        }
      ], !1), this._scrollToFocusNodePosition(s.getUnitId(), S);
    } else {
      const S = r.findNodeByCharIndex(a, d, g), C = r.findNodeByCharIndex(c, d, g), T = i.document.getOffsetConfig(), O = this._getTopOrBottomPosition(
        r,
        e === se.UP || l ? S : C,
        e === se.UP || l ? h : u,
        e === se.DOWN
      );
      if (O == null) {
        let b;
        l ? b = e === se.UP ? 0 : p - 2 : b = e === se.UP ? a : c, this._textSelectionManagerService.replaceTextRanges([
          {
            startOffset: Math.max(0, b),
            endOffset: Math.max(0, b),
            style: A
          }
        ], !1);
        return;
      }
      const P = new it(T, r).getRangePointData(
        O,
        O
      ).cursorList[0];
      this._textSelectionManagerService.replaceTextRanges([
        {
          ...P,
          style: A
        }
      ], !1), this._scrollToFocusNodePosition(s.getUnitId(), P.endOffset);
    }
  }
  _getTopOrBottomPosition(e, t, o, s, r = !1) {
    if (t == null || o == null)
      return;
    const i = this._getGlyphLeftOffsetInLine(t), a = this._getNextOrPrevLine(t, s, r);
    if (a == null)
      return;
    const c = this._matchPositionByLeftOffset(e, a, i, o);
    if (c != null)
      return { ...c, isBack: !0 };
  }
  _getGlyphLeftOffsetInLine(e) {
    const t = e.parent;
    if (t == null)
      return Number.NEGATIVE_INFINITY;
    const o = t.left, { left: s } = e;
    return o + s;
  }
  _matchPositionByLeftOffset(e, t, o, s) {
    const r = {
      distance: Number.POSITIVE_INFINITY
    };
    for (const a of t.divides) {
      const c = a.left;
      for (const A of a.glyphGroup) {
        if (A.streamType === U.SECTION_BREAK)
          continue;
        const { left: l } = A, d = c + l, h = Math.abs(o - d);
        h < r.distance && (r.glyph = A, r.distance = h);
      }
    }
    if (r.glyph == null)
      return;
    const { segmentPage: i } = s;
    return e.findPositionByGlyph(r.glyph, i);
  }
  // eslint-disable-next-line max-lines-per-function, complexity
  _getNextOrPrevLine(e, t, o = !1) {
    var f, p, m, E, I, v, R, S, C, T, O, P;
    const s = e.parent, r = s == null ? void 0 : s.parent, i = r == null ? void 0 : r.parent, a = i == null ? void 0 : i.parent, c = a == null ? void 0 : a.parent;
    if (s == null || r == null || i == null || a == null || c == null)
      return;
    const A = i.lines.indexOf(r);
    if (A === -1)
      return;
    let l;
    if (c.type === Ie.CELL && o) {
      const b = ri(c, t);
      if (b)
        return b;
    }
    if (t === !0) {
      l = i.lines[A + 1];
      const b = vh(r, c);
      if (b) {
        const B = Ih(b);
        B && (l = B);
      }
    } else {
      l = i.lines[A - 1];
      const b = Rh(r, c);
      if (b) {
        const B = Ch(b);
        B && (l = B);
      }
    }
    if (l != null)
      return l;
    const d = a.columns.indexOf(i);
    if (d === -1)
      return;
    if (t === !0)
      l = (f = a.columns[d + 1]) == null ? void 0 : f.lines[0];
    else {
      const b = (m = (p = a.columns) == null ? void 0 : p[d - 1]) == null ? void 0 : m.lines;
      l = b == null ? void 0 : b[b.length - 1];
    }
    if (l != null)
      return l;
    const h = c.sections.indexOf(a);
    if (h === -1)
      return;
    if (t === !0)
      l = (I = (E = c.sections[h - 1]) == null ? void 0 : E.columns[0]) == null ? void 0 : I.lines[0];
    else {
      const b = (R = (v = c.sections) == null ? void 0 : v[h - 1]) == null ? void 0 : R.columns, B = b == null ? void 0 : b[b.length - 1], M = B == null ? void 0 : B.lines;
      l = M == null ? void 0 : M[M.length - 1];
    }
    if (l != null)
      return l;
    if (c.type === Ie.CELL)
      return ri(c, t);
    const u = c.parent;
    if (u == null)
      return;
    const g = u.pages.indexOf(c);
    if (g !== -1) {
      if (t === !0)
        l = (T = (C = (S = u.pages[g + 1]) == null ? void 0 : S.sections[0]) == null ? void 0 : C.columns[0]) == null ? void 0 : T.lines[0];
      else {
        const b = (O = u.pages[g - 1]) == null ? void 0 : O.sections;
        if (b == null)
          return;
        const B = (P = b[b.length - 1]) == null ? void 0 : P.columns, M = B[B.length - 1], H = M == null ? void 0 : M.lines;
        l = H[H.length - 1];
      }
      if (l != null)
        return l;
    }
  }
  _scrollToFocusNodePosition(e, t) {
    var s;
    const o = (s = this._renderManagerService.getRenderById(e)) == null ? void 0 : s.with(kn);
    o != null && o.scrollToRange({
      startOffset: t,
      endOffset: t,
      collapsed: !0
    });
  }
  _getDocObject() {
    return cA(this._univerInstanceService, this._renderManagerService);
  }
};
Wn = yh([
  Rn(0, Q),
  Rn(1, fe),
  Rn(2, z(G)),
  Rn(3, y)
], Wn);
function ri(n, e) {
  var o, s;
  let t = null;
  if (e === !0) {
    const r = Pa(n);
    if (r)
      t = bh(r);
    else {
      const i = (o = n.parent) == null ? void 0 : o.parent, { lineAfterTable: a } = si(i);
      a && (t = a);
    }
  } else {
    const r = Da(n);
    if (r)
      t = xh(r);
    else {
      const i = (s = n.parent) == null ? void 0 : s.parent, { lineBeforeTable: a } = si(i);
      a && (t = a);
    }
  }
  return t;
}
const Bh = "univer-create", Mh = "univer-create-item", _h = "univer-create-label", Ph = "univer-create-input", gt = {
  create: Bh,
  createItem: Mh,
  createLabel: _h,
  createInput: Ph
}, Dh = ({
  handleRowColChange: n,
  tableCreateParams: e
}) => {
  const t = $(Ze), [o, s] = ve(3), [r, i] = ve(5);
  function a(c, A) {
    s(c), i(A), n(c, A);
  }
  return Re(() => {
    s(e.rowCount), i(e.colCount);
  }, [e]), /* @__PURE__ */ w.jsxs("div", { className: gt.create, children: [
    /* @__PURE__ */ w.jsxs("div", { className: gt.createItem, children: [
      /* @__PURE__ */ w.jsx("span", { className: gt.createLabel, children: t.t("toolbar.table.rowCount") }),
      /* @__PURE__ */ w.jsx(
        An,
        {
          min: 1,
          max: 20,
          precision: 0,
          value: o,
          onChange: (c) => {
            a(c, r);
          },
          className: gt.createInput
        }
      )
    ] }),
    /* @__PURE__ */ w.jsxs("div", { className: gt.createItem, children: [
      /* @__PURE__ */ w.jsx("span", { className: gt.createLabel, children: t.t("toolbar.table.colCount") }),
      /* @__PURE__ */ w.jsx(
        An,
        {
          min: 1,
          max: 20,
          precision: 0,
          value: r,
          onChange: (c) => {
            a(o, c);
          },
          className: gt.createInput
        }
      )
    ] })
  ] });
};
var wh = Object.defineProperty, Nh = Object.getOwnPropertyDescriptor, Qh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Nh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && wh(e, t, s), s;
}, ii = (n, e) => (t, o) => e(t, o, n);
let zn = class extends ue {
  constructor(n, e) {
    super(), this._commandService = n, this._componentManager = e, this._initialize();
  }
  _initialize() {
    this._init(), this._registerCommands(), this._initCustomComponents();
  }
  _registerCommands() {
    [
      sr
    ].forEach((n) => this.disposeWithMe(this._commandService.registerCommand(n)));
  }
  _initCustomComponents() {
    const n = this._componentManager;
    this.disposeWithMe(n.register(Ca, Dh));
  }
  _init() {
  }
};
zn = Qh([
  ii(0, y),
  ii(1, z(io))
], zn);
const ai = 4;
var Uh = Object.defineProperty, Lh = Object.getOwnPropertyDescriptor, Fh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Lh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Uh(e, t, s), s;
}, bn = (n, e) => (t, o) => e(t, o, n);
function wa(n, e) {
  const t = ci(n.left, n.top, e), o = ci(n.right, n.bottom, e);
  return {
    left: t.x,
    top: t.y,
    right: o.x,
    bottom: o.y
  };
}
function ci(n, e, t) {
  const { scaleX: o, scaleY: s } = t.getAncestorScale(), r = t.getViewport(Xe.VIEW_MAIN);
  if (!r)
    return {
      x: n,
      y: e
    };
  const { viewportScrollX: i, viewportScrollY: a } = r, c = (n - i) * o, A = (e - a) * s;
  return {
    x: c,
    y: A
  };
}
function Ai(n, e, t) {
  const { scaleX: o, scaleY: s } = t.getAncestorScale(), r = t.getViewport(Xe.VIEW_MAIN);
  if (!r)
    return {
      x: n,
      y: e
    };
  const { viewportScrollX: i, viewportScrollY: a } = r, c = n / o + i, A = e / s + a;
  return {
    x: c,
    y: A
  };
}
const ko = (n, e) => {
  const { scene: t, mainComponent: o, engine: s } = e, r = e.with(ie).getSkeleton(), i = r.findNodePositionByCharIndex(n.startOffset, !0, n.segmentId, n.segmentPage), a = r.findNodePositionByCharIndex(n.endOffset, !0, n.segmentId, n.segmentPage), c = o;
  if (!a || !i)
    return;
  const A = c.getOffsetConfig(), { docsLeft: l, docsTop: d } = A, h = s.getCanvasElement(), u = h.getBoundingClientRect(), g = Ti(h.style.width), { top: f, left: p, width: m } = u, E = m / g, { scaleX: I, scaleY: v } = t.getAncestorScale(), R = new it(A, r), { borderBoxPointGroup: S } = R.getRangePointData(i, a);
  return Bs(S).map((O) => wa(O, t)).map((O) => ({
    left: (O.left + l * I) * E + p,
    right: (O.right + l * I) * E + p,
    top: (O.top + d * v) * E + f,
    bottom: (O.bottom + d * v) * E + f
  }));
};
let is = class extends ue {
  constructor(n, e, t, o) {
    super(), this._globalPopupManagerService = n, this._renderManagerService = e, this._univerInstanceService = t, this._commandService = o;
  }
  _createObjectPositionObserver(n, e) {
    const t = () => {
      const { scene: a, engine: c } = e, { left: A, top: l, width: d, height: h } = n, u = {
        left: A,
        right: A + d,
        top: l,
        bottom: l + h
      }, g = c.getCanvasElement(), f = g.getBoundingClientRect(), p = Ti(g.style.width), m = wa(u, a), { top: E, left: I, width: v } = f, R = v / p;
      return {
        left: m.left * R + I,
        right: m.right * R + I,
        top: m.top * R + E,
        bottom: m.bottom * R + E
      };
    }, o = t(), s = new Le(o), r = new Dn();
    r.add(this._commandService.onCommandExecuted((a) => {
      if (a.id === Ye.id || a.id === J.id) {
        const c = t();
        c && s.next(c);
      }
    }));
    const i = e.scene.getViewport(Xe.VIEW_MAIN);
    return i && r.add(i.onScrollAfter$.subscribeEvent(() => {
      s.next(t());
    })), {
      position: o,
      position$: s,
      disposable: r
    };
  }
  _createRangePositionObserver(n, e) {
    var i;
    const t = (i = ko(n, e)) != null ? i : [], o = new Le(t), s = new Dn();
    s.add(this._commandService.onCommandExecuted((a) => {
      if ((a.id === Ye.id || a.id === J.id) && a.params.unitId === e.unitId) {
        const A = ko(n, e);
        A && o.next(A);
      }
    }));
    const r = e.scene.getViewport(Xe.VIEW_MAIN);
    return r && s.add(r.onScrollAfter$.subscribeEvent(() => {
      const a = ko(n, e);
      a && o.next(a);
    })), {
      positions: t,
      positions$: o,
      disposable: s
    };
  }
  // #region attach to object
  /**
   * attach a popup to canvas object
   * @param targetObject target canvas object
   * @param popup popup item
   * @returns disposable
   */
  attachPopupToObject(n, e, t) {
    const o = this._renderManagerService.getRenderById(t);
    if (!o)
      throw new Error(`Current render not found, unitId: ${t}`);
    const { position: s, position$: r, disposable: i } = this._createObjectPositionObserver(n, o), a = this._globalPopupManagerService.addPopup({
      ...e,
      unitId: t,
      subUnitId: "default",
      anchorRect: s,
      anchorRect$: r,
      canvasElement: o.engine.getCanvasElement()
    });
    return {
      dispose: () => {
        this._globalPopupManagerService.removePopup(a), r.complete(), i.dispose();
      }
    };
  }
  // #endregion
  // #region attach to range
  /**
   * attach a popup to doc range
   * @param range doc range
   * @param popup popup item
   * @param unitId unit id
   * @returns disposable
   */
  attachPopupToRange(n, e, t) {
    if (!this._univerInstanceService.getUnit(t))
      throw new Error(`Document not found, unitId: ${t}`);
    const { direction: s = "top", multipleDirection: r } = e, i = this._renderManagerService.getRenderById(t);
    if (!i)
      throw new Error(`Current render not found, unitId: ${t}`);
    const { positions: a, positions$: c, disposable: A } = this._createRangePositionObserver(n, i), l = c.pipe(gn((h) => s.includes("top") ? h[0] : h[h.length - 1])), d = this._globalPopupManagerService.addPopup({
      ...e,
      unitId: t,
      subUnitId: "default",
      anchorRect: s.includes("top") ? a[0] : a[a.length - 1],
      anchorRect$: l,
      excludeRects: a,
      excludeRects$: c,
      direction: s.includes("top") || s.includes("bottom") ? a.length > 1 ? r : s : "bottom",
      canvasElement: i.engine.getCanvasElement()
    });
    return {
      dispose: () => {
        this._globalPopupManagerService.removePopup(d), c.complete(), A.dispose();
      },
      canDispose: () => this._globalPopupManagerService.activePopupId !== d
    };
  }
  // #endregion
};
is = Fh([
  bn(0, z(Lc)),
  bn(1, fe),
  bn(2, Q),
  bn(3, y)
], is);
var Hh = Object.defineProperty, kh = Object.getOwnPropertyDescriptor, Vh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? kh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Hh(e, t, s), s;
}, jh = (n, e) => (t, o) => e(t, o, n);
const Wh = (n, e, t, o) => {
  var h, u, g, f, p;
  const s = t.findNodePositionByCharIndex(n.startOffset, !0, n.segmentId, o), r = t.getSkeletonData();
  let i = n.endOffset;
  if (n.segmentId) {
    const m = (p = Array.from((u = (h = r == null ? void 0 : r.skeFooters.get(n.segmentId)) == null ? void 0 : h.values()) != null ? u : [])[0]) != null ? p : Array.from((f = (g = r == null ? void 0 : r.skeHeaders.get(n.segmentId)) == null ? void 0 : g.values()) != null ? f : [])[0];
    m && (i = Math.min(m.ed, i));
  }
  const a = t.findNodePositionByCharIndex(i, !0, n.segmentId, o);
  if (!a || !s)
    return;
  const c = e.getOffsetConfig(), A = new it(c, t), { borderBoxPointGroup: l } = A.getRangePointData(s, a);
  return Bs(l).map((m) => ({
    top: m.top + c.docsTop - ai,
    bottom: m.bottom + c.docsTop + ai,
    left: m.left + c.docsLeft,
    right: m.right + c.docsLeft
  }));
}, zh = (n, e, t, o = -1) => {
  const s = t.findPositionByGlyph(n, o);
  if (!s)
    return;
  const r = e.getOffsetConfig(), i = { ...s, isBack: !0 }, a = new it(r, t), { borderBoxPointGroup: c } = a.getRangePointData(i, i), l = Bs(c)[0];
  return {
    top: l.top + r.docsTop,
    bottom: l.bottom + r.docsTop,
    left: l.left + r.docsLeft,
    right: l.left + r.docsLeft + n.width
  };
};
let Gn = class extends ue {
  constructor(e, t) {
    super();
    x(this, "_hoverCustomRanges$", new Le([]));
    x(this, "hoverCustomRanges$", this._hoverCustomRanges$.pipe(vr((e, t) => e.length === t.length && e.every((o, s) => t[s].range.rangeId === o.range.rangeId && t[s].segmentId === o.segmentId && t[s].segmentPageIndex === o.segmentPageIndex && t[s].range.startIndex === o.range.startIndex))));
    x(this, "_clickCustomRanges$", new Ee());
    x(this, "clickCustomRanges$", this._clickCustomRanges$.asObservable());
    x(this, "_hoverBullet$", new Ee());
    x(this, "hoverBullet$", this._hoverBullet$.pipe(vr((e, t) => (e == null ? void 0 : e.paragraph.startIndex) === (t == null ? void 0 : t.paragraph.startIndex) && (e == null ? void 0 : e.segmentId) === (t == null ? void 0 : t.segmentId) && (e == null ? void 0 : e.segmentPageIndex) === (t == null ? void 0 : t.segmentPageIndex))));
    x(this, "_clickBullet$", new Ee());
    x(this, "clickBullets$", this._clickBullet$.asObservable());
    x(this, "_customRangeDirty", !0);
    x(this, "_bulletDirty", !0);
    /**
     * cache the bounding of custom ranges,
     * it will be updated when the doc-skeleton is recalculated
     */
    x(this, "_customRangeBounds", []);
    /**
     * cache the bounding of bullets,
     * it will be updated when the doc-skeleton is recalculated
     */
    x(this, "_bulletBounds", []);
    this._context = e, this._docSkeletonManagerService = t, this._initResetDirty(), this._initEvents(), this._initPointer();
  }
  get _skeleton() {
    return this._docSkeletonManagerService.getSkeleton();
  }
  get _documents() {
    return this._context.mainComponent;
  }
  dispose() {
    this._hoverCustomRanges$.complete(), this._clickCustomRanges$.complete(), super.dispose();
  }
  _initPointer() {
    let e = mt.TEXT;
    this.disposeWithMe(this.hoverCustomRanges$.subscribe((t) => {
      t.length ? (e = this._context.scene.getCursor(), this._context.scene.setCursor(mt.POINTER)) : this._context.scene.setCursor(e);
    }));
  }
  _initResetDirty() {
    this.disposeWithMe(this._skeleton.dirty$.subscribe(() => {
      this._customRangeDirty = !0, this._bulletDirty = !0;
    })), this.disposeWithMe(
      nn(this._context.engine.onTransformChange$).pipe(
        Qn((e) => e.type === yi.resize)
      ).subscribe(() => {
        this._customRangeDirty = !0, this._bulletDirty = !0;
      })
    );
  }
  _initEvents() {
    this.disposeWithMe(nn(this._context.scene.onPointerMove$).pipe(Hi(30)).subscribe((o) => {
      this._hoverCustomRanges$.next(
        this._calcActiveRanges(o)
      ), this._hoverBullet$.next(
        this._calcActiveBullet(o)
      );
    })), this.disposeWithMe(this._context.scene.onPointerEnter$.subscribeEvent(() => {
      this._hoverBullet$.next(null), this._hoverCustomRanges$.next([]);
    }));
    const e = nn(this._context.mainComponent.onPointerDown$), t = nn(this._context.scene.onPointerUp$);
    this.disposeWithMe(e.pipe(
      jc((o) => t.pipe(Wc(1), gn((s) => ({ down: o, up: s })))),
      Qn(({ down: o, up: s }) => o.target === s.target && s.timeStamp - o.timeStamp < 300)
      // filter(({ down, up }) => down.offsetX === up.offsetX && down.offsetY === up.offsetY)
    ).subscribe(({ down: o }) => {
      if (o.button === 2)
        return;
      const s = this._calcActiveRanges(o);
      s.length && this._clickCustomRanges$.next(s.pop());
      const r = this._calcActiveBullet(o);
      r && this._clickBullet$.next(r);
    }));
  }
  _buildCustomRangeBoundsBySegment(e, t = -1) {
    var r, i, a;
    const o = (a = (i = (r = this._context.unit.getSelfOrHeaderFooterModel(e)) == null ? void 0 : r.getBody()) == null ? void 0 : i.customRanges) != null ? a : [], s = [];
    return o.forEach((c) => {
      const A = {
        startOffset: c.startIndex,
        endOffset: c.endIndex + 1,
        collapsed: !1,
        segmentId: e
      }, l = Wh(A, this._documents, this._skeleton, t);
      if (!l)
        return null;
      s.push({
        customRange: c,
        rects: l,
        segmentId: e,
        segmentPageIndex: t
      });
    }), s;
  }
  _buildCustomRangeBounds() {
    var t;
    if (!this._customRangeDirty)
      return;
    this._customRangeDirty = !1;
    const e = [];
    e.push(...this._buildCustomRangeBoundsBySegment()), (t = this._skeleton.getSkeletonData()) == null || t.pages.forEach((o, s) => {
      o.headerId && e.push(...this._buildCustomRangeBoundsBySegment(o.headerId, s)), o.footerId && e.push(...this._buildCustomRangeBoundsBySegment(o.footerId, s));
    }), this._customRangeBounds = e;
  }
  _calcActiveRanges(e) {
    this._buildCustomRangeBounds();
    const { offsetX: t, offsetY: o } = e, { x: s, y: r } = Ai(t, o, this._context.scene);
    return this._customRangeBounds.filter((a) => a.rects.some((c) => {
      const { left: A, right: l, top: d, bottom: h } = c;
      return s >= A && s <= l && r >= d && r <= h;
    })).map(
      (a) => ({
        segmentId: a.segmentId,
        range: a.customRange,
        segmentPageIndex: a.segmentPageIndex,
        rects: a.rects
      })
    );
  }
  _buildBulletBoundsBySegment(e, t = -1) {
    var c, A, l, d, h;
    const o = (c = this._context.unit.getSelfOrHeaderFooterModel(e)) == null ? void 0 : c.getBody(), s = ((A = o == null ? void 0 : o.paragraphs) != null ? A : []).filter((u) => u.bullet && u.bullet.listType.indexOf("CHECK_LIST") === 0), r = [], i = this._skeleton.getSkeletonData();
    if (!i)
      return r;
    const a = (u) => {
      var g, f, p;
      for (const m of u) {
        const E = [...m.sections];
        if (m.skeTables) {
          const I = Array.from(m.skeTables.values());
          E.push(...I.map((v) => v.rows.map((R) => R.cells.map((S) => S.sections))).flat(4));
        }
        for (const I of E)
          for (const v of I.columns)
            for (const R of v.lines)
              if (R.paragraphStart) {
                const S = s.find((C) => C.startIndex === R.paragraphIndex);
                if (S) {
                  const C = R, T = (p = (f = (g = C == null ? void 0 : C.divides) == null ? void 0 : g[0]) == null ? void 0 : f.glyphGroup) == null ? void 0 : p[0];
                  if (!T)
                    continue;
                  const O = zh(T, this._documents, this._skeleton, t);
                  if (!O)
                    continue;
                  r.push({
                    rect: O,
                    segmentId: e,
                    segmentPageIndex: t,
                    paragraph: S
                  });
                }
              }
      }
      return r;
    };
    if (e) {
      const u = (h = (l = i.skeFooters.get(e)) == null ? void 0 : l.values()) != null ? h : (d = i.skeHeaders.get(e)) == null ? void 0 : d.values();
      return u ? a(Array.from(u)) : r;
    }
    return a(i.pages);
  }
  _buildBulletBounds() {
    var e;
    this._bulletDirty && (this._bulletDirty = !1, this._bulletBounds = [], this._bulletBounds.push(...this._buildBulletBoundsBySegment()), (e = this._skeleton.getSkeletonData()) == null || e.pages.forEach((t, o) => {
      t.headerId && this._bulletBounds.push(...this._buildBulletBoundsBySegment(t.headerId, o)), t.footerId && this._bulletBounds.push(...this._buildBulletBoundsBySegment(t.footerId, o));
    }));
  }
  _calcActiveBullet(e) {
    this._buildBulletBounds();
    const { offsetX: t, offsetY: o } = e, { x: s, y: r } = Ai(t, o, this._context.scene);
    return this._bulletBounds.find((a) => {
      const { left: c, right: A, top: l, bottom: d } = a.rect;
      return s >= c && s <= A && r >= l && r <= d;
    });
  }
};
Gn = Vh([
  jh(1, z(ie))
], Gn);
var Gh = Object.defineProperty, Yh = Object.getOwnPropertyDescriptor, qh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Yh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Gh(e, t, s), s;
}, xn = (n, e) => (t, o) => e(t, o, n);
let as = class extends ue {
  constructor(n, e, t, o, s) {
    super(), this._context = n, this._docSkeletonManagerService = e, this._commandService = t, this._docEventManagerService = o, this._textSelectionManagerService = s, this._initPointerDownObserver(), this._initHoverCursor();
  }
  _initPointerDownObserver() {
    this._docEventManagerService.clickBullets$.subscribe((n) => {
      const e = this._textSelectionManagerService.getTextRanges();
      this._commandService.executeCommand(Ns.id, {
        index: n.paragraph.startIndex,
        segmentId: n.segmentId,
        textRanges: e
      });
    });
  }
  _initHoverCursor() {
    this.disposeWithMe(
      this._docEventManagerService.hoverBullet$.subscribe((n) => {
        n ? this._context.mainComponent.setCursor(mt.POINTER) : this._context.mainComponent.setCursor(mt.TEXT);
      })
    );
  }
  _getTransformCoordForDocumentOffset(n, e, t, o) {
    const { documentTransform: s } = n.getOffsetConfig(), r = e.transformVector2SceneCoord(rn.FromArray([t, o]));
    if (r)
      return s.clone().invert().applyPoint(r);
  }
};
as = qh([
  xn(1, z(ie)),
  xn(2, y),
  xn(3, z(Gn)),
  xn(4, z(G))
], as);
var Kh = Object.defineProperty, Xh = Object.getOwnPropertyDescriptor, Jh = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Xh(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Kh(e, t, s), s;
}, Zt = (n, e) => (t, o) => e(t, o, n);
let Yn = class extends At {
  constructor(n, e, t, o, s, r) {
    super(), this._context = n, this._commandService = e, this._docClipboardService = t, this._docSelectionRenderService = o, this._contextService = s, this._editorService = r, this._init();
  }
  _init() {
    this._initLegacyPasteCommand();
  }
  _initLegacyPasteCommand() {
    var n;
    (n = this._docSelectionRenderService) == null || n.onPaste$.pipe(st(this.dispose$)).subscribe((e) => {
      var c, A, l;
      if (!Io(this._contextService))
        return;
      e.event.preventDefault();
      const t = e.event;
      let o = (c = t.clipboardData) == null ? void 0 : c.getData(Ni);
      const s = (A = t.clipboardData) == null ? void 0 : A.getData(Qi), r = [
        wi,
        Di,
        Pi,
        _i
      ], i = [...((l = t.clipboardData) == null ? void 0 : l.items) || []].filter((d) => r.includes(d.type)).map((d) => d.getAsFile()).filter((d) => !!d);
      this._editorService.getEditor(this._context.unitId) && (o != null ? o : "").indexOf("</table>") > -1 && (o = ""), this._docClipboardService.legacyPaste({ html: o, text: s, files: i });
    });
  }
};
Yn = Jh([
  Zt(1, y),
  Zt(2, Sn),
  Zt(3, z(Se)),
  Zt(4, ms),
  Zt(5, He)
], Yn);
var Zh = Object.defineProperty, $h = Object.getOwnPropertyDescriptor, eg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? $h(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Zh(e, t, s), s;
}, li = (n, e) => (t, o) => e(t, o, n);
const tg = [
  pi,
  ec,
  vs,
  $e
];
let cs = class extends ue {
  constructor(n, e, t) {
    super(), this._context = n, this._contextMenuService = e, this._commandService = t, tg.includes(this._context.unitId) || (this._initPointerDown(), this._initEditChange());
  }
  _initPointerDown() {
    var t, o;
    const e = ((o = (t = this._context) == null ? void 0 : t.mainComponent) == null ? void 0 : o.onPointerDown$).subscribeEvent((s) => {
      s.button === 2 && this._contextMenuService.triggerContextMenu(s, Ui.MAIN_AREA);
    });
    this.disposeWithMe(e);
  }
  _initEditChange() {
    this.disposeWithMe(
      this._commandService.onCommandExecuted((n) => {
        n.id === J.id && this._contextMenuService.visible && this._contextMenuService.hideContextMenu();
      })
    );
  }
};
cs = eg([
  li(1, Fc),
  li(2, y)
], cs);
var ng = Object.defineProperty, og = Object.getOwnPropertyDescriptor, sg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? og(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && ng(e, t, s), s;
}, xt = (n, e) => (t, o) => e(t, o, n);
let qn = class extends ue {
  constructor(e, t, o, s, r, i, a) {
    super();
    x(this, "_initialEditors", /* @__PURE__ */ new Set());
    this._context = e, this._univerInstanceService = t, this._editorService = o, this._commandService = s, this._docSelectionRenderService = r, this._docSkeletonManagerService = i, this._renderManagerService = a, this._initialize();
  }
  _initialize() {
    this._editorService.getAllEditor().forEach((e) => {
      const t = e.getEditorId();
      t === this._context.unitId && (this._initialEditors.has(t) || (this._initialEditors.add(t), this._resize(t)));
    }), this._commandExecutedListener(), this._initialBlur(), this._initialFocus();
  }
  _resize(e) {
    if (e == null)
      return;
    const t = this._editorService.getEditor(e);
    if ((t == null ? void 0 : t.cancelDefaultResizeListener) === !0)
      return;
    const o = this._univerInstanceService.getUniverDocInstance(e);
    if (!o)
      return;
    const s = this._docSkeletonManagerService.getSkeleton();
    if (t == null || t.render == null || s == null || o == null)
      return;
    s.calculate();
    const { marginTop: r = 0, marginBottom: i = 0, marginLeft: a = 0, marginRight: c = 0 } = o.getSnapshot().documentStyle, { scene: A, mainComponent: l } = t.render;
    let { actualHeight: d, actualWidth: h } = s.getActualSize();
    d += r + i, h += a + c;
    const { width: u, height: g } = t.getBoundingClientRect(), f = Math.max(h, u), p = Math.max(d, g);
    A.transformByState({
      width: f,
      height: p
    }), l == null || l.resize(f, p);
  }
  _initialBlur() {
    this.disposeWithMe(
      this._editorService.blur$.subscribe(() => {
        this._docSelectionRenderService.blur();
      })
    ), this.disposeWithMe(
      this._docSelectionRenderService.onBlur$.subscribe(() => {
        const { unitId: e } = this._context, t = this._editorService.getEditor(e), o = this._editorService.getFocusEditor();
        t == null || t.isSheetEditor() || o && o.getEditorId() === e || e.includes("range_selector") || e.includes("embedding_formula_editor") || this._editorService.blur();
      })
    );
  }
  _initialFocus() {
    const e = [
      "univer-formula-search",
      "univer-formula-help",
      "formula-help-decorator",
      "univer-formula-help-param"
    ];
    this.disposeWithMe(
      Ue(window, "mousedown").subscribe((o) => {
        const r = o.target.classList[0] || "";
        tc(r, e) && o.stopPropagation();
      })
    ), this._univerInstanceService.getAllUnitsForType(_.UNIVER_SHEET).forEach((o) => {
      const s = o.getUnitId(), r = this._renderManagerService.getRenderById(s), i = r == null ? void 0 : r.engine.getCanvas().getCanvasEle();
      i != null && Ue(i, "mousedown").subscribe((a) => {
        a.stopPropagation();
      });
    });
  }
  /**
   * Listen to document edits to refresh the size of the formula editor.
   */
  _commandExecutedListener() {
    const e = [J.id];
    this.disposeWithMe(
      this._commandService.onCommandExecuted((t) => {
        if (e.includes(t.id)) {
          const o = t.params, { unitId: s } = o;
          if (this._editorService.isSheetEditor(s) || s !== this._context.unitId)
            return;
          const r = this._editorService.getEditor(s);
          r && !r.params.scrollBar && this._resize(s);
        }
      })
    );
  }
};
qn = sg([
  xt(1, Q),
  xt(2, He),
  xt(3, y),
  xt(4, z(Se)),
  xt(5, z(ie)),
  xt(6, fe)
], qn);
var rg = Object.defineProperty, ig = Object.getOwnPropertyDescriptor, ag = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? ig(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && rg(e, t, s), s;
}, On = (n, e) => (t, o) => e(t, o, n);
let As = class extends ue {
  constructor(e, t, o, s, r) {
    super();
    x(this, "_previousIMEContent", "");
    x(this, "_isCompositionStart", !0);
    x(this, "_onStartSubscription");
    x(this, "_onUpdateSubscription");
    x(this, "_onEndSubscription");
    this._context = e, this._docSelectionRenderService = t, this._docImeInputManagerService = o, this._docSkeletonManagerService = s, this._commandService = r, this._initialize();
  }
  dispose() {
    var e, t, o;
    (e = this._onStartSubscription) == null || e.unsubscribe(), (t = this._onUpdateSubscription) == null || t.unsubscribe(), (o = this._onEndSubscription) == null || o.unsubscribe();
  }
  _initialize() {
    this._initialOnCompositionstart(), this._initialOnCompositionUpdate(), this._initialOnCompositionend();
  }
  _initialOnCompositionstart() {
    this._onStartSubscription = this._docSelectionRenderService.onCompositionstart$.subscribe((e) => {
      if (e == null)
        return;
      this._resetIME();
      const { activeRange: t } = e;
      t != null && this._docImeInputManagerService.setActiveRange(X.deepClone(t));
    });
  }
  _initialOnCompositionUpdate() {
    this._onUpdateSubscription = this._docSelectionRenderService.onCompositionupdate$.subscribe((e) => {
      this._updateContent(e, !0);
    });
  }
  _initialOnCompositionend() {
    this._onEndSubscription = this._docSelectionRenderService.onCompositionend$.subscribe((e) => {
      this._updateContent(e, !1);
    });
  }
  async _updateContent(e, t) {
    if (e == null)
      return;
    const o = this._context.unitId, s = this._docSkeletonManagerService.getSkeleton(), { event: r, activeRange: i } = e;
    if (s == null || i == null)
      return;
    const c = r.data;
    c === this._previousIMEContent && t || (await this._commandService.executeCommand(Ba.id, {
      unitId: o,
      newText: c,
      oldTextLen: this._previousIMEContent.length,
      isCompositionStart: this._isCompositionStart,
      isCompositionEnd: !t
    }), t ? (this._isCompositionStart && (this._isCompositionStart = !1), this._previousIMEContent = c) : this._resetIME());
  }
  _resetIME() {
    this._previousIMEContent = "", this._isCompositionStart = !0, this._docImeInputManagerService.clearUndoRedoMutationParamsCache(), this._docImeInputManagerService.setActiveRange(null);
  }
};
As = ag([
  On(1, z(Se)),
  On(2, z(Ro)),
  On(3, z(ie)),
  On(4, y)
], As);
var cg = Object.defineProperty, Ag = Object.getOwnPropertyDescriptor, lg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Ag(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && cg(e, t, s), s;
}, Tn = (n, e) => (t, o) => e(t, o, n);
let ls = class extends ue {
  constructor(e, t, o, s, r) {
    super();
    x(this, "_onInputSubscription");
    this._context = e, this._docSelectionRenderService = t, this._docSkeletonManagerService = o, this._commandService = s, this._docMenuStyleService = r, this._init();
  }
  dispose() {
    var e;
    super.dispose(), (e = this._onInputSubscription) == null || e.unsubscribe();
  }
  _init() {
    this._initialNormalInput();
  }
  _initialNormalInput() {
    this._onInputSubscription = this._docSelectionRenderService.onInput$.subscribe(async (e) => {
      var p, m, E;
      if (e == null)
        return;
      const { unitId: t } = this._context, { event: o, content: s = "", activeRange: r } = e, i = o, a = this._docSkeletonManagerService.getSkeleton();
      if (i.data == null || a == null || r == null)
        return;
      const { segmentId: c } = r, l = this._context.unit.getSelfOrHeaderFooterModel(c).getBody(), d = this._docMenuStyleService.getDefaultStyle(), h = this._docMenuStyleService.getStyleCache(), u = Os((p = l == null ? void 0 : l.customRanges) != null ? p : [], r.endOffset, Is.includes(t)), g = co((m = l == null ? void 0 : l.textRuns) != null ? m : [], r.endOffset, d, h), f = Ts((E = l == null ? void 0 : l.customDecorations) != null ? E : [], r.endOffset);
      await this._commandService.executeCommand(Vs.id, {
        unitId: t,
        body: {
          dataStream: s,
          textRuns: g ? [
            {
              ...g,
              st: 0,
              ed: s.length
            }
          ] : [],
          customRanges: u ? [{
            ...u,
            startIndex: 0,
            endIndex: s.length - 1
          }] : [],
          customDecorations: f.map((I) => ({
            ...I,
            startIndex: 0,
            endIndex: s.length - 1
          }))
        },
        range: r,
        segmentId: c
      }), s === " " && await this._commandService.executeCommand(Ao.id);
    });
  }
};
ls = lg([
  Tn(1, z(Se)),
  Tn(2, z(ie)),
  Tn(3, y),
  Tn(4, z(Je))
], ls);
class ar extends ue {
  constructor(e) {
    super(), this._context = e;
  }
  calculatePagePosition() {
    var v, R;
    const e = rt(this._context), o = (R = (v = this._context.unit.getSettings()) == null ? void 0 : v.zoomRatio) != null ? R : 1, { document: s, scene: r, docBackground: i } = e, a = r == null ? void 0 : r.getParent(), { width: c, height: A, pageMarginLeft: l, pageMarginTop: d } = s;
    if (a == null || c === Number.POSITIVE_INFINITY || A === Number.POSITIVE_INFINITY)
      return;
    const { width: h, height: u } = a;
    let g = 0, f = d, p = 0, m = 0, E = Number.POSITIVE_INFINITY;
    h > (c + l * 2) * o ? (g = h / 2 - c * o / 2, g /= o, p = (h - l * 2) / o, E = 0) : (g = l, p = c + l * 2, E = (p - h / o) / 2), u > A ? m = (u - d * 2) / o : m = A + d * 2, r.resize(p, m), h <= 1 && (g = -1e4, f = -1e4), s.translate(g, f), i.translate(g, f);
    const I = r.getViewport(Xe.VIEW_MAIN);
    return E !== Number.POSITIVE_INFINITY && I != null && I.scrollToViewportPos({
      viewportScrollX: E
    }), this;
  }
}
var dg = Object.defineProperty, ug = Object.getOwnPropertyDescriptor, hg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? ug(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && dg(e, t, s), s;
}, di = (n, e) => (t, o) => e(t, o, n);
let ds = class extends ue {
  constructor(n, e, t) {
    super(), this._context = n, this._docPageLayoutService = e, this._textSelectionManagerService = t;
    const o = this._context.unitId;
    if (to(o) && o !== $e) return this;
    this._initResize();
  }
  _initResize() {
    this.disposeWithMe(
      nn(this._context.engine.onTransformChange$).pipe(
        Qn((n) => n.type === yi.resize),
        Hi(0, zc)
      ).subscribe(() => {
        this._docPageLayoutService.calculatePagePosition(), this._textSelectionManagerService.refreshSelection();
      })
    );
  }
};
ds = hg([
  di(1, z(ar)),
  di(2, z(G))
], ds);
var gg = Object.defineProperty, fg = Object.getOwnPropertyDescriptor, pg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? fg(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && gg(e, t, s), s;
}, Ot = (n, e) => (t, o) => e(t, o, n);
let us = class extends ue {
  constructor(e, t, o, s, r, i, a) {
    super();
    x(this, "_loadedMap", /* @__PURE__ */ new WeakSet());
    this._context = e, this._commandService = t, this._editorService = o, this._instanceSrv = s, this._docSelectionRenderService = r, this._docSkeletonManagerService = i, this._docSelectionManagerService = a, this._initialize();
  }
  _initialize() {
    this._init(), this._skeletonListener(), this._commandExecutedListener(), this._refreshListener(), this._syncSelection();
  }
  _init() {
    const { unitId: e } = this._context, t = rt(this._context);
    t == null || t.document == null || this._loadedMap.has(t.document) || (this._initialMain(e), this._loadedMap.add(t.document));
  }
  _refreshListener() {
    this.disposeWithMe(
      this._docSelectionManagerService.refreshSelection$.subscribe((e) => {
        if (e == null)
          return;
        const { unitId: t, docRanges: o, isEditing: s, options: r } = e;
        t === this._context.unitId && (this._docSelectionRenderService.removeAllRanges(), this._docSelectionRenderService.addDocRanges(o, s, r));
      })
    );
  }
  _syncSelection() {
    this.disposeWithMe(
      this._docSelectionRenderService.textSelectionInner$.subscribe((e) => {
        e != null && this._docSelectionManagerService.__replaceTextRangesWithNoRefresh(e, {
          unitId: this._context.unitId,
          subUnitId: this._context.unitId
        });
      })
    );
  }
  // eslint-disable-next-line max-lines-per-function
  _initialMain(e) {
    const t = rt(this._context), { document: o, scene: s } = t;
    this.disposeWithMe(o.onPointerEnter$.subscribeEvent(() => {
      this._isEditorReadOnly(e) || (o.cursor = mt.TEXT);
    })), this.disposeWithMe(o.onPointerLeave$.subscribeEvent(() => {
      o.cursor = mt.DEFAULT, s.resetCursor();
    })), this.disposeWithMe(o.onPointerDown$.subscribeEvent((r, i) => {
      if (this._isEditorReadOnly(e))
        return;
      const a = this._instanceSrv.getCurrentUnitForType(_.UNIVER_DOC);
      (a == null ? void 0 : a.getUnitId()) !== e && this._instanceSrv.setCurrentUnitForType(e);
      const c = this._docSkeletonManagerService.getSkeleton(), { offsetX: A, offsetY: l } = r, d = this._getTransformCoordForDocumentOffset(A, l);
      if (d != null) {
        const {
          pageLayoutType: h = an.VERTICAL,
          pageMarginLeft: u,
          pageMarginTop: g
        } = o.getOffsetConfig(), { editArea: f } = c.findEditAreaByCoord(
          d,
          h,
          u,
          g
        ), p = this._docSkeletonManagerService.getViewModel(), m = p.getEditArea();
        m !== ge.BODY && f !== ge.BODY && f !== m && p.setEditArea(f);
      }
      if (this._docSelectionRenderService.__onPointDown(r), this._editorService.getEditor(e)) {
        this._setEditorFocus(e);
        const { offsetX: h, offsetY: u } = r;
        setTimeout(() => {
          e !== this._editorService.getFocusId() && (this._setEditorFocus(e), this._docSelectionRenderService.setCursorManually(h, u));
        }, 0);
      }
      r.button !== 2 && i.stopPropagation();
    })), this.disposeWithMe(o.onDblclick$.subscribeEvent((r) => {
      this._isEditorReadOnly(e) || this._docSelectionRenderService.__handleDblClick(r);
    })), this.disposeWithMe(o.onTripleClick$.subscribeEvent((r) => {
      this._isEditorReadOnly(e) || this._docSelectionRenderService.__handleTripleClick(r);
    }));
  }
  _getTransformCoordForDocumentOffset(e, t) {
    const o = rt(this._context), { document: s, scene: r } = o, { documentTransform: i } = s.getOffsetConfig(), a = r.getViewports()[0];
    if (a == null)
      return;
    const c = a.transformVector2SceneCoord(rn.FromArray([e, t]));
    return i.clone().invert().applyPoint(c);
  }
  _isEditorReadOnly(e) {
    const t = this._editorService.getEditor(e);
    return t ? t.isReadOnly() : !1;
  }
  _setEditorFocus(e) {
    this._editorService.focus(e);
  }
  _commandExecutedListener() {
    const e = [Ye.id];
    this.disposeWithMe(
      this._commandService.onCommandExecuted((t) => {
        var o;
        if (e.includes(t.id)) {
          const s = t.params, { unitId: r } = s, i = (o = this._docSelectionManagerService.__getCurrentSelection()) == null ? void 0 : o.unitId;
          if (r !== i)
            return;
          this._docSelectionManagerService.refreshSelection();
        }
      })
    );
  }
  _skeletonListener() {
    this.disposeWithMe(this._docSkeletonManagerService.currentSkeleton$.subscribe((e) => {
      if (!e) return;
      const { unitId: t } = this._context;
      if (!to(t)) {
        this._docSelectionRenderService.focus();
        const r = this._context.unit.getSnapshot(), i = ea(r);
        this._docSelectionManagerService.replaceDocRanges([
          {
            startOffset: i,
            endOffset: i
          }
        ], {
          unitId: t,
          subUnitId: t
        }, !1);
      }
    }));
  }
};
us = pg([
  Ot(1, y),
  Ot(2, He),
  Ot(3, Q),
  Ot(4, z(Se)),
  Ot(5, z(ie)),
  Ot(6, z(G))
], us);
var mg = Object.defineProperty, Eg = Object.getOwnPropertyDescriptor, Sg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Eg(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && mg(e, t, s), s;
}, ft = (n, e) => (t, o) => e(t, o, n);
let hs = class extends ue {
  constructor(n, e, t, o, s, r, i, a) {
    super(), this._context = n, this._contextService = e, this._docSkeletonManagerService = t, this._univerInstanceService = o, this._commandService = s, this._textSelectionManagerService = r, this._editorService = i, this._docPageLayoutService = a, this._initSkeletonListener(), this._initCommandExecutedListener(), this._initRenderRefresher(), setTimeout(() => this.updateViewZoom(1, !0), 20);
  }
  _initRenderRefresher() {
    this._docSkeletonManagerService.currentSkeleton$.subscribe((n) => {
      if (n == null)
        return;
      const { unitId: e, scene: t } = this._context;
      this._editorService.isEditor(e) || this.disposeWithMe(t.onMouseWheel$.subscribeEvent((o) => {
        if (!o.ctrlKey || !this._contextService.getContextValue(hn))
          return;
        const s = this._univerInstanceService.getCurrentUniverDocInstance();
        if (!s)
          return;
        const { documentFlavor: r } = s.getSnapshot().documentStyle;
        if (r === ye.MODERN)
          return;
        const i = Math.abs(o.deltaX);
        let a = i < 40 ? 0.2 : i < 80 ? 0.4 : 0.2;
        a *= o.deltaY > 0 ? -1 : 1, t.scaleX < 1 && (a /= 2);
        const c = s.zoomRatio;
        let A = +Number.parseFloat(`${c + a}`).toFixed(1);
        A = A >= 4 ? 4 : A <= 0.1 ? 0.1 : A, this._commandService.executeCommand(ss.id, {
          zoomRatio: A,
          unitId: s.getUnitId()
        }), o.preventDefault();
      }));
    });
  }
  _initSkeletonListener() {
    this.disposeWithMe(this._docSkeletonManagerService.currentSkeleton$.subscribe((n) => {
      if (n == null)
        return;
      const e = this._univerInstanceService.getCurrentUniverDocInstance();
      if (!e) return;
      const t = e.zoomRatio || 1;
      this.updateViewZoom(t, !1);
    }));
  }
  _initCommandExecutedListener() {
    const n = [Ye.id];
    this.disposeWithMe(this._commandService.onCommandExecuted((e) => {
      if (n.includes(e.id) && e.params.unitId === this._context.unitId) {
        const o = this._context.unit.zoomRatio || 1;
        this.updateViewZoom(o);
      }
    })), this.disposeWithMe(
      this._commandService.beforeCommandExecuted((e) => {
        e.id === Co.id && this._commandService.executeCommand(ss.id, {
          zoomRatio: 1,
          unitId: this._context.unitId
        });
      })
    );
  }
  updateViewZoom(n, e = !0) {
    var o;
    const t = rt(this._context);
    t.scene.scale(n, n), this._editorService.isEditor(this._context.unitId) || this._docPageLayoutService.calculatePagePosition(), e && !this._editorService.isEditor(this._context.unitId) && this._textSelectionManagerService.refreshSelection(), (o = t.scene.getTransformer()) == null || o.clearSelectedObjects();
  }
};
hs = Sg([
  ft(1, ms),
  ft(2, z(ie)),
  ft(3, Q),
  ft(4, y),
  ft(5, z(G)),
  ft(6, He),
  ft(7, z(ar))
], hs);
var Ig = Object.defineProperty, Cg = Object.getOwnPropertyDescriptor, vg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Cg(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Ig(e, t, s), s;
}, $t = (n, e) => (t, o) => e(t, o, n);
const ui = 300;
let Kn = class extends At {
  constructor(e, t, o, s, r) {
    super();
    x(this, "_docStateChange$", new Le(null));
    x(this, "docStateChange$", this._docStateChange$.asObservable());
    // This cache used for history compose.
    x(this, "_historyStateCache", /* @__PURE__ */ new Map());
    // This cache used for collaboration state compose.
    x(this, "_changeStateCache", /* @__PURE__ */ new Map());
    x(this, "_historyTimer", null);
    x(this, "_changeStateCacheTimer", null);
    this._undoRedoService = e, this._commandService = t, this._univerInstanceService = o, this._docStateEmitService = s, this._renderManagerService = r, this._initialize(), this._listenDocStateChange();
  }
  getStateCache(e) {
    var t, o;
    return {
      history: (t = this._historyStateCache.get(e)) != null ? t : [],
      collaboration: (o = this._changeStateCache.get(e)) != null ? o : []
    };
  }
  setStateCache(e, t) {
    this._historyStateCache.set(e, t.history), this._changeStateCache.set(e, t.collaboration);
  }
  _setChangeState(e) {
    this._cacheChangeState(e, "history"), this._cacheChangeState(e, "collaboration");
  }
  _initialize() {
    this.disposeWithMe(
      this._commandService.beforeCommandExecuted((e) => {
        if (e.id === hr || e.id === gr) {
          const t = this._univerInstanceService.getCurrentUniverDocInstance();
          if (t == null)
            return;
          const o = t.getUnitId();
          this._pushHistory(o), this._emitChangeState(o);
        }
      })
    );
  }
  _listenDocStateChange() {
    this._docStateEmitService.docStateChangeParams$.pipe(st(this.dispose$)).subscribe((e) => {
      var a;
      if (e == null)
        return;
      const { isCompositionEnd: t, isSync: o, syncer: s, ...r } = e, i = (a = this._renderManagerService.getRenderById(o ? s : e.unitId)) == null ? void 0 : a.with(Ro);
      if (i != null) {
        if (t) {
          const c = i.fetchComposedUndoRedoMutationParams();
          if (c == null)
            throw new Error("historyParams is null in RichTextEditingMutation");
          const { undoMutationParams: A, redoMutationParams: l, previousActiveRange: d } = c;
          r.redoState.actions = l.actions, r.undoState.actions = A.actions, r.undoState.textRanges = [d];
        }
        this._setChangeState(r);
      }
    });
  }
  _cacheChangeState(e, t = "history") {
    const { trigger: o, unitId: s, noHistory: r, debounce: i = !1 } = e;
    if (r || o == null || t === "history" && (o === gr || o === hr))
      return;
    const a = t === "history" ? this._historyStateCache : this._changeStateCache, c = t === "history" ? this._pushHistory.bind(this) : this._emitChangeState.bind(this);
    if (a.has(s)) {
      const A = a.get(s);
      A == null || A.push(e);
    } else
      a.set(s, [e]);
    i ? t === "history" ? (this._historyTimer && clearTimeout(this._historyTimer), this._historyTimer = setTimeout(() => {
      c(s);
    }, ui)) : (this._changeStateCacheTimer && clearTimeout(this._changeStateCacheTimer), this._changeStateCacheTimer = setTimeout(() => {
      c(s);
    }, ui)) : c(s);
  }
  _pushHistory(e) {
    const t = this._undoRedoService, o = this._historyStateCache.get(e);
    if (!Array.isArray(o) || o.length === 0)
      return;
    const s = o.length, r = o[0].commandId, i = o[0], a = o[s - 1], c = {
      unitId: e,
      actions: o.reduce((l, d) => k.compose(l, d.redoState.actions), null),
      textRanges: a.redoState.textRanges
    }, A = {
      unitId: e,
      // Always need to put undoParams after redoParams, because `reverse` will change the `cacheStates` order.
      actions: o.reverse().reduce((l, d) => k.compose(l, d.undoState.actions), null),
      textRanges: i.undoState.textRanges
    };
    t.pushUndoRedo({
      unitID: e,
      undoMutations: [{ id: r, params: A }],
      redoMutations: [{ id: r, params: c }]
    }), o.length = 0;
  }
  _emitChangeState(e) {
    const t = this._changeStateCache.get(e);
    if (!Array.isArray(t) || t.length === 0)
      return;
    const o = t.length, { commandId: s, trigger: r, segmentId: i, noHistory: a, debounce: c } = t[0], A = t[0], l = t[o - 1], d = {
      unitId: e,
      actions: t.reduce((g, f) => k.compose(g, f.redoState.actions), null),
      textRanges: l.redoState.textRanges
    }, h = {
      unitId: e,
      // Always need to put undoParams after redoParams, because `reverse` will change the `cacheStates` order.
      actions: t.reverse().reduce((g, f) => k.compose(g, f.undoState.actions), null),
      textRanges: A.undoState.textRanges
    }, u = {
      commandId: s,
      unitId: e,
      trigger: r,
      redoState: d,
      undoState: h,
      segmentId: i,
      noHistory: a,
      debounce: c
    };
    t.length = 0, this._docStateChange$.next(u);
  }
};
Kn = vg([
  $t(0, z(eo)),
  $t(1, y),
  $t(2, Q),
  $t(3, z(ic)),
  $t(4, fe)
], Kn);
var Rg = Object.defineProperty, bg = Object.getOwnPropertyDescriptor, xg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? bg(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Rg(e, t, s), s;
}, hi = (n, e) => (t, o) => e(t, o, n);
const gi = "univer-doc-main-canvas";
let Xn = class extends At {
  constructor(n, e) {
    super(), this._instanceSrv = n, this._renderManagerService = e, this._init();
  }
  _init() {
    this._renderManagerService.createRender$.pipe(st(this.dispose$)).subscribe((n) => this._createRenderWithId(n)), this._instanceSrv.getAllUnitsForType(_.UNIVER_DOC).forEach((n) => this._createRenderer(n)), this._instanceSrv.getTypeOfUnitAdded$(_.UNIVER_DOC).pipe(st(this.dispose$)).subscribe((n) => this._createRenderer(n)), this._instanceSrv.getTypeOfUnitDisposed$(_.UNIVER_DOC).pipe(st(this.dispose$)).subscribe((n) => this._disposeRenderer(n));
  }
  _createRenderer(n) {
    var o;
    const e = n.getUnitId(), t = (o = this._instanceSrv.getCurrentUnitForType(_.UNIVER_DOC)) == null ? void 0 : o.getUnitId();
    this._renderManagerService.created$.subscribe((s) => {
      s.unitId === t && (s.engine.getCanvas().setId(gi), s.engine.getCanvas().getContext().setId(gi));
    }), this._renderManagerService.has(e) || (this._createRenderWithId(e), this._renderManagerService.setCurrent(e));
  }
  _createRenderWithId(n) {
    this._renderManagerService.createRender(n);
  }
  _disposeRenderer(n) {
    const e = n.getUnitId();
    this._renderManagerService.removeRender(e);
  }
};
Xn = xg([
  hi(0, Q),
  hi(1, fe)
], Xn);
class Og extends ue {
  constructor() {
    super(...arguments);
    x(this, "_currentSelectorId");
    x(this, "_selectionChange$", new Ee());
    x(this, "selectionChange$", this._selectionChange$.asObservable());
    x(this, "_openSelector$", new Ee());
    x(this, "openSelector$", this._openSelector$.asObservable());
    x(this, "_selectorModalVisible$", new Le(!1));
    x(this, "selectorModalVisible$", this._selectorModalVisible$.asObservable());
  }
  get selectorModalVisible() {
    return this._selectorModalVisible$.getValue();
  }
  setCurrentSelectorId(t) {
    this._currentSelectorId = t;
  }
  getCurrentSelectorId() {
    return this._currentSelectorId;
  }
  selectionChange(t) {
    this._currentSelectorId && this._selectionChange$.next(t);
  }
  openSelector() {
    this._openSelector$.next(null);
  }
  triggerModalVisibleChange(t) {
    this._selectorModalVisible$.next(t);
  }
}
const Tg = ps(
  "univer.range-selector.service"
), yg = {
  id: ln.id,
  preconditions: bl,
  binding: j.ENTER
}, Bg = {
  id: So.id,
  preconditions: de,
  binding: j.BACKSPACE
}, Mg = {
  id: ma.id,
  preconditions: de,
  binding: j.DELETE
}, _g = {
  id: at.id,
  binding: j.ARROW_UP,
  preconditions: de,
  staticParameters: {
    direction: se.UP
  }
}, Pg = {
  id: at.id,
  binding: j.ARROW_DOWN,
  preconditions: de,
  staticParameters: {
    direction: se.DOWN
  }
}, Dg = {
  id: at.id,
  binding: j.ARROW_LEFT,
  preconditions: de,
  staticParameters: {
    direction: se.LEFT
  }
}, wg = {
  id: at.id,
  binding: j.ARROW_RIGHT,
  preconditions: de,
  staticParameters: {
    direction: se.RIGHT
  }
}, Ng = {
  id: ct.id,
  binding: j.ARROW_UP | K.SHIFT,
  preconditions: de,
  staticParameters: {
    direction: se.UP
  }
}, Qg = {
  id: ct.id,
  binding: j.ARROW_DOWN | K.SHIFT,
  preconditions: de,
  staticParameters: {
    direction: se.DOWN
  }
}, Ug = {
  id: ct.id,
  binding: j.ARROW_LEFT | K.SHIFT,
  preconditions: de,
  staticParameters: {
    direction: se.LEFT
  }
}, Lg = {
  id: ct.id,
  binding: j.ARROW_RIGHT | K.SHIFT,
  preconditions: de,
  staticParameters: {
    direction: se.RIGHT
  }
}, Fg = {
  id: ya.id,
  binding: j.A | K.CTRL_COMMAND,
  preconditions: (n) => n.getContextValue(Ss) && (n.getContextValue(hn) || n.getContextValue(wn))
};
var Na = Object.defineProperty, Hg = Object.getOwnPropertyDescriptor, kg = (n, e, t) => e in n ? Na(n, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : n[e] = t, Vg = (n, e, t, o) => {
  for (var s = o > 1 ? void 0 : o ? Hg(e, t) : e, r = n.length - 1, i; r >= 0; r--)
    (i = n[r]) && (s = (o ? i(e, t, s) : i(s)) || s);
  return o && s && Na(e, t, s), s;
}, en = (n, e) => (t, o) => e(t, o, n), jg = (n, e, t) => kg(n, e + "", t);
let gs = class extends oc {
  // static override type = UniverInstanceType.UNIVER_DOC;
  constructor(n = qr, e, t, o, s, r) {
    super(), this._config = n, this._injector = e, this._renderManagerSrv = t, this._commandService = o, this._logService = s, this._configService = r;
    const { menu: i, ...a } = sc(
      {},
      qr,
      this._config
    );
    i && this._configService.setConfig("menu", i, { merge: !0 }), this._configService.setConfig(Us, a), this._initDependencies(e), this._initializeShortcut(), this._initCommand();
  }
  onReady() {
    this._initRenderBasics(), this._markDocAsFocused(), fr(this._injector, [
      [Kn],
      [Xn]
    ]);
  }
  onRendered() {
    this._initUI(), this._initRenderModules(), fr(this._injector, [
      [jn],
      [Wn],
      [Lt],
      [zn],
      // FIXME: LifecycleStages.Rendered must be used, otherwise the menu cannot be added to the DOM, but the sheet ui
      // plugin can be added in LifecycleStages.Ready
      [Hn]
    ]);
  }
  _initCommand() {
    [
      So,
      ma,
      Vt,
      jt,
      Wt,
      zt,
      Ct,
      Gt,
      Pt,
      Dt,
      wt,
      fn,
      Nt,
      lt,
      Ra,
      Vs,
      dn,
      js,
      pa,
      Ws,
      Ye,
      ho,
      uo,
      pn,
      go,
      fo,
      po,
      et,
      mo,
      ba,
      Ia,
      er,
      tr,
      Fd,
      nr,
      or,
      Xs,
      Js,
      In,
      Ps,
      Ma,
      _t,
      Ao,
      ln,
      es,
      lo,
      ws,
      Ns,
      da,
      Ba,
      Co,
      qe,
      fa,
      Qt,
      gA,
      Vi,
      fA,
      ss,
      ya,
      rr,
      at,
      ct,
      mA
    ].forEach((n) => {
      this._commandService.registerCommand(n);
    }), [Fn, qs, Ks].forEach((n) => this.disposeWithMe(this._commandService.registerMultipleCommand(n)));
  }
  _initializeShortcut() {
    [
      _g,
      Pg,
      wg,
      Dg,
      Ng,
      Qg,
      Ug,
      Lg,
      Fg,
      Bg,
      Mg,
      yg,
      Ol
    ].forEach((n) => {
      this._injector.get(ro).registerShortcut(n);
    });
  }
  _initDependencies(n) {
    rc([
      [Yn],
      [qn],
      [Hn],
      [jn],
      [zn],
      [Wn],
      [Vn],
      [Lt],
      [He, { useClass: Jo }],
      [Tg, { useClass: Og }],
      [Sn, { useClass: ns }],
      [is],
      [Xn],
      [Kn],
      [Et],
      [Je]
    ], this._config.override).forEach((t) => n.add(t));
  }
  _markDocAsFocused() {
    const n = this._injector.get(Q), e = this._injector.get(He);
    try {
      const t = n.getCurrentUnitForType(_.UNIVER_DOC);
      if (!t) return;
      const o = t.getUnitId();
      e.isEditor(o) || n.focusUnit(t.getUnitId());
    } catch (t) {
      this._logService.warn(t);
    }
  }
  _initUI() {
    this._injector.get(Vn);
  }
  _initRenderBasics() {
    [
      [ie],
      [Se],
      [ac],
      [ar],
      [Ro],
      [os],
      [hs]
    ].forEach((n) => {
      this._renderManagerSrv.registerRenderModule(_.UNIVER_DOC, n);
    });
  }
  _initRenderModules() {
    [
      [Gn],
      [kn],
      [us],
      [Zo],
      [ds],
      [cs],
      [as],
      [Yn],
      [ls],
      [As],
      [qn]
    ].forEach((n) => {
      this._renderManagerSrv.registerRenderModule(_.UNIVER_DOC, n);
    });
  }
};
jg(gs, "pluginName", rA);
gs = Vg([
  nc(xc),
  en(1, z(so)),
  en(2, fe),
  en(3, y),
  en(4, fs),
  en(5, Rs)
], gs);
export {
  Ao as AfterSpaceCommand,
  fo as AlignCenterCommand,
  mo as AlignJustifyCommand,
  go as AlignLeftCommand,
  et as AlignOperationCommand,
  po as AlignRightCommand,
  Ra as BreakLineCommand,
  uo as BulletListCommand,
  es as ChangeListNestingLevelCommand,
  Pn as ChangeListNestingLevelType,
  lo as ChangeListTypeCommand,
  ws as CheckListCommand,
  fA as CoverContentCommand,
  ba as CreateDocTableCommand,
  Qt as CutContentCommand,
  iA as DOCS_COMPONENT_BACKGROUND_LAYER_INDEX,
  xr as DOCS_COMPONENT_DEFAULT_Z_INDEX,
  aA as DOCS_COMPONENT_HEADER_LAYER_INDEX,
  Oo as DOCS_COMPONENT_MAIN_LAYER_INDEX,
  We as DOCS_VIEW_KEY,
  rA as DOC_UI_PLUGIN_NAME,
  ai as DOC_VERTICAL_PADDING,
  sA as DefaultDocContainerConfig,
  oA as DefaultToolbarConfig,
  dn as DeleteCommand,
  js as DeleteCustomBlockCommand,
  So as DeleteLeftCommand,
  ma as DeleteRightCommand,
  Et as DocAutoFormatService,
  kn as DocBackScrollRenderController,
  is as DocCanvasPopManagerService,
  Fn as DocCopyCommand,
  sr as DocCreateTableOperation,
  qs as DocCutCommand,
  Gn as DocEventManagerService,
  Ro as DocIMEInputManagerService,
  Ks as DocPasteCommand,
  os as DocRenderController,
  ya as DocSelectAllCommand,
  Se as DocSelectionRenderService,
  Kn as DocStateChangeManagerService,
  Js as DocTableDeleteColumnsCommand,
  Xs as DocTableDeleteRowsCommand,
  In as DocTableDeleteTableCommand,
  Fd as DocTableInsertColumnCommand,
  nr as DocTableInsertColumnLeftCommand,
  or as DocTableInsertColumnRightCommand,
  er as DocTableInsertRowAboveCommand,
  tr as DocTableInsertRowBellowCommand,
  Ia as DocTableInsertRowCommand,
  Ma as DocTableTabCommand,
  Hn as DocUIController,
  Xn as DocsRenderService,
  Zu as DocsUIMenuSchema,
  DA as Editor,
  Ed as EditorInsertTextCommandId,
  Jo as EditorService,
  ln as EnterCommand,
  Sn as IDocClipboardService,
  He as IEditorService,
  Ba as IMEInputCommand,
  Tg as IRangeSelectorService,
  fa as InnerPasteCommand,
  Vs as InsertCommand,
  pn as ListOperationCommand,
  Ws as MergeTwoParagraphCommand,
  at as MoveCursorOperation,
  ct as MoveSelectionOperation,
  ef as NORMAL_TEXT_SELECTION_PLUGIN_NAME,
  it as NodePositionConvertToCursor,
  Gi as NodePositionConvertToRectRange,
  ho as OrderListCommand,
  xd as PastePluginLark,
  Od as PastePluginUniver,
  Td as PastePluginWord,
  da as QuickListCommand,
  Og as RangeSelectorService,
  Yi as RectRange,
  gA as ReplaceContentCommand,
  Vi as ReplaceSnapshotCommand,
  mA as ReplaceTextRunsCommand,
  fn as ResetInlineFormatTextBackgroundColorCommand,
  cf as RichTextEditor,
  ss as SetDocZoomRatioCommand,
  Ye as SetDocZoomRatioOperation,
  Vt as SetInlineFormatBoldCommand,
  lt as SetInlineFormatCommand,
  Dt as SetInlineFormatFontFamilyCommand,
  Pt as SetInlineFormatFontSizeCommand,
  jt as SetInlineFormatItalicCommand,
  zt as SetInlineFormatStrikethroughCommand,
  Ct as SetInlineFormatSubscriptCommand,
  Gt as SetInlineFormatSuperscriptCommand,
  Nt as SetInlineFormatTextBackgroundColorCommand,
  wt as SetInlineFormatTextColorCommand,
  Wt as SetInlineFormatUnderlineCommand,
  qo as TEXT_RANGE_LAYER_INDEX,
  _t as TabCommand,
  Mt as TextRange,
  Ns as ToggleCheckListCommand,
  gs as UniverDocsUIPlugin,
  pa as UpdateCommand,
  Xe as VIEWPORT_KEY,
  nf as addCustomDecorationBySelectionFactory,
  AA as addCustomDecorationFactory,
  ko as calcDocRangePositions,
  Mo as convertPositionsToRectRanges,
  of as deleteCustomDecorationFactory,
  rf as docDrawingPositionToTransform,
  ua as genTableSource,
  va as generateParagraphs,
  Mn as getAnchorBounding,
  yA as getCanvasOffsetByEngine,
  ke as getCommandSkeleton,
  zs as getCursorWhenDelete,
  dd as getCustomBlockIdsInSelections,
  md as getCutActionsFromDocRanges,
  cA as getDocObject,
  tf as getDocObjectById,
  Fs as getEmptyTableCell,
  Hs as getEmptyTableRow,
  Bs as getLineBounding,
  yr as getOneTextSelectionRange,
  Qs as getParagraphsInRange,
  mn as getParagraphsInRanges,
  le as getRichTextEditPath,
  ks as getTableColumn,
  sf as hasParagraphInTable,
  Wi as isInSameTableCell,
  SA as isValidRectRange,
  rt as neoGetDocObject,
  af as transformToDocDrawingPosition,
  lA as useKeyboardEvent,
  dA as useResize,
  de as whenDocAndEditorFocused
};
