var Ol = Object.defineProperty;
var bl = (t, e, n) => e in t ? Ol(t, e, { enumerable: !0, configurable: !0, writable: !0, value: n }) : t[e] = n;
var C = (t, e, n) => bl(t, typeof e != "symbol" ? e + "" : e, n);
import { BehaviorSubject as lt, Subject as _t, Observable as sr, filter as Kt, tap as Wi, debounceTime as Sl, map as Da, ReplaySubject as Al, take as Nl, merge as xa, timer as Tl, distinctUntilChanged as Ml, skip as La, of as fr, combineLatest as Dl } from "rxjs";
import { filter as xl, debounceTime as Ll, first as Ul, map as Pl } from "rxjs/operators";
import * as St from "react";
import kl, { useState as _i, useEffect as Ei, useRef as Lr, useMemo as Ua, createContext as Fl, useCallback as $l, useContext as Bl } from "react";
function jl(t, e) {
  for (var n = 0; n < e.length; n++) {
    const r = e[n];
    if (typeof r != "string" && !Array.isArray(r)) {
      for (const s in r)
        if (s !== "default" && !(s in t)) {
          const i = Object.getOwnPropertyDescriptor(r, s);
          i && Object.defineProperty(t, s, i.get ? i : {
            enumerable: !0,
            get: () => r[s]
          });
        }
    }
  }
  return Object.freeze(Object.defineProperty(t, Symbol.toStringTag, { value: "Module" }));
}
function Hl() {
  Wl();
}
const gr = typeof global < "u" ? global : typeof self < "u" ? self : window;
function Wl() {
  typeof gr.requestIdleCallback != "function" && (gr.requestIdleCallback = function(n) {
    const r = Date.now();
    return setTimeout(function() {
      const i = Math.max(0, 50 - (Date.now() - r));
      n({
        didTimeout: i === 0,
        timeRemaining() {
          return i;
        }
      });
    }, 1);
  }), typeof gr.cancelIdleCallback != "function" && (gr.cancelIdleCallback = function(n) {
    clearTimeout(n);
  });
}
var Pa = typeof global == "object" && global && global.Object === Object && global, zl = typeof self == "object" && self && self.Object === Object && self, En = Pa || zl || Function("return this")(), Mn = En.Symbol, ka = Object.prototype, Yl = ka.hasOwnProperty, Vl = ka.toString, Fn = Mn ? Mn.toStringTag : void 0;
function Gl(t) {
  var e = Yl.call(t, Fn), n = t[Fn];
  try {
    t[Fn] = void 0;
    var r = !0;
  } catch {
  }
  var s = Vl.call(t);
  return r && (e ? t[Fn] = n : delete t[Fn]), s;
}
var Kl = Object.prototype, Xl = Kl.toString;
function Jl(t) {
  return Xl.call(t);
}
var Zl = "[object Null]", Ql = "[object Undefined]", zi = Mn ? Mn.toStringTag : void 0;
function ir(t) {
  return t == null ? t === void 0 ? Ql : Zl : zi && zi in Object(t) ? Gl(t) : Jl(t);
}
function Un(t) {
  return t != null && typeof t == "object";
}
var ql = "[object Symbol]";
function os(t) {
  return typeof t == "symbol" || Un(t) && ir(t) == ql;
}
function ec(t, e) {
  for (var n = -1, r = t == null ? 0 : t.length, s = Array(r); ++n < r; )
    s[n] = e(t[n], n, t);
  return s;
}
var Dn = Array.isArray, Yi = Mn ? Mn.prototype : void 0, Vi = Yi ? Yi.toString : void 0;
function Fa(t) {
  if (typeof t == "string")
    return t;
  if (Dn(t))
    return ec(t, Fa) + "";
  if (os(t))
    return Vi ? Vi.call(t) : "";
  var e = t + "";
  return e == "0" && 1 / t == -1 / 0 ? "-0" : e;
}
var tc = /\s/;
function nc(t) {
  for (var e = t.length; e-- && tc.test(t.charAt(e)); )
    ;
  return e;
}
var rc = /^\s+/;
function sc(t) {
  return t && t.slice(0, nc(t) + 1).replace(rc, "");
}
function yt(t) {
  var e = typeof t;
  return t != null && (e == "object" || e == "function");
}
var Gi = NaN, ic = /^[-+]0x[0-9a-f]+$/i, oc = /^0b[01]+$/i, ac = /^0o[0-7]+$/i, uc = parseInt;
function Ki(t) {
  if (typeof t == "number")
    return t;
  if (os(t))
    return Gi;
  if (yt(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = yt(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = sc(t);
  var n = oc.test(t);
  return n || ac.test(t) ? uc(t.slice(2), n ? 2 : 8) : ic.test(t) ? Gi : +t;
}
function $a(t) {
  return t;
}
var lc = "[object AsyncFunction]", cc = "[object Function]", hc = "[object GeneratorFunction]", dc = "[object Proxy]";
function Ci(t) {
  if (!yt(t))
    return !1;
  var e = ir(t);
  return e == cc || e == hc || e == lc || e == dc;
}
var Cs = En["__core-js_shared__"], Xi = function() {
  var t = /[^.]+$/.exec(Cs && Cs.keys && Cs.keys.IE_PROTO || "");
  return t ? "Symbol(src)_1." + t : "";
}();
function fc(t) {
  return !!Xi && Xi in t;
}
var gc = Function.prototype, pc = gc.toString;
function mc(t) {
  if (t != null) {
    try {
      return pc.call(t);
    } catch {
    }
    try {
      return t + "";
    } catch {
    }
  }
  return "";
}
var _c = /[\\^$.*+?()[\]{}|]/g, Ec = /^\[object .+?Constructor\]$/, Cc = Function.prototype, Rc = Object.prototype, Ic = Cc.toString, vc = Rc.hasOwnProperty, yc = RegExp(
  "^" + Ic.call(vc).replace(_c, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"
);
function wc(t) {
  if (!yt(t) || fc(t))
    return !1;
  var e = Ci(t) ? yc : Ec;
  return e.test(mc(t));
}
function Oc(t, e) {
  return t == null ? void 0 : t[e];
}
function Ri(t, e) {
  var n = Oc(t, e);
  return wc(n) ? n : void 0;
}
var Ji = Object.create, bc = /* @__PURE__ */ function() {
  function t() {
  }
  return function(e) {
    if (!yt(e))
      return {};
    if (Ji)
      return Ji(e);
    t.prototype = e;
    var n = new t();
    return t.prototype = void 0, n;
  };
}();
function Sc(t, e, n) {
  switch (n.length) {
    case 0:
      return t.call(e);
    case 1:
      return t.call(e, n[0]);
    case 2:
      return t.call(e, n[0], n[1]);
    case 3:
      return t.call(e, n[0], n[1], n[2]);
  }
  return t.apply(e, n);
}
function Ac(t, e) {
  var n = -1, r = t.length;
  for (e || (e = Array(r)); ++n < r; )
    e[n] = t[n];
  return e;
}
var Nc = 800, Tc = 16, Mc = Date.now;
function Dc(t) {
  var e = 0, n = 0;
  return function() {
    var r = Mc(), s = Tc - (r - n);
    if (n = r, s > 0) {
      if (++e >= Nc)
        return arguments[0];
    } else
      e = 0;
    return t.apply(void 0, arguments);
  };
}
function xc(t) {
  return function() {
    return t;
  };
}
var Kr = function() {
  try {
    var t = Ri(Object, "defineProperty");
    return t({}, "", {}), t;
  } catch {
  }
}(), Lc = Kr ? function(t, e) {
  return Kr(t, "toString", {
    configurable: !0,
    enumerable: !1,
    value: xc(e),
    writable: !0
  });
} : $a, Uc = Dc(Lc), Pc = 9007199254740991, kc = /^(?:0|[1-9]\d*)$/;
function Ii(t, e) {
  var n = typeof t;
  return e = e == null ? Pc : e, !!e && (n == "number" || n != "symbol" && kc.test(t)) && t > -1 && t % 1 == 0 && t < e;
}
function vi(t, e, n) {
  e == "__proto__" && Kr ? Kr(t, e, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : t[e] = n;
}
function as(t, e) {
  return t === e || t !== t && e !== e;
}
var Fc = Object.prototype, $c = Fc.hasOwnProperty;
function Ba(t, e, n) {
  var r = t[e];
  (!($c.call(t, e) && as(r, n)) || n === void 0 && !(e in t)) && vi(t, e, n);
}
function Bc(t, e, n, r) {
  var s = !n;
  n || (n = {});
  for (var i = -1, o = e.length; ++i < o; ) {
    var a = e[i], u = void 0;
    u === void 0 && (u = t[a]), s ? vi(n, a, u) : Ba(n, a, u);
  }
  return n;
}
var Zi = Math.max;
function jc(t, e, n) {
  return e = Zi(e === void 0 ? t.length - 1 : e, 0), function() {
    for (var r = arguments, s = -1, i = Zi(r.length - e, 0), o = Array(i); ++s < i; )
      o[s] = r[e + s];
    s = -1;
    for (var a = Array(e + 1); ++s < e; )
      a[s] = r[s];
    return a[e] = n(o), Sc(t, this, a);
  };
}
function Hc(t, e) {
  return Uc(jc(t, e, $a), t + "");
}
var Wc = 9007199254740991;
function ja(t) {
  return typeof t == "number" && t > -1 && t % 1 == 0 && t <= Wc;
}
function yi(t) {
  return t != null && ja(t.length) && !Ci(t);
}
function zc(t, e, n) {
  if (!yt(n))
    return !1;
  var r = typeof e;
  return (r == "number" ? yi(n) && Ii(e, n.length) : r == "string" && e in n) ? as(n[e], t) : !1;
}
function Ha(t) {
  return Hc(function(e, n) {
    var r = -1, s = n.length, i = s > 1 ? n[s - 1] : void 0, o = s > 2 ? n[2] : void 0;
    for (i = t.length > 3 && typeof i == "function" ? (s--, i) : void 0, o && zc(n[0], n[1], o) && (i = s < 3 ? void 0 : i, s = 1), e = Object(e); ++r < s; ) {
      var a = n[r];
      a && t(e, a, r, i);
    }
    return e;
  });
}
var Yc = Object.prototype;
function Wa(t) {
  var e = t && t.constructor, n = typeof e == "function" && e.prototype || Yc;
  return t === n;
}
function Vc(t, e) {
  for (var n = -1, r = Array(t); ++n < t; )
    r[n] = e(n);
  return r;
}
var Gc = "[object Arguments]";
function Qi(t) {
  return Un(t) && ir(t) == Gc;
}
var za = Object.prototype, Kc = za.hasOwnProperty, Xc = za.propertyIsEnumerable, Fs = Qi(/* @__PURE__ */ function() {
  return arguments;
}()) ? Qi : function(t) {
  return Un(t) && Kc.call(t, "callee") && !Xc.call(t, "callee");
};
function Jc() {
  return !1;
}
var Ya = typeof exports == "object" && exports && !exports.nodeType && exports, qi = Ya && typeof module == "object" && module && !module.nodeType && module, Zc = qi && qi.exports === Ya, eo = Zc ? En.Buffer : void 0, Qc = eo ? eo.isBuffer : void 0, Va = Qc || Jc, qc = "[object Arguments]", eh = "[object Array]", th = "[object Boolean]", nh = "[object Date]", rh = "[object Error]", sh = "[object Function]", ih = "[object Map]", oh = "[object Number]", ah = "[object Object]", uh = "[object RegExp]", lh = "[object Set]", ch = "[object String]", hh = "[object WeakMap]", dh = "[object ArrayBuffer]", fh = "[object DataView]", gh = "[object Float32Array]", ph = "[object Float64Array]", mh = "[object Int8Array]", _h = "[object Int16Array]", Eh = "[object Int32Array]", Ch = "[object Uint8Array]", Rh = "[object Uint8ClampedArray]", Ih = "[object Uint16Array]", vh = "[object Uint32Array]", Qe = {};
Qe[gh] = Qe[ph] = Qe[mh] = Qe[_h] = Qe[Eh] = Qe[Ch] = Qe[Rh] = Qe[Ih] = Qe[vh] = !0;
Qe[qc] = Qe[eh] = Qe[dh] = Qe[th] = Qe[fh] = Qe[nh] = Qe[rh] = Qe[sh] = Qe[ih] = Qe[oh] = Qe[ah] = Qe[uh] = Qe[lh] = Qe[ch] = Qe[hh] = !1;
function yh(t) {
  return Un(t) && ja(t.length) && !!Qe[ir(t)];
}
function wh(t) {
  return function(e) {
    return t(e);
  };
}
var Ga = typeof exports == "object" && exports && !exports.nodeType && exports, Jn = Ga && typeof module == "object" && module && !module.nodeType && module, Oh = Jn && Jn.exports === Ga, Rs = Oh && Pa.process, to = function() {
  try {
    var t = Jn && Jn.require && Jn.require("util").types;
    return t || Rs && Rs.binding && Rs.binding("util");
  } catch {
  }
}(), no = to && to.isTypedArray, Ka = no ? wh(no) : yh;
function bh(t, e) {
  var n = Dn(t), r = !n && Fs(t), s = !n && !r && Va(t), i = !n && !r && !s && Ka(t), o = n || r || s || i, a = o ? Vc(t.length, String) : [], u = a.length;
  for (var c in t)
    o && // Safari 9 has enumerable `arguments.length` in strict mode.
    (c == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    s && (c == "offset" || c == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    i && (c == "buffer" || c == "byteLength" || c == "byteOffset") || // Skip index properties.
    Ii(c, u)) || a.push(c);
  return a;
}
function Sh(t, e) {
  return function(n) {
    return t(e(n));
  };
}
function Ah(t) {
  var e = [];
  if (t != null)
    for (var n in Object(t))
      e.push(n);
  return e;
}
var Nh = Object.prototype, Th = Nh.hasOwnProperty;
function Mh(t) {
  if (!yt(t))
    return Ah(t);
  var e = Wa(t), n = [];
  for (var r in t)
    r == "constructor" && (e || !Th.call(t, r)) || n.push(r);
  return n;
}
function Xa(t) {
  return yi(t) ? bh(t) : Mh(t);
}
var Dh = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, xh = /^\w*$/;
function Lh(t, e) {
  if (Dn(t))
    return !1;
  var n = typeof t;
  return n == "number" || n == "symbol" || n == "boolean" || t == null || os(t) ? !0 : xh.test(t) || !Dh.test(t) || e != null && t in Object(e);
}
var qn = Ri(Object, "create");
function Uh() {
  this.__data__ = qn ? qn(null) : {}, this.size = 0;
}
function Ph(t) {
  var e = this.has(t) && delete this.__data__[t];
  return this.size -= e ? 1 : 0, e;
}
var kh = "__lodash_hash_undefined__", Fh = Object.prototype, $h = Fh.hasOwnProperty;
function Bh(t) {
  var e = this.__data__;
  if (qn) {
    var n = e[t];
    return n === kh ? void 0 : n;
  }
  return $h.call(e, t) ? e[t] : void 0;
}
var jh = Object.prototype, Hh = jh.hasOwnProperty;
function Wh(t) {
  var e = this.__data__;
  return qn ? e[t] !== void 0 : Hh.call(e, t);
}
var zh = "__lodash_hash_undefined__";
function Yh(t, e) {
  var n = this.__data__;
  return this.size += this.has(t) ? 0 : 1, n[t] = qn && e === void 0 ? zh : e, this;
}
function pn(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
pn.prototype.clear = Uh;
pn.prototype.delete = Ph;
pn.prototype.get = Bh;
pn.prototype.has = Wh;
pn.prototype.set = Yh;
function Vh() {
  this.__data__ = [], this.size = 0;
}
function us(t, e) {
  for (var n = t.length; n--; )
    if (as(t[n][0], e))
      return n;
  return -1;
}
var Gh = Array.prototype, Kh = Gh.splice;
function Xh(t) {
  var e = this.__data__, n = us(e, t);
  if (n < 0)
    return !1;
  var r = e.length - 1;
  return n == r ? e.pop() : Kh.call(e, n, 1), --this.size, !0;
}
function Jh(t) {
  var e = this.__data__, n = us(e, t);
  return n < 0 ? void 0 : e[n][1];
}
function Zh(t) {
  return us(this.__data__, t) > -1;
}
function Qh(t, e) {
  var n = this.__data__, r = us(n, t);
  return r < 0 ? (++this.size, n.push([t, e])) : n[r][1] = e, this;
}
function Wt(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
Wt.prototype.clear = Vh;
Wt.prototype.delete = Xh;
Wt.prototype.get = Jh;
Wt.prototype.has = Zh;
Wt.prototype.set = Qh;
var Ja = Ri(En, "Map");
function qh() {
  this.size = 0, this.__data__ = {
    hash: new pn(),
    map: new (Ja || Wt)(),
    string: new pn()
  };
}
function ed(t) {
  var e = typeof t;
  return e == "string" || e == "number" || e == "symbol" || e == "boolean" ? t !== "__proto__" : t === null;
}
function ls(t, e) {
  var n = t.__data__;
  return ed(e) ? n[typeof e == "string" ? "string" : "hash"] : n.map;
}
function td(t) {
  var e = ls(this, t).delete(t);
  return this.size -= e ? 1 : 0, e;
}
function nd(t) {
  return ls(this, t).get(t);
}
function rd(t) {
  return ls(this, t).has(t);
}
function sd(t, e) {
  var n = ls(this, t), r = n.size;
  return n.set(t, e), this.size += n.size == r ? 0 : 1, this;
}
function nn(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
nn.prototype.clear = qh;
nn.prototype.delete = td;
nn.prototype.get = nd;
nn.prototype.has = rd;
nn.prototype.set = sd;
var id = "Expected a function";
function wi(t, e) {
  if (typeof t != "function" || e != null && typeof e != "function")
    throw new TypeError(id);
  var n = function() {
    var r = arguments, s = e ? e.apply(this, r) : r[0], i = n.cache;
    if (i.has(s))
      return i.get(s);
    var o = t.apply(this, r);
    return n.cache = i.set(s, o) || i, o;
  };
  return n.cache = new (wi.Cache || nn)(), n;
}
wi.Cache = nn;
var od = 500;
function ad(t) {
  var e = wi(t, function(r) {
    return n.size === od && n.clear(), r;
  }), n = e.cache;
  return e;
}
var ud = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, ld = /\\(\\)?/g, cd = ad(function(t) {
  var e = [];
  return t.charCodeAt(0) === 46 && e.push(""), t.replace(ud, function(n, r, s, i) {
    e.push(s ? i.replace(ld, "$1") : r || n);
  }), e;
});
function hd(t) {
  return t == null ? "" : Fa(t);
}
function Za(t, e) {
  return Dn(t) ? t : Lh(t, e) ? [t] : cd(hd(t));
}
function Qa(t) {
  if (typeof t == "string" || os(t))
    return t;
  var e = t + "";
  return e == "0" && 1 / t == -1 / 0 ? "-0" : e;
}
function dd(t, e) {
  e = Za(e, t);
  for (var n = 0, r = e.length; t != null && n < r; )
    t = t[Qa(e[n++])];
  return n && n == r ? t : void 0;
}
function b0(t, e, n) {
  var r = t == null ? void 0 : dd(t, e);
  return r === void 0 ? n : r;
}
var qa = Sh(Object.getPrototypeOf, Object), fd = "[object Object]", gd = Function.prototype, pd = Object.prototype, eu = gd.toString, md = pd.hasOwnProperty, _d = eu.call(Object);
function Ed(t) {
  if (!Un(t) || ir(t) != fd)
    return !1;
  var e = qa(t);
  if (e === null)
    return !0;
  var n = md.call(e, "constructor") && e.constructor;
  return typeof n == "function" && n instanceof n && eu.call(n) == _d;
}
function Cd() {
  this.__data__ = new Wt(), this.size = 0;
}
function Rd(t) {
  var e = this.__data__, n = e.delete(t);
  return this.size = e.size, n;
}
function Id(t) {
  return this.__data__.get(t);
}
function vd(t) {
  return this.__data__.has(t);
}
var yd = 200;
function wd(t, e) {
  var n = this.__data__;
  if (n instanceof Wt) {
    var r = n.__data__;
    if (!Ja || r.length < yd - 1)
      return r.push([t, e]), this.size = ++n.size, this;
    n = this.__data__ = new nn(r);
  }
  return n.set(t, e), this.size = n.size, this;
}
function Pn(t) {
  var e = this.__data__ = new Wt(t);
  this.size = e.size;
}
Pn.prototype.clear = Cd;
Pn.prototype.delete = Rd;
Pn.prototype.get = Id;
Pn.prototype.has = vd;
Pn.prototype.set = wd;
var tu = typeof exports == "object" && exports && !exports.nodeType && exports, ro = tu && typeof module == "object" && module && !module.nodeType && module, Od = ro && ro.exports === tu, so = Od ? En.Buffer : void 0;
so && so.allocUnsafe;
function bd(t, e) {
  return t.slice();
}
var io = En.Uint8Array;
function Sd(t) {
  var e = new t.constructor(t.byteLength);
  return new io(e).set(new io(t)), e;
}
function Ad(t, e) {
  var n = Sd(t.buffer);
  return new t.constructor(n, t.byteOffset, t.length);
}
function Nd(t) {
  return typeof t.constructor == "function" && !Wa(t) ? bc(qa(t)) : {};
}
function Td(t) {
  return function(e, n, r) {
    for (var s = -1, i = Object(e), o = r(e), a = o.length; a--; ) {
      var u = o[++s];
      if (n(i[u], u, i) === !1)
        break;
    }
    return e;
  };
}
var Md = Td(), Is = function() {
  return En.Date.now();
}, Dd = "Expected a function", xd = Math.max, Ld = Math.min;
function S0(t, e, n) {
  var r, s, i, o, a, u, c = 0, l = !1, h = !1, d = !0;
  if (typeof t != "function")
    throw new TypeError(Dd);
  e = Ki(e) || 0, yt(n) && (l = !!n.leading, h = "maxWait" in n, i = h ? xd(Ki(n.maxWait) || 0, e) : i, d = "trailing" in n ? !!n.trailing : d);
  function f(A) {
    var H = r, Z = s;
    return r = s = void 0, c = A, o = t.apply(Z, H), o;
  }
  function E(A) {
    return c = A, a = setTimeout(U, e), l ? f(A) : o;
  }
  function R(A) {
    var H = A - u, Z = A - c, fe = e - H;
    return h ? Ld(fe, i - Z) : fe;
  }
  function O(A) {
    var H = A - u, Z = A - c;
    return u === void 0 || H >= e || H < 0 || h && Z >= i;
  }
  function U() {
    var A = Is();
    if (O(A))
      return ne(A);
    a = setTimeout(U, R(A));
  }
  function ne(A) {
    return a = void 0, d && r ? f(A) : (r = s = void 0, o);
  }
  function X() {
    a !== void 0 && clearTimeout(a), c = 0, r = u = s = a = void 0;
  }
  function de() {
    return a === void 0 ? o : ne(Is());
  }
  function T() {
    var A = Is(), H = O(A);
    if (r = arguments, s = this, u = A, H) {
      if (a === void 0)
        return E(u);
      if (h)
        return clearTimeout(a), a = setTimeout(U, e), f(u);
    }
    return a === void 0 && (a = setTimeout(U, e)), o;
  }
  return T.cancel = X, T.flush = de, T;
}
function $s(t, e, n) {
  (n !== void 0 && !as(t[e], n) || n === void 0 && !(e in t)) && vi(t, e, n);
}
function Ud(t) {
  return Un(t) && yi(t);
}
function Bs(t, e) {
  if (!(e === "constructor" && typeof t[e] == "function") && e != "__proto__")
    return t[e];
}
function Pd(t) {
  return Bc(t, Xa(t));
}
function kd(t, e, n, r, s, i, o) {
  var a = Bs(t, n), u = Bs(e, n), c = o.get(u);
  if (c) {
    $s(t, n, c);
    return;
  }
  var l = i ? i(a, u, n + "", t, e, o) : void 0, h = l === void 0;
  if (h) {
    var d = Dn(u), f = !d && Va(u), E = !d && !f && Ka(u);
    l = u, d || f || E ? Dn(a) ? l = a : Ud(a) ? l = Ac(a) : f ? (h = !1, l = bd(u)) : E ? (h = !1, l = Ad(u)) : l = [] : Ed(u) || Fs(u) ? (l = a, Fs(a) ? l = Pd(a) : (!yt(a) || Ci(a)) && (l = Nd(u))) : h = !1;
  }
  h && (o.set(u, l), s(l, u, r, i, o), o.delete(u)), $s(t, n, l);
}
function Oi(t, e, n, r, s) {
  t !== e && Md(e, function(i, o) {
    if (s || (s = new Pn()), yt(i))
      kd(t, e, o, n, Oi, r, s);
    else {
      var a = r ? r(Bs(t, o), i, o + "", t, e, s) : void 0;
      a === void 0 && (a = i), $s(t, o, a);
    }
  }, Xa);
}
var A0 = Ha(function(t, e, n, r) {
  Oi(t, e, n, r);
}), nu = Ha(function(t, e, n) {
  Oi(t, e, n);
});
function Fd(t, e, n, r) {
  if (!yt(t))
    return t;
  e = Za(e, t);
  for (var s = -1, i = e.length, o = i - 1, a = t; a != null && ++s < i; ) {
    var u = Qa(e[s]), c = n;
    if (u === "__proto__" || u === "constructor" || u === "prototype")
      return t;
    if (s != o) {
      var l = a[u];
      c = void 0, c === void 0 && (c = yt(l) ? l : Ii(e[s + 1]) ? [] : {});
    }
    Ba(a, u, c), a = a[u];
  }
  return t;
}
function N0(t, e, n) {
  return t == null ? t : Fd(t, e, n);
}
function wt(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var vs, oo;
function $d() {
  if (oo) return vs;
  oo = 1;
  var t = -1, e = 1, n = 0;
  function r(m, j, y, M, b) {
    if (m === j)
      return m ? [[n, m]] : [];
    if (y != null) {
      var w = fe(m, j, y);
      if (w)
        return w;
    }
    var k = a(m, j), $ = m.substring(0, k);
    m = m.substring(k), j = j.substring(k), k = c(m, j);
    var Y = m.substring(m.length - k);
    m = m.substring(0, m.length - k), j = j.substring(0, j.length - k);
    var se = s(m, j);
    return $ && se.unshift([n, $]), Y && se.push([n, Y]), ne(se, b), M && h(se), se;
  }
  function s(m, j) {
    var y;
    if (!m)
      return [[e, j]];
    if (!j)
      return [[t, m]];
    var M = m.length > j.length ? m : j, b = m.length > j.length ? j : m, w = M.indexOf(b);
    if (w !== -1)
      return y = [
        [e, M.substring(0, w)],
        [n, b],
        [e, M.substring(w + b.length)]
      ], m.length > j.length && (y[0][0] = y[2][0] = t), y;
    if (b.length === 1)
      return [
        [t, m],
        [e, j]
      ];
    var k = l(m, j);
    if (k) {
      var $ = k[0], Y = k[1], se = k[2], he = k[3], ge = k[4], Ae = r($, se), be = r(Y, he);
      return Ae.concat([[n, ge]], be);
    }
    return i(m, j);
  }
  function i(m, j) {
    for (var y = m.length, M = j.length, b = Math.ceil((y + M) / 2), w = b, k = 2 * b, $ = new Array(k), Y = new Array(k), se = 0; se < k; se++)
      $[se] = -1, Y[se] = -1;
    $[w + 1] = 0, Y[w + 1] = 0;
    for (var he = y - M, ge = he % 2 !== 0, Ae = 0, be = 0, v = 0, F = 0, V = 0; V < b; V++) {
      for (var K = -V + Ae; K <= V - be; K += 2) {
        var z = w + K, W;
        K === -V || K !== V && $[z - 1] < $[z + 1] ? W = $[z + 1] : W = $[z - 1] + 1;
        for (var ue = W - K; W < y && ue < M && m.charAt(W) === j.charAt(ue); )
          W++, ue++;
        if ($[z] = W, W > y)
          be += 2;
        else if (ue > M)
          Ae += 2;
        else if (ge) {
          var oe = w + he - K;
          if (oe >= 0 && oe < k && Y[oe] !== -1) {
            var B = y - Y[oe];
            if (W >= B)
              return o(m, j, W, ue);
          }
        }
      }
      for (var ee = -V + v; ee <= V - F; ee += 2) {
        var oe = w + ee, B;
        ee === -V || ee !== V && Y[oe - 1] < Y[oe + 1] ? B = Y[oe + 1] : B = Y[oe - 1] + 1;
        for (var ie = B - ee; B < y && ie < M && m.charAt(y - B - 1) === j.charAt(M - ie - 1); )
          B++, ie++;
        if (Y[oe] = B, B > y)
          F += 2;
        else if (ie > M)
          v += 2;
        else if (!ge) {
          var z = w + he - ee;
          if (z >= 0 && z < k && $[z] !== -1) {
            var W = $[z], ue = w + W - z;
            if (B = y - B, W >= B)
              return o(m, j, W, ue);
          }
        }
      }
    }
    return [
      [t, m],
      [e, j]
    ];
  }
  function o(m, j, y, M) {
    var b = m.substring(0, y), w = j.substring(0, M), k = m.substring(y), $ = j.substring(M), Y = r(b, w), se = r(k, $);
    return Y.concat(se);
  }
  function a(m, j) {
    if (!m || !j || m.charAt(0) !== j.charAt(0))
      return 0;
    for (var y = 0, M = Math.min(m.length, j.length), b = M, w = 0; y < b; )
      m.substring(w, b) == j.substring(w, b) ? (y = b, w = y) : M = b, b = Math.floor((M - y) / 2 + y);
    return X(m.charCodeAt(b - 1)) && b--, b;
  }
  function u(m, j) {
    var y = m.length, M = j.length;
    if (y == 0 || M == 0)
      return 0;
    y > M ? m = m.substring(y - M) : y < M && (j = j.substring(0, y));
    var b = Math.min(y, M);
    if (m == j)
      return b;
    for (var w = 0, k = 1; ; ) {
      var $ = m.substring(b - k), Y = j.indexOf($);
      if (Y == -1)
        return w;
      k += Y, (Y == 0 || m.substring(b - k) == j.substring(0, k)) && (w = k, k++);
    }
  }
  function c(m, j) {
    if (!m || !j || m.slice(-1) !== j.slice(-1))
      return 0;
    for (var y = 0, M = Math.min(m.length, j.length), b = M, w = 0; y < b; )
      m.substring(m.length - b, m.length - w) == j.substring(j.length - b, j.length - w) ? (y = b, w = y) : M = b, b = Math.floor((M - y) / 2 + y);
    return de(m.charCodeAt(m.length - b)) && b--, b;
  }
  function l(m, j) {
    var y = m.length > j.length ? m : j, M = m.length > j.length ? j : m;
    if (y.length < 4 || M.length * 2 < y.length)
      return null;
    function b(be, v, F) {
      for (var V = be.substring(F, F + Math.floor(be.length / 4)), K = -1, z = "", W, ue, oe, B; (K = v.indexOf(V, K + 1)) !== -1; ) {
        var ee = a(
          be.substring(F),
          v.substring(K)
        ), ie = c(
          be.substring(0, F),
          v.substring(0, K)
        );
        z.length < ie + ee && (z = v.substring(K - ie, K) + v.substring(K, K + ee), W = be.substring(0, F - ie), ue = be.substring(F + ee), oe = v.substring(0, K - ie), B = v.substring(K + ee));
      }
      return z.length * 2 >= be.length ? [
        W,
        ue,
        oe,
        B,
        z
      ] : null;
    }
    var w = b(
      y,
      M,
      Math.ceil(y.length / 4)
    ), k = b(
      y,
      M,
      Math.ceil(y.length / 2)
    ), $;
    if (!w && !k)
      return null;
    k ? w ? $ = w[4].length > k[4].length ? w : k : $ = k : $ = w;
    var Y, se, he, ge;
    m.length > j.length ? (Y = $[0], se = $[1], he = $[2], ge = $[3]) : (he = $[0], ge = $[1], Y = $[2], se = $[3]);
    var Ae = $[4];
    return [Y, se, he, ge, Ae];
  }
  function h(m) {
    for (var j = !1, y = [], M = 0, b = null, w = 0, k = 0, $ = 0, Y = 0, se = 0; w < m.length; )
      m[w][0] == n ? (y[M++] = w, k = Y, $ = se, Y = 0, se = 0, b = m[w][1]) : (m[w][0] == e ? Y += m[w][1].length : se += m[w][1].length, b && b.length <= Math.max(k, $) && b.length <= Math.max(Y, se) && (m.splice(y[M - 1], 0, [
        t,
        b
      ]), m[y[M - 1] + 1][0] = e, M--, M--, w = M > 0 ? y[M - 1] : -1, k = 0, $ = 0, Y = 0, se = 0, b = null, j = !0)), w++;
    for (j && ne(m), U(m), w = 1; w < m.length; ) {
      if (m[w - 1][0] == t && m[w][0] == e) {
        var he = m[w - 1][1], ge = m[w][1], Ae = u(he, ge), be = u(ge, he);
        Ae >= be ? (Ae >= he.length / 2 || Ae >= ge.length / 2) && (m.splice(w, 0, [
          n,
          ge.substring(0, Ae)
        ]), m[w - 1][1] = he.substring(
          0,
          he.length - Ae
        ), m[w + 1][1] = ge.substring(Ae), w++) : (be >= he.length / 2 || be >= ge.length / 2) && (m.splice(w, 0, [
          n,
          he.substring(0, be)
        ]), m[w - 1][0] = e, m[w - 1][1] = ge.substring(
          0,
          ge.length - be
        ), m[w + 1][0] = t, m[w + 1][1] = he.substring(be), w++), w++;
      }
      w++;
    }
  }
  var d = /[^a-zA-Z0-9]/, f = /\s/, E = /[\r\n]/, R = /\n\r?\n$/, O = /^\r?\n\r?\n/;
  function U(m) {
    function j(be, v) {
      if (!be || !v)
        return 6;
      var F = be.charAt(be.length - 1), V = v.charAt(0), K = F.match(d), z = V.match(d), W = K && F.match(f), ue = z && V.match(f), oe = W && F.match(E), B = ue && V.match(E), ee = oe && be.match(R), ie = B && v.match(O);
      return ee || ie ? 5 : oe || B ? 4 : K && !W && ue ? 3 : W || ue ? 2 : K || z ? 1 : 0;
    }
    for (var y = 1; y < m.length - 1; ) {
      if (m[y - 1][0] == n && m[y + 1][0] == n) {
        var M = m[y - 1][1], b = m[y][1], w = m[y + 1][1], k = c(M, b);
        if (k) {
          var $ = b.substring(b.length - k);
          M = M.substring(0, M.length - k), b = $ + b.substring(0, b.length - k), w = $ + w;
        }
        for (var Y = M, se = b, he = w, ge = j(M, b) + j(b, w); b.charAt(0) === w.charAt(0); ) {
          M += b.charAt(0), b = b.substring(1) + w.charAt(0), w = w.substring(1);
          var Ae = j(M, b) + j(b, w);
          Ae >= ge && (ge = Ae, Y = M, se = b, he = w);
        }
        m[y - 1][1] != Y && (Y ? m[y - 1][1] = Y : (m.splice(y - 1, 1), y--), m[y][1] = se, he ? m[y + 1][1] = he : (m.splice(y + 1, 1), y--));
      }
      y++;
    }
  }
  function ne(m, j) {
    m.push([n, ""]);
    for (var y = 0, M = 0, b = 0, w = "", k = "", $; y < m.length; ) {
      if (y < m.length - 1 && !m[y][1]) {
        m.splice(y, 1);
        continue;
      }
      switch (m[y][0]) {
        case e:
          b++, k += m[y][1], y++;
          break;
        case t:
          M++, w += m[y][1], y++;
          break;
        case n:
          var Y = y - b - M - 1;
          if (j) {
            if (Y >= 0 && A(m[Y][1])) {
              var se = m[Y][1].slice(-1);
              if (m[Y][1] = m[Y][1].slice(
                0,
                -1
              ), w = se + w, k = se + k, !m[Y][1]) {
                m.splice(Y, 1), y--;
                var he = Y - 1;
                m[he] && m[he][0] === e && (b++, k = m[he][1] + k, he--), m[he] && m[he][0] === t && (M++, w = m[he][1] + w, he--), Y = he;
              }
            }
            if (T(m[y][1])) {
              var se = m[y][1].charAt(0);
              m[y][1] = m[y][1].slice(1), w += se, k += se;
            }
          }
          if (y < m.length - 1 && !m[y][1]) {
            m.splice(y, 1);
            break;
          }
          if (w.length > 0 || k.length > 0) {
            w.length > 0 && k.length > 0 && ($ = a(k, w), $ !== 0 && (Y >= 0 ? m[Y][1] += k.substring(
              0,
              $
            ) : (m.splice(0, 0, [
              n,
              k.substring(0, $)
            ]), y++), k = k.substring($), w = w.substring($)), $ = c(k, w), $ !== 0 && (m[y][1] = k.substring(k.length - $) + m[y][1], k = k.substring(
              0,
              k.length - $
            ), w = w.substring(
              0,
              w.length - $
            )));
            var ge = b + M;
            w.length === 0 && k.length === 0 ? (m.splice(y - ge, ge), y = y - ge) : w.length === 0 ? (m.splice(y - ge, ge, [e, k]), y = y - ge + 1) : k.length === 0 ? (m.splice(y - ge, ge, [t, w]), y = y - ge + 1) : (m.splice(
              y - ge,
              ge,
              [t, w],
              [e, k]
            ), y = y - ge + 2);
          }
          y !== 0 && m[y - 1][0] === n ? (m[y - 1][1] += m[y][1], m.splice(y, 1)) : y++, b = 0, M = 0, w = "", k = "";
          break;
      }
    }
    m[m.length - 1][1] === "" && m.pop();
    var Ae = !1;
    for (y = 1; y < m.length - 1; )
      m[y - 1][0] === n && m[y + 1][0] === n && (m[y][1].substring(
        m[y][1].length - m[y - 1][1].length
      ) === m[y - 1][1] ? (m[y][1] = m[y - 1][1] + m[y][1].substring(
        0,
        m[y][1].length - m[y - 1][1].length
      ), m[y + 1][1] = m[y - 1][1] + m[y + 1][1], m.splice(y - 1, 1), Ae = !0) : m[y][1].substring(0, m[y + 1][1].length) == m[y + 1][1] && (m[y - 1][1] += m[y + 1][1], m[y][1] = m[y][1].substring(m[y + 1][1].length) + m[y + 1][1], m.splice(y + 1, 1), Ae = !0)), y++;
    Ae && ne(m, j);
  }
  function X(m) {
    return m >= 55296 && m <= 56319;
  }
  function de(m) {
    return m >= 56320 && m <= 57343;
  }
  function T(m) {
    return de(m.charCodeAt(0));
  }
  function A(m) {
    return X(m.charCodeAt(m.length - 1));
  }
  function H(m) {
    for (var j = [], y = 0; y < m.length; y++)
      m[y][1].length > 0 && j.push(m[y]);
    return j;
  }
  function Z(m, j, y, M) {
    return A(m) || T(M) ? null : H([
      [n, m],
      [t, j],
      [e, y],
      [n, M]
    ]);
  }
  function fe(m, j, y) {
    var M = typeof y == "number" ? { index: y, length: 0 } : y.oldRange, b = typeof y == "number" ? null : y.newRange, w = m.length, k = j.length;
    if (M.length === 0 && (b === null || b.length === 0)) {
      var $ = M.index, Y = m.slice(0, $), se = m.slice($), he = b ? b.index : null;
      e: {
        var ge = $ + k - w;
        if (he !== null && he !== ge || ge < 0 || ge > k)
          break e;
        var Ae = j.slice(0, ge), be = j.slice(ge);
        if (be !== se)
          break e;
        var v = Math.min($, ge), F = Y.slice(0, v), V = Ae.slice(0, v);
        if (F !== V)
          break e;
        var K = Y.slice(v), z = Ae.slice(v);
        return Z(F, K, z, se);
      }
      e: {
        if (he !== null && he !== $)
          break e;
        var W = $, Ae = j.slice(0, W), be = j.slice(W);
        if (Ae !== Y)
          break e;
        var ue = Math.min(w - W, k - W), oe = se.slice(se.length - ue), B = be.slice(be.length - ue);
        if (oe !== B)
          break e;
        var K = se.slice(0, se.length - ue), z = be.slice(0, be.length - ue);
        return Z(Y, K, z, oe);
      }
    }
    if (M.length > 0 && b && b.length === 0)
      e: {
        var F = m.slice(0, M.index), oe = m.slice(M.index + M.length), v = F.length, ue = oe.length;
        if (k < v + ue)
          break e;
        var V = j.slice(0, v), B = j.slice(k - ue);
        if (F !== V || oe !== B)
          break e;
        var K = m.slice(v, w - ue), z = j.slice(v, k - ue);
        return Z(F, K, z, oe);
      }
    return null;
  }
  function ae(m, j, y, M) {
    return r(m, j, y, M, !0);
  }
  return ae.INSERT = e, ae.DELETE = t, ae.EQUAL = n, vs = ae, vs;
}
var Bd = $d();
const ru = /* @__PURE__ */ wt(Bd);
function cs(t, e) {
  const n = t.indexOf(e);
  return n > -1 ? (t.splice(n, 1), !0) : !1;
}
function T0(t) {
  const e = /* @__PURE__ */ new Set(), n = [];
  for (const r of t)
    e.has(r) || (e.add(r), n.push(r));
  return n;
}
function jd(t, e) {
  for (let n = t.length - 1; n > -1; n--) {
    const r = t[n];
    if (e(r, n))
      return r;
  }
  return null;
}
function M0(t, e) {
  if (t.length === 0)
    return t;
  const n = e % t.length;
  return t.slice(n).concat(t.slice(0, n));
}
function D0(t, e) {
  const n = /* @__PURE__ */ new Map();
  return t.forEach((r) => {
    const s = e(r);
    let i = n.get(s);
    n.has(s) || (i = [], n.set(s, i)), i.push(r);
  }), n;
}
function x0(t) {
  return Array.isArray(t) ? t : [t];
}
function L0(t) {
  return ["true", "false"].includes(t.toLowerCase());
}
const or = "__INTERNAL_EDITOR__", su = `${or}DOCS_NORMAL`, iu = `${or}DOCS_FORMULA_BAR`, Hd = `${or}ZEN_EDITOR`, Wd = `\r
`, U0 = "isRowStylePrecedeColumnStyle", P0 = Symbol("AUTO_HEIGHT_FOR_MERGED_CELLS");
function k0(t) {
  return `${or}${t}`;
}
function zd(t) {
  return t.startsWith(or);
}
var bi = Symbol("$$IDENTIFIER_DECORATOR");
function Yd(t) {
  return t && t[bi] === !0;
}
function ou(t) {
  return typeof t == "function";
}
function ao(t) {
  return !!(t && typeof t.useClass < "u");
}
function uo(t) {
  return !!(t && typeof t.useFactory < "u");
}
function lo(t) {
  return !!(t && typeof t.useValue < "u");
}
function Vd(t) {
  return !!(t && typeof t.useExisting < "u");
}
function co(t) {
  return !!(t && typeof t.useAsync < "u");
}
var au = Symbol("AsyncHook");
function ys(t) {
  return !!(t && t.__symbol === au);
}
function Et(t) {
  return typeof t > "u" ? "undefined" : ou(t) && !t[bi] ? t.name : t.toString();
}
var Gd = /* @__PURE__ */ function() {
  var t = function(e, n) {
    return t = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(r, s) {
      r.__proto__ = s;
    } || function(r, s) {
      for (var i in s) Object.prototype.hasOwnProperty.call(s, i) && (r[i] = s[i]);
    }, t(e, n);
  };
  return function(e, n) {
    if (typeof n != "function" && n !== null)
      throw new TypeError("Class extends value " + String(n) + " is not a constructor or null");
    t(e, n);
    function r() {
      this.constructor = e;
    }
    e.prototype = n === null ? Object.create(n) : (r.prototype = n.prototype, new r());
  };
}(), at = (
  /** @class */
  function(t) {
    Gd(e, t);
    function e(n) {
      return t.call(this, "[redi]: ".concat(n)) || this;
    }
    return e;
  }(Error)
), Ge;
(function(t) {
  t.MANY = "many", t.OPTIONAL = "optional", t.REQUIRED = "required";
})(Ge || (Ge = {}));
var $t;
(function(t) {
  t.SELF = "self", t.SKIP_SELF = "skipSelf";
})($t || ($t = {}));
var uu = /* @__PURE__ */ function() {
  var t = function(e, n) {
    return t = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(r, s) {
      r.__proto__ = s;
    } || function(r, s) {
      for (var i in s) Object.prototype.hasOwnProperty.call(s, i) && (r[i] = s[i]);
    }, t(e, n);
  };
  return function(e, n) {
    if (typeof n != "function" && n !== null)
      throw new TypeError("Class extends value " + String(n) + " is not a constructor or null");
    t(e, n);
    function r() {
      this.constructor = e;
    }
    e.prototype = n === null ? Object.create(n) : (r.prototype = n.prototype, new r());
  };
}(), ho = Symbol("$$TARGET"), js = Symbol("$$DEPENDENCIES"), Kd = (
  /** @class */
  function(t) {
    uu(e, t);
    function e(n, r) {
      var s = "Could not find dependency registered on the ".concat(n, ' (indexed) parameter of the constructor of "').concat(Et(r), '".');
      return t.call(this, s) || this;
    }
    return e;
  }(at)
), lu = (
  /** @class */
  function(t) {
    uu(e, t);
    function e(n, r) {
      var s = 'It seems that you register "undefined" as dependency on the '.concat(r + 1, ' parameter of "').concat(Et(n), '". Please make sure that there is not cyclic dependency among your TypeScript files, or consider using "forwardRef". For more info please visit our website https://redi.wendell.fun/docs/debug#could-not-find-dependency-registered-on');
      return t.call(this, s) || this;
    }
    return e;
  }(at)
);
function cu(t) {
  var e = t;
  return e[js] || [];
}
function Si(t, e) {
  var n = cu(t), r = n.find(function(s) {
    return s.paramIndex === e;
  });
  if (!r)
    throw new Kd(e, t);
  return r;
}
function Ai(t, e, n, r, s) {
  r === void 0 && (r = Ge.REQUIRED);
  var i = {
    paramIndex: n,
    identifier: e,
    quantity: r,
    lookUp: s,
    withNew: !1
  };
  if (typeof e > "u")
    throw new lu(t, n);
  var o = t;
  o[ho] === o ? o[js].push(i) : (o[js] = [i], o[ho] = o);
}
var fo = /* @__PURE__ */ new Set();
function Ct(t) {
  if (fo.has(t))
    throw new at('Identifier "'.concat(t, '" already exists.'));
  fo.add(t);
  var e = function(n, r, s) {
    Ai(n, e, s);
  };
  return e.toString = function() {
    return t;
  }, e[bi] = !0, e;
}
function Xd(t, e, n) {
  var r = Si(t, e);
  r.lookUp = n;
}
function hu(t) {
  return function e() {
    return this instanceof e ? this : function(n, r, s) {
      Xd(n, s, t);
    };
  };
}
var Jd = hu($t.SKIP_SELF), Zd = hu($t.SELF), Qd = /* @__PURE__ */ function() {
  var t = function(e, n) {
    return t = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(r, s) {
      r.__proto__ = s;
    } || function(r, s) {
      for (var i in s) Object.prototype.hasOwnProperty.call(s, i) && (r[i] = s[i]);
    }, t(e, n);
  };
  return function(e, n) {
    if (typeof n != "function" && n !== null)
      throw new TypeError("Class extends value " + String(n) + " is not a constructor or null");
    t(e, n);
    function r() {
      this.constructor = e;
    }
    e.prototype = n === null ? Object.create(n) : (r.prototype = n.prototype, new r());
  };
}(), Hs = (
  /** @class */
  function(t) {
    Qd(e, t);
    function e(n, r, s) {
      var i = this, o = 'Expect "'.concat(r, '" dependency items for id "').concat(Et(n), '" but get ').concat(s, ".");
      return s === 0 && (o += " Did you forget to register it?"), s > 1 && (o += " You register it more than once."), i = t.call(this, o) || this, i.quantity = r, i.actual = s, i;
    }
    return e;
  }(at)
);
function Ni(t, e, n) {
  if (e === Ge.OPTIONAL && n > 1 || e === Ge.REQUIRED && n !== 1)
    throw new Hs(t, e, n);
}
function qd(t, e) {
  return t === Ge.MANY ? e : e[0];
}
function ef(t, e, n) {
  var r = Si(t, e);
  r.quantity = n;
}
function Ti(t) {
  return function e(n) {
    return this instanceof e ? this : function(r, s, i) {
      if (n)
        Ai(r, n, i, t);
      else {
        if (t === Ge.REQUIRED)
          throw new lu(r, i);
        ef(r, i, t);
      }
    };
  };
}
var tf = Ti(Ge.MANY), nf = Ti(Ge.OPTIONAL), ot = Ti(Ge.REQUIRED);
function rf(t, e, n) {
  var r = Si(t, e);
  r.withNew = n;
}
function sf(t) {
  return function e() {
    return this instanceof e ? this : function(n, r, s) {
      rf(n, s, t);
    };
  };
}
var of = sf(!0);
function du(t, e) {
  return e === void 0 && (e = 0), t ? t.map(function(n, r) {
    if (r += e, !Array.isArray(n))
      return {
        paramIndex: r,
        identifier: n,
        quantity: Ge.REQUIRED,
        withNew: !1
      };
    var s = n.slice(0, n.length - 1), i = n[n.length - 1], o, a = Ge.REQUIRED, u = !1;
    return s.forEach(function(c) {
      if (c instanceof Zd)
        o = $t.SELF;
      else if (c instanceof Jd)
        o = $t.SKIP_SELF;
      else if (c instanceof nf)
        a = Ge.OPTIONAL;
      else if (c instanceof tf)
        a = Ge.MANY;
      else if (c instanceof of)
        u = !0;
      else
        throw new at("unknown dep modifier ".concat(c, "."));
    }), {
      paramIndex: r,
      identifier: i,
      quantity: a,
      lookUp: o,
      withNew: u
    };
  }) : [];
}
function F0(t, e, n) {
  n === void 0 && (n = 0);
  var r = du(e, n);
  r.forEach(function(s) {
    Ai(t, s.identifier, s.paramIndex, s.quantity, s.lookUp);
  });
}
function $0(t) {
  return {
    unwrap: t
  };
}
function af(t) {
  return !!t && typeof t.unwrap == "function";
}
function uf(t) {
  return af(t) ? t.unwrap() : t;
}
function go(t) {
  return !!t && typeof t.dispose == "function";
}
var fu = /* @__PURE__ */ function() {
  var t = function(e, n) {
    return t = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(r, s) {
      r.__proto__ = s;
    } || function(r, s) {
      for (var i in s) Object.prototype.hasOwnProperty.call(s, i) && (r[i] = s[i]);
    }, t(e, n);
  };
  return function(e, n) {
    if (typeof n != "function" && n !== null)
      throw new TypeError("Class extends value " + String(n) + " is not a constructor or null");
    t(e, n);
    function r() {
      this.constructor = e;
    }
    e.prototype = n === null ? Object.create(n) : (r.prototype = n.prototype, new r());
  };
}();
function lf(t) {
  return t.length === 1;
}
var hs = [];
function po(t) {
  hs.push(t);
}
function mo() {
  hs.pop();
}
function cf() {
  hs.length = 0;
}
var _o = (
  /** @class */
  function(t) {
    fu(e, t);
    function e(n, r, s) {
      var i = 'Cannot find "'.concat(Et(r), '" registered by any injector. It is the ').concat(s, 'th param of "').concat(Yd(n) ? Et(n) : n.name, '".');
      return t.call(this, i) || this;
    }
    return e;
  }(at)
), Ur = (
  /** @class */
  function(t) {
    fu(e, t);
    function e(n) {
      var r = this, s = 'Cannot find "'.concat(Et(n), '" registered by any injector. The stack of dependencies is: "').concat(hs.map(function(i) {
        return Et(i);
      }).join(" -> "), '".');
      return r = t.call(this, s) || this, cf(), r;
    }
    return e;
  }(at)
), hf = (
  /** @class */
  function() {
    function t(e) {
      var n = this;
      this.dependencyMap = /* @__PURE__ */ new Map(), this.normalizeDependencies(e).map(function(r) {
        return n.add(r[0], r[1]);
      });
    }
    return t.prototype.add = function(e, n) {
      typeof n > "u" && (n = { useClass: e, lazy: !1 });
      var r = this.dependencyMap.get(e);
      typeof r > "u" && (r = [], this.dependencyMap.set(e, r)), r.push(n);
    }, t.prototype.delete = function(e) {
      this.dependencyMap.delete(e);
    }, t.prototype.get = function(e, n) {
      n === void 0 && (n = Ge.REQUIRED);
      var r = this.dependencyMap.get(e);
      return Ni(e, n, r.length), qd(n, r);
    }, t.prototype.has = function(e) {
      return this.dependencyMap.has(e);
    }, t.prototype.append = function(e) {
      var n = this;
      this.normalizeDependencies(e).forEach(function(r) {
        return n.add(r[0], r[1]);
      });
    }, t.prototype.dispose = function() {
      this.dependencyMap.clear();
    }, t.prototype.normalizeDependencies = function(e) {
      return e.map(function(n) {
        var r = n[0], s;
        return lf(n) ? s = {
          useClass: n[0],
          lazy: !1
        } : s = n[1], [r, s];
      });
    }, t;
  }()
), df = (
  /** @class */
  function() {
    function t() {
      this.resolvedDependencies = /* @__PURE__ */ new Map();
    }
    return t.prototype.add = function(e, n) {
      var r = this.resolvedDependencies.get(e);
      typeof r > "u" && (r = [], this.resolvedDependencies.set(e, r)), r.push(n);
    }, t.prototype.has = function(e) {
      return this.resolvedDependencies.has(e);
    }, t.prototype.delete = function(e) {
      if (this.resolvedDependencies.has(e)) {
        var n = this.resolvedDependencies.get(e);
        n.forEach(function(r) {
          return go(r) ? r.dispose() : void 0;
        }), this.resolvedDependencies.delete(e);
      }
    }, t.prototype.get = function(e, n) {
      n === void 0 && (n = Ge.REQUIRED);
      var r = this.resolvedDependencies.get(e);
      if (!r)
        throw new Ur(e);
      return Ni(e, n, r.length), n === Ge.MANY ? r : r[0];
    }, t.prototype.dispose = function() {
      Array.from(this.resolvedDependencies.values()).forEach(function(e) {
        e.forEach(function(n) {
          return go(n) ? n.dispose() : void 0;
        });
      }), this.resolvedDependencies.clear();
    }, t;
  }()
), Ws;
(function() {
  if (typeof requestIdleCallback < "u" && typeof cancelIdleCallback < "u")
    Ws = function(e, n) {
      var r = requestIdleCallback(e, typeof n == "number" ? { timeout: n } : void 0), s = !1;
      return function() {
        s || (s = !0, cancelIdleCallback(r));
      };
    };
  else {
    var t = Object.freeze({
      didTimeout: !0,
      timeRemaining: function() {
        return 15;
      }
    });
    Ws = function(e) {
      var n = setTimeout(function() {
        return e(t);
      }), r = !1;
      return function() {
        r || (r = !0, clearTimeout(n));
      };
    };
  }
})();
var ff = (
  /** @class */
  function() {
    function t(e) {
      var n = this;
      this.didRun = !1, this.selfExecutor = function() {
        try {
          n.value = e();
        } catch (r) {
          n.error = r;
        } finally {
          n.didRun = !0;
        }
      }, this.disposeCallback = Ws(function() {
        return n.selfExecutor();
      });
    }
    return t.prototype.hasRun = function() {
      return this.didRun;
    }, t.prototype.dispose = function() {
      this.disposeCallback();
    }, t.prototype.getValue = function() {
      if (this.didRun || (this.dispose(), this.selfExecutor()), this.error)
        throw this.error;
      return this.value;
    }, t;
  }()
), kn = /* @__PURE__ */ function() {
  var t = function(e, n) {
    return t = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(r, s) {
      r.__proto__ = s;
    } || function(r, s) {
      for (var i in s) Object.prototype.hasOwnProperty.call(s, i) && (r[i] = s[i]);
    }, t(e, n);
  };
  return function(e, n) {
    if (typeof n != "function" && n !== null)
      throw new TypeError("Class extends value " + String(n) + " is not a constructor or null");
    t(e, n);
    function r() {
      this.constructor = e;
    }
    e.prototype = n === null ? Object.create(n) : (r.prototype = n.prototype, new r());
  };
}(), Xr = function() {
  return Xr = Object.assign || function(t) {
    for (var e, n = 1, r = arguments.length; n < r; n++) {
      e = arguments[n];
      for (var s in e) Object.prototype.hasOwnProperty.call(e, s) && (t[s] = e[s]);
    }
    return t;
  }, Xr.apply(this, arguments);
}, on = function(t, e, n) {
  if (n || arguments.length === 2) for (var r = 0, s = e.length, i; r < s; r++)
    (i || !(r in e)) && (i || (i = Array.prototype.slice.call(e, 0, r)), i[r] = e[r]);
  return t.concat(i || Array.prototype.slice.call(e));
}, gf = 300, pr = Symbol("$$NOT_INSTANTIATED_SYMBOL"), pf = (
  /** @class */
  function(t) {
    kn(e, t);
    function e(n) {
      return t.call(this, 'Detecting cyclic dependency. The last identifier is "'.concat(Et(n), '".')) || this;
    }
    return e;
  }(at)
), mf = (
  /** @class */
  function(t) {
    kn(e, t);
    function e() {
      return t.call(this, "Injector cannot be accessed after it was disposed.") || this;
    }
    return e;
  }(at)
), _f = (
  /** @class */
  function(t) {
    kn(e, t);
    function e(n) {
      return t.call(this, 'Async item "'.concat(Et(n), '" returns another async item.')) || this;
    }
    return e;
  }(at)
), Ef = (
  /** @class */
  function(t) {
    kn(e, t);
    function e(n) {
      return t.call(this, 'Cannot get async item "'.concat(Et(n), '" from sync api.')) || this;
    }
    return e;
  }(at)
), Eo = (
  /** @class */
  function(t) {
    kn(e, t);
    function e(n) {
      return t.call(this, 'Cannot add dependency "'.concat(Et(n), '" after it is already resolved.')) || this;
    }
    return e;
  }(at)
), Cf = (
  /** @class */
  function(t) {
    kn(e, t);
    function e(n) {
      return t.call(this, 'Cannot dependency dependency "'.concat(Et(n), '" after it is already resolved.')) || this;
    }
    return e;
  }(at)
), Ot = (
  /** @class */
  function() {
    function t(e, n) {
      n === void 0 && (n = null), this.parent = n, this.children = [], this.resolutionOngoing = 0, this.disposingCallbacks = /* @__PURE__ */ new Set(), this.disposed = !1, this.dependencyCollection = new hf(e || []), this.resolvedDependencyCollection = new df(), n && n.children.push(this);
    }
    return t.prototype.onDispose = function(e) {
      var n = this;
      return this.disposingCallbacks.add(e), { dispose: function() {
        return n.disposingCallbacks.delete(e);
      } };
    }, t.prototype.createChild = function(e) {
      return this._ensureInjectorNotDisposed(), new t(e, this);
    }, t.prototype.dispose = function() {
      this.children.forEach(function(e) {
        return e.dispose();
      }), this.children.length = 0, this.dependencyCollection.dispose(), this.resolvedDependencyCollection.dispose(), this.deleteSelfFromParent(), this.disposed = !0, this.disposingCallbacks.forEach(function(e) {
        return e();
      }), this.disposingCallbacks.clear();
    }, t.prototype.deleteSelfFromParent = function() {
      if (this.parent) {
        var e = this.parent.children.indexOf(this);
        e > -1 && this.parent.children.splice(e, 1);
      }
    }, t.prototype.add = function(e) {
      this._ensureInjectorNotDisposed();
      var n = e[0], r = e[1];
      if (this.resolvedDependencyCollection.has(n))
        throw new Eo(n);
      typeof r > "u" ? this.dependencyCollection.add(n) : co(r) || ao(r) || lo(r) || uo(r) ? this.dependencyCollection.add(n, r) : this.resolvedDependencyCollection.add(n, r);
    }, t.prototype.replace = function(e) {
      this._ensureInjectorNotDisposed();
      var n = e[0];
      if (this.resolvedDependencyCollection.has(n))
        throw new Eo(n);
      this.dependencyCollection.delete(n), e.length === 1 ? this.dependencyCollection.add(n) : this.dependencyCollection.add(n, e[1]);
    }, t.prototype.delete = function(e) {
      if (this._ensureInjectorNotDisposed(), this.resolvedDependencyCollection.has(e))
        throw new Cf(e);
      this.dependencyCollection.delete(e);
    }, t.prototype.invoke = function(e) {
      for (var n = this, r = [], s = 1; s < arguments.length; s++)
        r[s - 1] = arguments[s];
      this._ensureInjectorNotDisposed();
      var i = {
        get: function(o, a, u) {
          return n._get(o, a, u);
        },
        has: function(o) {
          return n.has(o);
        }
      };
      return e.apply(void 0, on([i], r, !1));
    }, t.prototype.has = function(e) {
      var n;
      return this.dependencyCollection.has(e) || ((n = this.parent) === null || n === void 0 ? void 0 : n.has(e)) || !1;
    }, t.prototype.get = function(e, n, r) {
      this._ensureInjectorNotDisposed();
      var s = this._get(e, n, r);
      if (Array.isArray(s) && s.some(function(i) {
        return ys(i);
      }) || ys(s))
        throw new Ef(e);
      return s;
    }, t.prototype._get = function(e, n, r, s) {
      var i = Ge.REQUIRED;
      if (n === Ge.REQUIRED || n === Ge.OPTIONAL || n === Ge.MANY ? i = n : r = n, !s) {
        var o = this.getValue(e, i, r);
        if (o !== pr)
          return o;
      }
      return this.createDependency(e, i, r, !s);
    }, t.prototype.getAsync = function(e) {
      this._ensureInjectorNotDisposed();
      var n = this.getValue(e, Ge.REQUIRED);
      if (n !== pr)
        return Promise.resolve(n);
      var r = this.createDependency(e, Ge.REQUIRED);
      return ys(r) ? r.whenReady() : Promise.resolve(r);
    }, t.prototype.createInstance = function(e) {
      for (var n = [], r = 1; r < arguments.length; r++)
        n[r - 1] = arguments[r];
      return this._ensureInjectorNotDisposed(), this._resolveClassImpl.apply(this, on([{
        useClass: e
      }], n, !1));
    }, t.prototype._resolveDependency = function(e, n, r) {
      r === void 0 && (r = !0);
      var s;
      po(e);
      try {
        lo(n) ? s = this._resolveValueDependency(e, n) : uo(n) ? s = this._resolveFactory(e, n, r) : ao(n) ? s = this._resolveClass(e, n, r) : Vd(n) ? s = this._resolveExisting(e, n) : s = this._resolveAsync(e, n), mo();
      } catch (i) {
        throw mo(), i;
      }
      return s;
    }, t.prototype._resolveExisting = function(e, n) {
      var r = this.get(n.useExisting);
      return this.resolvedDependencyCollection.add(e, r), r;
    }, t.prototype._resolveValueDependency = function(e, n) {
      var r = n.useValue;
      return this.resolvedDependencyCollection.add(e, r), r;
    }, t.prototype._resolveClass = function(e, n, r) {
      var s = this;
      r === void 0 && (r = !0);
      var i;
      if (n.lazy) {
        var o = new ff(function() {
          return s._ensureInjectorNotDisposed(), s._resolveClassImpl(n);
        });
        i = new Proxy(/* @__PURE__ */ Object.create(null), {
          get: function(a, u) {
            if (u in a)
              return a[u];
            if (u !== "whenReady") {
              var c = o.getValue(), l = c[u];
              return typeof l != "function" || (l = l.bind(c), a[u] = l), l;
            }
          },
          set: function(a, u, c) {
            return o.getValue()[u] = c, !0;
          }
        });
      } else
        i = this._resolveClassImpl(n);
      return e && r && this.resolvedDependencyCollection.add(e, i), i;
    }, t.prototype._resolveClassImpl = function(e) {
      for (var n, r = [], s = 1; s < arguments.length; s++)
        r[s - 1] = arguments[s];
      var i = e.useClass;
      this.markNewResolution(i);
      for (var o = cu(i).sort(function(O, U) {
        return O.paramIndex - U.paramIndex;
      }).map(function(O) {
        return Xr(Xr({}, O), { identifier: uf(O.identifier) });
      }), a = [], u = 0, c = o; u < c.length; u++) {
        var l = c[u];
        try {
          var h = this._get(l.identifier, l.quantity, l.lookUp, l.withNew);
          a.push(h);
        } catch (O) {
          throw O instanceof Ur || O instanceof Hs && O.actual === 0 ? new _o(i, l.identifier, l.paramIndex) : O;
        }
      }
      var d = on([], r, !0), f = o.length > 0 ? o[0].paramIndex : d.length;
      if (d.length !== f) {
        console.warn("[redi]: Expect ".concat(f, " custom parameter(s) of ").concat(Et(i), " but get ").concat(d.length, "."));
        var E = f - d.length;
        E > 0 ? d = on(on([], d, !0), Array.from({ length: E }).fill(void 0), !0) : d = d.slice(0, f);
      }
      var R = new (i.bind.apply(i, on(on([void 0], d, !1), a, !1)))();
      return (n = e == null ? void 0 : e.onInstantiation) === null || n === void 0 || n.call(e, R), this.markResolutionCompleted(), R;
    }, t.prototype._resolveFactory = function(e, n, r) {
      var s;
      this.markNewResolution(e);
      for (var i = du(n.deps), o = [], a = 0, u = i; a < u.length; a++) {
        var c = u[a];
        try {
          var l = this._get(c.identifier, c.quantity, c.lookUp, c.withNew);
          o.push(l);
        } catch (d) {
          throw d instanceof Ur || d instanceof Hs && d.actual === 0 ? new _o(e, c.identifier, c.paramIndex) : d;
        }
      }
      var h = n.useFactory.apply(null, o);
      return r && this.resolvedDependencyCollection.add(e, h), this.markResolutionCompleted(), (s = n == null ? void 0 : n.onInstantiation) === null || s === void 0 || s.call(n, h), h;
    }, t.prototype._resolveAsync = function(e, n) {
      var r = this, s = {
        __symbol: au,
        whenReady: function() {
          return r._resolveAsyncImpl(e, n);
        }
      };
      return s;
    }, t.prototype._resolveAsyncImpl = function(e, n) {
      var r = this;
      return n.useAsync().then(function(s) {
        var i = r.getValue(e);
        if (i !== pr)
          return i;
        var o;
        if (Array.isArray(s)) {
          var a = s[1];
          if (co(a))
            throw new _f(e);
          o = r._resolveDependency(e, a);
        } else ou(s) ? o = r._resolveClassImpl({
          useClass: s,
          onInstantiation: n.onInstantiation
        }) : o = s;
        return r.resolvedDependencyCollection.add(e, o), o;
      });
    }, t.prototype.getValue = function(e, n, r) {
      var s = this;
      n === void 0 && (n = Ge.REQUIRED);
      var i = function() {
        return s.dependencyCollection.has(e) && !s.resolvedDependencyCollection.has(e) ? pr : s.resolvedDependencyCollection.get(e, n);
      }, o = function() {
        return s.parent ? s.parent.getValue(e, n) : (Ni(e, n, 0), n === Ge.MANY ? [] : null);
      };
      return r === $t.SKIP_SELF ? o() : e === t ? this : r === $t.SELF || this.resolvedDependencyCollection.has(e) || this.dependencyCollection.has(e) ? i() : o();
    }, t.prototype.createDependency = function(e, n, r, s) {
      var i = this;
      n === void 0 && (n = Ge.REQUIRED), s === void 0 && (s = !0);
      var o = function() {
        var u = i.dependencyCollection.get(e, n), c = null;
        return Array.isArray(u) ? c = u.map(function(l) {
          return i._resolveDependency(e, l, s);
        }) : u && (c = i._resolveDependency(e, u, s)), c;
      }, a = function() {
        if (i.parent)
          return i.parent.createDependency(e, n, void 0, s);
        if (n === Ge.OPTIONAL)
          return null;
        throw po(e), new Ur(e);
      };
      return r === $t.SKIP_SELF ? a() : this.dependencyCollection.has(e) ? o() : a();
    }, t.prototype.markNewResolution = function(e) {
      if (this.resolutionOngoing += 1, this.resolutionOngoing >= gf)
        throw new pf(e);
    }, t.prototype.markResolutionCompleted = function() {
      this.resolutionOngoing -= 1;
    }, t.prototype._ensureInjectorNotDisposed = function() {
      if (this.disposed)
        throw new mf();
    }, t;
  }()
), Co = typeof globalThis < "u" && globalThis || typeof window < "u" && window || typeof global < "u" && global, Ro = "REDI_GLOBAL_LOCK", Rf = typeof process < "u" && process.versions != null && process.versions.node != null;
Co[Ro] ? Rf || console.error(`[redi]: You are loading scripts of redi more than once! This may cause undesired behavior in your application.
Maybe your dependencies added redi as its dependency and bundled redi to its dist files. Or you import different versions of redi.
For more info please visit our website: https://redi.wendell.fun/en-US/docs/debug#import-scripts-of-redi-more-than-once`) : Co[Ro] = !0;
var Io = "REDI_CONTEXT_LOCK", If = typeof process < "u" && process.versions != null && process.versions.node != null, vo = typeof globalThis < "u" && globalThis || typeof window < "u" && window || typeof global < "u" && global;
vo[Io] ? If || console.error(`[redi]: "RediContext" is already created. You may import "RediContext" from different paths. Use "import { RediContext } from '@wendellhu/redi/react-bindings'; instead."`) : vo[Io] = !0;
var ds = St.createContext({
  injector: null
});
ds.displayName = "RediContext";
var gu = ds.Provider, vf = ds.Consumer, Jr = function() {
  return Jr = Object.assign || function(t) {
    for (var e, n = 1, r = arguments.length; n < r; n++) {
      e = arguments[n];
      for (var s in e) Object.prototype.hasOwnProperty.call(e, s) && (t[s] = e[s]);
    }
    return t;
  }, Jr.apply(this, arguments);
};
function yf(t) {
  var e = t.children, n = t.dependencies, r = St.useRef(null);
  return St.useEffect(function() {
    return function() {
      var s;
      return (s = r.current) === null || s === void 0 ? void 0 : s.dispose();
    };
  }, []), St.createElement(vf, null, function(s) {
    var i;
    return r.current ? i = r.current : (i = s.injector ? s.injector.createChild(n) : new Ot(n), r.current = i), St.createElement(gu, { value: { injector: i } }, e);
  });
}
function B0(t, e) {
  return function(r) {
    return St.createElement(
      gu,
      { value: { injector: e } },
      St.createElement(t, Jr({}, r))
    );
  };
}
function j0(t, e) {
  return function(r) {
    return St.createElement(
      yf,
      { dependencies: e },
      St.createElement(t, Jr({}, r))
    );
  };
}
var wf = /* @__PURE__ */ function() {
  var t = function(e, n) {
    return t = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(r, s) {
      r.__proto__ = s;
    } || function(r, s) {
      for (var i in s) Object.prototype.hasOwnProperty.call(s, i) && (r[i] = s[i]);
    }, t(e, n);
  };
  return function(e, n) {
    if (typeof n != "function" && n !== null)
      throw new TypeError("Class extends value " + String(n) + " is not a constructor or null");
    t(e, n);
    function r() {
      this.constructor = e;
    }
    e.prototype = n === null ? Object.create(n) : (r.prototype = n.prototype, new r());
  };
}(), Of = (
  /** @class */
  function(t) {
    wf(e, t);
    function e(n) {
      return t.call(this, 'You should make "RediContext" as '.concat(n.constructor.name, "'s default context type. ") + "If you want to use multiple context, please check this on React doc site. https://reactjs.org/docs/context.html#classcontexttype") || this;
    }
    return e;
  }(at)
);
function H0(t, e, n) {
  return function() {
    return {
      get: function() {
        var r = this, s = r.context;
        if (!s || !s.injector)
          throw new Of(r);
        var i = s.injector, o = i.get(t, e || Ge.REQUIRED, n);
        return o;
      }
    };
  };
}
var bf = /* @__PURE__ */ function() {
  var t = function(e, n) {
    return t = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(r, s) {
      r.__proto__ = s;
    } || function(r, s) {
      for (var i in s) Object.prototype.hasOwnProperty.call(s, i) && (r[i] = s[i]);
    }, t(e, n);
  };
  return function(e, n) {
    if (typeof n != "function" && n !== null)
      throw new TypeError("Class extends value " + String(n) + " is not a constructor or null");
    t(e, n);
    function r() {
      this.constructor = e;
    }
    e.prototype = n === null ? Object.create(n) : (r.prototype = n.prototype, new r());
  };
}(), Sf = (
  /** @class */
  function(t) {
    bf(e, t);
    function e() {
      return t.call(this, "Using dependency injection outside of a RediContext.") || this;
    }
    return e;
  }(at)
);
function Af() {
  var t = St.useContext(ds);
  if (!t.injector)
    throw new Sf();
  return t.injector;
}
function W0(t, e, n) {
  var r = Af();
  return St.useMemo(function() {
    return r.get(t, e, n);
  }, [t, e, n]);
}
var Nf = function(t, e, n) {
  if (n || arguments.length === 2) for (var r = 0, s = e.length, i; r < s; r++)
    (i || !(r in e)) && (i || (i = Array.prototype.slice.call(e, 0, r)), i[r] = e[r]);
  return t.concat(i || Array.prototype.slice.call(e));
};
function Tf(t, e) {
  var n = t instanceof lt && typeof e > "u" ? t.getValue() : e, r = _i(n), s = r[0], i = r[1];
  return Ei(function() {
    var o = t.subscribe(function(a) {
      return i(a);
    });
    return function() {
      return o.unsubscribe();
    };
  }, [t]), s;
}
function yo(t) {
  return typeof t == "function" ? t() : t;
}
function z0(t, e, n, r) {
  if (typeof t == "function" && !r)
    throw new at("Expected deps to be provided when observable is a function!");
  var s = Lr(null), i = Lr(!1), o = Ua(function() {
    return t;
  }, Nf([], typeof r < "u" ? r : [t], !0)), a = _i(0);
  a[0];
  var u = a[1], c = Lr(function() {
    var l;
    if (o) {
      var h = yo(o).subscribe(function(d) {
        i.current = !0, l = d;
      });
      h.unsubscribe();
    }
    return l != null ? l : e;
  }());
  if (Ei(function() {
    var l = null;
    return o && (s.current = yo(o), l = s.current.subscribe(function(h) {
      c.current = h, u(function(d) {
        return d + 1;
      });
    })), function() {
      return l == null ? void 0 : l.unsubscribe();
    };
  }, [o]), n && !i.current)
    throw new Error("Expect `shouldHaveSyncValue` but not getting a sync value!");
  return c.current;
}
function Y0(t) {
  var e = _i(0), n = e[1];
  Ei(function() {
    var r = t.subscribe(function() {
      return n(function(s) {
        return s + 1;
      });
    });
    return function() {
      return r.unsubscribe();
    };
  }, []);
}
var zs = /* @__PURE__ */ new WeakMap();
function V0(t, e) {
  var n = Lr(void 0), r = Tf(t, e), s = Ua(function() {
    return Fl(r);
  }, [t]), i = $l(function(o) {
    return kl.createElement(s.Provider, { value: r }, o.children);
  }, [t, r]);
  return n.current !== t && (n.current && zs.delete(n.current), n.current = t, zs.set(t, s)), {
    Provider: i,
    value: r
  };
}
function G0(t) {
  var e = zs.get(t);
  if (!e)
    throw new at("try to read context value but no ancestor component subscribed it.");
  return Bl(e);
}
function K0(t, e) {
  e.forEach((n) => t.add(n));
}
function Mf(t, e) {
  e.forEach(([n]) => {
    t.has(n) && t.get(n);
  });
}
function Df(t, e) {
  if (Object.is(t, e))
    return !0;
  if (typeof t != "object" || !t || typeof e != "object" || !e)
    return !1;
  const n = Object.keys(t), r = Object.keys(e);
  if (n.length !== r.length)
    return !1;
  const s = Object.prototype.hasOwnProperty.bind(e);
  for (let i = 0; i < n.length; i++) {
    const o = n[i];
    if (!s(o))
      return !1;
    const a = t[o], u = e[o];
    if (a !== u)
      return !1;
  }
  return !0;
}
class wo extends Error {
  constructor(e) {
    super(e), this.name = "CustomCommandExecutionError";
  }
}
class xf extends Error {
  constructor() {
    super("Canceled by facade"), this.name = "CanceledError";
  }
}
async function Lf(t) {
  for (const [e, n] of t.entries())
    try {
      if (!await n())
        return {
          index: e,
          result: !1
        };
    } catch (r) {
      return {
        index: e,
        result: !1,
        error: r
      };
    }
  return {
    result: !0,
    index: -1
  };
}
function Uf(t) {
  for (const [e, n] of t.entries())
    try {
      if (!n())
        return {
          index: e,
          result: !1
        };
    } catch (r) {
      return {
        index: e,
        result: !1,
        error: r
      };
    }
  return {
    result: !0,
    index: -1
  };
}
function Oo(t) {
  var e = typeof Symbol == "function" && Symbol.iterator, n = e && t[e], r = 0;
  if (n) return n.call(t);
  if (t && typeof t.length == "number") return {
    next: function() {
      return t && r >= t.length && (t = void 0), { value: t && t[r++], done: !t };
    }
  };
  throw new TypeError(e ? "Object is not iterable." : "Symbol.iterator is not defined.");
}
function bo(t, e) {
  var n = typeof Symbol == "function" && t[Symbol.iterator];
  if (!n) return t;
  var r = n.call(t), s, i = [], o;
  try {
    for (; (e === void 0 || e-- > 0) && !(s = r.next()).done; ) i.push(s.value);
  } catch (a) {
    o = { error: a };
  } finally {
    try {
      s && !s.done && (n = r.return) && n.call(r);
    } finally {
      if (o) throw o.error;
    }
  }
  return i;
}
function So(t, e, n) {
  if (n || arguments.length === 2) for (var r = 0, s = e.length, i; r < s; r++)
    (i || !(r in e)) && (i || (i = Array.prototype.slice.call(e, 0, r)), i[r] = e[r]);
  return t.concat(i || Array.prototype.slice.call(e));
}
function Zn(t) {
  return typeof t == "function";
}
function Pf(t) {
  var e = function(r) {
    Error.call(r), r.stack = new Error().stack;
  }, n = t(e);
  return n.prototype = Object.create(Error.prototype), n.prototype.constructor = n, n;
}
var ws = Pf(function(t) {
  return function(n) {
    t(this), this.message = n ? n.length + ` errors occurred during unsubscription:
` + n.map(function(r, s) {
      return s + 1 + ") " + r.toString();
    }).join(`
  `) : "", this.name = "UnsubscriptionError", this.errors = n;
  };
});
function Ao(t, e) {
  if (t) {
    var n = t.indexOf(e);
    0 <= n && t.splice(n, 1);
  }
}
var pu = function() {
  function t(e) {
    this.initialTeardown = e, this.closed = !1, this._parentage = null, this._finalizers = null;
  }
  return t.prototype.unsubscribe = function() {
    var e, n, r, s, i;
    if (!this.closed) {
      this.closed = !0;
      var o = this._parentage;
      if (o)
        if (this._parentage = null, Array.isArray(o))
          try {
            for (var a = Oo(o), u = a.next(); !u.done; u = a.next()) {
              var c = u.value;
              c.remove(this);
            }
          } catch (R) {
            e = { error: R };
          } finally {
            try {
              u && !u.done && (n = a.return) && n.call(a);
            } finally {
              if (e) throw e.error;
            }
          }
        else
          o.remove(this);
      var l = this.initialTeardown;
      if (Zn(l))
        try {
          l();
        } catch (R) {
          i = R instanceof ws ? R.errors : [R];
        }
      var h = this._finalizers;
      if (h) {
        this._finalizers = null;
        try {
          for (var d = Oo(h), f = d.next(); !f.done; f = d.next()) {
            var E = f.value;
            try {
              No(E);
            } catch (R) {
              i = i != null ? i : [], R instanceof ws ? i = So(So([], bo(i)), bo(R.errors)) : i.push(R);
            }
          }
        } catch (R) {
          r = { error: R };
        } finally {
          try {
            f && !f.done && (s = d.return) && s.call(d);
          } finally {
            if (r) throw r.error;
          }
        }
      }
      if (i)
        throw new ws(i);
    }
  }, t.prototype.add = function(e) {
    var n;
    if (e && e !== this)
      if (this.closed)
        No(e);
      else {
        if (e instanceof t) {
          if (e.closed || e._hasParent(this))
            return;
          e._addParent(this);
        }
        (this._finalizers = (n = this._finalizers) !== null && n !== void 0 ? n : []).push(e);
      }
  }, t.prototype._hasParent = function(e) {
    var n = this._parentage;
    return n === e || Array.isArray(n) && n.includes(e);
  }, t.prototype._addParent = function(e) {
    var n = this._parentage;
    this._parentage = Array.isArray(n) ? (n.push(e), n) : n ? [n, e] : e;
  }, t.prototype._removeParent = function(e) {
    var n = this._parentage;
    n === e ? this._parentage = null : Array.isArray(n) && Ao(n, e);
  }, t.prototype.remove = function(e) {
    var n = this._finalizers;
    n && Ao(n, e), e instanceof t && e._removeParent(this);
  }, t.EMPTY = function() {
    var e = new t();
    return e.closed = !0, e;
  }(), t;
}();
pu.EMPTY;
function kf(t) {
  return t instanceof pu || t && "closed" in t && Zn(t.remove) && Zn(t.add) && Zn(t.unsubscribe);
}
function No(t) {
  Zn(t) ? t() : t.unsubscribe();
}
function Ze(t) {
  let e = !1;
  return t ? kf(t) ? {
    dispose: () => t.unsubscribe()
  } : typeof t == "function" ? {
    dispose: () => {
      e || (e = !0, t());
    }
  } : t : Ze(() => {
  });
}
function X0(t) {
  return Ze(() => {
    t.unsubscribe();
  });
}
class Mi {
  constructor() {
    C(this, "_disposables", /* @__PURE__ */ new Set());
  }
  add(e) {
    const n = Ze(e);
    return this._disposables.add(n), {
      dispose: (r = !1) => {
        r || n.dispose(), this._disposables.delete(n);
      }
    };
  }
  dispose() {
    this._disposables.forEach((e) => {
      e.dispose();
    }), this._disposables.clear();
  }
}
class nt {
  constructor() {
    C(this, "_disposed", !1);
    C(this, "_collection", new Mi());
  }
  disposeWithMe(e) {
    return this._collection.add(e);
  }
  ensureNotDisposed() {
    if (this._disposed)
      throw new Error("[Disposable]: object is disposed!");
  }
  dispose() {
    this._disposed || (this._disposed = !0, this._collection.dispose());
  }
}
class J0 extends nt {
  constructor() {
    super(...arguments);
    C(this, "dispose$", new _t());
  }
  dispose() {
    super.dispose(), this.dispose$.next(), this.dispose$.complete();
  }
}
class Z0 extends nt {
  constructor(n) {
    super();
    C(this, "_ref", 0);
    this._rootDisposable = n;
  }
  inc() {
    if (this._disposed)
      throw new Error("[RCDisposable]: should not ref to a disposed.");
    this._ref += 1;
  }
  dec() {
    this._ref -= 1, this._ref === 0 && (this._rootDisposable.dispose(), this.dispose());
  }
}
const fs = Ct("univer.context-service");
class Ff extends nt {
  constructor() {
    super(...arguments);
    C(this, "_contextChanged$", new _t());
    C(this, "contextChanged$", this._contextChanged$.asObservable());
    C(this, "_contextMap", /* @__PURE__ */ new Map());
  }
  dispose() {
    super.dispose(), this._contextChanged$.complete();
  }
  getContextValue(n) {
    var r;
    return (r = this._contextMap.get(n)) != null ? r : !1;
  }
  setContextValue(n, r) {
    this._contextMap.set(n, r), this._contextChanged$.next({ [n]: r });
  }
  subscribeContextValue$(n) {
    return new sr((r) => {
      const s = this._contextChanged$.pipe(Kt((i) => typeof i[n] < "u")).subscribe((i) => r.next(i[n]));
      return this._contextMap.has(n) && r.next(this._contextMap.get(n)), () => s.unsubscribe();
    });
  }
}
var $f = /* @__PURE__ */ ((t) => (t[t.SILENT = 0] = "SILENT", t[t.ERROR = 1] = "ERROR", t[t.WARN = 2] = "WARN", t[t.INFO = 3] = "INFO", t[t.VERBOSE = 4] = "VERBOSE", t))($f || {});
const Mt = Ct("univer.log");
class Bf extends nt {
  constructor() {
    super(...arguments);
    C(this, "_logLevel", 3);
  }
  debug(...n) {
    this._logLevel >= 4 && this._log(console.debug, ...n);
  }
  log(...n) {
    this._logLevel >= 3 && this._log(console.log, ...n);
  }
  warn(...n) {
    this._logLevel >= 2 && this._log(console.warn, ...n);
  }
  error(...n) {
    this._logLevel >= 1 && this._log(console.error, ...n);
  }
  setLogLevel(n) {
    this._logLevel = n;
  }
  _log(n, ...r) {
    const s = r[0];
    /^\[(.*?)\]/g.test(s) ? n(`\x1B[97;104m${s}\x1B[0m`, ...r.slice(1)) : n(...r);
  }
}
var jf = Object.defineProperty, Hf = Object.getOwnPropertyDescriptor, Wf = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? Hf(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && jf(e, n, s), s;
}, To = (t, e) => (n, r) => e(n, r, t), ar = /* @__PURE__ */ ((t) => (t[t.COMMAND = 0] = "COMMAND", t[t.OPERATION = 1] = "OPERATION", t[t.MUTATION = 2] = "MUTATION", t))(ar || {});
const Pt = Ct("anywhere.command-service");
class zf {
  constructor() {
    C(this, "_commands", /* @__PURE__ */ new Map());
    C(this, "_commandTypes", /* @__PURE__ */ new Map());
  }
  registerCommand(e) {
    if (this._commands.has(e.id))
      throw new Error(`[CommandRegistry]: command "${e.id}" has been registered before.`);
    return this._commands.set(e.id, e), this._commandTypes.set(e.id, e.type), Ze(() => {
      this._commands.delete(e.id), this._commandTypes.delete(e.id);
    });
  }
  hasCommand(e) {
    return this._commands.has(e);
  }
  getCommand(e) {
    return this._commands.has(e) ? [this._commands.get(e)] : null;
  }
  getCommandType(e) {
    return this._commandTypes.get(e);
  }
}
const Yf = {
  id: "nil",
  type: 0,
  handler: () => !0
};
let Ys = class extends nt {
  constructor(e, n) {
    super();
    C(this, "_commandRegistry");
    C(this, "_beforeCommandExecutionListeners", []);
    C(this, "_commandExecutedListeners", []);
    C(this, "_multiCommandDisposables", /* @__PURE__ */ new Map());
    C(this, "_commandExecutingLevel", 0);
    C(this, "_commandExecutionStack", []);
    this._injector = e, this._logService = n, this._commandRegistry = new zf(), this._registerCommand(Yf);
  }
  dispose() {
    super.dispose(), this._commandExecutedListeners.length = 0, this._beforeCommandExecutionListeners.length = 0;
  }
  hasCommand(e) {
    return this._commandRegistry.hasCommand(e);
  }
  registerCommand(e) {
    return this._registerCommand(e);
  }
  registerMultipleCommand(e) {
    return this._registerMultiCommand(e);
  }
  beforeCommandExecuted(e) {
    if (this._beforeCommandExecutionListeners.indexOf(e) === -1)
      return this._beforeCommandExecutionListeners.push(e), Ze(() => {
        const n = this._beforeCommandExecutionListeners.indexOf(e);
        this._beforeCommandExecutionListeners.splice(n, 1);
      });
    throw new Error("[CommandService]: could not add a listener twice.");
  }
  onCommandExecuted(e) {
    if (this._commandExecutedListeners.indexOf(e) === -1)
      return this._commandExecutedListeners.push(e), Ze(() => {
        const n = this._commandExecutedListeners.indexOf(e);
        this._commandExecutedListeners.splice(n, 1);
      });
    throw new Error("[CommandService]: could not add a listener twice.");
  }
  async executeCommand(e, n, r) {
    try {
      const s = this._commandRegistry.getCommand(e);
      if (s) {
        const [i] = s, o = {
          id: i.id,
          type: i.type,
          params: n
        }, a = this._pushCommandExecutionStack(o);
        this._beforeCommandExecutionListeners.forEach((c) => c(o, r));
        const u = await this._execute(i, n, r);
        return this._commandExecutedListeners.forEach((c) => c(o, r)), a.dispose(), u;
      }
      throw new Error(`[CommandService]: command "${e}" is not registered.`);
    } catch (s) {
      if (s instanceof wo)
        return !1;
      throw s;
    }
  }
  syncExecuteCommand(e, n, r) {
    var s;
    try {
      const i = this._commandRegistry.getCommand(e);
      if (i) {
        const [o] = i, a = {
          id: o.id,
          type: o.type,
          params: n
        };
        if (o.type === 2) {
          const l = jd(
            this._commandExecutionStack,
            (h) => h.type === 0
            /* COMMAND */
          );
          l && (a.params = (s = a.params) != null ? s : {}, a.params.trigger = l.id);
        }
        const u = this._pushCommandExecutionStack(a);
        this._beforeCommandExecutionListeners.forEach((l) => l(a, r));
        const c = this._syncExecute(o, n, r);
        return this._commandExecutedListeners.forEach((l) => l(a, r)), u.dispose(), c;
      }
      throw new Error(`[CommandService]: command "${e}" is not registered.`);
    } catch (i) {
      if (i instanceof wo)
        return !1;
      throw i;
    }
  }
  _pushCommandExecutionStack(e) {
    return this._commandExecutionStack.push(e), Ze(() => cs(this._commandExecutionStack, e));
  }
  _registerCommand(e) {
    return this._commandRegistry.registerCommand(e);
  }
  _registerMultiCommand(e) {
    const n = this._commandRegistry.getCommand(e.id);
    let r;
    if (n) {
      if (n[0].multi !== !0)
        throw new Error("Command has registered as a single command.");
      r = n[0];
    } else {
      const i = new Mi();
      r = new Vf(e.id), i.add(this._commandRegistry.registerCommand(r)), i.add(
        Ze(() => {
          this._multiCommandDisposables.delete(e.id);
        })
      ), this._multiCommandDisposables.set(e.id, i);
    }
    const s = r.registerImplementation(e);
    return Ze(() => {
      var i;
      s.dispose(), r.hasImplementations() || (i = this._multiCommandDisposables.get(e.id)) == null || i.dispose();
    });
  }
  async _execute(e, n, r) {
    this._logService.debug(
      "[CommandService]",
      `${"|-".repeat(Math.max(this._commandExecutingLevel, 0))}executing command "${e.id}"`
    ), this._commandExecutingLevel++;
    let s;
    try {
      s = await this._injector.invoke(e.handler, n, r), this._commandExecutingLevel--;
    } catch (i) {
      throw s = !1, this._commandExecutingLevel = 0, i;
    }
    return s;
  }
  _syncExecute(e, n, r) {
    this._logService.debug(
      "[CommandService]",
      `${"|-".repeat(Math.max(0, this._commandExecutingLevel))}executing command "${e.id}".`
    ), this._commandExecutingLevel++;
    let s;
    try {
      if (s = this._injector.invoke(e.handler, n, r), s instanceof Promise)
        throw new TypeError("[CommandService]: Command handler should not return a promise.");
      this._commandExecutingLevel--;
    } catch (i) {
      throw s = !1, this._commandExecutingLevel = 0, i;
    }
    return s;
  }
};
Ys = Wf([
  To(0, ot(Ot)),
  To(1, Mt)
], Ys);
class Vf {
  constructor(e) {
    C(this, "name");
    C(this, "multi", !0);
    C(this, "type", 0);
    C(this, "priority", 0);
    C(this, "_implementations", []);
    C(this, "handler", async (e, n) => {
      if (!this._implementations.length)
        return !1;
      const r = e.get(Mt), s = e.get(fs), i = e.get(Ot);
      for (const o of this._implementations) {
        const a = o.command.preconditions;
        if ((!a || a && a(s)) && (r.debug("[MultiCommand]", `executing implementation "${o.command.name}".`), await i.invoke(o.command.handler, n)))
          return !0;
      }
      return !1;
    });
    this.id = e, this.name = e;
  }
  registerImplementation(e) {
    const n = { command: e };
    return this._implementations.push(n), this._implementations.sort((r, s) => s.command.priority - r.command.priority), Ze(() => {
      const r = this._implementations.indexOf(n);
      this._implementations.splice(r, 1);
    });
  }
  hasImplementations() {
    return this._implementations.length > 0;
  }
}
function mu(t, e, n) {
  const r = t.map((s) => () => e.syncExecuteCommand(s.id, s.params, n));
  return Uf(r);
}
function Q0(t, e, n) {
  const r = t.map((s) => () => e.executeCommand(s.id, s.params, n));
  return Lf(r);
}
function Gf(t) {
  return new sr((e) => {
    const n = t((...r) => e.next(r));
    return () => n == null ? void 0 : n.dispose();
  });
}
function Kf(t) {
  return function(n) {
    return new sr((r) => (n.subscribe({
      next: (s) => {
        r.next(s), t(s) && r.complete();
      },
      complete: () => r.complete(),
      error: (s) => r.error(s)
    }), () => r.unsubscribe()));
  };
}
function q0(t = 0) {
  return (e) => {
    let n = [];
    return e.pipe(
      Wi((r) => n.push(r)),
      Sl(t),
      Da(() => n),
      Wi(() => n = [])
    );
  };
}
function eC(t) {
  const e = new Al(1);
  return setTimeout(() => e.next(), t), e.pipe(Nl(1));
}
const tC = (t) => new Promise((e) => {
  xa(
    Gf(t.onCommandExecuted.bind(t)).pipe(xl(([n]) => n.type === ar.MUTATION)),
    Tl(300)
  ).pipe(Ll(16), Ul()).subscribe(() => {
    e();
  });
});
function Xf(t, e) {
  let n = 0, r = t.length - 1;
  if (e < t[0]) return 0;
  if (e >= t[t.length - 1]) return t.length - 1;
  for (; n <= r; ) {
    if (t[n] === e) {
      for (; n < t.length && t[n] === e; )
        n++;
      return n;
    }
    if (e > t[n] && e < t[n + 1])
      return n + 1;
    if (t[r] === e) {
      for (; r < t.length && t[r] === e; )
        r++;
      return r;
    }
    if (e > t[r - 1] && e < t[r])
      return r;
    n++, r--;
  }
  return -1;
}
function nC(t, e) {
  let n = 0, r = t.length - 1;
  for (; n <= r; ) {
    const s = Math.floor((r + n) / 2);
    if (e < t[s] && (s === 0 || e >= t[s - 1]))
      return s;
    if (e >= t[s])
      n = s + 1;
    else if (e < t[s])
      r = s - 1;
    else
      return -1;
  }
  return -1;
}
function Jf(t, e) {
  let n = 0, r = t.length;
  for (; n < r; ) {
    const s = Math.floor((n + r) / 2);
    t[s] <= e ? n = s + 1 : r = s;
  }
  return n < t.length ? n : t.length - 1;
}
function rC(t, e, n = !1) {
  let r = t.length - 1;
  if (e < 0 || e < t[0])
    return 0;
  if (t.length < 40 || e <= t[20] || e >= t[r - 20] ? r = Xf(t, e) : r = Jf(t, e), n) {
    const s = t[r];
    return t.indexOf(s);
  }
  return r;
}
function sC(t) {
  const e = new Blob([t], { type: "text/javascript" });
  return window.URL.createObjectURL(e);
}
const mr = 2, Zf = 1;
function iC(t, e) {
  if (e == null || t == null)
    return !0;
  const { left: n = 0, top: r = 0, height: s = 0, width: i = 0, angle: o = 0 } = e, { left: a = 0, top: u = 0, height: c = 0, width: l = 0, angle: h = 0 } = t, d = l, f = c, E = i, R = s;
  return Math.abs(a - n) > mr || Math.abs(u - r) > mr || Math.abs(d - E) > mr || Math.abs(f - R) > mr || Math.abs(h - o) > Zf;
}
var _u = /* @__PURE__ */ ((t) => (t[t.DEFAULT_SERIES = 0] = "DEFAULT_SERIES", t[t.ALTERNATE_SERIES = 1] = "ALTERNATE_SERIES", t))(_u || {}), Xe = /* @__PURE__ */ ((t) => (t[t.NONE = 0] = "NONE", t[t.THIN = 1] = "THIN", t[t.HAIR = 2] = "HAIR", t[t.DOTTED = 3] = "DOTTED", t[t.DASHED = 4] = "DASHED", t[t.DASH_DOT = 5] = "DASH_DOT", t[t.DASH_DOT_DOT = 6] = "DASH_DOT_DOT", t[t.DOUBLE = 7] = "DOUBLE", t[t.MEDIUM = 8] = "MEDIUM", t[t.MEDIUM_DASHED = 9] = "MEDIUM_DASHED", t[t.MEDIUM_DASH_DOT = 10] = "MEDIUM_DASH_DOT", t[t.MEDIUM_DASH_DOT_DOT = 11] = "MEDIUM_DASH_DOT_DOT", t[t.SLANT_DASH_DOT = 12] = "SLANT_DASH_DOT", t[t.THICK = 13] = "THICK", t))(Xe || {}), Eu = /* @__PURE__ */ ((t) => (t.TOP = "top", t.BOTTOM = "bottom", t.LEFT = "left", t.RIGHT = "right", t.NONE = "none", t.ALL = "all", t.OUTSIDE = "outside", t.INSIDE = "inside", t.HORIZONTAL = "horizontal", t.VERTICAL = "vertical", t.TLBR = "tlbr", t.TLBC_TLMR = "tlbc_tlmr", t.TLBR_TLBC_TLMR = "tlbr_tlbc_tlmr", t.BLTR = "bl_tr", t.MLTR_BCTR = "mltr_bctr", t))(Eu || {}), vt = /* @__PURE__ */ ((t) => (t[t.UNSUPPORTED = 0] = "UNSUPPORTED", t[t.RGB = 1] = "RGB", t[t.HEX = 2] = "HEX", t[t.THEME = 3] = "THEME", t))(vt || {}), Cu = /* @__PURE__ */ ((t) => (t[t.ON = 0] = "ON", t[t.OFF = 1] = "OFF", t))(Cu || {}), Ru = /* @__PURE__ */ ((t) => (t[t.PASTE_NORMAL = 0] = "PASTE_NORMAL", t[t.PASTE_NO_BORDERS = 1] = "PASTE_NO_BORDERS", t[t.PASTE_FORMAT = 2] = "PASTE_FORMAT", t[t.PASTE_FORMULA = 3] = "PASTE_FORMULA", t[t.PASTE_DATA_VALIDATION = 4] = "PASTE_DATA_VALIDATION", t[t.PASTE_VALUES = 5] = "PASTE_VALUES", t[t.PASTE_CONDITIONAL_FORMATTING = 6] = "PASTE_CONDITIONAL_FORMATTING", t[t.PASTE_COLUMN_WIDTHS = 7] = "PASTE_COLUMN_WIDTHS", t))(Ru || {}), Iu = /* @__PURE__ */ ((t) => (t[t.LEFT = 0] = "LEFT", t[t.RIGHT = 1] = "RIGHT", t))(Iu || {}), vu = /* @__PURE__ */ ((t) => (t[t.DOCUMENT = 0] = "DOCUMENT", t[t.PROJECT = 1] = "PROJECT", t))(vu || {}), yu = /* @__PURE__ */ ((t) => (t[t.COLUMNS = 0] = "COLUMNS", t[t.ROWS = 1] = "ROWS", t))(yu || {}), wu = /* @__PURE__ */ ((t) => (t[t.UP = 0] = "UP", t[t.RIGHT = 1] = "RIGHT", t[t.DOWN = 2] = "DOWN", t[t.LEFT = 3] = "LEFT", t))(wu || {});
function oC(t) {
  switch (t) {
    case 3:
      return 1;
    case 1:
      return 3;
    case 0:
      return 2;
    case 2:
      return 0;
  }
}
var Ou = /* @__PURE__ */ ((t) => (t[t.INTERPOLATION_POINT_TYPE_UNSPECIFIED = 0] = "INTERPOLATION_POINT_TYPE_UNSPECIFIED", t[t.MIN = 1] = "MIN", t[t.MAX = 2] = "MAX", t[t.NUMBER = 3] = "NUMBER", t[t.PERCENT = 4] = "PERCENT", t[t.PERCENTILE = 5] = "PERCENTILE", t))(Ou || {}), ur = /* @__PURE__ */ ((t) => (t.EN_US = "enUS", t.FR_FR = "frFR", t.ZH_CN = "zhCN", t.RU_RU = "ruRU", t.ZH_TW = "zhTW", t.VI_VN = "viVN", t.FA_IR = "faIR", t))(ur || {}), Zr = /* @__PURE__ */ ((t) => (t[t.PERSON = 0] = "PERSON", t[t.FILE = 1] = "FILE", t[t.DATE = 2] = "DATE", t[t.LOCATION = 3] = "LOCATION", t[t.EVENT = 4] = "EVENT", t))(Zr || {}), bu = /* @__PURE__ */ ((t) => (t[t.RANGE = 0] = "RANGE", t[t.SHEET = 1] = "SHEET", t))(bu || {}), Qf = /* @__PURE__ */ ((t) => (t.Line = "line", t.LineInv = "lineInv", t.Triangle = "triangle", t.RtTriangle = "rtTriangle", t.Rect = "rect", t.Diamond = "diamond", t.Parallelogram = "parallelogram", t.Trapezoid = "trapezoid", t.NonIsocelesTrapezoid = "nonIsocelesTrapezoid", t.Pentagon = "pentagon", t.Hexagon = "hexagon", t.Heptagon = "heptagon", t.Octagon = "octagon", t.Decagon = "decagon", t.Dodecagon = "dodecagon", t.Star4 = "star4", t.Star5 = "star5", t.Star6 = "star6", t.Star7 = "star7", t.Star8 = "star8", t.Star10 = "star10", t.Star12 = "star12", t.Star16 = "star16", t.Star24 = "star24", t.Star32 = "star32", t.RoundRect = "roundRect", t.Round1Rect = "round1Rect", t.Round2SameRect = "round2SameRect", t.Round2DiagRect = "round2DiagRect", t.Ellipse = "ellipse", t))(Qf || {}), qf = /* @__PURE__ */ ((t) => (t.RightArrow = "rightArrow", t.LeftArrow = "leftArrow", t.UpArrow = "upArrow", t.DownArrow = "downArrow", t.LeftRightArrow = "leftRightArrow", t.UpDownArrow = "upDownArrow", t.QuadArrow = "quadArrow", t.LeftRightUpArrow = "leftRightUpArrow", t.BentArrow = "bentArrow", t.UturnArrow = "uturnArrow", t.CircularArrow = "circularArrow", t.NotchedRightArrow = "notchedRightArrow", t.HomePlate = "homePlate", t.Chevron = "chevron", t.LeftCircularArrow = "leftCircularArrow", t.LeftRightCircularArrow = "leftRightCircularArrow", t))(qf || {}), eg = /* @__PURE__ */ ((t) => (t.Plaque = "plaque", t.Can = "can", t.Cube = "cube", t.Bevel = "bevel", t.Donut = "donut", t.NoSmoking = "noSmoking", t.BlockArc = "blockArc", t.FoldedCorner = "foldedCorner", t))(eg || {}), tg = /* @__PURE__ */ ((t) => (t.SmileyFace = "smileyFace", t.Heart = "heart", t.LightningBolt = "lightningBolt", t.Sun = "sun", t.Moon = "moon", t.Cloud = "cloud", t.Arc = "arc", t.Backpack = "backpack", t.Frame = "frame", t.HalfFrame = "halfFrame", t.Corner = "corner", t.Chord = "chord", t.Pie = "pie", t.Teardrop = "teardrop", t.WedgeRectCallout = "wedgeRectCallout", t.WedgeRRectCallout = "wedgeRRectCallout", t.WedgeEllipseCallout = "wedgeEllipseCallout", t.CloudCallout = "cloudCallout", t.BorderCallout1 = "borderCallout1", t.BorderCallout2 = "borderCallout2", t.BorderCallout3 = "borderCallout3", t.AccentCallout1 = "accentCallout1", t.AccentCallout2 = "accentCallout2", t.AccentCallout3 = "accentCallout3", t.Callout1 = "callout1", t.Callout2 = "callout2", t.Callout3 = "callout3", t.ActionButtonBackPrevious = "actionButtonBackPrevious", t.ActionButtonEnd = "actionButtonEnd", t.ActionButtonForwardNext = "actionButtonForwardNext", t.ActionButtonHelp = "actionButtonHelp", t.ActionButtonHome = "actionButtonHome", t.ActionButtonInformation = "actionButtonInformation", t.ActionButtonMovie = "actionButtonMovie", t.ActionButtonReturn = "actionButtonReturn", t.ActionButtonSound = "actionButtonSound", t))(tg || {}), Su = /* @__PURE__ */ ((t) => (t[t.RELATIVE_DATE_UNSPECIFIED = 0] = "RELATIVE_DATE_UNSPECIFIED", t[t.PAST_YEAR = 1] = "PAST_YEAR", t[t.PAST_MONTH = 2] = "PAST_MONTH", t[t.PAST_WEEK = 3] = "PAST_WEEK", t[t.YESTERDAY = 4] = "YESTERDAY", t[t.TODAY = 5] = "TODAY", t[t.TOMORROW = 6] = "TOMORROW", t))(Su || {}), Au = /* @__PURE__ */ ((t) => (t[t.GRID = 0] = "GRID", t[t.KANBAN = 1] = "KANBAN", t[t.GANTT = 2] = "GANTT", t))(Au || {}), er = /* @__PURE__ */ ((t) => (t[t.UNSPECIFIED = 0] = "UNSPECIFIED", t[t.LEFT_TO_RIGHT = 1] = "LEFT_TO_RIGHT", t[t.RIGHT_TO_LEFT = 2] = "RIGHT_TO_LEFT", t))(er || {}), Nu = /* @__PURE__ */ ((t) => (t[t.DASH = 0] = "DASH", t[t.DASH_DOT_DOT_HEAVY = 1] = "DASH_DOT_DOT_HEAVY", t[t.DASH_DOT_HEAVY = 2] = "DASH_DOT_HEAVY", t[t.DASHED_HEAVY = 3] = "DASHED_HEAVY", t[t.DASH_LONG = 4] = "DASH_LONG", t[t.DASH_LONG_HEAVY = 5] = "DASH_LONG_HEAVY", t[t.DOT_DASH = 6] = "DOT_DASH", t[t.DOT_DOT_DASH = 7] = "DOT_DOT_DASH", t[t.DOTTED = 8] = "DOTTED", t[t.DOTTED_HEAVY = 9] = "DOTTED_HEAVY", t[t.DOUBLE = 10] = "DOUBLE", t[t.NONE = 11] = "NONE", t[t.SINGLE = 12] = "SINGLE", t[t.THICK = 13] = "THICK", t[t.WAVE = 14] = "WAVE", t[t.WAVY_DOUBLE = 15] = "WAVY_DOUBLE", t[t.WAVY_HEAVY = 16] = "WAVY_HEAVY", t[t.WORDS = 17] = "WORDS", t))(Nu || {}), Xt = /* @__PURE__ */ ((t) => (t[t.UNSPECIFIED = 0] = "UNSPECIFIED", t[t.LEFT = 1] = "LEFT", t[t.CENTER = 2] = "CENTER", t[t.RIGHT = 3] = "RIGHT", t[t.JUSTIFIED = 4] = "JUSTIFIED", t[t.BOTH = 5] = "BOTH", t[t.DISTRIBUTED = 6] = "DISTRIBUTED", t))(Xt || {}), hn = /* @__PURE__ */ ((t) => (t[t.UNSPECIFIED = 0] = "UNSPECIFIED", t[t.TOP = 1] = "TOP", t[t.MIDDLE = 2] = "MIDDLE", t[t.BOTTOM = 3] = "BOTTOM", t))(hn || {}), xn = /* @__PURE__ */ ((t) => (t[t.UNSPECIFIED = 0] = "UNSPECIFIED", t[t.OVERFLOW = 1] = "OVERFLOW", t[t.CLIP = 2] = "CLIP", t[t.WRAP = 3] = "WRAP", t))(xn || {}), Vs = /* @__PURE__ */ ((t) => (t[t.NORMAL = 0] = "NORMAL", t[t.ITALIC = 1] = "ITALIC", t))(Vs || {}), Gs = /* @__PURE__ */ ((t) => (t[t.NORMAL = 0] = "NORMAL", t[t.BOLD = 1] = "BOLD", t))(Gs || {}), Bt = /* @__PURE__ */ ((t) => (t[t.NORMAL = 1] = "NORMAL", t[t.SUBSCRIPT = 2] = "SUBSCRIPT", t[t.SUPERSCRIPT = 3] = "SUPERSCRIPT", t))(Bt || {}), we = /* @__PURE__ */ ((t) => (t[t.FALSE = 0] = "FALSE", t[t.TRUE = 1] = "TRUE", t))(we || {}), dn = /* @__PURE__ */ ((t) => (t[t.STRING = 1] = "STRING", t[t.NUMBER = 2] = "NUMBER", t[t.BOOLEAN = 3] = "BOOLEAN", t[t.FORCE_STRING = 4] = "FORCE_STRING", t))(dn || {}), ft = /* @__PURE__ */ ((t) => (t[t.DARK1 = 0] = "DARK1", t[t.LIGHT1 = 1] = "LIGHT1", t[t.DARK2 = 2] = "DARK2", t[t.LIGHT2 = 3] = "LIGHT2", t[t.ACCENT1 = 4] = "ACCENT1", t[t.ACCENT2 = 5] = "ACCENT2", t[t.ACCENT3 = 6] = "ACCENT3", t[t.ACCENT4 = 7] = "ACCENT4", t[t.ACCENT5 = 8] = "ACCENT5", t[t.ACCENT6 = 9] = "ACCENT6", t[t.HYPERLINK = 10] = "HYPERLINK", t[t.FOLLOWED_HYPERLINK = 11] = "FOLLOWED_HYPERLINK", t))(ft || {}), Di = /* @__PURE__ */ ((t) => (t.OFFICE = "Office", t.OFFICE_2007_2010 = "Office 2007-2010", t.GRAYSCALE = "Grayscale", t.BLUE_WARM = "Blue Warm", t.BLUE = "Blue", t.BLUE_II = "Blue II", t.BLUE_GREEN = "Blue Green", t.GREEN = "Green", t.GREEN_YELLOW = "Green Yellow", t.YELLOW = "Yellow", t.YELLOW_ORANGE = "Yellow Orange", t.ORANGE = "Orange", t.ORANGE_RED = "Orange Red", t.RED_ORANGE = "Red Orange", t.RED = "Red", t.RED_VIOLET = "Red Violet", t.VIOLET = "Violet", t.VIOLET_II = "Violet II", t.MEDIAN = "Median", t.PAPER = "Paper", t.MARQUEE = "Marquee", t.SLIPSTREAM = "Slipstream", t.Aspect = "Aspect", t))(Di || {});
const ng = "useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict";
let rg = (t) => crypto.getRandomValues(new Uint8Array(t)), sg = (t, e, n) => {
  let r = (2 << Math.log2(t.length - 1)) - 1, s = -~(1.6 * r * e / t.length);
  return (i = e) => {
    let o = "";
    for (; ; ) {
      let a = n(s), u = s | 0;
      for (; u--; )
        if (o += t[a[u] & r] || "", o.length >= i) return o;
    }
  };
}, ig = (t, e = 21) => sg(t, e | 0, rg), og = (t = 21) => {
  let e = "", n = crypto.getRandomValues(new Uint8Array(t |= 0));
  for (; t--; )
    e += ng[n[t] & 63];
  return e;
};
const Tu = /* @__PURE__ */ new Set([
  "ac",
  "ad",
  "ae",
  "aero",
  "af",
  "ag",
  "ai",
  "al",
  "am",
  "ao",
  "aq",
  "ar",
  "arpa",
  "as",
  "asia",
  "at",
  "au",
  "aw",
  "ax",
  "az",
  "ba",
  "bb",
  "bd",
  "be",
  "bf",
  "bg",
  "bh",
  "bi",
  "biz",
  "bj",
  "bm",
  "bn",
  "bo",
  "br",
  "bs",
  "bt",
  "bv",
  "bw",
  "by",
  "bz",
  "ca",
  "cat",
  "cc",
  "cd",
  "cf",
  "cg",
  "ch",
  "ci",
  "ck",
  "cl",
  "cm",
  "cn",
  "co",
  "com",
  "coop",
  "cr",
  "cu",
  "cv",
  "cw",
  "cx",
  "cy",
  "cz",
  "de",
  "dj",
  "dk",
  "dm",
  "do",
  "dz",
  "ec",
  "edu",
  "ee",
  "eg",
  "er",
  "es",
  "et",
  "eu",
  "fi",
  "fj",
  "fk",
  "fm",
  "fo",
  "fr",
  "ga",
  "gb",
  "gd",
  "ge",
  "gf",
  "gg",
  "gh",
  "gi",
  "gl",
  "gm",
  "gn",
  "gov",
  "gp",
  "gq",
  "gr",
  "gs",
  "gt",
  "gu",
  "gw",
  "gy",
  "hk",
  "hm",
  "hn",
  "hr",
  "ht",
  "hu",
  "id",
  "ie",
  "il",
  "im",
  "in",
  "info",
  "int",
  "io",
  "iq",
  "ir",
  "is",
  "it",
  "je",
  "jm",
  "jo",
  "jobs",
  "jp",
  "ke",
  "kg",
  "kh",
  "ki",
  "km",
  "kn",
  "kp",
  "kr",
  "kw",
  "ky",
  "kz",
  "la",
  "lb",
  "lc",
  "li",
  "lk",
  "lr",
  "ls",
  "lt",
  "lu",
  "lv",
  "ly",
  "ma",
  "mc",
  "md",
  "me",
  "mg",
  "mh",
  "mil",
  "mk",
  "ml",
  "mm",
  "mn",
  "mo",
  "mobi",
  "mp",
  "mq",
  "mr",
  "ms",
  "mt",
  "mu",
  "museum",
  "mv",
  "mw",
  "mx",
  "my",
  "mz",
  "na",
  "name",
  "nc",
  "ne",
  "net",
  "nf",
  "ng",
  "ni",
  "nl",
  "no",
  "np",
  "nr",
  "nu",
  "nz",
  "om",
  "onion",
  "org",
  "pa",
  "pe",
  "pf",
  "pg",
  "ph",
  "pk",
  "pl",
  "pm",
  "pn",
  "post",
  "pr",
  "pro",
  "ps",
  "pt",
  "pw",
  "py",
  "qa",
  "re",
  "ro",
  "rs",
  "ru",
  "rw",
  "sa",
  "sb",
  "sc",
  "sd",
  "se",
  "sg",
  "sh",
  "si",
  "sj",
  "sk",
  "sl",
  "sm",
  "sn",
  "so",
  "sr",
  "ss",
  "st",
  "su",
  "sv",
  "sx",
  "sy",
  "sz",
  "tc",
  "td",
  "tel",
  "tf",
  "tg",
  "th",
  "tj",
  "tk",
  "tl",
  "tm",
  "tn",
  "to",
  "tr",
  "tt",
  "tv",
  "tw",
  "tz",
  "ua",
  "ug",
  "uk",
  "us",
  "uy",
  "uz",
  "va",
  "vc",
  "ve",
  "vg",
  "vi",
  "vn",
  "vu",
  "wf",
  "ws",
  "yt",
  "za",
  "zm",
  "zw"
]), ag = new RegExp(
  "^(?:(?:(?:https?|ftp):)?\\/\\/)?(?:\\S+(?::\\S*)?@)?(?:(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[1-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z0-9\\u00a1-\\uffff][a-z0-9\\u00a1-\\uffff_-]{0,62})?[a-z0-9\\u00a1-\\uffff]\\.)+(?:[a-z\\u00a1-\\uffff]{2,}\\.?))(?::\\d{2,5})?(?:[/?#]\\S*)?$",
  "i"
);
function ug(t) {
  if (!Number.isNaN(+t))
    return !1;
  if (t.startsWith("http://localhost:3002") || t.startsWith("localhost:3002"))
    return !0;
  if (ag.test(t)) {
    if (Mu(t))
      return !0;
    try {
      const r = new URL(Du(t)).hostname.split(".").pop();
      if (r && Tu.has(r))
        return !0;
    } catch {
      return !1;
    }
  }
  return !1;
}
function Mu(t) {
  return /^[a-zA-Z]+:\/\//.test(t);
}
function lg(t) {
  return /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(t);
}
function Du(t) {
  return Mu(t) ? t : lg(t) ? `mailto://${t}` : `https://${t}`;
}
const cg = /^-ms-/, hg = /-([a-z])/g, Vt = [
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
  "K",
  "L",
  "M",
  "N",
  "O",
  "P",
  "Q",
  "R",
  "S",
  "T",
  "U",
  "V",
  "W",
  "X",
  "Y",
  "Z"
];
function xi(t, e) {
  const n = re.getValueType(t), r = re.getValueType(e);
  return n !== r ? !1 : re.isArray(t) ? dg(t, e) : re.isObject(t) ? fg(t, e) : re.isDate(t) ? t.getTime() === e.getTime() : re.isRegExp(t) ? t.toString() === e.toString() : t === e;
}
function dg(t, e) {
  if (t.length !== e.length)
    return !1;
  for (let n = 0, r = t.length; n < r; n++) {
    const s = t[n], i = e[n];
    if (!xi(s, i))
      return !1;
  }
  return !0;
}
function fg(t, e) {
  const n = Object.keys(t), r = Object.keys(e);
  if (n.length !== r.length)
    return !1;
  for (const s of n) {
    if (!r.includes(s))
      return !1;
    const i = t[s], o = e[s];
    if (!xi(i, o))
      return !1;
  }
  return !0;
}
class re {
  static stringAt(e) {
    let n = "", r = e;
    for (; r >= Vt.length; )
      r /= Vt.length, r -= 1, n += Vt[r % Vt.length];
    const s = e % Vt.length;
    return n += Vt[s], n;
  }
  static indexAt(e) {
    let n = 0;
    for (let r = 0; r < e.length - 1; r += 1) {
      const s = e.charCodeAt(r) - 65, i = e.length - 1 - r;
      n += Vt.length ** i + Vt.length * s;
    }
    return n += e.charCodeAt(e.length - 1) - 65, n;
  }
  static deleteBlank(e) {
    return re.isString(e) ? e.replace(/\s/g, "") : e;
  }
  // eslint-disable-next-line complexity
  static getSystemType() {
    const e = navigator.userAgent, n = navigator.platform === "Win32" || navigator.platform === "Windows", r = navigator.platform === "Mac68K" || navigator.platform === "MacPPC" || navigator.platform === "Macintosh" || navigator.platform === "MacIntel";
    if (r) return "Mac";
    if (navigator.platform === "X11" && !n && !r) return "Unix";
    if (String(navigator.platform).indexOf("Linux") > -1) return "Linux";
    if (n) {
      if (e.indexOf("Windows NT 5.0") > -1 || e.indexOf("Windows 2000") > -1) return "Windows 2000";
      if (e.indexOf("Windows NT 5.1") > -1 || e.indexOf("Windows XP") > -1) return "Windows XP";
      if (e.indexOf("Windows NT 5.2") > -1 || e.indexOf("Windows 2003") > -1) return "Windows 2003";
      if (e.indexOf("Windows NT 6.0") > -1 || e.indexOf("Windows Vista") > -1) return "Windows Vista";
      if (e.indexOf("Windows NT 6.1") > -1 || e.indexOf("Windows 7") > -1) return "Windows 7";
      if (e.indexOf("Windows NT 10") > -1 || e.indexOf("Windows 10") > -1) return "Windows 10";
      if (e.indexOf("Windows NT 11") > -1 || e.indexOf("Windows 11") > -1) return "Windows 11";
    }
    return "Unknown system";
  }
  static getBrowserType() {
    const e = navigator.userAgent, n = e.indexOf("Opera") > -1, r = e.indexOf("compatible") > -1 && e.indexOf("MSIE") > -1 && !n, s = e.indexOf("Trident") > -1 && e.indexOf("rv:11.0") > -1, i = e.indexOf("Edge") > -1, o = e.indexOf("Firefox") > -1, a = e.indexOf("Safari") > -1 && e.indexOf("Chrome") === -1, u = e.indexOf("Chrome") > -1 && e.indexOf("Safari") > -1;
    if (r) {
      new RegExp("MSIE (\\d+\\.\\d+);").test(e);
      const l = Number.parseFloat(RegExp.$1);
      return l === 7 ? "IE7" : l === 8 ? "IE8" : l === 9 ? "IE9" : l === 10 ? "IE10" : "0";
    }
    return o ? "FF" : n ? "Opera" : a ? "Safari" : u ? "Chrome" : i ? "Edge" : s ? "IE11" : "Unknown browser";
  }
  /**
   * Use this method without `Tools`.
   *
   * @deprecated
   */
  static generateRandomId(e = 21, n) {
    return qt(e, n);
  }
  static getClassName(e) {
    return e.constructor.name;
  }
  /** @deprecated This method is deprecated, please use `import { merge } from '@univerjs/core` instead */
  static deepMerge(e, ...n) {
    n.forEach((o) => o && i(o));
    function r(o, a) {
      o.forEach((u, c) => {
        var l, h;
        if (re.isArray(u)) {
          const d = (l = a[c]) != null ? l : [];
          a[c] = d, r(u, d);
          return;
        }
        if (re.isObject(u)) {
          const d = (h = a[c]) != null ? h : {};
          a[c] = d, s(u, d);
          return;
        }
        a[c] = u;
      });
    }
    function s(o, a) {
      Object.keys(o).forEach((u) => {
        var l, h;
        const c = o[u];
        if (re.isObject(c)) {
          const d = (l = a[u]) != null ? l : {};
          a[u] = d, s(c, d);
          return;
        }
        if (re.isArray(c)) {
          const d = (h = a[u]) != null ? h : [];
          a[u] = d, r(c, d);
          return;
        }
        a[u] = c;
      });
    }
    function i(o) {
      Object.keys(o).forEach((a) => {
        var c, l;
        const u = o[a];
        if (re.isArray(u)) {
          const h = (c = e[a]) != null ? c : [];
          e[a] = h, r(u, h);
          return;
        }
        if (re.isObject(u)) {
          const h = (l = e[a]) != null ? l : {};
          e[a] = h, s(u, h);
          return;
        }
        e[a] = u;
      });
    }
    return e;
  }
  static numberFixed(e, n) {
    return Number(Number(e).toFixed(n));
  }
  static diffValue(e, n) {
    return xi(e, n);
  }
  static deepClone(e) {
    if (!this.isDefine(e))
      return e;
    if (this.isRegExp(e))
      return new RegExp(e);
    if (this.isDate(e))
      return new Date(e);
    if (this.isArray(e)) {
      const n = [];
      return e.forEach((r, s) => {
        n[s] = re.deepClone(r);
      }), n;
    }
    if (this.isObject(e)) {
      const n = {};
      return Object.keys(e).forEach((r) => {
        const s = e[r];
        n[r] = re.deepClone(s);
      }), Object.setPrototypeOf(n, Object.getPrototypeOf(e)), n;
    }
    return e;
  }
  static getLanguage() {
    const e = "en-US";
    return globalThis.navigator && (navigator.languages && navigator.languages[0] || navigator.language) || e;
  }
  static getValueType(e) {
    return Object.prototype.toString.apply(e);
  }
  static isDefine(e) {
    return e != null;
  }
  static isBlank(e) {
    return this.isDefine(e) ? this.isString(e) ? e.trim() === "" : !1 : !0;
  }
  static isBoolean(e) {
    return this.getValueType(e) === "[object Boolean]";
  }
  static isPlainObject(e) {
    return this.isDefine(e) ? Object.getPrototypeOf(e) === Object.getPrototypeOf({}) : !1;
  }
  static isFunction(e) {
    return this.getValueType(e) === "[object Function]";
  }
  static isDate(e) {
    return this.getValueType(e) === "[object Date]";
  }
  static isRegExp(e) {
    return this.getValueType(e) === "[object RegExp]";
  }
  static isArray(e) {
    return this.getValueType(e) === "[object Array]";
  }
  static isString(e) {
    return this.getValueType(e) === "[object String]";
  }
  static isNumber(e) {
    return this.getValueType(e) === "[object Number]";
  }
  static isStringNumber(e) {
    return !isNaN(Number.parseFloat(e)) && isFinite(e);
  }
  static isObject(e) {
    return this.getValueType(e) === "[object Object]";
  }
  static isEmptyObject(e) {
    for (const n in e)
      return !1;
    return !0;
  }
  static isMobile() {
    let e = 0, n = 0;
    return document.body.clientWidth && (e = document.body.clientWidth), document.body.clientHeight && (n = document.body.clientHeight), this.isAndroid() || this.isIPhone() || this.isTablet() || e < 350 && n < 500;
  }
  static isTablet() {
    return /ipad|android|android 3.0|xoom|sch-i800|playbook|tablet|kindle/i.test(navigator.userAgent.toLowerCase());
  }
  static isWeChat() {
    const e = navigator.userAgent.toLowerCase();
    return String(e.match(/MicroMessenger/i)) === "micromessenger";
  }
  static isAndroid() {
    const e = navigator.userAgent;
    return e.indexOf("Android") > -1 || e.indexOf("Linux") > -1;
  }
  static isIPhone() {
    return /iPhone/i.test(navigator.userAgent);
  }
  static isLegalUrl(e) {
    return ug(e);
  }
  static normalizeUrl(e) {
    return Du(e);
  }
  static topLevelDomainCombiningString() {
    return [...Tu].join("|");
  }
  static itCount(e) {
    return (n) => {
      for (let r = 0; r < e; r++)
        n && n();
    };
  }
  static hasLength(e, n) {
    return re.isDefine(e) ? re.isDefine(n) ? e.length === n : e.length > 0 : !1;
  }
  static capitalize(e) {
    return e.charAt(0).toUpperCase() + e.slice(1);
  }
  // Used by camelCase as callback to replace()
  static fCamelCase(e, n) {
    return n.toUpperCase();
  }
  // Convert dashed to camelCase; used by the css and data modules
  // Support: IE <=9 - 11, Edge 12 - 15
  // Microsoft forgot to hump their vendor prefix (#9572)
  static camelCase(e) {
    return e.replace(cg, "ms-").replace(hg, this.fCamelCase);
  }
  /**
   * remove all null from object
   * @param obj
   * @returns
   */
  static removeNull(e) {
    return this.isObject(e) && Object.keys(e).forEach((n) => {
      const r = e[n];
      r == null ? delete e[n] : re.removeNull(r);
    }), e;
  }
  /**
   * Generate a two-dimensional array with the specified number of rows and columns, and fill in the values
   * @param rows row length
   * @param columns column length
   * @param value value to be set
   * @returns
   */
  static fillTwoDimensionalArray(e, n, r) {
    return new Array(e).fill(r).map((s) => new Array(n).fill(r));
  }
  /**
   * Generate a two-dimensional array with the specified number of rows and columns, and fill in the values
   * @param rows row length
   * @param columns column length
   * @param value value to be set
   * @returns
   */
  // static fillObjectMatrix<T>(rows: number, columns: number, value: T): IObjectMatrixPrimitiveType<T> {
  //     const matrix = new ObjectMatrix<T>();
  //     for (let r = 0; r < rows; r++) {
  //         for (let c = 0; c < columns; c++) {
  //             matrix.setValue(r, c, value);
  //         }
  //     }
  //     return matrix.getData();
  // }
  static numToWord(e) {
    let n = "";
    for (; e > 0; ) {
      let r = e % 26;
      r = r === 0 ? r = 26 : r, n = String.fromCharCode(96 + r) + n, e = (e - r) / 26;
    }
    return n.toLocaleUpperCase();
  }
  /**
   *
   * Column subscript letter to number
   *
   * @privateRemarks
   * zh: 列下标  字母转数字
   *
   * @param a - Column subscript letter,e.g.,"A1"
   * @returns Column subscript number,e.g.,0
   *
   */
  static ABCatNum(e) {
    if (e == null || e.length === 0)
      return Number.NaN;
    const n = e.toLowerCase().split(""), r = n.length;
    let s = 0, i = 0;
    for (let o = 0; o < r; o++)
      i = n[o].charCodeAt(0) - 96, s += i * 26 ** (r - o - 1);
    return s === 0 ? Number.NaN : s - 1;
  }
  /**
   * en: Column subscript number to letter
   *
   * zh: 列下标  数字转字母
   *
   * @param n Column subscript number,e.g.,0
   * @returns Column subscript letter,e.g.,"A1"
   */
  static chatAtABC(e) {
    let i = "";
    for (; e >= 0; )
      i = String.fromCharCode(e % 26 + 97) + i, e = Math.floor(e / 26) - 1;
    return i.toUpperCase();
  }
  static randSort(e) {
    for (let n = 0, r = e.length; n < r; n++) {
      const s = Number.parseInt((Math.random() * r).toString()), i = e[s];
      e[s] = e[n], e[n] = i;
    }
    return e;
  }
  /**
   * extend two objects
   * @param originJson
   * @param extendJson
   * @returns
   */
  static commonExtend(e, n) {
    const r = {};
    for (const s in e)
      r[s] = e[s];
    for (const s in n)
      n[s] != null && (r[s] = n[s]);
    return r;
  }
  static commonExtend1(e, n) {
    for (const r in e)
      n[r] == null && (n[r] = e[r]);
    return n;
  }
  static arrayToObject(e) {
    const n = {};
    return e.forEach((r, s) => {
      n[s] = {}, r.forEach((i, o) => {
        n[s][o] = i;
      });
    }), n;
  }
  static hasIntersectionBetweenTwoRanges(e, n, r, s) {
    return n >= r && s >= e;
  }
  static isStartValidPosition(e) {
    return /^[A-Za-z_]/.test(e);
  }
  static isValidParameter(e) {
    const n = /[~!@#$%^&*()+=\-{}\[\]\|:;"'<>,?\/ ]+/.test(e), r = e.length <= 255;
    return !n && r;
  }
  static clamp(e, n, r) {
    return Math.max(n, Math.min(r, e));
  }
  static now() {
    return performance && performance.now ? performance.now() : Date.now();
  }
}
function qt(t = 21, e) {
  return e ? ig(e, t)() : og(t);
}
function Mo(...t) {
  const e = {}, n = t.length;
  for (let r = n - 1; r >= 0; r--) {
    const s = t[r];
    if (s) {
      const i = Object.keys(s);
      for (const o of i)
        e[o] === void 0 && (e[o] = s[o]);
    }
  }
  return e;
}
const aC = () => typeof process < "u" && process.versions != null && process.versions.node != null;
function Os(t, e, n) {
  const { dataStream: r, textRuns: s = [] } = t;
  let i = e;
  const o = [];
  for (const a of s) {
    const { st: u, ed: c } = a;
    re.hasIntersectionBetweenTwoRanges(e, n, u, c) && (u > i ? (o.push(r.slice(i, u)), o.push(Do(r, {
      ...a,
      ed: Math.min(c, n)
    }))) : o.push(Do(r, {
      ...a,
      st: i,
      ed: Math.min(c, n)
    }))), i = Math.max(e, Math.min(c, n));
  }
  return i !== n && o.push(r.slice(i, n)), o.join("");
}
function uC(t, e = !0) {
  var n;
  if (e && ((n = t.paragraphs) != null && n.length)) {
    const { dataStream: r, paragraphs: s = [] } = t;
    let i = "", o = -1;
    for (const a of s) {
      const { startIndex: u, paragraphStyle: c = {} } = a, { spaceAbove: l, spaceBelow: h, lineSpacing: d } = c, f = [];
      l != null && (typeof l == "number" ? f.push(`margin-top: ${l}px`) : f.push(`margin-top: ${l.v}px`)), h != null && (typeof h == "number" ? f.push(`margin-bottom: ${h}px`) : f.push(`margin-bottom: ${h.v}px`)), d != null && f.push(`line-height: ${d}`), u > o + 1 ? i += `<p class="UniverNormal" ${f.length ? `style="${f.join("; ")};"` : ""}>${Os(t, o + 1, u)}</p>` : i += `<p class="UniverNormal" ${f.length ? `style="${f.join("; ")};"` : ""}></p>`, o = u;
    }
    return o !== r.length && (i += Os(t, o, r.length)), i;
  } else
    return Os(t, 0, t.dataStream.length);
}
function Do(t, e) {
  const { st: n, ed: r, ts: s = {} } = e, { ff: i, fs: o, it: a, bl: u, ul: c, st: l, ol: h, bg: d, cl: f, va: E } = s;
  let R = t.slice(n, r);
  const O = [];
  return a === we.TRUE && (R = `<i>${R}</i>`), E === Bt.SUPERSCRIPT ? R = `<sup>${R}</sup>` : E === Bt.SUBSCRIPT && (R = `<sub>${R}</sub>`), (c == null ? void 0 : c.s) === we.TRUE && (R = `<u>${R}</u>`), (l == null ? void 0 : l.s) === we.TRUE && (R = `<s>${R}</s>`), u === we.TRUE && (R = `<strong>${R}</strong>`), i && O.push(`font-family: ${i}`), f && O.push(`color: ${f.rgb}`), o && O.push(`font-size: ${o}pt`), h && O.push("text-decoration: overline"), d && O.push(`background: ${d.rgb}`), O.length ? `<span style="${O.join("; ")};">${R}</span>` : R;
}
const gg = {
  [Di.OFFICE]: {
    [ft.ACCENT1]: "#4472C4",
    [ft.ACCENT2]: "#ED7D31",
    [ft.ACCENT3]: "#A5A5A5",
    [ft.ACCENT4]: "#70AD47",
    [ft.ACCENT5]: "#5B9BD5",
    [ft.ACCENT6]: "#70AD47",
    [ft.DARK1]: "#000000",
    [ft.DARK2]: "#44546A",
    [ft.LIGHT1]: "#FFFFFF",
    [ft.LIGHT2]: "#E7E6E6",
    [ft.HYPERLINK]: "#0563C1",
    [ft.FOLLOWED_HYPERLINK]: "#954F72"
  }
};
class gs {
  constructor() {
    C(this, "_themeValue", ft.LIGHT1);
    C(this, "_themeColors");
    C(this, "_themeTint");
    C(this, "_rgbValue", "");
    C(this, "_colorType");
    this._colorType = vt.UNSUPPORTED, this._themeColors = Di.OFFICE, this._themeTint = 0;
  }
  asRgbColor() {
    return new Ks(this._rgbValue, this);
  }
  asThemeColor() {
    return new Xs(this._themeValue, this._themeTint, this._themeColors, this);
  }
  build() {
    switch (this._colorType) {
      case vt.THEME:
        return this.asThemeColor();
      case vt.RGB:
        return this.asRgbColor();
      case vt.UNSUPPORTED:
        throw new Error("unsupported color type");
    }
  }
  setRgbColor(e) {
    return this._colorType = vt.RGB, this._rgbValue = e, this;
  }
  setThemeColors(e) {
    this._colorType = vt.THEME, this._themeColors = e;
  }
  setThemeTint(e) {
    this._colorType = vt.THEME, this._themeTint = e;
  }
  setThemeColor(e) {
    return this._colorType = vt.THEME, this._themeValue = e, this;
  }
  getColorType() {
    return this._colorType;
  }
}
class Ln {
  constructor(e) {
    C(this, "_builder");
    this._builder = e;
  }
  static rgbColorToHexValue(e) {
    return `#${((1 << 24) + (e.getRed() << 16) + (e.getGreen() << 8) + e.getBlue()).toString(16).slice(1)}`;
  }
  static hexValueToRgbColor(e) {
    e ? e.indexOf("#") > -1 && (e = e.substring(1)) : e = "#000000";
    const n = +`0x${e[0]}${e[1]}`, r = +`0x${e[2]}${e[3]}`, s = +`0x${e[4]}${e[5]}`;
    return new gs().setRgbColor(`rgb(${n},${r},${s})`).asRgbColor();
  }
  static hexToRgbString(e) {
    const n = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    e = e.replace(n, (i, o, a, u) => o + o + a + a + u + u);
    const r = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(e);
    let s = null;
    if (r) {
      const i = Number.parseInt(r[1], 16), o = Number.parseInt(r[2], 16), a = Number.parseInt(r[3], 16);
      s = `rgba(${i},${o},${a})`;
    }
    return s;
  }
  asRgbColor() {
    return this._builder.asRgbColor();
  }
  asThemeColor() {
    return this._builder.asThemeColor();
  }
  getColorType() {
    return this._builder.getColorType();
  }
  clone() {
    return new Ln(this._builder);
  }
  equals(e) {
    return !1;
  }
}
class pg {
  constructor(e) {
    C(this, "_saturation", 0);
    C(this, "_hue", 0);
    C(this, "_lightness", 0);
    C(this, "_alpha", 0);
    const n = e.getRed() / 255, r = e.getGreen() / 255, s = e.getBlue() / 255, i = e.getAlpha() / 255, o = Math.min(n, Math.min(r, s)), a = Math.max(n, Math.max(r, s)), u = a - o;
    if (a === o) {
      this._hue = 0, this._saturation = 0, this._lightness = a;
      return;
    }
    this._lightness = (o + a) / 2, this._lightness < 0.5 ? this._saturation = u / (a + o) : this._saturation = u / (2 - a - o), n === a && (this._hue = (r - s) / u), r === a && (this._hue = 2 + (s - n) / u), s === a && (this._hue = 4 + (n - r) / u), this._hue *= 60, this._hue < 0 && (this._hue += 360), this._alpha = i;
  }
  asRgbColor() {
    const e = new gs();
    if (this._saturation === 0)
      return e.setRgbColor(
        `rgba(${this._lightness * 255},${this._lightness * 255},${this._lightness * 255},${this._alpha * 255})`
      ), e.asRgbColor();
    let n;
    this._lightness < 0.5 ? n = this._lightness * (1 + this._saturation) : n = this._lightness + this._saturation - this._lightness * this._saturation;
    const r = 2 * this._lightness - n, s = this._hue / 360, i = s + 1 / 3, o = this.setColor(n, r, i), a = this.setColor(n, r, s), u = s - 1 / 3, c = this.setColor(n, r, u);
    return e.setRgbColor(
      `rgba(${Math.round(o * 255)},${Math.round(a * 255)},${Math.round(c * 255)},${this._alpha * 255})`
    ), e.asRgbColor();
  }
  getLightness() {
    return this._lightness;
  }
  getHue() {
    return this._hue;
  }
  getSaturation() {
    return this._saturation;
  }
  getAlpha() {
    return this._alpha;
  }
  setColor(e, n, r) {
    r < 0 && (r += 1), r > 1 && (r -= 1);
    let s;
    return 6 * r < 1 ? s = n + (e - n) * 6 * r : 2 * r < 1 ? s = e : 3 * r < 2 ? s = n + (e - n) * (2 / 3 - r) * 6 : s = n, s;
  }
  setLightness(e) {
    this._lightness = e;
  }
}
const It = class It extends Ln {
  constructor(n, r) {
    super(r);
    C(this, "_cssString");
    C(this, "_red");
    C(this, "_green");
    C(this, "_blue");
    C(this, "_alpha");
    let s = n.match(It.RGBA_EXTRACT);
    if (s) {
      const i = +s[1], o = +s[2], a = +s[3], u = +s[4];
      this._cssString = n, this._red = i, this._green = o, this._blue = a, this._alpha = u;
      return;
    }
    if (s = n.match(It.RGB_EXTRACT), s) {
      const i = +s[1], o = +s[2], a = +s[3];
      this._cssString = n, this._red = i, this._green = o, this._blue = a, this._alpha = 1;
      return;
    }
    throw new Error("Invalid rgba or rgb color");
  }
  asHexString() {
    return Ln.rgbColorToHexValue(this);
  }
  getRed() {
    let n = this._red + It.RGB_COLOR_AMT;
    return n > 255 ? n = 255 : n < 0 && (n = 0), n;
  }
  getGreen() {
    let n = this._green + It.RGB_COLOR_AMT;
    return n > 255 ? n = 255 : n < 0 && (n = 0), n;
  }
  getBlue() {
    let n = this._blue + It.RGB_COLOR_AMT;
    return n > 255 ? n = 255 : n < 0 && (n = 0), n;
  }
  getAlpha() {
    return this._alpha;
  }
  getColorType() {
    return vt.RGB;
  }
  clone() {
    return new It(this._cssString, this._builder);
  }
  asThemeColor() {
    throw new Error("rgb color not support to themeColor");
  }
  equals(n) {
    return n instanceof It ? n._red === this._red && n._blue === this._blue && n._green === this._green && n._alpha === this._alpha : !1;
  }
  getCssString() {
    return this._cssString;
  }
};
C(It, "RGB_COLOR_AMT", 0), C(It, "RGBA_EXTRACT", new RegExp(
  "\\s*rgba\\s*\\((\\s*\\d+\\s*),(\\s*\\d+\\s*),(\\s*\\d+\\s*),(\\s*\\d.\\d|\\d\\s*)\\)\\s*"
)), C(It, "RGB_EXTRACT", new RegExp("\\s*rgb\\s*\\((\\s*\\d+\\s*),(\\s*\\d+\\s*),(\\s*\\d+\\s*)\\)\\s*"));
let Ks = It;
const Gt = class Gt extends Ln {
  constructor(n, r, s, i) {
    super(i);
    C(this, "_themeColorType");
    C(this, "_themeTint");
    C(this, "_themeColors");
    this._themeColorType = n, this._themeTint = r, this._themeColors = s;
  }
  lumValue(n, r) {
    if (n == null)
      return r;
    let s;
    return n < 0 ? s = r * (1 + n) : s = r * (1 - n) + (255 - 255 * (1 - n)), s;
  }
  asRgbColor() {
    const n = gg[this._themeColors];
    if (n == null)
      throw new Error("not find themeColors type");
    const r = n[this._themeColorType];
    if (r == null)
      throw new Error("not find themeColors value");
    let s;
    if (Gt._cacheThemeColor.has(this._themeColors)) {
      if (s = Gt._cacheThemeColor.get(this._themeColors), s.has(this._themeColorType))
        return s.get(this._themeColorType);
    } else
      s = /* @__PURE__ */ new Map(), Gt._cacheThemeColor.set(this._themeColors, s);
    const i = new pg(Ln.hexValueToRgbColor(r));
    i.setLightness(this.lumValue(this._themeTint, i.getLightness() * 255) / 255);
    const o = i.asRgbColor();
    return s.set(this._themeColorType, o), o;
  }
  clone() {
    return new Gt(this._themeColorType, this._themeTint, this._themeColors, this._builder);
  }
  equals(n) {
    return n instanceof Gt ? n._themeColorType === this._themeColorType : !1;
  }
  getColorType() {
    return vt.THEME;
  }
  getThemeColorType() {
    return this._themeColorType;
  }
};
C(Gt, "_cacheThemeColor", /* @__PURE__ */ new Map());
let Xs = Gt;
const lC = "rgb(", cC = "rgba(", xo = {
  aliceBlue: [240, 248, 255],
  antiqueWhite: [250, 235, 215],
  aqua: [0, 255, 255],
  aquamarine: [127, 255, 212],
  azure: [240, 255, 255],
  beige: [245, 245, 220],
  bisque: [255, 228, 196],
  black: [0, 0, 0],
  blancheAlmond: [255, 235, 205],
  blue: [0, 0, 255],
  blueViolet: [138, 43, 226],
  brown: [165, 42, 42],
  burlyWood: [222, 184, 135],
  cadetBlue: [95, 158, 160],
  chartreuse: [127, 255, 0],
  chocolate: [210, 105, 30],
  coral: [255, 127, 80],
  cornFlowerBlue: [100, 149, 237],
  cornSilk: [255, 248, 220],
  crimson: [220, 20, 60],
  cyan: [0, 255, 255],
  darkblue: [0, 0, 139],
  darkCyan: [0, 139, 139],
  darkGoldenrod: [184, 132, 11],
  darkGray: [169, 169, 169],
  darkGreen: [0, 100, 0],
  darkGrey: [169, 169, 169],
  darkKhaki: [189, 183, 107],
  darkMagenta: [139, 0, 139],
  darkOliveGreen: [85, 107, 47],
  darkOrange: [255, 140, 0],
  darkOrchid: [153, 50, 204],
  darkRed: [139, 0, 0],
  darkSalmon: [233, 150, 122],
  darkSeaGreen: [143, 188, 143],
  darkSlateBlue: [72, 61, 139],
  darkSlateGray: [47, 79, 79],
  darkSlateGrey: [47, 79, 79],
  darkTurquoise: [0, 206, 209],
  darkViolet: [148, 0, 211],
  deepPink: [255, 20, 147],
  deepSkyBlue: [0, 191, 255],
  dimGray: [105, 105, 105],
  dimGrey: [105, 105, 105],
  dodgerBlue: [30, 144, 255],
  firebrick: [178, 34, 34],
  floralWhite: [255, 255, 240],
  forestGreen: [34, 139, 34],
  fuchsia: [255, 0, 255],
  gainsboro: [220, 220, 220],
  ghostWhite: [248, 248, 255],
  gold: [255, 215, 0],
  goldenrod: [218, 165, 32],
  gray: [128, 128, 128],
  green: [0, 128, 0],
  greenYellow: [173, 255, 47],
  grey: [128, 128, 128],
  honeydew: [240, 255, 240],
  hotPink: [255, 105, 180],
  indianRed: [205, 92, 92],
  indigo: [75, 0, 130],
  ivory: [255, 255, 240],
  khaki: [240, 230, 140],
  lavender: [230, 230, 250],
  lavenderBlush: [255, 240, 245],
  lawnGreen: [124, 252, 0],
  lemonChiffon: [255, 250, 205],
  lightblue: [173, 216, 230],
  lightCoral: [240, 128, 128],
  lightCyan: [224, 255, 255],
  lightGoldenrodYellow: [250, 250, 210],
  lightGray: [211, 211, 211],
  lightGreen: [144, 238, 144],
  lightGrey: [211, 211, 211],
  lightPink: [255, 182, 193],
  lightSalmon: [255, 160, 122],
  lightSeaGreen: [32, 178, 170],
  lightSkyBlue: [135, 206, 250],
  lightSlateGray: [119, 136, 153],
  lightSlateGrey: [119, 136, 153],
  lightSteelBlue: [176, 196, 222],
  lightYellow: [255, 255, 224],
  lime: [0, 255, 0],
  limeGreen: [50, 205, 50],
  linen: [250, 240, 230],
  magenta: [255, 0, 255],
  maroon: [128, 0, 0],
  mediumAquamarine: [102, 205, 170],
  mediumBlue: [0, 0, 205],
  mediumOrchid: [186, 85, 211],
  mediumPurple: [147, 112, 219],
  mediumSeaGreen: [60, 179, 113],
  mediumSlateBlue: [123, 104, 238],
  mediumSpringGreen: [0, 250, 154],
  mediumTurquoise: [72, 209, 204],
  mediumVioletRed: [199, 21, 133],
  midBightBlue: [25, 25, 112],
  mintCream: [245, 255, 250],
  mistyRose: [255, 228, 225],
  moccasin: [255, 228, 181],
  navajoWhite: [255, 222, 173],
  navy: [0, 0, 128],
  oldLace: [253, 245, 230],
  olive: [128, 128, 0],
  oliveDrab: [107, 142, 35],
  orange: [255, 165, 0],
  orangeRed: [255, 69, 0],
  orchid: [218, 112, 214],
  paleGoldenrod: [238, 232, 170],
  paleGreen: [152, 251, 152],
  paleTurquoise: [175, 238, 238],
  paleVioletRed: [219, 112, 147],
  papayaWhip: [255, 239, 213],
  peachPuff: [255, 218, 185],
  peru: [205, 133, 63],
  pink: [255, 192, 203],
  plum: [221, 160, 203],
  powderBlue: [176, 224, 230],
  purple: [128, 0, 128],
  rebeccaPurple: [102, 51, 153],
  red: [255, 0, 0],
  rosyBrown: [188, 143, 143],
  royalBlue: [65, 105, 225],
  saddleBrown: [139, 69, 19],
  salmon: [250, 128, 114],
  sandyBrown: [244, 164, 96],
  seaGreen: [46, 139, 87],
  seashell: [255, 245, 238],
  sienna: [160, 82, 45],
  silver: [192, 192, 192],
  skyBlue: [135, 206, 235],
  slateBlue: [106, 90, 205],
  slateGray: [119, 128, 144],
  slateGrey: [119, 128, 144],
  snow: [255, 255, 250],
  springGreen: [0, 255, 127],
  steelBlue: [70, 130, 180],
  tan: [210, 180, 140],
  teal: [0, 128, 128],
  thistle: [216, 191, 216],
  transparent: [255, 255, 255, 0],
  tomato: [255, 99, 71],
  turquoise: [64, 224, 208],
  violet: [238, 130, 238],
  wheat: [245, 222, 179],
  white: [255, 255, 255],
  whiteSmoke: [245, 245, 245],
  yellow: [255, 255, 0],
  yellowGreen: [154, 205, 5]
};
class Nt {
  constructor(e) {
    C(this, "_color");
    C(this, "_rgbColor");
    C(this, "_isValid", !1);
    if (e == null) {
      this._setNullColor();
      return;
    }
    if (e instanceof Nt) {
      this._color = { ...e._color }, this._rgbColor = { ...e._rgbColor };
      return;
    }
    const n = xu(e);
    if (n == null) {
      this._setNullColor();
      return;
    }
    this._color = n;
    const r = Rg(this._color);
    if (r == null) {
      this._setNullColor();
      return;
    }
    this._rgbColor = r, this._isValid = !0;
  }
  static mix(e, n, r) {
    var c, l;
    r = Math.min(1, Math.max(0, r));
    const s = new Nt(e).toRgb(), i = new Nt(n).toRgb(), o = (c = s.a) != null ? c : 1, a = (l = i.a) != null ? l : 1, u = {
      r: (i.r - s.r) * r + s.r,
      g: (i.g - s.g) * r + s.g,
      b: (i.b - s.b) * r + s.b,
      a: (a - o) * r + o
    };
    return new Nt(u);
  }
  static getContrastRatio(e, n) {
    const r = new Nt(e).getLuminance(), s = new Nt(n).getLuminance();
    return (Math.max(r, s) + 0.05) / (Math.min(r, s) + 0.05);
  }
  get isValid() {
    return this._isValid;
  }
  toRgb() {
    return this._rgbColor;
  }
  toRgbString() {
    const { r: e, g: n, b: r, a: s = 1 } = this.toRgb(), i = s < 1;
    return `rgb${i ? "a" : ""}(${e},${n},${r}${i ? `,${s}` : ""})`;
  }
  toString() {
    return this.toRgbString();
  }
  toHexString(e) {
    const { r: n, g: r, b: s, a: i = 1 } = this.toRgb(), o = i < 1, a = [
      _r(Math.round(n).toString(16)),
      _r(Math.round(r).toString(16)),
      _r(Math.round(s).toString(16)),
      _r(Math.round(i * 255).toString(16))
    ];
    return e && a[0][0] === a[0][1] && a[1][0] === a[1][1] && a[2][0] === a[2][1] && a[3][0] === a[3][1] ? o ? `#${a[0][0]}${a[1][0]}${a[2][0]}${a[3][0]}` : `#${a[0][0]}${a[1][0]}${a[2][0]}` : o ? `#${a[0]}${a[1]}${a[2]}${a[3]}` : `#${a[0]}${a[1]}${a[2]}`;
  }
  toHsv() {
    return wg(this.toRgb());
  }
  toHsl() {
    return yg(this.toRgb());
  }
  lighten(e = 10) {
    const n = this.toHsl();
    return n.l += e, n.l = Math.min(Math.max(n.l, 0), 100), new Nt(n);
  }
  darken(e = 10) {
    const n = this.toHsl();
    return n.l -= e, n.l = Math.min(Math.max(n.l, 0), 100), new Nt(n);
  }
  setAlpha(e) {
    return new Nt({ ...this._rgbColor, a: e });
  }
  getLuminance() {
    let { r: e, g: n, b: r } = this.toRgb();
    return e = bs(e), n = bs(n), r = bs(r), Number((0.2126 * e + 0.7152 * n + 0.0722 * r).toFixed(3));
  }
  getBrightness() {
    const { r: e, g: n, b: r } = this.toRgb();
    return (e * 299 + n * 587 + r * 114) / 1e3;
  }
  getAlpha() {
    var e;
    return (e = this._color.a) != null ? e : 1;
  }
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return !this.isDark();
  }
  _setNullColor() {
    this._isValid = !1, this._color = {
      r: 0,
      g: 0,
      b: 0,
      a: 0
    }, this._rgbColor = {
      r: 0,
      g: 0,
      b: 0,
      a: 0
    };
  }
}
const _r = (t) => t.length === 1 ? `0${t}` : t, bs = (t) => (t /= 255, t <= 0.03928 ? t / 12.92 : ((t + 0.055) / 1.055) ** 2.4), xu = (t) => {
  if (bg(t)) {
    if ("r" in t) {
      const r = {
        r: Math.round(t.r),
        g: Math.round(t.g),
        b: Math.round(t.b)
      };
      return t.a !== void 0 && (r.a = t.a), r;
    }
    if ("l" in t) {
      const r = {
        h: Math.round(t.h),
        s: t.s,
        l: t.l
      };
      return t.a !== void 0 && (r.a = t.a), r;
    }
    const n = {
      h: Math.round(t.h),
      s: t.s,
      v: t.v
    };
    return t.a !== void 0 && (n.a = t.a), n;
  }
  const e = t.trim();
  if (xo[e]) {
    const n = xo[e], r = {
      r: Math.round(n[0]),
      g: Math.round(n[1]),
      b: Math.round(n[2])
    };
    return r.a = n[3] || 1, r;
  }
  if (e.startsWith("#"))
    return mg(e);
  if (e.startsWith("rgb"))
    return _g(e);
  if (e.startsWith("hsl"))
    return Eg(e);
  if (e.startsWith("hsv"))
    return Cg(e);
}, mg = (t) => {
  const e = t.substring(1), n = new RegExp(`.{1,${e.length >= 6 ? 2 : 1}}`, "g");
  let r = e.match(n);
  if (!r || r.length < 3)
    throw new Error(`The color '${t}' is illegal hex color`);
  r[0].length === 1 && (r = r.map((i) => i + i));
  const s = {
    r: Number.parseInt(r[0], 16),
    g: Number.parseInt(r[1], 16),
    b: Number.parseInt(r[2], 16)
  };
  return r.length > 3 && (s.a = Number.parseInt(r[3], 16) / 255), s;
}, _g = (t) => {
  const e = t.indexOf("(");
  if (e === -1)
    throw new Error(`The color '${t}' is illegal rgb color`);
  const n = t.substring(e + 1, t.length - 1).split(",");
  if (n.length < 3)
    throw new Error(`The color '${t}' is illegal rgb color`);
  const r = {
    r: Number.parseInt(n[0], 10),
    g: Number.parseInt(n[1], 10),
    b: Number.parseInt(n[2], 10)
  };
  return n.length > 3 && (r.a = Number.parseFloat(n[3])), r;
}, Eg = (t) => {
  const e = t.indexOf("(");
  if (e === -1)
    throw new Error(`The color '${t}' is illegal hsl color`);
  const n = t.substring(e + 1, t.length - 1).split(",");
  if (n.length < 3)
    throw new Error(`The color '${t}' is illegal hsl color`);
  const r = {
    h: Number.parseInt(n[0], 10),
    s: Number.parseFloat(n[1]),
    l: Number.parseFloat(n[2])
  };
  return n.length > 3 && (r.a = Number.parseFloat(n[3])), r;
}, Cg = (t) => {
  const e = t.indexOf("(");
  if (e === -1)
    throw new Error(`The color '${t}' is illegal hsv color`);
  const n = t.substring(e + 1, t.length - 1).split(",");
  if (n.length < 3)
    throw new Error(`The color '${t}' is illegal hsv color`);
  const r = {
    h: Number.parseInt(n[0], 10),
    s: Number.parseFloat(n[1]),
    v: Number.parseFloat(n[2])
  };
  return n.length > 3 && (r.a = Number.parseFloat(n[3])), r;
}, Rg = (t) => {
  const e = xu(t);
  if (e != null)
    return "r" in e ? e : "l" in e ? Ig(e) : vg(e);
}, Ss = (t, e, n) => (n < 0 && (n += 1), n > 1 && (n -= 1), n < 1 / 6 ? t + (e - t) * 6 * n : n < 1 / 2 ? e : n < 2 / 3 ? t + (e - t) * (2 / 3 - n) * 6 : t), Ig = (t) => {
  let { h: e, s: n, l: r } = t;
  e /= 360, n /= 100, r /= 100;
  let s = 0, i = 0, o = 0;
  if (n === 0)
    s = i = o = r;
  else {
    const u = r < 0.5 ? r * (1 + n) : r + n - r * n, c = 2 * r - u;
    s = Ss(c, u, e + 1 / 3), i = Ss(c, u, e), o = Ss(c, u, e - 1 / 3);
  }
  const a = {
    r: Math.round(s * 255),
    g: Math.round(i * 255),
    b: Math.round(o * 255)
  };
  return t.a !== void 0 && (a.a = t.a), a;
}, vg = (t) => {
  let { h: e, s: n, v: r } = t;
  e = e / 360 * 6, n /= 100, r /= 100;
  const s = Math.floor(e), i = e - s, o = r * (1 - n), a = r * (1 - i * n), u = r * (1 - (1 - i) * n), c = s % 6, l = [r, a, o, o, u, r][c], h = [u, r, r, a, o, o][c], d = [o, o, u, r, r, a][c], f = {
    r: l * 255,
    g: h * 255,
    b: d * 255
  };
  return t.a !== void 0 && (f.a = t.a), f;
}, yg = (t) => {
  let { r: e, g: n, b: r } = t;
  e /= 255, n /= 255, r /= 255;
  const s = Math.max(e, n, r), i = Math.min(e, n, r), o = (s + i) / 2;
  let a, u;
  if (s === i)
    a = u = 0;
  else {
    const l = s - i;
    switch (u = o > 0.5 ? l / (2 - s - i) : l / (s + i), s) {
      case e:
        a = (n - r) / l + (n < r ? 6 : 0);
        break;
      case n:
        a = (r - e) / l + 2;
        break;
      default:
        a = (e - n) / l + 4;
        break;
    }
    a /= 6;
  }
  const c = {
    h: Math.round(a * 360),
    s: Math.round(u * 100),
    l: Math.round(o * 100)
  };
  return t.a !== void 0 && (c.a = t.a), c;
}, wg = (t) => {
  let { r: e, g: n, b: r } = t;
  e /= 255, n /= 255, r /= 255;
  const s = Math.max(e, n, r), i = Math.min(e, n, r);
  let o;
  const a = s, u = s - i, c = s === 0 ? 0 : u / s;
  if (s === i)
    o = 0;
  else {
    switch (s) {
      case e:
        o = (n - r) / u + (n < r ? 6 : 0);
        break;
      case n:
        o = (r - e) / u + 2;
        break;
      default:
        o = (e - n) / u + 4;
        break;
    }
    o /= 6;
  }
  const l = {
    h: Math.round(o * 360),
    s: Math.round(c * 100),
    v: Math.round(a * 100)
  };
  return t.a !== void 0 && (l.a = t.a), l;
}, Og = (t) => t == null, bg = (t) => !Og(t) && typeof t == "object";
function hC(t) {
  const e = /^#(?:[0]{3}|[0]{6})\b/, n = /^rgb\s*\(\s*0+\s*,\s*0+\s*,\s*0+\s*\)$/, r = /^rgba\s*\(\s*0+\s*,\s*0+\s*,\s*0+\s*,\s*(1|1\.0*|0?\.\d+)\)$/, s = /^hsl\s*\(\s*0*\s*,\s*0%*\s*,\s*0%*\s*\)$/, i = /^hsla\s*\(\s*0*\s*,\s*0%*\s*,\s*0%*\s*,\s*(1|1\.0*|0?\.\d+)\)$/;
  return !!(e.test(t) || n.test(t) || r.test(t) || s.test(t) || i.test(t));
}
function dC(t) {
  const e = /^#(?:[Ff]{3}|[Ff]{6})\b/, n = /^rgb\s*\(\s*255\s*,\s*255\s*,\s*255\s*\)$/, r = /^rgba\s*\(\s*255\s*,\s*255\s*,\s*255\s*,\s*(1|1\.0*|0?\.\d+)\)$/, s = /^hsl\s*\(\s*0*\s*,\s*0%*\s*,\s*100%*\s*\)$/, i = /^hsla\s*\(\s*0*\s*,\s*0%*\s*,\s*100%*\s*,\s*(1|1\.0*|0?\.\d+)\)$/;
  return !!(e.test(t) || n.test(t) || r.test(t) || s.test(t) || i.test(t));
}
var Pe = /* @__PURE__ */ ((t) => (t[t.COVER = 0] = "COVER", t[t.REPLACE = 1] = "REPLACE", t))(Pe || {});
function fC(t) {
  return t && (t.s !== void 0 || t.p !== void 0 || t.v !== void 0 || t.t !== void 0 || t.f !== void 0 || t.si !== void 0 || t.custom !== void 0);
}
function gC(t) {
  if (t.t !== void 0)
    return t.t;
  if (typeof t.v == "string")
    return dn.STRING;
  if (typeof t.v == "number")
    return dn.NUMBER;
  if (typeof t.v == "boolean")
    return dn.BOOLEAN;
}
function pC(t) {
  if (t == null)
    return !0;
  const { v: e, f: n, si: r, p: s, custom: i } = t;
  return !(!(e == null || typeof e == "string" && e.length === 0) || n != null && n.length > 0 || r != null && r.length > 0 || s != null || i != null);
}
function mC(t) {
  return t != null && (typeof t == "string" || typeof t == "number" || typeof t == "boolean");
}
var De = /* @__PURE__ */ ((t) => (t[t.NORMAL = 0] = "NORMAL", t[t.ROW = 1] = "ROW", t[t.COLUMN = 2] = "COLUMN", t[t.ALL = 3] = "ALL", t))(De || {}), tt = /* @__PURE__ */ ((t) => (t[t.NONE = 0] = "NONE", t[t.ROW = 1] = "ROW", t[t.COLUMN = 2] = "COLUMN", t[t.ALL = 3] = "ALL", t))(tt || {});
function _C(t) {
  return [t.startRow, t.startColumn, t.endRow, t.endColumn];
}
var Sg = /* @__PURE__ */ ((t) => (t.NONE = "none", t.BACKWARD = "backward", t.FORWARD = "forward", t))(Sg || {}), Ag = /* @__PURE__ */ ((t) => (t.RECT = "RECT", t.TEXT = "TEXT", t))(Ag || {});
function EC(t, e, n) {
  let r = !1, s = !1, i = t, o = e, a = t, u = e;
  if (n == null)
    return {
      actualRow: t,
      actualColumn: e,
      isMergedMainCell: s,
      isMerged: r,
      endRow: i,
      endColumn: o,
      startRow: a,
      startColumn: u
    };
  for (let c = 0; c < n.length; c++) {
    const {
      startRow: l,
      endRow: h,
      startColumn: d,
      endColumn: f
    } = n[c];
    if (t === l && e === d) {
      i = h, o = f, a = l, u = d, s = !0;
      break;
    }
    if (t >= l && t <= h && e >= d && e <= f) {
      i = h, o = f, a = l, u = d, r = !0;
      break;
    }
  }
  return {
    actualRow: t,
    actualColumn: e,
    isMergedMainCell: s,
    isMerged: r,
    endRow: i,
    endColumn: o,
    startRow: a,
    startColumn: u
  };
}
var zn = /* @__PURE__ */ ((t) => (t.Raw = "raw", t.Intercepted = "intercepted", t.Both = "both", t))(zn || {});
function Ng(t) {
  const { actualRow: e, actualColumn: n, isMerged: r, isMergedMainCell: s, mergeInfo: i } = t;
  let { startY: o, endY: a, startX: u, endX: c } = t, l = e, h = n, d = e, f = n;
  if (r && i) {
    const {
      startRow: E,
      startColumn: R,
      endRow: O,
      endColumn: U,
      startY: ne,
      endY: X,
      startX: de,
      endX: T
    } = i;
    l = E, h = R, d = O, f = U, o = ne, a = X, u = de, c = T;
  }
  return s && (o = i.startY, a = i.endY, u = i.startX, c = i.endX, d = i.endRow, f = i.endColumn), {
    startRow: l,
    startColumn: h,
    endRow: d,
    endColumn: f,
    startY: o,
    endY: a,
    startX: u,
    endX: c
  };
}
const CC = Ng;
function RC(t) {
  if (!t)
    return;
  const {
    actualRow: e,
    actualColumn: n,
    isMerged: r,
    isMergedMainCell: s,
    startRow: i,
    startColumn: o,
    endRow: a,
    endColumn: u
  } = t;
  let c = e, l = n, h = e, d = n;
  return (r || s) && (c = i, l = o, h = a, d = u), {
    startRow: c,
    startColumn: l,
    endRow: h,
    endColumn: d
  };
}
function Tg(t) {
  var n;
  return !t || (((n = t == null ? void 0 : t.v) == null ? void 0 : n.toString()) || "").length === 0 && !t.p;
}
function IC(t) {
  return Tg(t) && (t == null ? void 0 : t.coverable) !== !1;
}
function Lt(t) {
  if (t) {
    if (t.rgb)
      return t.rgb;
    if (t.th)
      return new gs().setThemeColor(t.th).asThemeColor().asRgbColor().getCssString();
  }
  return null;
}
function vC(t) {
  return re.isString(t) && t.substring(0, 1) === "=" && t.length > 1;
}
function yC(t) {
  return re.isString(t) && t.length > 0;
}
function wC(t, e = !1) {
  var i;
  let n = "";
  const r = /* @__PURE__ */ new Map([
    [
      "ff",
      () => {
        t.ff && (n += `font-family: ${t.ff}; `);
      }
    ],
    [
      "fs",
      () => {
        if (t.fs) {
          let o = t.fs;
          t.va && (o /= 2), n += `font-size: ${o}pt; `;
        }
      }
    ],
    [
      "it",
      () => {
        t.it && (n += "font-style: italic; ");
      }
    ],
    [
      "bl",
      () => {
        t.bl && (n += "font-weight: bold; ");
      }
    ],
    [
      "ul",
      () => {
        var o;
        (o = t.ul) != null && o.s && (n.indexOf("text-decoration-line") > -1 ? n = n.replace(/(text-decoration-line:\s*[^;]+)(?=;)/g, (a, u) => `${u} underline`) : n += "text-decoration: underline; ", t.ul.cl && n.indexOf("text-decoration-color") === -1 && (n += `text-decoration-color: ${Lt(t.ul.cl)}; `), t.ul.t && n.indexOf("text-decoration-style") === -1 && (n += `text-decoration-style: ${t.ul.t} `));
      }
    ],
    [
      "st",
      () => {
        var o;
        (o = t.st) != null && o.s && (n.indexOf("text-decoration-line") > -1 ? n = n.replace(/(text-decoration-line:\s*[^;]+)(?=;)/g, (a, u) => `${u} line-through`) : n += "text-decoration-line: line-through; ", t.st.cl && n.indexOf("text-decoration-color") === -1 && (n += `text-decoration-color: ${Lt(t.st.cl)}; `), t.st.t && n.indexOf("text-decoration-style") === -1 && (n += `text-decoration-style: ${t.st.t} `));
      }
    ],
    [
      "ol",
      () => {
        var o;
        (o = t.ol) != null && o.s && (n.indexOf("text-decoration-line") > -1 ? n = n.replace(/(text-decoration-line:\s*[^;]+)(?=;)/g, (a, u) => `${u} overline`) : n += "text-decoration-line: overline; ", t.ol.cl && n.indexOf("text-decoration-color") === -1 && (n += `text-decoration-color: ${Lt(t.ol.cl)}; `), t.ol.t && n.indexOf("text-decoration-style") === -1 && (n += `text-decoration-style: ${t.ol.t} `));
      }
    ],
    [
      "bg",
      () => {
        t.bg && (n += `background: ${Lt(t.bg)}; `);
      }
    ],
    [
      "bd",
      () => {
        var o, a, u, c, l, h, d, f, E, R, O, U;
        (o = t.bd) != null && o.b && (n += `border-bottom: ${Er((a = t.bd) == null ? void 0 : a.b.s)} ${(u = Lt(t.bd.b.cl)) != null ? u : ""}; `), (c = t.bd) != null && c.t && (n += `border-top: ${Er((l = t.bd) == null ? void 0 : l.t.s)} ${(h = Lt(t.bd.t.cl)) != null ? h : ""}; `), (d = t.bd) != null && d.r && (n += `border-right: ${Er((f = t.bd) == null ? void 0 : f.r.s)} ${(E = Lt(t.bd.r.cl)) != null ? E : ""}; `), (R = t.bd) != null && R.l && (n += `border-left: ${Er((O = t.bd) == null ? void 0 : O.l.s)} ${(U = Lt(t.bd.l.cl)) != null ? U : ""}; `);
      }
    ],
    [
      "cl",
      () => {
        t.cl && (n += `color: ${Lt(t.cl)}; `);
      }
    ],
    [
      "va",
      () => {
        t.va === Bt.SUBSCRIPT ? n += "vertical-align: sub; " : t.va === Bt.SUPERSCRIPT && (n += "vertical-align: super; ");
      }
    ],
    [
      "td",
      () => {
        t.td === er.LEFT_TO_RIGHT ? n += "direction: ltr; " : t.td === er.RIGHT_TO_LEFT && (n += "direction: rtl; ");
      }
    ],
    [
      "tr",
      () => {
        var o, a, u;
        t.tr && (n += `--data-rotate: (${(o = t.tr) == null ? void 0 : o.a}deg${(a = t.tr) != null && a.v ? ` ,${(u = t.tr) == null ? void 0 : u.v}` : ""});`);
      }
    ],
    [
      "ht",
      () => {
        t.ht === Xt.LEFT ? n += "text-align: left; " : t.ht === Xt.RIGHT ? n += "text-align: right; " : t.ht === Xt.CENTER ? n += "text-align: center; " : t.ht === Xt.JUSTIFIED && (n += "text-align: justify; ");
      }
    ],
    [
      "vt",
      () => {
        t.vt === hn.BOTTOM ? n += "vertical-align: bottom; " : t.vt === hn.TOP ? n += "vertical-align: top; " : t.vt === hn.MIDDLE && (n += "vertical-align: middle; ");
      }
    ],
    [
      "tb",
      () => {
        t.tb === xn.CLIP ? n += "white-space: nowrap; overflow-x: hidden; " : t.tb === xn.WRAP && (n += "white-space: normal;");
      }
    ],
    [
      "pd",
      () => {
        var l, h, d, f, E, R, O, U;
        const o = `${(l = t.pd) == null ? void 0 : l.b}pt`, a = `${(h = t.pd) == null ? void 0 : h.t}pt`, u = `${(d = t.pd) == null ? void 0 : d.l}pt`, c = `${(f = t.pd) == null ? void 0 : f.r}pt`;
        (E = t.pd) != null && E.b && (n += `padding-bottom: ${o}; `), (R = t.pd) != null && R.t && (n += `padding-top: ${a}; `), (O = t.pd) != null && O.l && (n += `padding-left: ${u}; `), (U = t.pd) != null && U.r && (n += `padding-right: ${c}; `);
      }
    ]
  ]), s = ["bd", "tr", "tb"];
  for (const o in t)
    e && s.includes(o) || (i = r.get(o)) == null || i();
  return n;
}
function Er(t) {
  let e = "";
  return t === Xe.NONE ? e = "none" : t === Xe.THIN ? e = "0.5pt solid" : t === Xe.HAIR ? e = "0.5pt double" : t === Xe.DOTTED ? e = "0.5pt dotted" : t === Xe.DASHED || t === Xe.DASH_DOT ? e = "0.5pt dashed" : t === Xe.DASH_DOT_DOT ? e = "0.5pt dotted" : t === Xe.DOUBLE ? e = "0.5pt double" : t === Xe.MEDIUM ? e = "1pt solid" : t === Xe.MEDIUM_DASHED || t === Xe.MEDIUM_DASH_DOT ? e = "1pt dashed" : t === Xe.MEDIUM_DASH_DOT_DOT ? e = "1pt dotted" : t === Xe.SLANT_DASH_DOT ? e = "0.5pt dashed" : t === Xe.THICK && (e = "1.5pt solid"), e;
}
function OC(t) {
  let e = 0;
  if (t = t.trim(), t === "none")
    e = Xe.NONE;
  else if (t === "0.5pt solid")
    e = Xe.THIN;
  else if (t === "0.5pt double")
    e = Xe.HAIR;
  else if (t === "0.5pt dotted")
    e = Xe.DOTTED;
  else if (t === "0.5pt dashed")
    e = Xe.DASHED;
  else if (t === "1pt solid")
    e = Xe.MEDIUM;
  else if (t === "1pt dashed")
    e = Xe.MEDIUM_DASHED;
  else if (t === "1pt dotted")
    e = Xe.MEDIUM_DASH_DOT_DOT;
  else if (t === "1.5pt solid")
    e = Xe.THICK;
  else if (!t.includes("none"))
    e = Xe.THIN;
  else
    return Xe.NONE;
  return e;
}
function bC(t, e) {
  let n = t.body;
  if (e) {
    const { headers: r, footers: s } = t;
    r != null && r[e] ? n = r[e].body : s != null && s[e] && (n = s[e].body);
  }
  return n;
}
function SC(t, e) {
  const { startRow: n, endRow: r, startColumn: s, endColumn: i, rangeType: o } = t;
  if (n < 0 || s < 0 || r < 0 || i < 0 || !(Number.isNaN(n) && Number.isNaN(r)) && o === De.COLUMN || !(Number.isNaN(s) && Number.isNaN(i)) && o === De.ROW || o !== De.ROW && o !== De.COLUMN && (Number.isNaN(s) || Number.isNaN(n) || Number.isNaN(i) || Number.isNaN(r)))
    return !1;
  if (e) {
    const a = e.getRowCount(), u = e.getColumnCount();
    if (r >= a || i >= u)
      return !1;
  }
  return !0;
}
function AC(t, e) {
  return { startRow: t, endRow: t, startColumn: e, endColumn: e };
}
function Lu(t, e) {
  return Object.prototype.toString.call(t) === Object.prototype.toString.call(e) ? Object.prototype.toString.call(t) === "[object Object]" || Object.prototype.toString.call(t) === "[object Array]" ? Object.keys(t).length !== Object.keys(e).length ? !1 : Object.keys(t).every((n) => Lu(t[n], e[n])) : t === e : !1;
}
function Mg(t, e) {
  const n = t.ts || {}, r = e.ts || {};
  return t.sId !== e.sId ? !1 : Lu(n, r);
}
function NC(t, e) {
  return e.some((n) => t.indexOf(n) > -1);
}
var Pr = { exports: {} }, Dg = Pr.exports, Lo;
function xg() {
  return Lo || (Lo = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(Dg, function() {
      var n = 1e3, r = 6e4, s = 36e5, i = "millisecond", o = "second", a = "minute", u = "hour", c = "day", l = "week", h = "month", d = "quarter", f = "year", E = "date", R = "Invalid Date", O = /^(\d{4})[-/]?(\d{1,2})?[-/]?(\d{0,2})[Tt\s]*(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?[.:]?(\d+)?$/, U = /\[([^\]]+)]|Y{1,4}|M{1,4}|D{1,2}|d{1,4}|H{1,2}|h{1,2}|a|A|m{1,2}|s{1,2}|Z{1,2}|SSS/g, ne = { name: "en", weekdays: "Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"), months: "January_February_March_April_May_June_July_August_September_October_November_December".split("_"), ordinal: function(M) {
        var b = ["th", "st", "nd", "rd"], w = M % 100;
        return "[" + M + (b[(w - 20) % 10] || b[w] || b[0]) + "]";
      } }, X = function(M, b, w) {
        var k = String(M);
        return !k || k.length >= b ? M : "" + Array(b + 1 - k.length).join(w) + M;
      }, de = { s: X, z: function(M) {
        var b = -M.utcOffset(), w = Math.abs(b), k = Math.floor(w / 60), $ = w % 60;
        return (b <= 0 ? "+" : "-") + X(k, 2, "0") + ":" + X($, 2, "0");
      }, m: function M(b, w) {
        if (b.date() < w.date()) return -M(w, b);
        var k = 12 * (w.year() - b.year()) + (w.month() - b.month()), $ = b.clone().add(k, h), Y = w - $ < 0, se = b.clone().add(k + (Y ? -1 : 1), h);
        return +(-(k + (w - $) / (Y ? $ - se : se - $)) || 0);
      }, a: function(M) {
        return M < 0 ? Math.ceil(M) || 0 : Math.floor(M);
      }, p: function(M) {
        return { M: h, y: f, w: l, d: c, D: E, h: u, m: a, s: o, ms: i, Q: d }[M] || String(M || "").toLowerCase().replace(/s$/, "");
      }, u: function(M) {
        return M === void 0;
      } }, T = "en", A = {};
      A[T] = ne;
      var H = "$isDayjsObject", Z = function(M) {
        return M instanceof j || !(!M || !M[H]);
      }, fe = function M(b, w, k) {
        var $;
        if (!b) return T;
        if (typeof b == "string") {
          var Y = b.toLowerCase();
          A[Y] && ($ = Y), w && (A[Y] = w, $ = Y);
          var se = b.split("-");
          if (!$ && se.length > 1) return M(se[0]);
        } else {
          var he = b.name;
          A[he] = b, $ = he;
        }
        return !k && $ && (T = $), $ || !k && T;
      }, ae = function(M, b) {
        if (Z(M)) return M.clone();
        var w = typeof b == "object" ? b : {};
        return w.date = M, w.args = arguments, new j(w);
      }, m = de;
      m.l = fe, m.i = Z, m.w = function(M, b) {
        return ae(M, { locale: b.$L, utc: b.$u, x: b.$x, $offset: b.$offset });
      };
      var j = function() {
        function M(w) {
          this.$L = fe(w.locale, null, !0), this.parse(w), this.$x = this.$x || w.x || {}, this[H] = !0;
        }
        var b = M.prototype;
        return b.parse = function(w) {
          this.$d = function(k) {
            var $ = k.date, Y = k.utc;
            if ($ === null) return /* @__PURE__ */ new Date(NaN);
            if (m.u($)) return /* @__PURE__ */ new Date();
            if ($ instanceof Date) return new Date($);
            if (typeof $ == "string" && !/Z$/i.test($)) {
              var se = $.match(O);
              if (se) {
                var he = se[2] - 1 || 0, ge = (se[7] || "0").substring(0, 3);
                return Y ? new Date(Date.UTC(se[1], he, se[3] || 1, se[4] || 0, se[5] || 0, se[6] || 0, ge)) : new Date(se[1], he, se[3] || 1, se[4] || 0, se[5] || 0, se[6] || 0, ge);
              }
            }
            return new Date($);
          }(w), this.init();
        }, b.init = function() {
          var w = this.$d;
          this.$y = w.getFullYear(), this.$M = w.getMonth(), this.$D = w.getDate(), this.$W = w.getDay(), this.$H = w.getHours(), this.$m = w.getMinutes(), this.$s = w.getSeconds(), this.$ms = w.getMilliseconds();
        }, b.$utils = function() {
          return m;
        }, b.isValid = function() {
          return this.$d.toString() !== R;
        }, b.isSame = function(w, k) {
          var $ = ae(w);
          return this.startOf(k) <= $ && $ <= this.endOf(k);
        }, b.isAfter = function(w, k) {
          return ae(w) < this.startOf(k);
        }, b.isBefore = function(w, k) {
          return this.endOf(k) < ae(w);
        }, b.$g = function(w, k, $) {
          return m.u(w) ? this[k] : this.set($, w);
        }, b.unix = function() {
          return Math.floor(this.valueOf() / 1e3);
        }, b.valueOf = function() {
          return this.$d.getTime();
        }, b.startOf = function(w, k) {
          var $ = this, Y = !!m.u(k) || k, se = m.p(w), he = function(z, W) {
            var ue = m.w($.$u ? Date.UTC($.$y, W, z) : new Date($.$y, W, z), $);
            return Y ? ue : ue.endOf(c);
          }, ge = function(z, W) {
            return m.w($.toDate()[z].apply($.toDate("s"), (Y ? [0, 0, 0, 0] : [23, 59, 59, 999]).slice(W)), $);
          }, Ae = this.$W, be = this.$M, v = this.$D, F = "set" + (this.$u ? "UTC" : "");
          switch (se) {
            case f:
              return Y ? he(1, 0) : he(31, 11);
            case h:
              return Y ? he(1, be) : he(0, be + 1);
            case l:
              var V = this.$locale().weekStart || 0, K = (Ae < V ? Ae + 7 : Ae) - V;
              return he(Y ? v - K : v + (6 - K), be);
            case c:
            case E:
              return ge(F + "Hours", 0);
            case u:
              return ge(F + "Minutes", 1);
            case a:
              return ge(F + "Seconds", 2);
            case o:
              return ge(F + "Milliseconds", 3);
            default:
              return this.clone();
          }
        }, b.endOf = function(w) {
          return this.startOf(w, !1);
        }, b.$set = function(w, k) {
          var $, Y = m.p(w), se = "set" + (this.$u ? "UTC" : ""), he = ($ = {}, $[c] = se + "Date", $[E] = se + "Date", $[h] = se + "Month", $[f] = se + "FullYear", $[u] = se + "Hours", $[a] = se + "Minutes", $[o] = se + "Seconds", $[i] = se + "Milliseconds", $)[Y], ge = Y === c ? this.$D + (k - this.$W) : k;
          if (Y === h || Y === f) {
            var Ae = this.clone().set(E, 1);
            Ae.$d[he](ge), Ae.init(), this.$d = Ae.set(E, Math.min(this.$D, Ae.daysInMonth())).$d;
          } else he && this.$d[he](ge);
          return this.init(), this;
        }, b.set = function(w, k) {
          return this.clone().$set(w, k);
        }, b.get = function(w) {
          return this[m.p(w)]();
        }, b.add = function(w, k) {
          var $, Y = this;
          w = Number(w);
          var se = m.p(k), he = function(be) {
            var v = ae(Y);
            return m.w(v.date(v.date() + Math.round(be * w)), Y);
          };
          if (se === h) return this.set(h, this.$M + w);
          if (se === f) return this.set(f, this.$y + w);
          if (se === c) return he(1);
          if (se === l) return he(7);
          var ge = ($ = {}, $[a] = r, $[u] = s, $[o] = n, $)[se] || 1, Ae = this.$d.getTime() + w * ge;
          return m.w(Ae, this);
        }, b.subtract = function(w, k) {
          return this.add(-1 * w, k);
        }, b.format = function(w) {
          var k = this, $ = this.$locale();
          if (!this.isValid()) return $.invalidDate || R;
          var Y = w || "YYYY-MM-DDTHH:mm:ssZ", se = m.z(this), he = this.$H, ge = this.$m, Ae = this.$M, be = $.weekdays, v = $.months, F = $.meridiem, V = function(W, ue, oe, B) {
            return W && (W[ue] || W(k, Y)) || oe[ue].slice(0, B);
          }, K = function(W) {
            return m.s(he % 12 || 12, W, "0");
          }, z = F || function(W, ue, oe) {
            var B = W < 12 ? "AM" : "PM";
            return oe ? B.toLowerCase() : B;
          };
          return Y.replace(U, function(W, ue) {
            return ue || function(oe) {
              switch (oe) {
                case "YY":
                  return String(k.$y).slice(-2);
                case "YYYY":
                  return m.s(k.$y, 4, "0");
                case "M":
                  return Ae + 1;
                case "MM":
                  return m.s(Ae + 1, 2, "0");
                case "MMM":
                  return V($.monthsShort, Ae, v, 3);
                case "MMMM":
                  return V(v, Ae);
                case "D":
                  return k.$D;
                case "DD":
                  return m.s(k.$D, 2, "0");
                case "d":
                  return String(k.$W);
                case "dd":
                  return V($.weekdaysMin, k.$W, be, 2);
                case "ddd":
                  return V($.weekdaysShort, k.$W, be, 3);
                case "dddd":
                  return be[k.$W];
                case "H":
                  return String(he);
                case "HH":
                  return m.s(he, 2, "0");
                case "h":
                  return K(1);
                case "hh":
                  return K(2);
                case "a":
                  return z(he, ge, !0);
                case "A":
                  return z(he, ge, !1);
                case "m":
                  return String(ge);
                case "mm":
                  return m.s(ge, 2, "0");
                case "s":
                  return String(k.$s);
                case "ss":
                  return m.s(k.$s, 2, "0");
                case "SSS":
                  return m.s(k.$ms, 3, "0");
                case "Z":
                  return se;
              }
              return null;
            }(W) || se.replace(":", "");
          });
        }, b.utcOffset = function() {
          return 15 * -Math.round(this.$d.getTimezoneOffset() / 15);
        }, b.diff = function(w, k, $) {
          var Y, se = this, he = m.p(k), ge = ae(w), Ae = (ge.utcOffset() - this.utcOffset()) * r, be = this - ge, v = function() {
            return m.m(se, ge);
          };
          switch (he) {
            case f:
              Y = v() / 12;
              break;
            case h:
              Y = v();
              break;
            case d:
              Y = v() / 3;
              break;
            case l:
              Y = (be - Ae) / 6048e5;
              break;
            case c:
              Y = (be - Ae) / 864e5;
              break;
            case u:
              Y = be / s;
              break;
            case a:
              Y = be / r;
              break;
            case o:
              Y = be / n;
              break;
            default:
              Y = be;
          }
          return $ ? Y : m.a(Y);
        }, b.daysInMonth = function() {
          return this.endOf(h).$D;
        }, b.$locale = function() {
          return A[this.$L];
        }, b.locale = function(w, k) {
          if (!w) return this.$L;
          var $ = this.clone(), Y = fe(w, k, !0);
          return Y && ($.$L = Y), $;
        }, b.clone = function() {
          return m.w(this.$d, this);
        }, b.toDate = function() {
          return new Date(this.valueOf());
        }, b.toJSON = function() {
          return this.isValid() ? this.toISOString() : null;
        }, b.toISOString = function() {
          return this.$d.toISOString();
        }, b.toString = function() {
          return this.$d.toUTCString();
        }, M;
      }(), y = j.prototype;
      return ae.prototype = y, [["$ms", i], ["$s", o], ["$m", a], ["$H", u], ["$W", c], ["$M", h], ["$y", f], ["$D", E]].forEach(function(M) {
        y[M[1]] = function(b) {
          return this.$g(b, M[0], M[1]);
        };
      }), ae.extend = function(M, b) {
        return M.$i || (M(b, j, ae), M.$i = !0), ae;
      }, ae.locale = fe, ae.isDayjs = Z, ae.unix = function(M) {
        return ae(1e3 * M);
      }, ae.en = A[T], ae.Ls = A, ae.p = {}, ae;
    });
  }(Pr)), Pr.exports;
}
var Lg = xg();
const rn = /* @__PURE__ */ wt(Lg);
var kr = { exports: {} }, Ug = kr.exports, Uo;
function Pg() {
  return Uo || (Uo = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(Ug, function() {
      return function(n, r) {
        var s = r.prototype, i = s.format;
        s.format = function(o) {
          var a = this, u = this.$locale();
          if (!this.isValid()) return i.bind(this)(o);
          var c = this.$utils(), l = (o || "YYYY-MM-DDTHH:mm:ssZ").replace(/\[([^\]]+)]|Q|wo|ww|w|WW|W|zzz|z|gggg|GGGG|Do|X|x|k{1,2}|S/g, function(h) {
            switch (h) {
              case "Q":
                return Math.ceil((a.$M + 1) / 3);
              case "Do":
                return u.ordinal(a.$D);
              case "gggg":
                return a.weekYear();
              case "GGGG":
                return a.isoWeekYear();
              case "wo":
                return u.ordinal(a.week(), "W");
              case "w":
              case "ww":
                return c.s(a.week(), h === "w" ? 1 : 2, "0");
              case "W":
              case "WW":
                return c.s(a.isoWeek(), h === "W" ? 1 : 2, "0");
              case "k":
              case "kk":
                return c.s(String(a.$H === 0 ? 24 : a.$H), h === "k" ? 1 : 2, "0");
              case "X":
                return Math.floor(a.$d.getTime() / 1e3);
              case "x":
                return a.$d.getTime();
              case "z":
                return "[" + a.offsetName() + "]";
              case "zzz":
                return "[" + a.offsetName("long") + "]";
              default:
                return h;
            }
          });
          return i.bind(this)(l);
        };
      };
    });
  }(kr)), kr.exports;
}
var kg = Pg();
const Fg = /* @__PURE__ */ wt(kg);
var Fr = { exports: {} }, $g = Fr.exports, Po;
function Bg() {
  return Po || (Po = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })($g, function() {
      var n = { LTS: "h:mm:ss A", LT: "h:mm A", L: "MM/DD/YYYY", LL: "MMMM D, YYYY", LLL: "MMMM D, YYYY h:mm A", LLLL: "dddd, MMMM D, YYYY h:mm A" }, r = /(\[[^[]*\])|([-_:/.,()\s]+)|(A|a|Q|YYYY|YY?|ww?|MM?M?M?|Do|DD?|hh?|HH?|mm?|ss?|S{1,3}|z|ZZ?)/g, s = /\d/, i = /\d\d/, o = /\d\d?/, a = /\d*[^-_:/,()\s\d]+/, u = {}, c = function(O) {
        return (O = +O) + (O > 68 ? 1900 : 2e3);
      }, l = function(O) {
        return function(U) {
          this[O] = +U;
        };
      }, h = [/[+-]\d\d:?(\d\d)?|Z/, function(O) {
        (this.zone || (this.zone = {})).offset = function(U) {
          if (!U || U === "Z") return 0;
          var ne = U.match(/([+-]|\d\d)/g), X = 60 * ne[1] + (+ne[2] || 0);
          return X === 0 ? 0 : ne[0] === "+" ? -X : X;
        }(O);
      }], d = function(O) {
        var U = u[O];
        return U && (U.indexOf ? U : U.s.concat(U.f));
      }, f = function(O, U) {
        var ne, X = u.meridiem;
        if (X) {
          for (var de = 1; de <= 24; de += 1) if (O.indexOf(X(de, 0, U)) > -1) {
            ne = de > 12;
            break;
          }
        } else ne = O === (U ? "pm" : "PM");
        return ne;
      }, E = { A: [a, function(O) {
        this.afternoon = f(O, !1);
      }], a: [a, function(O) {
        this.afternoon = f(O, !0);
      }], Q: [s, function(O) {
        this.month = 3 * (O - 1) + 1;
      }], S: [s, function(O) {
        this.milliseconds = 100 * +O;
      }], SS: [i, function(O) {
        this.milliseconds = 10 * +O;
      }], SSS: [/\d{3}/, function(O) {
        this.milliseconds = +O;
      }], s: [o, l("seconds")], ss: [o, l("seconds")], m: [o, l("minutes")], mm: [o, l("minutes")], H: [o, l("hours")], h: [o, l("hours")], HH: [o, l("hours")], hh: [o, l("hours")], D: [o, l("day")], DD: [i, l("day")], Do: [a, function(O) {
        var U = u.ordinal, ne = O.match(/\d+/);
        if (this.day = ne[0], U) for (var X = 1; X <= 31; X += 1) U(X).replace(/\[|\]/g, "") === O && (this.day = X);
      }], w: [o, l("week")], ww: [i, l("week")], M: [o, l("month")], MM: [i, l("month")], MMM: [a, function(O) {
        var U = d("months"), ne = (d("monthsShort") || U.map(function(X) {
          return X.slice(0, 3);
        })).indexOf(O) + 1;
        if (ne < 1) throw new Error();
        this.month = ne % 12 || ne;
      }], MMMM: [a, function(O) {
        var U = d("months").indexOf(O) + 1;
        if (U < 1) throw new Error();
        this.month = U % 12 || U;
      }], Y: [/[+-]?\d+/, l("year")], YY: [i, function(O) {
        this.year = c(O);
      }], YYYY: [/\d{4}/, l("year")], Z: h, ZZ: h };
      function R(O) {
        var U, ne;
        U = O, ne = u && u.formats;
        for (var X = (O = U.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g, function(ae, m, j) {
          var y = j && j.toUpperCase();
          return m || ne[j] || n[j] || ne[y].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g, function(M, b, w) {
            return b || w.slice(1);
          });
        })).match(r), de = X.length, T = 0; T < de; T += 1) {
          var A = X[T], H = E[A], Z = H && H[0], fe = H && H[1];
          X[T] = fe ? { regex: Z, parser: fe } : A.replace(/^\[|\]$/g, "");
        }
        return function(ae) {
          for (var m = {}, j = 0, y = 0; j < de; j += 1) {
            var M = X[j];
            if (typeof M == "string") y += M.length;
            else {
              var b = M.regex, w = M.parser, k = ae.slice(y), $ = b.exec(k)[0];
              w.call(m, $), ae = ae.replace($, "");
            }
          }
          return function(Y) {
            var se = Y.afternoon;
            if (se !== void 0) {
              var he = Y.hours;
              se ? he < 12 && (Y.hours += 12) : he === 12 && (Y.hours = 0), delete Y.afternoon;
            }
          }(m), m;
        };
      }
      return function(O, U, ne) {
        ne.p.customParseFormat = !0, O && O.parseTwoDigitYear && (c = O.parseTwoDigitYear);
        var X = U.prototype, de = X.parse;
        X.parse = function(T) {
          var A = T.date, H = T.utc, Z = T.args;
          this.$u = H;
          var fe = Z[1];
          if (typeof fe == "string") {
            var ae = Z[2] === !0, m = Z[3] === !0, j = ae || m, y = Z[2];
            m && (y = Z[2]), u = this.$locale(), !ae && y && (u = ne.Ls[y]), this.$d = function(k, $, Y, se) {
              try {
                if (["x", "X"].indexOf($) > -1) return new Date(($ === "X" ? 1e3 : 1) * k);
                var he = R($)(k), ge = he.year, Ae = he.month, be = he.day, v = he.hours, F = he.minutes, V = he.seconds, K = he.milliseconds, z = he.zone, W = he.week, ue = /* @__PURE__ */ new Date(), oe = be || (ge || Ae ? 1 : ue.getDate()), B = ge || ue.getFullYear(), ee = 0;
                ge && !Ae || (ee = Ae > 0 ? Ae - 1 : ue.getMonth());
                var ie, pe = v || 0, Oe = F || 0, Me = V || 0, G = K || 0;
                return z ? new Date(Date.UTC(B, ee, oe, pe, Oe, Me, G + 60 * z.offset * 1e3)) : Y ? new Date(Date.UTC(B, ee, oe, pe, Oe, Me, G)) : (ie = new Date(B, ee, oe, pe, Oe, Me, G), W && (ie = se(ie).week(W).toDate()), ie);
              } catch {
                return /* @__PURE__ */ new Date("");
              }
            }(A, fe, H, ne), this.init(), y && y !== !0 && (this.$L = this.locale(y).$L), j && A != this.format(fe) && (this.$d = /* @__PURE__ */ new Date("")), u = {};
          } else if (fe instanceof Array) for (var M = fe.length, b = 1; b <= M; b += 1) {
            Z[1] = fe[b - 1];
            var w = ne.apply(this, Z);
            if (w.isValid()) {
              this.$d = w.$d, this.$L = w.$L, this.init();
              break;
            }
            b === M && (this.$d = /* @__PURE__ */ new Date(""));
          }
          else de.call(this, T);
        };
      };
    });
  }(Fr)), Fr.exports;
}
var jg = Bg();
const Hg = /* @__PURE__ */ wt(jg);
var $r = { exports: {} }, Wg = $r.exports, ko;
function zg() {
  return ko || (ko = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(Wg, function() {
      return function(n, r, s) {
        var i = r.prototype, o = function(h) {
          return h && (h.indexOf ? h : h.s);
        }, a = function(h, d, f, E, R) {
          var O = h.name ? h : h.$locale(), U = o(O[d]), ne = o(O[f]), X = U || ne.map(function(T) {
            return T.slice(0, E);
          });
          if (!R) return X;
          var de = O.weekStart;
          return X.map(function(T, A) {
            return X[(A + (de || 0)) % 7];
          });
        }, u = function() {
          return s.Ls[s.locale()];
        }, c = function(h, d) {
          return h.formats[d] || function(f) {
            return f.replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g, function(E, R, O) {
              return R || O.slice(1);
            });
          }(h.formats[d.toUpperCase()]);
        }, l = function() {
          var h = this;
          return { months: function(d) {
            return d ? d.format("MMMM") : a(h, "months");
          }, monthsShort: function(d) {
            return d ? d.format("MMM") : a(h, "monthsShort", "months", 3);
          }, firstDayOfWeek: function() {
            return h.$locale().weekStart || 0;
          }, weekdays: function(d) {
            return d ? d.format("dddd") : a(h, "weekdays");
          }, weekdaysMin: function(d) {
            return d ? d.format("dd") : a(h, "weekdaysMin", "weekdays", 2);
          }, weekdaysShort: function(d) {
            return d ? d.format("ddd") : a(h, "weekdaysShort", "weekdays", 3);
          }, longDateFormat: function(d) {
            return c(h.$locale(), d);
          }, meridiem: this.$locale().meridiem, ordinal: this.$locale().ordinal };
        };
        i.localeData = function() {
          return l.bind(this)();
        }, s.localeData = function() {
          var h = u();
          return { firstDayOfWeek: function() {
            return h.weekStart || 0;
          }, weekdays: function() {
            return s.weekdays();
          }, weekdaysShort: function() {
            return s.weekdaysShort();
          }, weekdaysMin: function() {
            return s.weekdaysMin();
          }, months: function() {
            return s.months();
          }, monthsShort: function() {
            return s.monthsShort();
          }, longDateFormat: function(d) {
            return c(h, d);
          }, meridiem: h.meridiem, ordinal: h.ordinal };
        }, s.months = function() {
          return a(u(), "months");
        }, s.monthsShort = function() {
          return a(u(), "monthsShort", "months", 3);
        }, s.weekdays = function(h) {
          return a(u(), "weekdays", null, null, h);
        }, s.weekdaysShort = function(h) {
          return a(u(), "weekdaysShort", "weekdays", 3, h);
        }, s.weekdaysMin = function(h) {
          return a(u(), "weekdaysMin", "weekdays", 2, h);
        };
      };
    });
  }($r)), $r.exports;
}
var Yg = zg();
const Vg = /* @__PURE__ */ wt(Yg);
var Br = { exports: {} }, Gg = Br.exports, Fo;
function Kg() {
  return Fo || (Fo = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(Gg, function() {
      var n = { LTS: "h:mm:ss A", LT: "h:mm A", L: "MM/DD/YYYY", LL: "MMMM D, YYYY", LLL: "MMMM D, YYYY h:mm A", LLLL: "dddd, MMMM D, YYYY h:mm A" };
      return function(r, s, i) {
        var o = s.prototype, a = o.format;
        i.en.formats = n, o.format = function(u) {
          u === void 0 && (u = "YYYY-MM-DDTHH:mm:ssZ");
          var c = this.$locale().formats, l = function(h, d) {
            return h.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g, function(f, E, R) {
              var O = R && R.toUpperCase();
              return E || d[R] || n[R] || d[O].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g, function(U, ne, X) {
                return ne || X.slice(1);
              });
            });
          }(u, c === void 0 ? {} : c);
          return a.call(this, l);
        };
      };
    });
  }(Br)), Br.exports;
}
var Xg = Kg();
const Jg = /* @__PURE__ */ wt(Xg);
var jr = { exports: {} }, Zg = jr.exports, $o;
function Qg() {
  return $o || ($o = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(Zg, function() {
      var n = "minute", r = /[+-]\d\d(?::?\d\d)?/g, s = /([+-]|\d\d)/g;
      return function(i, o, a) {
        var u = o.prototype;
        a.utc = function(R) {
          var O = { date: R, utc: !0, args: arguments };
          return new o(O);
        }, u.utc = function(R) {
          var O = a(this.toDate(), { locale: this.$L, utc: !0 });
          return R ? O.add(this.utcOffset(), n) : O;
        }, u.local = function() {
          return a(this.toDate(), { locale: this.$L, utc: !1 });
        };
        var c = u.parse;
        u.parse = function(R) {
          R.utc && (this.$u = !0), this.$utils().u(R.$offset) || (this.$offset = R.$offset), c.call(this, R);
        };
        var l = u.init;
        u.init = function() {
          if (this.$u) {
            var R = this.$d;
            this.$y = R.getUTCFullYear(), this.$M = R.getUTCMonth(), this.$D = R.getUTCDate(), this.$W = R.getUTCDay(), this.$H = R.getUTCHours(), this.$m = R.getUTCMinutes(), this.$s = R.getUTCSeconds(), this.$ms = R.getUTCMilliseconds();
          } else l.call(this);
        };
        var h = u.utcOffset;
        u.utcOffset = function(R, O) {
          var U = this.$utils().u;
          if (U(R)) return this.$u ? 0 : U(this.$offset) ? h.call(this) : this.$offset;
          if (typeof R == "string" && (R = function(T) {
            T === void 0 && (T = "");
            var A = T.match(r);
            if (!A) return null;
            var H = ("" + A[0]).match(s) || ["-", 0, 0], Z = H[0], fe = 60 * +H[1] + +H[2];
            return fe === 0 ? 0 : Z === "+" ? fe : -fe;
          }(R), R === null)) return this;
          var ne = Math.abs(R) <= 16 ? 60 * R : R, X = this;
          if (O) return X.$offset = ne, X.$u = R === 0, X;
          if (R !== 0) {
            var de = this.$u ? this.toDate().getTimezoneOffset() : -1 * this.utcOffset();
            (X = this.local().add(ne + de, n)).$offset = ne, X.$x.$localOffset = de;
          } else X = this.utc();
          return X;
        };
        var d = u.format;
        u.format = function(R) {
          var O = R || (this.$u ? "YYYY-MM-DDTHH:mm:ss[Z]" : "");
          return d.call(this, O);
        }, u.valueOf = function() {
          var R = this.$utils().u(this.$offset) ? 0 : this.$offset + (this.$x.$localOffset || this.$d.getTimezoneOffset());
          return this.$d.valueOf() - 6e4 * R;
        }, u.isUTC = function() {
          return !!this.$u;
        }, u.toISOString = function() {
          return this.toDate().toISOString();
        }, u.toString = function() {
          return this.toDate().toUTCString();
        };
        var f = u.toDate;
        u.toDate = function(R) {
          return R === "s" && this.$offset ? a(this.format("YYYY-MM-DD HH:mm:ss:SSS")).toDate() : f.call(this);
        };
        var E = u.diff;
        u.diff = function(R, O, U) {
          if (R && this.$u === R.$u) return E.call(this, R, O, U);
          var ne = this.local(), X = a(R).local();
          return E.call(ne, X, O, U);
        };
      };
    });
  }(jr)), jr.exports;
}
var qg = Qg();
const ep = /* @__PURE__ */ wt(qg);
var Hr = { exports: {} }, tp = Hr.exports, Bo;
function np() {
  return Bo || (Bo = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(tp, function() {
      return function(n, r) {
        r.prototype.weekday = function(s) {
          var i = this.$locale().weekStart || 0, o = this.$W, a = (o < i ? o + 7 : o) - i;
          return this.$utils().u(s) ? a : this.subtract(a, "day").add(s, "day");
        };
      };
    });
  }(Hr)), Hr.exports;
}
var rp = np();
const sp = /* @__PURE__ */ wt(rp);
var Wr = { exports: {} }, ip = Wr.exports, jo;
function op() {
  return jo || (jo = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(ip, function() {
      var n = "week", r = "year";
      return function(s, i, o) {
        var a = i.prototype;
        a.week = function(u) {
          if (u === void 0 && (u = null), u !== null) return this.add(7 * (u - this.week()), "day");
          var c = this.$locale().yearStart || 1;
          if (this.month() === 11 && this.date() > 25) {
            var l = o(this).startOf(r).add(1, r).date(c), h = o(this).endOf(n);
            if (l.isBefore(h)) return 1;
          }
          var d = o(this).startOf(r).date(c).startOf(n).subtract(1, "millisecond"), f = this.diff(d, n, !0);
          return f < 0 ? o(this).startOf("week").week() : Math.ceil(f);
        }, a.weeks = function(u) {
          return u === void 0 && (u = null), this.week(u);
        };
      };
    });
  }(Wr)), Wr.exports;
}
var ap = op();
const up = /* @__PURE__ */ wt(ap);
var zr = { exports: {} }, lp = zr.exports, Ho;
function cp() {
  return Ho || (Ho = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(lp, function() {
      return function(n, r) {
        r.prototype.weekYear = function() {
          var s = this.month(), i = this.week(), o = this.year();
          return i === 1 && s === 11 ? o + 1 : s === 0 && i >= 52 ? o - 1 : o;
        };
      };
    });
  }(zr)), zr.exports;
}
var hp = cp();
const dp = /* @__PURE__ */ wt(hp);
rn.extend(Hg);
rn.extend(Fg);
rn.extend(sp);
rn.extend(Vg);
rn.extend(up);
rn.extend(dp);
rn.extend(ep);
rn.extend(Jg);
function Li(t, e, n, r) {
  if (t > e)
    throw new Error("a1 should be less than a2");
  if (n > r)
    throw new Error("b1 should be less than b2");
  if (e < n || r < t)
    return [t, e];
  if (n <= t && r >= e)
    return [];
  const s = r - n + 1;
  return t < n && e > r ? [t, e - s] : n <= t && r < e ? [r + 1 - s, e - s] : n > t && r >= e ? [t, n - 1] : [t, e];
}
function TC(t) {
  if (t == null)
    return !1;
  const e = t.bullet;
  return (e == null ? void 0 : e.listId) != null;
}
function MC(t) {
  if (t == null)
    return !1;
  const e = t.paragraphStyle;
  return fp(e);
}
function fp(t) {
  var e;
  return !(t == null || (t.indentStart == null || t.indentStart.v === 0) && t.hanging == null || ((e = t.hanging) == null ? void 0 : e.v) === 0);
}
function gp(t, e, n) {
  return t.slice(0, e) + n + t.slice(e);
}
function pp(t, e, n) {
  return e > n ? t : t.slice(0, e) + t.slice(n);
}
const mp = /\s/g;
function DC(t) {
  return t === null || t.toString().replace(mp, "") === "" || typeof t == "boolean" ? !1 : !isNaN(t);
}
function xC(t) {
  let e = 0;
  for (let n = 0; n < t.length; n++)
    e = t.charCodeAt(n) + (e << 6) + (e << 16) - e;
  return e >>> 0;
}
const Ye = Symbol("newer"), rt = Symbol("older");
class _p {
  constructor(e) {
    C(this, "entry");
    this.entry = e;
  }
  [Symbol.iterator]() {
    return this;
  }
  next() {
    const e = this.entry;
    return e ? (this.entry = e[Ye], { done: !1, value: e.key }) : { done: !0, value: void 0 };
  }
}
class Ep {
  constructor(e) {
    C(this, "entry");
    this.entry = e;
  }
  [Symbol.iterator]() {
    return this;
  }
  next() {
    const e = this.entry;
    return e ? (this.entry = e[Ye], { done: !1, value: e.value }) : { done: !0, value: void 0 };
  }
}
class Cp {
  constructor(e) {
    C(this, "entry");
    this.entry = e;
  }
  [Symbol.iterator]() {
    return this;
  }
  next() {
    const e = this.entry;
    return e ? (this.entry = e[Ye], { done: !1, value: [e.key, e.value] }) : { done: !0, value: void 0 };
  }
}
var Ta, Ma;
Ma = Ye, Ta = rt;
class Wo {
  constructor(e, n) {
    C(this, "key");
    C(this, "value");
    C(this, Ma);
    C(this, Ta);
    this.key = e, this.value = n, this[Ye] = void 0, this[rt] = void 0;
  }
  toJSON() {
    return {
      key: this.key,
      value: this.value
    };
  }
}
class Qr {
  constructor(...e) {
    C(this, "_keymap");
    C(this, "size", 0);
    C(this, "limit");
    C(this, "oldest");
    C(this, "newest");
    C(this, "_onShiftListeners", []);
    if (Cr.hasLength(e, 1)) {
      if (Cr.isNumber(e[0])) {
        const n = e[0];
        this._initialize(n, void 0);
        return;
      }
      if (Cr.isIterable(e[0])) {
        const n = e[0];
        this._initialize(0, n);
        return;
      }
      return;
    }
    if (Cr.hasLength(e, 2)) {
      const n = e[0], r = e[1];
      this._initialize(n, r);
    }
  }
  onShift(e) {
    if (this._onShiftListeners.indexOf(e) === -1)
      return this._onShiftListeners.push(e), Ze(() => cs(this._onShiftListeners, e));
    throw new Error("[LRUMap]: the listener has been registered!");
  }
  _initialize(e, n) {
    this.oldest = void 0, this.newest = void 0, this.size = 0, this.limit = e, this._keymap = /* @__PURE__ */ new Map(), n && (this.assign(n), e < 1 && (this.limit = this.size));
  }
  _markEntryAsUsed(e) {
    e !== this.newest && (e[Ye] && (e === this.oldest && (this.oldest = e[Ye]), e[Ye][rt] = e[rt]), e[rt] && (e[rt][Ye] = e[Ye]), e[Ye] = void 0, e[rt] = this.newest, this.newest && (this.newest[Ye] = e), this.newest = e);
  }
  assign(e) {
    let n, r = this.limit || Number.MAX_VALUE;
    this._keymap.clear();
    const s = e[Symbol.iterator]();
    for (let i = s.next(); !i.done; i = s.next()) {
      const o = new Wo(i.value[0], i.value[1]);
      if (this._keymap.set(o.key, o), n ? (n[Ye] = o, o[rt] = n) : this.oldest = o, n = o, r-- === 0)
        throw new Error("overflow");
    }
    this.newest = n, this.size = this._keymap.size;
  }
  set(e, n) {
    let r = this._keymap.get(e);
    return r ? (r.value = n, this._markEntryAsUsed(r), this) : (this._keymap.set(e, r = new Wo(e, n)), this.newest ? (this.newest[Ye] = r, r[rt] = this.newest) : this.oldest = r, this.newest = r, ++this.size, this.size > this.limit && this.shift(), this);
  }
  shift() {
    const e = this.oldest;
    if (e)
      return this.oldest && this.oldest[Ye] ? (this.oldest = this.oldest[Ye], this.oldest[rt] = void 0) : (this.oldest = void 0, this.newest = void 0), e[Ye] = e[rt] = void 0, this._keymap.delete(e.key), --this.size, this._onShiftListeners.forEach((n) => n(e)), [e.key, e.value];
  }
  get(e) {
    const n = this._keymap.get(e);
    if (n)
      return this._markEntryAsUsed(n), n.value;
  }
  has(e) {
    return this._keymap.has(e);
  }
  find(e) {
    const n = this._keymap.get(e);
    return n ? n.value : void 0;
  }
  delete(e) {
    const n = this._keymap.get(e);
    if (n)
      return this._keymap.delete(n.key), n[Ye] && n[rt] ? (n[rt][Ye] = n[Ye], n[Ye][rt] = n[rt]) : n[Ye] ? (n[Ye][rt] = void 0, this.oldest = n[Ye]) : n[rt] ? (n[rt][Ye] = void 0, this.newest = n[rt]) : this.oldest = this.newest = void 0, this.size--, n.value;
  }
  clear() {
    this.oldest = void 0, this.newest = void 0, this.size = 0, this._keymap.clear();
  }
  keys() {
    return new _p(this.oldest);
  }
  values() {
    return new Ep(this.oldest);
  }
  entries() {
    return this[Symbol.iterator]();
  }
  [Symbol.iterator]() {
    return new Cp(this.oldest);
  }
  forEach(e, n) {
    typeof n != "object" && (n = this);
    let r = this.oldest;
    for (; r; )
      e.call(n, r.value, r.key, this), r = r[Ye];
  }
  toJSON() {
    const e = new Array(this.size);
    let n = 0, r = this.oldest;
    for (; r; )
      e[n++] = { key: r.key, value: r.value }, r = r[Ye];
    return e;
  }
  toString() {
    let e = "", n = this.oldest;
    for (; n; )
      e += `${String(n.key)}:${n.value}`, n = n[Ye], n && (e += " < ");
    return e;
  }
}
class Cr {
  static hasLength(e, n) {
    return e.length === n;
  }
  static getValueType(e) {
    return Object.prototype.toString.apply(e);
  }
  static isObject(e) {
    return this.getValueType(e) === "[object Object]";
  }
  static isIterable(e) {
    return e[Symbol.iterator] != null;
  }
  static isNumber(e) {
    return this.getValueType(e) === "[object Number]";
  }
}
var Yr = { exports: {} }, Rp = Yr.exports, zo;
function Ip() {
  return zo || (zo = 1, function(t, e) {
    (function(n, r) {
      t.exports = r();
    })(typeof self < "u" ? self : Rp, function() {
      return function() {
        var n = { d: function(_, g) {
          for (var p in g) n.o(g, p) && !n.o(_, p) && Object.defineProperty(_, p, { enumerable: !0, get: g[p] });
        }, o: function(_, g) {
          return Object.prototype.hasOwnProperty.call(_, g);
        } }, r = {};
        n.d(r, { default: function() {
          return ht;
        } });
        var s = { 1078: "af", 1052: "sq", 1118: "am", 5121: "ar_DZ", 15361: "ar_BH", 3073: "ar_EG", 2049: "ar_IQ", 11265: "ar_JO", 13313: "ar_KW", 12289: "ar_LB", 4097: "ar_LY", 6145: "ar_MA", 8193: "ar_OM", 16385: "ar_QA", 1025: "ar_SA", 10241: "ar_SY", 7169: "ar_TN", 14337: "ar_AE", 9217: "ar_YE", 1067: "hy", 1101: "as", 2092: "az_AZ", 1068: "az_AZ", 1069: "eu", 1059: "be", 2117: "bn", 1093: "bn_IN", 5146: "bs", 1026: "bg", 1109: "my", 1027: "ca", 2052: "zh_CN", 3076: "zh_HK", 5124: "zh_MO", 4100: "zh_SG", 1028: "zh_TW", 1050: "hr", 1029: "cs", 1030: "da", 1125: "dv", 2067: "nl_BE", 1043: "nl_NL", 1126: "bin", 3081: "en_AU", 10249: "en_BZ", 4105: "en_CA", 9225: "en_CB", 2057: "en_GB", 16393: "en_IN", 6153: "en_IE", 8201: "en_JM", 5129: "en_NZ", 13321: "en_PH", 7177: "en_ZA", 11273: "en_TT", 1033: "en_US", 12297: "en_ZW", 1061: "et", 1071: "mk", 1080: "fo", 1065: "fa", 1124: "fil", 1035: "fi", 2060: "fr_BE", 11276: "fr_CM", 3084: "fr_CA", 9228: "fr_CG", 12300: "fr_CI", 1036: "fr_FR", 5132: "fr_LU", 13324: "fr_ML", 6156: "fr_MC", 14348: "fr_MA", 10252: "fr_SN", 4108: "fr_CH", 7180: "fr", 1122: "fy_NL", 2108: "gd_IE", 1084: "gd", 1110: "gl", 1079: "ka", 3079: "de_AT", 1031: "de_DE", 5127: "de_LI", 4103: "de_LU", 2055: "de_CH", 1032: "el", 1140: "gn", 1095: "gu", 1279: "en", 1037: "he", 1081: "hi", 1038: "hu", 1039: "is", 1136: "ig_NG", 1057: "id", 1040: "it_IT", 2064: "it_CH", 1041: "ja", 1099: "kn", 1120: "ks", 1087: "kk", 1107: "km", 1111: "kok", 1042: "ko", 1088: "ky", 1108: "lo", 1142: "la", 1062: "lv", 1063: "lt", 2110: "ms_BN", 1086: "ms_MY", 1100: "ml", 1082: "mt", 1112: "mni", 1153: "mi", 1102: "mr", 1104: "mn", 2128: "mn", 1121: "ne", 1044: "no_NO", 2068: "no_NO", 1096: "or", 1045: "pl", 1046: "pt_BR", 2070: "pt_PT", 1094: "pa", 1047: "rm", 2072: "ro_MO", 1048: "ro_RO", 1049: "ru", 2073: "ru_MO", 1083: "se", 1103: "sa", 3098: "sr_SP", 2074: "sr_SP", 1072: "st", 1074: "tn", 1113: "sd", 1115: "si", 1051: "sk", 1060: "sl", 1143: "so", 1070: "sb", 11274: "es_AR", 16394: "es_BO", 13322: "es_CL", 9226: "es_CO", 5130: "es_CR", 7178: "es_DO", 12298: "es_EC", 17418: "es_SV", 4106: "es_GT", 18442: "es_HN", 2058: "es_MX", 19466: "es_NI", 6154: "es_PA", 15370: "es_PY", 10250: "es_PE", 20490: "es_PR", 1034: "es_ES", 14346: "es_UY", 8202: "es_VE", 1089: "sw", 2077: "sv_FI", 1053: "sv_SE", 1114: "syc", 1064: "tg", 1097: "ta", 1092: "tt", 1098: "te", 1054: "th", 1105: "bo", 1073: "ts", 1055: "tr", 1090: "tk", 1058: "uk", 1056: "ur", 2115: "uz_UZ", 1091: "uz_UZ", 1075: "ve", 1066: "vi", 1106: "cy", 1076: "xh", 1085: "yi", 1077: "zu" };
        const i = /^([a-z\d]+)(?:[_-]([a-z\d]+))?(?:\.([a-z\d]+))?(?:@([a-z\d]+))?$/i, o = {}, a = { group: " ", decimal: ".", positive: "+", negative: "-", percent: "%", exponent: "E", nan: "NaN", infinity: "∞", ampm: ["AM", "PM"], mmmm6: ["Muharram", "Safar", "Rabiʻ I", "Rabiʻ II", "Jumada I", "Jumada II", "Rajab", "Shaʻban", "Ramadan", "Shawwal", "Dhuʻl-Qiʻdah", "Dhuʻl-Hijjah"], mmm6: ["Muh.", "Saf.", "Rab. I", "Rab. II", "Jum. I", "Jum. II", "Raj.", "Sha.", "Ram.", "Shaw.", "Dhuʻl-Q.", "Dhuʻl-H."], mmmm: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], mmm: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], dddd: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], ddd: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"] };
        function u(_) {
          const g = i.exec(_);
          if (!g) throw new SyntaxError("Malformed locale: ".concat(_));
          return { lang: g[1] + (g[2] ? "_" + g[2] : ""), language: g[1], territory: g[2] || "", codeset: g[3] || "", modifier: g[4] || "" };
        }
        function c(_) {
          if (typeof _ == "number") return s[65535 & _] || null;
          const g = parseInt(_, 16);
          return isFinite(g) && s[65535 & g] ? s[65535 & g] || null : i.test(_) ? _ : null;
        }
        function l(_) {
          const g = c(_);
          let p = null;
          if (g) {
            const S = u(g);
            p = o[S.lang] || o[S.language] || null;
          }
          return p;
        }
        function h(_) {
          return Object.assign({}, a, _);
        }
        function d(_, g) {
          const p = typeof g == "object" ? g : u(g);
          return o[p.lang] = h(_), p.language === p.lang || o[p.language] || (o[p.language] = h(_)), o[p.lang];
        }
        const f = h({ group: "," });
        function E(_, g) {
          if (typeof _ != "number") return _;
          if (_ < 0) return -E(-_, g);
          if (g) {
            const p = 10 ** (g || 0) || 1;
            return E(_ * p, 0) / p;
          }
          return Math.round(_);
        }
        f.isDefault = !0, d({ group: ",", ampm: ["上午", "下午"], mmmm: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"], mmm: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"], dddd: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"], ddd: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"] }, "zh_CN"), d({ group: ",", nan: "非數值", ampm: ["上午", "下午"], mmmm: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"], mmm: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"], dddd: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"], ddd: ["週日", "週一", "週二", "週三", "週四", "週五", "週六"] }, "zh_TW"), d({ group: ",", ampm: ["午前", "午後"], mmmm: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"], mmm: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"], dddd: ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日"], ddd: ["日", "月", "火", "水", "木", "金", "土"] }, "ja"), d({ group: ",", ampm: ["오전", "오후"], mmmm: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"], mmm: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"], dddd: ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"], ddd: ["일", "월", "화", "수", "목", "금", "토"] }, "ko"), d({ group: ",", ampm: ["ก่อนเที่ยง", "หลังเที่ยง"], mmmm: ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"], mmm: ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."], dddd: ["วันอาทิตย์", "วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์"], ddd: ["อา.", "จ.", "อ.", "พ.", "พฤ.", "ศ.", "ส."] }, "th"), d({ decimal: ",", ampm: ["dop.", "odp."], mmmm: ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"], mmm: ["led", "úno", "bře", "dub", "kvě", "čvn", "čvc", "srp", "zář", "říj", "lis", "pro"], dddd: ["neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota"], ddd: ["ne", "po", "út", "st", "čt", "pá", "so"] }, "cs"), d({ group: ".", decimal: ",", mmmm: ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september", "oktober", "november", "december"], mmm: ["jan.", "feb.", "mar.", "apr.", "maj", "jun.", "jul.", "aug.", "sep.", "okt.", "nov.", "dec."], dddd: ["søndag", "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag"], ddd: ["søn.", "man.", "tir.", "ons.", "tor.", "fre.", "lør."] }, "da"), d({ group: ".", decimal: ",", ampm: ["a.m.", "p.m."], mmmm: ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"], mmm: ["jan.", "feb.", "mrt.", "apr.", "mei", "jun.", "jul.", "aug.", "sep.", "okt.", "nov.", "dec."], dddd: ["zondag", "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag"], ddd: ["zo", "ma", "di", "wo", "do", "vr", "za"] }, "nl"), d({ group: "," }, "en"), d({ decimal: ",", nan: "epäluku", ampm: ["ap.", "ip."], mmmm: ["tammikuuta", "helmikuuta", "maaliskuuta", "huhtikuuta", "toukokuuta", "kesäkuuta", "heinäkuuta", "elokuuta", "syyskuuta", "lokakuuta", "marraskuuta", "joulukuuta"], mmm: ["tammik.", "helmik.", "maalisk.", "huhtik.", "toukok.", "kesäk.", "heinäk.", "elok.", "syysk.", "lokak.", "marrask.", "jouluk."], dddd: ["sunnuntaina", "maanantaina", "tiistaina", "keskiviikkona", "torstaina", "perjantaina", "lauantaina"], ddd: ["su", "ma", "ti", "ke", "to", "pe", "la"] }, "fi"), d({ group: " ", decimal: ",", mmmm: ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"], mmm: ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."], dddd: ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"], ddd: ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."] }, "fr"), d({ group: ".", decimal: ",", mmmm: ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"], mmm: ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."], dddd: ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"], ddd: ["So.", "Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa."] }, "de"), d({ group: ".", decimal: ",", ampm: ["π.μ.", "μ.μ."], mmmm: ["Ιανουαρίου", "Φεβρουαρίου", "Μαρτίου", "Απριλίου", "Μαΐου", "Ιουνίου", "Ιουλίου", "Αυγούστου", "Σεπτεμβρίου", "Οκτωβρίου", "Νοεμβρίου", "Δεκεμβρίου"], mmm: ["Ιαν", "Φεβ", "Μαρ", "Απρ", "Μαΐ", "Ιουν", "Ιουλ", "Αυγ", "Σεπ", "Οκτ", "Νοε", "Δεκ"], dddd: ["Κυριακή", "Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο"], ddd: ["Κυρ", "Δευ", "Τρί", "Τετ", "Πέμ", "Παρ", "Σάβ"] }, "el"), d({ decimal: ",", ampm: ["de.", "du."], mmmm: ["január", "február", "március", "április", "május", "június", "július", "augusztus", "szeptember", "október", "november", "december"], mmm: ["jan.", "febr.", "márc.", "ápr.", "máj.", "jún.", "júl.", "aug.", "szept.", "okt.", "nov.", "dec."], dddd: ["vasárnap", "hétfő", "kedd", "szerda", "csütörtök", "péntek", "szombat"], ddd: ["V", "H", "K", "Sze", "Cs", "P", "Szo"] }, "hu"), d({ group: ".", decimal: ",", ampm: ["f.h.", "e.h."], mmmm: ["janúar", "febrúar", "mars", "apríl", "maí", "júní", "júlí", "ágúst", "september", "október", "nóvember", "desember"], mmm: ["jan.", "feb.", "mar.", "apr.", "maí", "jún.", "júl.", "ágú.", "sep.", "okt.", "nóv.", "des."], dddd: ["sunnudagur", "mánudagur", "þriðjudagur", "miðvikudagur", "fimmtudagur", "föstudagur", "laugardagur"], ddd: ["sun.", "mán.", "þri.", "mið.", "fim.", "fös.", "lau."] }, "is"), d({ group: ".", decimal: ",", mmmm: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], mmm: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"], dddd: ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"], ddd: ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"] }, "id"), d({ group: ".", decimal: ",", mmmm: ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"], mmm: ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"], dddd: ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"], ddd: ["dom", "lun", "mar", "mer", "gio", "ven", "sab"] }, "it"), d({ decimal: ",", ampm: ["a.m.", "p.m."], mmmm: ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"], mmm: ["jan.", "feb.", "mar.", "apr.", "mai", "jun.", "jul.", "aug.", "sep.", "okt.", "nov.", "des."], dddd: ["søndag", "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag"], ddd: ["søn.", "man.", "tir.", "ons.", "tor.", "fre.", "lør."] }, "nb"), d({ decimal: ",", mmmm: ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia", "września", "października", "listopada", "grudnia"], mmm: ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"], dddd: ["niedziela", "poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota"], ddd: ["niedz.", "pon.", "wt.", "śr.", "czw.", "pt.", "sob."] }, "pl"), d({ group: ".", decimal: ",", mmmm: ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"], mmm: ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."], dddd: ["domingo", "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado"], ddd: ["dom.", "seg.", "ter.", "qua.", "qui.", "sex.", "sáb."] }, "pt"), d({ decimal: ",", nan: "не число", mmmm: ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"], mmm: ["янв.", "февр.", "мар.", "апр.", "мая", "июн.", "июл.", "авг.", "сент.", "окт.", "нояб.", "дек."], dddd: ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"], ddd: ["вс", "пн", "вт", "ср", "чт", "пт", "сб"] }, "ru"), d({ decimal: ",", mmmm: ["januára", "februára", "marca", "apríla", "mája", "júna", "júla", "augusta", "septembra", "októbra", "novembra", "decembra"], mmm: ["jan", "feb", "mar", "apr", "máj", "jún", "júl", "aug", "sep", "okt", "nov", "dec"], dddd: ["nedeľa", "pondelok", "utorok", "streda", "štvrtok", "piatok", "sobota"], ddd: ["ne", "po", "ut", "st", "št", "pi", "so"] }, "sk"), d({ group: ".", decimal: ",", ampm: ["a. m.", "p. m."], mmmm: ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"], mmm: ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sept.", "oct.", "nov.", "dic."], dddd: ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"], ddd: ["dom.", "lun.", "mar.", "mié.", "jue.", "vie.", "sáb."] }, "es"), d({ decimal: ",", ampm: ["fm", "em"], mmmm: ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"], mmm: ["jan.", "feb.", "mars", "apr.", "maj", "juni", "juli", "aug.", "sep.", "okt.", "nov.", "dec."], dddd: ["söndag", "måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag"], ddd: ["sön", "mån", "tis", "ons", "tors", "fre", "lör"] }, "sv"), d({ group: ".", decimal: ",", ampm: ["ÖÖ", "ÖS"], mmmm: ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], mmm: ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"], dddd: ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"], ddd: ["Paz", "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt"] }, "tr");
        function R(_, g, p) {
          const S = _ < 0 ? -1 : 1, N = 10 ** (g || 2), L = 10 ** (p || 2);
          let x, P, I = Math.abs(_), Q = 0, _e = 0, J = 0, me = 1;
          if ((_ = I) % 1 == 0) P = [_ * S, 1];
          else if (_ < 1e-19) P = [S, 1e19];
          else if (_ > 1e19) P = [1e19 * S, 1];
          else {
            do
              if (I = 1 / (I - Math.floor(I)), x = me, me = me * Math.floor(I) + Q, Q = x, _e = J, J = Math.floor(_ * me + 0.5), J >= N || me >= L) return [S * _e, Q];
            while (Math.abs(_ - J / me) >= 1e-10 && I !== Math.floor(I));
            P = [S * J, me];
          }
          return P;
        }
        const O = { overflow: "######", dateErrorThrows: !1, dateErrorNumber: !0, dateSpanLarge: !0, leap1900: !0, nbsp: !0, throws: !0, invalid: "######", locale: "", ignoreTimezone: !1 }, U = Object.assign({}, O);
        function ne(_) {
          if (_ === null && (_ = O), _) {
            for (const g in _) if (g in O) {
              const p = _[g];
              U[g] = p == null ? O[g] : p;
            }
          }
          return { ...U };
        }
        const X = { "#": "", 0: "0", "?": " " }, de = { "@": "text", "-": "minus", "+": "plus" }, T = ["#000", "#FFF", "#F00", "#0F0", "#00F", "#FF0", "#F0F", "#0FF", "#000", "#FFF", "#F00", "#0F0", "#00F", "#FF0", "#F0F", "#0FF", "#800", "#080", "#008", "#880", "#808", "#088", "#CCC", "#888", "#99F", "#936", "#FFC", "#CFF", "#606", "#F88", "#06C", "#CCF", "#008", "#F0F", "#FF0", "#0FF", "#808", "#800", "#088", "#00F", "#0CF", "#CFF", "#CFC", "#FF9", "#9CF", "#F9C", "#C9F", "#FC9", "#36F", "#3CC", "#9C0", "#FC0"], A = ["¤", "$", "£", "¥", "֏", "؋", "৳", "฿", "៛", "₡", "₦", "₩", "₪", "₫", "€", "₭", "₮", "₱", "₲", "₴", "₸", "₹", "₺", "₼", "₽", "₾", "₿"], H = new RegExp("[" + A.join("") + "]");
        function Z(_, g, p) {
          return g[p + "_max"] = _.length, g[p + "_min"] = _.replace(/#/g, "").length, g;
        }
        const fe = {};
        function ae(_) {
          if (!(_ in fe)) {
            const g = [], p = _.replace(/^[#,]+/, "").replace(/[1-9]\d*/g, (S) => "?".repeat(S.length));
            for (let S = 0; S < p.length; S++) {
              const N = p.charAt(S);
              g[S] = N in X ? X[N] : N;
            }
            fe[_] = g.join("");
          }
          return fe[_];
        }
        function m(_, g) {
          typeof _ == "string" && (_ = { type: "string", value: _ = _.replace(/ /g, X["?"]) }), g.push(_);
        }
        function j(_) {
          const g = [], p = { scale: 1, percent: !1, text: !1, date: 0, date_eval: !1, date_system: 1, sec_decimals: 0, general: !1, clock: 24, int_pattern: [], frac_pattern: [], man_pattern: [], den_pattern: [], num_pattern: [], tokens: g };
          let S = _ + "", N = "int", L = !1, x = null;
          const P = [];
          let I, Q, _e = !1;
          for (; S && !L; ) {
            if (I = /^General/i.exec(S)) p.general = !0, m({ type: "general" }, g);
            else if (N === "int" && (I = /^[#?0]+(?:,[#?0]+)*/.exec(S)) || N === "den" && (I = /^[#?\d]+/.exec(S)) || (I = /^[#?0]+/.exec(S))) p[N + "_pattern"].push(I[0]), x = { type: N, num: I[0] }, m(x, g);
            else if ((I = /^\//.exec(S)) && p[N + "_pattern"].length) {
              if (!x) throw new SyntaxError("Missing a numerator in pattern ".concat(_));
              p.fractions = !0, p.num_pattern.push(p[N + "_pattern"].pop()), x.type = "num", N = "den", m({ type: "div" }, g);
            } else if (I = /^,+/.exec(S)) {
              const D = S.charAt(1) in X;
              Q.slice(-1) in X && (I[0].length > 1 || !D) ? p.scale = 1e-3 ** I[0].length : p.dec_fractions || m(I[0], g);
            } else {
              if (I = /^;/.exec(S)) {
                L = !0;
                break;
              }
              if (I = /^[@+-]/.exec(S)) I[0] === "@" && (p.text = !0), m({ type: de[I[0]] }, g);
              else if (I = /^(?:\[(h+|m+|s+)\])/i.exec(S)) {
                const D = I[1].toLowerCase(), q = D[0], Ce = { type: "", size: 0, date: 1, raw: I[0], pad: D.length };
                q === "h" ? (Ce.size = 16, Ce.type = "hour-elap") : q === "m" ? (Ce.size = 32, Ce.type = "min-elap") : (Ce.size = 64, Ce.type = "sec-elap"), p.date = p.date | Ce.size, P.push(Ce), m(Ce, g);
              } else if (I = /^(?:B2)/i.exec(S)) _e || (p.date_system = 6);
              else if (I = /^(?:B1)/i.exec(S)) _e || (p.date_system = 1);
              else if (I = /^(?:([hHmMsSyYbBdDegG])\1*)/.exec(S)) {
                const D = { type: "", size: 0, date: 1, raw: I[0] }, q = I[0].toLowerCase(), Ce = q[0];
                if (q === "y" || q === "yy") D.size = 2, D.type = "year-short";
                else if (Ce === "y" || Ce === "e") D.size = 2, D.type = "year";
                else if (q === "b" || q === "bb") D.size = 2, D.type = "b-year-short";
                else if (Ce === "b") D.size = 2, D.type = "b-year";
                else if (q === "d" || q === "dd") D.size = 8, D.type = "day", D.pad = /dd/.test(q);
                else if (q === "ddd") D.size = 8, D.type = "weekday-short";
                else if (Ce === "d") D.size = 8, D.type = "weekday";
                else if (Ce === "h") D.size = 16, D.type = "hour", D.pad = /hh/i.test(q);
                else if (Ce === "m") {
                  q.length === 3 ? (D.size = 4, D.type = "monthname-short") : q.length === 5 ? (D.size = 4, D.type = "monthname-single") : q.length >= 4 && (D.size = 4, D.type = "monthname");
                  const Se = P[P.length - 1];
                  !D.type && Se && !Se.used && 80 & Se.size && (Se.used = !0, D.size = 32, D.type = "min", D.pad = /mm/.test(q)), D.type || (D.size = 4, D.type = "month", D.pad = /mm/.test(q), D.indeterminate = !0);
                } else if (Ce === "s") {
                  D.size = 64, D.type = "sec", D.pad = /ss/.test(q);
                  const Se = P[P.length - 1];
                  Se && 32 & Se.size ? D.used = !0 : Se && Se.indeterminate && (delete Se.indeterminate, Se.size = 32, Se.type = "min", D.used = !0);
                }
                p.date = p.date | D.size, p.date_eval = !0, P.push(D), m(D, g);
              } else if (I = /^(?:AM\/PM|am\/pm|A\/P)/.exec(S)) p.clock = 12, p.date = 16 | p.date, p.date_eval = !0, m({ type: "am", short: I[0] === "A/P" }, g);
              else if (p.date && (I = /^\.0{1,3}/i.exec(S))) {
                const D = I[0].length - 1, q = [64, 128, 256, 512][D];
                p.date = p.date | q, p.date_eval = !0, p.sec_decimals = Math.max(p.sec_decimals, D), m({ type: "subsec", size: q, decimals: D, date: 1, raw: I[0] }, g);
              } else if ((I = /^\\(.)/.exec(S)) || (I = /^"([^"]*?)"/.exec(S))) m(I[1], g);
              else if (I = /^\[(<[=>]?|>=?|=)\s*(-?[.\d]+)\]/.exec(S)) p.condition = [I[1], parseFloat(I[2], 10)];
              else if (I = /^\[\$([^\]]+)\]/.exec(S)) {
                const D = I[1].split("-"), q = D.length < 2 ? "" : D[D.length - 1], Ce = D[0];
                Ce && m(Ce, g);
                const Se = c(q);
                Se && (p.locale = Se);
                const Le = parseInt(q, 16);
                isFinite(Le) && 16711680 & Le && (Le >> 16 & 255) === 6 && (p.date_system = 6), _e = !0;
              } else if (I = /^\[(black|blue|cyan|green|magenta|red|white|yellow|color\s*(\d+))\]/i.exec(S)) p.color = I[2] ? T[parseInt(I[2], 10)] || "#000" : I[1].toLowerCase();
              else if (!(I = /^\[(DBNum1|ENG|HIJ|JPN|TWN)\]/i.exec(S))) {
                if (I = /^%/.exec(S)) p.scale = 100, p.percent = !0, m("%", g);
                else if (I = /^_(\\.|.)/.exec(S)) m(" ", g);
                else if (I = /^\./.exec(S)) m({ type: "point", value: I[0] }, g), p.dec_fractions = !0, N = "frac";
                else if (I = /^[Ee]([+-]?|(?=[0#?]))/.exec(S)) p.exponential = !0, p.exp_plus = I[1] === "+", N = "man", m({ type: "exp", plus: I[1] === "+" }, g);
                else if (!(I = /^\*(\\.|.)/.exec(S))) {
                  if (I = /^[BENn[]/.exec(S)) throw new SyntaxError("Unexpected char ".concat(S.charAt(0), " in pattern ").concat(_));
                  S[0] === "(" && (p.parens = !0), I = [S[0]], m(I[0], g);
                }
              }
            }
            Q = I[0], S = S.slice(I ? I[0].length : 1);
          }
          if (p.pattern = _.slice(0, _.length - S.length), /^((?:\[[^\]]+\])+)(;|$)/.test(p.pattern) && !/^\[(?:h+|m+|s+)\]/.test(p.pattern) && m({ type: "text" }, g), p.fractions && p.dec_fractions || p.fractions && p.exponential) throw new SyntaxError("Invalid pattern: ".concat(p.pattern));
          const J = p.int_pattern.join("");
          if (p.grouping = J.indexOf(",") >= 0, p.grouping) {
            const D = J.split(","), q = D.length;
            q === 2 ? (p.group_pri = D[1].length, p.group_sec = p.group_pri) : q > 2 && (p.group_pri = D[q - 1].length, p.group_sec = D[q - 2].length);
          } else p.group_pri = 0, p.group_sec = 0;
          Z(J.replace(/[,]/g, ""), p, "int"), Z(p.frac_pattern.join(""), p, "frac"), Z(p.man_pattern.join(""), p, "man");
          let me = p.num_pattern.join(""), ye = p.den_pattern.join("");
          const le = /\?/.test(ye) || /\?/.test(me);
          return ye = ye.replace(/\d/g, le ? "?" : "#"), le && (ye = ye.replace(/#$/g, "?")), Z(me, p, "num"), Z(ye, p, "den"), le && (me = me.replace(/#$/g, "?")), p.int_padding = ae(p.int_pattern.join("")), p.man_padding = ae(p.man_pattern.join("")), p.num_padding = ae(me), p.den_padding = ae(ye), p.den_pattern.length && (p.denominator = parseInt(p.den_pattern.join("").replace(/\D/g, ""), 10)), p.integer = !!p.int_pattern.join("").length, p.fractions && g.forEach((D, q) => {
            const Ce = g[q + 1];
            D.type === "string" && Ce && (Ce.type === "num" ? D.rule = "num+int" : Ce.type === "div" ? D.rule = "num" : Ce.type === "den" && (D.rule = "den"));
          }), p;
        }
        const y = (_) => {
          const g = _.condition;
          g && g[1] < 0 && (g[0] === "<" || g[0] === "<=" || g[0] === "=") || _.tokens.unshift({ type: "minus", volatile: !0 });
        };
        function M(_) {
          const g = [];
          let p, S = !1, N = null, L = _, x = 0, P = !1, I = 0, Q = 0;
          do {
            if (P = j(L), (P.date || P.general) && (P.int_pattern.length || P.frac_pattern.length || P.scale !== 1 || P.text)) throw new Error("Illegal format");
            if (P.condition && (Q++, S = !0), P.text) {
              if (N) throw new Error("Unexpected partition");
              N = P;
            }
            P.locale && (p = c(P.locale)), g.push(P), x = L.charAt(P.pattern.length) === ";" ? 1 : 0, L = L.slice(P.pattern.length + x), I++;
          } while (x && I < 4 && Q < 3);
          if (x) throw new Error("Unexpected partition");
          if (Q > 2) throw new Error("Unexpected condition");
          const _e = g[3];
          if (_e && (_e.int_pattern.length || _e.frac_pattern.length || _e.date)) throw new Error("Unexpected partition");
          if (S) {
            const J = g.length;
            if (J === 1 && (g[1] = j("General"), g[1].generated = !0), J < 3) {
              const me = g[0], ye = g[1];
              if (y(me), ye.condition) y(ye);
              else {
                const le = me.condition;
                (le[0] === "=" || le[1] >= 0 && (le[0] === ">" || le[0] === ">=")) && ye.tokens.unshift({ type: "minus", volatile: !0 });
              }
            } else g.forEach(y);
          } else {
            if (g.length < 4 && N) for (let J = 0, me = g.length; J < me; J++) g[J] === N && g.splice(J, 1);
            if (g.length < 1 && N && (g[0] = j("General"), g[0].generated = !0), g.length < 2) {
              const J = j(g[0].pattern);
              J.tokens.unshift({ type: "minus", volatile: !0 }), J.generated = !0, g.push(J);
            }
            if (g.length < 3) {
              const J = j(g[0].pattern);
              J.generated = !0, g.push(J);
            }
            if (g.length < 4) if (N) g.push(N);
            else {
              const J = j("@");
              J.generated = !0, g.push(J);
            }
            g[0].condition = [">", 0], g[1].condition = ["<", 0], g[2].condition = null;
          }
          return { pattern: _, partitions: g, locale: p };
        }
        const b = Math.floor;
        function w(_) {
          if ((!(arguments.length > 1 && arguments[1] !== void 0) || arguments[1]) && _ >= 0) {
            if (_ === 0) return [1900, 1, 0];
            if (_ === 60) return [1900, 2, 29];
            if (_ < 60) return [1900, _ < 32 ? 1 : 2, (_ - 1) % 31 + 1];
          }
          let p = _ + 68569 + 2415019;
          const S = b(4 * p / 146097);
          p -= b((146097 * S + 3) / 4);
          const N = b(4e3 * (p + 1) / 1461001);
          p = p - b(1461 * N / 4) + 31;
          const L = b(80 * p / 2447), x = p - b(2447 * L / 80);
          p = b(L / 11);
          const P = L + 2 - 12 * p;
          return [0 | 100 * (S - 49) + N + p, 0 | P, 0 | x];
        }
        function k(_) {
          return w(_ + 1462);
        }
        function $(_) {
          if (_ === 60) throw new Error("#VALUE!");
          if (_ <= 1) return [1317, 8, 29];
          if (_ < 60) return [1317, _ < 32 ? 9 : 10, 1 + (_ - 2) % 30];
          const g = 10631 / 30, p = 0.1335;
          let S = _ + 466935;
          const N = b(S / 10631);
          S -= 10631 * N;
          const L = b((S - p) / g);
          S -= b(L * g + p);
          const x = b((S + 28.5001) / 29.5);
          return x === 13 ? [30 * N + L, 12, 30] : [30 * N + L, x, S - b(29.5001 * x - 29)];
        }
        function Y(_) {
          let g = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 0, p = !(arguments.length > 2 && arguments[2] !== void 0) || arguments[2];
          const S = b(_);
          return g === 6 ? $(S) : g === -1 ? k(S) : w(S, p);
        }
        const se = Math.floor, he = 86400;
        function ge(_, g) {
          let p = null;
          if (Array.isArray(_)) {
            const [S, N, L, x, P, I] = _;
            p = Date.UTC(S, N == null ? 0 : N - 1, L != null ? L : 1, x || 0, P || 0, I || 0);
          } else if (_ instanceof Date && (p = 1 * _, !g || !g.ignoreTimezone)) {
            const S = /* @__PURE__ */ new Date();
            S.setUTCFullYear(_.getFullYear(), _.getMonth(), _.getDate()), S.setUTCHours(_.getHours(), _.getMinutes(), _.getSeconds(), _.getMilliseconds()), p = 1 * S;
          }
          if (p != null && isFinite(p)) {
            const S = p / 864e5;
            return S - (S <= -25509 ? -25568 : -25569);
          }
          return _;
        }
        function Ae(_, g) {
          let p = 0 | _;
          const S = he * (_ - p);
          let N = se(S);
          S - N > 0.9999 && (N += 1, N === he && (N = 0, p += 1));
          const L = N < 0 ? he + N : N, [x, P, I] = Y(_, 0, g && g.leap1900), Q = se(L / 60 / 60) % 60, _e = se(L / 60) % 60, J = se(L) % 60;
          if (g && g.nativeDate) {
            const me = /* @__PURE__ */ new Date(0);
            return me.setUTCFullYear(x, P - 1, I), me.setUTCHours(Q, _e, J), me;
          }
          return [x, P, I, Q, _e, J];
        }
        function be(_) {
          return !!(_[0] && _[0].percent || _[1] && _[1].percent || _[2] && _[2].percent || _[3] && _[3].percent);
        }
        function v(_) {
          return !!(_[0] && _[0].date || _[1] && _[1].date || _[2] && _[2].date || _[3] && _[3].date);
        }
        function F(_) {
          const [g, p, S, N] = _;
          return !(g && !g.generated || p && !p.generated || S && !S.generated || !N || !N.text || N.generated);
        }
        const V = { text: 15, datetime: 10.8, date: 10.8, time: 10.8, percent: 10.6, currency: 10.4, grouped: 10.2, scientific: 6, number: 4, fraction: 2, general: 0, error: 0 }, K = [["DMY", 1], ["DM", 2], ["MY", 3], ["MDY", 4], ["MD", 5], ["hmsa", 6], ["hma", 7], ["hms", 8], ["hm", 9]], z = { total: 1, sign: 0, period: 0, int: 1, frac: 0 }, W = (_, g) => _.replace(/\./, g.decimal);
        function ue(_, g, p, S) {
          const N = 0 | p;
          if (typeof p == "string") _.push(p);
          else if (p === N) _.push(Math.abs(N));
          else {
            const L = Math.abs(p);
            let x = L ? Math.floor(Math.log10(L)) : 0, P = x < 0 ? L * 10 ** -x : L / 10 ** x;
            P === 10 && (P = 1, x++);
            const I = function(_e) {
              let J = !(arguments.length > 1 && arguments[1] !== void 0) || arguments[1];
              const me = Math.abs(_e);
              if (!me) return z;
              const ye = J && _e < 0 ? 1 : 0, le = Math.floor(me), D = Math.floor(Math.log10(me) + 1);
              let q = 0, Ce = 0;
              if (le !== me) {
                q = 1;
                const Se = String(E(D < 0 ? me * 10 ** -D : me / 10 ** D, 15));
                let Le = Se.length, Ue = !0, je = 0;
                for (; je <= Se.length; ) {
                  if (Se[je] === ".") {
                    Le--;
                    break;
                  }
                  Se[je] === "0" && Ue ? Le-- : Ue = !1, je++;
                }
                Ce = Le - D, Ce < 0 && (Ce = 0, q = 0);
              }
              return { total: ye + Math.max(D, 1) + q + Ce, digits: Math.max(D, 0) + Ce, sign: ye, period: q, int: Math.max(D, 1), frac: Ce };
            }(L), Q = () => {
              const _e = Math.abs(x);
              let J;
              J = P === 1 ? P : E(P, 5), _.push(W(J + "", S), S.exponent, x < 0 ? S.negative : S.positive, _e < 10 ? "0" : "", _e);
            };
            if (x >= -4 && x <= -1) {
              const _e = L.toPrecision(10 + x).replace(/\.?0+$/, "");
              _.push(W(_e, S));
            } else if (x === 10) {
              const _e = L.toFixed(10).slice(0, 12).replace(/\.$/, "");
              _.push(W(_e, S));
            } else if (Math.abs(x) <= 9) if (I.total <= 11) {
              const _e = E(L, 9).toFixed(I.frac);
              _.push(W(_e, S));
            } else x === 9 ? _.push(Math.floor(L)) : x >= 0 && x < 9 ? _.push(E(L, 9 - x)) : Q();
            else I.total >= 12 ? Q() : Math.floor(L) === L ? _.push(Math.floor(L)) : _.push(W(E(L, 9).toFixed(I.frac), S));
          }
          return _;
        }
        const oe = 86400, B = { int: "integer", frac: "fraction", man: "mantissa", num: "numerator", den: "denominator" }, ee = function(_) {
          let g = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 0;
          const p = Math.floor(Math.log10(_));
          return g > 1 ? Math.floor(p / g) * g : p;
        };
        function ie(_, g, p, S) {
          let N = "", L = "", x = "", P = "", I = "", Q = 0, _e = 0 | _, J = 0, me = 0, ye = 1, le = 0, D = 0, q = 0, Ce = 0, Se = 0, Le = 0;
          const Ue = S || f;
          if (!g.text && isFinite(g.scale) && g.scale !== 1 && (_ = function(Ie) {
            if (Ie === 0) return Ie;
            const Ne = Math.ceil(Math.log10(Ie < 0 ? -Ie : Ie)), te = 10 ** (16 - Math.floor(Ne));
            return Math.round(Ie * te) / te;
          }(_ * g.scale)), g.exponential) {
            let Ie = Math.abs(_);
            if (Ie) {
              const Ne = 10 ** -ee(Ie, g.int_max), te = E(Ie * Ne, g.frac_max) / Ne;
              Q = ee(te, g.int_max);
            }
            Ie /= 10 ** Q, _ = _ < 0 ? -Ie : Ie, N += Math.abs(Q);
          }
          if (g.integer) {
            const Ie = Math.abs(E(_, g.fractions ? 1 : g.frac_max));
            I += Ie < 1 ? "" : Math.floor(Ie);
          }
          if (g.grouping) {
            let Ie = "", Ne = I.length;
            for (Ne > g.group_pri && (Ne -= g.group_pri, Ie = Ue.group + I.slice(Ne, Ne + g.group_pri) + Ie); Ne > g.group_sec; ) Ne -= g.group_sec, Ie = Ue.group + I.slice(Ne, Ne + g.group_sec) + Ie;
            I = Ne ? I.slice(0, Ne) + Ie : Ie;
          }
          g.dec_fractions && (P = String(E(_, g.frac_max)).split(".")[1] || "");
          let je = !1;
          if (g.fractions) {
            const Ie = Math.abs(g.integer ? _ % 1 : _);
            if (Ie) if (je = !0, isFinite(g.denominator)) x += g.denominator, L += E(Ie * g.denominator), L === "0" && (L = "", x = "", je = !1, I || (I = "0"));
            else {
              const Ne = R(Ie, g.integer ? g.num_max : 1 / 0, g.den_max);
              L += Ne[0], x += Ne[1], g.integer && L === "0" && (I || (I = "0"), L = "", x = "", je = !1);
            }
          }
          if (g.date) {
            _e = Math.trunc(_);
            const Ie = oe * (_ - _e);
            if (J = Math.floor(Ie), Le = Ie - J, Math.abs(Le) < 1e-6 ? Le = 0 : Le > 0.9999 && (Le = 0, J += 1, J === oe && (J = 0, _e += 1)), Le) {
              const Ne = 512 & g.date || 256 & g.date || 128 & g.date;
              (Ne === 512 && Le > 0.9995 || Ne === 256 && Le > 0.995 || Ne === 128 && Le > 0.95 || !Ne && Le >= 0.5) && (J++, Le = 0);
            }
            if (_e || g.date_system) {
              const Ne = Y(_, g.date_system, p.leap1900);
              me = Ne[0], ye = Ne[1], le = Ne[2];
            }
            if (J) {
              const Ne = J < 0 ? oe + J : J;
              Se = Math.floor(Ne) % 60, Ce = Math.floor(Ne / 60) % 60, q = Math.floor(Ne / 60 / 60) % 60;
            }
            if (D = (6 + _e) % 7, g.date_eval && (dt = _, pt = _e + J / oe, p.dateSpanLarge ? dt < -694324 || pt >= 35830291 : dt < 0 || pt >= 2958466)) {
              if (p.dateErrorThrows) throw new Error("Date out of bounds");
              return p.dateErrorNumber ? ue(_ < 0 ? [Ue.negative] : [], 0, _, Ue).join("") : p.overflow;
            }
          }
          var dt, pt;
          if (g.int_padding && (I = g.int_padding.length === 1 ? I || g.int_padding : g.int_padding.substring(0, g.int_padding.length - I.length) + I), g.num_padding && (L = g.num_padding.length === 1 ? L || g.num_padding : g.num_padding.substring(0, g.num_padding.length - L.length) + L), g.den_padding && (x = g.den_padding.length === 1 ? x || g.den_padding : x + g.den_padding.slice(x.length)), g.man_padding) {
            const Ie = g.exp_plus ? "+" : "";
            N = g.man_padding.length === 1 ? (Q < 0 ? "-" : Ie) + (N || g.man_padding) : (Q < 0 ? "-" : Ie) + g.man_padding.slice(0, g.man_padding.length - N.length) + N;
          }
          const Ee = [];
          let qe = 0;
          const ve = { int: 0, frac: 0, man: 0, num: 0, den: 0 };
          for (let Ie = 0, Ne = g.tokens.length; Ie < Ne; Ie++) {
            const te = g.tokens[Ie], ut = te.num ? te.num.length : 0;
            if (te.type === "string") te.rule ? te.rule === "num" ? je ? Ee.push(te.value) : (g.num_min > 0 || g.den_min > 0) && Ee.push(te.value.replace(/./g, X["?"])) : te.rule === "num+int" ? je && I ? Ee.push(te.value) : g.den_min > 0 && (I || g.num_min) && Ee.push(te.value.replace(/./g, X["?"])) : te.rule === "den" && (je ? Ee.push(te.value) : (g.den_min > 0 || g.den_min > 0) && Ee.push(te.value.replace(/./g, X["?"]))) : Ee.push(te.value);
            else if (te.type === "error") Ee.push(p.invalid);
            else if (te.type === "point") Ee.push(g.date ? te.value : Ue.decimal);
            else if (te.type === "general") ue(Ee, 0, _, Ue);
            else if (te.type === "exp") Ee.push(Ue.exponent);
            else if (te.type === "minus") te.volatile && g.date || te.volatile && (_ >= 0 || typeof _ != "number") || (te.volatile && !g.fractions && (g.integer || g.dec_fractions) ? (_ < 0 && I && I !== "0" || P) && Ee.push(Ue.negative) : Ee.push(Ue.negative));
            else if (te.type === "plus") Ee.push(Ue.positive);
            else if (te.type === "text") Ee.push(_);
            else if (te.type === "div") je ? Ee.push("/") : g.num_min > 0 || g.den_min > 0 ? Ee.push(X["?"]) : Ee.push(X["#"]);
            else if (te.type === "int") if (g.int_pattern.length === 1) Ee.push(I);
            else {
              const $e = qe ? g.int_pattern.join("").length - ve.int : 1 / 0, At = qe === g.int_pattern.length - 1 ? 0 : g.int_pattern.join("").length - (ve.int + te.num.length);
              Ee.push(I.substring(I.length - $e, I.length - At)), qe++, ve.int += te.num.length;
            }
            else if (te.type === "frac") {
              const $e = ve.frac;
              for (let At = 0; At < ut; At++) Ee.push(P[At + $e] || X[te.num[At]]);
              ve.frac += ut;
            } else if (te.type in B) g[te.type + "_pattern"].length === 1 ? (te.type === "int" && Ee.push(I), te.type === "frac" && Ee.push(P), te.type === "man" && Ee.push(N), te.type === "num" && Ee.push(L), te.type === "den" && Ee.push(x)) : (Ee.push(B[te.type].slice(ve[te.type], ve[te.type] + ut)), ve[te.type] += ut);
            else if (te.type === "year") me < 0 && Ee.push(Ue.negative), Ee.push(String(Math.abs(me)).padStart(4, "0"));
            else if (te.type === "year-short") {
              const $e = me % 100;
              Ee.push($e < 10 ? "0" : "", $e);
            } else if (te.type === "month") Ee.push(te.pad && ye < 10 ? "0" : "", ye);
            else if (te.type === "monthname-single") g.date_system === 6 ? Ee.push(Ue.mmmm6[ye - 1].charAt(0)) : Ee.push(Ue.mmmm[ye - 1].charAt(0));
            else if (te.type === "monthname-short") g.date_system === 6 ? Ee.push(Ue.mmm6[ye - 1]) : Ee.push(Ue.mmm[ye - 1]);
            else if (te.type === "monthname") g.date_system === 6 ? Ee.push(Ue.mmmm6[ye - 1]) : Ee.push(Ue.mmmm[ye - 1]);
            else if (te.type === "weekday-short") Ee.push(Ue.ddd[D]);
            else if (te.type === "weekday") Ee.push(Ue.dddd[D]);
            else if (te.type === "day") Ee.push(te.pad && le < 10 ? "0" : "", le);
            else if (te.type === "hour") {
              const $e = q % g.clock || (g.clock < 24 ? g.clock : 0);
              Ee.push(te.pad && $e < 10 ? "0" : "", $e);
            } else if (te.type === "min") Ee.push(te.pad && Ce < 10 ? "0" : "", Ce);
            else if (te.type === "sec") Ee.push(te.pad && Se < 10 ? "0" : "", Se);
            else if (te.type === "subsec") {
              Ee.push(Ue.decimal);
              const $e = Le.toFixed(g.sec_decimals);
              Ee.push($e.slice(2, 2 + te.decimals));
            } else if (te.type === "am") {
              const $e = q < 12 ? 0 : 1;
              te.short && !S ? Ee.push("AP"[$e]) : Ee.push(Ue.ampm[$e]);
            } else if (te.type === "hour-elap") {
              _ < 0 && Ee.push(Ue.negative);
              const $e = 24 * _e + Math.floor(Math.abs(J) / 3600);
              Ee.push(String(Math.abs($e)).padStart(te.pad, "0"));
            } else if (te.type === "min-elap") {
              _ < 0 && Ee.push(Ue.negative);
              const $e = 1440 * _e + Math.floor(Math.abs(J) / 60);
              Ee.push(String(Math.abs($e)).padStart(te.pad, "0"));
            } else if (te.type === "sec-elap") {
              _ < 0 && Ee.push(Ue.negative);
              const $e = _e * oe + Math.abs(J);
              Ee.push(String(Math.abs($e)).padStart(te.pad, "0"));
            } else if (te.type === "b-year") Ee.push(me + 543);
            else if (te.type === "b-year-short") {
              const $e = (me + 543) % 100;
              Ee.push($e < 10 ? "0" : "", $e);
            }
          }
          return p.nbsp ? Ee.join("") : Ee.join("").replace(/\u00a0/g, " ");
        }
        function pe(_, g) {
          for (let p = 0; p < 3; p++) {
            const S = g[p];
            if (S) {
              let N;
              if (S.condition) {
                const L = S.condition[0], x = S.condition[1];
                L === "=" ? N = _ === x : L === ">" ? N = _ > x : L === "<" ? N = _ < x : L === ">=" ? N = _ >= x : L === "<=" ? N = _ <= x : L === "<>" && (N = _ !== x);
              } else N = !0;
              if (N) return S;
            }
          }
        }
        const Oe = j("@"), Me = "black", G = {};
        function Re(_, g) {
          if (_) {
            const p = _[0];
            g[p] = g[p] || {}, Re(_.slice(1), g[p]);
          } else g.$ = !0;
        }
        ["d-F-y", "d-F-Y", "d-M-y", "d-M-Y", "F-d-y", "F-d-Y", "F-j-y", "F-j-Y", "j-F-y", "j-F-Y", "j-M-y", "j-M-Y", "M-d-y", "M-d-Y", "M-j-y", "M-j-Y", "m-d-y", "m-d-Y", "m-j-y", "m-j-Y", "n-d-y", "n-d-Y", "n-j-y", "n-j-Y", "y-F-d", "y-F-j", "y-M-d", "y-M-j", "Y-F-d", "Y-F-j", "Y-M-d", "Y-m-d", "Y-M-j", "Y-m-j", "Y-n-d", "Y-n-j", "j-F", "j-M", "d-F", "d-M", "n-d", "n-j", "n-Y", "m-d", "m-j", "m-Y", "M-Y", "M-y", "F-y", "F-Y", "Y-M", "Y-n", "Y-m", "Y-F", "Y-M"].forEach((_) => {
          Re(_, G), Re(_ + " x", G), Re(_ + " l", G), Re(_ + " l x", G), Re("l " + _, G), Re("l " + _ + " x", G), Re(_ + " D", G), Re(_ + " D x", G), Re("D " + _, G), Re("D " + _ + " x", G);
        });
        const He = { jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12 }, Be = { january: 1, february: 2, march: 3, april: 4, june: 6, july: 7, august: 8, september: 9, october: 10, november: 11, december: 12 }, xe = { sunday: "l", monday: "l", tuesday: "l", wednesday: "l", thursday: "l", friday: "l", saturday: "l", sun: "D", mon: "D", tue: "D", wed: "D", thu: "D", fri: "D", sat: "D" }, Je = (/* @__PURE__ */ new Date()).getUTCFullYear();
        function Rt(_) {
          const g = new RegExp("^([\\s+%" + A.join("") + "(-]*)(((?:(?:\\d[\\d,]*)(?:\\.\\d*)?|(?:\\.\\d+)))([eE][+-]?\\d+)?)([\\s%" + A.join("") + ")]*)$").exec(_);
          if (g) {
            const [, p, S, N, L, x] = g;
            let P = 1, I = "", Q = !1, _e = !1, J = !1, me = !1, ye = !1, le = null, D = !1, q = parseFloat(S.replace(/,/g, ""));
            if (!isFinite(q)) return null;
            for (let Se = 0; Se < p.length; Se++) {
              const Le = p[Se];
              if (Le === "-") {
                if (Q || _e) return null;
                Q = !0, P = -1;
              } else if (H.test(Le)) {
                if (ye) return null;
                ye = !0, le = Le;
              } else if (Le === "(") {
                if (_e || Q) return null;
                _e = !0, P = -1;
              } else if (Le === "%") {
                if (me) return null;
                me = !0;
              }
            }
            for (let Se = 0; Se < x.length; Se++) {
              const Le = x[Se];
              if (H.test(Le)) {
                if (ye) return null;
                ye = !0, le = Le, D = !0;
              } else if (Le === ")") {
                if (J || !_e) return null;
                J = !0;
              } else if (Le === "%") {
                if (me) return null;
                me = !0;
              }
            }
            if (L) {
              if (me || ye) return null;
              I = "0.00E+00";
            } else if (me) {
              if (ye) return null;
              I = N.includes(".") ? "0.00%" : "0%", q *= 0.01;
            } else if (ye) {
              const Se = N.includes(".") ? "#,##0.00" : "#,##0";
              I = D ? Se + le : le + Se;
            } else N.includes(",") && (I = N.includes(".") ? "#,##0.00" : "#,##0");
            const Ce = { v: q * P };
            return I && (Ce.z = I), Ce;
          }
        }
        const We = (_, g, p) => {
          const S = p.path || "", N = Object.keys(g);
          for (let L = 0; L < N.length; L++) {
            let x;
            const P = N[L];
            if (g[P]) {
              if (P === "$" || P === "€") _ || (x = p);
              else if (P === "-") {
                const I = /^(\s*([./-]|,\s)\s*|\s+)/.exec(_);
                if (I) {
                  const Q = I[1] === "-" || I[1] === "/" || I[1] === "." ? I[1] : " ";
                  if (!p.sep || p.sep === Q) {
                    const _e = I[0].replace(/\s+/g, " ");
                    x = We(_.slice(I[0].length), g[P], { ...p, sep: Q, path: S + _e });
                  }
                }
              } else if (P === " ") {
                const I = /^[,.]?\s+/.exec(_);
                if (I) {
                  const Q = I[0].replace(/\s+/g, " ");
                  x = We(_.slice(I[0].length), g[P], { ...p, path: S + Q });
                }
              } else if (P === "j" || P === "d") {
                const I = /^(0?[1-9]|1\d|2\d|3[01])\b/.exec(_);
                I && (x = We(_.slice(I[0].length), g[P], { ...p, day: I[0], path: S + P }));
              } else if (P === "n" || P === "m") {
                const I = /^(0?[1-9]|1[012])\b/.exec(_);
                I && (x = We(_.slice(I[0].length), g[P], { ...p, month: +I[0], _mon: I[0], path: S + P }));
              } else if (P === "F" || P === "M") {
                const I = /^([a-z]{3,9})\b/i.exec(_), Q = I && (P === "F" ? Be : He)[I[0].toLowerCase()];
                Q && (x = We(_.slice(I[0].length), g[P], { ...p, month: Q, _mon: I[0], path: S + P }));
              } else if (P === "l" || P === "D") {
                const I = /^([a-z]{3,9})\b/i.exec(_);
                (I && xe[I[0].toLowerCase()]) === P && (x = We(_.slice(I[0].length), g[P], { ...p, path: S + P }));
              } else if (P === "y") {
                const I = /^\d\d\b/.exec(_);
                if (I) {
                  const Q = +I[0] >= 30 ? +I[0] + 1900 : +I[0] + 2e3;
                  x = We(_.slice(I[0].length), g[P], { ...p, year: Q, path: S + P });
                }
              } else if (P === "Y") {
                const I = /^\d\d\d\d\b/.exec(_);
                I && (x = We(_.slice(I[0].length), g[P], { ...p, year: +I[0], path: S + P }));
              } else {
                if (P !== "x") throw new Error('Unknown date token "'.concat(P, '"'));
                {
                  const I = ze(_);
                  I && (x = We("", g[P], { ...p, time: I.v, tf: I.z, path: S + P }));
                }
              }
              if (x) return x;
            }
          }
        };
        function et(_, g) {
          const p = We(_.trim(), G, { path: "" });
          if (p) {
            var S;
            if (p.sep === "." && p.path.length === 3) return null;
            const N = +((S = p.year) !== null && S !== void 0 ? S : Je);
            if (p.day || (p.day = 1), !function(P, I, Q) {
              if (Q < 1 || I < 1 || I > 12) return !1;
              if (I === 2) {
                if (Q > (P % 4 == 0 && P % 100 != 0 || P % 400 == 0 || P === 1900 ? 29 : 28)) return !1;
              } else if ((I === 4 || I === 6 || I === 9 || I === 11) && Q > 30 || (I === 1 || I === 3 || I === 5 || I === 7 || I === 8 || I === 10 || I === 12) && Q > 31) return !1;
              return !0;
            }(N, p.month, p.day)) return null;
            let L = -1 / 0;
            if (N < 1900) return null;
            N <= 1900 && p.month <= 2 ? L = 25568 : N < 1e4 && (L = 25569);
            const x = Date.UTC(N, p.month - 1, p.day) / 864e5 + L + (p.time || 0);
            if (x >= 0 && x <= 2958465) {
              const P = p._mon[0] === "0" || p.day[0] === "0" || p._mon.length === 2 && p.day.length === 2, I = p.path.replace(/[jdlDnmMFyYx-]/g, (Q) => Q === "j" || Q === "d" ? P ? "dd" : "d" : Q === "D" ? "ddd" : Q === "l" ? "dddd" : Q === "n" || Q === "m" ? P ? "mm" : "m" : Q === "M" ? "mmm" : Q === "F" ? "mmmm" : Q === "y" ? "yy" : Q === "x" ? p.tf || "" : Q === "Y" ? "yyyy" : Q);
              return g && g.nativeDate ? { v: Ae(x, g), z: I } : { v: x, z: I };
            }
          }
          return null;
        }
        function ze(_) {
          const g = /^\s*([10]?\d|2[0-4])(?::([0-5]\d|\d))?(?::([0-5]\d|\d))?(\.\d{1,10})?(?:\s*([AP])M?)?\s*$/i.exec(_);
          if (g) {
            const [, p, S, N, L, x] = g;
            if (L && !N || !x && !S && !N) return null;
            let P = 1 * (p || 0);
            if (x) {
              if (P >= 13) return null;
              x[0] !== "p" && x[0] !== "P" || (P += 12);
            }
            return { v: (60 * P * 60 + 60 * (1 * (S || 0)) + 1 * (N || 0) + 1 * (L || 0)) / 86400, z: (p.length === 2 ? "hh" : "h") + ":mm" + (N ? ":ss" : "") + (x ? " AM/PM" : "") };
          }
          return null;
        }
        function ct(_) {
          return /^\s*true\s*$/i.test(_) ? { v: !0 } : /^\s*false\s*$/i.test(_) ? { v: !1 } : null;
        }
        const it = {};
        function xt(_, g) {
          const { pattern: p, partitions: S, locale: N } = _, L = (I) => {
            const Q = Object.assign({}, ne(), g, I);
            return N && (Q.locale = N), Q;
          }, x = (I, Q) => {
            const _e = L(Q);
            return function(J, me, ye) {
              const le = l(ye.locale), D = me[3] ? me[3] : Oe;
              if (typeof J == "boolean" && (J = J ? "TRUE" : "FALSE"), J == null) return "";
              if (typeof J != "number") return ie(J, D, ye, le);
              if (!isFinite(J)) {
                const Ce = le || f;
                return isNaN(J) ? Ce.nan : (J < 0 ? Ce.negative : "") + Ce.infinity;
              }
              const q = pe(J, me);
              return q ? ie(J, q, ye, le) : ye.overflow;
            }(ge(I, _e), S, _e);
          };
          x.color = (I, Q) => function(_e, J) {
            if (typeof _e != "number" || !isFinite(_e)) return (J[3] ? J[3].color : Oe.color) || Me;
            const me = pe(_e, J);
            return me && me.color || Me;
          }(ge(I, L(Q)), S);
          const P = function(I) {
            var Q;
            let _e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : null;
            const [J, me] = I, ye = J.frac_max, le = { type: "general", isDate: v(I), isText: F(I), isPercent: be(I), maxDecimals: J.general ? 9 : ye, scale: (Q = J.scale) !== null && Q !== void 0 ? Q : 1, color: 0, parentheses: 0, grouped: J.grouping ? 1 : 0, _partitions: I }, D = !le.isDate && !le.isText && !J.error && J.tokens.some((Ue) => Ue.type === "string" && (_e ? Ue.value === _e : H.test(Ue.value)));
            let q = "G", Ce = ye >= 0 ? Math.min(15, ye) : "", Se = "", Le = "";
            if (me && me.color && (Le = "-", le.color = 1), J.parens && (Se = "()", le.parentheses = 1), D) q = "C", le.type = "currency";
            else if (J.error) le.type = "error", le.maxDecimals = 0;
            else if (le.isDate) {
              let Ue = 0, je = 0, dt = "";
              J.tokens.forEach((Ee) => {
                const qe = Ee.type;
                /^(b-)?year/.test(qe) ? (dt += "Y", je++) : qe.startsWith("month") ? (dt += "M", je++) : /^(week)?day/.test(qe) ? (dt += "D", je++) : qe !== "hour" && qe !== "min" && qe !== "sec" && qe !== "am" || (dt += qe[0], Ue++);
              }), le.type = "date", je && Ue ? le.type = "datetime" : !je && Ue && (le.type = "time");
              const pt = K.find((Ee) => dt.startsWith(Ee[0]));
              q = pt ? "D" : "G", Ce = pt ? pt[1] : "";
            } else le.isText ? (q = "G", le.type = "text", Ce = "", le.maxDecimals = 0) : J.general ? (q = "G", le.type = "general", Ce = "") : J.fractions ? (q = "G", le.type = "fraction", Ce = "") : J.exponential ? (q = "S", le.type = "scientific") : le.isPercent ? (q = "P", le.type = "percent") : J.grouping ? (q = ",", le.type = "grouped") : (J.int_max || ye) && (q = "F", le.type = "number");
            return le.code = q + Ce + Le + Se, le.level = V[le.type], Object.freeze(le);
          }(S, (g || {}).currency) || new SyntaxError();
          return x.info = P, x.dateInfo = function(I) {
            const [Q] = I;
            return { year: !!(2 & Q.date), month: !!(4 & Q.date), day: !!(8 & Q.date), hours: !!(16 & Q.date), minutes: !!(32 & Q.date), seconds: !!(64 & Q.date), clockType: Q.clock === 12 ? 12 : 24 };
          }(S), x.isPercent = () => !!P.isPercent, x.isDate = () => !!P.isDate, x.isText = () => !!P.isText, x.pattern = p, _.error && (x.error = _.error), x.options = L, x.locale = N || g && g.locale || "", Object.freeze(x);
        }
        function ke(_, g) {
          _ || (_ = "General");
          let p = null;
          return it[_] ? p = it[_] : (p = Object.assign({}, ne(), g).throws ? M(_) : function(S) {
            try {
              return M(S);
            } catch (N) {
              const L = { tokens: [{ type: "error" }], error: N.message };
              return { pattern: S, partitions: [L, L, L, L], error: N.message, locale: null };
            }
          }(_), p.error || (it[_] = p)), xt(p, g);
        }
        ke.isDate = (_) => ke(_, { throws: !1 }).isDate(), ke.isPercent = (_) => ke(_, { throws: !1 }).isPercent(), ke.isText = (_) => ke(_, { throws: !1 }).isText(), ke.getInfo = (_, g) => ke(_, { ...g, throws: !1 }).info, ke.getDateInfo = (_, g) => ke(_, { ...g, throws: !1 }).dateInfo, ke.dateToSerial = ge, ke.dateFromSerial = Ae, ke.options = ne, ke.dec2frac = R, ke.round = E, ke.codeToLocale = s, ke.parseLocale = u, ke.getLocale = l, ke.addLocale = (_, g) => {
          const p = u(g);
          return delete it[p.lang], delete it[p.language], d(_, p);
        }, ke.format = function(_, g, p) {
          let S = arguments.length > 3 && arguments[3] !== void 0 && arguments[3];
          const N = p && typeof p == "object" ? p : { locale: p, throws: !S };
          return ke(_, N)(ge(g, N), N);
        }, ke.is_date = ke.isDate, ke.parseNumber = Rt, ke.parseDate = et, ke.parseTime = ze, ke.parseBool = ct, ke.parseValue = function(_, g) {
          var p, S, N;
          return (p = (S = (N = Rt(_)) !== null && N !== void 0 ? N : et(_, g)) !== null && S !== void 0 ? S : ze(_)) !== null && p !== void 0 ? p : ct(_);
        };
        var ht = ke;
        return r = r.default;
      }();
    });
  }(Yr)), Yr.exports;
}
var As, Yo;
function vp() {
  return Yo || (Yo = 1, As = Ip()), As;
}
var yp = vp();
const wp = /* @__PURE__ */ wt(yp), Op = wp;
function fn(t) {
  let e = 0;
  const n = Object.keys(t);
  for (const r of n) {
    const s = Number(r);
    e = Math.max(e, s);
  }
  return e + 1;
}
function Vo(t, e, n) {
  const r = fn(n), s = n;
  for (let i = r - 1; i >= t; i--)
    s[i + 1] = s[i];
  s[t] = e;
}
function Go(t, e, n) {
  const r = Object.keys(n).reduce((s, i) => Math.max(s, Number.parseInt(i)), 0) + 1;
  for (let s = t; s < r; s++)
    s < t + e ? delete n[s] : n[s] !== void 0 && (n[s - e] = n[s], delete n[s]);
}
function LC(t, e) {
  const n = t, r = Object.keys(n), s = r.length, i = e, o = Object.keys(i), a = o.length, u = {};
  let c = 0;
  for (let l = 0; l < s; l++, c++) {
    const h = r[l];
    u[c] = n[h];
  }
  for (let l = 0; l < a; l++, c++) {
    const h = o[l];
    u[c] = i[h];
  }
  return u;
}
function UC(t, e, n) {
  const r = n;
  if (fn(n) > 0) {
    const i = {};
    let o = 0;
    for (let a = t; a <= e; a++)
      r[a] && (i[o] = r[a], o++);
    return i;
  }
  return {};
}
function Ko(t, e, n, r) {
  const s = t > n;
  if (!s && t + e > n)
    throw new Error("Invalid move operation");
  s ? bp(t, e, n, r) : Sp(t, e, n, r);
}
function bp(t, e, n, r) {
  const s = r, i = [];
  for (let o = t; o < t + e; o++)
    i.push(s[o]);
  for (let o = t - 1; o >= n; o--) {
    const a = s[o];
    s[o + e] = a, a === void 0 && delete s[o + e];
  }
  i.forEach((o, a) => {
    s[n + a] = o, o === void 0 && delete s[n + a];
  });
}
function Sp(t, e, n, r) {
  const s = r, i = [];
  for (let o = t; o < t + e; o++)
    i.push(s[o]);
  for (let o = t + e; o < n; o++) {
    const a = s[o];
    s[o - e] = a, a === void 0 && delete s[o - e];
  }
  i.forEach((o, a) => {
    s[n + a - e] = o, o === void 0 && delete s[n + a - e];
  });
}
class kt {
  constructor(e = {}) {
    C(this, "_matrix");
    this._setOriginValue(e);
  }
  static MakeObjectMatrixSize(e) {
    return new kt({
      [e - 1]: {}
    });
  }
  getMatrix() {
    return this._matrix;
  }
  forEach(e) {
    const n = this._matrix, r = Object.keys(n);
    for (const s of r) {
      const i = Number(s), o = n[i];
      if (e(i, o) === !1)
        return this;
    }
    return this;
  }
  forRow(e) {
    const n = this._matrix, r = Object.keys(n);
    for (const s of r) {
      const i = Number(s), o = n[i];
      if (e(
        i,
        Object.keys(o).map((u) => Number(u))
      ) === !1)
        return this;
    }
    return this;
  }
  /**
   * Iterate the object matrix with row priority, which means it scan the whole range row by row.
   */
  forValue(e) {
    const n = this._matrix;
    for (const r in n) {
      const s = Number(r), i = n[s];
      if (i)
        for (const o in i) {
          const a = Number(o), u = i[a];
          if (e(s, a, u) === !1)
            return this;
        }
    }
    return this;
  }
  swapRow(e, n) {
    const r = this._matrix[e], s = this._matrix[n];
    this._matrix[e] = s, this._matrix[n] = r;
  }
  getRow(e) {
    return this._matrix[e];
  }
  getRowOrCreate(e) {
    let n = this.getRow(e);
    return n == null && (n = {}, this._matrix[e] = n), n;
  }
  reset() {
    this._setOriginValue({});
  }
  hasValue() {
    const e = this._matrix, n = Object.keys(e);
    if (n.length === 0)
      return !1;
    for (const r of n) {
      const s = Number(r), i = e[s];
      if (Object.keys(i).length > 0)
        return !0;
    }
    return !1;
  }
  getValue(e, n) {
    var r, s;
    return (s = (r = this._matrix) == null ? void 0 : r[e]) == null ? void 0 : s[n];
  }
  setValue(e, n, r) {
    const s = this.getRowOrCreate(e);
    s[n] = r;
  }
  /**
   * ！！
   * Please +1 ‘！’, who fell into this pit.
   * @deprecated use `realDelete` or `splice`
   */
  deleteValue(e, n) {
    var r, s;
    (s = (r = this._matrix) == null ? void 0 : r[e]) == null || delete s[n];
  }
  realDeleteValue(e, n) {
    var r, s, i;
    if ((s = (r = this._matrix) == null ? void 0 : r[e]) == null || delete s[n], this.getRow(e)) {
      const o = this.getRow(e);
      if (o == null)
        return;
      Object.keys(o).length === 0 && ((i = this._matrix) == null || delete i[e]);
    }
  }
  setRow(e, n) {
    this._matrix[e] = n;
  }
  moveRows(e, n, r) {
    Ko(e, n, r, this._matrix);
  }
  moveColumns(e, n, r) {
    this.forEach((s, i) => {
      Ko(e, n, r, i);
    });
  }
  insertRows(e, n) {
    for (let r = e; r < e + n; r++)
      Vo(r, {}, this._matrix);
  }
  insertColumns(e, n) {
    for (let r = e; r < e + n; r++)
      this.forEach((s, i) => {
        i && Vo(r, void 0, i);
      });
  }
  removeRows(e, n) {
    Go(e, n, this._matrix);
  }
  removeColumns(e, n) {
    this.forEach((r, s) => {
      s && Go(e, n, s);
    });
  }
  /**
   * Return a fragment of the original data matrix. Note that the returned matrix's row matrix would start from
   * 0 not `startRow`. Neither does its column matrix. If you want to get the original matrix, use `getSlice`.
   *
   * @param startRow
   * @param endRow
   * @param startColumn
   * @param endColumn
   * @returns
   */
  getFragment(e, n, r, s) {
    const i = new kt();
    let o = 0;
    for (let a = e; a <= n; a++) {
      const u = {};
      let c = 0;
      for (let l = r; l <= s; l++) {
        const h = this.getValue(a, l);
        u[c] = h, c++;
      }
      i.setRow(o, u), o++;
    }
    return i;
  }
  /**
   * Return a slice of the original data matrix. Note that the returned matrix's row matrix would start from
   * `startRow` not 0, and the same does its column index. You may be looking for `getFragment` if you want
   * both of the indexes start from 0.
   *
   * @param startRow
   * @param endRow
   * @param startColumn
   * @param endColumn
   * @returns
   */
  getSlice(e, n, r, s) {
    const i = new kt();
    for (let o = e; o <= n; o++)
      for (let a = r; a <= s; a++) {
        const u = this.getValue(o, a);
        u && i.setValue(o, a, re.deepClone(u));
      }
    return i;
  }
  getSizeOf() {
    return Object.keys(this._matrix).length;
  }
  getLength() {
    return fn(this._matrix);
  }
  getRange() {
    const r = this.getLength() - 1;
    let s = 0;
    const i = this.getLength();
    for (let o = 0; o < i; o++) {
      const a = this.getRow(o);
      if (a) {
        const u = fn(a) - 1;
        s = u > s ? u : s;
      }
    }
    return {
      startRow: 0,
      startColumn: 0,
      endRow: r,
      endColumn: s
    };
  }
  toNativeArray() {
    const e = new Array();
    return this.forValue((n, r, s) => {
      e.push(s);
    }), e;
  }
  toArray() {
    const e = [];
    return this.forRow((n, r) => {
      e[n] == null && (e[n] = []), r.forEach((s) => {
        e[n][s] = this.getValue(n, s);
      });
    }), e;
  }
  toFullArray() {
    const e = this.getRange(), { endColumn: n, endRow: r } = e, s = [];
    for (let i = 0; i <= r; i++) {
      const o = new Array(n + 1).fill(void 0);
      s.push(o);
    }
    return this.forValue((i, o, a) => {
      s[i][o] = a;
    }), s;
  }
  /**
   * @deprecated Use getMatrix as a substitute.
   */
  toJSON() {
    return this._matrix;
  }
  clone() {
    const e = JSON.stringify(this._matrix);
    return JSON.parse(e);
  }
  /**
   * @deprecated Use clone as a substitute.
   */
  getData() {
    const e = JSON.stringify(this._matrix);
    return JSON.parse(e);
  }
  getArrayData() {
    let e = 0, n = 0, r = !1, s = !1;
    const i = new kt();
    return this.forEach((o, a) => {
      r || (r = !0, e = o), Object.keys(a).forEach((u) => {
        const c = Number(u);
        s ? c < n && (n = c) : (s = !0, n = c);
        const l = this.getValue(o, c);
        i.setValue(o - e, c - n, l);
      });
    }), i.getData();
  }
  /**
   * the function can only be used in all the row and column are positive integer
   * @description the positive integer in V8 Object is stored in a fast memory space and it is sorted  when we get the keys
   * @returns {IRange} the start and end scope of the matrix
   */
  getStartEndScope() {
    let e = 1 / 0, n = -1 / 0, r = 1 / 0, s = -1 / 0;
    const i = Object.keys(this._matrix);
    i.length > 0 && (e = +i[0], n = +i[i.length - 1]);
    for (const o of i) {
      const a = Object.keys(this._matrix[o]);
      a.length > 0 && (r = Math.min(r, +a[0]), s = Math.max(s, +a[a.length - 1]));
    }
    return { startRow: e, endRow: n, startColumn: r, endColumn: s };
  }
  getDataRange() {
    let e = 0, n = 0, r = 0, s = -1, i = !1, o = !1;
    return this.forEach((a, u) => {
      if (i || (i = !0, e = a), u == null)
        return;
      const c = fn(u) - 1;
      c > r && (r = c), Object.keys(u).forEach((l) => {
        const h = Number(l);
        o ? h < n && (n = h) : (o = !0, n = h);
      }), a > s && (s = a);
    }), {
      startRow: e,
      startColumn: n,
      endRow: s,
      endColumn: r
    };
  }
  getDiscreteRanges() {
    const e = [];
    return this.forEach((n, r) => {
      Object.keys(r).forEach((s) => {
        const i = Number(s);
        let o = !1;
        for (const a of e)
          if (n >= a.startRow && n <= a.endRow + 1 && i >= a.startColumn && i <= a.endColumn + 1) {
            a.endRow = Math.max(n, a.endRow), a.endColumn = Math.max(i, a.endColumn), o = !0;
            break;
          }
        o || e.push({
          startRow: n,
          endRow: n,
          startColumn: i,
          endColumn: i
        });
      });
    }), e;
  }
  merge(e) {
    this.forValue((n, r) => {
      const s = e.getValue(n, r);
      s != null && this.setValue(n, r, s);
    });
  }
  _setOriginValue(e = {}) {
    this._matrix = e;
  }
}
const PC = {
  sheetId: "",
  range: {
    startRow: -1,
    endRow: -1,
    startColumn: -1,
    endColumn: -1
  }
}, kC = {
  startRow: -1,
  startColumn: -1,
  endRow: -1,
  endColumn: -1
}, FC = {
  startRow: 0,
  startColumn: 0,
  endRow: 0,
  endColumn: 0
}, $C = {
  row: 0,
  column: 0
}, gt = {
  /**
   * fontFamily
   */
  ff: "Arial",
  /**
   * fontSize
   */
  fs: 11,
  /**
   * italic
   * 0: false
   * 1: true
   */
  it: we.FALSE,
  /**
   * bold
   * 0: false
   * 1: true
   */
  bl: we.FALSE,
  /**
   * underline
   */
  ul: {
    s: we.FALSE
  },
  /**
   * strikethrough
   */
  st: {
    s: we.FALSE
  },
  /**
   * overline
   */
  ol: {
    s: we.FALSE
  },
  /**
   * textRotation
   */
  tr: {
    a: 0,
    /**
     * true : 1
     * false : 0
     */
    v: we.FALSE
  },
  /**
   * textDirection
   */
  td: er.UNSPECIFIED,
  /**
   * color
   */
  cl: {
    rgb: "#000"
  },
  /**
   * background
   */
  bg: {
    rgb: "#fff"
  },
  /**
   * horizontalAlignment
   */
  ht: Xt.UNSPECIFIED,
  /**
   * verticalAlignment
   */
  vt: hn.UNSPECIFIED,
  /**
   * wrapStrategy
   */
  tb: xn.UNSPECIFIED,
  /**
   * padding
   */
  pd: {
    t: 0,
    r: 0,
    b: 0,
    l: 0
  },
  n: null,
  /**
   * border
   */
  bd: {
    b: null,
    l: null,
    r: null,
    t: null
  }
}, Ap = {
  id: "default_slide",
  title: "defaultSlide",
  pageSize: {
    width: 300,
    height: 300
  }
}, BC = [su, Hd, iu];
var Np = /* @__PURE__ */ ((t) => (t.ARRAY_CONVERTOR = "ARRAY_CONVERTOR", t.MATRIX_CONVERTOR = "MATRIX_CONVERTOR", t))(Np || {});
function Rr(t, e) {
  const { textRuns: n = [] } = e;
  let r = 0;
  for (const i of n) {
    const { ts: o = {}, st: a, ed: u } = i;
    if (o[t] == null)
      return we.FALSE;
    switch (t) {
      case "bl":
      // fallthrough
      case "it": {
        if (o[t] === we.FALSE)
          return we.FALSE;
        break;
      }
      case "ul":
      // fallthrough
      case "st": {
        if (o[t].s === we.FALSE)
          return we.FALSE;
        break;
      }
      default:
        throw new Error(`unknown style key: ${t} in IStyleBase`);
    }
    r += u - a;
  }
  return e.dataStream.indexOf(`\r
`) === r ? we.TRUE : we.FALSE;
}
const Qn = class Qn {
  constructor(e, n, r) {
    C(this, "_range");
    C(this, "_worksheet");
    this._deps = r, this._range = n, this._worksheet = e;
  }
  static foreach(e, n) {
    const { startRow: r, startColumn: s, endRow: i, endColumn: o } = e;
    for (let a = r; a <= i; a++)
      for (let u = s; u <= o; u++)
        n(a, u);
  }
  /**
   * get current range data
   *
   * @returns current range
   */
  getRangeData() {
    return this._range;
  }
  /**
   * Returns the value of the top-left cell in the range. The value may be of type Number, Boolean, Date, or String
   * depending on the value of the cell. Empty cells return an empty string.
   * @returns  The value in this cell
   */
  getValue() {
    return this.getValues()[0][0];
  }
  /**
   * Returns the rectangular grid of values for this range.
   *
   * Returns a two-dimensional array of values, indexed by row, then by column. The values may be of type Number,
   * Boolean, Date, or String, depending on the value of the cell. Empty cells are represented by an empty string
   * in the array. Remember that while a range index starts at 0, 0, same as the JavaScript array is indexed from [0][0].
   *
   * In web apps, a Date value isn't a legal parameter. getValues() fails to return data to a web app if the range
   * contains a cell with a Date value. Instead, transform all the values retrieved from the sheet to a supported
   * JavaScript primitive like a Number, Boolean, or String.
   *
   * @returns  A two-dimensional array of values.
   */
  getValues() {
    const { startRow: e, endRow: n, startColumn: r, endColumn: s } = this._range, i = [];
    for (let o = e; o <= n; o++) {
      const a = [];
      for (let u = r; u <= s; u++)
        a.push(this.getMatrix().getValue(o, u) || null);
      i.push(a);
    }
    return i;
  }
  /**
   * get range matrix
   *
   * @returns range matrix
   */
  getMatrix() {
    const { startRow: e, endRow: n, startColumn: r, endColumn: s } = this._range, i = this._worksheet.getCellMatrix(), o = new kt();
    for (let a = e; a <= n; a++)
      for (let u = r; u <= s; u++)
        o.setValue(a, u, i.getValue(a, u) || null);
    return o;
  }
  /**
   * get range matrix object
   *
   * @returns range matrix object
   */
  getMatrixObject() {
    const { startRow: e, endRow: n, startColumn: r, endColumn: s } = this._range, i = this._worksheet.getCellMatrix(), o = new kt();
    for (let a = e; a <= n; a++)
      for (let u = r; u <= s; u++)
        o.setValue(a - e, u - r, i.getValue(a, u) || {});
    return o;
  }
  /**
   * Returns a string description of the range, in A1 notation.
   *
   * @returns The string description of the range in A1 notation.
   */
  getA1Notation() {
    const { startRow: e, endRow: n, startColumn: r, endColumn: s } = this._range;
    let i, o;
    return r < s ? (i = re.numToWord(r + 1) + (e + 1), o = re.numToWord(s + 1) + (n + 1)) : (i = re.numToWord(s + 1) + (n + 1), o = re.numToWord(r + 1) + (e + 1)), i === o ? `${i}` : `${i}:${o}`;
  }
  /**
   * Returns the background color of the top-left cell in the range (for example, '#ffffff').
   *
   * @returns — The color code of the background.
   */
  getBackground() {
    return this.getBackgrounds()[0][0];
  }
  /**
   * Returns the background colors of the cells in the range (for example, '#ffffff').
   *
   * @returns  — A two-dimensional array of color codes of the backgrounds.
   */
  getBackgrounds() {
    const e = this._deps.getStyles();
    return this.getValues().map(
      (n) => n.map((r) => {
        var i;
        const s = e.getStyleByCell(r);
        return ((i = s == null ? void 0 : s.bg) == null ? void 0 : i.rgb) || gt.bg.rgb;
      })
    );
  }
  /**
   * Returns a given cell within a range.
   *
   * The row and column here are relative to the range
   * e.g. "B2:D4", getCell(0,0) in this code returns the cell at B2
   * @returns  — A range containing a single cell at the specified coordinates.
   */
  getCell(e, n) {
    const { startRow: r, startColumn: s } = this._range, i = {
      startRow: r + e,
      endRow: r + e,
      startColumn: s + n,
      endColumn: s + n
    };
    return new Qn(this._worksheet, i, this._deps);
  }
  /**
   * Returns the starting column position for this range
   *
   * @returns  — The range's starting column position in the spreadsheet.
   */
  getColumn() {
    return this._range.startColumn;
  }
  /**
   * Returns the data of the object structure, and can set whether to bring styles
   */
  getObjectValue(e = {}) {
    return this.getObjectValues(e)[0][0];
  }
  /**
   * Returns the data of the object structure, and can set whether to bring styles
   *
   * @param options set whether to include style
   * @returns Returns a value in object format
   */
  getObjectValues(e = {}) {
    var a;
    const { startRow: n, endRow: r, startColumn: s, endColumn: i } = this._range, o = this._worksheet.getCellMatrix().getFragment(n, r, s, i).getData();
    if (e.isIncludeStyle) {
      const u = this._deps.getStyles();
      for (let c = 0; c <= r - n; c++)
        for (let l = 0; l <= i - s; l++) {
          if (o == null || ((a = o == null ? void 0 : o[c]) == null ? void 0 : a[l]) == null)
            continue;
          const h = o[c][l].s;
          h && (o[c][l].s = u.get(h));
        }
    }
    return o;
  }
  /**
   * Returns the font color of the cell in the top-left corner of the range, in CSS notation
   */
  getFontColor() {
    return this.getFontColors()[0][0];
  }
  /**
   * Returns the font colors of the cells in the range in CSS notation (such as '#ffffff' or 'white').
   */
  getFontColors() {
    const e = this._deps.getStyles();
    return this.getValues().map(
      (n) => n.map((r) => {
        var i;
        const s = e.getStyleByCell(r);
        return ((i = s == null ? void 0 : s.cl) == null ? void 0 : i.rgb) || gt.cl.rgb;
      })
    );
  }
  /**
   * Returns the font families of the cells in the range.
   */
  getFontFamilies() {
    return this._getStyles("ff");
  }
  /**
   * 	Returns the font family of the cell in the top-left corner of the range.
   */
  getFontFamily() {
    return this.getFontFamilies()[0][0];
  }
  /**
   * Returns the underlines of the cells in the range.
   */
  getUnderlines() {
    return this._getStyles("ul");
  }
  /**
   * Returns the underline of the cells in the range.
   */
  getUnderline() {
    var n, r;
    const { p: e } = (n = this.getValue()) != null ? n : {};
    return e && Array.isArray((r = e.body) == null ? void 0 : r.textRuns) && e.body.textRuns.length > 0 ? Rr("ul", e.body) === we.TRUE ? {
      s: we.TRUE
    } : {
      s: we.FALSE
    } : this.getUnderlines()[0][0];
  }
  /**
   * Returns the overlines of the cells in the range.
   */
  getOverlines() {
    return this._getStyles("ol");
  }
  /**
   * Returns the overline of the cells in the range.
   */
  getOverline() {
    return this.getOverlines()[0][0];
  }
  /**
   * Returns the strikeThrough of the cells in the range.
   */
  getStrikeThrough() {
    var n, r;
    const { p: e } = (n = this.getValue()) != null ? n : {};
    return e && Array.isArray((r = e.body) == null ? void 0 : r.textRuns) && e.body.textRuns.length > 0 ? Rr("st", e.body) === we.TRUE ? {
      s: we.TRUE
    } : {
      s: we.FALSE
    } : this.getStrikeThroughs()[0][0];
  }
  /**
   * Returns the strikeThroughs of the cells in the range.
   */
  getStrikeThroughs() {
    return this._getStyles("st");
  }
  /**
   * Returns the font size in point size of the cell in the top-left corner of the range.
   */
  getFontSize() {
    var n, r;
    const e = ((n = this.getValue()) == null ? void 0 : n.p) || {};
    return Array.isArray((r = e.body) == null ? void 0 : r.textRuns) && e.body.textRuns.length > 0 ? e.body.textRuns.some((s) => {
      var i;
      return ((i = s == null ? void 0 : s.ts) == null ? void 0 : i.fs) != null;
    }) ? Math.max(...e.body.textRuns.map((s) => {
      var i;
      return ((i = s == null ? void 0 : s.ts) == null ? void 0 : i.fs) || 0;
    })) : this.getFontSizes()[0][0] : this.getFontSizes()[0][0];
  }
  /**
   * Returns the font sizes of the cells in the range.
   */
  getFontSizes() {
    return this._getStyles("fs");
  }
  /**
   * Returns the border info of the cells in the range.
   */
  getBorder() {
    return this.getBorders()[0][0];
  }
  getBorders() {
    return this._getStyles("bd");
  }
  /**
   * Returns the font style ('italic' or 'normal') of the cell in the top-left corner of the range.
   */
  getFontStyle() {
    var n, r;
    const { p: e } = (n = this.getValue()) != null ? n : {};
    return e && Array.isArray((r = e.body) == null ? void 0 : r.textRuns) && e.body.textRuns.length > 0 ? Rr("it", e.body) === we.TRUE ? Vs.ITALIC : Vs.NORMAL : this._getFontStyles()[0][0];
  }
  /**
   * Returns the font styles of the cells in the range.
   */
  _getFontStyles() {
    return this._getStyles("it");
  }
  /**
   * Returns the font weight (normal/bold) of the cell in the top-left corner of the range.
   * If the cell has rich text, the return value according to the textRuns of the rich text,
   * when all styles of textRuns are bold, it will return FontWeight.BOLD,
   * otherwise return FontWeight.NORMAL.
   */
  getFontWeight() {
    var n, r;
    const { p: e } = (n = this.getValue()) != null ? n : {};
    return e && Array.isArray((r = e.body) == null ? void 0 : r.textRuns) && e.body.textRuns.length > 0 ? Rr("bl", e.body) === we.TRUE ? Gs.BOLD : Gs.NORMAL : this._getFontWeights()[0][0];
  }
  /**
   * Returns the font weights of the cells in the range.
   */
  _getFontWeights() {
    return this._getStyles("bl");
  }
  /**
   * Returns the grid ID of the range's parent sheet.
   */
  getGridId() {
    return this._worksheet.getSheetId();
  }
  /**
   * Returns the height of the range.
   */
  getHeight() {
    const { _range: e, _worksheet: n } = this, { startRow: r, endRow: s } = e;
    let i = 0;
    for (let o = 0; o <= s - r; o++) {
      const a = n.getRowHeight(o);
      i += a;
    }
    return i;
  }
  /**
   * 	Returns the horizontal alignment of the text (left/center/right) of the cell in the top-left corner of the range.
   */
  getHorizontalAlignment() {
    return this.getHorizontalAlignments()[0][0];
  }
  /**
   *Returns the horizontal alignments of the cells in the range.
   */
  getHorizontalAlignments() {
    return this._getStyles("ht");
  }
  /**
   * Returns the end column position.
   */
  getLastColumn() {
    return this._range.endColumn;
  }
  /**
   * 	Returns the end row position.
   */
  getLastRow() {
    return this._range.endRow;
  }
  /**
   * Returns the number of columns in this range.
   */
  getNumColumns() {
    const { startColumn: e, endColumn: n } = this._range;
    return n - e + 1;
  }
  /**
   * Returns the number of rows in this range.
   */
  getNumRows() {
    const { startRow: e, endRow: n } = this._range;
    return n - e + 1;
  }
  /**
   * Returns the Rich Text value for the top left cell of the range, or null if the cell value is not text.
   */
  getRichTextValue() {
    return this.getRichTextValues()[0][0];
  }
  /**
   * Returns the Rich Text values for the cells in the range.
   */
  getRichTextValues() {
    return this.getValues().map((e) => e.map((n) => (n == null ? void 0 : n.p) || ""));
  }
  /**
   * Returns the row position for this range.
   */
  getRowIndex() {
    return this._range.startRow;
  }
  /**
   * Returns the sheet this range belongs to.
   */
  getSheet() {
    return this._worksheet;
  }
  /**
   * Returns the text direction for the top left cell of the range.
   */
  getTextDirection() {
    return this.getTextDirections()[0][0];
  }
  /**
   * Returns the text directions for the cells in the range.
   */
  getTextDirections() {
    return this._getStyles("td");
  }
  /**
   * Returns the text rotation settings for the top left cell of the range.
   */
  // getTextRotation(): number {
  getTextRotation() {
    return this.getTextRotations()[0][0];
  }
  /**
   * Returns the text rotation settings for the cells in the range.
   */
  // getTextRotations(): number[][] {
  getTextRotations() {
    return this._getStyles("tr");
  }
  /**
   * 	Returns the text style for the top left cell of the range.
   */
  getTextStyle() {
    return this.getTextStyles()[0][0];
  }
  /**
   * Returns the text styles for the cells in the range.
   */
  getTextStyles() {
    const e = this._deps.getStyles();
    return this.getValues().map((n) => n.map((r) => e.getStyleByCell(r)));
  }
  /**
   * Returns the vertical alignment (top/middle/bottom) of the cell in the top-left corner of the range.
   */
  getVerticalAlignment() {
    return this.getVerticalAlignments()[0][0];
  }
  /**
   * Returns the vertical alignments of the cells in the range.
   */
  getVerticalAlignments() {
    return this._getStyles("vt");
  }
  /**
   * Returns the width of the range in columns.
   */
  getWidth() {
    const { _range: e, _worksheet: n } = this, { startColumn: r, endColumn: s } = e;
    let i = 0;
    for (let o = 0; o <= s - r; o++)
      i += n.getColumnWidth(o);
    return i;
  }
  /**
   * Returns whether the text in the cell wraps.
   */
  getWrap() {
    return this.getWrapStrategy() === xn.WRAP ? we.TRUE : we.FALSE;
  }
  /**
   * Returns the text wrapping strategies for the cells in the range.
   */
  getWrapStrategies() {
    return this._getStyles("tb");
  }
  /**
   * Returns the text wrapping strategy for the top left cell of the range.
   */
  getWrapStrategy() {
    return this.getWrapStrategies()[0][0];
  }
  forEach(e) {
    Qn.foreach(this._range, e);
  }
  /**
   *
   * @param arg Shorthand for the style that gets
   * @returns style value
   */
  _getStyles(e) {
    const n = this._deps.getStyles();
    return this.getValues().map(
      (r) => r.map((s) => {
        const i = n && n.getStyleByCell(s);
        return i && i[e] || gt[e];
      })
    );
  }
};
C(Qn, "transformRange", (e, n) => {
  const r = n.getMaxColumns() - 1, s = n.getMaxRows() - 1;
  return e.rangeType === De.ALL ? {
    startColumn: 0,
    startRow: 0,
    endColumn: r,
    endRow: s
  } : e.rangeType === De.COLUMN ? {
    startRow: 0,
    endRow: s,
    startColumn: e.startColumn,
    endColumn: e.endColumn
  } : e.rangeType === De.ROW ? {
    startColumn: 0,
    endColumn: r,
    startRow: e.startRow,
    endRow: e.endRow
  } : {
    startColumn: e.startColumn,
    endColumn: Math.min(e.endColumn, r),
    startRow: e.startRow,
    endRow: Math.min(e.endRow, s)
  };
});
let tr = Qn;
function jC(t, e, n, r = !1) {
  if (e === 0 && n === 0)
    return t;
  let s = { ...t };
  const i = s.startAbsoluteRefType || tt.NONE, o = s.endAbsoluteRefType || tt.NONE, a = s.rangeType || De.NORMAL;
  if (!r && i === tt.ALL && o === tt.ALL)
    return s;
  const u = Xo(s.startRow, n, s.startColumn, e, a), c = Xo(s.endRow, n, s.endColumn, e, a);
  return r || i === tt.NONE && o === tt.NONE ? s = {
    ...s,
    startRow: u.row,
    startColumn: u.column,
    endRow: c.row,
    endColumn: c.column
  } : (i === tt.NONE ? s = { ...s, startRow: u.row, startColumn: u.column } : i === tt.COLUMN ? s = { ...s, startRow: u.row } : i === tt.ROW && (s = { ...s, startColumn: u.column }), o === tt.NONE ? s = { ...s, endRow: c.row, endColumn: c.column } : o === tt.COLUMN ? s = { ...s, endRow: c.row } : o === tt.ROW && (s = { ...s, endColumn: c.column }), s);
}
function Xo(t, e, n, r, s) {
  return s === De.NORMAL ? { row: t + e, column: n + r } : s === De.ROW ? { row: t + e, column: n } : s === De.COLUMN ? { row: t, column: n + r } : { row: t, column: n };
}
function Uu(t) {
  const e = /* @__PURE__ */ new Set(), n = /* @__PURE__ */ new Set();
  for (const o of t)
    e.add(o.startColumn), e.add(o.endColumn + 1), n.add(o.startRow), n.add(o.endRow + 1);
  const r = Array.from(e).sort((o, a) => o - a), s = Array.from(n).sort((o, a) => o - a);
  t.sort((o, a) => o.startRow - a.startRow || o.startColumn - a.startColumn);
  const i = [];
  for (let o = 0; o < s.length - 1; o++)
    for (let a = 0; a < r.length - 1; a++) {
      const u = r[a], c = r[a + 1] - 1, l = s[o], h = s[o + 1] - 1;
      for (const d of t) {
        if (d.startRow > h)
          break;
        if (d.startRow <= l && d.endRow >= h && d.startColumn <= u && d.endColumn >= c) {
          i.push({
            startColumn: u,
            endColumn: c,
            startRow: l,
            endRow: h
          });
          break;
        }
      }
    }
  return i;
}
function Tp(t) {
  t.sort((r, s) => r.startRow - s.startRow || r.startColumn - s.startColumn);
  const e = {};
  for (const r of t)
    e[r.startRow] || (e[r.startRow] = []), e[r.startRow].push(r);
  const n = [];
  for (const r in e) {
    const s = e[+r];
    s.sort((o, a) => o.startColumn - a.startColumn);
    let i = s[0];
    for (let o = 1; o < s.length; o++) {
      const a = s[o];
      a.startColumn <= i.endColumn + 1 && a.startRow === i.startRow && a.endRow === i.endRow ? i.endColumn = Math.max(i.endColumn, a.endColumn) : (n.push(i), i = a);
    }
    n.push(i);
  }
  return n;
}
function Mp(t) {
  t.sort((r, s) => r.startColumn - s.startColumn || r.startRow - s.startRow);
  const e = {};
  for (const r of t)
    e[r.startColumn] || (e[r.startColumn] = []), e[r.startColumn].push(r);
  const n = [];
  for (const r in e) {
    const s = e[+r];
    s.sort((o, a) => o.startRow - a.startRow);
    let i = s[0];
    for (let o = 1; o < s.length; o++) {
      const a = s[o];
      a.startRow <= i.endRow + 1 && a.startColumn === i.startColumn && a.endColumn === i.endColumn ? i.endRow = Math.max(i.endRow, a.endRow) : (n.push(i), i = a);
    }
    n.push(i);
  }
  return n;
}
function Dp(t) {
  const e = Uu(t), n = Tp(e);
  return Mp(n);
}
function xp(t, e) {
  const n = [];
  return t.forEach((r) => {
    n.push(...en.subtract(r, e));
  }), en.mergeRanges(n);
}
function HC(t, e) {
  const n = Jo(
    t.startRow,
    t.endRow,
    e.startRow,
    e.endRow
  ), r = Jo(
    t.startColumn,
    t.endColumn,
    e.startColumn,
    e.endColumn
  );
  if (!n || !r)
    return null;
  const [s, i] = n, [o, a] = r, u = Lp(
    t.rangeType,
    e.rangeType,
    s,
    i,
    o,
    a
  );
  return {
    startRow: s,
    endRow: i,
    startColumn: o,
    endColumn: a,
    rangeType: u
  };
}
function Jo(t, e, n, r) {
  const s = isNaN(t) ? -1 / 0 : t, i = isNaN(e) ? 1 / 0 : e, o = isNaN(n) ? -1 / 0 : n, a = isNaN(r) ? 1 / 0 : r, u = Math.max(s, o), c = Math.min(i, a);
  if (u <= c) {
    const l = u === -1 / 0 ? Number.NaN : u, h = c === 1 / 0 ? Number.NaN : c;
    return [l, h];
  } else
    return null;
}
function Lp(t, e, n, r, s, i) {
  const o = t !== void 0 ? t : Zo(n, r, s, i), a = e !== void 0 ? e : Zo(n, r, s, i);
  return o === De.ALL || a === De.ALL ? o === a ? o : o === De.ALL ? a : o : o === a ? o : (o === De.NORMAL || a === De.NORMAL, De.NORMAL);
}
function Zo(t, e, n, r) {
  const s = !isNaN(t) && !isNaN(e), i = !isNaN(n) && !isNaN(r);
  return s && i ? De.NORMAL : s ? De.ROW : i ? De.COLUMN : De.ALL;
}
const Ut = class Ut {
  /**
   * Creates a deep copy of an IRange object
   * @param src
   * @example
   * ```typescript
   * const original = { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 };
   * const copy = Rectangle.clone(original);
   * // copy = { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 }
   * ```
   */
  static clone(e) {
    return e.rangeType !== void 0 ? {
      startRow: e.startRow,
      startColumn: e.startColumn,
      endRow: e.endRow,
      endColumn: e.endColumn,
      rangeType: e.rangeType
    } : {
      startRow: e.startRow,
      startColumn: e.startColumn,
      endRow: e.endRow,
      endColumn: e.endColumn
    };
  }
  /**
   * Checks if two ranges are equal by comparing their properties
   * @param src
   * @param target
   * @example
   * ```typescript
   * const range1 = { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 };
   * const range2 = { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 };
   * const areEqual = Rectangle.equals(range1, range2); // true
   * ```
   */
  static equals(e, n) {
    return e == null || n == null ? !1 : e.endRow === n.endRow && e.endColumn === n.endColumn && e.startRow === n.startRow && e.startColumn === n.startColumn && (e.rangeType === n.rangeType || e.rangeType === void 0 && n.rangeType === De.NORMAL || n.rangeType === void 0 && e.rangeType === De.NORMAL);
  }
  /**
   * Quickly checks if two normal ranges intersect. For specialized range types,
   * use the intersects() method instead.
   * @param rangeA
   * @param rangeB
   * @example
   * ```typescript
   * const range1 = { startRow: 0, startColumn: 0, endRow: 2, endColumn: 2 };
   * const range2 = { startRow: 1, startColumn: 1, endRow: 3, endColumn: 3 };
   * const doIntersect = Rectangle.simpleRangesIntersect(range1, range2); // true
   * ```
   */
  static simpleRangesIntersect(e, n) {
    const { startRow: r, endRow: s, startColumn: i, endColumn: o } = e, { startRow: a, endRow: u, startColumn: c, endColumn: l } = n, h = r <= u && s >= a, d = i <= l && o >= c;
    return h && d;
  }
  /**
   * Checks if two ranges intersect, handling special range types (ROW, COLUMN)
   * @param src
   * @param target
   * @example
   * ```typescript
   * const rowRange = {
   *   startRow: 0, endRow: 2,
   *   startColumn: NaN, endColumn: NaN,
   *   rangeType: RANGE_TYPE.ROW
   * };
   * const colRange = {
   *   startRow: NaN, endRow: NaN,
   *   startColumn: 0, endColumn: 2,
   *   rangeType: RANGE_TYPE.COLUMN
   * };
   * const doIntersect = Rectangle.intersects(rowRange, colRange); // true
   * ```
   */
  static intersects(e, n) {
    if (e.rangeType === De.ROW && n.rangeType === De.COLUMN || e.rangeType === De.COLUMN && n.rangeType === De.ROW)
      return !0;
    if (e.rangeType === De.ROW && n.rangeType === De.ROW)
      return e.startRow <= n.endRow && e.endRow >= n.startRow;
    if (e.rangeType === De.COLUMN && n.rangeType === De.COLUMN)
      return e.startColumn <= n.endColumn && e.endColumn >= n.startColumn;
    const r = Math.floor(Number.MAX_SAFE_INTEGER / 10), s = Number.isNaN(e.startRow) ? 0 : e.startRow, i = Number.isNaN(e.endRow) ? r : e.endRow, o = Number.isNaN(e.startColumn) ? 0 : e.startColumn, a = Number.isNaN(e.endColumn) ? r : e.endColumn, u = Number.isNaN(n.startRow) ? 0 : n.startRow, c = Number.isNaN(n.endRow) ? r : n.endRow, l = Number.isNaN(n.startColumn) ? 0 : n.startColumn, h = Number.isNaN(n.endColumn) ? r : n.endColumn, d = Math.abs(o + a - l - h), f = Math.abs(o - a) + Math.abs(l - h), E = Math.abs(s + i - u - c), R = Math.abs(s - i) + Math.abs(u - c);
    return d <= f && E <= R;
  }
  /**
   * Gets the intersection range between two ranges
   * @param src
   * @param target
   * @deprecated use `getIntersectRange` instead
   * @example
   * ```typescript
   * const range1 = { startRow: 0, startColumn: 0, endRow: 2, endColumn: 2 };
   * const range2 = { startRow: 1, startColumn: 1, endRow: 3, endColumn: 3 };
   * const intersection = Rectangle.getIntersects(range1, range2);
   * // intersection = { startRow: 1, startColumn: 1, endRow: 2, endColumn: 2 }
   * ```
   */
  static getIntersects(e, n) {
    const r = e.startRow, s = e.endRow, i = e.startColumn, o = e.endColumn, a = n.startRow, u = n.endRow, c = n.startColumn, l = n.endColumn;
    let h, d, f, E;
    if (a <= s)
      a >= r ? d = a : d = r;
    else
      return null;
    if (u >= r)
      u >= s ? E = s : E = u;
    else
      return null;
    if (c <= o)
      c > i ? h = c : h = i;
    else
      return null;
    if (l >= i)
      l >= o ? f = o : f = l;
    else
      return null;
    return {
      startRow: d,
      endRow: E,
      startColumn: h,
      endColumn: f,
      rangeType: De.NORMAL
      // TODO: this may not be accurate
    };
  }
  /**
   * Checks if one range completely contains another range
   * @param src
   * @param target
   * @example
   * ```typescript
   * const outer = { startRow: 0, startColumn: 0, endRow: 3, endColumn: 3 };
   * const inner = { startRow: 1, startColumn: 1, endRow: 2, endColumn: 2 };
   * const contains = Rectangle.contains(outer, inner); // true
   * ```
   */
  static contains(e, n) {
    return e.startRow <= n.startRow && e.endRow >= n.endRow && e.startColumn <= n.startColumn && e.endColumn >= n.endColumn;
  }
  /**
   * Checks if one range strictly contains another range (not equal)
   * @param src
   * @param target
   * @example
   * ```typescript
   * const outer = { startRow: 0, startColumn: 0, endRow: 3, endColumn: 3 };
   * const same = { startRow: 0, startColumn: 0, endRow: 3, endColumn: 3 };
   * const realContains = Rectangle.realContain(outer, same); // false
   * ```
   */
  static realContain(e, n) {
    return Ut.contains(e, n) && (e.startRow < n.startRow || e.endRow > n.endRow || e.startColumn < n.startColumn || e.endColumn > n.endColumn);
  }
  /**
   * Creates a union range that encompasses all input ranges
   * @param {...any} ranges
   * @example
   * ```typescript
   * const range1 = { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 };
   * const range2 = { startRow: 2, startColumn: 2, endRow: 3, endColumn: 3 };
   * const union = Rectangle.union(range1, range2);
   * // union = { startRow: 0, startColumn: 0, endRow: 3, endColumn: 3 }
   * ```
   */
  static union(...e) {
    return e.reduce(
      (n, r) => ({
        startRow: Math.min(n.startRow, r.startRow),
        startColumn: Math.min(n.startColumn, r.startColumn),
        endRow: Math.max(n.endRow, r.endRow),
        endColumn: Math.max(n.endColumn, r.endColumn),
        rangeType: De.NORMAL
      }),
      e[0]
    );
  }
  /**
   * Creates a union range considering special range types (ROW, COLUMN)
   * @param {...any} ranges
   * @example
   * ```typescript
   * const rowRange = {
   *   startRow: 0, endRow: 2,
   *   rangeType: RANGE_TYPE.ROW
   * };
   * const normalRange = {
   *   startRow: 1, startColumn: 1,
   *   endRow: 3, endColumn: 3
   * };
   * const union = Rectangle.realUnion(rowRange, normalRange);
   * // Result will have NaN for columns due to ROW type
   * ```
   */
  static realUnion(...e) {
    const n = e.some((i) => i.rangeType === De.COLUMN), r = e.some((i) => i.rangeType === De.ROW), s = Ut.union(...e);
    return {
      startColumn: r ? Number.NaN : s.startColumn,
      endColumn: r ? Number.NaN : s.endColumn,
      startRow: n ? Number.NaN : s.startRow,
      endRow: n ? Number.NaN : s.endRow,
      rangeType: r ? De.ROW : n ? De.COLUMN : De.NORMAL
    };
  }
  /**
   * Subtracts one range from another, returning the remaining areas as separate ranges
   * @param range1
   * @param range2
   * @example
   * ```typescript
   * const range1 = { startRow: 0, startColumn: 0, endRow: 3, endColumn: 3 };
   * const range2 = { startRow: 1, startColumn: 1, endRow: 2, endColumn: 2 };
   * const result = Rectangle.subtract(range1, range2);
   * // Results in up to 4 ranges representing the non-overlapping areas
   * ```
   */
  static subtract(e, n) {
    if (n.startRow > e.endRow || n.endRow < e.startRow || n.startColumn > e.endColumn || n.endColumn < e.startColumn)
      return [e];
    const r = [];
    n.startRow >= e.startRow && r.push({
      startRow: e.startRow,
      startColumn: e.startColumn,
      endRow: n.startRow - 1,
      endColumn: e.endColumn
    }), n.endRow <= e.endRow && r.push({
      startRow: n.endRow + 1,
      startColumn: e.startColumn,
      endRow: e.endRow,
      endColumn: e.endColumn
    });
    const s = Math.max(e.startRow, n.startRow), i = Math.min(e.endRow, n.endRow);
    return n.startColumn >= e.startColumn && r.push({
      startRow: s,
      startColumn: e.startColumn,
      endRow: i,
      endColumn: n.startColumn - 1
    }), n.endColumn <= e.endColumn && r.push({
      startRow: s,
      startColumn: n.endColumn + 1,
      endRow: i,
      endColumn: e.endColumn
    }), r.filter((a) => a.startRow <= a.endRow && a.startColumn <= a.endColumn);
  }
  /**
   * Merges overlapping or adjacent ranges into larger ranges
   * @param ranges
   * @example
   * ```typescript
   * const ranges = [
   *   { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 },
   *   { startRow: 1, startColumn: 1, endRow: 2, endColumn: 2 }
   * ];
   * const merged = Rectangle.mergeRanges(ranges);
   * // Combines overlapping ranges into larger ones
   * ```
   */
  static mergeRanges(e) {
    return Dp(e);
  }
  /**
   * Splits overlapping ranges into a grid of non-overlapping ranges
   * @param ranges
   * @example
   * ```typescript
   * const ranges = [
   *   { startRow: 0, startColumn: 0, endRow: 2, endColumn: 2 },
   *   { startRow: 1, startColumn: 1, endRow: 3, endColumn: 3 }
   * ];
   * const grid = Rectangle.splitIntoGrid(ranges);
   * // Splits into non-overlapping grid sections
   * ```
   */
  static splitIntoGrid(e) {
    return Uu(e);
  }
  /**
   * Subtracts multiple ranges from multiple ranges
   * @param ranges1
   * @param ranges2
   * @example
   * ```typescript
   * const ranges1 = [{ startRow: 0, startColumn: 0, endRow: 3, endColumn: 3 }];
   * const ranges2 = [
   *   { startRow: 1, startColumn: 1, endRow: 2, endColumn: 2 },
   *   { startRow: 2, startColumn: 2, endRow: 3, endColumn: 3 }
   * ];
   * const result = Rectangle.subtractMulti(ranges1, ranges2);
   * // Returns remaining non-overlapping areas
   * ```
   */
  static subtractMulti(e, n) {
    if (!n.length)
      return e;
    let r = e;
    return n.forEach((s) => {
      r = xp(r, s);
    }), r;
  }
  /**
   * Checks if two rectangles defined by left, top, right, bottom coordinates intersect
   * @param rect1
   * @param rect2
   * @example
   * ```typescript
   * const rect1 = { left: 0, top: 0, right: 10, bottom: 10 };
   * const rect2 = { left: 5, top: 5, right: 15, bottom: 15 };
   * const intersects = Rectangle.hasIntersectionBetweenTwoRect(rect1, rect2); // true
   * ```
   */
  static hasIntersectionBetweenTwoRect(e, n) {
    return !(e.left > n.right || // rect1 在 rect2 右侧
    e.right < n.left || // rect1 在 rect2 左侧
    e.top > n.bottom || // rect1 在 rect2 下方
    e.bottom < n.top);
  }
  /**
   * Gets the intersection area between two rectangles defined by LTRB coordinates
   * @param rect1
   * @param rect2
   * @example
   * ```typescript
   * const rect1 = { left: 0, top: 0, right: 10, bottom: 10 };
   * const rect2 = { left: 5, top: 5, right: 15, bottom: 15 };
   * const intersection = Rectangle.getIntersectionBetweenTwoRect(rect1, rect2);
   * // Returns { left: 5, top: 5, right: 10, bottom: 10, width: 5, height: 5 }
   * ```
   */
  static getIntersectionBetweenTwoRect(e, n) {
    const r = Math.max(e.left, n.left), s = Math.min(e.right, n.right), i = Math.max(e.top, n.top), o = Math.min(e.bottom, n.bottom);
    return s <= r || o <= i ? null : {
      left: r,
      right: s,
      top: i,
      bottom: o,
      width: s - r,
      height: o - i
    };
  }
  /**
   * Sorts an array of ranges by startRow, then by startColumn
   * @param ranges
   * @example
   * ```typescript
   * const ranges = [
   *   { startRow: 1, startColumn: 0, endRow: 2, endColumn: 1 },
   *   { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 }
   * ];
   * const sorted = Rectangle.sort(ranges);
   * // Ranges will be sorted by startRow first, then startColumn
   * ```
   */
  static sort(e) {
    return e.sort((n, r) => n.startRow - r.startRow || n.startColumn - r.startColumn);
  }
};
/**
 * Converts an absolute range to a relative range based on an origin range
 * @param range
 * @param originRange
 * @example
 * ```typescript
 * const range = { startRow: 5, startColumn: 5, endRow: 7, endColumn: 7 };
 * const origin = { startRow: 3, startColumn: 3, endRow: 8, endColumn: 8 };
 * const relative = Rectangle.getRelativeRange(range, origin);
 * // relative = { startRow: 2, startColumn: 2, endRow: 2, endColumn: 2 }
 * ```
 */
C(Ut, "getRelativeRange", (e, n) => ({
  startRow: e.startRow - n.startRow,
  endRow: e.endRow - e.startRow,
  startColumn: e.startColumn - n.startColumn,
  endColumn: e.endColumn - e.startColumn
})), /**
 * Converts a relative range back to an absolute range based on origin
 * @param relativeRange
 * @param originRange
 * @param absoluteRange
 * @example
 * ```typescript
 * const relative = { startRow: 2, startColumn: 2, endRow: 2, endColumn: 2 };
 * const origin = { startRow: 3, startColumn: 3, endRow: 8, endColumn: 8 };
 * const absolute = Rectangle.getPositionRange(relative, origin);
 * // absolute = { startRow: 5, startColumn: 5, endRow: 7, endColumn: 7 }
 * ```
 */
C(Ut, "getPositionRange", (e, n, r) => ({
  ...r || {},
  startRow: r && [tt.ROW, tt.ALL].includes(r.startAbsoluteRefType || 0) ? r.startRow : e.startRow + n.startRow,
  endRow: r && [tt.ROW, tt.ALL].includes(r.endAbsoluteRefType || 0) ? r.endRow : e.endRow + e.startRow + n.startRow,
  startColumn: r && [tt.COLUMN, tt.ALL].includes(r.startAbsoluteRefType || 0) ? r.startColumn : e.startColumn + n.startColumn,
  endColumn: r && [tt.COLUMN, tt.ALL].includes(r.endAbsoluteRefType || 0) ? r.endColumn : e.endColumn + e.startColumn + n.startColumn
})), /**
 * Moves a range horizontally by a specified step and optionally extends it
 * @param range
 * @param step
 * @param length
 * @example
 * ```typescript
 * const range = { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 };
 * const moved = Rectangle.moveHorizontal(range, 2, 1);
 * // moved = { startRow: 0, startColumn: 2, endRow: 1, endColumn: 4 }
 * ```
 */
C(Ut, "moveHorizontal", (e, n = 0, r = 0) => ({
  ...e,
  startColumn: e.startColumn + n,
  endColumn: e.endColumn + n + r
})), /**
 * Moves a range vertically by a specified step and optionally extends it
 * @param range
 * @param step
 * @param length
 * @example
 * ```typescript
 * const range = { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 };
 * const moved = Rectangle.moveVertical(range, 2, 1);
 * // moved = { startRow: 2, startColumn: 0, endRow: 4, endColumn: 1 }
 * ```
 */
C(Ut, "moveVertical", (e, n = 0, r = 0) => ({
  ...e,
  startRow: e.startRow + n,
  endRow: e.endRow + n + r
})), /**
 * Moves a range by specified offsets in both directions
 * @param range
 * @param offsetX
 * @param offsetY
 * @example
 * ```typescript
 * const range = { startRow: 0, startColumn: 0, endRow: 1, endColumn: 1 };
 * const moved = Rectangle.moveOffset(range, 2, 3);
 * // moved = { startRow: 3, startColumn: 2, endRow: 4, endColumn: 3 }
 * ```
 */
C(Ut, "moveOffset", (e, n, r) => ({
  ...e,
  startRow: e.startRow + r,
  endRow: e.endRow + r,
  startColumn: e.startColumn + n,
  endColumn: e.endColumn + n
}));
let en = Ut;
function Up(t, e) {
  if (t.length === 0 || t[0].length === 0) return null;
  const n = new Array(t[0].length).fill(0);
  let r = 0, s = null;
  for (let i = 0; i < t.length; i++) {
    for (let a = 0; a < t[0].length; a++)
      n[a] = e(t[i][a]) ? n[a] + 1 : 0;
    const o = Pp(n);
    o.area > r && (r = o.area, s = {
      startColumn: o.start,
      startRow: i - o.height + 1,
      endColumn: o.end,
      endRow: i
    });
  }
  return s;
}
function Pp(t) {
  const e = [];
  let n = 0, r = { area: 0, height: 0, start: 0, end: 0 }, s = 0;
  for (; s < t.length; )
    if (e.length === 0 || t[s] >= t[e[e.length - 1]])
      e.push(s++);
    else {
      const i = t[e.pop()], o = e.length === 0 ? s : s - e[e.length - 1] - 1;
      i * o > n && (n = i * o, r = { area: n, height: i, start: e.length === 0 ? 0 : e[e.length - 1] + 1, end: s - 1 });
    }
  for (; e.length > 0; ) {
    const i = t[e.pop()], o = e.length === 0 ? s : s - e[e.length - 1] - 1;
    i * o > n && (n = i * o, r = { area: n, height: i, start: e.length === 0 ? 0 : e[e.length - 1] + 1, end: s - 1 });
  }
  return r;
}
function kp(t, e) {
  tr.foreach(e, (n, r) => {
    t[n][r] = void 0;
  });
}
function WC(t, e) {
  const n = t.toFullArray(), r = [];
  for (; ; ) {
    const s = Up(n, e);
    if (!s)
      break;
    r.push(s), kp(n, s);
  }
  return r;
}
class zC {
  constructor(e, n) {
    C(this, "_values", []);
    C(this, "_keys", []);
    C(this, "_keyMaps", /* @__PURE__ */ new Map());
    this._values = e, this._keys = n, e.forEach((r) => {
      this._initKeyMap(r);
    });
  }
  _initKeyMap(e) {
    this._keys.forEach((n) => {
      const r = e[n], s = this._keyMaps.get(n) || /* @__PURE__ */ new Map();
      s.set(r, e), this._keyMaps.set(n, s);
    });
  }
  /**
   * If a key group is specified, the order of values is determined by the key group, otherwise it depends on the keys at initialization
   * @param {string} key
   * @param {K[]} [keyGroup]
   * @return {*}
   * @memberof RefAlias
   */
  getValue(e, n) {
    const r = n || this._keys;
    for (let s = 0; s < r.length; s++) {
      const i = this._keyMaps.get(r[s]);
      if (i != null && i.has(e))
        return i.get(e);
    }
    return null;
  }
  hasValue(e) {
    for (let n = 0; n < this._keys.length; n++) {
      const r = this._keyMaps.get(this._keys[n]);
      if (r != null && r.has(e))
        return !0;
    }
    return !1;
  }
  addValue(e) {
    this._values.push(e), this._initKeyMap(e);
  }
  setValue(e, n, r) {
    const s = this.getValue(e);
    s && Object.keys(s).includes(n) && (s[n] = r);
  }
  deleteValue(e, n) {
    const r = this.getValue(e, n);
    if (r) {
      this._keys.forEach((i) => {
        const o = this._keyMaps.get(i), a = r[i];
        o == null || o.delete(a);
      });
      const s = this._values.findIndex((i) => i === r);
      this._values.splice(s, 1);
    }
  }
  getValues() {
    return this._values;
  }
  getKeyMap(e) {
    var n;
    return [...((n = this._keyMaps.get(e)) == null ? void 0 : n.keys()) || []];
  }
  clear() {
    this._values = [], this._keys = [], this._keyMaps.clear();
  }
}
function Qo(t, e, n, r) {
  return {
    forEach(s) {
      for (let i = t; i <= e; i++)
        for (let o = n; o <= r; o++)
          s(i, o);
    }
  };
}
function YC(t) {
  if (t == null || t.length === 0)
    return Number.NaN;
  const e = t.toLowerCase().split(""), n = e.length, r = (o) => o.charCodeAt(0) - 96;
  let s = 0, i = 0;
  for (let o = 0; o < n; o++)
    i = r(e[o]), s += i * 26 ** (n - o - 1);
  return s === 0 ? Number.NaN : s - 1;
}
const qr = 65, Pu = 90, Fp = 97;
function VC(t) {
  const e = Pu - qr + 1;
  let n = "";
  for (; t >= 0; )
    n = String.fromCharCode(t % e + qr) + n, t = Math.floor(t / e) - 1;
  return n;
}
function $p(t, e) {
  let n = "";
  for (; e > 0; )
    n += t, e--;
  return n;
}
function GC(t, e = !1) {
  const n = Pu - qr + 1;
  let r = Fp;
  e && (r = qr);
  const s = String.fromCharCode(t % n + r), i = Math.floor(t / n) + 1;
  return $p(s, i);
}
function KC(t, e) {
  return t.zIndex > e.zIndex ? 1 : t.zIndex === e.zIndex ? 0 : -1;
}
function XC(t, e) {
  return t.zIndex > e.zIndex ? -1 : t.zIndex === e.zIndex ? 0 : 1;
}
function ps(t = "index", e = 1) {
  return (n, r) => n[t] > r[t] ? e : n[t] === r[t] ? 0 : -e;
}
var Bp = /* @__PURE__ */ ((t) => (t[t.character = 0] = "character", t[t.paragraph = 1] = "paragraph", t[t.table = 2] = "table", t[t.numbering = 3] = "numbering", t))(Bp || {}), jp = /* @__PURE__ */ ((t) => (t[t.TAB = 0] = "TAB", t[t.SPACE = 1] = "SPACE", t[t.NOTHING = 2] = "NOTHING", t))(jp || {}), Te = /* @__PURE__ */ ((t) => (t[t.BULLET = 0] = "BULLET", t[t.NONE = 1] = "NONE", t[t.DECIMAL = 2] = "DECIMAL", t[t.DECIMAL_ZERO = 3] = "DECIMAL_ZERO", t[t.UPPER_LETTER = 4] = "UPPER_LETTER", t[t.LOWER_LETTER = 5] = "LOWER_LETTER", t[t.UPPER_ROMAN = 6] = "UPPER_ROMAN", t[t.LOWER_ROMAN = 7] = "LOWER_ROMAN", t[t.ORDINAL = 8] = "ORDINAL", t[t.CARDINAL_TEXT = 9] = "CARDINAL_TEXT", t[t.ORDINAL_TEXT = 10] = "ORDINAL_TEXT", t[t.HEX = 11] = "HEX", t[t.CHICAGO = 12] = "CHICAGO", t[t.IDEOGRAPH_DIGITAL = 13] = "IDEOGRAPH_DIGITAL", t[t.JAPANESE_COUNTING = 14] = "JAPANESE_COUNTING", t[t.AIUEO = 15] = "AIUEO", t[t.IROHA = 16] = "IROHA", t[t.DECIMAL_FULL_WIDTH = 17] = "DECIMAL_FULL_WIDTH", t[t.DECIMAL_HALF_WIDTH = 18] = "DECIMAL_HALF_WIDTH", t[t.JAPANESE_LEGAL = 19] = "JAPANESE_LEGAL", t[t.JAPANESE_DIGITAL_TEN_THOUSAND = 20] = "JAPANESE_DIGITAL_TEN_THOUSAND", t[t.DECIMAL_ENCLOSED_CIRCLE = 21] = "DECIMAL_ENCLOSED_CIRCLE", t[t.DECIMAL_FULL_WIDTH2 = 22] = "DECIMAL_FULL_WIDTH2", t[t.AIUEO_FULL_WIDTH = 23] = "AIUEO_FULL_WIDTH", t[t.IROHA_FULL_WIDTH = 24] = "IROHA_FULL_WIDTH", t[t.GANADA = 25] = "GANADA", t[t.CHOSUNG = 26] = "CHOSUNG", t[t.DECIMAL_ENCLOSED_FULLSTOP = 27] = "DECIMAL_ENCLOSED_FULLSTOP", t[t.DECIMAL_ENCLOSED_PAREN = 28] = "DECIMAL_ENCLOSED_PAREN", t[t.DECIMAL_ENCLOSED_CIRCLE_CHINESE = 29] = "DECIMAL_ENCLOSED_CIRCLE_CHINESE", t[t.IDEOGRAPH_ENCLOSED_CIRCLE = 30] = "IDEOGRAPH_ENCLOSED_CIRCLE", t[t.IDEOGRAPH_TRADITIONAL = 31] = "IDEOGRAPH_TRADITIONAL", t[t.IDEOGRAPH_ZODIAC = 32] = "IDEOGRAPH_ZODIAC", t[t.IDEOGRAPH_ZODIAC_TRADITIONAL = 33] = "IDEOGRAPH_ZODIAC_TRADITIONAL", t[t.TAIWANESE_COUNTING = 34] = "TAIWANESE_COUNTING", t[t.IDEOGRAPH_LEGAL_TRADITIONAL = 35] = "IDEOGRAPH_LEGAL_TRADITIONAL", t[t.TAIWANESE_COUNTING_THOUSAND = 36] = "TAIWANESE_COUNTING_THOUSAND", t[t.TAIWANESE_DIGITAL = 37] = "TAIWANESE_DIGITAL", t[t.CHINESE_COUNTING = 38] = "CHINESE_COUNTING", t[t.CHINESE_LEGAL_SIMPLIFIED = 39] = "CHINESE_LEGAL_SIMPLIFIED", t[t.CHINESE_COUNTING_THOUSAND = 40] = "CHINESE_COUNTING_THOUSAND", t[t.KOREAN_DIGITAL = 41] = "KOREAN_DIGITAL", t[t.KOREAN_COUNTING = 42] = "KOREAN_COUNTING", t[t.KOREAN_LEGAL = 43] = "KOREAN_LEGAL", t[t.KOREAN_DIGITAL2 = 44] = "KOREAN_DIGITAL2", t[t.VIETNAMESE_COUNTING = 45] = "VIETNAMESE_COUNTING", t[t.RUSSIAN_LOWER = 46] = "RUSSIAN_LOWER", t[t.RUSSIAN_UPPER = 47] = "RUSSIAN_UPPER", t[t.NUMBER_IN_DASH = 48] = "NUMBER_IN_DASH", t[t.HEBREW1 = 49] = "HEBREW1", t[t.HEBREW2 = 50] = "HEBREW2", t[t.ARABIC_ALPHA = 51] = "ARABIC_ALPHA", t[t.ARABIC_ABJAD = 52] = "ARABIC_ABJAD", t[t.HINDI_VOWELS = 53] = "HINDI_VOWELS", t[t.HINDI_CONSONANTS = 54] = "HINDI_CONSONANTS", t[t.HINDI_NUMBERS = 55] = "HINDI_NUMBERS", t[t.HINDI_COUNTING = 56] = "HINDI_COUNTING", t[t.THAI_LETTERS = 57] = "THAI_LETTERS", t[t.THAI_NUMBERS = 58] = "THAI_NUMBERS", t[t.THAI_COUNTING = 59] = "THAI_COUNTING", t[t.CUSTOM = 60] = "CUSTOM", t))(Te || {}), ms = /* @__PURE__ */ ((t) => (t[t.BULLET_ALIGNMENT_UNSPECIFIED = 0] = "BULLET_ALIGNMENT_UNSPECIFIED", t[t.START = 1] = "START", t[t.CENTER = 2] = "CENTER", t[t.END = 3] = "END", t[t.BOTH = 4] = "BOTH", t))(ms || {}), mn = /* @__PURE__ */ ((t) => (t[t.HYPERLINK = 0] = "HYPERLINK", t[t.FIELD = 1] = "FIELD", t[t.SDT = 2] = "SDT", t[t.BOOKMARK = 3] = "BOOKMARK", t[t.COMMENT = 4] = "COMMENT", t[t.CUSTOM = 5] = "CUSTOM", t[t.MENTION = 6] = "MENTION", t[t.UNI_FORMULA = 7] = "UNI_FORMULA", t[t.DELTED = 9999] = "DELTED", t))(mn || {}), An = /* @__PURE__ */ ((t) => (t[t.COMMENT = 0] = "COMMENT", t[t.DELETED = 9999] = "DELETED", t))(An || {}), Hp = /* @__PURE__ */ ((t) => (t[t.DRAWING = 0] = "DRAWING", t[t.CUSTOM = 1] = "CUSTOM", t))(Hp || {}), ku = /* @__PURE__ */ ((t) => (t[t.UNSPECIFIED = 0] = "UNSPECIFIED", t[t.TRADITIONAL = 1] = "TRADITIONAL", t[t.MODERN = 2] = "MODERN", t))(ku || {}), Wp = /* @__PURE__ */ ((t) => (t[t.DEFAULT = 0] = "DEFAULT", t[t.LINES = 1] = "LINES", t[t.LINES_AND_CHARS = 2] = "LINES_AND_CHARS", t[t.SNAP_TO_CHARS = 3] = "SNAP_TO_CHARS", t))(Wp || {}), zp = /* @__PURE__ */ ((t) => (t[t.SECTION_TYPE_UNSPECIFIED = 0] = "SECTION_TYPE_UNSPECIFIED", t[t.CONTINUOUS = 1] = "CONTINUOUS", t[t.NEXT_PAGE = 2] = "NEXT_PAGE", t[t.EVEN_PAGE = 3] = "EVEN_PAGE", t[t.ODD_PAGE = 4] = "ODD_PAGE", t))(zp || {}), Yp = /* @__PURE__ */ ((t) => (t[t.COLUMN_SEPARATOR_STYLE_UNSPECIFIED = 0] = "COLUMN_SEPARATOR_STYLE_UNSPECIFIED", t[t.NONE = 1] = "NONE", t[t.BETWEEN_EACH_COLUMN = 2] = "BETWEEN_EACH_COLUMN", t))(Yp || {}), Vp = /* @__PURE__ */ ((t) => (t[t.NORMAL = 0] = "NORMAL", t[t.TBRL = 1] = "TBRL", t[t.LRTBV = 2] = "LRTBV", t))(Vp || {}), Gp = /* @__PURE__ */ ((t) => (t[t.TEXT_RUN = 0] = "TEXT_RUN", t[t.AUTO_TEXT = 1] = "AUTO_TEXT", t[t.PAGE_BREAK = 2] = "PAGE_BREAK", t[t.COLUMN_BREAK = 3] = "COLUMN_BREAK", t[t.FOOT_NOTE_REFERENCE = 4] = "FOOT_NOTE_REFERENCE", t[t.HORIZONTAL_RULE = 5] = "HORIZONTAL_RULE", t[t.EQUATION = 6] = "EQUATION", t[t.DRAWING = 7] = "DRAWING", t[t.PERSON = 8] = "PERSON", t[t.RICH_LINK = 9] = "RICH_LINK", t))(Gp || {}), Kp = /* @__PURE__ */ ((t) => (t[t.BOTH_SIDES = 0] = "BOTH_SIDES", t[t.LEFT = 1] = "LEFT", t[t.RIGHT = 2] = "RIGHT", t[t.LARGEST = 3] = "LARGEST", t))(Kp || {}), Xp = /* @__PURE__ */ ((t) => (t[t.INLINE = 0] = "INLINE", t[t.WRAP_NONE = 1] = "WRAP_NONE", t[t.WRAP_POLYGON = 2] = "WRAP_POLYGON", t[t.WRAP_SQUARE = 3] = "WRAP_SQUARE", t[t.WRAP_THROUGH = 4] = "WRAP_THROUGH", t[t.WRAP_TIGHT = 5] = "WRAP_TIGHT", t[t.WRAP_TOP_AND_BOTTOM = 6] = "WRAP_TOP_AND_BOTTOM", t))(Xp || {}), Jp = /* @__PURE__ */ ((t) => (t[t.NAMED_STYLE_TYPE_UNSPECIFIED = 0] = "NAMED_STYLE_TYPE_UNSPECIFIED", t[t.NORMAL_TEXT = 1] = "NORMAL_TEXT", t[t.TITLE = 2] = "TITLE", t[t.SUBTITLE = 3] = "SUBTITLE", t[t.HEADING_1 = 4] = "HEADING_1", t[t.HEADING_2 = 5] = "HEADING_2", t[t.HEADING_3 = 6] = "HEADING_3", t[t.HEADING_4 = 7] = "HEADING_4", t[t.HEADING_5 = 8] = "HEADING_5", t[t.HEADING_6 = 9] = "HEADING_6", t))(Jp || {}), Zp = /* @__PURE__ */ ((t) => (t[t.AUTO = 0] = "AUTO", t[t.AT_LEAST = 1] = "AT_LEAST", t[t.EXACT = 2] = "EXACT", t))(Zp || {}), Qp = /* @__PURE__ */ ((t) => (t[t.DASH_STYLE_UNSPECIFIED = 0] = "DASH_STYLE_UNSPECIFIED", t[t.SOLID = 1] = "SOLID", t[t.DOT = 2] = "DOT", t[t.DASH = 3] = "DASH", t))(Qp || {}), qp = /* @__PURE__ */ ((t) => (t[t.TAB_STOP_ALIGNMENT_UNSPECIFIED = 0] = "TAB_STOP_ALIGNMENT_UNSPECIFIED", t[t.START = 1] = "START", t[t.CENTER = 2] = "CENTER", t[t.END = 3] = "END", t))(qp || {}), em = /* @__PURE__ */ ((t) => (t[t.UNSPECIFIED = 0] = "UNSPECIFIED", t[t.SPECIFIED = 1] = "SPECIFIED", t))(em || {}), tm = /* @__PURE__ */ ((t) => (t[t.START = 0] = "START", t[t.CENTER = 1] = "CENTER", t[t.END = 2] = "END", t))(tm || {}), nm = /* @__PURE__ */ ((t) => (t[t.AUTO_FIT = 0] = "AUTO_FIT", t[t.FIXED = 1] = "FIXED", t))(nm || {}), rm = /* @__PURE__ */ ((t) => (t[t.NONE = 0] = "NONE", t[t.WRAP = 1] = "WRAP", t))(rm || {}), sm = /* @__PURE__ */ ((t) => (t[t.AUTO = 0] = "AUTO", t[t.AT_LEAST = 1] = "AT_LEAST", t[t.EXACT = 2] = "EXACT", t))(sm || {}), im = /* @__PURE__ */ ((t) => (t[t.CONTENT_ALIGNMENT_UNSPECIFIED = 0] = "CONTENT_ALIGNMENT_UNSPECIFIED", t[t.BOTH = 1] = "BOTH", t[t.TOP = 2] = "TOP", t[t.CENTER = 3] = "CENTER", t[t.BOTTOM = 4] = "BOTTOM", t))(im || {}), Yn = /* @__PURE__ */ ((t) => (t.NORMAL = "normal", t.BOLD = "bold", t.ITALIC = "italic", t))(Yn || {}), om = /* @__PURE__ */ ((t) => (t[t.PAGE = 0] = "PAGE", t[t.COLUMN = 1] = "COLUMN", t[t.CHARACTER = 2] = "CHARACTER", t[t.MARGIN = 3] = "MARGIN", t[t.INSIDE_MARGIN = 4] = "INSIDE_MARGIN", t[t.OUTSIDE_MARGIN = 5] = "OUTSIDE_MARGIN", t[t.LEFT_MARGIN = 6] = "LEFT_MARGIN", t[t.RIGHT_MARGIN = 7] = "RIGHT_MARGIN", t))(om || {}), am = /* @__PURE__ */ ((t) => (t[t.PAGE = 0] = "PAGE", t[t.PARAGRAPH = 1] = "PARAGRAPH", t[t.LINE = 2] = "LINE", t[t.MARGIN = 3] = "MARGIN", t[t.TOP_MARGIN = 4] = "TOP_MARGIN", t[t.BOTTOM_MARGIN = 5] = "BOTTOM_MARGIN", t[t.INSIDE_MARGIN = 6] = "INSIDE_MARGIN", t[t.OUTSIDE_MARGIN = 7] = "OUTSIDE_MARGIN", t))(am || {}), um = /* @__PURE__ */ ((t) => (t[t.POINT = 0] = "POINT", t[t.LINE = 1] = "LINE", t[t.CHARACTER = 2] = "CHARACTER", t[t.PIXEL = 3] = "PIXEL", t[t.PERCENT = 4] = "PERCENT", t))(um || {}), lm = /* @__PURE__ */ ((t) => (t[t.CENTER = 0] = "CENTER", t[t.INSIDE = 1] = "INSIDE", t[t.LEFT = 2] = "LEFT", t[t.OUTSIDE = 3] = "OUTSIDE", t[t.RIGHT = 4] = "RIGHT", t[t.BOTH = 5] = "BOTH", t[t.DISTRIBUTE = 6] = "DISTRIBUTE", t))(lm || {}), cm = /* @__PURE__ */ ((t) => (t[t.BOTTOM = 0] = "BOTTOM", t[t.CENTER = 1] = "CENTER", t[t.INSIDE = 2] = "INSIDE", t[t.OUTSIDE = 3] = "OUTSIDE", t[t.TOP = 4] = "TOP", t))(cm || {}), hm = /* @__PURE__ */ ((t) => (t[t.compressPunctuation = 0] = "compressPunctuation", t[t.compressPunctuationAndJapaneseKana = 1] = "compressPunctuationAndJapaneseKana", t[t.doNotCompress = 2] = "doNotCompress", t))(hm || {}), dm = /* @__PURE__ */ ((t) => (t[t.PORTRAIT = 0] = "PORTRAIT", t[t.LANDSCAPE = 1] = "LANDSCAPE", t))(dm || {}), fm = /* @__PURE__ */ ((t) => (t[t.forward = 0] = "forward", t[t.backward = 1] = "backward", t[t.front = 2] = "front", t[t.back = 3] = "back", t))(fm || {}), gm = /* @__PURE__ */ ((t) => (t[t.UNRECOGNIZED = -1] = "UNRECOGNIZED", t[t.DRAWING_IMAGE = 0] = "DRAWING_IMAGE", t[t.DRAWING_SHAPE = 1] = "DRAWING_SHAPE", t[t.DRAWING_CHART = 2] = "DRAWING_CHART", t[t.DRAWING_TABLE = 3] = "DRAWING_TABLE", t[t.DRAWING_SMART_ART = 4] = "DRAWING_SMART_ART", t[t.DRAWING_VIDEO = 5] = "DRAWING_VIDEO", t[t.DRAWING_GROUP = 6] = "DRAWING_GROUP", t[t.DRAWING_UNIT = 7] = "DRAWING_UNIT", t[t.DRAWING_DOM = 8] = "DRAWING_DOM", t))(gm || {}), Fu = /* @__PURE__ */ ((t) => (t[t.SLIDE = 0] = "SLIDE", t[t.MASTER = 1] = "MASTER", t[t.LAYOUT = 2] = "LAYOUT", t[t.HANDOUT_MASTER = 3] = "HANDOUT_MASTER", t[t.NOTES_MASTER = 4] = "NOTES_MASTER", t))(Fu || {}), pm = /* @__PURE__ */ ((t) => (t[t.SHAPE = 0] = "SHAPE", t[t.IMAGE = 1] = "IMAGE", t[t.TEXT = 2] = "TEXT", t[t.SPREADSHEET = 3] = "SPREADSHEET", t[t.DOCUMENT = 4] = "DOCUMENT", t[t.SLIDE = 5] = "SLIDE", t))(pm || {}), mm = /* @__PURE__ */ ((t) => (t[t.RELATIVE_SLIDE_LINK_UNSPECIFIED = 0] = "RELATIVE_SLIDE_LINK_UNSPECIFIED", t[t.NEXT_SLIDE = 1] = "NEXT_SLIDE", t[t.PREVIOUS_SLIDE = 2] = "PREVIOUS_SLIDE", t[t.FIRST_SLIDE = 3] = "FIRST_SLIDE", t[t.LAST_SLIDE = 4] = "LAST_SLIDE", t))(mm || {}), Fe = /* @__PURE__ */ ((t) => (t[t.UNIVER_UNKNOWN = 0] = "UNIVER_UNKNOWN", t[t.UNIVER_DOC = 1] = "UNIVER_DOC", t[t.UNIVER_SHEET = 2] = "UNIVER_SHEET", t[t.UNIVER_SLIDE = 3] = "UNIVER_SLIDE", t[t.UNIVER_PROJECT = 4] = "UNIVER_PROJECT", t[t.UNRECOGNIZED = -1] = "UNRECOGNIZED", t))(Fe || {}), Tt = /* @__PURE__ */ ((t) => (t[t.Reader = 0] = "Reader", t[t.Editor = 1] = "Editor", t[t.Owner = 2] = "Owner", t[t.UNRECOGNIZED = -1] = "UNRECOGNIZED", t))(Tt || {}), Js = /* @__PURE__ */ ((t) => (t[t.SomeCollaborator = 0] = "SomeCollaborator", t[t.AllCollaborator = 1] = "AllCollaborator", t[t.OneSelf = 2] = "OneSelf", t[t.UNRECOGNIZED = -1] = "UNRECOGNIZED", t))(Js || {});
class Ui extends nt {
}
function _m(t = re.generateRandomId(6), e = ur.EN_US, n = "") {
  return {
    id: t,
    locale: e,
    title: n,
    // title should get from request.
    tableSource: {},
    drawings: {},
    drawingsOrder: [],
    headers: {},
    footers: {},
    body: {
      dataStream: `\r
`,
      textRuns: [],
      customBlocks: [],
      tables: [],
      paragraphs: [
        {
          startIndex: 0,
          paragraphStyle: {
            spaceAbove: { v: 5 },
            lineSpacing: 1,
            spaceBelow: { v: 0 }
          }
        }
      ],
      sectionBreaks: [
        {
          startIndex: 1
        }
      ]
    },
    documentStyle: {
      pageSize: {
        width: 793.3333333333334,
        height: 1122.6666666666667
      },
      documentFlavor: ku.TRADITIONAL,
      marginTop: 50,
      marginBottom: 50,
      marginRight: 50,
      marginLeft: 50,
      renderConfig: {
        zeroWidthParagraphBreak: we.FALSE,
        vertexAngle: 0,
        centerAngle: 0,
        background: {
          rgb: "#ccc"
        }
      },
      autoHyphenation: we.TRUE,
      doNotHyphenateCaps: we.FALSE,
      consecutiveHyphenLimit: 2,
      defaultHeaderId: "",
      defaultFooterId: "",
      evenPageHeaderId: "",
      evenPageFooterId: "",
      firstPageHeaderId: "",
      firstPageFooterId: "",
      evenAndOddHeaders: we.FALSE,
      useFirstPageHeaderFooter: we.FALSE,
      marginHeader: 30,
      marginFooter: 30
    },
    settings: {}
  };
}
var $n = {}, Ir = {}, vr = {}, qo;
function Em() {
  if (qo) return vr;
  qo = 1, Object.defineProperty(vr, "__esModule", { value: !0 });
  function t(r, s) {
    if (Array.isArray(s))
      return !1;
    for (let i in r)
      if (!n(r[i], s[i]))
        return !1;
    for (let i in s)
      if (r[i] === void 0)
        return !1;
    return !0;
  }
  function e(r, s) {
    if (!Array.isArray(s) || r.length !== s.length)
      return !1;
    for (let i = 0; i < r.length; i++)
      if (!n(r[i], s[i]))
        return !1;
    return !0;
  }
  function n(r, s) {
    return r === s ? !0 : r === null || s === null || typeof r != "object" || typeof s != "object" ? !1 : Array.isArray(r) ? e(r, s) : t(r, s);
  }
  return vr.default = n, vr;
}
var yr = {}, ea;
function Cm() {
  if (ea) return yr;
  ea = 1, Object.defineProperty(yr, "__esModule", { value: !0 });
  function t(e) {
    if (e === null)
      return null;
    if (Array.isArray(e))
      return e.map(t);
    if (typeof e == "object") {
      const n = {};
      for (let r in e)
        n[r] = t(e[r]);
      return n;
    } else
      return e;
  }
  return yr.default = t, yr;
}
var Ns = {}, ta;
function $u() {
  return ta || (ta = 1, function(t) {
    Object.defineProperty(t, "__esModule", { value: !0 }), t.eachChildOf = t.advancer = t.readCursor = t.writeCursor = t.WriteCursor = t.ReadCursor = t.isValidPathItem = void 0;
    function e(l, h) {
      if (!l)
        throw new Error(h);
    }
    const n = (l) => l != null && typeof l == "object" && !Array.isArray(l), r = (l, h) => (
      // All the numbers, then all the letters. Just as the gods of ascii intended.
      typeof l == typeof h ? l > h : typeof l == "string" && typeof h == "number"
    );
    function s(l, h) {
      for (let d in l) {
        const f = d;
        h.write(f, l[f]);
      }
    }
    t.isValidPathItem = (l) => typeof l == "number" || typeof l == "string" && l !== "__proto__";
    class i {
      constructor(h = null) {
        this.parents = [], this.indexes = [], this.lcIdx = -1, this.idx = -1, this.container = h;
      }
      ascend() {
        e(this.parents.length === this.indexes.length / 2), this.idx === 0 ? this.parents.length ? (this.lcIdx = this.indexes.pop(), this.container = this.parents.pop(), this.idx = this.indexes.pop()) : (this.lcIdx = 0, this.idx = -1) : (e(this.idx > 0), this.idx--, n(this.container[this.idx]) && this.idx--);
      }
      getPath() {
        const h = [];
        let d = this.container, f = this.parents.length - 1, E = this.idx;
        for (; E >= 0; )
          h.unshift(d[E]), E === 0 ? (E = this.indexes[f * 2], d = this.parents[f--]) : E -= n(d[E - 1]) ? 2 : 1;
        return h;
      }
    }
    class o extends i {
      get() {
        return this.container ? this.container.slice(this.idx + 1) : null;
      }
      // Its only valid to call this after descending into a child.
      getKey() {
        return e(this.container != null, "Invalid call to getKey before cursor descended"), this.container[this.idx];
      }
      getComponent() {
        let h;
        return this.container && this.container.length > this.idx + 1 && n(h = this.container[this.idx + 1]) ? h : null;
      }
      descendFirst() {
        let h = this.idx + 1;
        if (!this.container || h >= this.container.length || n(this.container[h]) && h + 1 >= this.container.length)
          return !1;
        n(this.container[h]) && h++;
        const d = this.container[h];
        return Array.isArray(d) ? (this.indexes.push(this.idx), this.parents.push(this.container), this.indexes.push(h), this.idx = 0, this.container = d) : this.idx = h, !0;
      }
      nextSibling() {
        if (e(this.parents.length === this.indexes.length / 2), this.idx > 0 || this.parents.length === 0)
          return !1;
        const h = this.indexes[this.indexes.length - 1] + 1, d = this.parents[this.parents.length - 1];
        return h >= d.length ? !1 : (e(!isNaN(h)), this.indexes[this.indexes.length - 1] = h, this.container = d[h], !0);
      }
      _init(h, d, f, E) {
        this.container = h, this.idx = d, this.parents = f.slice(), this.indexes = E.slice();
      }
      clone() {
        const h = new o();
        return h._init(this.container, this.idx, this.parents, this.indexes), h;
      }
      *[Symbol.iterator]() {
        if (this.descendFirst()) {
          do
            yield this.getKey();
          while (this.nextSibling());
          this.ascend();
        }
      }
      // TODO(cleanup): Consider moving these functions out of cursor, since
      // they're really just helper methods.
      // It'd be really nice to do this using generators.
      traverse(h, d) {
        const f = this.getComponent();
        f && d(f, h);
        for (const E of this)
          h && h.descend(E), this.traverse(h, d), h && h.ascend();
      }
      eachPick(h, d) {
        this.traverse(h, (f, E) => {
          f.p != null && d(f.p, E);
        });
      }
      eachDrop(h, d) {
        this.traverse(h, (f, E) => {
          f.d != null && d(f.d, E);
        });
      }
    }
    t.ReadCursor = o;
    class a extends i {
      constructor(h = null) {
        super(h), this.pendingDescent = [], this._op = h;
      }
      flushDescent() {
        e(this.parents.length === this.indexes.length / 2), this.container === null && (this._op = this.container = []);
        for (let h = 0; h < this.pendingDescent.length; h++) {
          const d = this.pendingDescent[h];
          let f = this.idx + 1;
          if (f < this.container.length && n(this.container[f]) && f++, e(f === this.container.length || !n(this.container[f])), f === this.container.length)
            this.container.push(d), this.idx = f;
          else if (this.container[f] === d)
            this.idx = f;
          else {
            if (!Array.isArray(this.container[f])) {
              const E = this.container.splice(f, this.container.length - f);
              this.container.push(E), this.lcIdx > -1 && (this.lcIdx = f);
            }
            for (this.indexes.push(this.idx), this.parents.push(this.container), this.lcIdx !== -1 && (e(r(d, this.container[this.lcIdx][0])), f = this.lcIdx + 1, this.lcIdx = -1); f < this.container.length && r(d, this.container[f][0]); )
              f++;
            if (this.indexes.push(f), this.idx = 0, f < this.container.length && this.container[f][0] === d)
              this.container = this.container[f];
            else {
              const E = [d];
              this.container.splice(f, 0, E), this.container = E;
            }
          }
        }
        this.pendingDescent.length = 0;
      }
      reset() {
        this.lcIdx = -1;
      }
      // Creates and returns a component, creating one if need be. You should
      // probably write to it immediately - ops are not valid with empty
      // components.
      getComponent() {
        this.flushDescent();
        const h = this.idx + 1;
        if (h < this.container.length && n(this.container[h]))
          return this.container[h];
        {
          const d = {};
          return this.container.splice(h, 0, d), d;
        }
      }
      write(h, d) {
        const f = this.getComponent();
        e(f[h] == null || f[h] === d, "Internal consistency error: Overwritten component. File a bug"), f[h] = d;
      }
      get() {
        return this._op;
      }
      descend(h) {
        if (!t.isValidPathItem(h))
          throw Error("Invalid JSON key");
        this.pendingDescent.push(h);
      }
      descendPath(h) {
        return this.pendingDescent.push(...h), this;
      }
      ascend() {
        this.pendingDescent.length ? this.pendingDescent.pop() : super.ascend();
      }
      mergeTree(h, d = s) {
        if (h === null)
          return;
        if (e(Array.isArray(h)), h === this._op)
          throw Error("Cannot merge into my own tree");
        const f = this.lcIdx, E = this.parents.length;
        let R = 0;
        for (let O = 0; O < h.length; O++) {
          const U = h[O];
          typeof U == "string" || typeof U == "number" ? (R++, this.descend(U)) : Array.isArray(U) ? this.mergeTree(U, d) : typeof U == "object" && d(U, this);
        }
        for (; R--; )
          this.ascend();
        this.lcIdx = this.parents.length === E ? f : -1;
      }
      at(h, d) {
        this.descendPath(h), d(this);
        for (let f = 0; f < h.length; f++)
          this.ascend();
        return this;
      }
      // This is used by helpers, so the strict ordering guarantees are
      // relaxed.
      writeAtPath(h, d, f) {
        return this.at(h, () => this.write(d, f)), this.reset(), this;
      }
      writeMove(h, d, f = 0) {
        return this.writeAtPath(h, "p", f).writeAtPath(d, "d", f);
      }
      getPath() {
        const h = super.getPath();
        return h.push(...this.pendingDescent), h;
      }
    }
    t.WriteCursor = a, t.writeCursor = () => new a(), t.readCursor = (l) => new o(l);
    function u(l, h, d) {
      let f, E;
      E = f = l ? l.descendFirst() : !1;
      function R(O) {
        let U;
        for (; E; ) {
          const ne = U = l.getKey();
          if (O != null) {
            let X = !1;
            if (h && typeof ne == "number" && (U = h(ne, l.getComponent()), U < 0 && (U = ~U, X = !0)), r(U, O))
              return null;
            if (U === O && !X)
              return l;
          }
          d && typeof U == "number" && d(U, l.getComponent()), E = l.nextSibling();
        }
        return null;
      }
      return R.end = () => {
        f && l.ascend();
      }, R;
    }
    t.advancer = u;
    function c(l, h, d) {
      let f, E, R, O;
      for (f = E = l && l.descendFirst(), R = O = h && h.descendFirst(); f || R; ) {
        let U = f ? l.getKey() : null, ne = R ? h.getKey() : null;
        U !== null && ne !== null && (r(ne, U) ? ne = null : U !== ne && (U = null)), d(U == null ? ne : U, U != null ? l : null, ne != null ? h : null), U != null && f && (f = l.nextSibling()), ne != null && R && (R = h.nextSibling());
      }
      E && l.ascend(), O && h.ascend();
    }
    t.eachChildOf = c;
  }(Ns)), Ns;
}
var Ts = {}, na;
function Bu() {
  return na || (na = 1, function(t) {
    Object.defineProperty(t, "__esModule", { value: !0 }), t.ConflictType = void 0, function(e) {
      e[e.RM_UNEXPECTED_CONTENT = 1] = "RM_UNEXPECTED_CONTENT", e[e.DROP_COLLISION = 2] = "DROP_COLLISION", e[e.BLACKHOLE = 3] = "BLACKHOLE";
    }(t.ConflictType || (t.ConflictType = {}));
  }(Ts)), Ts;
}
var an = {}, un = {}, ra;
function Pi() {
  return ra || (ra = 1, Object.defineProperty(un, "__esModule", { value: !0 }), un.uniToStrPos = un.strPosToUni = void 0, un.strPosToUni = (t, e = t.length) => {
    let n = 0, r = 0;
    for (; r < e; r++) {
      const s = t.charCodeAt(r);
      s >= 55296 && s <= 57343 && (n++, r++);
    }
    if (r !== e)
      throw Error("Invalid offset - splits unicode bytes");
    return r - n;
  }, un.uniToStrPos = (t, e) => {
    let n = 0;
    for (; e > 0; e--) {
      const r = t.charCodeAt(n);
      n += r >= 55296 && r <= 57343 ? 2 : 1;
    }
    return n;
  }), un;
}
var Ms = {}, sa;
function Zs() {
  return sa || (sa = 1, function(t) {
    Object.defineProperty(t, "__esModule", { value: !0 }), t.uniSlice = t.dlen = t.eachOp = void 0;
    const e = Pi(), n = (T) => {
      if (!Array.isArray(T))
        throw Error("Op must be an array of components");
      let A = null;
      for (let H = 0; H < T.length; H++) {
        const Z = T[H];
        switch (typeof Z) {
          case "object":
            if (typeof Z.d != "number" && typeof Z.d != "string")
              throw Error("Delete must be number or string");
            if (t.dlen(Z.d) <= 0)
              throw Error("Deletes must not be empty");
            break;
          case "string":
            if (!(Z.length > 0))
              throw Error("Inserts cannot be empty");
            break;
          case "number":
            if (!(Z > 0))
              throw Error("Skip components must be >0");
            if (typeof A == "number")
              throw Error("Adjacent skip components should be combined");
            break;
        }
        A = Z;
      }
      if (typeof A == "number")
        throw Error("Op has a trailing skip");
    };
    function r(T, A) {
      let H = 0, Z = 0;
      for (let fe = 0; fe < T.length; fe++) {
        const ae = T[fe];
        switch (A(ae, H, Z), typeof ae) {
          case "object":
            H += t.dlen(ae.d);
            break;
          case "string":
            Z += e.strPosToUni(ae);
            break;
          case "number":
            H += ae, Z += ae;
            break;
        }
      }
    }
    t.eachOp = r;
    function s(T, A) {
      const H = [], Z = a(H);
      return r(T, (fe, ae, m) => {
        Z(A(fe, ae, m));
      }), h(H);
    }
    const i = (T) => T, o = (T) => s(T, i);
    t.dlen = (T) => typeof T == "number" ? T : e.strPosToUni(T);
    const a = (T) => (A) => {
      if (!(!A || A.d === 0 || A.d === "")) if (T.length === 0)
        T.push(A);
      else if (typeof A == typeof T[T.length - 1])
        if (typeof A == "object") {
          const H = T[T.length - 1];
          H.d = typeof H.d == "string" && typeof A.d == "string" ? H.d + A.d : t.dlen(H.d) + t.dlen(A.d);
        } else
          T[T.length - 1] += A;
      else
        T.push(A);
    }, u = (T) => typeof T == "number" ? T : typeof T == "string" ? e.strPosToUni(T) : typeof T.d == "number" ? T.d : e.strPosToUni(T.d);
    t.uniSlice = (T, A, H) => {
      const Z = e.uniToStrPos(T, A), fe = H == null ? 1 / 0 : e.uniToStrPos(T, H);
      return T.slice(Z, fe);
    };
    const c = (T, A, H) => typeof T == "number" ? H == null ? T - A : Math.min(T, H) - A : t.uniSlice(T, A, H), l = (T) => {
      let A = 0, H = 0;
      return { take: (ae, m) => {
        if (A === T.length)
          return ae === -1 ? null : ae;
        const j = T[A];
        let y;
        if (typeof j == "number")
          return ae === -1 || j - H <= ae ? (y = j - H, ++A, H = 0, y) : (H += ae, ae);
        if (typeof j == "string") {
          if (ae === -1 || m === "i" || e.strPosToUni(j.slice(H)) <= ae)
            return y = j.slice(H), ++A, H = 0, y;
          {
            const M = H + e.uniToStrPos(j.slice(H), ae);
            return y = j.slice(H, M), H = M, y;
          }
        } else {
          if (ae === -1 || m === "d" || t.dlen(j.d) - H <= ae)
            return y = { d: c(j.d, H) }, ++A, H = 0, y;
          {
            let M = c(j.d, H, H + ae);
            return H += ae, { d: M };
          }
        }
      }, peek: () => T[A] };
    }, h = (T) => (T.length > 0 && typeof T[T.length - 1] == "number" && T.pop(), T);
    function d(T, A, H) {
      if (H !== "left" && H !== "right")
        throw Error("side (" + H + ") must be 'left' or 'right'");
      n(T), n(A);
      const Z = [], fe = a(Z), { take: ae, peek: m } = l(T);
      for (let y = 0; y < A.length; y++) {
        const M = A[y];
        let b, w;
        switch (typeof M) {
          case "number":
            for (b = M; b > 0; )
              w = ae(b, "i"), fe(w), typeof w != "string" && (b -= u(w));
            break;
          case "string":
            H === "left" && typeof m() == "string" && fe(ae(-1)), fe(e.strPosToUni(M));
            break;
          case "object":
            for (b = t.dlen(M.d); b > 0; )
              switch (w = ae(b, "i"), typeof w) {
                case "number":
                  b -= w;
                  break;
                case "string":
                  fe(w);
                  break;
                case "object":
                  b -= t.dlen(w.d);
              }
            break;
        }
      }
      let j;
      for (; j = ae(-1); )
        fe(j);
      return h(Z);
    }
    function f(T, A) {
      n(T), n(A);
      const H = [], Z = a(H), { take: fe } = l(T);
      for (let m = 0; m < A.length; m++) {
        const j = A[m];
        let y, M;
        switch (typeof j) {
          case "number":
            for (y = j; y > 0; )
              M = fe(y, "d"), Z(M), typeof M != "object" && (y -= u(M));
            break;
          case "string":
            Z(j);
            break;
          case "object":
            y = t.dlen(j.d);
            let b = 0;
            for (; b < y; )
              switch (M = fe(y - b, "d"), typeof M) {
                case "number":
                  Z({ d: c(j.d, b, b + M) }), b += M;
                  break;
                case "string":
                  b += e.strPosToUni(M);
                  break;
                case "object":
                  Z(M);
              }
            break;
        }
      }
      let ae;
      for (; ae = fe(-1); )
        Z(ae);
      return h(H);
    }
    const E = (T, A) => {
      let H = 0;
      for (let Z = 0; Z < A.length && T > H; Z++) {
        const fe = A[Z];
        switch (typeof fe) {
          case "number": {
            H += fe;
            break;
          }
          case "string":
            const ae = e.strPosToUni(fe);
            H += ae, T += ae;
            break;
          case "object":
            T -= Math.min(t.dlen(fe.d), T - H);
            break;
        }
      }
      return T;
    }, R = (T, A) => typeof T == "number" ? E(T, A) : T.map((H) => E(H, A));
    function O(T, A, H) {
      return s(T, (Z, fe) => typeof Z == "object" && typeof Z.d == "number" ? { d: H.slice(A, fe, fe + Z.d) } : Z);
    }
    function U(T) {
      return s(T, (A) => {
        switch (typeof A) {
          case "object":
            if (typeof A.d == "number")
              throw Error("Cannot invert text op: Deleted characters missing from operation. makeInvertible must be called first.");
            return A.d;
          // delete -> insert
          case "string":
            return { d: A };
          // Insert -> delete
          case "number":
            return A;
        }
      });
    }
    function ne(T) {
      return s(T, (A) => typeof A == "object" && typeof A.d == "string" ? { d: e.strPosToUni(A.d) } : A);
    }
    function X(T) {
      let A = !0;
      return r(T, (H) => {
        typeof H == "object" && typeof H.d == "number" && (A = !1);
      }), A;
    }
    function de(T) {
      return {
        name: "text-unicode",
        uri: "http://sharejs.org/types/text-unicode",
        trim: h,
        normalize: o,
        checkOp: n,
        /** Create a new text snapshot.
         *
         * @param {string} initial - initial snapshot data. Optional. Defaults to ''.
         * @returns {Snap} Initial document snapshot object
         */
        create(A = "") {
          if (typeof A != "string")
            throw Error("Initial data must be a string");
          return T.create(A);
        },
        /** Apply an operation to a document snapshot
         */
        apply(A, H) {
          n(H);
          const Z = T.builder(A);
          for (let fe = 0; fe < H.length; fe++) {
            const ae = H[fe];
            switch (typeof ae) {
              case "number":
                Z.skip(ae);
                break;
              case "string":
                Z.append(ae);
                break;
              case "object":
                Z.del(t.dlen(ae.d));
                break;
            }
          }
          return Z.build();
        },
        transform: d,
        compose: f,
        transformPosition: E,
        transformSelection: R,
        isInvertible: X,
        makeInvertible(A, H) {
          return O(A, H, T);
        },
        stripInvertible: ne,
        invert: U,
        invertWithDoc(A, H) {
          return U(O(A, H, T));
        },
        isNoop: (A) => A.length === 0
      };
    }
    t.default = de;
  }(Ms)), Ms;
}
var wr = {}, ia;
function Rm() {
  if (ia) return wr;
  ia = 1, Object.defineProperty(wr, "__esModule", { value: !0 });
  const t = Zs(), e = Pi();
  function n(r, s) {
    return {
      // Returns the text content of the document
      get: r,
      // Returns the number of characters in the string
      getLength() {
        return r().length;
      },
      // Insert the specified text at the given position in the document
      insert(i, o, a) {
        const u = e.strPosToUni(r(), i);
        return s([u, o], a);
      },
      remove(i, o, a) {
        const u = e.strPosToUni(r(), i);
        return s([u, { d: o }], a);
      },
      // When you use this API, you should implement these two methods
      // in your editing context.
      //onInsert: function(pos, text) {},
      //onRemove: function(pos, removedLength) {},
      _onOp(i) {
        t.eachOp(i, (o, a, u) => {
          switch (typeof o) {
            case "string":
              this.onInsert && this.onInsert(u, o);
              break;
            case "object":
              const c = t.dlen(o.d);
              this.onRemove && this.onRemove(u, c);
          }
        });
      },
      onInsert: null,
      onRemove: null
    };
  }
  return wr.default = n, n.provides = { text: !0 }, wr;
}
var oa;
function Im() {
  return oa || (oa = 1, function(t) {
    var e = an.__createBinding || (Object.create ? function(d, f, E, R) {
      R === void 0 && (R = E), Object.defineProperty(d, R, { enumerable: !0, get: function() {
        return f[E];
      } });
    } : function(d, f, E, R) {
      R === void 0 && (R = E), d[R] = f[E];
    }), n = an.__setModuleDefault || (Object.create ? function(d, f) {
      Object.defineProperty(d, "default", { enumerable: !0, value: f });
    } : function(d, f) {
      d.default = f;
    }), r = an.__importStar || function(d) {
      if (d && d.__esModule) return d;
      var f = {};
      if (d != null) for (var E in d) Object.hasOwnProperty.call(d, E) && e(f, d, E);
      return n(f, d), f;
    }, s = an.__importDefault || function(d) {
      return d && d.__esModule ? d : { default: d };
    };
    Object.defineProperty(t, "__esModule", { value: !0 }), t.type = t.remove = t.insert = void 0;
    const i = Pi(), o = r(Zs()), a = s(Rm()), u = {
      create(d) {
        return d;
      },
      toString(d) {
        return d;
      },
      builder(d) {
        if (typeof d != "string")
          throw Error("Invalid document snapshot: " + d);
        const f = [];
        return {
          skip(E) {
            let R = i.uniToStrPos(d, E);
            if (R > d.length)
              throw Error("The op is too long for this document");
            f.push(d.slice(0, R)), d = d.slice(R);
          },
          append(E) {
            f.push(E);
          },
          del(E) {
            d = d.slice(i.uniToStrPos(d, E));
          },
          build() {
            return f.join("") + d;
          }
        };
      },
      slice: o.uniSlice
    }, c = o.default(u), l = Object.assign(Object.assign({}, c), { api: a.default });
    t.type = l, t.insert = (d, f) => f.length === 0 ? [] : d === 0 ? [f] : [d, f], t.remove = (d, f) => o.dlen(f) === 0 ? [] : d === 0 ? [{ d: f }] : [d, { d: f }];
    var h = Zs();
    Object.defineProperty(t, "makeType", { enumerable: !0, get: function() {
      return h.default;
    } });
  }(an)), an;
}
var aa;
function vm() {
  return aa || (aa = 1, function(t) {
    var e = Ir.__importDefault || function(v) {
      return v && v.__esModule ? v : {
        default: v
      };
    };
    Object.defineProperty(t, "__esModule", {
      value: !0
    }), t.editOp = t.replaceOp = t.insertOp = t.moveOp = t.removeOp = t.type = void 0;
    const n = e(Em()), r = e(Cm()), s = $u(), i = Bu();
    function o(v, F) {
      if (!v) throw new Error(F);
    }
    t.type = {
      name: "json1",
      uri: "http://sharejs.org/types/JSONv1",
      readCursor: s.readCursor,
      writeCursor: s.writeCursor,
      create: (v) => v,
      isNoop: (v) => v == null,
      setDebug(v) {
      },
      registerSubtype: U,
      checkValidOp: fe,
      normalize: ae,
      apply: m,
      transformPosition: j,
      compose: y,
      tryTransform: Y,
      transform: he,
      makeInvertible: w,
      invert: M,
      invertWithDoc: k,
      RM_UNEXPECTED_CONTENT: i.ConflictType.RM_UNEXPECTED_CONTENT,
      DROP_COLLISION: i.ConflictType.DROP_COLLISION,
      BLACKHOLE: i.ConflictType.BLACKHOLE,
      transformNoConflict: (v, F, V) => be(() => !0, v, F, V),
      typeAllowingConflictsPred: (v) => Object.assign(Object.assign({}, t.type), {
        transform: (F, V, K) => be(v, F, V, K)
      })
    };
    const a = (v) => v ? v.getComponent() : null;
    function u(v) {
      return v && typeof v == "object" && !Array.isArray(v);
    }
    const c = (v) => Array.isArray(v) ? v.slice() : v !== null && typeof v == "object" ? Object.assign({}, v) : v, l = (v) => v && (v.p != null || v.r !== void 0), h = (v) => v && (v.d != null || v.i !== void 0);
    function d(v, F) {
      return o(v != null), typeof F == "number" ? (o(Array.isArray(v), "Invalid key - child is not an array"), (v = v.slice()).splice(F, 1)) : (o(u(v), "Invalid key - child is not an object"), delete (v = Object.assign({}, v))[F]), v;
    }
    function f(v, F, V) {
      return typeof F == "number" ? (o(v != null, "Container is missing for key"), o(Array.isArray(v), "Cannot use numerical key for object container"), o(v.length >= F, "Cannot insert into out of bounds index"), v.splice(F, 0, V)) : (o(u(v), "Cannot insert into missing item"), o(v[F] === void 0, "Trying to overwrite value at key. Your op needs to remove it first"), v[F] = V), V;
    }
    t.removeOp = (v, F = !0) => s.writeCursor().writeAtPath(v, "r", F).get(), t.moveOp = (v, F) => s.writeCursor().writeMove(v, F).get(), t.insertOp = (v, F) => s.writeCursor().writeAtPath(v, "i", F).get(), t.replaceOp = (v, F, V) => s.writeCursor().at(v, (K) => {
      K.write("r", F), K.write("i", V);
    }).get(), t.editOp = (v, F, V, K = !1) => s.writeCursor().at(v, (z) => A(z, F, V, K)).get();
    const E = (v, F) => v != null && (typeof F == "number" ? Array.isArray(v) : typeof v == "object"), R = (v, F) => E(v, F) ? v[F] : void 0, O = {};
    function U(v) {
      let F = v.type ? v.type : v;
      F.name && (O[F.name] = F), F.uri && (O[F.uri] = F);
    }
    const ne = (v) => {
      const F = O[v];
      if (F) return F;
      throw Error("Missing type: " + v);
    };
    U(Im());
    const X = (v, F) => v + F;
    U({
      name: "number",
      apply: X,
      compose: X,
      invert: (v) => -v,
      transform: (v) => v
    });
    const de = (v) => v == null ? null : v.et ? ne(v.et) : v.es ? O["text-unicode"] : v.ena != null ? O.number : null, T = (v) => v.es ? v.es : v.ena != null ? v.ena : v.e, A = (v, F, V, K = !1) => {
      const [z, W] = typeof F == "string" ? [ne(F), F] : [F, F.name];
      !K && z.isNoop && z.isNoop(V) || (W === "number" ? v.write("ena", V) : W === "text-unicode" ? v.write("es", V) : (v.write("et", W), v.write("e", V)));
    };
    function H(v) {
      o(typeof v == "number"), o(v >= 0), o(v === (0 | v));
    }
    function Z(v) {
      typeof v == "number" ? H(v) : o(typeof v == "string");
    }
    function fe(v) {
      if (v === null) return;
      const F = /* @__PURE__ */ new Set(), V = /* @__PURE__ */ new Set(), K = (W) => {
        let ue = !0, oe = !1;
        for (let B in W) {
          const ee = W[B];
          if (ue = !1, o(B === "p" || B === "r" || B === "d" || B === "i" || B === "e" || B === "es" || B === "ena" || B === "et", "Invalid component item '" + B + "'"), B === "p") H(ee), o(!F.has(ee)), F.add(ee), o(W.r === void 0);
          else if (B === "d") H(ee), o(!V.has(ee)), V.add(ee), o(W.i === void 0);
          else if (B === "e" || B === "es" || B === "ena") {
            o(!oe), oe = !0;
            const ie = de(W);
            o(ie, "Missing type in edit"), ie.checkValidOp && ie.checkValidOp(T(W));
          }
        }
        o(!ue);
      }, z = (W, ue, oe) => {
        if (!Array.isArray(W)) throw Error("Op must be null or a list");
        if (W.length === 0) throw Error("Empty descent");
        ue || Z(W[0]);
        let B = 1, ee = 0, ie = 0;
        for (let pe = 0; pe < W.length; pe++) {
          const Oe = W[pe];
          if (o(Oe != null), Array.isArray(Oe)) {
            const Me = z(Oe, !1);
            if (ee) {
              const G = typeof ie, Re = typeof Me;
              G === Re ? o(ie < Me, "descent keys are not in order") : o(G === "number" && Re === "string");
            }
            ie = Me, ee++, B = 3;
          } else typeof Oe == "object" ? (o(B === 1, `Prev not scalar - instead ${B}`), K(Oe), B = 2) : (o(B !== 3), Z(Oe), o(s.isValidPathItem(Oe), "Invalid path key"), B = 1);
        }
        return o(ee !== 1, "Operation makes multiple descents. Remove some []"), o(B === 2 || B === 3), W[0];
      };
      z(v, !0), o(F.size === V.size, "Mismatched picks and drops in op");
      for (let W = 0; W < F.size; W++) o(F.has(W)), o(V.has(W));
    }
    function ae(v) {
      let F = 0, V = [];
      const K = s.writeCursor();
      return K.mergeTree(v, (z, W) => {
        const ue = de(z);
        if (ue) {
          const B = T(z);
          A(W, ue, ue.normalize ? ue.normalize(B) : B);
        }
        for (const B of ["r", "p", "i", "d"]) if (z[B] !== void 0) {
          const ee = B === "p" || B === "d" ? (oe = z[B], V[oe] == null && (V[oe] = F++), V[oe]) : z[B];
          W.write(B, ee);
        }
        var oe;
      }), K.get();
    }
    function m(v, F) {
      if (fe(F), F === null) return v;
      const V = [];
      return function K(z, W) {
        let ue = z, oe = 0, B = {
          root: z
        }, ee = 0, ie = B, pe = "root";
        function Oe() {
          for (; ee < oe; ee++) {
            let Me = W[ee];
            typeof Me != "object" && (o(E(ie, pe)), ie = ie[pe] = c(ie[pe]), pe = Me);
          }
        }
        for (; oe < W.length; oe++) {
          const Me = W[oe];
          if (Array.isArray(Me)) {
            const G = K(ue, Me);
            G !== ue && G !== void 0 && (Oe(), ue = ie[pe] = G);
          } else if (typeof Me == "object") {
            Me.d != null ? (Oe(), ue = f(ie, pe, V[Me.d])) : Me.i !== void 0 && (Oe(), ue = f(ie, pe, Me.i));
            const G = de(Me);
            if (G) Oe(), ue = ie[pe] = G.apply(ue, T(Me));
            else if (Me.e !== void 0) throw Error("Subtype " + Me.et + " undefined");
          } else ue = R(ue, Me);
        }
        return B.root;
      }(v = function K(z, W) {
        const ue = [];
        let oe = 0;
        for (; oe < W.length; oe++) {
          const pe = W[oe];
          if (Array.isArray(pe)) break;
          typeof pe != "object" && (ue.push(z), z = R(z, pe));
        }
        for (let pe = W.length - 1; pe >= oe; pe--) z = K(z, W[pe]);
        for (--oe; oe >= 0; oe--) {
          const pe = W[oe];
          if (typeof pe != "object") {
            const Oe = ue.pop();
            z = z === R(Oe, pe) ? Oe : z === void 0 ? d(Oe, pe) : (ee = pe, ie = z, (B = c(B = Oe))[ee] = ie, B);
          } else l(pe) && (o(z !== void 0, "Cannot pick up or remove undefined"), pe.p != null && (V[pe.p] = z), z = void 0);
        }
        var B, ee, ie;
        return z;
      }(v, F), F);
    }
    function j(v, F) {
      v = v.slice(), fe(F);
      const V = s.readCursor(F);
      let K, z, W = !1;
      const ue = [];
      for (let B = 0; ; B++) {
        const ee = v[B], ie = V.getComponent();
        if (ie && (ie.r !== void 0 ? W = !0 : ie.p != null && (W = !1, K = ie.p, z = B)), B >= v.length) break;
        let pe = 0;
        const Oe = s.advancer(V, void 0, (G, Re) => {
          l(Re) && pe++;
        });
        ue.unshift(Oe);
        const Me = Oe(ee);
        if (typeof ee == "number" && (v[B] -= pe), !Me) break;
      }
      if (ue.forEach((B) => B.end()), W) return null;
      const oe = () => {
        let B = 0;
        if (K != null) {
          const ee = V.getPath();
          B = ee.length, v = ee.concat(v.slice(z));
        }
        for (; B < v.length; B++) {
          const ee = v[B], ie = a(V), pe = de(ie);
          if (pe) {
            const G = T(ie);
            pe.transformPosition && (v[B] = pe.transformPosition(v[B], G));
            break;
          }
          let Oe = 0;
          const Me = s.advancer(V, (G, Re) => h(Re) ? ~(G - Oe) : G - Oe, (G, Re) => {
            h(Re) && Oe++;
          })(ee);
          if (typeof ee == "number" && (v[B] += Oe), !Me) break;
        }
      };
      return K != null ? V.eachDrop(null, (B) => {
        B === K && oe();
      }) : oe(), v;
    }
    function y(v, F) {
      if (fe(v), fe(F), v == null) return F;
      if (F == null) return v;
      let V = 0;
      const K = s.readCursor(v), z = s.readCursor(F), W = s.writeCursor(), ue = [], oe = [], B = [], ee = [], ie = [], pe = [], Oe = /* @__PURE__ */ new Set();
      K.traverse(null, (G) => {
        G.p != null && (B[G.p] = K.clone());
      }), z.traverse(null, (G) => {
        G.d != null && (ee[G.d] = z.clone());
      });
      const Me = s.writeCursor();
      return function G(Re, He, Be, xe, Je, Rt, We, et) {
        o(He || Be);
        const ze = a(He), ct = a(Be), it = !!ct && ct.r !== void 0, xt = !!ze && ze.i !== void 0, ke = ze ? ze.d : null, ht = ct ? ct.p : null, _ = (Rt || it) && ht == null;
        if (ht != null) xe = ee[ht], We = oe[ht] = new s.WriteCursor();
        else if (ct && ct.r !== void 0) xe = null;
        else {
          const D = a(xe);
          D && D.d != null && (xe = null);
        }
        const g = a(xe);
        if (ke != null) if (Re = B[ke], et = ue[ke] = new s.WriteCursor(), _) Rt && !it && et.write("r", !0);
        else {
          const D = ie[ke] = V++;
          We.write("d", D);
        }
        else if (ze && ze.i !== void 0) Re = null;
        else {
          const D = a(Re);
          D && D.p != null && (Re = null);
        }
        let p;
        xt ? (o(Je === void 0), p = ze.i) : p = Je;
        const S = (ht == null ? !xt || Rt || it : p === void 0) ? null : We.getComponent();
        if (ht != null) {
          if (!(Je !== void 0 || xt)) {
            const D = ke != null ? ie[ke] : V++;
            pe[ht] = D, et.write("p", D);
          }
        } else it && (xt || Je !== void 0 || (ct.r, et.write("r", ct.r)));
        const N = _ ? null : de(ze), L = de(g);
        if ((N || L) && (N && N.name, L && L.name), N && L) {
          o(N === L);
          const D = T(ze), q = T(g), Ce = N.compose(D, q);
          A(We, N, Ce), Oe.add(g);
        } else N ? A(We, N, T(ze)) : L && (A(We, L, T(g)), Oe.add(g));
        const x = typeof p == "object" && p != null;
        let P = !1, I = 0, Q = 0, _e = 0, J = 0, me = 0;
        const ye = s.advancer(xe, (D, q) => h(q) ? J - D - 1 : D - J, (D, q) => {
          h(q) && J++;
        }), le = s.advancer(Re, (D, q) => l(q) ? I - D - 1 : D - I, (D, q) => {
          l(q) && I++;
        });
        if (s.eachChildOf(He, Be, (D, q, Ce) => {
          let Se, Le, Ue = D, je = D, dt = D;
          if (typeof D == "number") {
            let Ne = D + _e;
            Le = ye(Ne), je = Ne + J;
            let te = D + Q;
            Se = le(te), h(a(Le)) && (Se = null), Ue = te + I, dt = D + me, o(Ue >= 0, "p1PickKey is negative"), o(je >= 0, "p2DropKey is negative");
            const ut = h(a(q)), $e = l(a(Ce));
            (ut || $e && !_) && me--, ut && Q--, $e && _e--;
          } else Se = le(D), Le = ye(D);
          et.descend(Ue), We.descend(je);
          const pt = x && !h(a(q)) ? p[dt] : void 0, Ee = G(Se, q, Ce, Le, pt, _, We, et);
          var qe, ve, Ie;
          x && !_ ? pt !== Ee && (P || (p = Array.isArray(p) ? p.slice() : Object.assign({}, p), P = !0), qe = p, Ie = Ee, typeof (ve = dt) == "number" ? (o(Array.isArray(qe)), o(ve < qe.length)) : (o(!Array.isArray(qe)), o(qe[ve] !== void 0)), Ie === void 0 ? typeof ve == "number" ? qe.splice(ve, 1) : delete qe[ve] : qe[ve] = Ie) : o(Ee === void 0), We.ascend(), et.ascend();
        }), le.end(), ye.end(), S != null) S.i = p;
        else if (!Rt && !it && ht == null) return p;
      }(K, K.clone(), z, z.clone(), void 0, !1, W, Me), W.reset(), W.mergeTree(Me.get()), W.reset(), W.get(), ue.map((G) => G.get()), oe.map((G) => G.get()), K.traverse(W, (G, Re) => {
        const He = G.p;
        if (He != null) {
          const Be = ie[He];
          Be != null && Re.write("p", Be);
          const xe = ue[He];
          xe && xe.get(), xe && Re.mergeTree(xe.get());
        } else G.r !== void 0 && Re.write("r", G.r);
      }), W.reset(), W.get(), z.traverse(W, (G, Re) => {
        const He = G.d;
        if (He != null) {
          const xe = pe[He];
          xe != null && Re.write("d", xe);
          const Je = oe[He];
          Je && Re.mergeTree(Je.get());
        } else G.i !== void 0 && Re.write("i", G.i);
        const Be = de(G);
        Be && !Oe.has(G) && A(Re, Be, T(G));
      }), W.get();
    }
    function M(v) {
      if (v == null) return null;
      const F = new s.ReadCursor(v), V = new s.WriteCursor();
      let K;
      const z = [], W = [];
      return function ue(oe, B, ee) {
        const ie = oe.getComponent();
        let pe, Oe = !1;
        if (ie) {
          ie.p != null && (B.write("d", ie.p), z[ie.p] = oe.clone()), ie.r !== void 0 && B.write("i", ie.r), ie.d != null && (B.write("p", ie.d), ee = void 0), ie.i !== void 0 && (ee = pe = ie.i);
          const G = de(ie);
          G && (ee === void 0 ? (K || (K = /* @__PURE__ */ new Set()), K.add(ie)) : (T(ie), ee = G.apply(ee, T(ie)), Oe = !0));
        }
        let Me = 0;
        for (const G of oe) {
          B.descend(G);
          const Re = typeof G == "number" ? G - Me : G, He = R(ee, Re);
          h(oe.getComponent()) && Me++;
          const Be = ue(oe, B, He);
          if (ee !== void 0 && Be !== void 0) {
            if (Oe || (Oe = !0, ee = c(ee)), !E(ee, Re)) throw Error("Cannot modify child - invalid operation");
            ee[Re] = Be;
          }
          B.ascend();
        }
        if (pe === void 0) return Oe ? ee : void 0;
        B.write("r", ee);
      }(F, V, void 0), K && (V.reset(), function ue(oe, B, ee) {
        const ie = B.getComponent();
        if (ie) {
          const G = ie.d;
          if (G != null && (oe = z[G], ee = W[G] = s.writeCursor()), K.has(ie)) {
            const Re = de(ie);
            if (!Re.invert) throw Error(`Cannot invert subtype ${Re.name}`);
            A(ee, Re, Re.invert(T(ie)));
          }
        }
        let pe = 0, Oe = 0;
        const Me = s.advancer(oe, (G, Re) => l(Re) ? pe - G - 1 : G - pe, (G, Re) => {
          l(Re) && pe++;
        });
        for (const G of B) if (typeof G == "number") {
          const Re = G - Oe, He = Me(Re), Be = Re + pe;
          ee.descend(Be), ue(He, B, ee), h(B.getComponent()) && Oe++, ee.ascend();
        } else ee.descend(G), ue(Me(G), B, ee), ee.ascend();
        Me.end();
      }(F.clone(), F, V), W.length && (V.reset(), F.traverse(V, (ue, oe) => {
        const B = ue.p;
        if (B != null) {
          const ee = W[B];
          ee && ee.get(), ee && oe.mergeTree(ee.get());
        }
      }))), V.get();
    }
    const b = (v, F) => v.some((V) => typeof V == "object" && (Array.isArray(V) ? b(V, F) : F(V)));
    function w(v, F) {
      if (v == null || !b(v, (B) => {
        var ee;
        return B.r !== void 0 || ((ee = de(B)) === null || ee === void 0 ? void 0 : ee.makeInvertible) != null;
      })) return v;
      const V = new s.ReadCursor(v), K = new s.WriteCursor();
      let z = !1;
      const W = [], ue = [], oe = (B, ee, ie) => {
        const pe = B.getComponent();
        let Oe = !1;
        if (pe) {
          pe.d != null && ee.write("d", pe.d), pe.i !== void 0 && ee.write("i", pe.i);
          const G = pe.p;
          if (G != null && (W[G] = B.clone(), o(ie !== void 0, "Operation picks up at an invalid key"), ue[G] = ie, ee.write("p", pe.p)), pe.r !== void 0 && ie === void 0) throw Error("Invalid doc / op in makeInvertible: removed item missing from doc");
          const Re = de(pe);
          Re && (Re.makeInvertible ? z = !0 : A(ee, Re, T(pe), !0));
        }
        let Me = 0;
        for (const G of B) {
          ee.descend(G);
          const Re = typeof G == "number" ? G - Me : G, He = R(ie, Re), Be = oe(B, ee, He);
          He !== Be && (Oe || (Oe = !0, ie = c(ie)), Be === void 0 ? (ie = d(ie, Re), typeof G == "number" && Me++) : ie[Re] = Be), ee.ascend();
        }
        return pe && (pe.r !== void 0 ? (ee.write("r", r.default(ie)), ie = void 0) : pe.p != null && (ie = void 0)), ie;
      };
      return oe(V, K, F), K.get(), z && (K.reset(), function B(ee, ie, pe, Oe, Me) {
        const G = ie.getComponent();
        if (G) {
          G.i !== void 0 ? (Oe = G.i, Me = !0) : G.d != null && (Oe = ue[G.d], ee = W[G.d], Me = !1, G.d);
          let xe = de(G);
          if (xe && xe.makeInvertible) {
            const Je = T(G);
            A(pe, xe, xe.makeInvertible(Je, Oe), !0);
          }
        }
        let Re = 0, He = 0;
        const Be = s.advancer(ee, (xe, Je) => l(Je) ? Re - xe - 1 : xe - Re, (xe, Je) => {
          l(Je) && Re++;
        });
        for (const xe of ie) if (typeof xe == "number") {
          const Je = xe - He, Rt = Be(Je), We = Je + Re, et = R(Oe, Me ? Je : We);
          pe.descend(xe), B(Rt, ie, pe, et, Me), h(ie.getComponent()) && He++, pe.ascend();
        } else {
          const Je = R(Oe, xe);
          pe.descend(xe), B(Be(xe), ie, pe, Je, Me), pe.ascend();
        }
        Be.end();
      }(V.clone(), V, K, F, !1)), K.get();
    }
    function k(v, F) {
      return M(w(v, F));
    }
    const $ = (v) => {
      if (v == null) return null;
      const F = v.slice();
      for (let V = 0; V < v.length; V++) {
        const K = F[V];
        Array.isArray(K) && (F[V] = $(K));
      }
      return F;
    };
    function Y(v, F, V) {
      o(V === "left" || V === "right", "Direction must be left or right");
      const K = V === "left" ? 0 : 1;
      if (F == null) return {
        ok: !0,
        result: v
      };
      fe(v), fe(F);
      let z = null;
      const W = [], ue = [], oe = [], B = [], ee = [], ie = [], pe = [], Oe = [], Me = [], G = [], Re = [], He = [], Be = [], xe = [], Je = [];
      let Rt = 0;
      const We = s.readCursor(v), et = s.readCursor(F), ze = s.writeCursor();
      if (function g(p, S = null, N) {
        const L = a(S);
        L && (L.r !== void 0 ? N = S.clone() : L.p != null && (N = null, ie[L.p] = p.clone()));
        const x = p.getComponent();
        let P;
        x && (P = x.p) != null && (ee[P] = S ? S.clone() : null, oe[P] = p.clone(), N && (G[P] = !0, Me[P] = N), L && L.p != null && (xe[P] = L.p));
        const I = s.advancer(S);
        for (const Q of p) g(p, I(Q), N);
        I.end();
      }(et, We, null), function g(p, S, N, L, x) {
        const P = N.getComponent();
        let I, Q = !1;
        P && ((I = P.d) != null ? (B[I] = N.clone(), L != null && (Je[L] == null && (Je[L] = []), Je[L].push(I)), G[I], p = ee[I] || null, S = oe[I] || null, G[I] ? (x && (Re[I] = !0), x = Me[I] || null) : !x || K !== 1 && xe[I] != null || z == null && (z = {
          type: i.ConflictType.RM_UNEXPECTED_CONTENT,
          op1: t.removeOp(x.getPath()),
          op2: t.moveOp(S.getPath(), N.getPath())
        }), Q = !0) : P.i !== void 0 && (p = S = null, Q = !0, x && z == null && (z = {
          type: i.ConflictType.RM_UNEXPECTED_CONTENT,
          op1: t.removeOp(x.getPath()),
          op2: t.insertOp(N.getPath(), P.i)
        })));
        const _e = a(p);
        _e && (_e.r !== void 0 ? x = p.clone() : _e.p != null && (_e.p, L = _e.p, x = null));
        const J = de(P);
        J && x && z == null && (z = {
          type: i.ConflictType.RM_UNEXPECTED_CONTENT,
          op1: t.removeOp(x.getPath()),
          op2: t.editOp(N.getPath(), J, T(P), !0)
        });
        let me = 0, ye = 0;
        const le = s.advancer(S, (q, Ce) => l(Ce) ? me - q - 1 : q - me, (q, Ce) => {
          l(Ce) && me++;
        }), D = s.advancer(p);
        for (const q of N) if (typeof q == "number") {
          const Ce = q - ye, Se = le(Ce);
          ye += +g(D(Ce + me), Se, N, L, x);
        } else {
          const Ce = le(q);
          g(D(q), Ce, N, L, x);
        }
        return le.end(), D.end(), Q;
      }(We, et, et.clone(), null, null), B.map((g) => g && g.get()), z) return {
        ok: !1,
        conflict: z
      };
      Re.map((g) => !!g);
      const ct = [];
      let it = null;
      (function g(p, S, N, L, x) {
        let P = !1;
        const I = a(S);
        if (l(I)) {
          const le = I.p;
          le != null ? (N = B[le], L = He[le] = s.writeCursor(), P = !0, x = null) : (N = null, x = S.clone());
        } else h(a(N)) && (N = null);
        const Q = p.getComponent();
        if (Q) {
          const le = Q.p;
          le != null ? (x && (Oe[le] = x), ct[le] = x || K === 1 && P ? null : L.getComponent(), W[le] = p.clone(), N && (pe[le] = N.clone())) : Q.r !== void 0 && (x || L.write("r", !0), (x || P) && (it == null && (it = /* @__PURE__ */ new Set()), it.add(Q)));
        }
        let _e = 0, J = 0;
        const me = s.advancer(S, void 0, (le, D) => {
          l(D) && _e++;
        }), ye = s.advancer(N, (le, D) => h(D) ? ~(le - J) : le - J, (le, D) => {
          h(D) && J++;
        });
        if (p) for (const le of p) if (typeof le == "string") {
          const D = me(le), q = ye(le);
          L.descend(le), g(p, D, q, L, x), L.ascend();
        } else {
          const D = me(le), q = le - _e, Ce = l(a(D)) ? null : ye(q), Se = q + J;
          o(Se >= 0), L.descend(Se), g(p, D, Ce, L, x), L.ascend();
        }
        me.end(), ye.end();
      })(We, et, et.clone(), ze, null), ze.reset();
      let xt = [];
      if (function g(p, S, N, L, x, P) {
        o(S);
        const I = S.getComponent();
        let Q = a(L), _e = !1;
        const J = (ve, Ie, Ne) => ve ? t.moveOp(ve.getPath(), Ie.getPath()) : t.insertOp(Ie.getPath(), Ne.i);
        if (h(I)) {
          const ve = I.d;
          ve != null && (ue[ve] = S.clone());
          const Ie = ve != null ? ct[ve] : null;
          let Ne = !1;
          if (I.i !== void 0 || ve != null && Ie) {
            let te;
            Q && (Q.i !== void 0 || (te = Q.d) != null && !G[te]) && (Ne = te != null ? ve != null && ve === xe[te] : n.default(Q.i, I.i), Ne || te != null && K !== 1 && xe[te] != null || z == null && (z = {
              type: i.ConflictType.DROP_COLLISION,
              op1: J(ve != null ? W[ve] : null, S, I),
              op2: J(te != null ? oe[te] : null, L, Q)
            })), Ne || (P ? z == null && (z = {
              type: i.ConflictType.RM_UNEXPECTED_CONTENT,
              op1: J(ve != null ? W[ve] : null, S, I),
              op2: t.removeOp(P.getPath())
            }) : (ve != null ? (xt[Rt] = ve, x.write("d", Ie.p = Rt++)) : x.write("i", r.default(I.i)), _e = !0));
          } else if (ve != null && !Ie) {
            const te = Oe[ve];
            te && (P = te.clone());
          }
          ve != null ? (p = W[ve], N = ie[ve], L = pe[ve]) : I.i !== void 0 && (p = N = null, Ne || (L = null));
        } else l(a(p)) && (p = N = L = null);
        const me = a(p), ye = a(N);
        if (l(ye)) {
          const ve = ye.p;
          ye.r !== void 0 && (!me || me.r === void 0) || G[ve] ? (L = null, P = N.clone()) : ve != null && (L = B[ve], K !== 1 && xe[ve] != null || ((x = Be[ve]) || (x = Be[ve] = s.writeCursor()), x.reset(), P = null));
        } else !h(I) && h(Q) && (L = null);
        Q = L != null ? L.getComponent() : null;
        const le = de(I);
        if (le) {
          const ve = T(I);
          if (P) z == null && (z = {
            type: i.ConflictType.RM_UNEXPECTED_CONTENT,
            op1: t.editOp(S.getPath(), le, ve, !0),
            op2: t.removeOp(P.getPath())
          });
          else {
            const Ie = de(Q);
            let Ne;
            if (Ie) {
              if (le !== Ie) throw Error("Transforming incompatible types");
              const te = T(Q);
              Ne = le.transform(ve, te, V);
            } else Ne = r.default(ve);
            A(x, le, Ne);
          }
        }
        let D = 0, q = 0, Ce = 0, Se = 0, Le = 0, Ue = 0, je = p != null && p.descendFirst(), dt = je;
        const pt = s.advancer(N, void 0, (ve, Ie) => {
          l(Ie) && Ce++;
        });
        let Ee = L != null && L.descendFirst(), qe = Ee;
        for (const ve of S) if (typeof ve == "number") {
          let Ie;
          const Ne = h(S.getComponent()), te = ve - q;
          {
            let zt;
            for (; je && typeof (zt = p.getKey()) == "number"; ) {
              zt += D;
              const bt = p.getComponent(), Cn = l(bt);
              if (zt > te || zt === te && (!Cn || K === 0 && Ne)) break;
              if (Cn) {
                D--;
                const sn = bt.p;
                xe.includes(sn), bt.d, a(Be[bt.d]), l(a(Be[bt.d])), (bt.r === void 0 || it && it.has(bt)) && (sn == null || !ct[sn] || K !== 1 && xe.includes(sn)) || Le--;
              }
              je = p.nextSibling();
            }
            Ie = je && zt === te ? p : null;
          }
          const ut = te - D;
          let $e = pt(ut);
          const At = ut - Ce;
          let dr = null;
          {
            let zt, bt;
            for (; Ee && typeof (zt = L.getKey()) == "number"; ) {
              bt = zt - Se;
              const Cn = L.getComponent(), sn = h(Cn);
              if (bt > At) break;
              if (bt === At) {
                if (!sn) {
                  dr = L;
                  break;
                }
                {
                  if (K === 0 && Ne) {
                    dr = L;
                    break;
                  }
                  const Yt = $e && l($e.getComponent());
                  if (K === 0 && Yt) break;
                }
              }
              if (sn) {
                const Yt = Cn.d;
                G[Yt], xe[Yt], Cn.i === void 0 && (G[Yt] || xe[Yt] != null && K !== 1) ? (G[Yt] || xe[Yt] != null && K === 0) && (Se++, Ue--) : Se++;
              }
              Ee = L.nextSibling();
            }
          }
          const Hi = At + Se + Le + Ue;
          o(Hi >= 0, "trying to descend to a negative index"), x.descend(Hi), Ne && (Ie = $e = dr = null, q++), g(Ie, S, $e, dr, x, P) && Ue++, x.ascend();
        } else {
          let Ie;
          for (; je && (Ie = p.getKey(), typeof Ie != "string" || !(Ie > ve || Ie === ve)); ) je = p.nextSibling();
          const Ne = je && Ie === ve ? p : null, te = pt(ve);
          let ut;
          for (; Ee && (ut = L.getKey(), typeof ut != "string" || !(ut > ve || ut === ve)); ) Ee = L.nextSibling();
          const $e = Ee && ut === ve ? L : null;
          x.descend(ve), g(Ne, S, te, $e, x, P), x.ascend();
        }
        return pt.end(), dt && p.ascend(), qe && L.ascend(), _e;
      }(We, We.clone(), et, et.clone(), ze, null), z) return {
        ok: !1,
        conflict: z
      };
      ze.reset();
      const ke = (g, p, S) => g.traverse(p, (N, L) => {
        N.d != null && S(N.d, g, L);
      });
      (G.length || He.length) && (ke(et, ze, (g, p, S) => {
        G[g] && !Re[g] && S.write("r", !0), He[g] && S.mergeTree(He[g].get());
      }), ze.reset());
      const ht = [], _ = [];
      if ((Be.length || G.length) && !z) {
        const g = s.readCursor($(ze.get()));
        if (ke(g, null, (p, S) => {
          ht[p] = S.clone();
        }), Be.forEach((p) => {
          p && ke(s.readCursor(p.get()), null, (S, N) => {
            ht[S] = N.clone();
          });
        }), function p(S, N, L, x, P, I) {
          const Q = a(N);
          if (Q && l(Q)) if (Q.p != null) {
            const D = Q.p;
            ht[D].getPath(), L = ht[D], x = _[D] = s.writeCursor();
          } else Q.r !== void 0 && (L = null);
          else h(a(L)) && (L = null);
          const _e = S.getComponent();
          if (_e) {
            let D;
            if ((D = _e.d) != null) {
              const q = Be[D];
              q && (q.get(), x.mergeTree(q.get()), L = s.readCursor(q.get()));
            }
          }
          let J = 0, me = 0;
          const ye = s.advancer(N, void 0, (D, q) => {
            l(q) && J--;
          }), le = s.advancer(L, (D, q) => h(q) ? -(D - me) - 1 : D - me, (D, q) => {
            h(q) && me++;
          });
          for (const D of S) if (typeof D == "number") {
            const q = ye(D), Ce = D + J, Se = le(Ce), Le = Ce + me;
            x.descend(Le), p(S, q, Se, x), x.ascend();
          } else x.descend(D), p(S, ye(D), le(D), x), x.ascend();
          ye.end(), le.end();
        }(et, g, g.clone(), ze), ze.reset(), z) return {
          ok: !1,
          conflict: z
        };
        if (ze.get(), _.length) {
          const p = _.map((N) => N ? N.get() : null), S = s.readCursor($(ze.get()));
          if (ke(S, ze, (N, L, x) => {
            const P = p[N];
            P && (x.mergeTree(P), p[N] = null);
          }), p.find((N) => N)) {
            const N = s.writeCursor(), L = s.writeCursor();
            let x = 0, P = 0;
            p.forEach((I) => {
              I != null && ke(s.readCursor(I), null, (Q) => {
                const _e = xt[Q];
                N.writeMove(W[_e].getPath(), ue[_e].getPath(), x++);
                const J = Je[_e];
                J && J.forEach((me) => {
                  G[me] || K !== 1 && xe[me] != null || L.writeMove(oe[me].getPath(), B[me].getPath(), P++);
                });
              });
            }), z = {
              type: i.ConflictType.BLACKHOLE,
              op1: N.get(),
              op2: L.get()
            };
          }
        }
      }
      return z ? {
        ok: !1,
        conflict: z
      } : {
        ok: !0,
        result: ze.get()
      };
    }
    const se = (v) => {
      const F = new Error("Transform detected write conflict");
      throw F.conflict = v, F.type = F.name = "writeConflict", F;
    };
    function he(v, F, V) {
      const K = Y(v, F, V);
      if (K.ok) return K.result;
      se(K.conflict);
    }
    const ge = (v) => {
      const F = s.writeCursor();
      return s.readCursor(v).traverse(F, (V, K) => {
        (h(V) || de(V)) && K.write("r", !0);
      }), F.get();
    }, Ae = (v, F) => {
      const { type: V, op1: K, op2: z } = v;
      switch (V) {
        case i.ConflictType.DROP_COLLISION:
          return F === "left" ? [null, ge(z)] : [ge(K), null];
        case i.ConflictType.RM_UNEXPECTED_CONTENT:
          let W = !1;
          return s.readCursor(K).traverse(null, (ue) => {
            ue.r !== void 0 && (W = !0);
          }), W ? [null, ge(z)] : [ge(K), null];
        case i.ConflictType.BLACKHOLE:
          return [ge(K), ge(z)];
        default:
          throw Error("Unrecognised conflict: " + V);
      }
    };
    function be(v, F, V, K) {
      let z = null;
      for (; ; ) {
        const W = Y(F, V, K);
        if (W.ok) return y(z, W.result);
        {
          const { conflict: ue } = W;
          v(ue) || se(ue);
          const [oe, B] = Ae(ue, K);
          F = y(ae(F), oe), V = y(ae(V), B), z = y(z, B);
        }
      }
    }
  }(Ir)), Ir;
}
var ua;
function ym() {
  return ua || (ua = 1, function(t) {
    var e = $n.__createBinding || (Object.create ? function(i, o, a, u) {
      u === void 0 && (u = a), Object.defineProperty(i, u, { enumerable: !0, get: function() {
        return o[a];
      } });
    } : function(i, o, a, u) {
      u === void 0 && (u = a), i[u] = o[a];
    }), n = $n.__exportStar || function(i, o) {
      for (var a in i) a !== "default" && !o.hasOwnProperty(a) && e(o, i, a);
    };
    Object.defineProperty(t, "__esModule", { value: !0 }), n(vm(), t);
    var r = $u();
    Object.defineProperty(t, "ReadCursor", { enumerable: !0, get: function() {
      return r.ReadCursor;
    } }), Object.defineProperty(t, "WriteCursor", { enumerable: !0, get: function() {
      return r.WriteCursor;
    } });
    var s = Bu();
    Object.defineProperty(t, "ConflictType", { enumerable: !0, get: function() {
      return s.ConflictType;
    } });
  }($n)), $n;
}
var mt = ym();
const wm = /* @__PURE__ */ wt(mt), JC = /* @__PURE__ */ jl({
  __proto__: null,
  default: wm
}, [mt]);
var ce = /* @__PURE__ */ ((t) => (t.RETAIN = "r", t.INSERT = "i", t.DELETE = "d", t))(ce || {});
function _s(t, e = !1) {
  const n = [];
  for (const r of t) {
    const { st: s, ed: i, ts: o } = r;
    if (r.sId === void 0 && delete r.sId, s === i || !e && re.isEmptyObject(o) && r.sId == null)
      continue;
    if (n.length === 0) {
      n.push(r);
      continue;
    }
    const a = n.pop();
    Mg(r, a) && re.hasIntersectionBetweenTwoRanges(a.st, a.ed, r.st, r.ed) ? n.push({
      ...r,
      st: a.st,
      ed: i
    }) : n.push(a, r);
  }
  return n;
}
function ju(t, e, n, r) {
  var c;
  const { textRuns: s } = t;
  if (s == null)
    return;
  const i = [], o = s.length;
  let a = !1;
  const u = (c = e.textRuns) != null ? c : [];
  if (u.length)
    for (const l of u)
      l.st += r, l.ed += r;
  for (let l = 0; l < o; l++) {
    const h = s[l], { st: d, ed: f } = h;
    if (f <= r)
      i.push(h);
    else if (r > d && r < f) {
      a = !0;
      const E = {
        ...h,
        ed: r
      };
      i.push(E), u.length && i.push(...u);
      const R = {
        ...h,
        st: r + n,
        ed: f + n
      };
      i.push(R);
    } else
      h.st += n, h.ed += n, a || (a = !0, i.push(...u)), i.push(h);
  }
  a || (a = !0, i.push(...u)), t.textRuns = _s(i);
}
function Hu(t, e, n, r) {
  const { paragraphs: s } = t;
  if (s == null)
    return;
  const { paragraphs: i } = e, o = [];
  for (let u = 0, c = s.length; u < c; u++) {
    const l = s[u], { startIndex: h } = l;
    h >= r && (l.startIndex += n), o.push(l.startIndex);
  }
  let a = -1;
  if (i) {
    for (let u = 0, c = i.length; u < c; u++) {
      const l = i[u];
      l.startIndex += r;
      const h = l.startIndex;
      a = o.indexOf(h);
    }
    a !== -1 && s.splice(a, 1), s.push(...i), s.sort(ps("startIndex"));
  }
}
function Wu(t, e, n, r) {
  const { sectionBreaks: s } = t;
  if (s == null)
    return;
  for (let o = 0, a = s.length; o < a; o++) {
    const u = s[o], { startIndex: c } = u;
    c >= r && (u.startIndex += n);
  }
  const i = e.sectionBreaks;
  if (i) {
    for (let o = 0, a = i.length; o < a; o++) {
      const u = i[o];
      u.startIndex += r;
    }
    s.push(...i), s.sort(ps("startIndex"));
  }
}
function zu(t, e, n, r) {
  const { customBlocks: s = [] } = t;
  for (let o = 0, a = s.length; o < a; o++) {
    const u = s[o], { startIndex: c } = u;
    c >= r && (u.startIndex += n);
  }
  const i = e.customBlocks;
  if (i) {
    for (let o = 0, a = i.length; o < a; o++) {
      const u = i[o];
      u.startIndex += r;
    }
    s.push(...i), s.sort(ps("startIndex"));
  }
  s.length && !t.customBlocks && (t.customBlocks = s);
}
function Yu(t, e, n, r) {
  const { tables: s } = t;
  if (s == null)
    return;
  for (let o = 0, a = s.length; o < a; o++) {
    const u = s[o], { startIndex: c, endIndex: l } = u;
    c > r ? (u.startIndex += n, u.endIndex += n) : l > r && (u.endIndex += n);
  }
  const i = e.tables;
  if (i) {
    for (let o = 0, a = i.length; o < a; o++) {
      const u = i[o];
      u.startIndex += r, u.endIndex += r;
    }
    s.push(...i), s.sort(ps("startIndex"));
  }
}
const Vu = "$", la = (t) => t.split(Vu)[0];
function ki(t) {
  if (t.length <= 1) return t;
  t.sort((s, i) => s.startIndex - i.startIndex);
  const e = [];
  let n = { ...t[0] };
  n.rangeId = la(n.rangeId);
  for (let s = 1; s < t.length; s++) {
    const i = t[s];
    i.rangeId = la(i.rangeId), i.rangeId === n.rangeId && Df(n.properties, i.properties) && n.endIndex + 1 >= i.startIndex ? n.endIndex = i.endIndex : (e.push(n), n = { ...i });
  }
  e.push(n);
  const r = /* @__PURE__ */ Object.create(null);
  for (let s = 0, i = e.length; s < i; s++) {
    const o = e[s], a = o.rangeId;
    r[a] ? (o.rangeId = `${a}${Vu}${r[a]}`, r[a] = r[a] + 1) : r[a] = 1;
  }
  return e;
}
function Qs(t, e) {
  const n = t.findIndex((s) => s.startIndex < e && s.endIndex >= e), r = t[n];
  r && t.splice(
    n,
    1,
    {
      rangeId: r.rangeId,
      rangeType: r.rangeType,
      startIndex: r.startIndex,
      endIndex: e - 1,
      properties: { ...r.properties }
    },
    {
      rangeId: r.rangeId,
      rangeType: r.rangeType,
      startIndex: e,
      endIndex: r.endIndex,
      properties: { ...r.properties }
    }
  );
}
function Gu(t) {
  if (t.length <= 1) return t;
  t.sort((r, s) => r.startIndex - s.startIndex);
  const e = [];
  let n = { ...t[0] };
  for (let r = 1; r < t.length; r++) {
    const s = t[r];
    s.id === n.id && n.endIndex + 1 >= s.startIndex ? n.endIndex = s.endIndex : (e.push(n), n = { ...s });
  }
  return e.push(n), e;
}
function qs(t, e) {
  t.filter((r) => r.startIndex < e && r.endIndex >= e).forEach((r) => {
    const s = t.indexOf(r);
    t.splice(
      s,
      1,
      {
        id: r.id,
        type: r.type,
        startIndex: r.startIndex,
        endIndex: e - 1
      },
      {
        id: r.id,
        type: r.type,
        startIndex: e,
        endIndex: r.endIndex
      }
    );
  });
}
function Om(t, e, n, r) {
  t.customRanges || (t.customRanges = []);
  const { customRanges: s } = t;
  Qs(s, r);
  for (let o = 0, a = s.length; o < a; o++) {
    const u = s[o], { startIndex: c } = u;
    c >= r && (u.startIndex += n, u.endIndex += n);
  }
  const i = [];
  if (e.customRanges) {
    for (let o = 0, a = e.customRanges.length; o < a; o++) {
      const u = e.customRanges[o];
      u.startIndex += r, u.endIndex += r, i.push(u);
    }
    s.push(...i);
  }
  t.customRanges = ki(s);
}
function bm(t, e, n, r) {
  t.customDecorations || (t.customDecorations = []);
  const { customDecorations: s } = t;
  qs(s, r);
  for (let o = 0, a = s.length; o < a; o++) {
    const u = s[o], { startIndex: c } = u;
    c >= r && (u.startIndex += n, u.endIndex += n);
  }
  const i = [];
  if (e.customDecorations) {
    for (let o = 0, a = e.customDecorations.length; o < a; o++) {
      const u = e.customDecorations[o];
      u.startIndex += r, u.endIndex += r, i.push(u);
    }
    s.push(...i);
  }
  t.customDecorations = Gu(s);
}
function Ku(t, e, n) {
  const { textRuns: r } = t, s = n, i = n + e, o = [];
  if (r) {
    const a = [];
    for (let u = 0, c = r.length; u < c; u++) {
      const l = r[u], { st: h, ed: d } = l;
      if (s <= h && i >= d) {
        o.push({
          ...l,
          st: h - s,
          ed: d - s
        });
        continue;
      } else h <= s && d >= i ? (o.push({
        ...l,
        st: s - s,
        ed: i - s
      }), l.ed -= e) : s >= h && s < d ? (o.push({
        ...l,
        st: s - s,
        ed: d - s
      }), l.ed = s) : i > h && i <= d ? (o.push({
        ...l,
        st: h - s,
        ed: i - s
      }), l.st = i - e, l.ed -= e) : h >= i && (l.st -= e, l.ed -= e);
      a.push(l);
    }
    t.textRuns = a;
  }
  return o.length === 0 && o.push({
    st: 0,
    ed: e,
    ts: {}
  }), o;
}
function Xu(t, e, n) {
  const { paragraphs: r } = t, s = n, i = n + e, o = [];
  if (r) {
    const a = [];
    for (let u = 0, c = r.length; u < c; u++) {
      const l = r[u], { startIndex: h } = l;
      if (h >= s && h < i) {
        o.push({
          ...l,
          startIndex: h - n
        });
        continue;
      } else h >= i && (l.startIndex -= e);
      a.push(l);
    }
    t.paragraphs = a;
  }
  return o;
}
function Ju(t, e, n) {
  const { sectionBreaks: r } = t, s = n, i = n + e - 1, o = [];
  if (r) {
    const a = [];
    for (let u = 0, c = r.length; u < c; u++) {
      const l = r[u], { startIndex: h } = l;
      if (h >= s && h <= i) {
        o.push({
          ...l,
          startIndex: h - n
        });
        continue;
      } else h > i && (l.startIndex -= e);
      a.push(l);
    }
    t.sectionBreaks = a;
  }
  return o;
}
function Zu(t, e, n) {
  const { customBlocks: r = [] } = t, s = n, i = n + e - 1, o = [];
  if (r) {
    const a = [];
    for (let u = 0, c = r.length; u < c; u++) {
      const l = r[u], { startIndex: h } = l;
      if (h >= s && h <= i) {
        o.push({
          ...l,
          startIndex: h - n
        });
        continue;
      } else h > i && (l.startIndex -= e);
      a.push(l);
    }
    t.customBlocks = a;
  }
  return r.length && !t.customBlocks && (t.customBlocks = r), o;
}
function Qu(t, e, n) {
  const { tables: r } = t, s = n, i = n + e - 1, o = [];
  if (r) {
    const a = [];
    for (let u = 0, c = r.length; u < c; u++) {
      const l = r[u], { startIndex: h, endIndex: d } = l;
      if (s <= h && i >= d) {
        o.push({
          ...l,
          startIndex: h - n,
          endIndex: d - n
        });
        continue;
      } else if (h <= s && d >= i) {
        const f = Li(h, d, s, i);
        if (f.length === 0 || (l.startIndex = f[0], l.endIndex = f[1], l.startIndex === l.endIndex))
          continue;
      } else i < h && (l.startIndex -= e, l.endIndex -= e);
      a.push(l);
    }
    t.tables = a;
  }
  return o;
}
function Sm(t, e, n) {
  const { customRanges: r } = t, s = n, i = n + e - 1, o = [];
  if (r) {
    const a = [];
    for (let u = 0, c = r.length; u < c; u++) {
      const l = r[u], { startIndex: h, endIndex: d } = l;
      if (h >= s && d <= i) {
        o.push(l);
        continue;
      } else if (Math.max(s, h) <= Math.min(i, d)) {
        const f = Li(h, d, s, i);
        if (f.length === 0)
          continue;
        l.startIndex = f[0], l.endIndex = f[1];
      } else i < h && (l.startIndex -= e, l.endIndex -= e);
      a.push(l);
    }
    t.customRanges = ki(a);
  }
  return o;
}
function Am(t, e, n, r = !0) {
  const { customDecorations: s } = t, i = n, o = n + e - 1, a = [];
  if (s) {
    const u = [];
    for (let c = 0, l = s.length; c < l; c++) {
      const h = s[c], { startIndex: d, endIndex: f } = h;
      if (d >= i && f <= o) {
        a.push(h);
        continue;
      } else if (Math.max(i, d) <= Math.min(o, f)) {
        const E = Li(d, f, i, o);
        if (E.length === 0)
          continue;
        h.startIndex = E[0], h.endIndex = E[1];
      } else o < d && r && (h.startIndex -= e, h.endIndex -= e);
      u.push(h);
    }
    t.customDecorations = u;
  }
  return a;
}
var Nm = /* @__PURE__ */ ((t) => (t.ORDER_LIST_QUICK_1 = "1.", t.ORDER_LIST_QUICK_2 = "a)", t.ORDER_LIST_QUICK_3 = "a.", t.ORDER_LIST_QUICK_4 = "i.", t.ORDER_LIST_QUICK_5 = "A.", t.ORDER_LIST_QUICK_6 = "I.", t.ORDER_LIST_QUICK_7 = "01.", t))(Nm || {}), Ft = /* @__PURE__ */ ((t) => (t.BULLET_LIST = "BULLET_LIST", t.BULLET_LIST_1 = "BULLET_LIST_1", t.BULLET_LIST_2 = "BULLET_LIST_2", t.BULLET_LIST_3 = "BULLET_LIST_3", t.BULLET_LIST_4 = "BULLET_LIST_4", t.BULLET_LIST_5 = "BULLET_LIST_5", t.ORDER_LIST = "ORDER_LIST", t.ORDER_LIST_1 = "ORDER_LIST_1", t.ORDER_LIST_2 = "ORDER_LIST_2", t.ORDER_LIST_3 = "ORDER_LIST_3", t.ORDER_LIST_4 = "ORDER_LIST_4", t.ORDER_LIST_5 = "ORDER_LIST_5", t.ORDER_LIST_QUICK_2 = "ORDER_LIST_QUICK_2", t.ORDER_LIST_QUICK_3 = "ORDER_LIST_QUICK_3", t.ORDER_LIST_QUICK_4 = "ORDER_LIST_QUICK_4", t.ORDER_LIST_QUICK_5 = "ORDER_LIST_QUICK_5", t.ORDER_LIST_QUICK_6 = "ORDER_LIST_QUICK_6", t.CHECK_LIST = "CHECK_LIST", t.CHECK_LIST_CHECKED = "CHECK_LIST_CHECKED", t))(Ft || {});
const Or = {
  "a)": { glyphFormat: "%1)", glyphType: Te.DECIMAL },
  "1.": { glyphFormat: "%1.", glyphType: Te.DECIMAL },
  "a.": { glyphFormat: "%1.", glyphType: Te.LOWER_LETTER },
  "A.": { glyphFormat: "%1.", glyphType: Te.UPPER_LETTER },
  "i.": { glyphFormat: "%1.", glyphType: Te.LOWER_ROMAN },
  "I.": { glyphFormat: "%1.", glyphType: Te.UPPER_LETTER }
}, Rn = (t) => [
  ...t,
  ...t,
  ...t
].map((e, n) => ({
  glyphFormat: ` %${n + 1}`,
  glyphSymbol: e,
  bulletAlignment: ms.START,
  textStyle: {
    fs: 12
  },
  startNumber: 0,
  paragraphProperties: {
    hanging: { v: 21 },
    indentStart: { v: 21 * n }
  }
})), In = (t) => t.map((e, n) => ({
  ...e,
  bulletAlignment: ms.START,
  textStyle: {
    fs: 12
  },
  startNumber: 0,
  paragraphProperties: {
    hanging: { v: 21 },
    indentStart: { v: 21 * n }
  }
})), ca = (t, e) => new Array(9).fill(0).map((n, r) => ({
  glyphFormat: ` %${r + 1}`,
  glyphSymbol: t,
  bulletAlignment: ms.START,
  textStyle: {
    fs: 16
  },
  startNumber: 0,
  paragraphProperties: {
    hanging: { v: 21 },
    indentStart: { v: 21 * r },
    textStyle: e
  }
})), Es = {
  BULLET_LIST: {
    listType: "BULLET_LIST",
    nestingLevel: Rn(["●", "○", "■"])
  },
  BULLET_LIST_1: {
    listType: "BULLET_LIST",
    nestingLevel: Rn(["❖", "➢", "■"])
  },
  BULLET_LIST_2: {
    listType: "BULLET_LIST",
    nestingLevel: Rn(["✔", "●", "◆"])
  },
  BULLET_LIST_3: {
    listType: "BULLET_LIST",
    nestingLevel: Rn(["■", "◆", "○"])
  },
  BULLET_LIST_4: {
    listType: "BULLET_LIST",
    nestingLevel: Rn(["✧", "○", "■"])
  },
  BULLET_LIST_5: {
    listType: "BULLET_LIST",
    nestingLevel: Rn(["➢", "○", "◆"])
  },
  ORDER_LIST: {
    listType: "ORDER_LIST",
    nestingLevel: In([
      { glyphFormat: "%1.", glyphType: Te.DECIMAL },
      { glyphFormat: "%2.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%3.", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%4.", glyphType: Te.DECIMAL },
      { glyphFormat: "%5.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%6.", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%7.", glyphType: Te.DECIMAL },
      { glyphFormat: "%8.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%9.", glyphType: Te.LOWER_ROMAN }
    ])
  },
  ORDER_LIST_1: {
    listType: "ORDER_LIST",
    nestingLevel: In([
      { glyphFormat: "%1)", glyphType: Te.DECIMAL },
      { glyphFormat: "%2)", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%3)", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%4)", glyphType: Te.DECIMAL },
      { glyphFormat: "%5)", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%6)", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%7)", glyphType: Te.DECIMAL },
      { glyphFormat: "%8)", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%9)", glyphType: Te.LOWER_ROMAN }
    ])
  },
  ORDER_LIST_2: {
    listType: "ORDER_LIST",
    nestingLevel: In([
      "%1.",
      "%1.%2.",
      "%1.%2.%3.",
      "%1.%2.%3.%4.",
      "%1.%2.%3.%4.%5.",
      "%1.%2.%3.%4.%5.%6.",
      "%1.%2.%3.%4.%5.%6.%7."
    ].map((t) => ({ glyphFormat: t, glyphType: Te.DECIMAL })))
  },
  ORDER_LIST_3: {
    listType: "ORDER_LIST",
    nestingLevel: In([
      { glyphFormat: "%1.", glyphType: Te.UPPER_LETTER },
      { glyphFormat: "%2.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%3.", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%4.", glyphType: Te.UPPER_LETTER },
      { glyphFormat: "%5.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%6.", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%7.", glyphType: Te.UPPER_LETTER },
      { glyphFormat: "%8.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%9.", glyphType: Te.LOWER_ROMAN }
    ])
  },
  ORDER_LIST_4: {
    listType: "ORDER_LIST",
    nestingLevel: In([
      { glyphFormat: "%1.", glyphType: Te.UPPER_LETTER },
      { glyphFormat: "%2.", glyphType: Te.DECIMAL },
      { glyphFormat: "%3.", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%4.", glyphType: Te.UPPER_LETTER },
      { glyphFormat: "%5.", glyphType: Te.DECIMAL },
      { glyphFormat: "%6.", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%7.", glyphType: Te.UPPER_LETTER },
      { glyphFormat: "%8.", glyphType: Te.DECIMAL },
      { glyphFormat: "%9.", glyphType: Te.LOWER_ROMAN }
    ])
  },
  ORDER_LIST_5: {
    listType: "ORDER_LIST",
    nestingLevel: In([
      { glyphFormat: "%1.", glyphType: Te.DECIMAL_ZERO },
      { glyphFormat: "%2.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%3.", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%4.", glyphType: Te.DECIMAL_ZERO },
      { glyphFormat: "%5.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%6.", glyphType: Te.LOWER_ROMAN },
      { glyphFormat: "%7.", glyphType: Te.DECIMAL_ZERO },
      { glyphFormat: "%8.", glyphType: Te.LOWER_LETTER },
      { glyphFormat: "%9.", glyphType: Te.LOWER_ROMAN }
    ])
  },
  CHECK_LIST: {
    listType: "CHECK_LIST",
    nestingLevel: ca("☐")
  },
  CHECK_LIST_CHECKED: {
    listType: "CHECK_LIST_CHECKED",
    nestingLevel: ca(
      "☑",
      {
        st: {
          s: we.TRUE
        }
      }
    )
  }
}, br = (t) => {
  const { glyphFormat: e, glyphType: n } = t, r = re.deepClone(Es.ORDER_LIST);
  return r.nestingLevel[0].glyphFormat = e, r.nestingLevel[0].glyphType = n, r;
}, Tm = {
  ORDER_LIST_QUICK_2: br(Or[
    "a)"
    /* ORDER_LIST_QUICK_2 */
  ]),
  ORDER_LIST_QUICK_3: br(Or[
    "a."
    /* ORDER_LIST_QUICK_3 */
  ]),
  ORDER_LIST_QUICK_4: br(Or[
    "i."
    /* ORDER_LIST_QUICK_4 */
  ]),
  ORDER_LIST_QUICK_6: br(Or[
    "I."
    /* ORDER_LIST_QUICK_6 */
  ])
};
Object.assign(Es, Tm);
const ZC = {
  "1.": "ORDER_LIST",
  "a)": "ORDER_LIST_QUICK_2",
  "a.": "ORDER_LIST_QUICK_3",
  "i.": "ORDER_LIST_QUICK_4",
  "A.": "ORDER_LIST_3",
  "I.": "ORDER_LIST_QUICK_6",
  "01.": "ORDER_LIST_5"
  /* ORDER_LIST_5 */
};
function Mm(t, e, n, r, s) {
  const i = Dm(t, e, n, r, s), o = xm(t, e, n, r, s), a = Lm(t, e, n, r, s), u = Um(t, e, n, r, s), c = Pm(t, e, n, r, s), l = km(t, e, n, r), h = Fm(t, e, n, r, s);
  return {
    dataStream: "",
    textRuns: i,
    paragraphs: o,
    sectionBreaks: a,
    customBlocks: u,
    tables: c,
    customRanges: l,
    customDecorations: h
  };
}
function Dm(t, e, n, r, s) {
  const { textRuns: i } = t, { textRuns: o } = e;
  if (i == null || o == null)
    return;
  const a = Ku(t, n, r);
  if (s !== Pe.REPLACE) {
    const u = qu(o, a, s);
    e.textRuns = u;
  }
  return ju(t, e, n, r), a;
}
function qu(t, e, n) {
  if (e.length === 0)
    return t;
  t = re.deepClone(t), e = re.deepClone(e);
  const r = [], s = t.length, i = e.length;
  let o = 0, a = 0, u = null;
  function c() {
    return u ? (r.push(u), u = null, !0) : !1;
  }
  for (; o < s && a < i; ) {
    const { st: f, ed: E, ts: R } = t[o], { st: O, ed: U, ts: ne, sId: X } = e[a];
    let de;
    if (n === Pe.COVER ? de = { ...ne, ...R } : de = { ...R }, E < O)
      c() || r.push(t[o]), o++;
    else if (U < f)
      c() || r.push(e[a]), a++;
    else {
      const T = {
        st: Math.min(f, O),
        ed: Math.max(f, O),
        ts: f < O ? { ...R } : { ...ne },
        sId: f < O ? void 0 : X
      };
      T.ed > T.st && r.push(T), r.push({
        st: Math.max(f, O),
        ed: Math.min(E, U),
        ts: de,
        sId: X
      }), E < U ? (o++, e[a].st = E, e[a].st === e[a].ed && a++) : (a++, t[o].st = U, t[o].st === t[o].ed && o++);
      const A = {
        st: Math.min(E, U),
        ed: Math.max(E, U),
        ts: E < U ? { ...ne } : { ...R },
        sId: E < U ? X : void 0
      };
      u = A.ed > A.st ? A : null;
    }
  }
  c();
  const l = r[r.length - 1], h = t[s - 1], d = e[i - 1];
  return l && l.ed !== Math.max(h.ed, d.ed) && (h.ed > d.ed ? r.push(h) : r.push(d)), _s(r);
}
function xm(t, e, n, r, s) {
  const { paragraphs: i } = t, { paragraphs: o } = e;
  if (i == null || o == null)
    return;
  const a = Xu(t, n, r);
  if (s !== Pe.REPLACE) {
    const u = [];
    for (const c of o) {
      const {
        startIndex: l,
        paragraphStyle: h,
        bullet: d
      } = c;
      let f = [];
      for (const E of a) {
        const {
          startIndex: R,
          paragraphStyle: O,
          bullet: U
        } = E;
        let ne, X;
        if (s === Pe.COVER ? (ne = { ...O, ...h }, X = {
          listId: "",
          listType: Ft.BULLET_LIST,
          nestingLevel: 0,
          textStyle: {},
          ...U,
          ...d
        }) : (ne = { ...h, ...O }, X = {
          listId: "",
          listType: Ft.BULLET_LIST,
          nestingLevel: 0,
          textStyle: {},
          ...d,
          ...U
        }), l === R) {
          f.push({
            startIndex: l,
            paragraphStyle: ne,
            bullet: X
          });
          break;
        }
      }
      u.push(...f), f = [];
    }
    e.paragraphs = u;
  }
  return Hu(t, e, n, r), a;
}
function Lm(t, e, n, r, s) {
  const { sectionBreaks: i } = t, { sectionBreaks: o } = e;
  if (i == null || o == null)
    return;
  const a = Ju(t, n, r);
  if (s !== Pe.REPLACE) {
    const u = [];
    for (const c of o) {
      const { startIndex: l } = c;
      let h = [];
      for (const d of a) {
        const { startIndex: f } = d;
        if (l === f) {
          s === Pe.COVER ? h.push({
            ...d,
            ...c
          }) : h.push({
            ...c,
            ...d
          });
          break;
        }
      }
      u.push(...h), h = [];
    }
    e.sectionBreaks = u;
  }
  return Wu(t, e, n, r), a;
}
function Um(t, e, n, r, s) {
  const { customBlocks: i = [] } = t, { customBlocks: o } = e;
  if (i == null || o == null)
    return;
  const a = Zu(t, n, r);
  if (s !== Pe.REPLACE) {
    const u = [];
    for (const c of o) {
      const { startIndex: l } = c;
      let h = [];
      for (const d of a) {
        const { startIndex: f } = d;
        if (l === f) {
          s === Pe.COVER ? h.push({
            ...d,
            ...c
          }) : h.push({
            ...c,
            ...d
          });
          break;
        }
      }
      u.push(...h), h = [];
    }
    e.customBlocks = u;
  }
  return zu(t, e, n, r), i.length && !t.customBlocks && (t.customBlocks = i), a;
}
function Pm(t, e, n, r, s) {
  const { tables: i } = t, { tables: o } = e;
  if (i == null || o == null)
    return;
  const a = Qu(t, n, r);
  if (s !== Pe.REPLACE) {
    const u = [];
    for (const c of o) {
      const { startIndex: l, endIndex: h } = c;
      let d = [];
      for (const f of a) {
        const { startIndex: E, endIndex: R } = f;
        if (E >= l && R <= h) {
          s === Pe.COVER ? d.push({
            ...f,
            ...c
          }) : d.push({
            ...c,
            ...f
          });
          break;
        }
      }
      u.push(...d), d = [];
    }
    e.tables = u;
  }
  return Yu(t, e, n, r), a;
}
function km(t, e, n, r, s) {
  t.customRanges || (t.customRanges = []), Qs(t.customRanges, r), Qs(t.customRanges, r + n);
  const i = r, o = r + n - 1, { customRanges: a } = e, u = [], c = /* @__PURE__ */ new Map();
  t.customRanges.forEach((h) => {
    const { startIndex: d, endIndex: f } = h;
    d >= i && f <= o ? c.set(h.rangeId, h) : u.push(h);
  });
  const l = [];
  return a ? (a.forEach((h) => {
    const { startIndex: d, endIndex: f } = h;
    u.push({
      ...h,
      startIndex: d + r,
      endIndex: f + r
    });
  }), t.customRanges = ki(u), l) : [];
}
function Fm(t, e, n, r, s) {
  t.customDecorations || (t.customDecorations = []), qs(t.customDecorations, r), qs(t.customDecorations, r + n);
  const i = [], { customDecorations: o } = t, { customDecorations: a = [] } = e;
  if (s === Pe.REPLACE) {
    for (let u = 0; u < o.length; u++) {
      const c = o[u], { startIndex: l, endIndex: h } = c;
      l >= r && h <= r + n - 1 && i.push(c);
    }
    a.forEach((u) => {
      const { startIndex: c, endIndex: l } = u;
      o.push({
        ...u,
        startIndex: c + r,
        endIndex: l + r
      });
    });
  } else
    for (const u of a) {
      const { id: c } = u;
      if (u.type === An.DELETED) {
        const l = o.filter((h) => h.id === c);
        l.length && i.push(...l);
      } else
        o.push({
          ...u,
          startIndex: u.startIndex + r,
          endIndex: u.endIndex + r
        });
    }
  for (const u of i) {
    const { id: c } = u, l = o.findIndex((h) => h.id === c);
    l !== -1 && o.splice(l, 1);
  }
  return t.customDecorations = Gu(o), i;
}
var el = /* @__PURE__ */ ((t) => (t[t.copy = 0] = "copy", t[t.cut = 1] = "cut", t))(el || {});
function ei(t, e, n, r = !0) {
  const { textRuns: s } = t;
  if (s) {
    const i = [];
    for (const o of s) {
      const a = re.deepClone(o), { st: u, ed: c } = a;
      re.hasIntersectionBetweenTwoRanges(u, c, e, n) && (e >= u && e <= c ? i.push({
        ...a,
        st: e,
        ed: Math.min(n, c)
      }) : n >= u && n <= c ? i.push({
        ...a,
        st: Math.max(e, u),
        ed: n
      }) : i.push(a));
    }
    return _s(
      i.map((o) => {
        const { st: a, ed: u } = o;
        return {
          ...o,
          st: a - e,
          ed: u - e
        };
      })
    );
  } else if (r)
    return [{
      st: 0,
      ed: n - e,
      ts: {}
    }];
}
function $m(t, e, n) {
  const { tables: r = [] } = t, s = [];
  for (const i of r) {
    const o = re.deepClone(i), { startIndex: a, endIndex: u } = o;
    a >= e && u <= n && s.push({
      ...o,
      startIndex: a - e,
      endIndex: u - e
    });
  }
  return s;
}
function Bm(t, e, n) {
  const { paragraphs: r = [] } = t, s = [];
  for (const i of r) {
    const { startIndex: o } = i;
    o >= e && o < n && s.push(re.deepClone(i));
  }
  if (s.length)
    return s.map((i) => ({
      ...i,
      startIndex: i.startIndex - e
    }));
}
function QC(t, e, n) {
  const { sectionBreaks: r = [] } = t, s = [];
  for (const i of r) {
    const { startIndex: o } = i;
    o >= e && o <= n && s.push(re.deepClone(i));
  }
  if (s.length)
    return s.map((i) => ({
      ...i,
      startIndex: i.startIndex - e
    }));
}
function jm(t, e, n) {
  const { customBlocks: r = [] } = t, s = [];
  for (const i of r) {
    const { startIndex: o } = i;
    o >= e && o <= n && s.push(re.deepClone(i));
  }
  if (s.length)
    return s.map((i) => ({
      ...i,
      startIndex: i.startIndex - e
    }));
}
function Dt(t, e, n, r = !0, s = 1) {
  const { dataStream: i } = t, o = {
    dataStream: i.slice(e, n)
  };
  o.textRuns = ei(t, e, n, r);
  const a = $m(t, e, n);
  if (a.length && (o.tables = a), o.paragraphs = Bm(t, e, n), s === 1) {
    const c = Wm(t, e, n);
    c ? o.customDecorations = c : r && (o.customDecorations = []);
  }
  const { customRanges: u } = Hm(t, e, n);
  return u ? o.customRanges = u : r && (o.customRanges = []), o.customBlocks = jm(t, e, n), o;
}
function qC(t) {
  const { dataStream: e, textRuns: n, paragraphs: r, customRanges: s, customDecorations: i, tables: o } = t;
  let a = 0, u = 0;
  s == null || s.forEach((l) => {
    l.startIndex < 0 && (a = Math.max(a, -l.startIndex)), l.endIndex > e.length - 1 && (u = Math.max(u, l.endIndex - e.length + 1));
  });
  const c = `${e}`;
  return n && (n[0] && (n[0].st = n[0].st - a), n[n.length - 1] && (n[n.length - 1].ed = n[n.length - 1].ed + u)), n == null || n.forEach((l) => {
    l.st += a, l.ed += a;
  }), r == null || r.forEach((l) => {
    l.startIndex += a;
  }), s == null || s.forEach((l) => {
    l.startIndex += a, l.endIndex += a;
  }), i == null || i.forEach((l) => {
    l.startIndex += a, l.endIndex += u;
  }), o == null || o.forEach((l) => {
    l.startIndex += a, l.endIndex += u;
  }), {
    ...t,
    dataStream: c,
    textRuns: n,
    paragraphs: r,
    customRanges: s,
    customDecorations: i,
    tables: o
  };
}
function Hm(t, e, n) {
  if (t.customRanges == null)
    return {};
  const { customRanges: r } = t;
  return {
    customRanges: r.filter((a) => Math.max(a.startIndex, e) <= Math.min(a.endIndex, n - 1)).map((a) => ({
      ...a,
      startIndex: Math.max(a.startIndex, e),
      endIndex: Math.min(a.endIndex, n - 1)
    })).map((a) => ({
      ...a,
      startIndex: a.startIndex - e,
      endIndex: a.endIndex - e
    })),
    leftOffset: 0,
    rightOffset: 0
  };
}
function Wm(t, e, n) {
  if (t.customDecorations == null)
    return;
  const { customDecorations: r = [] } = t, s = [];
  return r.forEach((i) => {
    if (Math.max(i.startIndex, e) <= Math.min(i.endIndex, n - 1)) {
      const o = re.deepClone(i);
      s.push({
        ...o,
        startIndex: Math.max(o.startIndex - e, 0),
        endIndex: Math.min(o.endIndex, n - 1) - e
      });
    }
  }), s;
}
function zm(t, e, n) {
  return t == null || e == null ? t != null ? t : e : qu(t, e, n);
}
function Ym(t, e, n) {
  if (t == null || e == null)
    return t != null ? t : e;
  if (e.length === 0 || t.length === 0)
    return t;
  if (e.length > 1 || t.length > 1)
    throw new Error("Cannot cover multiple customRanges");
  return n === Pe.REPLACE ? [{
    ...t[0]
  }] : [{
    ...e[0],
    ...t[0]
  }];
}
function Vm(t, e, n) {
  return e.length === 0 || t.length === 0 || n === Pe.REPLACE ? t : [
    ...t,
    ...e.filter((r) => !t.some((s) => r.id === s.id))
  ];
}
function ha(t, e, n = Pe.COVER) {
  if (e.dataStream !== "")
    throw new Error("Cannot compose other body with non-empty dataStream");
  const r = {
    dataStream: t.dataStream
  }, {
    textRuns: s,
    paragraphs: i = [],
    customRanges: o,
    customDecorations: a = []
  } = t, {
    textRuns: u,
    paragraphs: c = [],
    customRanges: l,
    customDecorations: h = []
  } = e;
  r.textRuns = zm(u, s, n), r.customRanges = Ym(l, o, n);
  const d = Vm(h, a, n);
  d.length && (r.customDecorations = d);
  const f = [];
  let E = 0, R = 0;
  for (; E < i.length && R < c.length; ) {
    const O = i[E], U = c[R], { startIndex: ne } = O, { startIndex: X } = U;
    ne === X ? (f.push(re.deepMerge(O, U)), E++, R++) : ne < X ? (f.push(re.deepClone(O)), E++) : (f.push(re.deepClone(U)), R++);
  }
  return E < i.length && f.push(...i.slice(E)), R < c.length && f.push(...c.slice(R)), f.length && (r.paragraphs = f), r;
}
function Gm(t) {
  const { body: e } = t;
  if (e == null)
    return !0;
  const { textRuns: n, paragraphs: r, customRanges: s, customBlocks: i, customDecorations: o, tables: a } = e;
  return n == null && r == null && s == null && i == null && o == null && a == null;
}
class Bn {
  constructor(e) {
    C(this, "_index", 0);
    C(this, "_offset", 0);
    this._actions = e;
  }
  hasNext() {
    return this.peekLength() < Number.POSITIVE_INFINITY;
  }
  next(e) {
    e || (e = Number.POSITIVE_INFINITY);
    const n = this._actions[this._index];
    if (n) {
      const r = this._offset, s = n.len;
      return e >= s - r ? (e = s - r, this._index += 1, this._offset = 0) : this._offset += e, n.t === ce.DELETE || n.t === ce.RETAIN && n.body == null ? re.deepClone({
        ...n,
        len: e
      }) : re.deepClone({
        ...n,
        len: e,
        body: Dt(n.body, r, r + e, !1)
      });
    } else
      return {
        t: ce.RETAIN,
        len: Number.POSITIVE_INFINITY
      };
  }
  peek() {
    return this._actions[this._index];
  }
  peekLength() {
    return this._actions[this._index] ? this._actions[this._index].len - this._offset : Number.POSITIVE_INFINITY;
  }
  peekType() {
    const e = this._actions[this._index];
    return e ? e.t : ce.RETAIN;
  }
  rest() {
    if (this.hasNext()) {
      if (this._offset === 0)
        return this._actions.slice(this._index);
      {
        const e = this._offset, n = this._index, r = this.next(), s = this._actions.slice(this._index);
        return this._offset = e, this._index = n, [r].concat(s);
      }
    } else return [];
  }
}
class lr {
  constructor() {
    C(this, "cursor", 0);
  }
  reset() {
    return this.cursor = 0, this;
  }
  moveCursor(e) {
    this.cursor += e;
  }
  moveCursorTo(e) {
    this.cursor = e;
  }
}
function Km(t, e, n) {
  const { dataStream: r } = t, s = n, i = n + e, o = Ku(t, e, n), a = Xu(t, e, n), u = Ju(t, e, n), c = Zu(t, e, n), l = Qu(t, e, n), h = Sm(t, e, n), d = Am(t, e, n);
  let f = "";
  return r && (t.dataStream = pp(r, s, i), f = r.slice(s, i)), {
    dataStream: f,
    textRuns: o,
    paragraphs: a,
    sectionBreaks: u,
    customBlocks: c,
    tables: l,
    customRanges: h,
    customDecorations: d
  };
}
function Xm(t, e, n, r) {
  t.dataStream = gp(t.dataStream, r, e.dataStream), ju(t, e, n, r), Hu(t, e, n, r), Wu(t, e, n, r), zu(t, e, n, r), Yu(t, e, n, r), Om(t, e, n, r), bm(t, e, n, r);
}
function Jm(t, e, n, r, s = Pe.COVER) {
  return Mm(t, e, n, r, s);
}
function Zm(t, e, n) {
  return e <= 0 ? { dataStream: "" } : Km(t, e, n);
}
function Qm(t, e, n, r) {
  n !== 0 && Xm(t, e, n, r);
}
function qm(t, e) {
  const n = new lr();
  return n.reset(), e.forEach((r) => {
    const s = re.deepClone(r);
    switch (s.t) {
      case ce.RETAIN: {
        const { coverType: i, body: o, len: a } = s;
        o != null && Jm(t, o, a, n.cursor, i), n.moveCursor(a);
        break;
      }
      case ce.INSERT: {
        const { body: i, len: o } = s;
        Qm(t, i, o, n.cursor), n.moveCursor(o);
        break;
      }
      case ce.DELETE: {
        const { len: i } = s;
        Zm(t, i, n.cursor);
        break;
      }
      default:
        throw new Error(`Unknown action type for action: ${s}.`);
    }
  }), t;
}
function e_(t, e, n, r, s) {
  if (t == null || e == null)
    return e;
  if (t.length === 0 || e.length === 0)
    return [];
  e = re.deepClone(e), t = re.deepClone(t);
  const i = [], o = e.length, a = t.length;
  let u = 0, c = 0, l = null;
  function h() {
    return l ? (i.push(l), l = null, !0) : !1;
  }
  for (; u < o && c < a; ) {
    const { st: R, ed: O, ts: U } = e[u], { st: ne, ed: X, ts: de, sId: T } = t[c];
    let A = {};
    if (s === 0)
      A = { ...U }, n === Pe.COVER && r === Pe.REPLACE && de && (A = Object.assign({}, de, A));
    else if (A = { ...U }, n === Pe.REPLACE) {
      if (r === Pe.REPLACE)
        A = { ...de };
      else if (U && de) {
        const H = Object.keys(U);
        for (const Z of H)
          de[Z] && delete A[Z];
      }
    } else if (r === Pe.REPLACE) {
      if (de) {
        const H = Object.keys(de);
        for (const Z of H)
          de[Z] !== void 0 && (A[Z] = de[Z]);
      }
    } else if (de) {
      const H = Object.keys(de);
      for (const Z of H)
        A[Z] !== void 0 && delete A[Z];
    }
    if (O < ne)
      h() || i.push(e[u]), u++;
    else if (X < R)
      h() || i.push(t[c]), c++;
    else {
      const H = {
        st: Math.min(R, ne),
        ed: Math.max(R, ne),
        ts: R < ne ? { ...U } : { ...de },
        sId: R < ne ? void 0 : T
      };
      H.ed > H.st && i.push(), i.push({
        st: Math.max(R, ne),
        ed: Math.min(O, X),
        ts: A,
        sId: T
      }), O < X ? (u++, t[c].st = O, t[c].st === t[c].ed && c++) : (c++, e[u].st = X, e[u].st === e[u].ed && u++);
      const Z = {
        st: Math.min(O, X),
        ed: Math.max(O, X),
        ts: O < X ? { ...de } : { ...U },
        sId: O < X ? T : void 0
      };
      l = Z.ed > Z.st ? Z : null;
    }
  }
  h();
  const d = i[i.length - 1], f = e[o - 1], E = t[a - 1];
  return d.ed !== Math.max(f.ed, E.ed) && (f.ed > E.ed ? i.push(f) : i.push(E)), _s(i, !0);
}
function t_(t, e, n, r, s) {
  if (t == null || e == null)
    return e;
  if (t.length === 0 || e.length === 0)
    return [];
  if (t.length > 1 || e.length > 1)
    throw new Error("CustomRanges is only supported transform for length one now.");
  const i = t[0], o = e[0];
  if (n === Pe.REPLACE)
    return s === 1 ? [re.deepClone(i)] : [re.deepClone(o)];
  if (r === Pe.REPLACE) {
    const a = re.deepClone(o);
    return s === 1 && Object.assign(a, re.deepClone(i)), [a];
  } else {
    const a = re.deepClone(o);
    return s === 1 && Object.assign(a, re.deepClone(i)), [a];
  }
}
function da(t, e, n, r, s) {
  const i = {
    startIndex: e.startIndex
  };
  if (e.paragraphStyle && (i.paragraphStyle = re.deepClone(e.paragraphStyle), t.paragraphStyle)) {
    if (n === Pe.REPLACE)
      if (r === Pe.REPLACE)
        s === 1 && (i.paragraphStyle = {
          ...t.paragraphStyle
        });
      else if (s === 1) {
        const o = Object.keys(t.paragraphStyle);
        for (const a of o)
          t.paragraphStyle[a] !== void 0 && (i.paragraphStyle[a] = t.paragraphStyle[a]);
      } else {
        const o = Object.keys(t.paragraphStyle);
        for (const a of o)
          i.paragraphStyle[a] === void 0 && (i.paragraphStyle[a] = t.paragraphStyle[a]);
      }
    else if (r === Pe.REPLACE)
      if (s === 1) {
        const o = Object.keys(t.paragraphStyle);
        for (const a of o)
          t.paragraphStyle[a] !== void 0 && (i.paragraphStyle[a] = t.paragraphStyle[a]);
      } else {
        const o = Object.keys(t.paragraphStyle);
        for (const a of o)
          i.paragraphStyle[a] === void 0 && (i.paragraphStyle[a] = t.paragraphStyle[a]);
      }
    else if (s === 1) {
      const o = Object.keys(t.paragraphStyle);
      for (const a of o)
        i.paragraphStyle[a] && delete i.paragraphStyle[a];
    }
  }
  return n === Pe.REPLACE && r === Pe.REPLACE ? i.bullet = s === 1 ? re.deepClone(t.bullet) : re.deepClone(e.bullet) : t.bullet === void 0 ? i.bullet = re.deepClone(e.bullet) : n === Pe.REPLACE || r === Pe.REPLACE ? i.bullet = s === 0 && e.bullet ? re.deepClone(e.bullet) : re.deepClone(t.bullet) : s === 0 && e.bullet !== void 0 && (i.bullet = re.deepClone(e.bullet)), i;
}
function n_(t, e) {
  if (t == null || e == null)
    return e;
  if (t.length === 0 || e.length === 0)
    return re.deepClone(e);
  const n = [];
  for (const r of e) {
    const { id: s, type: i } = r;
    let o = !1;
    for (const a of t)
      if (a.id === s) {
        (a.type === An.DELETED || i === An.DELETED) && (o = !0, n.push({
          ...r,
          type: An.DELETED
        }));
        break;
      }
    o || n.push(r);
  }
  return n;
}
function r_(t, e, n = !1) {
  const { body: r, coverType: s = Pe.COVER } = t, { body: i, coverType: o = Pe.COVER } = e;
  if (r == null || r.dataStream !== "" || i == null || i.dataStream !== "")
    throw new Error("Data stream is not supported in retain transform.");
  const a = {
    dataStream: ""
  }, u = o, {
    textRuns: c,
    paragraphs: l = [],
    customRanges: h,
    customDecorations: d
  } = r, {
    textRuns: f,
    paragraphs: E = [],
    customRanges: R,
    customDecorations: O
  } = i, U = e_(
    c,
    f,
    s,
    o,
    n ? 1 : 0
    /* COVER */
  );
  U && (a.textRuns = U);
  const ne = t_(
    h,
    R,
    s,
    o,
    n ? 1 : 0
    /* COVER */
  );
  ne && (a.customRanges = ne);
  const X = n_(
    d,
    O
  );
  X && (a.customDecorations = X);
  const de = [];
  let T = 0, A = 0;
  for (; T < l.length && A < E.length; ) {
    const H = l[T], Z = E[A], { startIndex: fe } = H, { startIndex: ae } = Z;
    if (fe === ae) {
      let m = {
        startIndex: fe
      };
      n ? m = da(
        H,
        Z,
        s,
        o,
        1
        /* COVER_ONLY_NOT_EXISTED */
      ) : m = da(
        H,
        Z,
        s,
        o,
        0
        /* COVER */
      ), de.push(m), T++, A++;
    } else fe < ae ? T++ : (de.push(re.deepClone(Z)), A++);
  }
  return A < E.length && de.push(...E.slice(A)), de.length && (a.paragraphs = de), {
    coverType: u,
    body: a
  };
}
function fa(t) {
  return Object.keys(t).length === 1;
}
const wn = class wn {
  constructor() {
    C(this, "_actions", []);
  }
  static apply(e, n) {
    return qm(e, n);
  }
  // eslint-disable-next-line complexity
  static compose(e, n) {
    const r = new Bn(e), s = new Bn(n), i = new wn();
    for (; r.hasNext() || s.hasNext(); )
      if (s.peekType() === ce.INSERT)
        i.push(s.next());
      else if (r.peekType() === ce.DELETE)
        i.push(r.next());
      else {
        const o = Math.min(r.peekLength(), s.peekLength()), a = r.next(o), u = s.next(o);
        if (a.t === ce.INSERT && u.t === ce.RETAIN)
          u.body == null ? i.push(a) : i.push({
            ...a,
            body: ha(a.body, u.body, u.coverType)
          });
        else if (a.t === ce.RETAIN && u.t === ce.RETAIN)
          if (a.body == null && u.body == null)
            i.push(a.len !== Number.POSITIVE_INFINITY ? a : u);
          else if (a.body && u.body) {
            const c = a.coverType === Pe.REPLACE || u.coverType === Pe.REPLACE ? Pe.REPLACE : Pe.COVER;
            i.push({
              ...a,
              t: ce.RETAIN,
              coverType: c,
              body: ha(a.body, u.body, u.coverType)
            });
          } else
            i.push(a.body ? a : u);
        else a.t === ce.RETAIN && u.t === ce.DELETE ? i.push(u) : a.t === ce.INSERT && (u.t, ce.DELETE);
      }
    return i.trimEndUselessRetainAction(), i.serialize();
  }
  /**
   * |(this↓ \| other→) | **insert** | **retain** | **delete** |
   * | ---------------- | ---------- | ---------- | ---------- |
   * |    **insert**    |   Case 1   |   Case 2   |   Case 2   |
   * |    **retain**    |   Case 1   |   Case 5   |   Case 4   |
   * |    **delete**    |   Case 1   |   Case 3   |   Case 3   |
   *
   * Case 1: When the other action type is an insert operation,
   *         the insert operation is retained regardless of the type of action this action
   * Case 2: When this action type is an insert operation and the other action type is a
   *         non-insert operation, you need to retain the length of this action insert
   * Case 3: When this action is a delete operation, there are two scenarios:
   *      1) When other is a delete operation, since it is a delete operation, this has
   *         already been deleted, so the target does not need to be in delete, and it can
   *         be continued directly
   *      2) When other is the retain operation, although this action delete occurs first,
   *         the delete priority is higher, so the delete operation is retained, and the origin
   *         delete has been applied, so it is directly continued
   * Case 4: other is the delete operation, this is the retain operation, and the target delete operation
   *         is kept
   * Case 5: When both other and this are retain operations
   *      1) If the other body attribute does not exist, directly retain length
   *      2) If the other body property exists, then execute the TransformBody logic to override it
   */
  // priority - if true, this actions takes priority over other, that is, this actions are considered to happen "first".
  // thisActions is the target action.
  static transform(e, n, r = "right") {
    return this._transform(n, e, r === "left" ? "right" : "left");
  }
  // otherActions is the actions to be transformed.
  static _transform(e, n, r = "right") {
    const s = new Bn(e), i = new Bn(n), o = new wn();
    for (; s.hasNext() || i.hasNext(); )
      if (s.peekType() === ce.INSERT && (r === "left" || i.peekType() !== ce.INSERT)) {
        const a = s.next();
        o.retain(a.len);
      } else if (i.peekType() === ce.INSERT)
        o.push(i.next());
      else {
        const a = Math.min(s.peekLength(), i.peekLength()), u = s.next(a), c = i.next(a);
        if (u.t === ce.DELETE)
          continue;
        if (c.t === ce.DELETE) {
          o.push(c);
          continue;
        }
        if (u.body == null || c.body == null)
          o.push(c);
        else {
          const { coverType: l, body: h } = r_(u, c, r === "left");
          o.push({
            ...c,
            t: ce.RETAIN,
            coverType: l,
            body: h
          });
        }
      }
    return o.trimEndUselessRetainAction(), o.serialize();
  }
  /**
   * Used to transform selection. Why not named transformSelection?
   * Because Univer Doc supports multiple Selections in one document, user need to encapsulate transformSelections at the application layer.
   */
  static transformPosition(e, n, r = !1) {
    const s = new Bn(e);
    let i = 0;
    for (; s.hasNext() && i <= n; ) {
      const o = s.peekLength(), a = s.peekType();
      if (s.next(), a === ce.DELETE) {
        n -= Math.min(o, n - i);
        continue;
      } else a === ce.INSERT && (i < n || !r) && (n += o);
      i += o;
    }
    return n;
  }
  static isNoop(e) {
    return e.length === 0;
  }
  static invert(e) {
    const n = [];
    for (const r of e)
      if (r.t === ce.INSERT)
        n.push({
          t: ce.DELETE,
          len: r.len,
          body: r.body
        });
      else if (r.t === ce.DELETE) {
        if (r.body == null)
          throw new Error("Can not invert DELETE action without body property, makeInvertible must be called first.");
        n.push({
          t: ce.INSERT,
          body: r.body,
          len: r.len
        });
      } else if (r.body != null) {
        if (r.oldBody == null)
          throw new Error("Can not invert RETAIN action without oldBody property, makeInvertible must be called first.");
        n.push({
          t: ce.RETAIN,
          body: r.oldBody,
          oldBody: r.body,
          len: r.len,
          coverType: Pe.REPLACE
        });
      } else
        n.push(r);
    return n;
  }
  static makeInvertible(e, n) {
    const r = [];
    let s = 0;
    for (const i of e) {
      if (i.t === ce.DELETE && (i.body == null || i.body && i.body.dataStream.length !== i.len)) {
        const o = Dt(n, s, s + i.len, !1);
        i.len = o.dataStream.length, i.body = o;
      }
      if (i.t === ce.RETAIN && i.body != null) {
        const o = Dt(n, s, s + i.len, !0);
        i.oldBody = {
          ...o,
          dataStream: ""
        }, i.len = o.dataStream.length;
      }
      r.push(i), i.t !== ce.INSERT && (s += i.len);
    }
    return r;
  }
  insert(e, n) {
    const r = {
      t: ce.INSERT,
      body: n,
      len: e
    };
    return this.push(r), this;
  }
  retain(e, n, r) {
    const s = {
      t: ce.RETAIN,
      len: e
    };
    return n != null && (s.body = n), r != null && (s.coverType = r), this.push(s), this;
  }
  delete(e) {
    const n = {
      t: ce.DELETE,
      len: e
    };
    return this.push(n), this;
  }
  empty() {
    return this._actions = [], this;
  }
  serialize() {
    return this._actions;
  }
  // eslint-disable-next-line complexity
  push(...e) {
    if (e.length > 1) {
      for (const i of e)
        this.push(i);
      return this;
    }
    let n = this._actions.length, r = this._actions[n - 1];
    const s = re.deepClone(e[0]);
    if (s.t === ce.RETAIN && s.len === 0 && s.body == null)
      return this;
    if (typeof r == "object") {
      if (r.t === ce.DELETE && s.t === ce.DELETE)
        return r.len += s.len, this;
      if (r.t === ce.DELETE && s.t === ce.INSERT && (n -= 1, r = this._actions[n - 1], r == null))
        return this._actions.unshift(s), this;
      if (r.t === ce.RETAIN && s.t === ce.RETAIN && r.body == null && s.body == null)
        return r.len += s.len, this;
      if (r.t === ce.INSERT && fa(r.body) && s.t === ce.INSERT && fa(s.body))
        return r.len += s.len, r.body.dataStream += s.body.dataStream, this;
    }
    return n === this._actions.length ? this._actions.push(s) : this._actions.splice(n, 0, s), this;
  }
  trimEndUselessRetainAction() {
    let e = this._actions[this._actions.length - 1];
    for (; e && e.t === ce.RETAIN && Gm(e); )
      this._actions.pop(), e = this._actions[this._actions.length - 1];
    return this;
  }
};
// static name = 'text-x';
C(wn, "id", "text-x"), C(wn, "uri", "https://github.com/dream-num/univer#text-x");
let Ke = wn;
Object.defineProperty(Ke, "name", {
  value: "text-x"
});
const On = class On {
  static registerSubtype(e) {
    var n;
    e == null || this._subTypes.has(e.name) && ((n = this._subTypes.get(e.name)) == null ? void 0 : n.id) !== Ke.id || (this._subTypes.set(e.name, e), mt.type.registerSubtype(e));
  }
  static apply(e, n) {
    if (!mt.type.isNoop(n))
      return mt.type.apply(e, n);
  }
  static compose(e, n) {
    return mt.type.compose(e, n);
  }
  static transform(e, n, r) {
    return mt.type.transform(e, n, r);
  }
  // Use to transform cursor position, just call TextXPro.transformPosition.
  static transformPosition(e, n, r = "right") {
    return e && e.length === 2 && e[0] === "body" && e[1].et === Ke.name ? Ke.transformPosition(e[1].e, n, r === "left") : n;
  }
  static invertWithDoc(e, n) {
    return mt.type.invertWithDoc(e, n);
  }
  static isNoop(e) {
    return mt.type.isNoop(e);
  }
  static getInstance() {
    return this._instance == null && (this._instance = new On()), this._instance;
  }
  // eslint-disable-next-line ts/no-explicit-any
  removeOp(e, n) {
    return mt.removeOp(e, n);
  }
  moveOp(e, n) {
    return mt.moveOp(e, n);
  }
  // eslint-disable-next-line ts/no-explicit-any
  insertOp(e, n) {
    return mt.insertOp(e, n);
  }
  // eslint-disable-next-line ts/no-explicit-any
  replaceOp(e, n, r) {
    return mt.replaceOp(e, n, r);
  }
  editOp(e, n = ["body"]) {
    return mt.editOp(n, Ke.name, e);
  }
};
// static name = 'json-x';
C(On, "uri", "https://github.com/dream-num/univer#json-x"), C(On, "_subTypes", /* @__PURE__ */ new Map()), C(On, "_instance", null);
let tn = On;
tn.registerSubtype(Ke);
const tl = {
  id: "default_doc",
  documentStyle: {}
};
class s_ extends Ui {
  constructor(n) {
    var r;
    super();
    C(this, "type", Fe.UNIVER_DOC);
    C(this, "_name$", new lt(""));
    C(this, "name$", this._name$.asObservable());
    C(this, "snapshot");
    this.snapshot = { ...tl, ...n }, this._name$.next((r = this.snapshot.title) != null ? r : "No Title");
  }
  getUnitId() {
    throw new Error("Method not implemented.");
  }
  getRev() {
    var n;
    return (n = this.snapshot.rev) != null ? n : 1;
  }
  incrementRev() {
    this.snapshot.rev = this.getRev() + 1;
  }
  setRev(n) {
    this.snapshot.rev = n;
  }
  setName(n) {
    this.snapshot.title = n, this._name$.next(n);
  }
  get drawings() {
    return this.snapshot.drawings;
  }
  get documentStyle() {
    return this.snapshot.documentStyle;
  }
  get lists() {
    return this.snapshot.lists;
  }
  get zoomRatio() {
    var n;
    return ((n = this.snapshot.settings) == null ? void 0 : n.zoomRatio) || 1;
  }
  resetDrawing(n, r) {
    this.snapshot.drawings = n, this.snapshot.drawingsOrder = r;
  }
  getBody() {
    return this.snapshot.body;
  }
  getSnapshot() {
    return this.snapshot;
  }
  getBulletPresetList() {
    var s;
    const n = (s = this.snapshot.lists) != null ? s : {};
    return {
      ...Es,
      ...n
    };
  }
  updateDocumentId(n) {
    this.snapshot.id = n;
  }
  updateDocumentRenderConfig(n) {
    const { documentStyle: r } = this.snapshot;
    r.renderConfig == null ? r.renderConfig = n : r.renderConfig = {
      ...r.renderConfig,
      ...n
    };
  }
  updateDocumentStyle(n) {
    this.snapshot.documentStyle == null ? this.snapshot.documentStyle = n : this.snapshot.documentStyle = {
      ...this.snapshot.documentStyle,
      ...n
    };
  }
  updateDocumentDataMargin(n) {
    const { t: r, l: s, b: i, r: o } = n, { documentStyle: a } = this.snapshot;
    r != null && (a.marginTop = r), s != null && (a.marginLeft = s), i != null && (a.marginBottom = i), o != null && (a.marginRight = o);
  }
  updateDocumentDataPageSize(n, r) {
    const { documentStyle: s } = this.snapshot;
    if (!s.pageSize) {
      n = n != null ? n : Number.POSITIVE_INFINITY, r = r != null ? r : Number.POSITIVE_INFINITY, s.pageSize = {
        width: n,
        height: r
      };
      return;
    }
    n !== void 0 && (s.pageSize.width = n), r !== void 0 && (s.pageSize.height = r);
  }
  updateDrawing(n, r) {
    const { drawings: s } = this, { width: i, height: o, left: a, top: u } = r, c = s == null ? void 0 : s[n];
    if (!c)
      return;
    const l = c.docTransform;
    l.size.width = i, l.size.height = o, l.positionH.posOffset = a, l.positionV.posOffset = u;
  }
  setZoomRatio(n = 1) {
    this.snapshot.settings == null ? this.snapshot.settings = {
      zoomRatio: n
    } : this.snapshot.settings.zoomRatio = 1;
  }
}
class jt extends s_ {
  constructor(n) {
    var s, i;
    super(re.isEmptyObject(n) ? _m() : n);
    C(this, "_unitId");
    C(this, "headerModelMap", /* @__PURE__ */ new Map());
    C(this, "footerModelMap", /* @__PURE__ */ new Map());
    C(this, "change$", new lt(0));
    const r = 6;
    this._unitId = (s = this.snapshot.id) != null ? s : re.generateRandomId(r), this._initializeHeaderFooterModel(), this._name$.next((i = this.snapshot.title) != null ? i : "");
  }
  dispose() {
    super.dispose(), this.headerModelMap.forEach((n) => {
      n.dispose();
    }), this.footerModelMap.forEach((n) => {
      n.dispose();
    }), this._name$.complete();
  }
  getDrawings() {
    return this.snapshot.drawings;
  }
  getDrawingsOrder() {
    return this.snapshot.drawingsOrder;
  }
  getCustomRanges() {
    var n;
    return (n = this.snapshot.body) == null ? void 0 : n.customRanges;
  }
  getCustomDecorations() {
    var n;
    return (n = this.snapshot.body) == null ? void 0 : n.customDecorations;
  }
  getSettings() {
    return this.snapshot.settings;
  }
  // TODO: @JOCS do not use reset, please use apply to modify the snapshot.
  reset(n) {
    if (n.id && n.id !== this._unitId)
      throw new Error("Cannot reset a document model with a different unit id!");
    this.snapshot = { ...tl, ...n }, this._initializeHeaderFooterModel(), this.change$.next(this.change$.value + 1);
  }
  getSelfOrHeaderFooterModel(n) {
    if (n != null) {
      if (this.headerModelMap.has(n))
        return this.headerModelMap.get(n);
      if (this.footerModelMap.has(n))
        return this.footerModelMap.get(n);
    }
    return this;
  }
  getUnitId() {
    return this._unitId;
  }
  apply(n) {
    if (!tn.isNoop(n))
      return this.snapshot = tn.apply(this.snapshot, n), n != null && n.some((r) => Array.isArray(r) && ((r == null ? void 0 : r[0]) === "headers" || (r == null ? void 0 : r[0]) === "footers")) && (this.headerModelMap.clear(), this.footerModelMap.clear(), this._initializeHeaderFooterModel()), this.change$.next(this.change$.value + 1), this.snapshot;
  }
  sliceBody(n, r, s = el.copy) {
    const i = this.getBody();
    if (i != null)
      return Dt(i, n, r, !1, s);
  }
  _initializeHeaderFooterModel() {
    const { headers: n, footers: r } = this.getSnapshot();
    if (n)
      for (const s in n) {
        const i = n[s];
        this.headerModelMap.set(s, new jt(i)), this.headerModelMap.get(s).updateDocumentId(this.getUnitId());
      }
    if (r)
      for (const s in r) {
        const i = r[s];
        this.footerModelMap.set(s, new jt(i)), this.footerModelMap.get(s).updateDocumentId(this.getUnitId());
      }
  }
  updateDocumentId(n) {
    super.updateDocumentId(n), this._unitId = n;
  }
}
function i_(t) {
  const { ranges: e, id: n, type: r } = t, s = new Ke();
  let i = 0;
  for (let o = 0; o < e.length; o++) {
    const a = e[o], { startOffset: u, endOffset: c } = a;
    u > 0 && s.push({
      t: ce.RETAIN,
      len: u - i
    }), s.push({
      t: ce.RETAIN,
      body: {
        dataStream: "",
        customDecorations: [{
          id: n,
          type: r,
          startIndex: 0,
          endIndex: c - u - 1
        }]
      },
      len: c - u
    }), i = c;
  }
  return s;
}
function o_(t) {
  var l, h, d;
  const { id: e, segmentId: n, documentDataModel: r } = t, s = r == null ? void 0 : r.getBody();
  if (!r || !s)
    return !1;
  const i = (d = (h = (l = r.getSelfOrHeaderFooterModel(n)) == null ? void 0 : l.getBody()) == null ? void 0 : h.customDecorations) == null ? void 0 : d.find((f) => f.id === e);
  if (!i)
    return !1;
  const o = new Ke(), { startIndex: a, endIndex: u } = i, c = u - a + 1;
  return o.push({
    t: ce.RETAIN,
    len: a
  }), o.push({
    t: ce.RETAIN,
    len: c,
    body: {
      dataStream: "",
      customDecorations: [
        {
          startIndex: 0,
          endIndex: c - 1,
          id: e,
          type: An.DELETED
        }
      ]
    }
  }), o;
}
function nl(t, e, n, r) {
  return t <= n && e >= n || t >= n && t <= r;
}
function a_(t, e) {
  const n = [];
  for (let r = 0, s = e.length; r < s; r++) {
    const i = e[r];
    t.collapsed ? i.startIndex < t.startOffset && t.startOffset <= i.endIndex && n.push(i) : nl(t.startOffset, t.endOffset - 1, i.startIndex, i.endIndex) && n.push(i);
  }
  return n;
}
function u_(t) {
  return {
    ...re.deepClone(t),
    rangeId: qt()
  };
}
function l_(t, e) {
  const n = [];
  let r = t[0];
  for (const s of e)
    s < t[0] || s > t[1] || (r < s && n.push([r, s - 1]), r = s + 1);
  return r <= t[1] && n.push([r, t[1]]), n;
}
function rl(t, e, n, r) {
  const s = [];
  for (let i = 0, o = n.length; i < o; i++) {
    const a = n[i];
    if ((r === void 0 || a.rangeType === r) && Math.max(a.startIndex, t) <= Math.min(a.endIndex, e) && s.push({ ...a }), a.startIndex > e)
      break;
  }
  return s;
}
function c_(t, e) {
  var i, o, a, u, c;
  const n = rl(t.startOffset, t.collapsed ? t.startOffset : t.endOffset - 1, (i = e.customRanges) != null ? i : []), r = Math.min(t.startOffset, (a = (o = n[0]) == null ? void 0 : o.startIndex) != null ? a : 1 / 0), s = Math.max(t.endOffset, ((c = (u = n[n.length - 1]) == null ? void 0 : u.endIndex) != null ? c : -1 / 0) + 1);
  return {
    startOffset: r,
    endOffset: s,
    collapsed: r === s
  };
}
function h_(t) {
  var h, d, f;
  const { rangeId: e, segmentId: n, documentDataModel: r, insert: s } = t, i = (d = (h = r.getSelfOrHeaderFooterModel(n).getBody()) == null ? void 0 : h.customRanges) == null ? void 0 : d.find((E) => E.rangeId === e);
  if (!i)
    return !1;
  const { startIndex: o, endIndex: a } = i, u = new Ke(), c = a - o + 1;
  u.push({
    t: ce.RETAIN,
    len: o
  }), u.push({
    t: ce.RETAIN,
    len: c,
    body: {
      dataStream: "",
      customRanges: []
    }
  }), s && u.push({
    t: ce.INSERT,
    body: s,
    len: s.dataStream.length
  });
  const l = a + 1 + ((f = s == null ? void 0 : s.dataStream.length) != null ? f : 0);
  return u.selections = [{
    startOffset: l,
    endOffset: l,
    collapsed: !0
  }], u;
}
function d_(t) {
  const { ranges: e, rangeId: n, rangeType: r, wholeEntity: s, properties: i, body: o } = t;
  let a = 0;
  const u = new Ke();
  let c = !1;
  return e.forEach((l) => {
    var X, de, T;
    const h = c_(l, o);
    if (!h || !o)
      return !1;
    const { startOffset: d, endOffset: f } = h, E = (X = o.customRanges) != null ? X : [], R = (A, H, Z) => {
      var y, M, b, w;
      const fe = rl(A, H, E, r), ae = Math.min((M = (y = fe[0]) == null ? void 0 : y.startIndex) != null ? M : 1 / 0, A), m = Math.max((w = (b = fe[fe.length - 1]) == null ? void 0 : b.endIndex) != null ? w : -1 / 0, H), j = {
        rangeId: Z ? `${n}$${Z}` : n,
        rangeType: r,
        startIndex: 0,
        endIndex: m - ae,
        wholeEntity: s,
        properties: {
          ...i
        }
      };
      u.push({
        t: ce.RETAIN,
        len: ae - a
      }), u.push({
        t: ce.RETAIN,
        len: m - ae + 1,
        body: {
          dataStream: "",
          customRanges: [j]
        },
        coverType: Pe.COVER
      }), a = m + 1;
    }, O = ((de = o.paragraphs) != null ? de : []).filter((A) => A.startIndex < f && A.startIndex > d), U = ((T = o.customBlocks) != null ? T : []).filter((A) => A.startIndex < f && A.startIndex > d);
    l_([d, f - 1], [...O.map((A) => A.startIndex), ...U.map((A) => A.startIndex)]).forEach(([A, H], Z) => R(A, H, Z)), c = !0, u.selections = [{
      startOffset: h.endOffset,
      endOffset: h.endOffset,
      collapsed: !0
    }];
  }), c ? u : !1;
}
function sl(t, e, n = 0, r = null, s = !0) {
  t.sort((c, l) => c.startOffset - l.startOffset);
  const i = [], { paragraphs: o = [] } = e, a = o == null ? void 0 : o.find(
    (c) => c.startIndex >= t[0].startOffset && c.startIndex < t[0].endOffset
  );
  let u = n;
  if (t.forEach((c) => {
    const { startOffset: l, endOffset: h } = c;
    l > u && (i.push({
      t: ce.RETAIN,
      len: l - u
    }), u = l), u < h && (i.push({
      t: ce.DELETE,
      len: h - u
    }), u = h);
  }), r && i.push({
    t: ce.INSERT,
    body: r,
    len: r.dataStream.length
  }), a && s) {
    const c = o.find((l) => l.startIndex - n >= t[t.length - 1].endOffset - 1);
    c && (c.startIndex > u && (i.push({
      t: ce.RETAIN,
      len: c.startIndex - u
    }), u = c.startIndex), i.push({
      t: ce.RETAIN,
      len: 1,
      body: {
        dataStream: "",
        paragraphs: [
          {
            ...c,
            startIndex: 0,
            bullet: a == null ? void 0 : a.bullet
          }
        ]
      },
      coverType: Pe.REPLACE
    }));
  }
  return i;
}
function f_(t, e, n = 0) {
  const r = [];
  let s = n;
  return t.forEach((i) => {
    const { startOffset: o, endOffset: a } = i;
    o > s && (r.push({
      t: ce.RETAIN,
      len: o - s
    }), s = o), a > s && (r.push({
      t: ce.RETAIN,
      len: a - s,
      body: {
        ...re.deepClone(e),
        dataStream: ""
      }
    }), s = a);
  }), r;
}
const g_ = (t) => {
  var h;
  const { selection: e, body: n, doc: r } = t, s = e.segmentId, i = (h = r.getSelfOrHeaderFooterModel(s)) == null ? void 0 : h.getBody();
  if (!i) return !1;
  const o = e.collapsed ? null : Dt(i, e.startOffset, e.endOffset), a = ru(o ? o.dataStream : "", n.dataStream);
  let u = 0;
  const c = a.map(([d, f]) => {
    switch (d) {
      // retain
      case 0: {
        const E = {
          t: ce.RETAIN,
          body: {
            ...Dt(n, u, u + f.length, !1),
            dataStream: ""
          },
          len: f.length
        };
        return u += f.length, E;
      }
      // insert
      case 1: {
        const E = {
          t: ce.INSERT,
          body: Dt(n, u, u + f.length),
          len: f.length
        };
        return u += f.length, E;
      }
      // delete
      default:
        return {
          t: ce.DELETE,
          len: f.length
        };
    }
  }), l = new Ke();
  return l.push({
    t: ce.RETAIN,
    len: e.startOffset
  }), l.push(...c), l;
};
function p_(t, e) {
  return !!((t == null ? void 0 : t.length) === (e == null ? void 0 : e.length) && (t != null && t.every((n, r) => JSON.stringify(n) === JSON.stringify(e == null ? void 0 : e[r]))));
}
const m_ = (t) => {
  var h;
  const { selection: e, body: n, doc: r } = t, s = e.segmentId, i = (h = r.getSelfOrHeaderFooterModel(s)) == null ? void 0 : h.getBody();
  if (!i) return !1;
  const o = e.collapsed ? null : Dt(i, e.startOffset, e.endOffset), a = ru(o ? o.dataStream : "", n.dataStream);
  let u = 0;
  const c = a.map(([d, f]) => {
    switch (d) {
      // retain
      case 0: {
        const E = ei(n, u, u + f.length, !1), R = ei(o, u, u + f.length, !1), O = {
          t: ce.RETAIN,
          body: p_(E, R) ? void 0 : {
            textRuns: E,
            dataStream: ""
          },
          len: f.length
        };
        return u += f.length, O;
      }
      // insert
      case 1: {
        const E = {
          t: ce.INSERT,
          body: Dt(n, u, u + f.length),
          len: f.length
        };
        return u += f.length, E;
      }
      // delete
      default:
        return {
          t: ce.DELETE,
          len: f.length
        };
    }
  });
  if (c.every((d) => d.t === ce.RETAIN && !d.body))
    return !1;
  const l = new Ke();
  return l.push({
    t: ce.RETAIN,
    len: e.startOffset
  }), l.push(...c), l;
};
function __(t, e) {
  const n = [], { customBlocks: r = [] } = t;
  for (const s of e) {
    const { startOffset: i, endOffset: o } = s;
    if (!(i == null || o == null))
      for (const a of r) {
        const { startIndex: u } = a;
        u >= i && u < o && n.push(a.blockId);
      }
  }
  return n;
}
function E_(t, e = "") {
  if (!e)
    return ["body"];
  const { headers: n, footers: r } = t.getSnapshot();
  if (n == null && r == null)
    throw new Error("Document data model must have headers or footers when update by segment id");
  if ((n == null ? void 0 : n[e]) != null)
    return ["headers", e, "body"];
  if ((r == null ? void 0 : r[e]) != null)
    return ["footers", e, "body"];
  throw new Error("Segment id not found in headers or footers");
}
const C_ = (t) => {
  var R, O, U, ne;
  const { selection: e, documentDataModel: n, drawings: r } = t, { collapsed: s, startOffset: i, segmentId: o } = e, a = new Ke(), u = tn.getInstance(), c = [], l = n.getSelfOrHeaderFooterModel(o).getBody();
  if (!l)
    return !1;
  const h = (O = (R = n.getSnapshot().drawingsOrder) == null ? void 0 : R.length) != null ? O : 0;
  let d = 0;
  if (s)
    i > 0 && a.push({
      t: ce.RETAIN,
      len: i
    });
  else {
    const X = sl([e], l, 0, null, !1);
    a.push(...X);
    const de = __(l, [e]), T = (U = n.getDrawings()) != null ? U : {}, A = (ne = n.getDrawingsOrder()) != null ? ne : [], H = de.sort((Z, fe) => A.indexOf(Z) > A.indexOf(fe) ? -1 : A.indexOf(Z) < A.indexOf(fe) ? 1 : 0);
    if (H.length > 0)
      for (const Z of H) {
        const fe = T[Z], ae = A.indexOf(Z);
        if (fe == null || ae < 0)
          continue;
        const m = u.removeOp(["drawings", Z], fe), j = u.removeOp(["drawingsOrder", ae], Z);
        c.push(m), c.push(j), d++;
      }
  }
  a.push({
    t: ce.INSERT,
    body: {
      dataStream: "\b".repeat(r.length),
      customBlocks: r.map((X, de) => ({
        startIndex: de,
        blockId: X.drawingId
      }))
    },
    len: r.length
  });
  const f = E_(n, o), E = u.editOp(a.serialize(), f);
  c.push(E);
  for (const X of r) {
    const { drawingId: de } = X, T = u.insertOp(["drawings", de], X), A = u.insertOp(["drawingsOrder", h - d], de);
    c.push(T), c.push(A);
  }
  return c.reduce((X, de) => tn.compose(X, de), null);
}, R_ = (t) => {
  var h, d, f;
  const { paragraphs: e, segmentId: n, document: r } = t;
  let s = t.listType;
  const i = (d = (h = r.getSelfOrHeaderFooterModel(n).getBody()) == null ? void 0 : h.paragraphs) != null ? d : [], o = e.every((E) => {
    var R;
    return ((R = E.bullet) == null ? void 0 : R.listType.indexOf(s)) === 0;
  });
  let u = re.generateRandomId(6);
  if (e.length === 1) {
    const E = i.indexOf(e[0]), R = i[E - 1], O = i[E + 1];
    R && R.bullet && R.bullet.listType.indexOf(s) === 0 ? (u = R.bullet.listId, s !== Ft.CHECK_LIST && (s = R.bullet.listType)) : O && O.bullet && O.bullet.listType.indexOf(s) === 0 && (u = O.bullet.listId, s !== Ft.CHECK_LIST && (s = O.bullet.listType));
  }
  const c = new lr();
  c.reset();
  const l = new Ke();
  for (const E of e) {
    const { startIndex: R, paragraphStyle: O = {}, bullet: U } = E;
    l.push({
      t: ce.RETAIN,
      len: R - c.cursor
    }), l.push({
      t: ce.RETAIN,
      len: 1,
      body: {
        dataStream: "",
        paragraphs: [
          o ? {
            paragraphStyle: O,
            startIndex: 0
          } : {
            startIndex: 0,
            paragraphStyle: {
              ...O
            },
            bullet: {
              nestingLevel: (f = U == null ? void 0 : U.nestingLevel) != null ? f : 0,
              textStyle: {
                fs: 20
              },
              listType: s,
              listId: u
            }
          }
        ]
      },
      coverType: Pe.REPLACE
    }), c.moveCursorTo(R + 1);
  }
  return l;
}, I_ = (t) => {
  var h;
  const { paragraphIndex: e, segmentId: n, document: r } = t, s = (h = r.getSelfOrHeaderFooterModel(n).getBody()) == null ? void 0 : h.paragraphs;
  if (s == null)
    return !1;
  const i = s.find((d) => d.startIndex === e);
  if (!(i != null && i.bullet) || i.bullet.listType.indexOf(Ft.CHECK_LIST) === -1)
    return !1;
  const o = new lr();
  o.reset();
  const a = new Ke(), { startIndex: u, paragraphStyle: c = {} } = i, l = i.bullet.listType === Ft.CHECK_LIST ? Ft.CHECK_LIST_CHECKED : Ft.CHECK_LIST;
  return a.push({
    t: ce.RETAIN,
    len: u - o.cursor
  }), a.push({
    t: ce.RETAIN,
    len: 1,
    body: {
      dataStream: "",
      paragraphs: [
        {
          ...i,
          paragraphStyle: c,
          startIndex: 0,
          bullet: {
            ...i.bullet,
            listType: l
          }
        }
      ]
    },
    coverType: Pe.REPLACE
  }), o.moveCursorTo(u + 1), a;
}, v_ = (t) => {
  var l, h;
  const { paragraphs: e, listType: n, segmentId: r, document: s } = t;
  if (((l = s.getSelfOrHeaderFooterModel(r).getBody()) == null ? void 0 : l.paragraphs) == null)
    return !1;
  const a = re.generateRandomId(6), u = new lr();
  u.reset();
  const c = new Ke();
  for (const d of e) {
    const { startIndex: f, paragraphStyle: E = {}, bullet: R } = d;
    c.push({
      t: ce.RETAIN,
      len: f - u.cursor
    }), c.push({
      t: ce.RETAIN,
      len: 1,
      body: {
        dataStream: "",
        paragraphs: [
          {
            startIndex: 0,
            paragraphStyle: E,
            bullet: {
              nestingLevel: (h = R == null ? void 0 : R.nestingLevel) != null ? h : 0,
              textStyle: (R == null ? void 0 : R.listType) === n ? R.textStyle : {
                fs: 20
              },
              listType: n,
              listId: a
            }
          }
        ]
      },
      coverType: Pe.REPLACE
    }), u.moveCursorTo(f + 1);
  }
  return c;
};
function y_(t, e) {
  return e.some((n) => t.startIndex > n.startIndex && t.startIndex < n.endIndex);
}
const w_ = (t) => {
  var l, h, d;
  const { paragraphs: e, segmentId: n, document: r, type: s } = t, i = new lr();
  i.reset();
  const o = new Ke(), a = (l = r.getSnapshot().lists) != null ? l : {}, u = (d = (h = r.getBody()) == null ? void 0 : h.tables) != null ? d : [], c = {
    ...Es,
    ...a
  };
  for (const f of e) {
    const { startIndex: E, paragraphStyle: R = {}, bullet: O } = f, U = y_(f, u);
    if (o.push({
      t: ce.RETAIN,
      len: E - i.cursor
    }), O) {
      const ne = O.listType;
      let X = c[ne].nestingLevel.length - 1;
      U && (X = Math.min(X, 2)), o.push({
        t: ce.RETAIN,
        len: 1,
        body: {
          dataStream: "",
          paragraphs: [
            {
              startIndex: 0,
              paragraphStyle: {
                ...R
              },
              bullet: {
                ...O,
                nestingLevel: Math.max(Math.min(O.nestingLevel + s, X), 0)
              }
            }
          ]
        },
        coverType: Pe.REPLACE
      });
    } else
      o.push({
        t: ce.RETAIN,
        len: 1
      });
    i.moveCursorTo(E + 1);
  }
  return o;
};
var O_ = /* @__PURE__ */ ((t) => (t.PARAGRAPH = "PARAGRAPH", t.SECTION_BREAK = "SECTION_BREAK", t.TABLE = "TABLE", t.TABLE_ROW = "TABLE_ROW", t.TABLE_CELL = "TABLE_CELL", t.CUSTOM_BLOCK = "CUSTOM_BLOCK", t))(O_ || {}), ln = /* @__PURE__ */ ((t) => (t.PARAGRAPH = "\r", t.SECTION_BREAK = `
`, t.TABLE_START = "", t.TABLE_ROW_START = "\x1B", t.TABLE_CELL_START = "", t.TABLE_CELL_END = "", t.TABLE_ROW_END = "", t.TABLE_END = "", t.CUSTOM_RANGE_START = "", t.CUSTOM_RANGE_END = "", t.COLUMN_BREAK = "\v", t.PAGE_BREAK = "\f", t.DOCS_END = "\0", t.TAB = "	", t.CUSTOM_BLOCK = "\b", t.LETTER = "", t.SPACE = " ", t))(ln || {});
function eR(t) {
  return `${t}`;
}
const b_ = [
  // DataStreamTreeTokenType.PARAGRAPH, // 段落
  // DataStreamTreeTokenType.SECTION_BREAK, // 章节
  ln.TABLE_START,
  // 表格开始
  ln.TABLE_ROW_START,
  // 表格开始
  ln.TABLE_CELL_START,
  // 表格开始
  ln.TABLE_CELL_END,
  // 表格开始
  ln.TABLE_ROW_END,
  // 表格开始
  ln.TABLE_END
  // 表格结束
  // DataStreamTreeTokenType.COLUMN_BREAK, // 换列
  // DataStreamTreeTokenType.PAGE_BREAK, // 换页
  // DataStreamTreeTokenType.DOCS_END, // 文档结尾
  // DataStreamTreeTokenType.TAB, // 制表符
  // DataStreamTreeTokenType.CUSTOM_BLOCK, // 图片 mention 等不参与文档流的场景
], il = (t) => {
  const e = t.endsWith(`\r
`) ? t.slice(0, -2) : t;
  return b_.reduce((n, r) => n.replaceAll(r, ""), e);
}, S_ = (t) => t ? il(t).replaceAll("\r", "") === "" : !0, A_ = (t) => {
  const e = t.replace(/\n/g, "\r"), n = [], r = [];
  let s = 0, i = "";
  const o = (u, c = !0) => {
    const l = e.slice(s, u);
    if (re.isLegalUrl(l)) {
      const h = qt(), d = `${l}`, f = {
        startIndex: s,
        endIndex: s + d.length - 1,
        rangeId: h,
        rangeType: mn.HYPERLINK,
        properties: {
          url: t
        }
      };
      r.push(f), i += d, s = u + 1, c && (i += "\r", n.push({ startIndex: u }));
    } else
      i += e.slice(s, u + 1), s = u + 1, c && n.push({ startIndex: u });
  };
  let a = 0;
  for (let u = 0; u < e.length; u++)
    e[u] === "\r" && (o(u), a = u);
  return (a !== e.length - 1 || e.length === 1) && o(e.length, !1), {
    dataStream: i,
    paragraphs: n,
    customRanges: r
  };
};
function N_(t, e) {
  if (typeof e > "u")
    return { startOffset: t, endOffset: t, collapsed: !0 };
  if (e < t)
    throw new Error(`Cannot make a doc selection when endOffset ${e} is less than startOffset ${t}.`);
  return { startOffset: t, endOffset: e, collapsed: t === e };
}
function T_(t) {
  const { startOffset: e, endOffset: n, collapsed: r } = t, s = Math.min(e, n), i = Math.max(e, n);
  return {
    startOffset: s,
    endOffset: i,
    collapsed: r
  };
}
function M_(t, e, n, r) {
  return Math.max(t, n) <= Math.min(e, r);
}
class st {
}
C(st, "customRange", {
  add: d_,
  delete: h_,
  copyCustomRange: u_,
  getCustomRangesInterestsWithSelection: a_,
  isIntersecting: nl
}), C(st, "customDecoration", {
  add: i_,
  delete: o_
}), C(st, "selection", {
  replace: g_,
  makeSelection: N_,
  normalizeSelection: T_,
  delete: sl,
  replaceTextRuns: m_,
  retain: f_
}), C(st, "range", {
  isIntersects: M_
}), C(st, "transform", {
  getPlainText: il,
  fromPlainText: A_,
  isEmptyDocument: S_
}), C(st, "paragraph", {
  bullet: {
    set: v_,
    switch: R_,
    toggleChecklist: I_,
    changeNestLevel: w_
  }
}), C(st, "drawing", {
  add: C_
});
function D_(t) {
  if (t.customRanges || (t.customRanges = []), !t.paragraphs) {
    t.paragraphs = [];
    for (let e = 0; e < t.dataStream.length; e++)
      t.dataStream[e] === "\r" && t.paragraphs.push({ startIndex: e });
  }
  return t.customBlocks || (t.customBlocks = []), t.textRuns || (t.textRuns = []), t.customDecorations || (t.customDecorations = []), t.sectionBreaks || (t.sectionBreaks = []), t.tables || (t.tables = []), t;
}
function ol(t) {
  var e;
  return t.body = D_((e = t.body) != null ? e : { dataStream: "" }), t.drawingsOrder || (t.drawingsOrder = []), t.drawings || (t.drawings = {}), t.documentStyle || (t.documentStyle = {}), t;
}
class cr {
  /**
   * Creates a new TextStyleValue instance
   * @param {ITextStyle} style The initial style object
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style);
   * ```
   */
  constructor(e = {}) {
    C(this, "_style");
    this._style = e;
  }
  /**
   * Creates an instance of TextStyleValue.
   * @param {ITextStyle} style style object
   * @returns {TextStyleValue} font style instance
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style);
   * ```
   */
  static create(e = {}) {
    return new cr(e);
  }
  /**
   * Gets the font family
   * @returns {Nullable<string>} The font family name or undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.fontFamily);
   * ```
   */
  get fontFamily() {
    return this._style.ff;
  }
  /**
   * Gets the font size in points
   * @returns {number | undefined} The font size or undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.fontSize);
   * ```
   */
  get fontSize() {
    return this._style.fs;
  }
  /**
   * Gets whether the text is italic
   * @returns {boolean} True if italic, false otherwise
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.italic);
   * ```
   */
  get italic() {
    return this._style.it === we.TRUE;
  }
  /**
   * Gets whether the text is bold
   * @returns {boolean} True if bold, false otherwise
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.bold);
   * ```
   */
  get bold() {
    return this._style.bl === we.TRUE;
  }
  /**
   * Gets the underline decoration
   * @returns {TextDecorationBuilder | undefined} The underline decoration or undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.underline);
   * ```
   */
  get underline() {
    return this._style.ul && Jt.create(this._style.ul);
  }
  /**
   * Gets the bottom border line decoration
   * @returns {TextDecorationBuilder | undefined} The bottom border line decoration or undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.bottomBorderLine);
   * ```
   */
  get bottomBorderLine() {
    return this._style.bbl && Jt.create(this._style.bbl);
  }
  /**
   * Gets the strikethrough decoration
   * @returns {TextDecorationBuilder | undefined} The strikethrough decoration or undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.strikethrough);
   * ```
   */
  get strikethrough() {
    return this._style.st && Jt.create(this._style.st);
  }
  /**
   * Gets the overline decoration
   * @returns {TextDecorationBuilder | undefined} The overline decoration or undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.overline);
   * ```
   */
  get overline() {
    return this._style.ol && Jt.create(this._style.ol);
  }
  /**
   * Gets the background color
   * @returns {Nullable<IColorStyle>} The background color or null/undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.background);
   * ```
   */
  get background() {
    return this._style.bg;
  }
  /**
   * Gets the border settings
   * @returns {Nullable<IBorderData>} The border settings or null/undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.border);
   * ```
   */
  get border() {
    return this._style.bd;
  }
  /**
   * Gets the text color
   * @returns {Nullable<IColorStyle>} The text color or null/undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.color);
   * ```
   */
  get color() {
    return this._style.cl;
  }
  /**
   * Gets the vertical alignment (subscript/superscript)
   * @returns {Nullable<BaselineOffset>} The vertical alignment or null/undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.verticalAlign);
   * ```
   */
  get verticalAlign() {
    return this._style.va;
  }
  /**
   * Gets the number format pattern
   * @returns {Nullable<{ pattern: string }>} The number format pattern or null/undefined
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.numberFormat);
   * ```
   */
  get numberFormat() {
    return this._style.n;
  }
  /**
   * Creates a copy of this font style as a builder
   * @returns {TextStyleBuilder} A new TextStyleBuilder instance with the same style
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * const copy = style.copy();
   * console.log(copy);
   * ```
   */
  copy() {
    return Qt.create(re.deepClone(this._style));
  }
  /**
   * Gets the raw style object
   * @returns {ITextStyle} The underlying style object
   * @example
   * ```ts
   * const style = TextStyleValue.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style.getValue());
   * ```
   */
  getValue() {
    return { ...this._style };
  }
}
class Qt extends cr {
  /**
   * Creates a new TextStyleBuilder instance
   * @param {ITextStyle} style Initial style object
   * @returns {TextStyleBuilder} A new TextStyleBuilder instance
   * @example
   * ```ts
   * const style = TextStyleBuilder.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style);
   * ```
   */
  static create(e = {}) {
    return new Qt(e);
  }
  /**
   * Creates a new TextStyleBuilder instance
   * @param {ITextStyle} style The initial style object
   * @example
   * ```ts
   * const style = new TextStyleBuilder({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * console.log(style);
   * ```
   */
  constructor(e = {}) {
    super(e);
  }
  /**
   * Sets the font family
   * @param {string} family The font family name
   * @returns {TextStyleBuilder} The builder instance for chaining
   * @example
   * ```ts
   * const style = TextStyleBuilder.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * style.setFontFamily('Times New Roman');
   * console.log(style.fontFamily);
   * ```
   */
  setFontFamily(e) {
    return this._style.ff = e, this;
  }
  /**
   * Sets the font size in points
   * @param {number} size The font size
   * @returns {TextStyleBuilder} The builder instance for chaining
   * @example
   * ```ts
   * const style = TextStyleBuilder.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * style.setFontSize(14);
   * console.log(style.fontSize);
   * ```
   */
  setFontSize(e) {
    return this._style.fs = e, this;
  }
  /**
   * Sets the italic style
   * @param {boolean} value True to make italic, false otherwise
   * @returns {TextStyleBuilder} The builder instance for chaining
   * @example
   * ```ts
   * const style = TextStyleBuilder.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * style.setItalic(true);
   * console.log(style.italic);
   * ```
   */
  setItalic(e) {
    return this._style.it = e ? 1 : 0, this;
  }
  /**
   * Sets the bold style
   * @param {boolean} value True to make bold, false otherwise
   * @returns {TextStyleBuilder} The builder instance for chaining
   * @example
   * ```ts
   * const style = TextStyleBuilder.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * style.setBold(true);
   * console.log(style.bold);
   * ```
   */
  setBold(e) {
    return this._style.bl = e ? 1 : 0, this;
  }
  /**
   * Sets the underline decoration
   * @param {TextDecorationBuilder} decoration The underline decoration settings
   * @returns {TextStyleBuilder} The builder instance for chaining
   * @example
   * ```ts
   * const style = TextStyleBuilder.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * style.setUnderline({ type: 'single', color: '#FF0000' });
   * console.log(style.underline);
   * ```
   */
  setUnderline(e) {
    return this._style.ul = e.build(), this;
  }
  /**
   * Sets the bottom border line decoration
   * @param {TextDecorationBuilder} decoration The bottom border line decoration settings
   * @returns {TextStyleBuilder} The builder instance for chaining
   * @example
   * ```ts
   * const style = TextStyleBuilder.create({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * style.setBottomBorderLine({ type: 'single', color: '#FF0000' });
   * console.log(style.bottomBorderLine);
   * ```
   */
  setBottomBorderLine(e) {
    return this._style.bbl = e.build(), this;
  }
  /**
   * Sets the strikethrough decoration
   * @param {TextDecorationBuilder} decoration The strikethrough decoration settings
   * @returns {TextStyleBuilder} The builder instance for chaining
   */
  setStrikethrough(e) {
    return this._style.st = e.build(), this;
  }
  /**
   * Sets the overline decoration
   * @param {TextDecorationBuilder} decoration The overline decoration settings
   * @returns {TextStyleBuilder} The builder instance for chaining
   */
  setOverline(e) {
    return this._style.ol = e.build(), this;
  }
  /**
   * Sets the background color
   * @param {IColorStyle | null} color The background color or null to remove
   * @returns {TextStyleBuilder} The builder instance for chaining
   */
  setBackground(e) {
    return this._style.bg = e, this;
  }
  /**
   * Sets the border settings
   * @param {IBorderData | null} border The border settings or null to remove
   * @returns {TextStyleBuilder} The builder instance for chaining
   */
  setBorder(e) {
    return this._style.bd = e, this;
  }
  /**
   * Sets the text color
   * @param {IColorStyle | null} color The text color or null to remove
   * @returns {TextStyleBuilder} The builder instance for chaining
   */
  setColor(e) {
    return this._style.cl = e, this;
  }
  /**
   * Sets the vertical alignment (subscript/superscript)
   * @param {BaselineOffset | null} offset The vertical alignment or null to remove
   * @returns {TextStyleBuilder} The builder instance for chaining
   */
  setVerticalAlign(e) {
    return this._style.va = e, this;
  }
  /**
   * Creates a copy of this font style builder
   * @returns {TextStyleBuilder} A new TextStyleBuilder instance with the same style
   */
  copy() {
    return Qt.create(re.deepClone(this._style));
  }
  /**
   * Builds and returns the final style object
   * @returns {ITextStyle} The complete style object
   */
  build() {
    return this.getValue();
  }
}
class Jt {
  /**
   * Creates a new TextDecorationBuilder instance
   * @param {ITextDecoration} decoration The initial decoration object
   * @example
   * ```ts
   * const decoration = new TextDecorationBuilder({ s: 1, t: TextDecoration.SINGLE });
   * ```
   */
  constructor(e = { s: 1 }) {
    C(this, "_decoration");
    this._decoration = e;
  }
  /**
   * Creates an instance of TextDecorationBuilder.
   * @param {ITextDecoration} decoration Initial decoration object
   * @returns {TextDecorationBuilder} text decoration builder instance
   * @example
   * ```ts
   * const decoration = TextDecorationBuilder.create({ s: 1, t: TextDecoration.SINGLE });
   * console.log(decoration);
   * ```
   */
  static create(e = { s: 1 }) {
    return new Jt(e);
  }
  /**
   * Gets whether the decoration is shown
   * @returns {boolean} True if the decoration is shown
   */
  get show() {
    return this._decoration.s === we.TRUE;
  }
  /**
   * Gets whether the decoration color follows the font color
   * @returns {boolean} True if the decoration color follows the font color
   */
  get followFontColor() {
    return this._decoration.c === we.TRUE;
  }
  /**
   * Gets the decoration color
   * @returns {Nullable<IColorStyle>} The decoration color
   */
  get color() {
    return this._decoration.cl;
  }
  /**
   * Gets the decoration line type
   * @returns {Nullable<TextDecoration>} The decoration line type
   */
  get type() {
    return this._decoration.t;
  }
  /**
   * Sets whether the decoration is shown
   * @param {boolean} value True to show the decoration
   * @returns {TextDecorationBuilder} The builder instance for chaining
   * @example
   * ```ts
   * decoration.setShow(true);
   * ```
   */
  setShow(e) {
    return this._decoration.s = e ? 1 : 0, this;
  }
  /**
   * Sets whether the decoration color follows the font color
   * @param {boolean} value True to follow font color
   * @returns {TextDecorationBuilder} The builder instance for chaining
   * @example
   * ```ts
   * decoration.setFollowFontColor(false);
   * ```
   */
  setFollowFontColor(e) {
    return this._decoration.c = e ? 1 : 0, this;
  }
  /**
   * Sets the decoration color
   * @param {IColorStyle} color The color style
   * @returns {TextDecorationBuilder} The builder instance for chaining
   * @example
   * ```ts
   * decoration.setColor({ rgb: '#FF0000' });
   * ```
   */
  setColor(e) {
    return this._decoration.cl = e, this;
  }
  /**
   * Sets the decoration line type
   * @param {TextDecoration} type The line type
   * @returns {TextDecorationBuilder} The builder instance for chaining
   * @example
   * ```ts
   * decoration.setLineType(TextDecoration.SINGLE);
   * ```
   */
  setLineType(e) {
    return this._decoration.t = e, this;
  }
  /**
   * Creates a copy of this text decoration builder
   * @returns {TextDecorationBuilder} A new TextDecorationBuilder instance with the same decoration
   * @example
   * ```ts
   * const copy = decoration.copy();
   * ```
   */
  copy() {
    return Jt.create(re.deepClone(this._decoration));
  }
  /**
   * Builds and returns the final decoration object
   * @returns {ITextDecoration} The complete text decoration object
   * @example
   * ```ts
   * const style = decoration.build();
   * ```
   */
  build() {
    return { ...this._decoration };
  }
}
class hr {
  constructor(e = {}) {
    C(this, "_style");
    this._style = e;
  }
  /**
   * Creates a new ParagraphStyleValue instance
   * @param {IParagraphStyle} style The initial style object
   * @returns A new ParagraphStyleValue instance
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * ```
   */
  static create(e = {}) {
    return new hr(e);
  }
  /**
   * Gets the first line indent
   * @returns {Nullable<INumberUnit>} The first line indent
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.indentFirstLine);
   * ```
   */
  get indentFirstLine() {
    return this._style.indentFirstLine;
  }
  /**
   * Gets the hanging indent
   * @returns {Nullable<INumberUnit>} The hanging indent
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.hanging);
   * ```
   */
  get hanging() {
    return this._style.hanging;
  }
  /**
   * Gets the indent start
   * @returns {Nullable<INumberUnit>} The indent start
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.indentStart);
   * ```
   */
  get indentStart() {
    return this._style.indentStart;
  }
  /**
   * Gets the indent end
   * @returns {Nullable<INumberUnit>} The indent end
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.indentEnd);
   * ```
   */
  get tabStops() {
    return this._style.tabStops;
  }
  /**
   * Gets the indent end
   * @returns {Nullable<INumberUnit>} The indent end
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.indentEnd);
   * ```
   */
  get indentEnd() {
    return this._style.indentEnd;
  }
  /**
   * Gets the text style
   * @returns {Nullable<ITextStyle>} The text style
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.textStyle);
   * ```
   */
  get textStyle() {
    return this._style.textStyle;
  }
  /**
   * Gets the heading id
   * @returns {Nullable<string>} The heading id
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.headingId);
   * ```
   */
  get headingId() {
    return this._style.headingId;
  }
  /**
   * Gets the named style type
   * @returns {Nullable<NamedStyleType>} The named style type
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.namedStyleType);
   * ```
   */
  get namedStyleType() {
    return this._style.namedStyleType;
  }
  /**
   * Gets the horizontal align
   * @returns {Nullable<HorizontalAlign>} The horizontal align
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.horizontalAlign);
   * ```
   */
  get horizontalAlign() {
    return this._style.horizontalAlign;
  }
  /**
   * Gets the line spacing
   * @returns {Nullable<number>} The line spacing
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.lineSpacing);
   * ```
   */
  get lineSpacing() {
    return this._style.lineSpacing;
  }
  /**
   * Gets the text direction
   * @returns {Nullable<TextDirection>} The text direction
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.direction);
   * ```
   */
  get direction() {
    return this._style.direction;
  }
  /**
   * Gets the spacing rule
   * @returns {Nullable<SpacingRule>} The spacing rule
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.spacingRule);
   * ```
   */
  get spacingRule() {
    return this._style.spacingRule;
  }
  /**
   * Gets the snap to grid
   * @returns {Nullable<BooleanNumber>} The snap to grid
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.snapToGrid);
   * ```
   */
  get snapToGrid() {
    return this._style.snapToGrid;
  }
  /**
   * Gets the space above
   * @returns {Nullable<INumberUnit>} The space above
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.spaceAbove);
   * ```
   */
  get spaceAbove() {
    return this._style.spaceAbove;
  }
  /**
   * Gets the space below
   * @returns {Nullable<INumberUnit>} The space below
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.spaceBelow);
   * ```
   */
  get spaceBelow() {
    return this._style.spaceBelow;
  }
  /**
   * Gets the border between
   * @returns {Nullable<IParagraphBorder>} The border between
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.borderBetween);
   * ```
   */
  get borderBetween() {
    return this._style.borderBetween;
  }
  /**
   * Gets the border top
   * @returns {Nullable<IParagraphBorder>} The border top
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.borderTop);
   * ```
   */
  get borderTop() {
    return this._style.borderTop;
  }
  /**
   * Gets the border bottom
   * @returns {Nullable<IParagraphBorder>} The border bottom
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.borderBottom);
   * ```
   */
  get borderBottom() {
    return this._style.borderBottom;
  }
  /**
   * Gets the border left
   * @returns {Nullable<IParagraphBorder>} The border left
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.borderLeft);
   * ```
   */
  get borderLeft() {
    return this._style.borderLeft;
  }
  /**
   * Gets the border right
   * @returns {Nullable<IParagraphBorder>} The border right
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.borderRight);
   * ```
   */
  get borderRight() {
    return this._style.borderRight;
  }
  /**
   * Gets the keep lines
   * @returns {boolean} The keep lines
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.keepLines);
   * ```
   */
  get keepLines() {
    return this._style.keepLines === we.TRUE;
  }
  /**
   * Gets the keep next
   * @returns {boolean} The keep next
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.keepNext);
   * ```
   */
  get keepNext() {
    return this._style.keepNext === we.TRUE;
  }
  /**
   * Gets the word wrap
   * @returns {boolean} The word wrap
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.wordWrap);
   * ```
   */
  get wordWrap() {
    return this._style.wordWrap === we.TRUE;
  }
  /**
   * Gets the widow control
   * @returns {boolean} The widow control
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.widowControl);
   * ```
   */
  get widowControl() {
    return this._style.widowControl === we.TRUE;
  }
  /**
   * Gets the shading
   * @returns {Nullable<IShading>} The shading
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.shading);
   * ```
   */
  get shading() {
    return this._style.shading;
  }
  /**
   * Gets the suppress hyphenation
   * @returns {boolean} The suppress hyphenation
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.suppressHyphenation);
   * ```
   */
  get suppressHyphenation() {
    return this._style.suppressHyphenation === we.TRUE;
  }
  /**
   * Creates a copy of the paragraph style
   * @returns {ParagraphStyleBuilder} The copy
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * ```
   */
  copy() {
    return nr.create(re.deepClone(this._style));
  }
  /**
   * Gets the value
   * @returns {IParagraphStyle} The value
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * console.log(style.getValue());
   * ```
   */
  getValue() {
    return this._style;
  }
}
class nr extends hr {
  /**
   * Creates a new paragraph style builder
   * @param style The paragraph style
   * @returns A new paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * ```
   */
  static create(e = {}) {
    return new nr(e);
  }
  constructor(e = {}) {
    super(e);
  }
  /**
   * Sets the indent first line
   * @param value The indent first line
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setIndentFirstLine(10);
   * ```
   */
  setIndentFirstLine(e) {
    return this._style.indentFirstLine = e, this;
  }
  /**
   * Sets the hanging
   * @param value The hanging
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setHanging(10);
   * ```
   */
  setHanging(e) {
    return this._style.hanging = e, this;
  }
  /**
   * Sets the indent start
   * @param value The indent start
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setIndentStart(10);
   * ```
   */
  setIndentStart(e) {
    return this._style.indentStart = e, this;
  }
  /**
   * Sets the tab stops
   * @param value The tab stops
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setTabStops([{ value: 10 }]);
   * ```
   */
  setTabStops(e) {
    return this._style.tabStops = e, this;
  }
  /**
   * Sets the indent end
   * @param value The indent end
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setIndentEnd(10);
   * ```
   */
  setIndentEnd(e) {
    return this._style.indentEnd = e, this;
  }
  /**
   * Sets the text style
   * @param value The text style
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setTextStyle({ ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE });
   * ```
   */
  setTextStyle(e) {
    return this._style.textStyle = e, this;
  }
  /**
   * Sets the heading id
   * @param value The heading id
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setHeadingId('test');
   * ```
   */
  setHeadingId(e) {
    return this._style.headingId = e, this;
  }
  /**
   * Sets the named style type
   * @param value The named style type
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setNamedStyleType(NamedStyleType.CHAPTER);
   * ```
   */
  setNamedStyleType(e) {
    return this._style.namedStyleType = e, this;
  }
  /**
   * Sets the vertical align
   * @param value The vertical align
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setVerticalAlign(VerticalAlign.CENTER);
   * ```
   */
  setHorizontalAlign(e) {
    return this._style.horizontalAlign = e, this;
  }
  /**
   * Sets the line spacing
   * @param value The line spacing
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setLineSpacing(10);
   * ```
   */
  setLineSpacing(e) {
    return this._style.lineSpacing = e, this;
  }
  /**
   * Sets the text direction
   * @param value The text direction
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setTextDirection(TextDirection.RIGHT_TO_LEFT);
   * ```
   */
  setDirection(e) {
    return this._style.direction = e, this;
  }
  /**
   * Sets the spacing rule
   * @param value The spacing rule
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setSpacingRule(SpacingRule.AUTO);
   * ```
   */
  setSpacingRule(e) {
    return this._style.spacingRule = e, this;
  }
  /**
   * Sets the snap to grid
   * @param value The snap to grid
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setSnapToGrid(true);
   * ```
   */
  setSnapToGrid(e) {
    return this._style.snapToGrid = e ? 1 : 0, this;
  }
  /**
   * Sets the space above
   * @param value The space above
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setSpaceAbove(10);
   * ```
   */
  setSpaceAbove(e) {
    return this._style.spaceAbove = e, this;
  }
  /**
   * Sets the space below
   * @param value The space below
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setSpaceBelow(10);
   * ```
   */
  setSpaceBelow(e) {
    return this._style.spaceBelow = e, this;
  }
  /**
   * Sets the border between
   * @param {IParagraphBorder} value The border between
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setBorderBetween({ color: 'red', width: 1 });
   * ```
   */
  setBorderBetween(e) {
    return this._style.borderBetween = e, this;
  }
  /**
   * Sets the border top
   * @param {IParagraphBorder} value The border top
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setBorderTop({ color: 'red', width: 1 });
   * ```
   */
  setBorderTop(e) {
    return this._style.borderTop = e, this;
  }
  /**
   * Sets the border bottom
   * @param {IParagraphBorder} value The border bottom
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setBorderBottom({ color: 'red', width: 1 });
   * ```
   */
  setBorderBottom(e) {
    return this._style.borderBottom = e, this;
  }
  /**
   * Sets the border left
   * @param {IParagraphBorder} value The border left
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setBorderLeft({ color: 'red', width: 1 });
   * ```
   */
  setBorderLeft(e) {
    return this._style.borderLeft = e, this;
  }
  /**
   * Sets the border right
   * @param {IParagraphBorder} value The border right
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setBorderRight({ color: 'red', width: 1 });
   * ```
   */
  setBorderRight(e) {
    return this._style.borderRight = e, this;
  }
  /**
   * Sets the keep lines
   * @param value The keep lines
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setKeepLines(true);
   * ```
   */
  setKeepLines(e) {
    return this._style.keepLines = e ? 1 : 0, this;
  }
  /**
   * Sets the keep next
   * @param value The keep next
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setKeepNext(true);
   * ```
   */
  setKeepNext(e) {
    return this._style.keepNext = e ? 1 : 0, this;
  }
  /**
   * Sets the word wrap
   * @param value The word wrap
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setWordWrap(true);
   * ```
   */
  setWordWrap(e) {
    return this._style.wordWrap = e ? 1 : 0, this;
  }
  /**
   * Sets the widow control
   * @param {boolean} value The widow control value
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setWidowControl(true);
   * ```
   */
  setWidowControl(e) {
    return this._style.widowControl = e ? 1 : 0, this;
  }
  /**
   * Sets the shading style
   * @param {IShading} value The shading configuration
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setShading({ backgroundColor: '#f0f0f0' });
   * ```
   */
  setShading(e) {
    return this._style.shading = e, this;
  }
  /**
   * Sets whether to suppress hyphenation
   * @param {boolean} value The suppress hyphenation value
   * @returns {ParagraphStyleBuilder} The paragraph style builder
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * copy.setSuppressHyphenation(true);
   * ```
   */
  setSuppressHyphenation(e) {
    return this._style.suppressHyphenation = e ? 1 : 0, this;
  }
  /**
   * Creates a copy of the current paragraph style builder
   * @returns {ParagraphStyleBuilder} A new instance of ParagraphStyleBuilder with the same settings
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const copy = style.copy();
   * ```
   */
  copy() {
    return nr.create(re.deepClone(this._style));
  }
  /**
   * Builds and returns the final paragraph style configuration
   * @returns {IParagraphStyle} The constructed paragraph style object
   * @example
   * ```ts
   * const style = ParagraphStyleValue.create({ textStyle: { ff: 'Arial', fs: 12, it: univerAPI.Enum.BooleanNumber.TRUE, bl: univerAPI.Enum.BooleanNumber.TRUE } });
   * const finalStyle = style.build();
   * ```
   */
  build() {
    return this.getValue();
  }
}
class Zt {
  constructor(e) {
    C(this, "_data");
    if (!e.body)
      throw new Error("Invalid document data, body is required");
    this._data = ol(e);
  }
  /**
   * Creates a new RichTextValue instance
   * @param {IDocumentData} data The initial data for the rich text value
   * @returns {RichTextValue} A new RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * ```
   */
  static create(e) {
    return new Zt(e);
  }
  /**
   * Creates a new RichTextValue instance
   * @param {IDocumentBody} data The initial data for the rich text value
   * @returns {RichTextValue} A new RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.createByBody({ dataStream: 'Hello World\r\n' });
   * ```
   */
  static createByBody(e) {
    return new Zt({ body: e, id: "d", documentStyle: {} });
  }
  /**
   * Creates a copy of the current RichTextValue instance
   * @returns {RichTextValue} A new instance of RichTextValue with the same data
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const copy = richText.copy();
   * ```
   */
  copy() {
    return gn.create(re.deepClone(this._data));
  }
  /**
   * Slices the current RichTextValue instance
   * @param {number} start The start index
   * @param {number} end The end index
   * @returns {RichTextBuilder} A new instance of RichTextBuilder with the sliced data
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const sliced = richText.slice(0, 5);
   * ```
   */
  slice(e, n) {
    const { body: r, ...s } = this._data;
    return gn.create({
      ...re.deepClone(s),
      body: Dt(r, e, n)
    });
  }
  /**
   * Converts the current RichTextValue instance to plain text
   * @returns {string} The plain text representation of the current RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const plainText = richText.toPlainText();
   * ```
   */
  toPlainText() {
    var e, n;
    return st.transform.getPlainText((n = (e = this._data.body) == null ? void 0 : e.dataStream) != null ? n : "").replaceAll("\r", `
`);
  }
  /**
   * Gets the paragraph style of the current RichTextValue instance
   * @returns {ParagraphStyleValue} The paragraph style of the current RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const style = richText.getParagraphStyle();
   * ```
   */
  getParagraphStyle() {
    var e, n;
    return hr.create((n = (e = this._data.body) == null ? void 0 : e.paragraphs) == null ? void 0 : n[0].paragraphStyle);
  }
  /**
   * Gets the paragraph bullet of the current RichTextValue instance
   * @returns {ParagraphBulletValue} The paragraph bullet of the current RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const bullet = richText.getParagraphBullet();
   * ```
   */
  getParagraphBullet() {
    var e, n;
    return (n = (e = this._data.body) == null ? void 0 : e.paragraphs) == null ? void 0 : n[0].bullet;
  }
  /**
   * Gets the paragraphs of the current RichTextValue instance
   * @returns {RichTextValue[]} The paragraphs of the current RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const paragraphs = richText.getParagraphs();
   * ```
   */
  getParagraphs() {
    var r, s;
    const e = (s = (r = this._data.body) == null ? void 0 : r.paragraphs) != null ? s : [];
    let n = 0;
    return e.map((i) => {
      const o = this.slice(n, i.startIndex);
      return n = i.startIndex, o;
    });
  }
  /**
   * Gets the text runs of the current RichTextValue instance
   * @returns {TextRunValue[]} The text runs of the current RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const textRuns = richText.getTextRuns();
   * ```
   */
  getTextRuns() {
    var e, n;
    return ((n = (e = this._data.body) == null ? void 0 : e.textRuns) != null ? n : []).map((r) => ({
      ...r,
      ts: r.ts ? cr.create(r.ts) : null
    }));
  }
  /**
   * Gets the links of the current RichTextValue instance
   * @returns {ICustomRange[]} The links of the current RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const links = richText.getLinks();
   * ```
   */
  getLinks() {
    var e, n, r;
    return (r = (n = (e = this._data.body) == null ? void 0 : e.customRanges) == null ? void 0 : n.filter((s) => s.rangeType === mn.HYPERLINK)) != null ? r : [];
  }
  /**
   * Gets the data of the current RichTextValue instance
   * @returns {IDocumentData} The data of the current RichTextValue instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const data = richText.getData();
   * ```
   */
  getData() {
    return this._data;
  }
}
class gn extends Zt {
  constructor(n) {
    super(n);
    C(this, "_doc");
    this._doc = new jt(n);
  }
  static newEmptyData() {
    return ol({
      id: "d",
      documentStyle: {},
      drawings: {},
      drawingsOrder: [],
      body: {
        dataStream: `\r
`,
        customBlocks: [],
        customRanges: [],
        paragraphs: [{ startIndex: 0 }],
        textRuns: [],
        tables: [],
        sectionBreaks: []
      }
    });
  }
  /**
   * Creates a new RichTextBuilder instance
   * @param {IDocumentData} data The initial data for the rich text builder
   * @returns {RichTextBuilder} A new RichTextBuilder instance
   */
  static create(n) {
    return new gn(n != null ? n : gn.newEmptyData());
  }
  insertText(n, r, s) {
    var l, h;
    let i = ((h = (l = this._data.body) == null ? void 0 : l.dataStream.length) != null ? h : 2) - 2, o, a;
    if (typeof n == "string" ? o = n : (i = Math.min(n, i), o = r), typeof r == "object" ? a = r instanceof Qt ? r.build() : r : a = s instanceof Qt ? s.build() : s, !o) return this;
    const u = {
      dataStream: o,
      textRuns: a ? [
        {
          ts: a,
          st: i,
          ed: i + o.length
        }
      ] : []
    }, c = st.selection.replace({
      doc: this._doc,
      selection: { startOffset: i, endOffset: i, collapsed: !0 },
      body: u
    });
    if (!c)
      throw new Error("Insert text failed, please check.");
    return Ke.apply(this._doc.getBody(), c.serialize()), this;
  }
  insertRichText(n, r) {
    var a, u;
    let s = ((u = (a = this._data.body) == null ? void 0 : a.dataStream.length) != null ? u : 2) - 2, i;
    typeof n == "object" ? i = n instanceof Zt ? n.getData() : n : (s = Math.min(n, s), i = r instanceof Zt ? r.getData() : r);
    const o = st.selection.replace({
      doc: this._doc,
      selection: { startOffset: s, endOffset: s, collapsed: !0 },
      body: i.body
    });
    if (!o)
      throw new Error("Insert text failed, please check.");
    return Ke.apply(this._doc.getBody(), o.serialize()), this;
  }
  delete(n, r) {
    if (r !== void 0) {
      if (!r) return this;
      const s = st.selection.delete([{ startOffset: n, endOffset: n + r, collapsed: !0 }], this._data.body);
      Ke.apply(this._doc.getBody(), s);
    }
    return this;
  }
  /**
   * Sets the style of the text at the specified start and end positions
   * @param {number} start The start position of the text to set the style
   * @param {number} end The end position of the text to set the style
   * @param {TextStyleBuilder | ITextStyle} style The style to set
   * @returns {RichTextBuilder} The current RichTextBuilder instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const newRichText = richText.setStyle(5, 10, { ff: 'Arial', fs: 12 });
   * ```
   */
  setStyle(n, r, s) {
    const i = {
      dataStream: "",
      textRuns: [{
        ts: s instanceof Qt ? s.build() : s,
        st: 0,
        ed: r - n
      }]
    }, o = st.selection.retain([{ startOffset: n, endOffset: r, collapsed: !0 }], i);
    return Ke.apply(this._doc.getBody(), o), this;
  }
  /**
   * Sets the link of the text at the specified start and end positions
   * @param {number} start The start position of the text to set the link
   * @param {number} end The end position of the text to set the link
   * @param {string} link The link to set
   * @returns {RichTextBuilder} The current RichTextBuilder instance
   * @example
   * ```ts
   * const richText = RichTextValue.create({ body: { dataStream: 'Hello World\r\n' } });
   * const newRichText = richText.setLink(5, 10, 'https://www.example.com');
   * ```
   */
  setLink(n, r, s) {
    const i = st.customRange.add({
      rangeType: mn.HYPERLINK,
      rangeId: qt(),
      properties: {
        url: s
      },
      ranges: [{ startOffset: n, endOffset: r, collapsed: !1 }],
      body: this._data.body
    });
    if (!i)
      throw new Error("Insert text failed, please check.");
    return Ke.apply(this._doc.getBody(), i.serialize()), this;
  }
  cancelLink(n, r) {
    if (typeof n == "string") {
      const s = st.customRange.delete({
        rangeId: n,
        documentDataModel: this._doc
      });
      if (!s)
        throw new Error("Insert text failed, please check.");
      Ke.apply(this._doc.getBody(), s.serialize());
    } else
      this.slice(n, r).getLinks().forEach((i) => {
        const o = st.customRange.delete({
          rangeId: i.rangeId,
          documentDataModel: this._doc
        });
        if (!o)
          throw new Error("Insert text failed, please check.");
        Ke.apply(this._doc.getBody(), o.serialize());
      });
    return this;
  }
  updateLink(n, r) {
    var i, o;
    const s = (o = (i = this._data.body) == null ? void 0 : i.customRanges) == null ? void 0 : o.find((a) => a.rangeId === n);
    if (!s)
      throw new Error("Link not found");
    return s.properties.url = r, this;
  }
  insertParagraph(n, r) {
    var o, a;
    let s, i;
    return typeof n == "object" ? (s = {
      dataStream: "\r",
      paragraphs: [{
        startIndex: 0,
        paragraphStyle: n.build()
      }]
    }, i = ((a = (o = this._data.body) == null ? void 0 : o.dataStream.length) != null ? a : 2) - 2) : (i = n, s = {
      dataStream: "\r",
      paragraphs: [{
        startIndex: 0,
        paragraphStyle: r == null ? void 0 : r.build()
      }]
    }), this.insertRichText(i, Zt.create({ body: s, id: "d", documentStyle: {} })), this;
  }
  insertLink(n, r, s) {
    let i = "", o = "";
    typeof n == "string" ? (i = n, o = r) : (i = r, o = s);
    const a = gn.createByBody({
      dataStream: i,
      customRanges: [{
        rangeType: mn.HYPERLINK,
        rangeId: qt(),
        properties: {
          url: o
        },
        startIndex: 0,
        endIndex: i.length - 1
      }]
    });
    return typeof n == "number" ? this.insertRichText(n, a) : this.insertRichText(a);
  }
}
function tR(t, e = 16) {
  let n = 0, r = null;
  return function(...i) {
    const o = Date.now();
    o - n < e ? (r && clearTimeout(r), r = setTimeout(() => {
      n = o, t.apply(this, i);
    }, e)) : (n = o, t.apply(this, i));
  };
}
var Vn = /* @__PURE__ */ ((t) => (t[t.Style = 1] = "Style", t[t.Value = 2] = "Value", t))(Vn || {});
function nR(t) {
  return `sheet_interceptor_${t}`;
}
const x_ = (t) => function(e, n) {
  let r = -1, s = e;
  for (let i = 0; i <= t.length; i++) {
    if (i <= r)
      throw new Error("[SheetInterceptorService]: next() called multiple times!");
    if (r = i, i === t.length)
      return s;
    const o = t[i];
    let a = !1;
    if (s = o.handler(s, n, (u) => (a = !0, u)), !a)
      break;
  }
  return s;
};
class rR {
  constructor(e) {
    C(this, "_interceptorsByName", /* @__PURE__ */ new Map());
    C(this, "_interceptorPoints");
    this._interceptorPoints = e;
  }
  /**
   * Get the interceptors.
   * @param name Name of the intercepted point.
   * @param filter A callback function to filter the interceptors.
   * @returns It will return a composed interceptor function. If you will perform the interceptor repeatedly,
   * you should cache the result instead of calling this function multiple times.
   */
  fetchThroughInterceptors(e, n) {
    const r = e;
    let s = this._interceptorsByName.get(r);
    return n && (s = s.filter(n)), x_(s || []);
  }
  intercept(e, n) {
    const r = e;
    this._interceptorsByName.has(r) || this._interceptorsByName.set(r, []);
    const s = this._interceptorsByName.get(r);
    return s.push(n), this._interceptorsByName.set(
      r,
      s.sort((i, o) => {
        var a, u;
        return ((a = o.priority) != null ? a : 0) - ((u = i.priority) != null ? u : 0);
      })
      // from large to small
    ), () => cs(this._interceptorsByName.get(r), n);
  }
  getInterceptPoints() {
    return this._interceptorPoints;
  }
  dispose() {
    this._interceptorsByName.clear();
  }
}
function sR(t) {
  return `sheet_async_interceptor_${t}`;
}
const L_ = (t) => async function(e, n) {
  let r = -1, s = e;
  for (let i = 0; i <= t.length; i++) {
    if (i <= r)
      throw new Error("[SheetInterceptorService]: next() called multiple times!");
    if (r = i, i === t.length)
      return s;
    const o = t[i];
    let a = !1;
    if (s = await o.handler(s, n, async (u) => (a = !0, u)), !a)
      break;
  }
  return s;
};
class iR {
  constructor(e) {
    C(this, "_asyncInterceptorsByName", /* @__PURE__ */ new Map());
    C(this, "_asyncInterceptorPoints");
    this._asyncInterceptorPoints = e;
  }
  /**
   * Get the interceptors.
   * @param name Name of the intercepted point.
   * @param filter A callback function to filter the interceptors.
   * @returns It will return a composed interceptor function. If you will perform the interceptor repeatedly,
   * you should cache the result instead of calling this function multiple times.
   */
  fetchThroughAsyncInterceptors(e, n) {
    const r = e;
    let s = this._asyncInterceptorsByName.get(r);
    return n && (s = s.filter(n)), L_(s || []);
  }
  async interceptAsync(e, n) {
    const r = e;
    this._asyncInterceptorsByName.has(r) || this._asyncInterceptorsByName.set(r, []);
    const s = this._asyncInterceptorsByName.get(r);
    return s.push(n), this._asyncInterceptorsByName.set(
      r,
      s.sort((i, o) => {
        var a, u;
        return ((a = o.priority) != null ? a : 0) - ((u = i.priority) != null ? u : 0);
      })
      // from large to small
    ), () => cs(this._asyncInterceptorsByName.get(r), n);
  }
  getInterceptPoints() {
    return this._asyncInterceptorPoints;
  }
  dispose() {
    this._asyncInterceptorsByName.clear();
  }
}
function oR(t, e) {
  for (const n in e)
    e.hasOwnProperty(n) && (t[n] = e[n]);
}
class Fi extends nt {
  static extend(e) {
    Object.getOwnPropertyNames(e.prototype).forEach((n) => {
      n !== "constructor" && (this.prototype[n] = e.prototype[n]);
    }), Object.getOwnPropertyNames(e).forEach((n) => {
      n !== "prototype" && n !== "name" && n !== "length" && (this[n] = e[n]);
    });
  }
}
const Ds = Symbol("initializers");
class al extends nt {
  constructor(e) {
    super(), this._injector = e;
    const n = this, r = Object.getPrototypeOf(this)[Ds];
    r && r.forEach(function(s) {
      s.apply(n, [e]);
    });
  }
  _initialize(e) {
  }
  static extend(e) {
    Object.getOwnPropertyNames(e.prototype).forEach((n) => {
      if (n === "_initialize") {
        let r = this.prototype[Ds];
        r || (r = [], this.prototype[Ds] = r), r.push(e.prototype._initialize);
      } else n !== "constructor" && (this.prototype[n] = e.prototype[n]);
    }), Object.getOwnPropertyNames(e).forEach((n) => {
      n !== "prototype" && n !== "name" && n !== "length" && (this[n] = e[n]);
    });
  }
}
class $i {
  constructor() {
    C(this, "_data", []);
  }
  static create() {
    return new $i();
  }
  add(e) {
    this._data.indexOf(e) > -1 || this._data.push(e);
  }
  delete(e) {
    const n = this._data.indexOf(e);
    this._data.splice(n, 1);
  }
  getData() {
    return this._data;
  }
}
class ul {
  constructor() {
    C(this, "_data", /* @__PURE__ */ new Map());
  }
  static create() {
    return new ul();
  }
  add(e, n) {
    this._data.has(e) || this._data.set(e, n);
  }
  delete(e) {
    this._data.delete(e);
  }
  getData() {
    return this._data;
  }
}
const U_ = "0.5.5";
function P_(t = "", e = ur.ZH_CN, n = "") {
  return {
    id: t,
    sheetOrder: [],
    name: n,
    appVersion: U_,
    locale: e,
    styles: {},
    sheets: {},
    resources: []
  };
}
class k_ {
  constructor(e = {}) {
    C(this, "_styles");
    C(this, "_cacheMap", new Qr(1e5));
    this._styles = e, this._generateCacheMap();
  }
  each(e) {
    return Object.entries(this._styles).forEach(e), this;
  }
  search(e, n) {
    if (this._cacheMap.has(n))
      return this._cacheMap.get(n);
    const r = this._getExistingStyleId(e);
    return r || "-1";
  }
  get(e) {
    return typeof e != "string" ? e : (e = String(e), this._styles[e]);
  }
  add(e, n) {
    const r = re.generateRandomId(6);
    return this._styles[r] = e, this._cacheMap.set(n, r), r;
  }
  setValue(e) {
    if (e == null) return;
    const n = JSON.stringify(e), r = this.search(e, n);
    return r !== "-1" ? r : this.add(e, n);
  }
  toJSON() {
    return this._styles;
  }
  getStyleByCell(e) {
    let n;
    e && re.isObject(e.s) ? n = e.s : n = (e == null ? void 0 : e.s) && this.get(e.s);
    const r = e == null ? void 0 : e.interceptorStyle;
    return r ? {
      ...n,
      ...r
    } : n;
  }
  _generateCacheMap() {
    const { _styles: e, _cacheMap: n } = this;
    for (const r in e) {
      const s = JSON.stringify(e[r]);
      n.set(s, r);
    }
  }
  _getExistingStyleId(e) {
    const { _styles: n } = this;
    for (const r in n)
      if (re.diffValue(n[r], e))
        return r;
    return null;
  }
}
const aR = (t, e) => e.length === t.length && !t.some((n) => e.some((r) => !en.equals(r, n))), uR = (t, e) => e.length === t.length && t.every((n, r) => {
  const s = e[r];
  return s.unitId === n.unitId && s.sheetId === n.sheetId && en.equals(n.range, s.range);
}), ti = {
  t: 0,
  b: 2,
  // must over 1, see https://github.com/dream-num/univer/issues/2727
  l: 2,
  r: 2
}, F_ = (t) => ({
  sbr: 0.6,
  sbo: t,
  spr: 0.6,
  spo: t
}), ga = 90;
function Sr(t, e, n = {}) {
  const r = t.length, {
    textRotation: s,
    paddingData: i,
    horizontalAlign: o = Xt.UNSPECIFIED,
    verticalAlign: a = hn.UNSPECIFIED,
    wrapStrategy: u = xn.UNSPECIFIED,
    cellValueType: c
  } = n, { t: l, r: h, b: d, l: f } = i || ti, { vertexAngle: E, centerAngle: R } = ll(s), O = {
    id: "d",
    body: {
      dataStream: `${t}${Wd}`,
      textRuns: [
        {
          ts: e,
          st: 0,
          ed: r
        }
      ],
      paragraphs: [
        {
          startIndex: r,
          paragraphStyle: {
            horizontalAlign: o
          }
        }
      ],
      sectionBreaks: [{
        startIndex: r + 1
      }]
    },
    documentStyle: {
      pageSize: {
        width: Number.POSITIVE_INFINITY,
        height: Number.POSITIVE_INFINITY
      },
      marginTop: l,
      marginBottom: d,
      marginRight: h,
      marginLeft: f,
      renderConfig: {
        horizontalAlign: o,
        verticalAlign: a,
        centerAngle: R,
        vertexAngle: E,
        wrapStrategy: u,
        cellValueType: c,
        zeroWidthParagraphBreak: 1
      }
    },
    drawings: {},
    drawingsOrder: []
  };
  return new jt(O);
}
function $_(t) {
  if (!t) return {};
  const {
    tr: e,
    td: n,
    ht: r,
    vt: s,
    tb: i,
    pd: o
  } = t;
  return {
    textRotation: e,
    textDirection: n,
    horizontalAlign: r,
    verticalAlign: s,
    wrapStrategy: i,
    paddingData: o
  };
}
function pa(t) {
  if (!t)
    return {};
  const { ff: e, fs: n, it: r, bl: s, ul: i, st: o, ol: a, cl: u } = t, c = {};
  return e && (c.ff = e), n && (c.fs = n), r && (c.it = r), s && (c.bl = s), i && (c.ul = i), o && (c.st = o), a && (c.ol = a), u && (c.cl = u), c;
}
function B_(t, e, n) {
  var i;
  const r = t.getBody();
  if ((i = r.customRanges) != null && i.some((o) => o.rangeType === mn.HYPERLINK))
    return;
  const s = st.customRange.add({
    ranges: [
      {
        startOffset: 0,
        endOffset: r.dataStream.length - 1,
        collapsed: !1
      }
    ],
    rangeId: n,
    rangeType: mn.HYPERLINK,
    body: r,
    properties: {
      url: e,
      refId: n
    }
  });
  s && Ke.apply(r, s.serialize());
}
function j_(t) {
  return t != null;
}
const H_ = '"Helvetica Neue", Helvetica, Arial, "PingFang SC", "Hiragino Sans GB", "Heiti SC", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif';
function ma(t) {
  const e = gt.ff, n = gt.fs;
  if (!t) {
    const h = `${n}pt  ${e}`;
    return {
      fontCache: h,
      fontString: h,
      fontSize: n,
      originFontSize: n,
      fontFamily: e
    };
  }
  let r = Yn.ITALIC;
  (t.it === 0 || t.it === void 0) && (r = Yn.NORMAL);
  let s = Yn.BOLD;
  (t.bl === 0 || t.bl === void 0) && (s = Yn.NORMAL);
  let i = n;
  t.fs && (i = Math.ceil(t.fs));
  let o = e;
  if (t.ff) {
    let h = t.ff;
    h = h.replace(/"/g, "").replace(/'/g, ""), h.indexOf(" ") > -1 && (h = `"${h}"`), h == null && (h = e), o = h;
  }
  const { va: a } = t;
  let u = i;
  if (a === Bt.SUBSCRIPT || a === Bt.SUPERSCRIPT) {
    const h = W_(o, u), { sbr: d, spr: f } = h;
    u *= a === Bt.SUBSCRIPT ? d : f;
  }
  const c = `${r} ${s} ${u}pt ${o}`, l = `${c}, ${H_} `;
  return {
    fontCache: c,
    fontString: l,
    fontSize: u,
    originFontSize: i,
    fontFamily: o
  };
}
function W_(t, e) {
  return F_(e);
}
function ll(t) {
  const { a: e = 0, v: n = we.FALSE } = t || { a: 0, v: we.FALSE };
  let r = 0, s = e;
  return n === we.TRUE && (r = ga, s = ga), { centerAngle: r, vertexAngle: s };
}
class z_ {
  constructor(e, n) {
    C(this, "_columnData", {});
    this._config = e, this._columnData = n;
  }
  /**
   * Get width and hidden status of columns in the sheet
   * @returns
   */
  getColumnData() {
    return this._columnData;
  }
  getColVisible(e) {
    const { _columnData: n } = this, r = n[e];
    return r ? r.hd !== we.TRUE : !0;
  }
  /**
   * Get the column style
   * @param {number} col Column index
   * @returns {string | Nullable<IStyleData>} Style data, may be undefined
   */
  getColumnStyle(e) {
    var n;
    return (n = this._columnData[e]) == null ? void 0 : n.s;
  }
  /**
   * Set the set column  default style
   * @param {number} col Column index
   * @param {string | Nullable<IStyleData>} style Style data
   */
  setColumnStyle(e, n) {
    const r = this.getColumnOrCreate(e);
    r.s = n;
  }
  /**
   * Get all hidden columns
   * @param start Start index
   * @param end End index
   * @returns Hidden columns range list
   */
  getHiddenCols(e = 0, n = this.getSize() - 1) {
    const r = [];
    let s = !1, i = -1;
    for (let o = e; o <= n; o++) {
      const a = this.getColVisible(o);
      s && a ? (s = !1, r.push({
        rangeType: De.COLUMN,
        startColumn: i,
        endColumn: o - 1,
        startRow: 0,
        endRow: 0
      })) : !s && !a && (s = !0, i = o);
    }
    return s && r.push({
      startRow: 0,
      endRow: 0,
      startColumn: i,
      endColumn: n,
      rangeType: De.COLUMN
    }), r;
  }
  /**
   * Get all visible columns
   * @param start Start index
   * @param end End index
   * @returns Visible columns range list
   */
  getVisibleCols(e = 0, n = this.getSize() - 1) {
    const r = [];
    let s = !1, i = -1;
    for (let o = e; o <= n; o++) {
      const a = this.getColVisible(o);
      s && !a ? (s = !1, r.push({
        rangeType: De.COLUMN,
        startColumn: i,
        endColumn: o - 1,
        startRow: 0,
        endRow: 0
      })) : !s && a && (s = !0, i = o);
    }
    return s && r.push({
      startRow: 0,
      endRow: 0,
      startColumn: i,
      endColumn: n,
      rangeType: De.COLUMN
    }), r;
  }
  getColumnDatas(e, n) {
    const r = {};
    let s = 0;
    for (let i = e; i < e + n; i++) {
      const o = this.getColumnOrCreate(i);
      r[s] = o, s++;
    }
    return r;
  }
  /**
   * Get count of column in the sheet
   * @returns
   */
  getSize() {
    return fn(this._columnData);
  }
  /**
   * Get the width of column
   * @param columnPos column index
   * @returns
   */
  getColumnWidth(e) {
    const { _columnData: n } = this, r = this._config;
    let s = 0;
    return s = (n[e] || {
      hd: we.FALSE,
      w: r.defaultColumnWidth
    }).w || r.defaultColumnWidth, s;
  }
  /**
   * get given column data
   * @param columnPos column index
   */
  getColumn(e) {
    const n = this._columnData[e];
    if (n)
      return n;
  }
  /**
   * Remove column data of given column
   * @param columnPos
   */
  removeColumn(e) {
    delete this._columnData[e];
  }
  /**
   * get given column data or create a column data when it's null
   * @param columnPos column index
   * @returns {Partial<IColumnData>} columnData
   */
  getColumnOrCreate(e) {
    const { _columnData: n } = this, r = n[e];
    if (r)
      return r;
    const s = {};
    return this._columnData[e] = s, s;
  }
  setCustomMetadata(e, n) {
    const r = this.getColumn(e);
    r && (r.custom = n);
  }
  getCustomMetadata(e) {
    var n;
    return (n = this.getColumn(e)) == null ? void 0 : n.custom;
  }
}
class Y_ {
  constructor(e, n, r) {
    C(this, "_rowData");
    this._config = e, this._viewModel = n, this._rowData = r;
  }
  /**
   * Get height and hidden status of columns in the sheet
   * @returns
   */
  getRowData() {
    return this._rowData;
  }
  /**
   * Get the row style
   * @param {number} row Row index
   * @returns {string | Nullable<IStyleData>} Style data, may be undefined
   */
  getRowStyle(e) {
    var n;
    return (n = this._rowData[e]) == null ? void 0 : n.s;
  }
  /**
   * Set row default style
   * @param {number} row The row index
   * @param {string | Nullable<IStyleData>} style The style data
   */
  setRowStyle(e, n) {
    const r = this.getRowOrCreate(e);
    r.s = n;
  }
  getRowDatas(e, n) {
    const r = {};
    let s = 0;
    for (let i = e; i < e + n; i++) {
      const o = this.getRowOrCreate(i);
      r[s] = o, s++;
    }
    return r;
  }
  getRowHeight(e, n = 1) {
    const { _rowData: r } = this, s = this._config;
    let i = 0;
    for (let o = 0; o < n; o++) {
      const a = r[o + e] || {
        hd: we.FALSE,
        h: s.defaultRowHeight
      }, { ia: u, ah: c, h: l = s.defaultRowHeight } = a;
      i += (u == null || u === we.TRUE) && typeof c == "number" ? c : l;
    }
    return i;
  }
  /**
   * Get row data of given row
   * @param rowPos row index
   * @returns {Nullable<Partial<IRowData>>} rowData
   */
  getRow(e) {
    return this._rowData[e];
  }
  /**
   * Remove row data of given row
   * @param rowPos
   */
  removeRow(e) {
    delete this._rowData[e];
  }
  /**
   * Get given row data or create a row data when it's null
   * @param rowPos row index
   * @returns {Partial<IRowData>} rowData
   */
  getRowOrCreate(e) {
    const { _rowData: n } = this, r = n[e];
    if (r)
      return r;
    const s = {};
    return n[e] = s, s;
  }
  /**
   * Get all hidden rows
   * @param start Start index
   * @param end End index
   * @returns Hidden rows range list
   */
  getHiddenRows(e = 0, n = this.getSize() - 1) {
    const r = [];
    let s = !1, i = -1;
    for (let o = e; o <= n; o++) {
      const a = this.getRowRawVisible(o);
      s && a ? (s = !1, r.push({
        startRow: i,
        endRow: o - 1,
        startColumn: 0,
        endColumn: 0,
        rangeType: De.ROW
      })) : !s && !a && (s = !0, i = o);
    }
    return s && r.push({ startRow: i, endRow: n, startColumn: 0, endColumn: 0, rangeType: De.ROW }), r;
  }
  /**
   * Get all visible rows
   * @param start Start index
   * @param end End index
   * @returns Visible rows range list
   */
  getVisibleRows(e = 0, n = this.getSize() - 1) {
    const r = [];
    let s = !1, i = -1;
    for (let o = e; o <= n; o++) {
      const a = this.getRowRawVisible(o);
      s && !a ? (s = !1, r.push({
        startRow: i,
        endRow: o - 1,
        startColumn: 0,
        endColumn: 0,
        rangeType: De.ROW
      })) : !s && a && (s = !0, i = o);
    }
    return s && r.push({ startRow: i, endRow: n, startColumn: 0, endColumn: 0, rangeType: De.ROW }), r;
  }
  getRowRawVisible(e) {
    const n = this.getRow(e);
    return n ? n.hd !== we.TRUE : !0;
  }
  /**
   * Get count of row in the sheet
   * @returns {number} row count
   */
  getSize() {
    return fn(this._rowData);
  }
  setCustomMetadata(e, n) {
    const r = this.getRow(e);
    r && (r.custom = n);
  }
  getCustomMetadata(e) {
    var n;
    return (n = this.getRow(e)) == null ? void 0 : n.custom;
  }
}
const lR = "DEFAULT_WORKSHEET_ROW_COUNT", V_ = 1e3, cR = "DEFAULT_WORKSHEET_COLUMN_COUNT", G_ = 20, hR = "DEFAULT_WORKSHEET_ROW_HEIGHT", K_ = 24, dR = "DEFAULT_WORKSHEET_COLUMN_WIDTH", X_ = 88, fR = "DEFAULT_WORKSHEET_ROW_TITLE_WIDTH", J_ = 46, gR = "DEFAULT_WORKSHEET_COLUMN_TITLE_HEIGHT", Z_ = 20;
function Q_(t) {
  const e = {
    name: "Sheet1",
    // TODO: name should have i18n
    id: "sheet-01",
    tabColor: "",
    hidden: we.FALSE,
    rowCount: V_,
    columnCount: G_,
    zoomRatio: 1,
    freeze: {
      xSplit: 0,
      ySplit: 0,
      startRow: -1,
      startColumn: -1
    },
    scrollTop: 0,
    scrollLeft: 0,
    defaultColumnWidth: X_,
    defaultRowHeight: K_,
    mergeData: [],
    cellData: {},
    rowData: {},
    columnData: {},
    showGridlines: we.TRUE,
    rowHeader: {
      width: J_,
      hidden: we.FALSE
    },
    columnHeader: {
      height: Z_,
      hidden: we.FALSE
    },
    rightToLeft: we.FALSE
  };
  return Object.keys(e).forEach((n) => {
    const r = n;
    typeof t[r] > "u" && (t[r] = e[r]);
  }), t;
}
class q_ extends nt {
  constructor(n) {
    super();
    /**
     * @property Cache for RANGE_TYPE.NORMAL
     */
    C(this, "_cellCache", /* @__PURE__ */ new Map());
    /**
     * @property Cache for RANGE_TYPE.ROW
     */
    C(this, "_rowCache", /* @__PURE__ */ new Map());
    /**
     * @property Cache for RANGE_TYPE.COLUMN
     */
    C(this, "_columnCache", /* @__PURE__ */ new Map());
    /**
     * @property Whether has RANGE_TYPE.ROW
     */
    C(this, "_hasRow", !1);
    /**
     * @property Whether has RANGE_TYPE.COLUMN
     */
    C(this, "_hasColumn", !1);
    /**
     * @property Whether has RANGE_TYPE.ALL
     */
    C(this, "_hasAll", !1);
    /**
     * @property Index for RANGE_TYPE.ALL
     */
    C(this, "_allIndex", -1);
    /**
     * @property the original merge data
     */
    C(this, "_mergeData");
    C(this, "_rangeMap", new Qr(5e4));
    C(this, "_skeletonCache", new Qr(5e4));
    this._init(n.concat());
  }
  _init(n) {
    this._mergeData = n, this._createCache(n);
  }
  _clearCache() {
    this._cellCache.clear(), this._rowCache.clear(), this._columnCache.clear(), this._hasAll = !1, this._allIndex = -1, this._rangeMap.clear(), this._skeletonCache.clear(), this._hasColumn = !1, this._hasRow = !1;
  }
  _createCache(n) {
    let r = 0;
    for (const s of n) {
      const { rangeType: i } = s;
      i === De.ROW ? this._createRowCache(s, r) : i === De.COLUMN ? this._createColumnCache(s, r) : i === De.ALL ? this._createCellAllCache(r) : this._createCellCache(s, r), r++;
    }
  }
  /**
   * Rebuild the merge data cache when the merge data is changed.
   * @param {IRange[]} mergeData
   */
  rebuild(n) {
    this._clearCache(), this._init(n.concat());
  }
  _createRowCache(n, r) {
    const { startRow: s, endRow: i } = n;
    for (let o = s; o <= i; o++)
      this._rowCache.set(o, r), this._hasRow = !0;
  }
  _createColumnCache(n, r) {
    const { startColumn: s, endColumn: i } = n;
    for (let o = s; o <= i; o++)
      this._columnCache.set(o, r), this._hasColumn = !0;
  }
  _createCellAllCache(n) {
    this._hasAll = !0, this._allIndex = n;
  }
  _createCellCache(n, r) {
    for (let s = n.startRow; s <= n.endRow; s++) {
      let i = this._cellCache.get(s);
      i == null && (i = /* @__PURE__ */ new Map(), this._cellCache.set(s, i));
      for (let o = n.startColumn; o <= n.endColumn; o++)
        i.set(o, r);
    }
  }
  add(n) {
    this._mergeData.push(n), this._clearCache(), this._createCache(this._mergeData);
  }
  remove(n, r) {
    const s = this._getMergeDataIndex(n, r);
    s !== -1 && (this._mergeData.splice(s, 1), this._clearCache(), this._createCache(this._mergeData));
  }
  getMergedCell(n, r) {
    const s = this._getMergeDataIndex(n, r);
    return s !== -1 ? this._mergeData[s] : null;
  }
  /**
   * Return index of merge data if (row,col) is in merge range. -1 means not in merge range.
   * @param row
   * @param column
   * @returns {number} index of merge range.
   */
  getMergeDataIndex(n, r) {
    return this._getMergeDataIndex(n, r);
  }
  isRowContainsMergedCell(n) {
    return this._hasAll || !re.isEmptyObject(this._columnCache) ? !0 : this._mergeData.some((r) => r.startRow <= n && n <= r.endRow);
  }
  isColumnContainsMergedCell(n) {
    return this._hasAll || !re.isEmptyObject(this._rowCache) ? !0 : this._mergeData.some((r) => r.startColumn <= n && n <= r.endColumn);
  }
  getMergedCellRange(n, r, s, i) {
    const o = [], a = `${n}-${r}-${s}-${i}`;
    if (this._rangeMap.has(a))
      return this._getRangeFromCache(a);
    let u = 0;
    const c = [];
    for (const l of this._mergeData || [])
      en.intersects(l, {
        startRow: n,
        endRow: s,
        startColumn: r,
        endColumn: i
      }) && (o.push({
        ...l
      }), c.push(u)), u++;
    return this._rangeMap.set(a, c), o;
  }
  /**
   * @deprecated sigificant performance impact, use _getCellMergeInfo instead.
   * @param startRow
   * @param startColumn
   * @param endRow
   * @param endColumn
   */
  getMergedCellRangeForSkeleton(n, r, s, i) {
    const o = [], a = this._mergeData, u = `${n}-${r}-${s}-${i}`;
    if (this._skeletonCache.has(u))
      return this._getSkeletonRangeFromCache(u);
    const c = [];
    for (let l = 0; l < a.length; l++) {
      const {
        startRow: h,
        endRow: d,
        startColumn: f,
        endColumn: E
      } = a[l];
      for (let R = n; R <= s; R++) {
        let O = !1;
        for (let U = r; U <= i; U++)
          if (R >= h && R <= d && U >= f && U <= E) {
            o.push({
              startRow: h,
              endRow: d,
              startColumn: f,
              endColumn: E
            }), c.push(l), O = !0;
            break;
          }
        if (O)
          break;
      }
    }
    return this._skeletonCache.set(u, c), o;
  }
  _getRangeFromCache(n) {
    const r = this._rangeMap.get(n) || [], s = [];
    for (const i of r)
      s.push({
        ...this._mergeData[i]
      });
    return s;
  }
  _getSkeletonRangeFromCache(n) {
    const r = this._skeletonCache.get(n) || [], s = [];
    for (const i of r)
      s.push({
        ...this._mergeData[i]
      });
    return s;
  }
  _getMergeDataIndex(n, r) {
    var i;
    if (this._hasAll)
      return this._allIndex;
    if (this._hasRow) {
      const o = this._rowCache.get(n);
      if (o !== void 0)
        return o;
    }
    if (this._hasColumn) {
      const o = this._columnCache.get(r);
      if (o !== void 0)
        return o;
    }
    const s = (i = this._cellCache.get(n)) == null ? void 0 : i.get(r);
    return s !== void 0 ? s : -1;
  }
  getMergeDataSnapshot() {
    return this._mergeData;
  }
  dispose() {
    this._clearCache(), this._mergeData = [];
  }
}
class eE extends nt {
  constructor(n) {
    super();
    C(this, "_cellContentInterceptor", null);
    C(this, "_rowFilteredInterceptor", null);
    this.getRawCell = n;
  }
  dispose() {
    super.dispose(), this._cellContentInterceptor = null, this._rowFilteredInterceptor = null;
  }
  getCell(n, r, s, i) {
    return this._cellContentInterceptor ? this._cellContentInterceptor.getCell(n, r, Vn.Value | Vn.Style, s, i) : this.getRawCell(n, r);
  }
  getCellValueOnly(n, r) {
    return this._cellContentInterceptor ? this._cellContentInterceptor.getCell(n, r, Vn.Value) : this.getRawCell(n, r);
  }
  getCellStyleOnly(n, r) {
    return this._cellContentInterceptor ? this._cellContentInterceptor.getCell(n, r, Vn.Style) : this.getRawCell(n, r);
  }
  getRowFiltered(n) {
    var r, s;
    return (s = (r = this._rowFilteredInterceptor) == null ? void 0 : r.getRowFiltered(n)) != null ? s : !1;
  }
  registerCellContentInterceptor(n) {
    if (this._cellContentInterceptor)
      throw new Error("[SheetViewModel]: Interceptor already registered.");
    return this._cellContentInterceptor = n, Ze(() => this._cellContentInterceptor = null);
  }
  registerRowFilteredInterceptor(n) {
    if (this._rowFilteredInterceptor)
      throw new Error("[SheetViewModel]: Interceptor already registered.");
    return this._rowFilteredInterceptor = n, Ze(() => this._rowFilteredInterceptor = null);
  }
}
const _a = {
  isDeepClone: !1,
  displayRawFormula: !1,
  ignoreTextRotation: !1
};
class es {
  constructor(e, n, r) {
    C(this, "_sheetId");
    C(this, "_snapshot");
    C(this, "_cellData");
    C(this, "_rowManager");
    C(this, "_columnManager");
    C(this, "_viewModel");
    C(this, "_spanModel");
    var a;
    this.unitId = e, this._styles = r, this._snapshot = Q_(n);
    const { columnData: s, rowData: i, cellData: o } = this._snapshot;
    this._sheetId = (a = this._snapshot.id) != null ? a : re.generateRandomId(6), this._cellData = new kt(o), this._viewModel = new eE((u, c) => this.getCellRaw(u, c)), this._rowManager = new Y_(this._snapshot, this._viewModel, i), this._columnManager = new z_(this._snapshot, s), this._spanModel = new q_(this._snapshot.mergeData);
  }
  /**
   * @internal
   * @param callback
   */
  __interceptViewModel(e) {
    e(this._viewModel);
  }
  getSnapshot() {
    return this._snapshot;
  }
  /**
   * Set the merge data of the sheet, all the merged cells will be rebuilt.
   * @param mergeData
   */
  setMergeData(e) {
    this._snapshot.mergeData = e, this.getSpanModel().rebuild(e);
  }
  getSpanModel() {
    return this._spanModel;
  }
  getStyleDataByHash(e) {
    return { ...this._styles.get(e) };
  }
  setStyleData(e) {
    return this._styles.setValue(e);
  }
  /**
   * Get the style of the column.
   * @param {number} column The column index
   * @param {boolean} [keepRaw] If true, return the raw style data, otherwise return the style data object
   * @returns {Nullable<IStyleData>|string} The style of the column
   */
  getColumnStyle(e, n = !1) {
    return n ? this._columnManager.getColumnStyle(e) : this._styles.get(this._columnManager.getColumnStyle(e));
  }
  /**
   * Set the style of the column.
   * @param {number} column The column index
   * @param {string|Nullable<IStyleData>} style The style to be set
   */
  setColumnStyle(e, n) {
    this._columnManager.setColumnStyle(e, n);
  }
  /**
   * Get the style of the row.
   * @param {number} row The row index
   * @param {boolean} [keepRaw] If true, return the raw style data, otherwise return the style data object
   * @returns {Nullable<IStyleData>} The style of the row
   */
  getRowStyle(e, n = !1) {
    return n ? this._rowManager.getRowStyle(e) : this._styles.get(this._rowManager.getRowStyle(e));
  }
  /**
   * Set the style of the row.
   * @param {number} row
   * @param {string|Nullable<IStyleData>} style The style to be set
   */
  setRowStyle(e, n) {
    this._rowManager.setRowStyle(e, n);
  }
  /**
   * this function is used to mixin default style to cell raw{number}
   * @param {number} row The row index
   * @param {number} col The column index
   * @param cellRaw The cell raw data
   * @param {boolean} isRowStylePrecedeColumnStyle The priority of row style and column style
   */
  mixinDefaultStyleToCellRaw(e, n, r, s) {
    const i = this.getColumnStyle(n), o = this.getRowStyle(e), a = this.getDefaultCellStyleInternal();
    if (a || i || o) {
      let u = r == null ? void 0 : r.s;
      typeof u == "string" && (u = this._styles.get(u));
      const c = s ? Mo(a, i, o, u) : Mo(a, o, i, u);
      r || (r = {}), r.s = c;
    }
  }
  /**
   * Get the default style of the worksheet.
   * @returns {Nullable<IStyleData>} Default Style
   */
  getDefaultCellStyle() {
    return this._snapshot.defaultStyle;
  }
  getDefaultCellStyleInternal() {
    const e = this._snapshot.defaultStyle;
    return this._styles.get(e);
  }
  /**
   * Set Default Style, if the style has been set, all cells style will be base on this style.
   * @param {Nullable<IStyleData>} style The style to be set as default style
   */
  setDefaultCellStyle(e) {
    this._snapshot.defaultStyle = e;
  }
  /**
   * Returns WorkSheet Cell Data Matrix
   * @returns WorkSheet Cell Data Matrix
   */
  getCellMatrix() {
    return this._cellData;
  }
  /**
   * Get worksheet printable cell range.
   * @returns
   */
  // eslint-disable-next-line max-lines-per-function
  getCellMatrixPrintRange() {
    const e = this.getCellMatrix(), n = this.getMergeData();
    let r = -1, s = -1, i = -1, o = -1, a = !1, u = !1;
    return e.forEach((c, l) => {
      Object.keys(l).forEach((h) => {
        const d = +h, f = e.getValue(c, d), E = f != null && f.s ? this._styles.get(f.s) : null, R = (E == null ? void 0 : E.bd) && (E.bd.b || E.bd.l || E.bd.r || E.bd.t || E.bd.bc_tr || E.bd.bl_tr || E.bd.ml_tr || E.bd.tl_bc || E.bd.tl_br || E.bd.tl_mr);
        (f && (f.v || f.p) || E != null && E.bg || R) && (a ? r = Math.min(r, c) : (r = c, a = !0), s = Math.max(s, c), u ? i = Math.min(i, d) : (u = !0, i = d), o = Math.max(o, d));
      });
    }), n.forEach((c) => {
      a ? r = Math.min(r, c.startRow) : (r = c.startRow, a = !0), s = Math.max(s, c.endRow), u ? i = Math.min(i, c.startColumn) : (i = c.startColumn, a = !0), o = Math.max(o, c.endColumn);
    }), !a || !u ? null : {
      startColumn: i,
      startRow: r,
      endColumn: o,
      endRow: s
    };
  }
  /**
   * Returns Row Manager
   * @returns Row Manager
   */
  getRowManager() {
    return this._rowManager;
  }
  /**
   * Returns the ID of its parent unit.
   */
  getUnitId() {
    return this.unitId;
  }
  /**
   * Returns the ID of the sheet represented by this object.
   * @returns ID of the sheet
   */
  getSheetId() {
    return this._sheetId;
  }
  /**
   * Returns Column Manager
   * @returns Column Manager
   */
  getColumnManager() {
    return this._columnManager;
  }
  /**
   * Returns the name of the sheet.
   * @returns name of the sheet
   */
  getName() {
    return this._snapshot.name;
  }
  /**
   * Returns WorkSheet Clone Object
   * @returns WorkSheet Clone Object
   * @deprecated
   */
  clone() {
    const { _snapshot: e } = this, n = re.deepClone(e);
    return new es(this.unitId, n, this._styles);
  }
  /**
   * Get the merged cell list of the sheet.
   * @returns {IRange[]} merged cell list
   */
  getMergeData() {
    return this._spanModel.getMergeDataSnapshot();
  }
  /**
   * Get the merged cell Range of the sheet cell.
   * If (row, col) is not in a merged cell, return null
   *
   * @param {number} row The row index of test cell
   * @param {number} col The column index of test cell
   * @returns {Nullable<IRange>} The merged cell range of the cell, if the cell is not in a merged cell, return null
   */
  getMergedCell(e, n) {
    return this._spanModel.getMergedCell(e, n);
  }
  /**
   * Get the merged cell info list which has intersection with the given range.
   * @param {number} startRow The start row index of the range
   * @param {number} startColumn The start column index of the range
   * @param {number} endRow The end row index of the range
   * @param {number} endColumn The end column index of the range
   * @returns {IRange} The merged cell info list which has intersection with the given range or empty array if no merged cell in the range
   */
  getMergedCellRange(e, n, r, s) {
    return this._spanModel.getMergedCellRange(e, n, r, s);
  }
  /**
   * Get if the row contains merged cell
   * @param {number} row The row index
   * @returns {boolean} Is merge cell across row
   */
  isRowContainsMergedCell(e) {
    return this._spanModel.isRowContainsMergedCell(e);
  }
  /**
   * Get if the column contains merged cell
   * @param {number} column The column index
   * @returns {boolean} Is merge cell across column
   */
  isColumnContainsMergedCell(e) {
    return this._spanModel.isColumnContainsMergedCell(e);
  }
  /**
   * Get cell info with merge data
   * @param {number} row - The row index of the cell.
   * @param {number} column - The column index of the cell.
   * @type {selectionCell}
   * @property {number} actualRow - The actual row index of the cell
   * @property {number} actualColumn - The actual column index of the cell
   * @property {boolean} isMergedMainCell - Whether the cell is the main cell of the merged cell, only the upper left cell in the merged cell returns true here
   * @property {boolean} isMerged - Whether the cell is in a merged cell, the upper left cell in the merged cell returns false here
   * @property {number} endRow - The end row index of the merged cell
   * @property {number} endColumn - The end column index of the merged cell
   * @property {number} startRow - The start row index of the merged cell
   * @property {number} startColumn - The start column index of the merged cell
   * @returns  {selectionCell} - The cell info with merge data
   */
  getCellInfoInMergeData(e, n) {
    const r = this.getMergedCell(e, n);
    let s = !1, i = !1, o = e, a = n, u = e, c = n;
    if (r) {
      const {
        startRow: l,
        endRow: h,
        startColumn: d,
        endColumn: f
      } = r;
      e === l && n === d ? (o = h, a = f, u = l, c = d, i = !0) : e >= l && e <= h && n >= d && n <= f && (o = h, a = f, u = l, c = d, s = !0);
    }
    return {
      actualRow: e,
      actualColumn: n,
      isMergedMainCell: i,
      isMerged: s,
      endRow: o,
      endColumn: a,
      startRow: u,
      startColumn: c
    };
  }
  /**
   * Get cellData, includes cellData, customRender, markers, dataValidate, etc.
   *
   * WARNING: All sheet CELL_CONTENT interceptors will be called in this method, cause performance issue.
   * example: this._sheetInterceptorService.intercept(INTERCEPTOR_POINT.CELL_CONTENT);
   *
   * @param row
   * @param col
   * @returns ICellDataForSheetInterceptor
   */
  getCell(e, n) {
    return e < 0 || n < 0 ? null : this._viewModel.getCell(e, n);
  }
  /**
   * Get cellData only use effect on value interceptor
   * @param {number} number row The row index of the cell.
   * @param {number} number col The column index of the cell.
   * @returns {Nullable<ICellDataForSheetInterceptor>} The cell data only use effect on value interceptor
   */
  getCellValueOnly(e, n) {
    return e < 0 || n < 0 ? null : this._viewModel.getCellValueOnly(e, n);
  }
  /**
   * Get cellData only use effect on style interceptor
   * @param {number} row The row index of the cell.
   * @param {number} col The column index of the cell.
   * @returns {Nullable<ICellDataForSheetInterceptor>} The cell data only use effect on style interceptor
   */
  getCellStyleOnly(e, n) {
    return e < 0 || n < 0 ? null : this._viewModel.getCellStyleOnly(e, n);
  }
  getCellRaw(e, n) {
    return this.getCellMatrix().getValue(e, n);
  }
  // eslint-disable-next-line ts/no-explicit-any
  getCellWithFilteredInterceptors(e, n, r, s) {
    return this._viewModel.getCell(e, n, r, s);
  }
  getRowFiltered(e) {
    return this._viewModel.getRowFiltered(e);
  }
  getMatrixWithMergedCells(e, n, r, s, i = zn.Raw) {
    const o = this.getCellMatrix(), a = this._spanModel.getMergedCellRange(e, n, r, s), u = new kt();
    return Qo(e, r, n, s).forEach((c, l) => {
      var d;
      let h;
      if (i === zn.Raw)
        h = this.getCellRaw(c, l);
      else if (i === zn.Intercepted)
        h = this.getCell(c, l);
      else if (i === zn.Both) {
        const f = this.getCellRaw(c, l);
        if (f) {
          h = { ...f };
          const E = (d = this.getCell(c, l)) == null ? void 0 : d.v;
          j_(E) && h && (h.displayV = String(E));
        }
      }
      h && u.setValue(c, l, h);
    }), a.forEach((c) => {
      const { startColumn: l, startRow: h, endColumn: d, endRow: f } = c;
      Qo(h, f, l, d).forEach((E, R) => {
        E === h && R === l && u.setValue(E, R, {
          ...o.getValue(E, R),
          rowSpan: f - h + 1,
          colSpan: d - l + 1
        }), (E !== h || R !== l) && u.realDeleteValue(E, R);
      });
    }), u;
  }
  getRange(e, n, r, s) {
    return typeof e == "object" ? new tr(this, e, {
      getStyles: () => this._styles
    }) : new tr(
      this,
      {
        startRow: e,
        startColumn: n,
        endColumn: s || n,
        endRow: r || e
      },
      {
        getStyles: () => this._styles
      }
    );
  }
  getScrollLeftTopFromSnapshot() {
    return {
      scrollLeft: this._snapshot.scrollLeft,
      scrollTop: this._snapshot.scrollTop
    };
  }
  /**
   * Return WorkSheetZoomRatio
   * @return zoomRatio
   */
  getZoomRatio() {
    return this._snapshot.zoomRatio || 1;
  }
  /**
   * Returns WorkSheet Configures
   * @returns WorkSheet Configures
   */
  getConfig() {
    return this._snapshot;
  }
  /**
   * Returns  frozen.
   * @returns  frozen
   */
  getFreeze() {
    return this._snapshot.freeze;
  }
  /**
   * Returns the current number of columns in the sheet, regardless of content.
   * @returns the current number of columns in the sheet, regardless of content
   */
  getMaxColumns() {
    const { _snapshot: e } = this, { columnCount: n } = e;
    return n;
  }
  /**
   * Returns the current number of rows in the sheet, regardless of content.
   * @returns the current number of rows in the sheet, regardless of content
   */
  getMaxRows() {
    const { _snapshot: e } = this, { rowCount: n } = e;
    return n;
  }
  getRowCount() {
    return this._snapshot.rowCount;
  }
  setRowCount(e) {
    this._snapshot.rowCount = e;
  }
  getColumnCount() {
    return this._snapshot.columnCount;
  }
  setColumnCount(e) {
    this._snapshot.columnCount = e;
  }
  /**
   * isSheetHidden
   * @returns hidden status of sheet
   */
  isSheetHidden() {
    return this._snapshot.hidden;
  }
  /**
   * Returns true if the sheet's gridlines are hidden; otherwise returns false. Gridlines are visible by default.
   * @returns {boolean} Gridlines Hidden Status.
   */
  hasHiddenGridlines() {
    const { _snapshot: e } = this, { showGridlines: n } = e;
    return n === 0;
  }
  /**
   * Returns the color of the gridlines, or undefined if the gridlines are not colored.
   * @returns {string | undefined} returns the color of the gridlines, or undefined if the gridlines are default.
   */
  getGridlinesColor() {
    return this.getConfig().gridlinesColor;
  }
  /**
   * Gets the sheet tab color, or null if the sheet tab has no color.
   * @returns the sheet tab color or null
   */
  getTabColor() {
    const { _snapshot: e } = this, { tabColor: n } = e;
    return n;
  }
  /**
   * Gets the width in pixels of the given column.
   * @param columnPosition column index
   * @returns Gets the width in pixels of the given column.
   */
  getColumnWidth(e) {
    return this.getColumnManager().getColumnWidth(e);
  }
  /**
   * Gets the height in pixels of the given row.
   * @param row row index
   * @returns Gets the height in pixels of the given row.
   */
  getRowHeight(e) {
    return this._viewModel.getRowFiltered(e) ? 0 : this.getRowManager().getRowHeight(e);
  }
  /**
   * Row is filtered out, that means this row is invisible.
   * @param row
   * @returns {boolean} is row hidden by filter
   */
  isRowFiltered(e) {
    return this._viewModel.getRowFiltered(e);
  }
  /**
   * Get if the row is visible. It may be affected by features like filter and view.
   * @param row the row index
   * @returns {boolean} if the row in visible to the user
   */
  getRowVisible(e) {
    return !this.isRowFiltered(e) && this.getRowRawVisible(e);
  }
  /**
   * Get if the row does not have `hidden` property. This value won't affected by features like filter and view.
   * @param row the row index
   * @returns if the row does not have `hidden` property
   */
  getRowRawVisible(e) {
    return this.getRowManager().getRowRawVisible(e);
  }
  getHiddenRows(e, n) {
    const r = this.getMaxColumns() - 1, s = this._rowManager.getHiddenRows(e, n);
    return s.forEach((i) => i.endColumn = r), s;
  }
  getColVisible(e) {
    return this._columnManager.getColVisible(e);
  }
  getHiddenCols(e, n) {
    const r = this.getMaxRows() - 1, s = this._columnManager.getHiddenCols(e, n);
    return s.forEach((i) => i.endRow = r), s;
  }
  /**
   * Get all visible rows in the sheet.(not include filter & view, like getRawVisibleRows)
   * @returns Visible rows range list
   */
  getVisibleRows() {
    const e = this.getRowCount();
    return this._rowManager.getVisibleRows(0, e - 1);
  }
  /**
   * Get all visible columns in the sheet.(not include filter & view)
   * @returns Visible columns range list
   */
  getVisibleCols() {
    const e = this.getColumnCount();
    return this._columnManager.getVisibleCols(0, e - 1);
  }
  /**
   * Returns true if this sheet layout is right-to-left. Returns false if the sheet uses the default left-to-right layout.
   * @returns true if this sheet layout is right-to-left. Returns false if the sheet uses the default left-to-right layout.
   */
  isRightToLeft() {
    const { _snapshot: e } = this, { rightToLeft: n } = e;
    return n;
  }
  /**
   * Returns the position of the last row that has content.
   * @returns the position of the last row that has content.
   */
  getLastRowWithContent() {
    return this._cellData.getLength() - 1;
  }
  /**
   * Returns the position of the last column that has content.
   * @returns the position of the last column that has content.
   */
  getLastColumnWithContent() {
    return this._cellData.getRange().endColumn;
  }
  getDataRangeScope() {
    return this._cellData.getStartEndScope();
  }
  cellHasValue(e) {
    return e && (e.v !== void 0 || e.f !== void 0 || e.p !== void 0);
  }
  // #region iterators
  // NOTE: performance intensive. Should keep an eye on methods in this region.
  /**
   * Iterate a range row by row.
   *
   * Performance intensive.
   *
   * @param range the iterate range
   * @param skipEmpty whether to skip empty cells, default to be `true`
   */
  iterateByRow(e, n = !0) {
    const { startRow: r, startColumn: s, endRow: i, endColumn: o } = e, a = this;
    return {
      [Symbol.iterator]: () => {
        let u = r, c = s;
        return {
          next() {
            for (; ; ) {
              if (c > o && (u += 1, c = s), u > i)
                return { done: !0, value: void 0 };
              const l = a.getCell(u, c), h = !l, d = a.getMergedCell(u, c);
              if (d) {
                if (u !== d.startRow || c !== d.startColumn) {
                  c = d.endColumn + 1;
                  continue;
                }
                if (h && n) {
                  c = d.endColumn + 1;
                  continue;
                }
                const E = { row: u, col: c, value: l };
                return E.colSpan = d.endColumn - d.startColumn + 1, E.rowSpan = d.endRow - d.startRow + 1, c = d.endColumn + 1, { done: !1, value: E };
              }
              if (h && n)
                c += 1;
              else {
                const f = { row: u, col: c, value: l };
                return c += 1, { done: !1, value: f };
              }
            }
          }
        };
      }
    };
  }
  /**
   * Iterate a range column by column. This is pretty similar to `iterateByRow` but with different order.
   *
   * Performance intensive.
   *
   * @param range The iterate range.
   * @param skipEmpty Whether to skip empty cells, default to be `true`.
   * @param skipNonTopLeft Whether to skip non-top-left cells of merged cells, default to be `true`. If the
   * parameter is set to `false`, the iterator will return cells in the top row.
   */
  iterateByColumn(e, n = !0, r = !0) {
    const { startRow: s, startColumn: i, endRow: o, endColumn: a } = e, u = this;
    return {
      [Symbol.iterator]: () => {
        let c = s, l = i;
        return {
          next() {
            for (; ; ) {
              if (c > o && (l += 1, c = s), l > a)
                return { done: !0, value: void 0 };
              const h = u.getMergedCell(c, l);
              if (h) {
                const E = c !== h.startRow, R = E || l !== h.startColumn;
                if (r && R || !r && E) {
                  c = h.endRow + 1;
                  continue;
                }
                const O = u.getCell(h.startRow, h.startColumn);
                if (!O && n) {
                  c = h.endRow + 1;
                  continue;
                }
                const ne = { row: c, col: h.startColumn, value: O };
                return ne.colSpan = h.endColumn - h.startColumn + 1, ne.rowSpan = h.endRow - h.startRow + 1, c = h.endRow + 1, { done: !1, value: ne };
              }
              const d = u.getCell(c, l);
              if (!d && n)
                c += 1;
              else {
                const E = { row: c, col: l, value: d };
                return c += 1, { done: !1, value: E };
              }
            }
          }
        };
      }
    };
  }
  /**
   * This method generates a document model based on the cell's properties and handles the associated styles and configurations.
   * If the cell does not exist, it will return null.
   * PS: This method has significant impact on performance.
   * @param cell
   * @param options
   */
  // eslint-disable-next-line complexity, max-lines-per-function
  _getCellDocumentModel(e, n = _a) {
    var R;
    const { isDeepClone: r, displayRawFormula: s, ignoreTextRotation: i } = {
      ..._a,
      ...n
    }, o = this._styles.getStyleByCell(e);
    if (!e)
      return;
    let a, u = "document";
    const c = $_(o), l = i ? gt.tr : c.textRotation || gt.tr;
    let h = c.horizontalAlign || gt.ht;
    const d = c.verticalAlign || gt.vt, f = c.wrapStrategy || gt.tb, E = c.paddingData || ti;
    if (e.f && s)
      a = Sr(e.f.toString(), {}, { verticalAlign: d }), h = gt.ht;
    else if (e.p) {
      const { centerAngle: O, vertexAngle: U } = ll(l);
      a = this._updateConfigAndGetDocumentModel(
        r ? re.deepClone(e.p) : e.p,
        h,
        E,
        {
          horizontalAlign: h,
          verticalAlign: d,
          centerAngle: O,
          vertexAngle: U,
          wrapStrategy: f,
          zeroWidthParagraphBreak: 1
        }
      );
    } else if (e.v != null) {
      const O = pa(o);
      u = ma(O).fontCache;
      let U = tE(e);
      e.t === dn.FORCE_STRING && s && (U = `'${U}`), a = Sr(U, O, {
        ...c,
        textRotation: l,
        cellValueType: e.t
      });
    }
    return a && e.linkUrl && e.linkId && B_(a, e.linkUrl, e.linkId), {
      documentModel: a,
      fontString: u,
      textRotation: l,
      wrapStrategy: f,
      verticalAlign: d,
      horizontalAlign: h,
      paddingData: E,
      fill: (R = o == null ? void 0 : o.bg) == null ? void 0 : R.rgb
    };
  }
  _updateConfigAndGetDocumentModel(e, n, r, s) {
    var o, a, u, c, l;
    if (!s || !((o = e.body) != null && o.dataStream))
      return;
    e.documentStyle || (e.documentStyle = {}), e.documentStyle.marginTop = (a = r.t) != null ? a : 0, e.documentStyle.marginBottom = (u = r.b) != null ? u : 2, e.documentStyle.marginLeft = (c = r.l) != null ? c : 2, e.documentStyle.marginRight = (l = r.r) != null ? l : 2, e.documentStyle.pageSize = {
      width: Number.POSITIVE_INFINITY,
      height: Number.POSITIVE_INFINITY
    }, e.documentStyle.renderConfig = {
      ...e.documentStyle.renderConfig,
      ...s
    };
    const i = e.body.paragraphs || [];
    for (const h of i)
      h.paragraphStyle || (h.paragraphStyle = {}), h.paragraphStyle.horizontalAlign = n;
    return new jt(e);
  }
  /**
   * Only used for cell edit, and no need to rotate text when edit cell content!
   */
  getBlankCellDocumentModel(e) {
    const n = this._getCellDocumentModel(e, { ignoreTextRotation: !0 }), r = this._styles.getStyleByCell(e), s = pa(r);
    if (n != null)
      return n.documentModel == null && (n.documentModel = Sr("", s)), n;
    const i = "";
    let o = "document";
    const a = gt.tr, u = gt.ht, c = gt.vt, l = gt.tb, h = ti;
    return o = ma({}).fontCache, {
      documentModel: Sr(i, s),
      fontString: o,
      textRotation: a,
      wrapStrategy: l,
      verticalAlign: c,
      horizontalAlign: u,
      paddingData: h
    };
  }
  // Only used for cell edit, and no need to rotate text when edit cell content!
  getCellDocumentModelWithFormula(e) {
    return this._getCellDocumentModel(e, {
      isDeepClone: !0,
      displayRawFormula: !0,
      ignoreTextRotation: !0
    });
  }
  /**
   * Get custom metadata of worksheet
   * @returns {CustomData | undefined} custom metadata
   */
  getCustomMetadata() {
    return this._snapshot.custom;
  }
  /**
   * Set custom metadata of workbook
   * @param {CustomData | undefined} custom custom metadata
   */
  setCustomMetadata(e) {
    this._snapshot.custom = e;
  }
}
function tE(t) {
  var r, s;
  if (!t)
    return "";
  const e = (s = (r = t.p) == null ? void 0 : r.body) == null ? void 0 : s.dataStream;
  if (e)
    return st.transform.getPlainText(e);
  const n = t.v;
  return typeof n == "string" ? t.t === dn.BOOLEAN ? n.toUpperCase() : n.replace(/[\r\n]/g, "") : typeof n == "number" ? t.t === dn.BOOLEAN ? n ? "TRUE" : "FALSE" : n.toString() : typeof n == "boolean" ? n ? "TRUE" : "FALSE" : "";
}
function pR(t) {
  if (t === null)
    return "";
  if (t != null && t.p) {
    const e = t == null ? void 0 : t.p.body;
    if (e == null)
      return "";
    const n = e.dataStream;
    return st.transform.getPlainText(n);
  }
  return t == null ? void 0 : t.v;
}
var nE = Object.defineProperty, rE = Object.getOwnPropertyDescriptor, sE = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? rE(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && nE(e, n, s), s;
}, iE = (t, e) => (n, r) => e(n, r, t);
function mR(t, e) {
  return `${t.getUnitId()}|${e.getSheetId()}`;
}
let ts = class extends Ui {
  constructor(e = {}, n) {
    super();
    C(this, "type", Fe.UNIVER_SHEET);
    C(this, "_sheetCreated$", new _t());
    C(this, "sheetCreated$", this._sheetCreated$.asObservable());
    C(this, "_sheetDisposed$", new _t());
    C(this, "sheetDisposed$", this._sheetDisposed$.asObservable());
    C(this, "_activeSheet$", new lt(null));
    C(this, "activeSheet$", this._activeSheet$.asObservable());
    /**
     * sheets list
     * @private
     */
    C(this, "_worksheets");
    /**
     * Common style
     * @private
     */
    C(this, "_styles");
    /**
     * number format
     * @private
     */
    // private _formatManage: FormatManager;
    C(this, "_snapshot");
    C(this, "_unitId");
    C(this, "_count");
    C(this, "_name$");
    C(this, "name$");
    this._logService = n;
    const r = P_();
    re.isEmptyObject(e) ? this._snapshot = r : this._snapshot = re.commonExtend(r, e);
    const { styles: s } = this._snapshot;
    (this._snapshot.id == null || this._snapshot.id.length === 0) && (this._snapshot.id = re.generateRandomId(6)), this._unitId = this._snapshot.id, this._styles = new k_(s), this._count = 1, this._worksheets = /* @__PURE__ */ new Map(), this._name$ = new lt(e.name || ""), this.name$ = this._name$.asObservable(), this._parseWorksheetSnapshots();
  }
  get _activeSheet() {
    return this._activeSheet$.getValue();
  }
  get name() {
    return this._name$.getValue();
  }
  static isIRangeType(e) {
    return typeof e == "string" || "startRow" in e || "row" in e;
  }
  dispose() {
    super.dispose(), this._sheetCreated$.complete(), this._sheetDisposed$.complete(), this._activeSheet$.complete(), this._name$.complete();
  }
  /**
   * Create a clone of the current snapshot.
   * Call resourceLoaderService.saveWorkbook to save the data associated with the current plugin if needed.
   * @memberof Workbook
   */
  save() {
    return re.deepClone(this._snapshot);
  }
  /**
   * Get current snapshot reference.
   * Call resourceLoaderService.saveWorkbook to save the data associated with the current plugin if needed.
   * @return {*}  {IWorkbookData}
   * @memberof Workbook
   */
  getSnapshot() {
    return this._snapshot;
  }
  /** @deprecated use use name property instead */
  getName() {
    return this._snapshot.name;
  }
  setName(e) {
    this._name$.next(e), this._snapshot.name = e;
  }
  getUnitId() {
    return this._unitId;
  }
  getRev() {
    var e;
    return (e = this._snapshot.rev) != null ? e : 1;
  }
  incrementRev() {
    this._snapshot.rev = this.getRev() + 1;
  }
  setRev(e) {
    this._snapshot.rev = e;
  }
  /**
   * Add a Worksheet into Workbook.
   */
  addWorksheet(e, n, r) {
    const { sheets: s, sheetOrder: i } = this._snapshot;
    if (s[e])
      return !1;
    s[e] = r, i.splice(n, 0, e);
    const o = new es(this._unitId, r, this._styles);
    return this._worksheets.set(e, o), this._sheetCreated$.next(o), !0;
  }
  getSheetOrders() {
    return this._snapshot.sheetOrder;
  }
  getWorksheets() {
    return this._worksheets;
  }
  getActiveSpreadsheet() {
    return this;
  }
  getStyles() {
    return this._styles;
  }
  getConfig() {
    return this._snapshot;
  }
  getIndexBySheetId(e) {
    const { sheetOrder: n } = this._snapshot;
    return n.findIndex((r) => r === e);
  }
  getActiveSheet(e) {
    if (!this._activeSheet && typeof e > "u")
      throw new Error(`[Workbook]: no active Worksheet on Workbook ${this._unitId}!`);
    return this._activeSheet;
  }
  /**
   * If there is no active sheet, the first sheet would
   * be set active.
   * @returns
   */
  ensureActiveSheet() {
    const e = this._activeSheet;
    if (e)
      return e;
    const n = this._snapshot.sheetOrder;
    for (let s = 0, i = n.length; s < i; s++) {
      const o = this._worksheets.get(n[s]);
      if (o && o.isSheetHidden() !== we.TRUE)
        return this.setActiveSheet(o), o;
    }
    const r = this._worksheets.get(n[0]);
    return this.setActiveSheet(r), r;
  }
  /**
   * ActiveSheet should not be null!
   * There is at least one sheet in a workbook. You can not delete all sheets in a workbook.
   * @param worksheet
   */
  setActiveSheet(e) {
    this._activeSheet$.next(e);
  }
  removeSheet(e) {
    const n = this._worksheets.get(e);
    return n ? (this._worksheets.delete(e), this._snapshot.sheetOrder.splice(this._snapshot.sheetOrder.indexOf(e), 1), delete this._snapshot.sheets[e], this._sheetDisposed$.next(n), !0) : !1;
  }
  getActiveSheetIndex() {
    const { sheetOrder: e } = this._snapshot;
    return e.findIndex((n) => this._worksheets.get(n) === this._activeSheet);
  }
  getSheetSize() {
    return this._snapshot.sheetOrder.length;
  }
  getSheets() {
    const { sheetOrder: e } = this._snapshot;
    return e.map((n) => this._worksheets.get(n));
  }
  getSheetsName() {
    const { sheetOrder: e } = this._snapshot, n = [];
    return e.forEach((r) => {
      const s = this._worksheets.get(r);
      s && n.push(s.getName());
    }), n;
  }
  getSheetIndex(e) {
    const { sheetOrder: n } = this._snapshot;
    return n.findIndex((r) => e.getSheetId() === r);
  }
  getSheetBySheetName(e) {
    const { sheetOrder: n } = this._snapshot, r = n.find((s) => this._worksheets.get(s).getName() === e);
    return this._worksheets.get(r);
  }
  getSheetBySheetId(e) {
    return this._worksheets.get(e);
  }
  getSheetByIndex(e) {
    const { sheetOrder: n } = this._snapshot;
    return this._worksheets.get(n[e]);
  }
  getHiddenWorksheets() {
    return this.getSheets().filter((e) => e.getConfig().hidden === we.TRUE).map((e) => e.getConfig().id);
  }
  getUnhiddenWorksheets() {
    return this.getSheets().filter((e) => e.getConfig().hidden !== we.TRUE).map((e) => e.getConfig().id);
  }
  load(e) {
    this._snapshot = e;
  }
  /**
   * Check if sheet name is unique
   * @param name sheet name
   * @returns True if sheet name is unique
   */
  checkSheetName(e) {
    return this.getSheetsName().includes(e);
  }
  /**
   *  Check whether the sheet name is unique and generate a new unique sheet name
   * @param name sheet name
   * @returns Unique sheet name
   */
  uniqueSheetName(e = "Sheet1") {
    let n = e;
    for (; this.checkSheetName(n); )
      n = e + this._count, this._count++;
    return n;
  }
  /**
   * Automatically generate new sheet name
   * @param name sheet name
   * @returns New sheet name
   */
  generateNewSheetName(e) {
    let n = e + this._count;
    for (; this.checkSheetName(n); )
      n = e + this._count, this._count++;
    return n;
  }
  // FIXME: now we always create worksheet from DEFAULT_WORKSHEET?
  /**
   * Get Default Sheet
   */
  _parseWorksheetSnapshots() {
    const { _snapshot: e, _worksheets: n } = this, { sheets: r, sheetOrder: s } = e;
    if (re.isEmptyObject(r)) {
      const i = re.generateRandomId();
      r[i] = { id: i };
    }
    for (const i in r) {
      const o = r[i], { name: a } = o;
      o.name = this.uniqueSheetName(a), o.name !== a && this._logService.debug("[Workbook]", `The worksheet name ${a} is duplicated, we changed it to ${o.name}. Please fix the problem in your snapshot.`);
      const u = new es(this._unitId, o, this._styles);
      n.set(i, u), s.includes(i) || s.push(i);
    }
    this.ensureActiveSheet();
  }
  /**
   * Get custom metadata of workbook
   * @returns {CustomData | undefined} custom metadata
   */
  getCustomMetadata() {
    return this._snapshot.custom;
  }
  /**
   * Set custom metadata of workbook
   * @param {CustomData | undefined} custom custom metadata
   */
  setCustomMetadata(e) {
    this._snapshot.custom = e;
  }
};
ts = sE([
  iE(1, Mt)
], ts);
class cl extends Ui {
  constructor(n) {
    var r;
    super();
    C(this, "type", Fe.UNIVER_SLIDE);
    C(this, "_activePage$", new lt(null));
    C(this, "activePage$", this._activePage$.asObservable());
    C(this, "_name$");
    C(this, "name$");
    C(this, "_snapshot");
    C(this, "_unitId");
    this._snapshot = { ...Ap, ...n }, this._unitId = (r = this._snapshot.id) != null ? r : re.generateRandomId(6), this._name$ = new lt(this._snapshot.title), this.name$ = this._name$.asObservable();
  }
  get _activePage() {
    var r, s;
    const n = this._activePage$.getValue();
    if (!n) {
      const i = (r = this.getPageOrder()) == null ? void 0 : r[0];
      return i ? (s = this.getPages()) == null ? void 0 : s[i] : null;
    }
    return n;
  }
  setName(n) {
    var r;
    this._snapshot.title = n, this._name$.next(n), this._unitId = (r = this._snapshot.id) != null ? r : qt(6);
  }
  getRev() {
    return 0;
  }
  incrementRev() {
  }
  setRev(n) {
  }
  getSnapshot() {
    return this._snapshot;
  }
  getUnitId() {
    return this._unitId;
  }
  getPages() {
    var n;
    return (n = this._snapshot.body) == null ? void 0 : n.pages;
  }
  getPageOrder() {
    var n;
    return (n = this._snapshot.body) == null ? void 0 : n.pageOrder;
  }
  getPage(n) {
    const r = this.getPages();
    return r == null ? void 0 : r[n];
  }
  getElementsByPage(n) {
    var r;
    return (r = this.getPage(n)) == null ? void 0 : r.pageElements;
  }
  getElement(n, r) {
    var s;
    return (s = this.getElementsByPage(n)) == null ? void 0 : s[r];
  }
  getPageSize() {
    return this._snapshot.pageSize;
  }
  getBlankPage() {
    const n = qt(6);
    return {
      id: n,
      pageType: Fu.SLIDE,
      zIndex: 10,
      title: n,
      description: "",
      pageBackgroundFill: {
        rgb: "rgb(255,255,255)"
      },
      pageElements: {}
    };
  }
  setActivePage(n) {
    this._activePage$.next(n);
  }
  getActivePage() {
    return this._activePage;
  }
  updatePage(n, r) {
    this._snapshot.body && (this._snapshot.body.pages[n] = r);
  }
  appendPage(n) {
    var i;
    if (!this._snapshot.body) return;
    this._snapshot.body.pages[n.id] = n;
    const r = this._activePage, s = this._snapshot.body.pageOrder.indexOf((i = r == null ? void 0 : r.id) != null ? i : "");
    this._snapshot.body.pageOrder.splice(s + 1, 0, n.id);
  }
}
const Ar = "FOCUSING_UNIT", Gn = "FOCUSING_SHEET", Nr = "FOCUSING_DOC", Tr = "FOCUSING_SLIDE", _R = "FOCUSING_EDITOR_BUT_HIDDEN", oE = "EDITOR_ACTIVATED", ER = "FOCUSING_EDITOR_INPUT_FORMULA", aE = "FOCUSING_FX_BAR_EDITOR", CR = "FOCUSING_UNIVER_EDITOR", RR = "FOCUSING_EDITOR_INPUT_FORMULA", IR = "FOCUSING_PANEL_EDITOR", vR = "FOCUSING_UNIVER_EDITOR_STANDALONE_SINGLE_MODE", yR = "FOCUSING_COMMON_DRAWINGS", wR = "FORMULA_EDITOR_ACTIVATED";
var uE = Object.defineProperty, lE = Object.getOwnPropertyDescriptor, cE = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? lE(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && uE(e, n, s), s;
}, Ea = (t, e) => (n, r) => e(n, r, t);
const _n = Ct("univer.current");
let ni = class extends nt {
  constructor(e, n) {
    super();
    C(this, "_unitsByType", /* @__PURE__ */ new Map());
    C(this, "_createHandler");
    C(this, "_ctorByType", /* @__PURE__ */ new Map());
    C(this, "_currentUnits", /* @__PURE__ */ new Map());
    C(this, "_currentUnits$", new lt(this._currentUnits));
    C(this, "currentUnits$", this._currentUnits$.asObservable());
    C(this, "_unitAdded$", new _t());
    C(this, "unitAdded$", this._unitAdded$.asObservable());
    C(this, "_unitDisposed$", new _t());
    C(this, "unitDisposed$", this._unitDisposed$.asObservable());
    C(this, "_focused$", new lt(null));
    C(this, "focused$", this._focused$.asObservable());
    this._injector = e, this._contextService = n;
  }
  dispose() {
    super.dispose(), this._focused$.complete();
  }
  __setCreateHandler(e) {
    this._createHandler = e;
  }
  createUnit(e, n, r) {
    return this._createHandler(e, n, this._ctorByType.get(e), r);
  }
  registerCtorForType(e, n) {
    return this._ctorByType.set(e, n), {
      dispose: () => {
        this._ctorByType.delete(e);
      }
    };
  }
  getCurrentTypeOfUnit$(e) {
    return this.currentUnits$.pipe(Da((n) => {
      var r;
      return (r = n.get(e)) != null ? r : null;
    }), Ml());
  }
  getCurrentUnitForType(e) {
    return this._currentUnits.get(e);
  }
  setCurrentUnitForType(e) {
    const n = this._getUnitById(e);
    if (!n) throw new Error(`[UniverInstanceService]: no document with unitId ${e}!`);
    this._currentUnits.set(n[1], n[0]), this._currentUnits$.next(this._currentUnits);
  }
  getTypeOfUnitAdded$(e) {
    return this._unitAdded$.pipe(Kt((n) => n.type === e));
  }
  /**
   * Add a unit into Univer.
   *
   * @ignore
   *
   * @param unit The unit to be added.
   */
  __addUnit(e, n) {
    var o;
    const r = e.type;
    this._unitsByType.has(r) || this._unitsByType.set(r, []);
    const s = this._unitsByType.get(r), i = e.getUnitId();
    if (s.findIndex((a) => a.getUnitId() === i) !== -1)
      throw new Error(`[UniverInstanceService]: cannot create a unit with the same unit id: ${i}.`);
    s.push(e), this._unitAdded$.next(e), ((o = n == null ? void 0 : n.makeCurrent) == null || o) && this.setCurrentUnitForType(e.getUnitId());
  }
  getTypeOfUnitDisposed$(e) {
    return this.unitDisposed$.pipe(Kt((n) => n.type === e));
  }
  getUnit(e, n) {
    var s;
    const r = (s = this._getUnitById(e)) == null ? void 0 : s[0];
    return n && (r == null ? void 0 : r.type) !== n ? null : r;
  }
  getCurrentUniverDocInstance() {
    return this.getCurrentUnitForType(Fe.UNIVER_DOC);
  }
  getUniverDocInstance(e) {
    return this.getUnit(e, Fe.UNIVER_DOC);
  }
  getUniverSheetInstance(e) {
    return this.getUnit(e, Fe.UNIVER_SHEET);
  }
  getAllUnitsForType(e) {
    var n;
    return (n = this._unitsByType.get(e)) != null ? n : [];
  }
  changeDoc(e, n) {
    const r = this.getAllUnitsForType(Fe.UNIVER_DOC), s = r.find((i) => i.getUnitId() === e);
    if (s != null) {
      const i = r.indexOf(s);
      r.splice(i, 1);
    }
    this.__addUnit(n);
  }
  get focused() {
    var n;
    const e = this._focused$.getValue();
    return e ? (n = this._getUnitById(e)) == null ? void 0 : n[0] : null;
  }
  focusUnit(e) {
    this._focused$.next(e), this.focused instanceof ts ? (this._contextService.setContextValue(Ar, !0), this._contextService.setContextValue(Nr, !1), this._contextService.setContextValue(Gn, !0), this._contextService.setContextValue(Tr, !1), this.setCurrentUnitForType(e)) : this.focused instanceof jt ? (this._contextService.setContextValue(Ar, !0), this._contextService.setContextValue(Nr, !0), this._contextService.setContextValue(Gn, !1), this._contextService.setContextValue(Tr, !1), this.setCurrentUnitForType(e)) : this.focused instanceof cl ? (this._contextService.setContextValue(Ar, !0), this._contextService.setContextValue(Nr, !1), this._contextService.setContextValue(Gn, !1), this._contextService.setContextValue(Tr, !0), this.setCurrentUnitForType(e)) : (this._contextService.setContextValue(Ar, !1), this._contextService.setContextValue(Nr, !1), this._contextService.setContextValue(Gn, !1), this._contextService.setContextValue(Tr, !1));
  }
  getFocusedUnit() {
    return this.focused;
  }
  getUnitType(e) {
    const n = this._getUnitById(e);
    return n ? n[1] : Fe.UNRECOGNIZED;
  }
  disposeUnit(e) {
    const n = this._getUnitById(e);
    if (!n) return !1;
    const [r, s] = n, i = this._unitsByType.get(s), o = i.indexOf(r);
    return i.splice(o, 1), this._tryRemoveCurrentUnitForType(e, s), this._tryBlurUnitOnRemoval(e), this._unitDisposed$.next(r), !0;
  }
  _tryRemoveCurrentUnitForType(e, n) {
    const r = this.getCurrentUnitForType(n);
    (r == null ? void 0 : r.getUnitId()) === e && (this._currentUnits.set(n, null), this._currentUnits$.next(this._currentUnits));
  }
  _tryBlurUnitOnRemoval(e) {
    var n;
    ((n = this.focused) == null ? void 0 : n.getUnitId()) === e && this._focused$.next(null);
  }
  _getUnitById(e) {
    for (const [n, r] of this._unitsByType) {
      const s = r.find((i) => i.getUnitId() === e);
      if (s)
        return [s, n];
    }
  }
};
ni = cE([
  Ea(0, ot(Ot)),
  Ea(1, fs)
], ni);
var Ve = /* @__PURE__ */ ((t) => (t[t.Starting = 0] = "Starting", t[t.Ready = 1] = "Ready", t[t.Rendered = 2] = "Rendered", t[t.Steady = 3] = "Steady", t))(Ve || {});
const hE = {
  0: "Starting",
  1: "Ready",
  2: "Rendered",
  3: "Steady"
};
var dE = Object.defineProperty, fE = Object.getOwnPropertyDescriptor, gE = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? fE(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && dE(e, n, s), s;
}, pE = (t, e) => (n, r) => e(n, r, t);
let Ht = class extends nt {
  constructor(e) {
    super();
    C(this, "_lifecycle$", new lt(Ve.Starting));
    C(this, "lifecycle$", this._lifecycle$.asObservable());
    C(this, "_lock", !1);
    this._logService = e, this._reportProgress(Ve.Starting);
  }
  get stage() {
    return this._lifecycle$.getValue();
  }
  set stage(e) {
    if (this._lock) throw new Error("[LifecycleService]: cannot set new stage when related logic is all handled!");
    if (e < this.stage) throw new Error("[LifecycleService]: lifecycle stage cannot go backward!");
    e !== this.stage && (this._lock = !0, this._reportProgress(e), this._lifecycle$.next(e), this._lock = !1);
  }
  dispose() {
    this._lifecycle$.complete(), super.dispose();
  }
  /**
   * Subscribe to lifecycle changes and all previous stages and the current
   * stage will be emitted immediately.
   * @returns
   */
  subscribeWithPrevious() {
    return xa(hl(this.stage), this._lifecycle$.pipe(La(1))).pipe(Kf((e) => e === Ve.Steady));
  }
  _reportProgress(e) {
    this._logService.debug("[LifecycleService]", `lifecycle progressed to "${hE[e]}".`);
  }
};
Ht = gE([
  pE(0, Mt)
], Ht);
function hl(t) {
  switch (t) {
    case Ve.Starting:
      return fr(Ve.Starting);
    case Ve.Ready:
      return fr(Ve.Starting, Ve.Ready);
    case Ve.Rendered:
      return fr(Ve.Starting, Ve.Ready, Ve.Rendered);
    default:
      return fr(
        Ve.Starting,
        Ve.Ready,
        Ve.Rendered,
        Ve.Steady
      );
  }
}
var mE = Object.defineProperty, _E = Object.getOwnPropertyDescriptor, EE = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? _E(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && mE(e, n, s), s;
}, xs = (t, e) => (n, r) => e(n, r, t);
const cn = Ct("univer.undo-redo.service"), CE = 20;
class dl {
  dispose() {
  }
  async dispatchToHandlers() {
    return !1;
  }
}
const RE = "univer.command.redo", IE = "univer.command.undo", Nn = new class extends dl {
  constructor() {
    super(...arguments);
    C(this, "type", ar.COMMAND);
    C(this, "id", IE);
  }
  handler(e) {
    const n = e.get(cn), r = n.pitchTopUndoElement();
    if (!r)
      return !1;
    const s = e.get(Pt);
    return mu(r.undoMutations, s) ? (n.popUndoToRedo(), !0) : !1;
  }
}(), Tn = new class extends dl {
  constructor() {
    super(...arguments);
    C(this, "type", ar.COMMAND);
    C(this, "id", RE);
  }
  handler(e) {
    const n = e.get(cn), r = n.pitchTopRedoElement();
    if (!r)
      return !1;
    const s = e.get(Pt);
    return mu(r.redoMutations, s) ? (n.popRedoToUndo(), !0) : !1;
  }
}();
let ri = class extends nt {
  constructor(e, n, r) {
    super();
    C(this, "undoRedoStatus$");
    C(this, "_undoRedoStatus$", new lt({ undos: 0, redos: 0 }));
    // Undo and redo stacks are per unit.
    C(this, "_undoStacks", /* @__PURE__ */ new Map());
    C(this, "_redoStacks", /* @__PURE__ */ new Map());
    C(this, "_batchingStatus", /* @__PURE__ */ new Map());
    this._univerInstanceService = e, this._commandService = n, this._contextService = r, this.undoRedoStatus$ = this._undoRedoStatus$.asObservable(), this.disposeWithMe(this._commandService.registerCommand(Nn)), this.disposeWithMe(this._commandService.registerCommand(Tn)), this.disposeWithMe(Ze(() => this._undoRedoStatus$.complete())), this.disposeWithMe(Ze(this._univerInstanceService.focused$.subscribe(() => this._updateStatus())));
  }
  pushUndoRedo(e) {
    const { unitID: n } = e, r = this._getRedoStack(n, !0), s = this._getUndoStack(n, !0);
    if (r.length = 0, this._batchingStatus.has(e.unitID)) {
      const o = this._batchingStatus.get(e.unitID), a = this._pitchUndoElement(e.unitID);
      o === 0 || !a ? (i(e), this._batchingStatus.set(
        e.unitID,
        1
        /* CREATED */
      )) : this._tryBatchingElements(a, e);
    } else
      i(e);
    function i(o) {
      s.push(o), s.length > CE && s.splice(0, 1);
    }
    this._updateStatus();
  }
  clearUndoRedo(e) {
    const n = this._getRedoStack(e);
    n && (n.length = 0);
    const r = this._getUndoStack(e);
    r && (r.length = 0), this._updateStatus();
  }
  pitchTopUndoElement() {
    const e = this._getFocusedUnitId();
    return this._pitchUndoElement(e);
  }
  pitchTopRedoElement() {
    const e = this._getFocusedUnitId();
    return this._pitchRedoElement(e);
  }
  _pitchUndoElement(e) {
    const n = this._getUndoStack(e);
    return n != null && n.length ? n[n.length - 1] : null;
  }
  _pitchRedoElement(e) {
    const n = this._getRedoStack(e);
    return n != null && n.length ? n[n.length - 1] : null;
  }
  popUndoToRedo() {
    const n = this._getUndoStackForFocused().pop();
    n && (this._getRedoStackForFocused().push(n), this._updateStatus());
  }
  popRedoToUndo() {
    const n = this._getRedoStackForFocused().pop();
    n && (this._getUndoStackForFocused().push(n), this._updateStatus());
  }
  __tempBatchingUndoRedo(e) {
    if (this._batchingStatus.has(e))
      throw new Error("[LocalUndoRedoService]: cannot batching undo redo twice at the same time!");
    return this._batchingStatus.set(
      e,
      0
      /* WAITING */
    ), Ze(() => this._batchingStatus.delete(e));
  }
  _updateStatus() {
    var s, i;
    const e = this._getFocusedUnitId(), n = e && ((s = this._undoStacks.get(e)) == null ? void 0 : s.length) || 0, r = e && ((i = this._redoStacks.get(e)) == null ? void 0 : i.length) || 0;
    this._undoRedoStatus$.next({
      undos: n,
      redos: r
    });
  }
  _getUndoStack(e, n = !1) {
    let r = this._undoStacks.get(e);
    return !r && n && (r = [], this._undoStacks.set(e, r)), r || null;
  }
  _getRedoStack(e, n = !1) {
    let r = this._redoStacks.get(e);
    return !r && n && (r = [], this._redoStacks.set(e, r)), r || null;
  }
  _getUndoStackForFocused() {
    const e = this._getFocusedUnitId();
    if (!e)
      throw new Error("No focused univer instance!");
    return this._getUndoStack(e, !0);
  }
  _getRedoStackForFocused() {
    const e = this._getFocusedUnitId();
    if (!e)
      throw new Error("No focused univer instance!");
    return this._getRedoStack(e, !0);
  }
  _tryBatchingElements(e, n) {
    e.redoMutations.push(...n.redoMutations), e.undoMutations.push(...n.undoMutations);
  }
  _getFocusedUnitId() {
    var i, o, a, u;
    let e = "";
    const n = this._contextService.getContextValue(Gn), r = this._contextService.getContextValue(aE), s = this._contextService.getContextValue(oE);
    return n ? r ? e = iu : s ? e = su : e = (o = (i = this._univerInstanceService.getFocusedUnit()) == null ? void 0 : i.getUnitId()) != null ? o : "" : e = (u = (a = this._univerInstanceService.getFocusedUnit()) == null ? void 0 : a.getUnitId()) != null ? u : "", e;
  }
};
ri = EE([
  xs(0, _n),
  xs(1, Pt),
  xs(2, fs)
], ri);
const Bi = Ct("core.resource-manager.service"), si = {
  [Tt.Editor]: "Editor",
  [Tt.Owner]: "Owner",
  [Tt.Reader]: "Reader",
  [Tt.UNRECOGNIZED]: "UNRECOGNIZED"
}, ii = (t) => t ? {
  userID: `${si[t]}_${re.generateRandomId(8)}`,
  name: si[t],
  avatar: ""
} : {
  userID: "",
  name: "",
  avatar: "",
  anonymous: !0,
  canBindAnonymous: !1
}, vE = (t, e) => t.startsWith(si[e]);
class rr {
  constructor() {
    C(this, "_model", /* @__PURE__ */ new Map());
    C(this, "_userChange$", new _t());
    C(this, "userChange$", this._userChange$.asObservable());
    C(this, "_currentUser$", new lt(ii()));
    /**
     * When the current user undergoes a switch or change
     * @memberof UserManagerService
     */
    C(this, "currentUser$", this._currentUser$.asObservable());
  }
  getCurrentUser() {
    return this._currentUser$.getValue();
  }
  setCurrentUser(e) {
    this.addUser(e), this._currentUser$.next(e);
  }
  addUser(e) {
    this._model.set(e.userID, e), this._userChange$.next({ type: "add", user: e });
  }
  getUser(e, n) {
    const r = this._model.get(e);
    if (r)
      return r;
    n && n();
  }
  delete(e) {
    const n = this.getUser(e);
    this._model.delete(e), n && this._userChange$.next({ type: "delete", user: n });
  }
  clear() {
    this._model.clear(), this._userChange$.next({ type: "clear" });
  }
  list() {
    return Array.from(this._model.values());
  }
}
var yE = Object.defineProperty, wE = Object.getOwnPropertyDescriptor, OE = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? wE(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && yE(e, n, s), s;
}, Ca = (t, e) => (n, r) => e(n, r, t);
let oi = class {
  // private _sheetPermissionPointMap: Map<string, { action: UnitAction; allowed: boolean }[]> = new Map();
  constructor(t, e) {
    C(this, "_permissionMap", /* @__PURE__ */ new Map([]));
    this._resourceManagerService = t, this._userManagerService = e, this._initSnapshot(), this._initDefaultUser();
  }
  _initDefaultUser() {
    const t = this._userManagerService.getCurrentUser();
    t && t.userID || this._userManagerService.setCurrentUser(ii(Tt.Owner));
  }
  _getRole(t) {
    const e = this._userManagerService.getCurrentUser();
    return e ? vE(e.userID, t) : !1;
  }
  _initSnapshot() {
    this._resourceManagerService.registerPluginResource({
      toJson: (t) => {
        const e = [...this._permissionMap.keys()].reduce((n, r) => {
          const s = this._permissionMap.get(r);
          return n[r] = s, n;
        }, {});
        return JSON.stringify(e);
      },
      parseJson: (t) => JSON.parse(t),
      pluginName: "SHEET_AuthzIoMockService_PLUGIN",
      businesses: [Fe.UNIVER_SHEET, Fe.UNIVER_DOC, Fe.UNIVER_SLIDE],
      onLoad: (t, e) => {
        for (const n in e)
          this._permissionMap.set(n, e[n]);
      },
      onUnLoad: () => {
        this._permissionMap.clear();
      }
    });
  }
  async create(t) {
    return qt(8);
  }
  async allowed(t) {
    return Promise.resolve([]);
  }
  async batchAllowed(t) {
    return Promise.resolve([]);
  }
  // eslint-disable-next-line max-lines-per-function
  async list(t) {
    const e = [];
    return t.objectIDs.forEach((n) => {
      const r = this._permissionMap.get(n);
      if (r) {
        const s = {
          objectID: n,
          unitID: t.unitID,
          objectType: r.objectType,
          name: r.name,
          shareOn: !1,
          shareRole: Tt.Owner,
          shareScope: -1,
          scope: {
            read: Js.AllCollaborator,
            edit: Js.AllCollaborator
          },
          creator: ii(Tt.Owner),
          strategies: [
            {
              action: 6,
              role: 1
            },
            {
              action: 16,
              role: 1
            },
            {
              action: 17,
              role: 1
            },
            {
              action: 18,
              role: 1
            },
            {
              action: 19,
              role: 1
            },
            {
              action: 33,
              role: 1
            },
            {
              action: 34,
              role: 1
            },
            {
              action: 35,
              role: 1
            },
            {
              action: 36,
              role: 1
            },
            {
              action: 37,
              role: 1
            },
            {
              action: 38,
              role: 1
            },
            {
              action: 39,
              role: 1
            },
            {
              action: 40,
              role: 1
            }
          ],
          actions: t.actions.map((i) => ({ action: i, allowed: this._getRole(Tt.Owner) || this._getRole(Tt.Editor) }))
        };
        e.push(s);
      }
    }), e;
  }
  async listCollaborators() {
    return [];
  }
  async listRoles() {
    return {
      roles: [],
      actions: []
    };
  }
  async deleteCollaborator() {
  }
  async update(t) {
  }
  async updateCollaborator() {
  }
  async createCollaborator() {
  }
  async putCollaborators(t) {
  }
};
oi = OE([
  Ca(0, Bi),
  Ca(1, ot(rr))
], oi);
const bE = Ct("IAuthzIoIoService"), SE = Ct("univer.config-service");
class AE {
  constructor() {
    C(this, "_configChanged$", new _t());
    C(this, "configChanged$", this._configChanged$.asObservable());
    C(this, "_config", /* @__PURE__ */ new Map());
  }
  dispose() {
    this._configChanged$.complete();
  }
  getConfig(e) {
    return this._config.get(e);
  }
  setConfig(e, n, r) {
    var o;
    const { merge: s = !1 } = r || {};
    let i = (o = this._config.get(e)) != null ? o : {};
    s ? i = nu(i, n) : i = n, this._config.set(e, i), this._configChanged$.next({ [e]: i });
  }
  deleteConfig(e) {
    return this._config.delete(e);
  }
  subscribeConfigValue$(e) {
    return new sr((n) => {
      Object.prototype.hasOwnProperty.call(this._config, e) && n.next(this._config.get(e));
      const r = this.configChanged$.pipe(Kt((s) => Object.prototype.hasOwnProperty.call(s, e))).subscribe((s) => n.next(s[e]));
      return () => r.unsubscribe();
    });
  }
}
class NE extends nt {
  constructor() {
    super(...arguments);
    C(this, "_error$", new _t());
    C(this, "error$", this._error$.asObservable());
  }
  dispose() {
    this._error$.complete();
  }
  emit(n) {
    this._error$.next({ errorKey: n });
  }
}
class Vr extends nt {
  constructor() {
    super();
    C(this, "_currentLocale$", new lt(ur.ZH_CN));
    C(this, "currentLocale$", this._currentLocale$.asObservable());
    C(this, "_locales", null);
    C(this, "localeChanged$", new _t());
    /**
     * Translate a key to the current locale
     *
     * @param {string} key the key to translate
     * @param {string[]} args optional arguments to replace in the translated string
     * @returns {string} the translated string
     *
     * @example
     * const locales = {
     *   [LocaleType.EN_US]: {
     *     foo: {
     *       bar: 'Hello'
     *    }
     * }
     * t('foo.bar') => 'Hello'
     *
     * @example
     * const locales = {
     *   [LocaleType.EN_US]: {
     *     foo: {
     *       bar: 'Hello {0}'
     *    }
     * }
     * t('foo.bar', 'World') => 'Hello World'
     */
    C(this, "t", (n, ...r) => {
      if (!this._locales) throw new Error("[LocaleService]: Locale not initialized");
      const s = n.split("."), i = this.resolveKeyPath(this._locales[this._currentLocale], s);
      if (typeof i == "string") {
        let o = i;
        return r.forEach((a, u) => {
          o = o.replace(`{${u}}`, a);
        }), o;
      } else
        return n;
    });
    this.disposeWithMe(Ze(() => this.localeChanged$.complete()));
  }
  get _currentLocale() {
    return this._currentLocale$.value;
  }
  /**
   * Load more locales after init.
   *
   * @param locales - Locale object
   */
  load(n) {
    var r;
    this._locales = nu((r = this._locales) != null ? r : {}, n);
  }
  setLocale(n) {
    this._currentLocale$.next(n), this.localeChanged$.next();
  }
  getLocales() {
    var n;
    return (n = this._locales) == null ? void 0 : n[this._currentLocale];
  }
  getCurrentLocale() {
    return this._currentLocale;
  }
  resolveKeyPath(n, r) {
    const s = r.shift();
    if (s && n && s in n) {
      const i = n[s];
      return r.length > 0 && (typeof i == "object" || Array.isArray(i)) ? this.resolveKeyPath(i, r) : i;
    }
    return null;
  }
}
var TE = Object.defineProperty, ME = Object.getOwnPropertyDescriptor, DE = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? ME(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && TE(e, n, s), s;
}, xE = (t, e) => (n, r) => e(n, r, t);
let ai = class {
  constructor(t) {
    this._userManagerService = t;
  }
  async list(t) {
    return {
      list: [{
        type: Zr.PERSON,
        mentions: [
          {
            objectType: Zr.PERSON,
            objectId: this._userManagerService.getCurrentUser().userID,
            label: this._userManagerService.getCurrentUser().name,
            metadata: {
              icon: this._userManagerService.getCurrentUser().avatar
            }
          }
        ],
        metadata: {},
        title: "PEOPLE"
      }],
      page: t.page,
      size: t.size,
      total: 1
    };
  }
};
ai = DE([
  xE(0, ot(rr))
], ai);
const LE = Ct("univer.service.mention-io");
var fl = /* @__PURE__ */ ((t) => (t.INIT = "init", t.FETCHING = "fetching", t.DONE = "done", t))(fl || {});
const UE = Ct("univer.permission-service");
class PE extends nt {
  constructor() {
    super(...arguments);
    C(this, "_permissionPointMap", /* @__PURE__ */ new Map());
    C(this, "_permissionPointUpdate$", new _t());
    C(this, "permissionPointUpdate$", this._permissionPointUpdate$.asObservable());
    C(this, "_showComponents", !0);
  }
  setShowComponents(n) {
    this._showComponents = n;
  }
  getShowComponents() {
    return this._showComponents;
  }
  deletePermissionPoint(n) {
    const r = this._permissionPointMap.get(n);
    r && (r.complete(), this._permissionPointMap.delete(n));
  }
  addPermissionPoint(n) {
    const r = n instanceof lt, s = r ? n.getValue() : n;
    if (!s.id)
      return !1;
    if (this._permissionPointMap.get(s.id))
      throw new Error(`${s.id} PermissionPoint already exists`);
    return this._permissionPointMap.set(s.id, r ? n : new lt(s)), this._permissionPointUpdate$.next(s), !0;
  }
  updatePermissionPoint(n, r) {
    const s = this._permissionPointMap.get(n);
    if (!s)
      return;
    const i = s.getValue();
    i.value = r, i.status = fl.DONE, s.next(i), this._permissionPointUpdate$.next(i);
  }
  clearPermissionMap() {
    this._permissionPointMap.clear();
  }
  getPermissionPoint(n) {
    const r = this._permissionPointMap.get(n);
    if (r)
      return r.getValue();
  }
  getPermissionPoint$(n) {
    const r = this._permissionPointMap.get(n);
    if (r)
      return r;
  }
  composePermission$(n) {
    const r = n.map((s) => {
      var o;
      const i = (o = this._permissionPointMap) == null ? void 0 : o.get(s);
      if (!i)
        throw new Error(`[PermissionService]: ${s} permissionPoint does not exist!`);
      return i.asObservable();
    });
    return Dl(r).pipe(
      // Check that all permissions exist
      Pl((s) => s)
    );
  }
  composePermission(n) {
    return n.map((s) => {
      var o;
      const i = (o = this._permissionPointMap) == null ? void 0 : o.get(s);
      if (!i)
        throw new Error(`[PermissionService]: ${s} permissionPoint does not exist!`);
      return i.getValue();
    });
  }
  getAllPermissionPoint() {
    const n = /* @__PURE__ */ new Map();
    return this._permissionPointMap.forEach((r, s) => {
      n.set(s, r);
    }), n;
  }
}
function kE(t, e) {
  if (!e) return t;
  const n = [];
  for (const r of t) {
    const s = e.find(([i]) => i === r[0]);
    if (s) {
      if (s[1] === null) continue;
      n.push([r[0], s[1]]);
    } else
      n.push(r);
  }
  return n;
}
const gl = Symbol("DependentOn");
class Ra extends nt {
  onStarting() {
  }
  onReady() {
  }
  onRendered() {
  }
  onSteady() {
  }
  getUniverInstanceType() {
    return this.constructor.type;
  }
  getPluginName() {
    return this.constructor.pluginName;
  }
}
C(Ra, "pluginName"), C(Ra, "type", Fe.UNIVER_UNKNOWN);
class FE {
  constructor() {
    C(this, "_plugins", []);
  }
  addPlugin(e) {
    this._plugins.push(e);
  }
  removePlugins() {
    const e = this._plugins.slice();
    return this._plugins.length = 0, e;
  }
  forEachPlugin(e) {
    this._plugins.forEach(e);
  }
}
class $E {
  constructor() {
    C(this, "_pluginsRegistered", []);
  }
  // eslint-disable-next-line ts/no-explicit-any
  registerPlugin(e, n) {
    this._pluginsRegistered.push({ plugin: e, options: n });
  }
  getRegisterPlugins() {
    return this._pluginsRegistered.slice();
  }
  removePlugins() {
    this._pluginsRegistered = [];
  }
}
var BE = Object.defineProperty, jE = Object.getOwnPropertyDescriptor, pl = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? jE(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && BE(e, n, s), s;
}, Gr = (t, e) => (n, r) => e(n, r, t);
const HE = 4;
function OR(...t) {
  return function(e) {
    e[gl] = t;
  };
}
let ns = class {
  constructor(t) {
    C(this, "_pluginHolderForUniver");
    C(this, "_pluginHoldersForTypes", /* @__PURE__ */ new Map());
    C(this, "_seenPlugins", /* @__PURE__ */ new Set());
    C(this, "_flushTimer");
    this._injector = t, this._pluginHolderForUniver = this._injector.createInstance(
      rs,
      this._checkPluginSeen.bind(this),
      this._immediateInitPlugin.bind(this)
    ), this._pluginHoldersForTypes.set(Fe.UNIVER_UNKNOWN, this._pluginHolderForUniver), this._pluginHolderForUniver.start();
  }
  dispose() {
    this._clearFlushTimer();
    for (const t of this._pluginHoldersForTypes.values())
      t.dispose();
    this._pluginHolderForUniver.dispose();
  }
  /** Register a plugin into univer. */
  registerPlugin(t, e) {
    this._assertPluginValid(t), this._scheduleInitPlugin();
    const { type: n } = t;
    n === Fe.UNIVER_UNKNOWN ? (this._pluginHolderForUniver.register(t, e), this._pluginHolderForUniver.flush()) : this._ensurePluginHolderForType(n).register(t, e);
  }
  startPluginForType(t) {
    this._ensurePluginHolderForType(t).start();
  }
  _ensurePluginHolderForType(t) {
    if (!this._pluginHoldersForTypes.has(t)) {
      const e = this._injector.createInstance(
        rs,
        this._checkPluginSeen.bind(this),
        this._immediateInitPlugin.bind(this)
      );
      return this._pluginHoldersForTypes.set(t, e), e;
    }
    return this._pluginHoldersForTypes.get(t);
  }
  _immediateInitPlugin(t) {
    this._seenPlugins.add(t.pluginName), this._ensurePluginHolderForType(t.type).immediateInitPlugin(t);
  }
  _checkPluginSeen(t) {
    return this._seenPlugins.has(t.pluginName);
  }
  _assertPluginValid(t) {
    const { type: e, pluginName: n } = t;
    if (e === Fe.UNRECOGNIZED)
      throw new Error(`[PluginService]: invalid plugin type for ${t.name}. Please assign a "type" to your plugin.`);
    if (!n)
      throw new Error(`[PluginService]: no plugin name for ${t.name}. Please assign a "pluginName" to your plugin.`);
    if (this._seenPlugins.has(n))
      throw new Error(`[PluginService]: duplicated plugin name for "${n}". Maybe a plugin that dependents on "${n} has already registered it. In that case please register "${n}" before the that plugin.`);
    this._seenPlugins.add(t.pluginName);
  }
  _scheduleInitPlugin() {
    this._flushTimer === void 0 && (this._flushTimer = setTimeout(
      () => {
        this._pluginHolderForUniver.started || this._pluginHolderForUniver.start(), this._flushPlugins(), this._clearFlushTimer();
      },
      HE
    ));
  }
  _clearFlushTimer() {
    this._flushTimer && (clearTimeout(this._flushTimer), this._flushTimer = void 0);
  }
  _flushPlugins() {
    this._pluginHolderForUniver.flush();
    for (const [t, e] of this._pluginHoldersForTypes)
      e.started && e.flush();
  }
};
ns = pl([
  Gr(0, ot(Ot))
], ns);
let rs = class extends nt {
  constructor(e, n, r, s, i) {
    super();
    C(this, "_started", !1);
    C(this, "_warnedAboutOnStartingDeprecation", !1);
    /** Plugin constructors waiting to be initialized. */
    C(this, "_pluginRegistry", new $E());
    /** Stores initialized plugin instances. */
    C(this, "_pluginStore", new FE());
    /** Plugins instances as they are registered in batches. */
    C(this, "_pluginsInBatches", []);
    this._checkPluginRegistered = e, this._registerPlugin = n, this._logService = r, this._injector = s, this._lifecycleService = i, this.disposeWithMe(this._lifecycleService.lifecycle$.pipe(La(1)).subscribe((o) => {
      this._pluginsInBatches.forEach((a) => this._runStage(a, o));
    }));
  }
  get started() {
    return this._started;
  }
  dispose() {
    super.dispose(), this._pluginStore.forEachPlugin((e) => e.dispose()), this._pluginStore.removePlugins(), this._pluginRegistry.removePlugins(), this._pluginsInBatches.length = 0;
  }
  register(e, n) {
    this._pluginRegistry.registerPlugin(e, n);
  }
  immediateInitPlugin(e) {
    const n = this._initPlugin(e, void 0);
    this._pluginsRunLifecycle([n]);
  }
  start() {
    this._started || (this._started = !0, this.flush());
  }
  flush() {
    if (!this._started)
      return;
    const e = this._pluginRegistry.getRegisterPlugins().map(({ plugin: n, options: r }) => this._initPlugin(n, r));
    e.length && (this._pluginsRunLifecycle(e), this._pluginRegistry.removePlugins());
  }
  // eslint-disable-next-line ts/no-explicit-any
  _initPlugin(e, n) {
    const r = e[gl];
    if (r) {
      const i = () => {
        const o = r.find((a) => !this._checkPluginRegistered(a));
        return o ? (this._logService.debug(
          "[PluginService]",
          `Plugin "${e.pluginName}" depends on "${o.pluginName}" which is not registered. Univer will automatically register it with default configuration.`
        ), this._registerPlugin(o, void 0), !0) : !1;
      };
      for (; i(); )
        ;
    }
    const s = this._injector.createInstance(e, n);
    return this._pluginStore.addPlugin(s), this._logService.debug("[PluginService]", `Plugin "${s.getPluginName()}" registered.`), s;
  }
  // Here we should be careful with the sequence of which plugin should run first. We should manually add a queue here.
  // Because lately registered plugins may get executed first.
  _pluginsRunLifecycle(e) {
    hl(this._lifecycleService.stage).subscribe((n) => this._runStage(e, n)), this._pluginsInBatches.push(e);
  }
  _runStage(e, n) {
    e.forEach((r) => {
      switch (n) {
        case Ve.Starting:
          r.onStarting();
          break;
        case Ve.Ready:
          r.onReady();
          break;
        case Ve.Rendered:
          r.onRendered();
          break;
        case Ve.Steady:
          r.onSteady();
          break;
      }
    });
  }
};
rs = pl([
  Gr(2, Mt),
  Gr(3, ot(Ot)),
  Gr(4, ot(Ht))
], rs);
var WE = Object.defineProperty, zE = Object.getOwnPropertyDescriptor, YE = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? zE(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && WE(e, n, s), s;
}, Ia = (t, e) => (n, r) => e(n, r, t);
let ui = class extends nt {
  constructor(t, e) {
    super(), this._resourceManagerService = t, this._univerInstanceService = e, this._init();
  }
  _init() {
    const t = (n) => {
      n.businesses.forEach((r) => {
        switch (r) {
          case Fe.UNRECOGNIZED:
          case Fe.UNIVER_UNKNOWN:
          case Fe.UNIVER_SLIDE:
          case Fe.UNIVER_DOC: {
            this._univerInstanceService.getAllUnitsForType(Fe.UNIVER_DOC).forEach((s) => {
              const o = (s.getSnapshot().resources || []).find((a) => a.name === n.pluginName);
              if (o)
                try {
                  const a = n.parseJson(o.data);
                  n.onLoad(s.getUnitId(), a);
                } catch {
                  console.error(`Load Document{${s.getUnitId()}} Resources{${n.pluginName}} Data Error.`);
                }
            });
            break;
          }
          case Fe.UNIVER_SHEET:
            this._univerInstanceService.getAllUnitsForType(Fe.UNIVER_SHEET).forEach((s) => {
              const o = (s.getSnapshot().resources || []).find((a) => a.name === n.pluginName);
              if (o)
                try {
                  const a = n.parseJson(o.data);
                  n.onLoad(s.getUnitId(), a);
                } catch {
                  console.error(`Load Workbook{${s.getUnitId()}} Resources{${n.pluginName}} Data Error.`);
                }
            });
        }
      });
    };
    this._resourceManagerService.getAllResourceHooks().forEach((n) => t(n)), this.disposeWithMe(this._resourceManagerService.register$.subscribe((n) => t(n))), this.disposeWithMe(
      this._univerInstanceService.getTypeOfUnitAdded$(Fe.UNIVER_SHEET).subscribe((n) => {
        this._resourceManagerService.loadResources(n.getUnitId(), n.getSnapshot().resources);
      })
    ), this.disposeWithMe(
      this._univerInstanceService.getTypeOfUnitAdded$(Fe.UNIVER_DOC).subscribe((n) => {
        const r = n.getUnitId();
        zd(r) || this._resourceManagerService.loadResources(n.getUnitId(), n.getSnapshot().resources);
      })
    ), this.disposeWithMe(
      this._univerInstanceService.getTypeOfUnitDisposed$(Fe.UNIVER_SHEET).subscribe((n) => {
        this._resourceManagerService.unloadResources(n.getUnitId());
      })
    ), this.disposeWithMe(
      this._univerInstanceService.getTypeOfUnitDisposed$(Fe.UNIVER_DOC).subscribe((n) => {
        this._resourceManagerService.unloadResources(n.getUnitId());
      })
    );
  }
  saveUnit(t) {
    const e = this._univerInstanceService.getUnit(t);
    if (!e)
      return null;
    const n = this._resourceManagerService.getResources(t, e.type), r = re.deepClone(e.getSnapshot());
    return r.resources = n, r;
  }
};
ui = YE([
  Ia(0, ot(Bi)),
  Ia(1, ot(_n))
], ui);
const va = Ct("resource-loader-service");
class VE extends nt {
  constructor() {
    super(...arguments);
    C(this, "_resourceMap", /* @__PURE__ */ new Map());
    C(this, "_register$", new _t());
    C(this, "register$", this._register$.asObservable());
  }
  getAllResourceHooks() {
    return [...this._resourceMap.values()];
  }
  getResources(n, r) {
    return r ? this.getResourcesByType(n, r) : this.getAllResourceHooks().map((o) => {
      const a = o.toJson(n);
      return {
        name: o.pluginName,
        data: a
      };
    });
  }
  getResourcesByType(n, r) {
    return this.getAllResourceHooks().filter((o) => o.businesses.includes(r)).map((o) => {
      const a = o.toJson(n);
      return {
        name: o.pluginName,
        data: a
      };
    });
  }
  registerPluginResource(n) {
    const r = n.pluginName;
    if (this._resourceMap.has(r))
      throw new Error(`the pluginName is registered {${r}}`);
    return this._resourceMap.set(r, n), this._register$.next(n), Ze(() => this._resourceMap.delete(r));
  }
  disposePluginResource(n) {
    this._resourceMap.delete(n);
  }
  loadResources(n, r) {
    this.getAllResourceHooks().forEach((s) => {
      var o;
      const i = (o = r == null ? void 0 : r.find((a) => a.name === s.pluginName)) == null ? void 0 : o.data;
      if (i)
        try {
          const a = s.parseJson(i);
          s.onLoad(n, a);
        } catch {
          console.error("LoadResources Error!");
        }
    });
  }
  unloadResources(n) {
    this.getAllResourceHooks().forEach((r) => {
      r.onUnLoad(n);
    });
  }
  dispose() {
    this._register$.complete(), this._resourceMap.clear();
  }
}
class ml extends nt {
  constructor() {
    super();
    C(this, "_currentTheme");
    C(this, "_currentTheme$", new lt({}));
    C(this, "currentTheme$", this._currentTheme$.asObservable());
    this.disposeWithMe(Ze(() => this._currentTheme$.complete()));
  }
  getCurrentTheme() {
    if (!this._currentTheme)
      throw new Error("[ThemeService]: current theme is not set!");
    return this._currentTheme;
  }
  setTheme(n) {
    this._currentTheme = n, this._currentTheme$.next(n);
  }
}
class GE {
  /**
   * Create a Univer instance.
   * @param config Configuration data for Univer
   * @param parentInjector An optional parent injector of the Univer injector. For more information, see https://redi.wendell.fun/docs/hierarchy.
   */
  constructor(e = {}, n) {
    C(this, "_startedTypes", /* @__PURE__ */ new Set());
    C(this, "_injector");
    C(this, "_disposingCallbacks", new Mi());
    const r = this._injector = KE(n, e == null ? void 0 : e.override), { theme: s, locale: i, locales: o, logLevel: a } = e;
    s && this._injector.get(ml).setTheme(s), o && this._injector.get(Vr).load(o), i && this._injector.get(Vr).setLocale(i), a && this._injector.get(Mt).setLogLevel(a), this._init(r);
  }
  get _univerInstanceService() {
    return this._injector.get(_n);
  }
  get _pluginService() {
    return this._injector.get(ns);
  }
  __getInjector() {
    return this._injector;
  }
  /**
   * Register a callback function which will be called when this Univer instance is disposing.
   *
   * @ignore
   *
   * @param callback The callback function.
   * @returns To remove this callback function from this Univer instance's on disposing list.
   */
  onDispose(e) {
    const n = this._disposingCallbacks.add(Ze(e));
    return Ze(() => n.dispose(!0));
  }
  dispose() {
    this._disposingCallbacks.dispose(), this._injector.dispose();
  }
  setLocale(e) {
    this._injector.get(Vr).setLocale(e);
  }
  createUnit(e, n) {
    return this._univerInstanceService.createUnit(e, n);
  }
  /**
   * Create a univer sheet instance with internal dependency injection.
   *
   * @deprecated use `createUnit` instead
   */
  createUniverSheet(e) {
    return this._injector.get(Mt).warn("[Univer]: Univer.createUniverSheet is deprecated, use createUnit instead"), this._univerInstanceService.createUnit(Fe.UNIVER_SHEET, e);
  }
  /**
   * @deprecated use `createUnit` instead
   */
  createUniverDoc(e) {
    return this._injector.get(Mt).warn("[Univer]: Univer.createUniverDoc is deprecated, use createUnit instead"), this._univerInstanceService.createUnit(Fe.UNIVER_DOC, e);
  }
  /**
   * @deprecated use `createUnit` instead
   */
  createUniverSlide(e) {
    return this._injector.get(Mt).warn("[Univer]: Univer.createUniverSlide is deprecated, use createUnit instead"), this._univerInstanceService.createUnit(Fe.UNIVER_SLIDE, e);
  }
  _init(e) {
    this._univerInstanceService.registerCtorForType(Fe.UNIVER_SHEET, ts), this._univerInstanceService.registerCtorForType(Fe.UNIVER_DOC, jt), this._univerInstanceService.registerCtorForType(Fe.UNIVER_SLIDE, cl);
    const n = e.get(_n);
    n.__setCreateHandler(
      (r, s, i, o) => {
        if (!this._startedTypes.has(r)) {
          this._pluginService.startPluginForType(r), this._startedTypes.add(r);
          const u = e.createInstance(i, s);
          return n.__addUnit(u, o), this._tryProgressToReady(), u;
        }
        const a = e.createInstance(i, s);
        return n.__addUnit(a, o), a;
      }
    );
  }
  _tryProgressToReady() {
    this._injector.get(Ht).stage < Ve.Ready && (this._injector.get(Ht).stage = Ve.Ready);
  }
  /** Register a plugin into univer. */
  registerPlugin(e, n) {
    this._pluginService.registerPlugin(e, n);
  }
}
function KE(t, e) {
  const n = kE([
    [NE],
    [Vr],
    [ml],
    [Ht],
    [ns],
    [rr],
    // abstract services
    [_n, { useClass: ni }],
    [UE, { useClass: PE }],
    [Mt, { useClass: Bf, lazy: !0 }],
    [Pt, { useClass: Ys }],
    [cn, { useClass: ri, lazy: !0 }],
    [SE, { useClass: AE }],
    [fs, { useClass: Ff }],
    [Bi, { useClass: VE, lazy: !0 }],
    [va, { useClass: ui, lazy: !0 }],
    [bE, { useClass: oi, lazy: !0 }],
    [LE, { useClass: ai, lazy: !0 }]
  ], e), r = t ? t.createChild(n) : new Ot(n);
  return Mf(r, [
    [rr],
    [va]
  ]), r;
}
var XE = Object.defineProperty, JE = Object.getOwnPropertyDescriptor, ZE = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? JE(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && XE(e, n, s), s;
}, QE = (t, e) => (n, r) => e(n, r, t);
let ss = class extends Fi {
  constructor(t, e) {
    super(), this._blob = t, this._injector = e;
  }
  /**
   * Returns a copy of this blob.
   * @returns a new blob by copying the current blob
   * @example
   * ```ts
   * const blob = univerAPI.newBlob(blob);
   * const newBlob = blob.copyBlob();
   * console.log(newBlob);
   * ```
   */
  copyBlob() {
    return this._injector.createInstance(ss, this._blob);
  }
  /**
   * Return the data inside this object as a blob converted to the specified content type.
   * @param contentType the content type refer to https://developer.mozilla.org/en-US/docs/Web/HTTP/MIME_types/Common_types
   * @returns a new blob by converting the current blob to the specified content type
   * @example
   * ```ts
   * const blob = univerAPI.newBlob(blob);
   * const newBlob = blob.getBlob();
   * ```
   */
  getAs(t) {
    const e = this.copyBlob();
    return e.setContentType(t), e;
  }
  getDataAsString(t) {
    return this._blob === null ? Promise.resolve("") : t === void 0 ? this._blob.text() : new Promise((e, n) => {
      this._blob.arrayBuffer().then((r) => {
        const s = new TextDecoder(t).decode(r);
        e(s);
      }).catch((r) => {
        n(new Error(`Failed to read Blob as ArrayBuffer: ${r.message}`));
      });
    });
  }
  /**
   * Gets the data stored in this blob.
   * @returns the blob content as a byte array
   * @example
   * ```ts
   * const blob = univerAPI.newBlob(blob);
   * const newBlob = blob.getBytes();
   * console.log(newBlob);
   * ```
   */
  getBytes() {
    return this._blob ? this._blob.arrayBuffer().then((t) => new Uint8Array(t)) : Promise.reject(new Error("Blob is undefined or null."));
  }
  /**
   * Sets the data stored in this blob.
   * @param bytes a byte array
   * @returns the blob object
   * @example
   * ```ts
   * const blob = univerAPI.newBlob();
   * const bytes = new Uint8Array(10);
   * blob.setBytes(bytes);
   * ```
   */
  setBytes(t) {
    return this._blob = new Blob([t]), this;
  }
  setDataFromString(t, e) {
    const n = e != null ? e : "text/plain", r = new Blob([t], { type: n });
    return this._blob = r, this;
  }
  /**
   * Gets the content type of the data stored in this blob.
   * @returns the content type
   * @example
   * ```ts
   * const blob = univerAPI.newBlob(blob);
   * const newBlob = blob.getContentType();
   * console.log(newBlob);
   * ```
   */
  getContentType() {
    var t;
    return (t = this._blob) == null ? void 0 : t.type;
  }
  /**
   * Sets the content type of the data stored in this blob.
   * @param contentType the content type refer to https://developer.mozilla.org/en-US/docs/Web/HTTP/MIME_types/Common_types
   * @returns the blob object
   * @example
   * ```ts
   * const blob = univerAPI.newBlob(blob);
   * const newBlob = blob.setContentType('text/plain');
   * console.log(newBlob);
   * ```
   */
  setContentType(t) {
    var e;
    return this._blob = (e = this._blob) == null ? void 0 : e.slice(0, this._blob.size, t), this;
  }
};
ss = ZE([
  QE(1, ot(Ot))
], ss);
var qE = Object.defineProperty, e0 = Object.getOwnPropertyDescriptor, t0 = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? e0(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && qE(e, n, s), s;
}, n0 = (t, e) => (n, r) => e(n, r, t);
let li = class extends al {
  constructor(t, e) {
    super(e), this.doc = t;
  }
};
li = t0([
  n0(1, ot(Ot))
], li);
var _l = /* @__PURE__ */ ((t) => (t[t.INFO = 0] = "INFO", t[t.STOP = 1] = "STOP", t[t.WARNING = 2] = "WARNING", t))(_l || {}), El = /* @__PURE__ */ ((t) => (t.BETWEEN = "between", t.EQUAL = "equal", t.GREATER_THAN = "greaterThan", t.GREATER_THAN_OR_EQUAL = "greaterThanOrEqual", t.LESS_THAN = "lessThan", t.LESS_THAN_OR_EQUAL = "lessThanOrEqual", t.NOT_BETWEEN = "notBetween", t.NOT_EQUAL = "notEqual", t))(El || {}), Cl = /* @__PURE__ */ ((t) => (t[t.TEXT = 0] = "TEXT", t[t.ARROW = 1] = "ARROW", t[t.CUSTOM = 2] = "CUSTOM", t))(Cl || {}), Rl = /* @__PURE__ */ ((t) => (t.VALID = "valid", t.INVALID = "invalid", t.VALIDATING = "validating", t))(Rl || {}), Il = /* @__PURE__ */ ((t) => (t.CUSTOM = "custom", t.LIST = "list", t.LIST_MULTIPLE = "listMultiple", t.NONE = "none", t.TEXT_LENGTH = "textLength", t.DATE = "date", t.TIME = "time", t.WHOLE = "whole", t.DECIMAL = "decimal", t.CHECKBOX = "checkbox", t.ANY = "any", t))(Il || {});
const bn = class bn {
  static get() {
    if (this._instance)
      return this._instance;
    const e = new bn();
    return this._instance = e, e;
  }
  static extend(e) {
    Object.getOwnPropertyNames(e.prototype).forEach((n) => {
      n !== "constructor" && (this.prototype[n] = e.prototype[n]);
    }), Object.getOwnPropertyNames(e).forEach((n) => {
      n !== "prototype" && n !== "name" && n !== "length" && (this[n] = e[n]);
    });
  }
  constructor() {
    for (const e in bn.prototype)
      this[e] = bn.prototype[e];
  }
  /**
   *  Defines different types of Univer instances
   */
  get UniverInstanceType() {
    return Fe;
  }
  /**
   * Represents different stages in the lifecycle
   */
  get LifecycleStages() {
    return Ve;
  }
  /**
   * Different types of data validation
   */
  get DataValidationType() {
    return Il;
  }
  /**
   * Different error display styles
   */
  get DataValidationErrorStyle() {
    return _l;
  }
  /**
   * Different validation rendering modes
   */
  get DataValidationRenderMode() {
    return Cl;
  }
  /**
   * Different validation operators
   */
  get DataValidationOperator() {
    return El;
  }
  /**
   * Different validation states
   */
  get DataValidationStatus() {
    return Rl;
  }
  /**
   * Different types of commands
   */
  get CommandType() {
    return ar;
  }
  /**
   * Different baseline offsets for text baseline positioning
   */
  get BaselineOffset() {
    return Bt;
  }
  /**
   * Boolean number representations
   */
  get BooleanNumber() {
    return we;
  }
  /**
   * Different horizontal text alignment options
   */
  get HorizontalAlign() {
    return Xt;
  }
  /**
   * Different text decoration styles
   */
  get TextDecoration() {
    return Nu;
  }
  /**
   * Different text direction options
   */
  get TextDirection() {
    return er;
  }
  /**
   * Different vertical text alignment options
   */
  get VerticalAlign() {
    return hn;
  }
  /**
   * Different border types
   */
  get BorderType() {
    return Eu;
  }
  /**
   * Different border style types
   */
  get BorderStyleTypes() {
    return Xe;
  }
  /**
   * Auto fill series types
   */
  get AutoFillSeries() {
    return _u;
  }
  /**
   * Color types
   */
  get ColorType() {
    return vt;
  }
  /**
   * Common hide types
   */
  get CommonHideTypes() {
    return Cu;
  }
  /**
   * Copy paste types
   */
  get CopyPasteType() {
    return Ru;
  }
  /**
   * Delete direction types
   */
  get DeleteDirection() {
    return Iu;
  }
  /**
   * Developer metadata visibility types
   */
  get DeveloperMetadataVisibility() {
    return vu;
  }
  /**
   * Dimension types
   */
  get Dimension() {
    return yu;
  }
  /**
   * Direction types
   */
  get Direction() {
    return wu;
  }
  /**
   * Interpolation point types
   */
  get InterpolationPointType() {
    return Ou;
  }
  /**
   * Locale types
   */
  get LocaleType() {
    return ur;
  }
  /**
   * Mention types
   */
  get MentionType() {
    return Zr;
  }
  /**
   * Protection types
   */
  get ProtectionType() {
    return bu;
  }
  /**
   * Relative date types
   */
  get RelativeDate() {
    return Su;
  }
  /**
   * Sheet types
   */
  get SheetTypes() {
    return Au;
  }
  /**
   * Theme color types
   */
  get ThemeColorType() {
    return ft;
  }
};
C(bn, "_instance");
let ci = bn;
const Sn = class Sn {
  static get() {
    if (this._instance)
      return this._instance;
    const e = new Sn();
    return this._instance = e, e;
  }
  static extend(e) {
    Object.getOwnPropertyNames(e.prototype).forEach((n) => {
      n !== "constructor" && (this.prototype[n] = e.prototype[n]);
    }), Object.getOwnPropertyNames(e).forEach((n) => {
      n !== "prototype" && n !== "name" && n !== "length" && (this[n] = e[n]);
    });
  }
  constructor() {
    for (const e in Sn.prototype)
      this[e] = Sn.prototype[e];
  }
  /**
   * Event fired when a document is created
   * @see {@link IDocCreatedParam}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.DocCreated, (params) => {
   *     const { unitId, type, doc, unit } = params;
   *     console.log('doc created', params);
   * });
   * ```
   */
  get DocCreated() {
    return "DocCreated";
  }
  /**
   * Event fired when a document is disposed
   * @see {@link IDocDisposedEvent}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.DocDisposed, (params) => {
   *     const { unitId, unitType, snapshot } = params;
   *     console.log('doc disposed', params);
   * });
   * ```
   */
  get DocDisposed() {
    return "DocDisposed";
  }
  /**
   * Event fired when life cycle is changed
   * @see {@link ILifeCycleChangedEvent}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.LifeCycleChanged, (params) => {
   *      const { stage } = params;
   *     console.log('life cycle changed', params);
   * });
   * ```
   */
  get LifeCycleChanged() {
    return "LifeCycleChanged";
  }
  /**
   * Event fired when a redo command is executed
   * @see {@link ICommandEvent}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.Redo, (event) => {
   *     const { params, id, type } = event;
   *     console.log('command executed', event);
   * });
   * ```
   */
  get Redo() {
    return "Redo";
  }
  /**
   * Event fired when an undo command is executed
   * @see {@link ICommandEvent}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.Undo, (event) => {
   *     const { params, id, type } = event;
   *     console.log('command executed', event);
   * });
   * ```
   */
  get Undo() {
    return "Undo";
  }
  /**
   * Event fired before a redo command is executed
   * @see {@link ICommandEvent}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.BeforeRedo, (event) => {
   *     const { params, id, type } = event;
   *     console.log('command executed', event);
   * });
   * ```
   */
  get BeforeRedo() {
    return "BeforeRedo";
  }
  /**
   * Event fired before an undo command is executed
   * @see {@link ICommandEvent}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.BeforeUndo, (event) => {
   *     const { params, id, type } = event;
   *     console.log('command executed', event);
   * });
   * ```
   */
  get BeforeUndo() {
    return "BeforeUndo";
  }
  /**
   * Event fired when a command is executed
   * @see {@link ICommandEvent}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.CommandExecuted, (event) => {
   *     const { params, id, type } = event;
   *     console.log('command executed', event);
   * });
   * ```
   */
  get CommandExecuted() {
    return "CommandExecuted";
  }
  /**
   * Event fired before a command is executed
   * @see {@link ICommandEvent}
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.BeforeCommandExecute, (event) => {
   *     const { params, id, type } = event;
   *     console.log('command executed', event);
   * });
   * ```
   */
  get BeforeCommandExecute() {
    return "BeforeCommandExecute";
  }
};
C(Sn, "_instance");
let hi = Sn;
var r0 = Object.defineProperty, s0 = Object.getOwnPropertyDescriptor, i0 = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? s0(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && r0(e, n, s), s;
}, ya = (t, e) => (n, r) => e(n, r, t);
let di = class extends Fi {
  constructor(t, e) {
    super(), this._injector = t, this._lifecycleService = e;
  }
  /**
   * @deprecated use `univerAPI.addEvent(univerAPI.Event.LifecycleChanged)` as instead
   */
  onStarting(t) {
    return Ze(this._lifecycleService.lifecycle$.pipe(Kt((e) => e === Ve.Starting)).subscribe(t));
  }
  /**
   * @deprecated use `univerAPI.addEvent(univerAPI.Event.LifecycleChanged)` as instead
   */
  onReady(t) {
    return Ze(this._lifecycleService.lifecycle$.pipe(Kt((e) => e === Ve.Ready)).subscribe(t));
  }
  /**
   * @deprecated use `univerAPI.addEvent(univerAPI.Event.LifecycleChanged, () => {})` as instead
   */
  onRendered(t) {
    return Ze(this._lifecycleService.lifecycle$.pipe(Kt((e) => e === Ve.Rendered)).subscribe(t));
  }
  /**
   * @deprecated use `univerAPI.addEvent(univerAPI.Event.LifecycleChanged, () => {})` as instead
   */
  onSteady(t) {
    return Ze(this._lifecycleService.lifecycle$.pipe(Kt((e) => e === Ve.Steady)).subscribe(t));
  }
  /**
   * @deprecated use `univerAPI.addEvent(univerAPI.Event.BeforeUndo, () => {})` as instead
   */
  onBeforeUndo(t) {
    return this._injector.get(Pt).beforeCommandExecuted((n) => {
      if (n.id === Nn.id) {
        const s = this._injector.get(cn).pitchTopUndoElement();
        s && t(s);
      }
    });
  }
  /**
   * @deprecated use `univerAPI.addEvent(univerAPI.Event.Undo, () => {})` as instead
   */
  onUndo(t) {
    return this._injector.get(Pt).onCommandExecuted((n) => {
      if (n.id === Nn.id) {
        const s = this._injector.get(cn).pitchTopUndoElement();
        s && t(s);
      }
    });
  }
  /**
   * @deprecated use `univerAPI.addEvent(univerAPI.Event.BeforeRedo, () => {})` as instead
   */
  onBeforeRedo(t) {
    return this._injector.get(Pt).beforeCommandExecuted((n) => {
      if (n.id === Tn.id) {
        const s = this._injector.get(cn).pitchTopRedoElement();
        s && t(s);
      }
    });
  }
  /**
   * @deprecated use `univerAPI.addEvent(univerAPI.Event.Redo, () => {})` as instead
   */
  onRedo(t) {
    return this._injector.get(Pt).onCommandExecuted((n) => {
      if (n.id === Tn.id) {
        const s = this._injector.get(cn).pitchTopRedoElement();
        s && t(s);
      }
    });
  }
};
di = i0([
  ya(0, ot(Ot)),
  ya(1, ot(Ht))
], di);
var o0 = Object.defineProperty, a0 = Object.getOwnPropertyDescriptor, u0 = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? a0(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && o0(e, n, s), s;
}, wa = (t, e) => (n, r) => e(n, r, t);
let fi = class extends Fi {
  constructor(t, e) {
    super(), this._injector = t, this._userManagerService = e;
  }
  /**
   * Get current user info.
   * @returns {IUser} Current user info.
   * @example
   * ```typescript
   * univerAPI.getUserManager().getCurrentUser();
   * ```
   */
  getCurrentUser() {
    return this._userManagerService.getCurrentUser();
  }
};
fi = u0([
  wa(0, ot(Ot)),
  wa(1, ot(rr))
], fi);
const is = class is {
  static get() {
    if (this._instance)
      return this._instance;
    const e = new is();
    return this._instance = e, e;
  }
  static extend(e) {
    Object.getOwnPropertyNames(e.prototype).forEach((n) => {
      n !== "constructor" && (this.prototype[n] = e.prototype[n]);
    }), Object.getOwnPropertyNames(e).forEach((n) => {
      n !== "prototype" && n !== "name" && n !== "length" && (this[n] = e[n]);
    });
  }
  /**
   * Rectangle utils, including range operations likes merge, subtract, split
   */
  get rectangle() {
    return en;
  }
  /**
   * Number format utils, including parse and strigify about date, price, etc
   */
  get numfmt() {
    return Op;
  }
  /**
   * common tools
   */
  get tools() {
    return re;
  }
};
C(is, "_instance");
let gi = is;
var l0 = Object.defineProperty, c0 = Object.getOwnPropertyDescriptor, h0 = (t, e, n, r) => {
  for (var s = r > 1 ? void 0 : r ? c0(e, n) : e, i = t.length - 1, o; i >= 0; i--)
    (o = t[i]) && (s = (r ? o(e, n, s) : o(s)) || s);
  return r && s && l0(e, n, s), s;
}, Mr = (t, e) => (n, r) => e(n, r, t);
let pi = class extends al {
  constructor(e, n, r, s) {
    super(e);
    C(this, "_eventRegistry", /* @__PURE__ */ new Map());
    this._injector = e, this._commandService = n, this._univerInstanceService = r, this._lifecycleService = s, this.disposeWithMe(
      this._lifecycleService.lifecycle$.subscribe((i) => {
        this.fireEvent(this.Event.LifeCycleChanged, { stage: i });
      })
    ), this.disposeWithMe(
      this._commandService.beforeCommandExecuted((i) => {
        if (!this._eventRegistry.get(this.Event.BeforeRedo) && !this._eventRegistry.get(this.Event.BeforeUndo) && !this._eventRegistry.get(this.Event.BeforeCommandExecute))
          return;
        const { id: o, type: a, params: u } = i, l = { id: o, type: a, params: u };
        switch (i.id) {
          case Tn.id:
            this.fireEvent(this.Event.BeforeRedo, l);
            break;
          case Nn.id:
            this.fireEvent(this.Event.BeforeUndo, l);
            break;
          default:
            this.fireEvent(this.Event.BeforeCommandExecute, l);
            break;
        }
        if (l.cancel)
          throw new xf();
      })
    ), this.disposeWithMe(
      this._commandService.onCommandExecuted((i) => {
        if (!this._eventRegistry.get(this.Event.Redo) && !this._eventRegistry.get(this.Event.Undo) && !this._eventRegistry.get(this.Event.CommandExecuted))
          return;
        const { id: o, type: a, params: u } = i, l = { id: o, type: a, params: u };
        switch (i.id) {
          case Tn.id:
            this.fireEvent(this.Event.Redo, l);
            break;
          case Nn.id:
            this.fireEvent(this.Event.Undo, l);
            break;
          default:
            this.fireEvent(this.Event.CommandExecuted, l);
            break;
        }
      })
    ), this._initUnitEvent(this._injector), this._injector.onDispose(() => {
      this.dispose();
    });
  }
  /**
   * Create an FUniver instance, if the injector is not provided, it will create a new Univer instance.
   * @static
   * @param {Univer | Injector} wrapped - The Univer instance or injector instance.
   * @returns {FUniver} - The FUniver instance.
   */
  static newAPI(e) {
    return (e instanceof GE ? e.__getInjector() : e).createInstance(pi);
  }
  _ensureEventRegistry(e) {
    return this._eventRegistry.has(e) || this._eventRegistry.set(e, new $i()), this._eventRegistry.get(e);
  }
  _initUnitEvent(e) {
    const n = e.get(_n);
    this.disposeWithMe(
      n.unitDisposed$.subscribe((r) => {
        this._eventRegistry.get(this.Event.DocDisposed) && r.type === Fe.UNIVER_DOC && this.fireEvent(
          this.Event.DocDisposed,
          {
            unitId: r.getUnitId(),
            unitType: r.type,
            snapshot: r.getSnapshot()
          }
        );
      })
    ), this.disposeWithMe(
      n.unitAdded$.subscribe((r) => {
        if (this._eventRegistry.get(this.Event.DocCreated) && r.type === Fe.UNIVER_DOC) {
          const s = r, i = e.createInstance(li, s);
          this.fireEvent(
            this.Event.DocCreated,
            {
              unitId: r.getUnitId(),
              type: r.type,
              doc: i,
              unit: i
            }
          );
        }
      })
    );
  }
  _eventListend(e) {
    return this._eventRegistry.get(e);
  }
  /**
   * Dispose the UniverSheet by the `unitId`. The UniverSheet would be unload from the application.
   * @param unitId The unit id of the UniverSheet.
   * @returns Whether the Univer instance is disposed successfully.
   */
  disposeUnit(e) {
    return this._univerInstanceService.disposeUnit(e);
  }
  /**
   * Get the current lifecycle stage.
   * @returns {LifecycleStages} - The current lifecycle stage.
   */
  getCurrentLifecycleStage() {
    return this._injector.get(Ht).stage;
  }
  /**
   * Undo an editing on the currently focused document.
   * @returns {Promise<boolean>} undo result
   */
  undo() {
    return this._commandService.executeCommand(Nn.id);
  }
  /**
   * Redo an editing on the currently focused document.
   * @returns {Promise<boolean>} redo result
   */
  redo() {
    return this._commandService.executeCommand(Tn.id);
  }
  /**
   * Register a callback that will be triggered before invoking a command.
   * @deprecated use `addEvent(univerAPI.event.BeforeCommandExecute, () => {})` instead.
   * @param {CommandListener} callback The callback.
   * @returns {IDisposable} The disposable instance.
   */
  onBeforeCommandExecute(e) {
    return this._commandService.beforeCommandExecuted((n, r) => {
      e(n, r);
    });
  }
  /**
   * Register a callback that will be triggered when a command is invoked.
   * @deprecated use `addEvent(univerAPI.event.CommandExecuted, () => {})` instead.
   * @param {CommandListener} callback The callback.
   * @returns {IDisposable} The disposable instance.
   */
  onCommandExecuted(e) {
    return this._commandService.onCommandExecuted((n, r) => {
      e(n, r);
    });
  }
  /**
   * Execute a command with the given id and parameters.
   * @param id Identifier of the command.
   * @param params Parameters of this execution.
   * @param options Options of this execution.
   * @returns The result of the execution. It is a boolean value by default which indicates the command is executed.
   */
  executeCommand(e, n, r) {
    return this._commandService.executeCommand(e, n, r);
  }
  /**
   * Execute a command with the given id and parameters synchronously.
   * @param id Identifier of the command.
   * @param params Parameters of this execution.
   * @param options Options of this execution.
   * @returns The result of the execution. It is a boolean value by default which indicates the command is executed.
   */
  syncExecuteCommand(e, n, r) {
    return this._commandService.syncExecuteCommand(e, n, r);
  }
  /**
   * Get hooks.
   * @deprecated use `addEvent` instead.
   * @returns {FHooks} FHooks instance
   */
  getHooks() {
    return this._injector.createInstance(di);
  }
  get Enum() {
    return ci.get();
  }
  get Event() {
    return hi.get();
  }
  get Util() {
    return gi.get();
  }
  /**
   * Add an event listener
   * @param event key of event
   * @param callback callback when event triggered
   * @returns {Disposable} The Disposable instance, for remove the listener
   * @example
   * ```ts
   * univerAPI.addEvent(univerAPI.event.UnitCreated, (params) => {
   *     console.log('unit created', params);
   * });
   * ```
   */
  addEvent(e, n) {
    return this._ensureEventRegistry(e).add(n), Ze(() => this._ensureEventRegistry(e).delete(n));
  }
  /**
   * Fire an event, used in internal only.
   * @param event {string} key of event
   * @param params {any} params of event
   * @returns {boolean} should cancel
   * @example
   * ```ts
   * this.fireEvent(univerAPI.event.UnitCreated, params);
   * ```
   */
  fireEvent(e, n) {
    var r;
    return (r = this._eventRegistry.get(e)) == null || r.getData().forEach((s) => {
      s(n);
    }), n.cancel;
  }
  /**
   * Get the callback map corresponding to the event
   * @param event
   * @returns {number} The number of callbacks
   */
  hasEventCallback(e) {
    var r, s;
    return ((s = (r = this._eventRegistry.get(e)) == null ? void 0 : r.getData().length) != null ? s : 0) > 0;
  }
  getUserManager() {
    return this._injector.createInstance(fi);
  }
  /**
   * Create a new blob.
   * @returns {FBlob} The new blob instance
   * @example
   * ```ts
   * const blob = univerApi.newBlob();
   * ```
   */
  newBlob() {
    return this._injector.createInstance(ss);
  }
  /**
   * Create a new color.
   * @returns {ColorBuilder} The new color instance
   * @example
   * ```ts
   * const color = univerApi.newColor();
   * ```
   */
  newColor() {
    return new gs();
  }
  /**
   * Create a new rich text.
   * @param data
   * @returns {RichTextBuilder} The new rich text instance
   * @example
   * ```ts
   * const richText = univerApi.newRichText();
   * ```
   */
  newRichText(e) {
    return gn.create(e);
  }
  /**
   * Create a new rich text value.
   * @param data - The rich text data
   * @returns {RichTextValue} The new rich text value instance
   * @example
   * ```ts
   * const richTextValue = univerApi.newRichTextValue();
   * ```
   */
  newRichTextValue(e) {
    return Zt.create(e);
  }
  /**
   * Create a new paragraph style.
   * @param style - The paragraph style
   * @returns {ParagraphStyleBuilder} The new paragraph style instance
   * @example
   * ```ts
   * const paragraphStyle = univerApi.newParagraphStyle();
   * ```
   */
  newParagraphStyle(e) {
    return nr.create(e);
  }
  /**
   * Create a new paragraph style value.
   * @param style - The paragraph style
   * @returns {ParagraphStyleValue} The new paragraph style value instance
   * @example
   * ```ts
   * const paragraphStyleValue = univerApi.newParagraphStyleValue();
   * ```
   */
  newParagraphStyleValue(e) {
    return hr.create(e);
  }
  /**
   * Create a new text style.
   * @param style - The text style
   * @returns {TextStyleBuilder} The new text style instance
   * @example
   * ```ts
   * const textStyle = univerApi.newTextStyle();
   * ```
   */
  newTextStyle(e) {
    return Qt.create(e);
  }
  /**
   * Create a new text style value.
   * @param style - The text style
   * @returns {TextStyleValue} The new text style value instance
   * @example
   * ```ts
   * const textStyleValue = univerApi.newTextStyleValue();
   * ```
   */
  newTextStyleValue(e) {
    return cr.create(e);
  }
  newTextDecoration(e) {
    return new Jt(e);
  }
};
pi = h0([
  Mr(0, ot(Ot)),
  Mr(1, Pt),
  Mr(2, _n),
  Mr(3, ot(Ht))
], pi);
function d0(t) {
  return /^-?\d+(\.\d+)?$/.test(t);
}
function bR(t) {
  return d0(t) ? Number(t) <= Number.MAX_SAFE_INTEGER : !1;
}
function SR(t) {
  const e = new MessageChannel();
  let n = !1;
  const r = () => {
    n || t();
  };
  return e.port1.onmessage = r, e.port2.postMessage(null), () => {
    n = !0, e.port1.close(), e.port2.close();
  };
}
function AR(t, e) {
  return e.forEach((n) => t.add(n)), t;
}
function NR(t, e, n, r) {
  var c;
  if (e === "")
    return t;
  const s = {
    id: "mock-id",
    body: t,
    documentStyle: {}
  }, i = new jt(s), o = e.length;
  let a;
  for (; (a = (r ? i.getBody().dataStream : i.getBody().dataStream.toLowerCase()).indexOf(e)) >= 0; ) {
    const l = new Ke(), h = tn.getInstance();
    if (a > 0 && l.retain(a), n.length > 0) {
      const d = i.sliceBody(a, a + o), f = {
        dataStream: n
      };
      if (Array.isArray(d == null ? void 0 : d.textRuns) && d.textRuns.length && (f.textRuns = [{
        ...d.textRuns[0],
        st: 0,
        ed: n.length
      }]), (c = d == null ? void 0 : d.customRanges) != null && c.length) {
        const E = d.customRanges[0];
        f.customRanges = [{
          ...E,
          startIndex: 0,
          endIndex: n.length - 1
        }];
      }
      l.insert(n.length, f);
    }
    l.delete(o), i.apply(h.editOp(l.serialize()));
  }
  const u = i.getBody();
  return i.dispose(), u;
}
const TR = "__default_document_sub_component_id20231101__";
class f0 {
  constructor() {
    /**
     * An WorkBookObserver can set this property to true to prevent subsequent observers of being notified
     */
    C(this, "skipNextObservers", !1);
    /**
     * This will be populated with the return value of the last function that was executed.
     * If it is the first function in the callback chain it will be the event data.
     */
    C(this, "lastReturnValue");
    C(this, "isStopPropagation", !1);
  }
  stopPropagation() {
    this.isStopPropagation = !0;
  }
}
class MR extends _t {
  constructor() {
    super(...arguments);
    C(this, "_sortedObservers", []);
  }
  /** @deprecated Use `subscribeEvent` instead. */
  subscribe() {
    throw new Error("[EventSubject]: please use `subscribeEvent` instead of `subscribe` method for `EventSubject`.");
  }
  /** @deprecated Use `emitEvent` instead. */
  next() {
    throw new Error("[EventSubject]: please use `emitEvent` instead of `next` method for `EventSubject`.");
  }
  unsubscribe() {
    super.unsubscribe(), this._sortedObservers.length = 0;
  }
  complete() {
    super.complete(), this._sortedObservers.length = 0;
  }
  subscribeEvent(n) {
    let r;
    typeof n == "function" ? r = { next: ([i, o]) => n(i, o) } : r = n;
    const s = super.subscribe(r);
    return this._sortedObservers.push(r), this._sortedObservers.sort((i, o) => {
      var a, u;
      return ((a = i.priority) != null ? a : 0) - ((u = o.priority) != null ? u : 0);
    }), s.add(() => this._sortedObservers = this._sortedObservers.filter((i) => i !== r)), s;
  }
  clearObservers() {
    this._sortedObservers.forEach((n) => {
      var r;
      return (r = n.complete) == null ? void 0 : r.call(n);
    }), this._sortedObservers.length = 0;
  }
  emitEvent(n) {
    var r;
    if (!this.closed) {
      const s = new f0();
      s.lastReturnValue = n;
      for (const i of this._sortedObservers) {
        const o = (r = i.next) == null ? void 0 : r.call(i, [n, s]);
        if (s.lastReturnValue = o, s.skipNextObservers)
          return {
            handled: !0,
            lastReturnValue: s.lastReturnValue,
            stopPropagation: s.isStopPropagation
          };
      }
      return {
        handled: this._sortedObservers.length > 0,
        lastReturnValue: s.lastReturnValue,
        stopPropagation: s.isStopPropagation
      };
    }
    throw new Error("[EventSubject]: cannot emit event on a closed subject.");
  }
}
function DR(t) {
  return new sr((e) => {
    const n = t.subscribeEvent((r) => {
      e.next(r);
    });
    return () => n.unsubscribe();
  });
}
const xR = Ct("ILocalStorageService");
function LR(t) {
  return !(t.length === 0 || t.length > 31 || t.startsWith("'") || t.endsWith("'") || /[:\\\/\?\*\[\]]/.test(t));
}
function UR(t) {
  return new Promise((e) => setTimeout(e, t));
}
function PR(t = 1) {
  return new Promise((e) => {
    let n = 0;
    const r = () => {
      n++, n >= t ? e() : requestAnimationFrame(r);
    };
    requestAnimationFrame(r);
  });
}
var vl = /* @__PURE__ */ ((t) => (t.URL = "URL", t.UUID = "UUID", t.BASE64 = "BASE64", t))(vl || {}), g0 = /* @__PURE__ */ ((t) => (t.SUCCUSS = "0", t.ERROR_EXCEED_SIZE = "1", t.ERROR_IMAGE_TYPE = "2", t.ERROR_UPLOAD_COUNT_LIMIT = "3", t.ERROR_IMAGE = "4", t))(g0 || {});
const Oa = Ct("core.image-io.service");
class kR {
  constructor(e, n = 100) {
    C(this, "_imageCacheMap");
    this._injector = e, this._imageCacheMap = new Qr(n);
  }
  _getImageCacheKey(e, n) {
    return `${e}-${n}`;
  }
  getImage(e, n, r, s) {
    const i = this._getImageCacheKey(e, n);
    let o = this._imageCacheMap.get(i);
    return o || ((async () => {
      o = new Image();
      const a = this._injector.has(Oa) ? this._injector.get(Oa) : null;
      if (e === vl.UUID)
        try {
          o.src = await (a == null ? void 0 : a.getImage(n)) || "";
        } catch (u) {
          console.error(u);
        }
      else
        o.src = n;
      o.onload = () => {
        r == null || r();
      }, o.onerror = () => {
        s == null || s();
      }, this._imageCacheMap.set(i, o);
    })(), null);
  }
}
const FR = ["script", "style", "meta", "comment", "link"];
var p0 = /* @__PURE__ */ ((t) => (t[t.DISABLED = 0] = "DISABLED", t[t.FULL_ALPHA = 1] = "FULL_ALPHA", t[t.FULL_HANGUL = 2] = "FULL_HANGUL", t[t.FULL_KATAKANA = 3] = "FULL_KATAKANA", t[t.HALF_ALPHA = 4] = "HALF_ALPHA", t[t.HALF_HANGUL = 5] = "HALF_HANGUL", t[t.HALF_KATAKANA = 6] = "HALF_KATAKANA", t[t.HIRAGANA = 7] = "HIRAGANA", t[t.NO_CONTROL = 8] = "NO_CONTROL", t[t.OFF = 9] = "OFF", t[t.ON = 10] = "ON", t))(p0 || {});
const ba = [
  Int8Array,
  Uint8Array,
  Uint8ClampedArray,
  Int16Array,
  Uint16Array,
  Int32Array,
  Uint32Array,
  Float32Array,
  Float64Array
], Ls = 1, jn = 8;
class ji {
  /**
   * Creates an index from raw `ArrayBuffer` data.
   * @param {ArrayBuffer} data
   */
  static from(e) {
    if (!(e instanceof ArrayBuffer))
      throw new Error("Data must be an instance of ArrayBuffer.");
    const [n, r] = new Uint8Array(e, 0, 2);
    if (n !== 219)
      throw new Error("Data does not appear to be in a KDBush format.");
    const s = r >> 4;
    if (s !== Ls)
      throw new Error(`Got v${s} data when expected v${Ls}.`);
    const i = ba[r & 15];
    if (!i)
      throw new Error("Unrecognized array type.");
    const [o] = new Uint16Array(e, 2, 1), [a] = new Uint32Array(e, 4, 1);
    return new ji(a, o, i, e);
  }
  /**
   * Creates an index that will hold a given number of items.
   * @param {number} numItems
   * @param {number} [nodeSize=64] Size of the KD-tree node (64 by default).
   * @param {TypedArrayConstructor} [ArrayType=Float64Array] The array type used for coordinates storage (`Float64Array` by default).
   * @param {ArrayBuffer} [data] (For internal use only)
   */
  constructor(e, n = 64, r = Float64Array, s) {
    if (isNaN(e) || e < 0) throw new Error(`Unpexpected numItems value: ${e}.`);
    this.numItems = +e, this.nodeSize = Math.min(Math.max(+n, 2), 65535), this.ArrayType = r, this.IndexArrayType = e < 65536 ? Uint16Array : Uint32Array;
    const i = ba.indexOf(this.ArrayType), o = e * 2 * this.ArrayType.BYTES_PER_ELEMENT, a = e * this.IndexArrayType.BYTES_PER_ELEMENT, u = (8 - a % 8) % 8;
    if (i < 0)
      throw new Error(`Unexpected typed array class: ${r}.`);
    s && s instanceof ArrayBuffer ? (this.data = s, this.ids = new this.IndexArrayType(this.data, jn, e), this.coords = new this.ArrayType(this.data, jn + a + u, e * 2), this._pos = e * 2, this._finished = !0) : (this.data = new ArrayBuffer(jn + o + a + u), this.ids = new this.IndexArrayType(this.data, jn, e), this.coords = new this.ArrayType(this.data, jn + a + u, e * 2), this._pos = 0, this._finished = !1, new Uint8Array(this.data, 0, 2).set([219, (Ls << 4) + i]), new Uint16Array(this.data, 2, 1)[0] = n, new Uint32Array(this.data, 4, 1)[0] = e);
  }
  /**
   * Add a point to the index.
   * @param {number} x
   * @param {number} y
   * @returns {number} An incremental index associated with the added item (starting from `0`).
   */
  add(e, n) {
    const r = this._pos >> 1;
    return this.ids[r] = r, this.coords[this._pos++] = e, this.coords[this._pos++] = n, r;
  }
  /**
   * Perform indexing of the added points.
   */
  finish() {
    const e = this._pos >> 1;
    if (e !== this.numItems)
      throw new Error(`Added ${e} items when expected ${this.numItems}.`);
    return mi(this.ids, this.coords, this.nodeSize, 0, this.numItems - 1, 0), this._finished = !0, this;
  }
  /**
   * Search the index for items within a given bounding box.
   * @param {number} minX
   * @param {number} minY
   * @param {number} maxX
   * @param {number} maxY
   * @returns {number[]} An array of indices correponding to the found items.
   */
  range(e, n, r, s) {
    if (!this._finished) throw new Error("Data not yet indexed - call index.finish().");
    const { ids: i, coords: o, nodeSize: a } = this, u = [0, i.length - 1, 0], c = [];
    for (; u.length; ) {
      const l = u.pop() || 0, h = u.pop() || 0, d = u.pop() || 0;
      if (h - d <= a) {
        for (let O = d; O <= h; O++) {
          const U = o[2 * O], ne = o[2 * O + 1];
          U >= e && U <= r && ne >= n && ne <= s && c.push(i[O]);
        }
        continue;
      }
      const f = d + h >> 1, E = o[2 * f], R = o[2 * f + 1];
      E >= e && E <= r && R >= n && R <= s && c.push(i[f]), (l === 0 ? e <= E : n <= R) && (u.push(d), u.push(f - 1), u.push(1 - l)), (l === 0 ? r >= E : s >= R) && (u.push(f + 1), u.push(h), u.push(1 - l));
    }
    return c;
  }
  /**
   * Search the index for items within a given radius.
   * @param {number} qx
   * @param {number} qy
   * @param {number} r Query radius.
   * @returns {number[]} An array of indices correponding to the found items.
   */
  within(e, n, r) {
    if (!this._finished) throw new Error("Data not yet indexed - call index.finish().");
    const { ids: s, coords: i, nodeSize: o } = this, a = [0, s.length - 1, 0], u = [], c = r * r;
    for (; a.length; ) {
      const l = a.pop() || 0, h = a.pop() || 0, d = a.pop() || 0;
      if (h - d <= o) {
        for (let O = d; O <= h; O++)
          Sa(i[2 * O], i[2 * O + 1], e, n) <= c && u.push(s[O]);
        continue;
      }
      const f = d + h >> 1, E = i[2 * f], R = i[2 * f + 1];
      Sa(E, R, e, n) <= c && u.push(s[f]), (l === 0 ? e - r <= E : n - r <= R) && (a.push(d), a.push(f - 1), a.push(1 - l)), (l === 0 ? e + r >= E : n + r >= R) && (a.push(f + 1), a.push(h), a.push(1 - l));
    }
    return u;
  }
}
function mi(t, e, n, r, s, i) {
  if (s - r <= n) return;
  const o = r + s >> 1;
  yl(t, e, o, r, s, i), mi(t, e, n, r, o - 1, 1 - i), mi(t, e, n, o + 1, s, 1 - i);
}
function yl(t, e, n, r, s, i) {
  for (; s > r; ) {
    if (s - r > 600) {
      const c = s - r + 1, l = n - r + 1, h = Math.log(c), d = 0.5 * Math.exp(2 * h / 3), f = 0.5 * Math.sqrt(h * d * (c - d) / c) * (l - c / 2 < 0 ? -1 : 1), E = Math.max(r, Math.floor(n - l * d / c + f)), R = Math.min(s, Math.floor(n + (c - l) * d / c + f));
      yl(t, e, n, E, R, i);
    }
    const o = e[2 * n + i];
    let a = r, u = s;
    for (Hn(t, e, r, n), e[2 * s + i] > o && Hn(t, e, r, s); a < u; ) {
      for (Hn(t, e, a, u), a++, u--; e[2 * a + i] < o; ) a++;
      for (; e[2 * u + i] > o; ) u--;
    }
    e[2 * r + i] === o ? Hn(t, e, r, u) : (u++, Hn(t, e, u, s)), u <= n && (r = u + 1), n <= u && (s = u - 1);
  }
}
function Hn(t, e, n, r) {
  Us(t, n, r), Us(e, 2 * n, 2 * r), Us(e, 2 * n + 1, 2 * r + 1);
}
function Us(t, e, n) {
  const r = t[e];
  t[e] = t[n], t[n] = r;
}
function Sa(t, e, n, r) {
  const s = t - n, i = e - r;
  return s * s + i * i;
}
function wl(t, e, n = 0, r = t.length - 1, s = m0) {
  for (; r > n; ) {
    if (r - n > 600) {
      const u = r - n + 1, c = e - n + 1, l = Math.log(u), h = 0.5 * Math.exp(2 * l / 3), d = 0.5 * Math.sqrt(l * h * (u - h) / u) * (c - u / 2 < 0 ? -1 : 1), f = Math.max(n, Math.floor(e - c * h / u + d)), E = Math.min(r, Math.floor(e + (u - c) * h / u + d));
      wl(t, e, f, E, s);
    }
    const i = t[e];
    let o = n, a = r;
    for (Wn(t, n, e), s(t[r], i) > 0 && Wn(t, n, r); o < a; ) {
      for (Wn(t, o, a), o++, a--; s(t[o], i) < 0; ) o++;
      for (; s(t[a], i) > 0; ) a--;
    }
    s(t[n], i) === 0 ? Wn(t, n, a) : (a++, Wn(t, a, r)), a <= e && (n = a + 1), e <= a && (r = a - 1);
  }
}
function Wn(t, e, n) {
  const r = t[e];
  t[e] = t[n], t[n] = r;
}
function m0(t, e) {
  return t < e ? -1 : t > e ? 1 : 0;
}
class Aa {
  constructor(e = 9) {
    this._maxEntries = Math.max(4, e), this._minEntries = Math.max(2, Math.ceil(this._maxEntries * 0.4)), this.clear();
  }
  all() {
    return this._all(this.data, []);
  }
  search(e) {
    let n = this.data;
    const r = [];
    if (!xr(e, n)) return r;
    const s = this.toBBox, i = [];
    for (; n; ) {
      for (let o = 0; o < n.children.length; o++) {
        const a = n.children[o], u = n.leaf ? s(a) : a;
        xr(e, u) && (n.leaf ? r.push(a) : ks(e, u) ? this._all(a, r) : i.push(a));
      }
      n = i.pop();
    }
    return r;
  }
  collides(e) {
    let n = this.data;
    if (!xr(e, n)) return !1;
    const r = [];
    for (; n; ) {
      for (let s = 0; s < n.children.length; s++) {
        const i = n.children[s], o = n.leaf ? this.toBBox(i) : i;
        if (xr(e, o)) {
          if (n.leaf || ks(e, o)) return !0;
          r.push(i);
        }
      }
      n = r.pop();
    }
    return !1;
  }
  load(e) {
    if (!(e && e.length)) return this;
    if (e.length < this._minEntries) {
      for (let r = 0; r < e.length; r++)
        this.insert(e[r]);
      return this;
    }
    let n = this._build(e.slice(), 0, e.length - 1, 0);
    if (!this.data.children.length)
      this.data = n;
    else if (this.data.height === n.height)
      this._splitRoot(this.data, n);
    else {
      if (this.data.height < n.height) {
        const r = this.data;
        this.data = n, n = r;
      }
      this._insert(n, this.data.height - n.height - 1, !0);
    }
    return this;
  }
  insert(e) {
    return e && this._insert(e, this.data.height - 1), this;
  }
  clear() {
    return this.data = yn([]), this;
  }
  remove(e, n) {
    if (!e) return this;
    let r = this.data;
    const s = this.toBBox(e), i = [], o = [];
    let a, u, c;
    for (; r || i.length; ) {
      if (r || (r = i.pop(), u = i[i.length - 1], a = o.pop(), c = !0), r.leaf) {
        const l = _0(e, r.children, n);
        if (l !== -1)
          return r.children.splice(l, 1), i.push(r), this._condense(i), this;
      }
      !c && !r.leaf && ks(r, s) ? (i.push(r), o.push(a), a = 0, u = r, r = r.children[0]) : u ? (a++, r = u.children[a], c = !1) : r = null;
    }
    return this;
  }
  toBBox(e) {
    return e;
  }
  compareMinX(e, n) {
    return e.minX - n.minX;
  }
  compareMinY(e, n) {
    return e.minY - n.minY;
  }
  toJSON() {
    return this.data;
  }
  fromJSON(e) {
    return this.data = e, this;
  }
  _all(e, n) {
    const r = [];
    for (; e; )
      e.leaf ? n.push(...e.children) : r.push(...e.children), e = r.pop();
    return n;
  }
  _build(e, n, r, s) {
    const i = r - n + 1;
    let o = this._maxEntries, a;
    if (i <= o)
      return a = yn(e.slice(n, r + 1)), vn(a, this.toBBox), a;
    s || (s = Math.ceil(Math.log(i) / Math.log(o)), o = Math.ceil(i / Math.pow(o, s - 1))), a = yn([]), a.leaf = !1, a.height = s;
    const u = Math.ceil(i / o), c = u * Math.ceil(Math.sqrt(o));
    Na(e, n, r, c, this.compareMinX);
    for (let l = n; l <= r; l += c) {
      const h = Math.min(l + c - 1, r);
      Na(e, l, h, u, this.compareMinY);
      for (let d = l; d <= h; d += u) {
        const f = Math.min(d + u - 1, h);
        a.children.push(this._build(e, d, f, s - 1));
      }
    }
    return vn(a, this.toBBox), a;
  }
  _chooseSubtree(e, n, r, s) {
    for (; s.push(n), !(n.leaf || s.length - 1 === r); ) {
      let i = 1 / 0, o = 1 / 0, a;
      for (let u = 0; u < n.children.length; u++) {
        const c = n.children[u], l = Ps(c), h = R0(e, c) - l;
        h < o ? (o = h, i = l < i ? l : i, a = c) : h === o && l < i && (i = l, a = c);
      }
      n = a || n.children[0];
    }
    return n;
  }
  _insert(e, n, r) {
    const s = r ? e : this.toBBox(e), i = [], o = this._chooseSubtree(s, this.data, n, i);
    for (o.children.push(e), Xn(o, s); n >= 0 && i[n].children.length > this._maxEntries; )
      this._split(i, n), n--;
    this._adjustParentBBoxes(s, i, n);
  }
  // split overflowed node into two
  _split(e, n) {
    const r = e[n], s = r.children.length, i = this._minEntries;
    this._chooseSplitAxis(r, i, s);
    const o = this._chooseSplitIndex(r, i, s), a = yn(r.children.splice(o, r.children.length - o));
    a.height = r.height, a.leaf = r.leaf, vn(r, this.toBBox), vn(a, this.toBBox), n ? e[n - 1].children.push(a) : this._splitRoot(r, a);
  }
  _splitRoot(e, n) {
    this.data = yn([e, n]), this.data.height = e.height + 1, this.data.leaf = !1, vn(this.data, this.toBBox);
  }
  _chooseSplitIndex(e, n, r) {
    let s, i = 1 / 0, o = 1 / 0;
    for (let a = n; a <= r - n; a++) {
      const u = Kn(e, 0, a, this.toBBox), c = Kn(e, a, r, this.toBBox), l = I0(u, c), h = Ps(u) + Ps(c);
      l < i ? (i = l, s = a, o = h < o ? h : o) : l === i && h < o && (o = h, s = a);
    }
    return s || r - n;
  }
  // sorts node children by the best axis for split
  _chooseSplitAxis(e, n, r) {
    const s = e.leaf ? this.compareMinX : E0, i = e.leaf ? this.compareMinY : C0, o = this._allDistMargin(e, n, r, s), a = this._allDistMargin(e, n, r, i);
    o < a && e.children.sort(s);
  }
  // total margin of all possible split distributions where each node is at least m full
  _allDistMargin(e, n, r, s) {
    e.children.sort(s);
    const i = this.toBBox, o = Kn(e, 0, n, i), a = Kn(e, r - n, r, i);
    let u = Dr(o) + Dr(a);
    for (let c = n; c < r - n; c++) {
      const l = e.children[c];
      Xn(o, e.leaf ? i(l) : l), u += Dr(o);
    }
    for (let c = r - n - 1; c >= n; c--) {
      const l = e.children[c];
      Xn(a, e.leaf ? i(l) : l), u += Dr(a);
    }
    return u;
  }
  _adjustParentBBoxes(e, n, r) {
    for (let s = r; s >= 0; s--)
      Xn(n[s], e);
  }
  _condense(e) {
    for (let n = e.length - 1, r; n >= 0; n--)
      e[n].children.length === 0 ? n > 0 ? (r = e[n - 1].children, r.splice(r.indexOf(e[n]), 1)) : this.clear() : vn(e[n], this.toBBox);
  }
}
function _0(t, e, n) {
  if (!n) return e.indexOf(t);
  for (let r = 0; r < e.length; r++)
    if (n(t, e[r])) return r;
  return -1;
}
function vn(t, e) {
  Kn(t, 0, t.children.length, e, t);
}
function Kn(t, e, n, r, s) {
  s || (s = yn(null)), s.minX = 1 / 0, s.minY = 1 / 0, s.maxX = -1 / 0, s.maxY = -1 / 0;
  for (let i = e; i < n; i++) {
    const o = t.children[i];
    Xn(s, t.leaf ? r(o) : o);
  }
  return s;
}
function Xn(t, e) {
  return t.minX = Math.min(t.minX, e.minX), t.minY = Math.min(t.minY, e.minY), t.maxX = Math.max(t.maxX, e.maxX), t.maxY = Math.max(t.maxY, e.maxY), t;
}
function E0(t, e) {
  return t.minX - e.minX;
}
function C0(t, e) {
  return t.minY - e.minY;
}
function Ps(t) {
  return (t.maxX - t.minX) * (t.maxY - t.minY);
}
function Dr(t) {
  return t.maxX - t.minX + (t.maxY - t.minY);
}
function R0(t, e) {
  return (Math.max(e.maxX, t.maxX) - Math.min(e.minX, t.minX)) * (Math.max(e.maxY, t.maxY) - Math.min(e.minY, t.minY));
}
function I0(t, e) {
  const n = Math.max(t.minX, e.minX), r = Math.max(t.minY, e.minY), s = Math.min(t.maxX, e.maxX), i = Math.min(t.maxY, e.maxY);
  return Math.max(0, s - n) * Math.max(0, i - r);
}
function ks(t, e) {
  return t.minX <= e.minX && t.minY <= e.minY && e.maxX <= t.maxX && e.maxY <= t.maxY;
}
function xr(t, e) {
  return e.minX <= t.maxX && e.minY <= t.maxY && e.maxX >= t.minX && e.maxY >= t.minY;
}
function yn(t) {
  return {
    children: t,
    height: 1,
    leaf: !0,
    minX: 1 / 0,
    minY: 1 / 0,
    maxX: -1 / 0,
    maxY: -1 / 0
  };
}
function Na(t, e, n, r, s) {
  const i = [e, n];
  for (; i.length; ) {
    if (n = i.pop(), e = i.pop(), n - e <= r) continue;
    const o = e + Math.ceil((n - e) / r / 2) * r;
    wl(t, o, e, n, s), i.push(e, o, o, n);
  }
}
class $R {
  constructor(e = !1) {
    C(this, "_tree", /* @__PURE__ */ new Map());
    // unitId -> subUnitId -> row -> column -> ids
    C(this, "_oneCellCache", /* @__PURE__ */ new Map());
    C(this, "_kdTree", /* @__PURE__ */ new Map());
    this._enableOneCellCache = e;
  }
  dispose() {
    this.clear();
  }
  getTree(e, n) {
    return this._tree.has(e) || this._tree.set(e, /* @__PURE__ */ new Map()), this._tree.get(e).has(n) || this._tree.get(e).set(n, new Aa()), this._tree.get(e).get(n);
  }
  _getOneCellCache(e, n, r, s) {
    return this._oneCellCache.has(e) || this._oneCellCache.set(e, /* @__PURE__ */ new Map()), this._oneCellCache.get(e).has(n) || this._oneCellCache.get(e).set(n, /* @__PURE__ */ new Map()), this._oneCellCache.get(e).get(n).has(r) || this._oneCellCache.get(e).get(n).set(r, /* @__PURE__ */ new Map()), this._oneCellCache.get(e).get(n).get(r).has(s) || this._oneCellCache.get(e).get(n).get(r).set(s, /* @__PURE__ */ new Set()), this._oneCellCache.get(e).get(n).get(r).get(s);
  }
  _removeOneCellCache(e, n, r, s, i) {
    const o = this._oneCellCache.get(e);
    if (!o) return;
    const a = o.get(n);
    if (!a) return;
    const u = a.get(r);
    if (!u) return;
    const c = u.get(s);
    c && c.delete(i);
  }
  _removeCellCacheByRange(e) {
    const { unitId: n, sheetId: r, range: s, id: i } = e, o = this._oneCellCache.get(n);
    if (!o) return;
    const a = o.get(r);
    if (!a) return;
    const { startRow: u, startColumn: c, endRow: l, endColumn: h } = s;
    for (let d = u; d <= l; d++) {
      const f = a.get(d);
      if (f)
        for (let E = c; E <= h; E++) {
          const R = f.get(E);
          R && R.delete(i);
        }
    }
  }
  _insertOneCellCache(e, n, r, s, i) {
    this._getOneCellCache(e, n, r, s).add(i);
  }
  _getRdTreeItems(e) {
    const n = [];
    for (const [r, s] of e)
      for (const [i, o] of s)
        n.push({
          x: i,
          y: r,
          ids: o
        });
    return n;
  }
  _searchByOneCellCache(e) {
    var E;
    const { unitId: n, sheetId: r, range: s } = e, { startRow: i, startColumn: o, endRow: a, endColumn: u } = s, c = (E = this._kdTree.get(n)) == null ? void 0 : E.get(r);
    if (!c)
      return [];
    const { tree: l, items: h } = c, d = l.range(o, i, u, a), f = [];
    for (const R of d) {
      const O = h[R];
      f.push(...Array.from(O.ids));
    }
    return f;
  }
  /**
   * Open the kd-tree search state.
   * The kd-tree is used to search for data in a single cell.
   */
  openKdTree() {
    var e;
    for (const [n, r] of this._oneCellCache) {
      this._kdTree.has(n) || this._kdTree.set(n, /* @__PURE__ */ new Map());
      for (const [s, i] of r) {
        const o = this._getRdTreeItems(i), a = new ji(o.length);
        (e = this._kdTree.get(n)) == null || e.set(s, {
          tree: a,
          items: o
        });
        for (const u of o)
          a.add(u.x, u.y);
        a.finish();
      }
    }
  }
  closeKdTree() {
    var e;
    for (const [n, r] of this._oneCellCache)
      for (const [s, i] of r)
        (e = this._kdTree.get(n)) == null || e.set(s, void 0);
  }
  insert(e) {
    const { unitId: n, sheetId: r, range: s, id: i } = e;
    if (!n || n.length === 0)
      return;
    let { startRow: o, endRow: a, startColumn: u, endColumn: c } = s;
    if (this._enableOneCellCache && o === a && u === c) {
      this._insertOneCellCache(n, r, o, u, i);
      return;
    }
    const l = this.getTree(n, r);
    Number.isNaN(o) && (o = 0), Number.isNaN(u) && (u = 0), Number.isNaN(a) && (a = Number.POSITIVE_INFINITY), Number.isNaN(c) && (c = Number.POSITIVE_INFINITY), l.insert({
      minX: u,
      minY: o,
      maxX: c,
      maxY: a,
      id: i
    });
  }
  bulkInsert(e) {
    for (const n of e)
      this.insert(n);
  }
  *searchGenerator(e) {
    var a;
    const { unitId: n, sheetId: r, range: s } = e;
    if (this._enableOneCellCache) {
      const u = this._searchByOneCellCache(e);
      for (const c of u)
        yield c;
    }
    const i = (a = this._tree.get(n)) == null ? void 0 : a.get(r);
    if (!i)
      return;
    const o = i.search({
      minX: s.startColumn,
      minY: s.startRow,
      maxX: s.endColumn,
      maxY: s.endRow
    });
    for (const u of o)
      yield u.id;
  }
  bulkSearch(e, n) {
    const r = /* @__PURE__ */ new Set();
    for (const s of e)
      for (const i of this.searchGenerator(s))
        (n == null ? void 0 : n.has(i)) !== !0 && r.add(i);
    return r;
  }
  removeById(e, n) {
    var r, s;
    n ? ((r = this._tree.get(e)) == null || r.delete(n), (s = this._oneCellCache.get(e)) == null || s.delete(n)) : (this._tree.delete(e), this._oneCellCache.delete(e));
  }
  _removeRTreeItem(e) {
    const { unitId: n, sheetId: r, range: s, id: i } = e, o = this.getTree(n, r), a = o.search({
      minX: s.startColumn,
      minY: s.startRow,
      maxX: s.endColumn,
      maxY: s.endRow
    });
    for (let u = 0; u < a.length; u++)
      a[u].id === i && o.remove(a[u]);
  }
  remove(e) {
    const { unitId: n, sheetId: r, range: s, id: i } = e, { startRow: o, startColumn: a, endRow: u, endColumn: c } = s;
    this._enableOneCellCache ? o === u && a === c ? this._removeOneCellCache(n, r, s.startRow, s.startColumn, i) : (this._removeCellCacheByRange(e), this._removeRTreeItem(e)) : this._removeRTreeItem(e);
  }
  bulkRemove(e) {
    for (const n of e)
      this.remove(n);
  }
  clear() {
    this._tree.clear(), this._oneCellCache.clear();
  }
  toJSON() {
    const e = {};
    return this._tree.forEach((n, r) => {
      e[r] = {}, n.forEach((s, i) => {
        e[r][i] = s.toJSON();
      });
    }), e;
  }
  fromJSON(e) {
    this._tree.clear();
    for (const n in e) {
      this._tree.set(n, /* @__PURE__ */ new Map());
      for (const r in e[n]) {
        const s = new Aa();
        s.fromJSON(e[n][r]), this._tree.get(n).set(r, s);
      }
    }
  }
}
Hl();
export {
  YC as ABCToNumber,
  P0 as AUTO_HEIGHT_FOR_MERGED_CELLS,
  tt as AbsoluteRefType,
  Bn as ActionIterator,
  lm as AlignTypeH,
  cm as AlignTypeV,
  fm as ArrangeTypeEnum,
  qf as ArrowsAndMarkersShapes,
  iR as AsyncInterceptorManager,
  oi as AuthzIoLocalService,
  _u as AutoFillSeries,
  Bt as BaselineOffset,
  Qf as BasicShapes,
  Hp as BlockType,
  we as BooleanNumber,
  Xe as BorderStyleTypes,
  Eu as BorderType,
  st as BuildTextUtils,
  ms as BulletAlignment,
  xo as COLORS,
  xf as CanceledError,
  zn as CellModeEnum,
  dn as CellValueType,
  Ln as Color,
  gs as ColorBuilder,
  Nt as ColorKit,
  vt as ColorType,
  Yp as ColumnSeparatorType,
  Ys as CommandService,
  ar as CommandType,
  Cu as CommonHideTypes,
  AE as ConfigService,
  Ff as ContextService,
  Ru as CopyPasteType,
  wo as CustomCommandExecutionError,
  An as CustomDecorationType,
  mn as CustomRangeType,
  $C as DEFAULT_CELL,
  tl as DEFAULT_DOC,
  TR as DEFAULT_DOCUMENT_SUB_COMPONENT_ID,
  Wd as DEFAULT_EMPTY_DOCUMENT_VALUE,
  kC as DEFAULT_RANGE,
  PC as DEFAULT_RANGE_ARRAY,
  FC as DEFAULT_SELECTION,
  Ap as DEFAULT_SLIDE,
  gt as DEFAULT_STYLES,
  G_ as DEFAULT_WORKSHEET_COLUMN_COUNT,
  cR as DEFAULT_WORKSHEET_COLUMN_COUNT_KEY,
  Z_ as DEFAULT_WORKSHEET_COLUMN_TITLE_HEIGHT,
  gR as DEFAULT_WORKSHEET_COLUMN_TITLE_HEIGHT_KEY,
  X_ as DEFAULT_WORKSHEET_COLUMN_WIDTH,
  dR as DEFAULT_WORKSHEET_COLUMN_WIDTH_KEY,
  V_ as DEFAULT_WORKSHEET_ROW_COUNT,
  lR as DEFAULT_WORKSHEET_ROW_COUNT_KEY,
  K_ as DEFAULT_WORKSHEET_ROW_HEIGHT,
  hR as DEFAULT_WORKSHEET_ROW_HEIGHT_KEY,
  J_ as DEFAULT_WORKSHEET_ROW_TITLE_WIDTH,
  fR as DEFAULT_WORKSHEET_ROW_TITLE_WIDTH_KEY,
  iu as DOCS_FORMULA_BAR_EDITOR_UNIT_ID_KEY,
  su as DOCS_NORMAL_EDITOR_UNIT_ID_KEY,
  Hd as DOCS_ZEN_EDITOR_UNIT_ID_KEY,
  Ag as DOC_RANGE_TYPE,
  Qp as DashStyleType,
  O_ as DataStreamTreeNodeType,
  ln as DataStreamTreeTokenType,
  _l as DataValidationErrorStyle,
  p0 as DataValidationImeMode,
  El as DataValidationOperator,
  Cl as DataValidationRenderMode,
  Rl as DataValidationStatus,
  Il as DataValidationType,
  Iu as DeleteDirection,
  OR as DependentOn,
  Bf as DesktopLogService,
  vu as DeveloperMetadataVisibility,
  yu as Dimension,
  wu as Direction,
  nt as Disposable,
  Mi as DisposableCollection,
  Bp as DocStyleType,
  jt as DocumentDataModel,
  ku as DocumentFlavor,
  gm as DrawingTypeEnum,
  oE as EDITOR_ACTIVATED,
  Np as EXTENSION_NAMES,
  NE as ErrorService,
  f0 as EventState,
  MR as EventSubject,
  Fi as FBase,
  al as FBaseInitialable,
  ss as FBlob,
  ci as FEnum,
  hi as FEventName,
  di as FHooks,
  yR as FOCUSING_COMMON_DRAWINGS,
  Nr as FOCUSING_DOC,
  _R as FOCUSING_EDITOR_BUT_HIDDEN,
  ER as FOCUSING_EDITOR_INPUT_FORMULA,
  RR as FOCUSING_EDITOR_STANDALONE,
  aE as FOCUSING_FX_BAR_EDITOR,
  IR as FOCUSING_PANEL_EDITOR,
  Gn as FOCUSING_SHEET,
  Tr as FOCUSING_SLIDE,
  Ar as FOCUSING_UNIT,
  CR as FOCUSING_UNIVER_EDITOR,
  vR as FOCUSING_UNIVER_EDITOR_STANDALONE_SINGLE_MODE,
  wR as FORMULA_EDITOR_ACTIVATED,
  pi as FUniver,
  gi as FUtil,
  jp as FollowNumberWithType,
  Vs as FontItalic,
  Yn as FontStyleType,
  Gs as FontWeight,
  Wp as GridType,
  pg as HLSColor,
  Xt as HorizontalAlign,
  bE as IAuthzIoService,
  Pt as ICommandService,
  SE as IConfigService,
  fs as IContextService,
  Oa as IImageIoService,
  xR as ILocalStorageService,
  Mt as ILogService,
  LE as IMentionIOService,
  UE as IPermissionService,
  va as IResourceLoaderService,
  Bi as IResourceManagerService,
  U0 as IS_ROW_STYLE_PRECEDE_COLUMN_STYLE,
  cn as IUndoRedoService,
  _n as IUniverInstanceService,
  kR as ImageCacheMap,
  vl as ImageSourceType,
  g0 as ImageUploadStatusType,
  ot as Inject,
  Ot as Injector,
  Vn as InterceptorEffectEnum,
  rR as InterceptorManager,
  Ou as InterpolationPointType,
  JC as JSON1,
  tn as JSONX,
  Cr as LRUHelper,
  Qr as LRUMap,
  Ht as LifecycleService,
  Ve as LifecycleStages,
  Te as ListGlyphType,
  ri as LocalUndoRedoService,
  Vr as LocaleService,
  ur as LocaleType,
  $f as LogLevel,
  $t as LookUp,
  mr as MOVE_BUFFER_VALUE,
  tf as Many,
  lr as MemoryCursor,
  ai as MentionIOLocalService,
  Zr as MentionType,
  Jp as NamedStyleType,
  Yf as NilCommand,
  um as NumberUnitType,
  kt as ObjectMatrix,
  om as ObjectRelativeFromH,
  am as ObjectRelativeFromV,
  nf as Optional,
  eg as OtherShapes,
  Es as PRESET_LIST_TYPE,
  pm as PageElementType,
  dm as PageOrientType,
  Fu as PageType,
  Gp as ParagraphElementType,
  nr as ParagraphStyleBuilder,
  hr as ParagraphStyleValue,
  PE as PermissionService,
  fl as PermissionStatus,
  Ra as Plugin,
  ns as PluginService,
  Xp as PositionedObjectLayoutType,
  Ft as PresetListType,
  bu as ProtectionType,
  Ge as Quantity,
  Nm as QuickListType,
  ZC as QuickListTypeMap,
  Sg as RANGE_DIRECTION,
  De as RANGE_TYPE,
  Aa as RBush,
  Z0 as RCDisposable,
  cC as RGBA_PAREN,
  lC as RGB_PAREN,
  Zf as ROTATE_BUFFER_VALUE,
  $R as RTree,
  tr as Range,
  en as Rectangle,
  vf as RediConsumer,
  ds as RediContext,
  at as RediError,
  gu as RediProvider,
  Tn as RedoCommand,
  RE as RedoCommandId,
  zC as RefAlias,
  $i as Registry,
  ul as RegistryAsMap,
  Su as RelativeDate,
  mm as RelativeSlideLink,
  VE as ResourceManagerService,
  Ks as RgbColor,
  gn as RichTextBuilder,
  Zt as RichTextValue,
  J0 as RxDisposable,
  BC as SHEET_EDITOR_UNITS,
  zp as SectionType,
  Zd as Self,
  Au as SheetTypes,
  eE as SheetViewModel,
  Jd as SkipSelf,
  el as SliceBodyType,
  cl as SlideDataModel,
  Zp as SpacingRule,
  tg as SpecialShapes,
  k_ as Styles,
  gg as THEME_COLORS,
  qp as TabStopAlignment,
  tm as TableAlignmentType,
  nm as TableLayoutType,
  sm as TableRowHeightRule,
  em as TableSizeType,
  rm as TableTextWrapType,
  Nu as TextDecoration,
  Jt as TextDecorationBuilder,
  er as TextDirection,
  Vp as TextDirectionType,
  Qt as TextStyleBuilder,
  cr as TextStyleValue,
  Ke as TextX,
  ce as TextXActionType,
  Xs as ThemeColor,
  ft as ThemeColorType,
  Di as ThemeColors,
  ml as ThemeService,
  re as Tools,
  Nn as UndoCommand,
  IE as UndoCommandId,
  Ui as UnitModel,
  GE as Univer,
  ni as UniverInstanceService,
  Fe as UniverInstanceType,
  Pe as UpdateDocsAttributeType,
  rr as UserManagerService,
  hn as VerticalAlign,
  im as VerticalAlignmentType,
  H0 as WithDependency,
  of as WithNew,
  ts as Workbook,
  es as Worksheet,
  xn as WrapStrategy,
  Kp as WrapTextType,
  B_ as addLinkToDocumentModel,
  tC as afterInitApply,
  eC as afterTime,
  UR as awaitTime,
  Jf as binSearchFirstGreaterThanTarget,
  nC as binarySearchArray,
  q0 as bufferDebounceTime,
  AC as cellToRange,
  hm as characterSpacingControlType,
  NC as checkForSubstrings,
  iC as checkIfMove,
  TC as checkParagraphHasBullet,
  MC as checkParagraphHasIndent,
  fp as checkParagraphHasIndentByStyle,
  sC as codeToBlob,
  ha as composeBody,
  x_ as composeInterceptors,
  Mo as composeStyles,
  LC as concatMatrixArray,
  j0 as connectDependencies,
  B0 as connectInjector,
  uC as convertBodyToHtml,
  Ng as convertCellToRange,
  Do as covertTextRunToHtml,
  sR as createAsyncInterceptorKey,
  ii as createDefaultUser,
  Sr as createDocumentModelWithStyle,
  Ct as createIdentifier,
  nR as createInterceptorKey,
  k0 as createInternalEditorID,
  Qo as createRowColIter,
  rn as dayjs,
  S0 as debounce,
  T0 as dedupe,
  Lu as deepCompare,
  PR as delayAnimationFrame,
  pp as deleteContent,
  tE as extractPureTextFromCell,
  $0 as forwardRef,
  Gf as fromCallback,
  DR as fromEventSubject,
  X0 as fromObservable,
  qt as generateRandomId,
  b0 as get,
  fn as getArrayLength,
  Dt as getBodySlice,
  Os as getBodySliceHtml,
  OC as getBorderStyleType,
  EC as getCellInfoInMergeData,
  gC as getCellValueType,
  Lt as getColorStyle,
  jm as getCustomBlockSlice,
  Wm as getCustomDecorationSlice,
  Hm as getCustomRangeSlice,
  bC as getDocsUpdateBody,
  HC as getIntersectRange,
  pR as getOriginCellValue,
  Bm as getParagraphsSlice,
  oC as getReverseDirection,
  QC as getSectionBreakSlice,
  $m as getTableSlice,
  ei as getTextRunSlice,
  mR as getWorksheetUID,
  D0 as groupBy,
  wC as handleStyleToString,
  xC as hashAlgorithm,
  Li as horizontalLineSegmentsSubtraction,
  Vo as insertMatrixArray,
  gp as insertTextToContent,
  co as isAsyncDependencyItem,
  ys as isAsyncHook,
  hC as isBlackColor,
  L0 as isBooleanString,
  IC as isCellCoverable,
  mC as isCellV,
  ao as isClassDependencyItem,
  ou as isCtor,
  go as isDisposable,
  Tg as isEmptyCell,
  uo as isFactoryDependencyItem,
  yC as isFormulaId,
  vC as isFormulaString,
  fC as isICellData,
  zd as isInternalEditorID,
  aC as isNodeEnv,
  j_ as isNotNullOrUndefined,
  pC as isNullCell,
  d0 as isNumeric,
  aR as isRangesEqual,
  DC as isRealNum,
  bR as isSafeNumeric,
  Mg as isSameStyleTextRun,
  uR as isUnitRangesEqual,
  SC as isValidRange,
  lo as isValueDependencyItem,
  dC as isWhiteColor,
  x0 as makeArray,
  RC as makeCellRangeToRangeData,
  CC as makeCellToSelection,
  eR as makeCustomRangeStream,
  nu as merge,
  kE as mergeOverrideWithDependencies,
  AR as mergeSets,
  A0 as mergeWith,
  Q_ as mergeWorksheetSnapshotWithDefault,
  oR as mixinClass,
  Ko as moveMatrixArray,
  jC as moveRangeByOffset,
  LR as nameCharacterCheck,
  qC as normalizeBody,
  _s as normalizeTextRuns,
  VC as numberToABC,
  GC as numberToListABC,
  Op as numfmt,
  WC as queryObjectMatrix,
  K0 as registerDependencies,
  cs as remove,
  $p as repeatStringNumTimes,
  NR as replaceInDocumentBody,
  SR as requestImmediateMacroTask,
  M0 as rotate,
  rC as searchArray,
  Xf as searchInOrderedArray,
  _C as selectionToArray,
  Uf as sequence,
  Lf as sequenceAsync,
  mu as sequenceExecute,
  Q0 as sequenceExecuteAsync,
  N0 as set,
  F0 as setDependencies,
  Df as shallowEqual,
  FR as skipParseTagNames,
  UC as sliceMatrixArray,
  KC as sortRules,
  XC as sortRulesByDesc,
  ps as sortRulesFactory,
  Go as spliceArray,
  Uu as splitIntoGrid,
  Kf as takeAfter,
  ru as textDiff,
  tR as throttle,
  Ze as toDisposable,
  Mf as touchDependencies,
  Km as updateAttributeByDelete,
  Xm as updateAttributeByInsert,
  W0 as useDependency,
  V0 as useDependencyContext,
  G0 as useDependencyContextValue,
  Tf as useDependencyValue,
  Af as useInjector,
  z0 as useObservable,
  Y0 as useUpdateBinder
};
