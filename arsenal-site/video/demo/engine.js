/* Drawing toolkit for the Arsenal demo. Everything is a pure function of time t,
   so any frame can be rendered on its own and every render is identical. */
(function () {
  'use strict';
  var W = 1920, H = 1080;
  var cv = document.getElementById('c'), ctx = cv.getContext('2d');

  var C = {
    bg: '#EEF2FA', ink: '#0B1226', muted: '#5A6480', line: '#DCE2EF', card: '#FFFFFF',
    navy: '#34489A', brand: '#3F548B', ice: '#9CC8EC', facet: '#6E8FD6', deep: '#3B47A6',
    tip: '#8B5CF6', green: '#14915F', greenSoft: '#DDF3EA', red: '#D9463B', gold: '#F2B33D',
    night: '#060912', nightInk: '#E9EEF9', nightMuted: '#9AA6C3', soft: '#E2E8F8'
  };
  var F = '"Archivo", system-ui, sans-serif', M = '"JetBrains Mono", ui-monospace, monospace';

  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function seg(t, a, b) { return clamp((t - a) / (b - a), 0, 1); }
  function eo(x) { x = clamp(x, 0, 1); return 1 - Math.pow(1 - x, 3); }
  function eio(x) { x = clamp(x, 0, 1); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
  function back(x) { x = clamp(x, 0, 1); var c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function life(t, a, b, fi, fo) { return Math.min(eo(seg(t, a, a + (fi || .4))), 1 - eio(seg(t, b - (fo || .4), b))); }
  function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function hex(h, a) { var n = parseInt(h.slice(1), 16); return 'rgba(' + (n >> 16 & 255) + ',' + (n >> 8 & 255) + ',' + (n & 255) + ',' + (a == null ? 1 : clamp(a, 0, 1)) + ')'; }

  function font(w, size, fam, style, stretch) { ctx.font = (style || 'normal') + ' ' + w + ' ' + size + 'px ' + (fam || F); ctx.fontStretch = stretch || 'normal'; }
  function rr(x, y, w, h, r) { r = Math.min(r, w / 2, h / 2); ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function card(x, y, w, h, r, opts) {
    opts = opts || {};
    ctx.save();
    ctx.shadowColor = 'rgba(11,18,38,' + (opts.shadow == null ? .16 : opts.shadow) + ')'; ctx.shadowBlur = opts.blur || 50; ctx.shadowOffsetY = opts.oy == null ? 18 : opts.oy;
    rr(x, y, w, h, r); ctx.fillStyle = opts.fill || C.card; ctx.fill();
    ctx.restore();
    if (opts.stroke !== false) { rr(x, y, w, h, r); ctx.strokeStyle = opts.stroke || C.line; ctx.lineWidth = opts.lw || 1.5; ctx.stroke(); }
  }
  function text(s, x, y, size, w, color, opts) {
    opts = opts || {}; font(w || '600', size, opts.fam, opts.style, opts.stretch);
    ctx.textAlign = opts.align || 'left'; ctx.textBaseline = opts.base || 'alphabetic'; ctx.fillStyle = color || C.ink;
    if (opts.track) { ctx.letterSpacing = opts.track + 'px'; }
    ctx.fillText(s, x, y); ctx.letterSpacing = '0px'; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  }
  function width(s, size, w, opts) { opts = opts || {}; font(w || '600', size, opts.fam, opts.style, opts.stretch); if (opts.track) ctx.letterSpacing = opts.track + 'px'; var m = ctx.measureText(s).width; ctx.letterSpacing = '0px'; return m; }
  function mono(s, x, y, size, color, opts) { opts = opts || {}; text(s.toUpperCase(), x, y, size, '600', color || C.muted, { fam: M, align: opts.align, track: opts.track == null ? 1.5 : opts.track, base: opts.base }); }
  function typed(s, k) { return s.slice(0, Math.round(s.length * clamp(k, 0, 1))); }

  // a check mark in a circle
  function check(x, y, r, color, a, k) {
    k = k == null ? 1 : k; ctx.save(); ctx.globalAlpha *= a == null ? 1 : a;
    ctx.fillStyle = color || C.green; ctx.beginPath(); ctx.arc(x, y, r * (.6 + .4 * back(k)), 0, 6.283); ctx.fill();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = r * .24; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    var p = [[x - r * .42, y + r * .02], [x - r * .1, y + r * .34], [x + r * .46, y - r * .32]]; partial(p, seg(k, .3, 1));
    ctx.restore();
  }
  function partial(pts, k) {
    var L = 0, d = []; for (var i = 1; i < pts.length; i++) { var l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); d.push(l); L += l; }
    var g = L * clamp(k, 0, 1); ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
    for (var j = 1; j < pts.length; j++) { if (g >= d[j - 1]) { ctx.lineTo(pts[j][0], pts[j][1]); g -= d[j - 1]; } else { var f = d[j - 1] ? g / d[j - 1] : 0; ctx.lineTo(lerp(pts[j - 1][0], pts[j][0], f), lerp(pts[j - 1][1], pts[j][1], f)); break; } }
    ctx.stroke();
  }
  function glow(x, y, r, color, a) { var g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, hex(color, a)); g.addColorStop(1, hex(color, 0)); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 6.283); ctx.fill(); }
  function star(x, y, r, color, a) { glow(x, y, r * 8, color, .35 * a); ctx.fillStyle = hex(color, a); ctx.beginPath(); ctx.arc(x, y, r, 0, 6.283); ctx.fill(); ctx.fillStyle = 'rgba(255,255,255,' + a + ')'; ctx.beginPath(); ctx.arc(x, y, r * .5, 0, 6.283); ctx.fill(); }
  function spark(x, y, s, color, a, rot) { ctx.save(); ctx.translate(x, y); ctx.rotate(rot || 0); ctx.fillStyle = hex(color, a == null ? 1 : a); ctx.beginPath(); ctx.moveTo(0, -s); ctx.quadraticCurveTo(s * .18, -s * .18, s, 0); ctx.quadraticCurveTo(s * .18, s * .18, 0, s); ctx.quadraticCurveTo(-s * .18, s * .18, -s, 0); ctx.quadraticCurveTo(-s * .18, -s * .18, 0, -s); ctx.fill(); ctx.restore(); }

  // mouse pointer with a name tag ("Agent", "Partner")
  function cursor(x, y, label, color, a) {
    ctx.save(); ctx.globalAlpha *= a == null ? 1 : a; ctx.translate(x, y);
    ctx.shadowColor = 'rgba(11,18,38,.25)'; ctx.shadowBlur = 8; ctx.shadowOffsetY = 3;
    ctx.fillStyle = color; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, 30); ctx.lineTo(8, 23); ctx.lineTo(14, 36); ctx.lineTo(19, 33); ctx.lineTo(13, 21); ctx.lineTo(23, 21); ctx.closePath(); ctx.fill();
    ctx.shadowColor = 'transparent'; ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.stroke();
    if (label) { var w = width(label, 15, '700') + 22; rr(18, 34, w, 28, 14); ctx.fillStyle = color; ctx.fill(); text(label, 29, 53, 15, '700', '#fff'); }
    ctx.restore();
  }

  // rubber stamp that slams in, with a shockwave
  function stamp(label, x, y, t, t0, color, opts) {
    opts = opts || {}; if (t < t0) return;
    var k = seg(t, t0, t0 + .28), s = lerp(2.4, 1, eo(k)), a = Math.min(1, k * 3) * (opts.alpha == null ? 1 : opts.alpha);
    var size = opts.size || 54, w = width(label, size, '850', { stretch: 'expanded', track: 4 }) + 70, h = size + 44;
    ctx.save(); ctx.translate(x, y); ctx.rotate((opts.rot == null ? -6 : opts.rot) * Math.PI / 180); ctx.scale(s, s); ctx.globalAlpha *= a;
    if (opts.fill) { rr(-w / 2, -h / 2, w, h, 16); ctx.fillStyle = opts.fill; ctx.fill(); }
    rr(-w / 2, -h / 2, w, h, 16); ctx.strokeStyle = color; ctx.lineWidth = 7; ctx.stroke();
    rr(-w / 2 + 9, -h / 2 + 9, w - 18, h - 18, 10); ctx.lineWidth = 2; ctx.stroke();
    text(label, 0, 4, size, '850', color, { align: 'center', base: 'middle', stretch: 'expanded', track: 4 });
    ctx.restore();
    var sk = seg(t, t0 + .2, t0 + .9);
    if (sk > 0 && sk < 1) { ctx.save(); ctx.strokeStyle = hex(opts.ring || C.navy, (1 - sk) * .45); ctx.lineWidth = 4 * (1 - sk) + 1; ctx.beginPath(); ctx.arc(x, y, 80 + sk * 380, 0, 6.283); ctx.stroke(); ctx.restore(); }
    if (opts.confetti !== false) confetti(x, y, t, t0 + .22, opts.seed || 3, opts.count || 26);
  }

  var CONF = ['#34489A', '#9CC8EC', '#F2B33D', '#14915F', '#8B5CF6', '#6E8FD6', '#D9463B'];
  function confetti(x, y, t, t0, seed, n) {
    var u = t - t0; if (u < 0 || u > 1.8) return; var r = rng(seed);
    for (var i = 0; i < n; i++) {
      var ang = r() * 6.283, sp = 260 + r() * 520, vx = Math.cos(ang) * sp, vy = Math.sin(ang) * sp - 260, rot = r() * 6, vr = (r() - .5) * 14, col = CONF[i % CONF.length];
      var px = x + vx * u * (1 - u * .35), py = y + vy * u + 560 * u * u, a = 1 - seg(u, 1.1, 1.8);
      ctx.save(); ctx.translate(px, py); ctx.rotate(rot + vr * u); ctx.fillStyle = hex(col, a); ctx.fillRect(-7, -3.5, 14, 7); ctx.restore();
    }
  }

  // number that counts up between t0 and t1
  function countTo(to, t, t0, t1, dec) { var k = eo(seg(t, t0, t1)); return (to * k).toFixed(dec || 0); }

  window.K = { W: W, H: H, ctx: ctx, C: C, F: F, M: M, clamp: clamp, seg: seg, eo: eo, eio: eio, back: back, lerp: lerp, life: life, rng: rng, hex: hex,
    font: font, rr: rr, card: card, text: text, width: width, mono: mono, typed: typed, check: check, partial: partial, glow: glow, star: star, spark: spark,
    cursor: cursor, stamp: stamp, confetti: confetti, countTo: countTo };
})();
