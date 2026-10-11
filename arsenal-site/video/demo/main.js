/* Arsenal demo: timeline, camera and screen-space scenes. Load with ?v=tech or ?v=epic. */
(function () {
  'use strict';
  var k = window.K, ctx = k.ctx, C = k.C, seg = k.seg, eo = k.eo, eio = k.eio, back = k.back, lerp = k.lerp, clamp = k.clamp, W = k.W, H = k.H;
  var POS = window.POS, ev = window.SCN.ev;
  var version = (/[?&]v=(\w+)/.exec(location.search) || [0, 'tech'])[1];
  var Q = null;

  function makeQ(c) {
    return {
      c: c, beat: c.beat,
      V: function (key) { return c.vo[key]; }, D: function (key) { return c.vodur[key]; }, S: function (s) { return c.sec[s]; },
      nb: function (t) { return c.b0 + Math.ceil((t - c.b0) / c.beat - 1e-6) * c.beat; },            // next beat at or after t
      lastBar: function (t) { var n = Math.floor((t - c.b0) / c.bar); return c.b0 + n * c.bar; },
      hi: function (t) { return c.hi.some(function (r) { return t >= r[0] && t <= r[1]; }); }
    };
  }

  // ───────── the Arsenal mark as a crystal (the real lattice of the logo) ─────────
  var TRIS = [['a',[5,2],[5,0],[6,1]],['a',[6,3],[6,1],[7,2]],['a',[7,4],[7,2],[8,3]],['a',[8,5],[8,3],[9,4]],['a',[9,6],[9,4],[10,5]],['a',[5,4],[5,2],[6,3]],['a',[6,5],[6,3],[7,4]],['a',[7,6],[7,4],[8,5]],['a',[8,7],[8,5],[9,6]],['b',[5,4],[5,2],[4,3]],['b',[6,1],[6,3],[5,2]],['b',[7,2],[7,4],[6,3]],['b',[8,3],[8,5],[7,4]],['b',[9,4],[9,6],[8,5]],['b',[6,3],[6,5],[5,4]],['b',[7,4],[7,6],[6,5]],['b',[8,5],[8,7],[7,6]],['b',[5,2],[5,0],[4,1]],['b',[4,3],[4,1],[3,2]],['b',[3,4],[3,2],[2,3]],['b',[2,5],[2,3],[1,4]],['b',[1,6],[1,4],[0,5]],['b',[4,5],[4,3],[3,4]],['b',[3,6],[3,4],[2,5]],['b',[2,7],[2,5],[1,6]],['a',[4,1],[4,3],[5,2]],['a',[3,2],[3,4],[4,3]],['a',[2,3],[2,5],[3,4]],['a',[1,4],[1,6],[2,5]],['a',[4,3],[4,5],[5,4]],['a',[3,4],[3,6],[4,5]],['a',[2,5],[2,7],[3,6]],['t',[5,6],[4,7],[5,8]],['t',[5,6],[6,7],[5,8]],['t',[4,7],[3,8],[5,8]],['t',[6,7],[7,8],[5,8]]];
  var EDGES = []; (function () { var seen = {}; TRIS.forEach(function (tr) { for (var e = 0; e < 3; e++) { var a = tr[e + 1], b = tr[(e + 1) % 3 + 1], key = [a, b].map(String).sort().join('|'); if (!seen[key]) { seen[key] = 1; EDGES.push([a, b]); } } }); })();
  var COMPANY_PTS = [[3, 2], [7, 2], [1, 4], [9, 4], [5, 4], [2, 7], [8, 7]];
  var COMPANIES = ['Accounting AI', 'Family Office', 'Insurance', 'Implementation', 'Legacy AI', 'Publishing', 'Robotics'];
  function crystal(cx, top, h, o) {
    var w = h * 640.68 / 750.13, x0 = cx - w / 2; function P(p) { return [x0 + p[0] / 10 * w, top + p[1] / 8 * h]; }
    var fa = o.facets == null ? 1 : o.facets, ek = o.edges == null ? 1 : o.edges;
    if (fa > 0) TRIS.forEach(function (tr, i) {
      var a = P(tr[1]), b = P(tr[2]), c = P(tr[3]), u = ((a[0] + b[0] + c[0]) / 3 - x0) / w, v = ((a[1] + b[1] + c[1]) / 3 - top) / h, g = clamp(u * .6 + v * .4, 0, 1);
      var col = tr[0] === 't' ? C.tip : (g < .5 ? (tr[0] === 'a' ? '#9CC8EC' : '#BFD9F2') : (tr[0] === 'a' ? '#6E8FD6' : '#8FA9E3'));
      if (g > .75) col = tr[0] === 'a' ? '#3B47A6' : '#5A6BC4';
      var sweep = o.sweep != null ? Math.exp(-Math.pow((u + v) / 2 - o.sweep, 2) / .01) * .5 : 0;
      ctx.fillStyle = k.hex(col, clamp(fa * (o.fillA || .85) + sweep, 0, 1)); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.lineTo(c[0], c[1]); ctx.closePath(); ctx.fill();
    });
    if (ek > 0) { ctx.strokeStyle = k.hex(o.edgeColor || '#DCEBFA', .55 * (o.edgeA || 1)); ctx.lineWidth = Math.max(1, h / 420); EDGES.forEach(function (ed, i) { var a = P(ed[0]), b = P(ed[1]), p = clamp(ek * 1.4 - (Math.min(ed[0][1], ed[1][1]) / 8) * .4, 0, 1); if (p <= 0) return; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(lerp(a[0], b[0], p), lerp(a[1], b[1], p)); ctx.stroke(); }); }
    return P;
  }

  // ───────── night sky (hook and end card) ─────────
  var R = k.rng(5), SKY = []; for (var i = 0; i < 700; i++) { var z = Math.pow(R(), 1.8); SKY.push([R() * W, R() * H, .4 + z * 1.7, R() * 6.28, .6 + R() * 1.5, z]); }
  function sky(t, a) {
    var g = ctx.createRadialGradient(W * .66, H * .38, 0, W * .66, H * .38, W * .9); g.addColorStop(0, '#13204A'); g.addColorStop(.55, '#070B18'); g.addColorStop(1, '#03050b');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    SKY.forEach(function (s) { var x = ((s[0] - t * (3 + s[5] * 12)) % W + W) % W, al = a * (.25 + s[5] * .7) * (.65 + .35 * Math.sin(t * s[4] + s[3])); ctx.fillStyle = 'rgba(225,235,255,' + al + ')'; ctx.beginPath(); ctx.arc(x, s[1], s[2], 0, 6.283); ctx.fill(); });
  }

  // headline text helper: "plain *accent* plain"
  function rich(str, x, y, size, color, accent, align, weight) {
    var parts = str.split('*'), total = 0;
    parts.forEach(function (p, i) { total += k.width(p, size, weight || '700', { style: i % 2 ? 'italic' : 'normal' }); });
    var cx = align === 'center' ? x - total / 2 : x;
    parts.forEach(function (p, i) { k.text(p, cx, y, size, weight || '700', i % 2 ? accent : color, { style: i % 2 ? 'italic' : 'normal' }); cx += k.width(p, size, weight || '700', { style: i % 2 ? 'italic' : 'normal' }); });
    return total;
  }

  // ───────── hook ─────────
  function hook(t) {
    var acc = Q.S('acc'), h1 = Q.V('h1'), h2 = Q.V('h2'), h3 = Q.V('h3'), d1 = Q.D('h1'), d2 = Q.D('h2');
    sky(t, eo(seg(t, 0, 1.2)));
    var push = eio(seg(t, h3 - .1, acc + .1)), ax = 1260, ay = 520;
    ctx.save(); ctx.translate(ax, ay); ctx.scale(1 + push * 1.6, 1 + push * 1.6); ctx.translate(-ax, -ay);
    var top = 190, hh = 640, w = hh * 640.68 / 750.13, x0 = ax - w / 2;
    var built = eio(seg(t, h2 - .1, h2 + 2.4)), fill = eo(seg(t, h2 + 1.6, h2 + 3.2));
    var P = crystal(ax, top, hh, { facets: fill * .9, edges: built, sweep: t > h2 + 3 ? ((t - h2 - 3) % 4) / 1.6 - .3 : null });
    k.glow(ax, top + hh * .45, 520, '#6E8FD6', .18 * fill);
    // the seven companies ignite one by one
    COMPANY_PTS.forEach(function (p, i) {
      var t0 = Q.nb(h1 + .15 + i * (d1 - .4) / 7), u = seg(t, t0, t0 + .4); if (u <= 0) return; ev('pop', t0);
      var q = P(p); k.star(q[0], q[1], 5 * back(u), '#BFE0FF', 1);
      var la = u * (1 - seg(t, h2 + 2.6, h2 + 3.4)); k.mono(COMPANIES[i], q[0] + (p[0] < 5 ? -18 : 18), q[1] + 6, 15, k.hex('#CFE4FF', la), { align: p[0] < 5 ? 'right' : 'left' });
    });
    var apex = P([5, 0]), ak = seg(t, h2, h2 + .5); if (ak > 0) { k.star(apex[0], apex[1], 7 * back(ak), '#FFFFFF', 1); k.mono('One platform', apex[0], apex[1] - 26, 15, k.hex('#FFFFFF', ak * (1 - seg(t, h2 + 2.6, h2 + 3.4))), { align: 'center' }); }
    ctx.restore();
    // words on the left
    var fadeAll = 1 - seg(t, h3 + .2, acc - .2);
    function line(str, y, t0, size) { var u = eo(seg(t, t0, t0 + .45)); if (u <= 0) return; ctx.save(); ctx.globalAlpha = u * fadeAll; rich(str, 130, y + (1 - u) * 26, size || 76, '#F2F5FC', '#9CC8EC', 'left', '800'); ctx.restore(); }
    ctx.save(); ctx.fontStretch = 'normal';
    if (t < h2 - .1) { line('Companies that', 380, h1); line('run on *AI agents.*', 466, h1 + .35); line('Run by *people.*', 600, h1 + d1 * .62); }
    else if (t < h3 - .05) { var o = seg(t, h2 - .1, h2 + .2); ctx.globalAlpha = o; line('One *platform.*', 380, h2); line('A whole *portfolio.*', 470, h2 + d2 * .22); line('Same *clients.*', 560, h2 + d2 * .62); }
    else line('Here’s *how.*', 470, h3, 110);
    ctx.restore();
    k.mono('Arsenal Digital Holdings · OTCID: ADHI', 130, 120, 16, k.hex('#9AA6C3', eo(seg(t, .4, 1.2)) * fadeAll));
    k.stamp('AI-POWERED · HUMAN-LED', 640, 800, t, Q.nb(h2 + d2 + .02), '#E9EEF9', { size: 36, rot: -4, ring: '#9CC8EC', alpha: 1 - seg(t, h3 + .1, h3 + .5), seed: 7, count: 20 });
  }

  // ───────── camera over the world scenes ─────────
  var KEYS = null;
  function buildCamera() {
    var M = ['m1', 'm2', 'm3', 'm4'];
    KEYS = [[0, POS.acc[0], 40, 1.18, 0]];
    KEYS.push([Q.S('acc'), POS.acc[0], 40, 1.0, 1.4]);
    [['fam', POS.fam], ['ins', POS.ins], ['loan', POS.loan]].forEach(function (s) { KEYS.push([Q.S(s[0]) - .55, s[1][0], 40, 1.0, .9]); });
    KEYS.push([Q.S('energy') - .55, POS.energy[0] - 120, 20, .98, .9]);
    KEYS.push([Q.S('energy') + .4, POS.energy[0] + 160, 20, .98, Q.S('mont') - Q.S('energy') - 1.2]);
    M.forEach(function (m, i) { KEYS.push([Q.V(m) - .5, POS['m' + i][0], 40, 1.0, .5]); });
    var mid = (POS.acc[0] + POS.m3[0]) / 2;
    KEYS.push([Q.S('reveal') + .2, mid, 240, .094, Math.max(1.6, Q.V('r1') + 1 - Q.S('reveal'))]);
    KEYS.push([Q.V('r2'), mid, 300, .1, 4]);
    KEYS.forEach(function (kf, i) { if (i > 1) ev('whoosh', kf[0]); });
  }
  function camAt(t) {
    var cur = KEYS[0], prev = KEYS[0];
    for (var i = 1; i < KEYS.length; i++) { if (t >= KEYS[i][0]) { prev = KEYS[i - 1]; cur = KEYS[i]; } }
    if (cur === KEYS[0]) return { x: cur[1], y: cur[2], z: cur[3] };
    // value we were at when this move started (the previous move may not have finished)
    var from = camAtRaw(cur[0], KEYS.indexOf(cur) - 1), u = eio(seg(t, cur[0], cur[0] + cur[4]));
    var z = Math.exp(lerp(Math.log(from.z), Math.log(cur[3]), u));
    return { x: lerp(from.x, cur[1], u), y: lerp(from.y, cur[2], u), z: z };
  }
  function camAtRaw(t, idx) {
    if (idx <= 0) return { x: KEYS[0][1], y: KEYS[0][2], z: KEYS[0][3] };
    var cur = KEYS[idx], from = camAtRaw(cur[0], idx - 1), u = eio(seg(t, cur[0], cur[0] + cur[4]));
    return { x: lerp(from.x, cur[1], u), y: lerp(from.y, cur[2], u), z: Math.exp(lerp(Math.log(from.z), Math.log(cur[3]), u)) };
  }

  function lightBg(cam) {
    ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
    var step = 120; while (step * cam.z < 60) step *= 4;
    ctx.strokeStyle = 'rgba(11,18,38,.045)'; ctx.lineWidth = 1;
    var sx = ((-cam.x * cam.z + W / 2) % (step * cam.z) + step * cam.z) % (step * cam.z), sy = ((-cam.y * cam.z + H / 2) % (step * cam.z) + step * cam.z) % (step * cam.z);
    ctx.beginPath(); for (var x = sx; x < W; x += step * cam.z) { ctx.moveTo(x, 0); ctx.lineTo(x, H); } for (var y = sy; y < H; y += step * cam.z) { ctx.moveTo(0, y); ctx.lineTo(W, y); } ctx.stroke();
    k.glow(W * .2, H * .15, 700, '#9CC8EC', .22); k.glow(W * .85, H * .85, 760, '#C9B8FA', .14);
  }

  // the platform slab revealed under every scene
  function slab(t) {
    var r1 = Q.V('r1'), r2 = Q.V('r2'), u = eo(seg(t, r1 + .2, r1 + 1.4)); if (u <= 0) return;
    var x0 = POS.acc[0] - 1000, x1 = POS.m3[0] + 900, y0 = 560;
    ctx.save(); ctx.globalAlpha = u;
    k.rr(x0, y0, x1 - x0, 1500, 220); ctx.fillStyle = 'rgba(52,72,154,.10)'; ctx.fill(); ctx.strokeStyle = k.hex(C.navy, .5); ctx.lineWidth = 24; ctx.stroke();
    var L = ['Models', 'Data', 'Agents', 'Tools'];
    L.forEach(function (l, i) { var lk = eo(seg(t, r2 + i * .35, r2 + .4 + i * .35)), lx = x0 + 600 + i * 4200; k.rr(lx, y0 + 380, 3600, 700, 140); ctx.fillStyle = k.hex(C.navy, .12 + .5 * lk); ctx.fill(); k.text(l, lx + 1800, y0 + 860, 330, '800', lk > .5 ? '#fff' : C.navy, { align: 'center', stretch: 'semi-expanded' }); if (lk > 0 && lk < .2) ev('pop', r2 + i * .35); });
    k.text('ONE SHARED AI PLATFORM', (x0 + x1) / 2, y0 + 250, 220, '800', C.navy, { align: 'center', fam: k.M });
    // threads between the companies
    var keys = ['acc', 'fam', 'ins', 'loan', 'energy', 'm0', 'm1', 'm2', 'm3'];
    ctx.strokeStyle = k.hex(C.navy, .7); ctx.lineWidth = 26; ctx.setLineDash([60, 60]); ctx.lineDashOffset = -t * 600;
    for (var i = 1; i < keys.length; i++) { var a = POS[keys[i - 1]], b = POS[keys[i]], lk = seg(t, r1 + .6 + i * .12, r1 + 1 + i * .12); if (lk > 0) k.partial([[a[0] + 700, 0], [b[0] - 700, 0]], lk); }
    ctx.setLineDash([]); ctx.restore();
  }

  // ───────── the flywheel ─────────
  var SLOTS = 9;
  function ringKeys() {
    var wh = Q.S('wheel'), en = Q.S('engine'), g2 = Q.V('g2a'), g3 = Q.V('g3'), pr = Q.S('proof'), ct = Q.S('cta');
    return [[wh, 1060, 560, 1, 1], [en + .1, 960, 370, .55, 1], [g2 - .5, 960, 370, .55, .2], [g3 - .4, 650, 540, .78, 1], [pr - .2, 650, 540, .78, 0], [ct + .2, 1390, 500, .5, 1], [Q.V('c3') - .3, 1390, 500, .5, 0]];
  }
  function ringState(t) {
    var K2 = ringKeys(), cur = K2[0], prev = K2[0];
    for (var i = 1; i < K2.length; i++) if (t >= K2[i][0]) { prev = K2[i - 1]; cur = K2[i]; }
    if (cur === K2[0]) return { x: cur[1], y: cur[2], s: cur[3], a: cur[4] };
    var u = eio(seg(t, cur[0], cur[0] + .8));
    return { x: lerp(prev[1], cur[1], u), y: lerp(prev[2], cur[2], u), s: lerp(prev[3], cur[3], u), a: lerp(prev[4], cur[4], u) };
  }
  function ring(t) {
    var wh = Q.S('wheel'); if (t < wh - .2 || t > Q.V('c3') + .6) return;
    var st = ringState(t), appear = eo(seg(t, wh - .1, wh + .6)); if (st.a * appear <= .01) return;
    var r3 = Q.V('r3'), r4 = Q.V('r4'), g3 = Q.V('g3'), d3 = Q.D('g3'), c1 = Q.V('c1');
    var fired = 0, lineT = COMPANIES.map(function (_, i) { return Q.nb(r3 + .9 + i * Q.beat); });
    var healthT = Q.nb(r4 + Q.D('r4') + .2), newT = g3 + d3 + .1, ownT = c1 + Q.D('c1') * .55;
    ctx.save(); ctx.globalAlpha = st.a * appear; ctx.translate(st.x, st.y); ctx.scale(st.s, st.s);
    var RAD = 360, burst = seg(t, r4, r4 + 1.2);
    if (burst > 0 && burst < 1) { for (var b = 0; b < 24; b++) { var an = b / 24 * 6.283; ctx.strokeStyle = k.hex(C.navy, (1 - burst) * .35); ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(Math.cos(an) * 120, Math.sin(an) * 120); ctx.lineTo(Math.cos(an) * (140 + burst * 520), Math.sin(an) * (140 + burst * 520)); ctx.stroke(); } }
    ctx.strokeStyle = k.hex(C.navy, .18); ctx.lineWidth = 2; ctx.setLineDash([6, 12]); ctx.beginPath(); ctx.arc(0, 0, RAD, 0, 6.283); ctx.stroke(); ctx.setLineDash([]);
    for (var s = 0; s < SLOTS; s++) {
      var an = -Math.PI / 2 + s / SLOTS * 6.283, x = Math.cos(an) * RAD, y = Math.sin(an) * RAD;
      var kind = s < 7 ? 'co' : s === 7 ? 'health' : 'new', on = kind === 'co' ? t >= lineT[s] : kind === 'health' ? t >= healthT : t >= newT;
      var pop = eo(seg(t, wh + s * .06, wh + .5 + s * .06));
      if (kind === 'co' && t >= lineT[s]) { fired++; var lk = seg(t, lineT[s], lineT[s] + .35); ctx.strokeStyle = k.hex(C.navy, .8); ctx.lineWidth = 4; k.partial([[0, 0], [x * .5 + Math.cos(an + .6) * 90, y * .5 + Math.sin(an + .6) * 90], [x, y]], lk); if (lk < 1) { var q = lk; k.star(lerp(0, x, q), lerp(0, y, q), 5, C.navy, 1); } ev('pop', lineT[s]); }
      ctx.save(); ctx.translate(x, y); ctx.scale(pop, pop);
      if (kind === 'co') { tile(COMPANIES[s], on ? C.navy : C.muted, on, t >= r4 ? 1 + .08 * Math.sin(Math.min(1, (t - r4) * 3) * Math.PI) : 1); }
      else if (kind === 'health') { if (t < healthT) emptySlot(); else { var hk = back(seg(t, healthT, healthT + .5)); ctx.scale(hk, hk); tile('Health & insurance · next', C.tip, true, 1, true); ev('hit', healthT); } }
      else { if (t < newT) emptySlot(); else { var nk = back(seg(t, newT, newT + .5)); ctx.scale(nk, nk); tile(t >= ownT ? 'Your business' : 'Next business', C.green, true, 1, true); } }
      ctx.restore();
    }
    // centre: one relationship
    ctx.beginPath(); ctx.arc(0, 0, 112, 0, 6.283); ctx.fillStyle = '#fff'; ctx.shadowColor = 'rgba(11,18,38,.18)'; ctx.shadowBlur = 40; ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.strokeStyle = k.hex(C.navy, .3); ctx.lineWidth = 3; ctx.stroke();
    window.SCN.person(0, -6, .3, C.navy);
    k.text('Accountant', 0, 58, 24, '800', C.ink, { align: 'center' }); k.mono('1 relationship', 0, 84, 13, C.navy, { align: 'center' });
    ctx.restore();
    // the counter (only while the wheel owns the screen)
    var ca = st.a * appear * (1 - seg(t, Q.S('engine') - .2, Q.S('engine') + .3));
    if (ca > 0) { ctx.save(); ctx.globalAlpha = ca; k.mono('Revenue lines', 150, 410, 18, C.navy); var big = 1 + .25 * Math.max(0, 1 - Math.abs(t - r4) * 3);
      ctx.save(); ctx.translate(150, 600); ctx.scale(big, big); k.text(String(Math.max(1, fired)), 0, 0, 230, '850', C.navy, { stretch: 'expanded' }); ctx.restore();
      k.mono('From one relationship', 150, 660, 18, C.muted); ctx.restore(); }
  }
  function tile(name, color, on, sc, filled) {
    ctx.save(); ctx.scale(sc || 1, sc || 1); var w = Math.max(230, k.width(name, 21, '800') + 90), h = 88;
    ctx.shadowColor = 'rgba(11,18,38,.16)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 10; k.rr(-w / 2, -h / 2, w, h, 26); ctx.fillStyle = filled ? color : '#fff'; ctx.fill(); ctx.shadowColor = 'transparent';
    if (!filled) { ctx.strokeStyle = on ? color : C.line; ctx.lineWidth = on ? 3 : 1.5; ctx.stroke(); }
    var ic = filled ? '#fff' : color; ctx.fillStyle = ic; ctx.beginPath(); ctx.moveTo(-w / 2 + 34, -12); ctx.lineTo(-w / 2 + 48, 12); ctx.lineTo(-w / 2 + 20, 12); ctx.closePath(); ctx.fill();
    k.text(name, -w / 2 + 64, 8, 21, '800', filled ? '#fff' : (on ? C.ink : C.muted)); ctx.restore();
  }
  function emptySlot() { ctx.strokeStyle = k.hex(C.navy, .35); ctx.lineWidth = 2.5; ctx.setLineDash([8, 8]); k.rr(-115, -44, 230, 88, 26); ctx.stroke(); ctx.setLineDash([]); k.text('+', 0, 14, 40, '500', k.hex(C.navy, .5), { align: 'center' }); }

  // ───────── the engine ─────────
  var MOVES = [['Build', 'Spin up AI-native companies on the platform'], ['Embed', 'Install agentic AI into the operation'], ['Scale', 'Grow and cross-sell across the portfolio'], ['Compound', 'Audit, governance and a public listing turn growth into acquisition currency']];
  function engine(t) {
    var e0 = Q.S('engine'), g1 = Q.V('g1'), g2 = Q.V('g2a'), g3 = Q.V('g3'), d3 = Q.D('g3'), pr = Q.S('proof');
    if (t < e0 - .2 || t > pr + .5) return;
    // foundation and cash flow
    var fa = eo(seg(t, e0 + .2, e0 + .9)) * (1 - seg(t, g2 - .6, g2 - .1));
    if (fa > 0) {
      ctx.save(); ctx.globalAlpha = fa;
      k.card(460, 650, 1000, 84, 30, { fill: C.navy, stroke: false }); k.text('SHARED AI PLATFORM', 960, 704, 26, '800', '#fff', { align: 'center', fam: k.M });
      [['Energy', 460], ['Finance', 1020]].forEach(function (f) { k.card(f[1], 820, 440, 130, 28); k.text(f[0], f[1] + 40, 880, 36, '800', C.ink, { stretch: 'semi-expanded' }); ctx.beginPath(); ctx.arc(f[1] + 48, 916, 7, 0, 6.283); ctx.fillStyle = C.green; ctx.fill(); k.mono('Operating today · cash flow', f[1] + 64, 922, 14, C.green); });
      if (t > g1) for (var i = 0; i < 26; i++) { var ph = ((t - g1) * .55 + i / 26) % 1, side = i % 2, x = (side ? 1240 : 680) + Math.sin(i * 7.3) * 120 + (960 - (side ? 1240 : 680)) * eio(ph), y = lerp(810, 380, ph), a = Math.sin(ph * Math.PI) * seg(t, g1, g1 + .5);
        ctx.save(); ctx.globalAlpha *= a; k.rr(x - 20, y - 14, 40, 28, 8); ctx.fillStyle = C.green; ctx.fill(); k.text('$', x, y + 8, 20, '800', '#fff', { align: 'center' }); ctx.restore(); }
      ctx.restore();
    }
    // the four moves
    var ma = eo(seg(t, g2 - .4, g2)) * (1 - seg(t, g3 - .4, g3 + .1));
    if (ma > 0) {
      ctx.save(); ctx.globalAlpha = ma;
      ['g2a', 'g2b', 'g2c', 'g2d'].forEach(function (key, i) {
        var t0 = Q.V(key) - .05; if (t < t0) return; var u = seg(t, t0, t0 + .32), x = 110 + i * 435, y = 330; ev('hit', t0);
        ctx.save(); ctx.translate(x + 200, y + 190); var sc = lerp(1.35, 1, back(u)); ctx.scale(sc, sc); ctx.globalAlpha *= Math.min(1, u * 3);
        k.card(-200, -190, 400, 380, 30, { fill: i === 3 ? C.navy : '#fff' });
        k.mono('0' + (i + 1), -160, -130, 18, i === 3 ? '#C9D4F5' : C.navy);
        k.text(MOVES[i][0], -160, -40, 64, '850', i === 3 ? '#fff' : C.ink, { stretch: 'semi-expanded' });
        wrap(MOVES[i][1], -160, 30, 300, 22, i === 3 ? '#DCE3FA' : C.muted);
        ctx.restore();
      });
      ctx.restore();
    }
    // the public-company chassis turns growth into the next acquisition
    var ta = eo(seg(t, g3 - .3, g3 + .3)) * (1 - seg(t, pr - .3, pr + .2));
    if (ta > 0) {
      ctx.save(); ctx.globalAlpha = ta; ctx.translate((1 - eo(seg(t, g3 - .3, g3 + .4))) * 300, 0);
      var x = 1180, y = 250; k.card(x, y, 520, 560, 34);
      k.mono('OTCID', x + 40, y + 56, 16); k.mono('Public-company chassis', x + 480, y + 56, 16, C.muted, { align: 'right' });
      k.text('ADHI', x + 260, y + 190, 128, '850', C.brand, { align: 'center', stretch: 'expanded' });
      ctx.strokeStyle = C.line; ctx.lineWidth = 3; ctx.setLineDash([10, 10]); ctx.beginPath(); ctx.moveTo(x + 40, y + 236); ctx.lineTo(x + 480, y + 236); ctx.stroke(); ctx.setLineDash([]);
      ['Audit', 'Governance', 'Public listing'].forEach(function (s, i) { var t0 = g3 + d3 * (.12 + i * .14); if (t < t0) return; var u = seg(t, t0, t0 + .35); ev('pop', t0); k.check(x + 64, y + 300 + i * 70, 18, C.navy, 1, u); k.text(s, x + 100, y + 309 + i * 70, 30, '700', C.ink); });
      var bt = g3 + d3 * .62; if (t > bt && t < g3 + d3 + .15) { var u = eio(seg(t, bt, g3 + d3 + .1)), sx = x + 260, sy = y + 520, rs = ringState(t), an = -Math.PI / 2 + 8 / SLOTS * 6.283, ex = rs.x + Math.cos(an) * 360 * rs.s, ey = rs.y + Math.sin(an) * 360 * rs.s;
        ctx.save(); ctx.translate(lerp(sx, ex, u), lerp(sy, ey, u) - Math.sin(u * Math.PI) * 160); ctx.scale(rs.s, rs.s); tile('Next business', C.green, true, 1, true); ctx.restore(); }
      ctx.restore();
    }
  }
  function wrap(str, x, y, maxW, size, color) { var words = str.split(' '), line = '', yy = y; words.forEach(function (w) { var test = line ? line + ' ' + w : w; if (k.width(test, size, '500') > maxW) { k.text(line, x, yy, size, '500', color); line = w; yy += size * 1.4; } else line = test; }); if (line) k.text(line, x, yy, size, '500', color); }

  // ───────── proof ─────────
  function proof(t) {
    var p0 = Q.S('proof'), ct = Q.S('cta'); if (t < p0 - .3 || t > ct + .3) return;
    var a = eo(seg(t, p0 - .3, p0 + .3)) * (1 - seg(t, ct - .3, ct + .1)); ctx.save(); ctx.globalAlpha = a;
    var strike = Q.nb(p0 + .6), sel = Q.nb(p0 + 1.5);
    k.card(240, 260, 640, 330, 34); k.mono('Option A', 290, 320, 16); k.text('AI in operations only', 290, 400, 44, '800', C.ink, { stretch: 'semi-expanded' }); k.text('Back-office efficiency', 290, 450, 24, '500', C.muted);
    if (t > strike) { ctx.strokeStyle = C.red; ctx.lineWidth = 8; ctx.lineCap = 'round'; k.partial([[280, 392], [860, 372]], seg(t, strike, strike + .3)); ctx.lineCap = 'butt'; ev('whoosh', strike); }
    k.card(1040, 260, 640, 330, 34, { stroke: t > sel ? C.green : C.line, lw: t > sel ? 4 : 1.5 }); k.mono('Option B', 1090, 320, 16); k.text('AI in what you sell', 1090, 400, 44, '800', C.ink, { stretch: 'semi-expanded' }); k.text('Transformation of the offering', 1090, 450, 24, '500', C.muted);
    k.stamp('SELECTED', 1500, 560, t, sel, C.green, { size: 40, seed: 51, ring: C.green, fill: 'rgba(255,255,255,.95)' });
    if (t > sel) { k.text('+' + k.countTo(43, t, sel, sel + 1.4) + '%', 960, 800, 170, '850', C.navy, { align: 'center', stretch: 'expanded' });
      k.text('higher median revenue multiple', 960, 860, 28, '600', C.ink, { align: 'center' });
      k.mono('McKinsey & Company · 471 PE-backed companies', 960, 910, 16, C.muted, { align: 'center' });
      k.text('Third-party finding; a correlation, not a guarantee, and not a projection of Arsenal’s results.', 960, 960, 17, '500', '#8A93AC', { align: 'center' }); }
    ctx.restore();
  }

  // ───────── call to action ─────────
  function cta(t) {
    var c0 = Q.S('cta'), c1 = Q.V('c1'), c2 = Q.V('c2'), d2 = Q.D('c2'), c3 = Q.V('c3'), end = Q.S('end'); if (t < c0 - .3 || t > end + .6) return;
    var a = eo(seg(t, c0 - .2, c0 + .4)) * (1 - seg(t, c3 - .4, c3));
    if (a > 0) {
      ctx.save(); ctx.globalAlpha = a; ctx.translate((1 - a) * -60, 0);
      var x = 260, y = 250; k.card(x, y, 640, 470, 34);
      k.mono('Owner-led company', x + 44, y + 60, 16); k.text('Your business', x + 44, y + 130, 56, '850', C.ink, { stretch: 'semi-expanded' });
      ['Your team stays', 'Your name stays', 'Your upside grows'].forEach(function (s, i) { var t0 = c2 + d2 * (.02 + i * .32); var on = t >= t0; if (on) ev('pop', t0); k.check(x + 70, y + 210 + i * 76, 20, on ? C.green : '#D6DCE9', 1, on ? seg(t, t0, t0 + .35) : 1); k.text(s, x + 110, y + 220 + i * 76, 32, '700', on ? C.ink : '#A5ADC2'); });
      // plug into the system
      var pt = c1 + Q.D('c1') * .5, pk = eo(seg(t, pt, pt + .4)), rs = ringState(t), an = -Math.PI / 2 + 8 / SLOTS * 6.283, ex = rs.x + Math.cos(an) * 360 * rs.s - 70, ey = rs.y + Math.sin(an) * 360 * rs.s;
      ctx.fillStyle = C.ink; k.rr(x + 630, y + 210, 40, 50, 10); ctx.fill(); ctx.fillRect(x + 668, y + 222, 18, 8); ctx.fillRect(x + 668, y + 240, 18, 8);
      if (pk > 0) { ctx.strokeStyle = C.green; ctx.lineWidth = 6; ctx.lineCap = 'round'; k.partial([[x + 690, y + 235], [x + 840, y + 235], [ex - 120, ey], [ex, ey]], pk); ctx.lineCap = 'butt'; if (pk >= 1) k.glow(ex, ey, 120, C.green, .35 * (1 - seg(t, pt + .4, pt + 1.2))); ev('click', pt + .4); }
      // deal structures
      ['Full acquisition', 'Majority + earnout', 'Partnership / JV'].forEach(function (s, i) { var t0 = c2 + d2 + .15 + i * .18, u = eo(seg(t, t0, t0 + .4)); if (u <= 0) return; ctx.save(); ctx.globalAlpha *= u; var w = 420, xx = 300 + i * 450, yy = 820 + (1 - u) * 40; k.card(xx, yy, w, 96, 28, { fill: i === 1 ? C.navy : '#fff' }); k.text(s, xx + w / 2, yy + 60, 28, '800', i === 1 ? '#fff' : C.ink, { align: 'center' }); ctx.restore(); });
      ctx.restore();
    }
    // investors
    var ia = eo(seg(t, c3 - .2, c3 + .3)) * (1 - seg(t, end - .3, end)); if (ia > 0) {
      ctx.save(); ctx.globalAlpha = ia; ctx.translate(0, (1 - ia) * 40);
      k.card(560, 250, 800, 560, 40); k.mono('Investors · OTCID', 960, 340, 20, C.navy, { align: 'center' });
      k.text('ADHI', 960, 560, 230, '850', C.brand, { align: 'center', stretch: 'expanded' });
      k.text('Investor relations at arsenalholdingscorp.com', 960, 680, 28, '600', C.muted, { align: 'center' });
      ctx.restore(); ev('hit', c3);
    }
  }

  // ───────── end card ─────────
  function endCard(t) {
    var e0 = Q.S('end'), d4 = Q.D('c4'); if (t < e0 - .1) return;
    var iris = eio(seg(t, e0 - .1, e0 + .6)), r = iris * 1300;
    ctx.save(); ctx.beginPath(); ctx.arc(960, 540, Math.max(1, r), 0, 6.283); ctx.clip();
    sky(t, 1);
    var cA = eo(seg(t, e0 + .2, e0 + 1.4));
    crystal(960, 120, 380, { facets: cA * .9, edges: eio(seg(t, e0, e0 + 1.4)), sweep: ((t - e0 - 1.2) % 4) / 1.6 - .3 });
    k.glow(960, 300, 420, '#6E8FD6', .2 * cA);
    var l1 = eo(seg(t, e0 + .3, e0 + .8)), l2 = eo(seg(t, e0 + d4 * .55, e0 + d4 * .55 + .45));
    ctx.save(); ctx.globalAlpha = l1; rich('We don’t back the future.', 960, 640 + (1 - l1) * 20, 80, '#F2F5FC', '#9CC8EC', 'center', '800'); ctx.restore();
    ctx.save(); ctx.globalAlpha = l2; rich('We *build it.*', 960, 740 + (1 - l2) * 20, 80, '#F2F5FC', '#9CC8EC', 'center', '800'); ctx.restore();
    var bt = Q.nb(e0 + d4 + .1), bk = back(seg(t, bt, bt + .45));
    if (t > bt) { ctx.save(); ctx.translate(960, 850); ctx.scale(bk, bk); var bw = 640; k.rr(-bw / 2, -40, bw, 80, 40); ctx.fillStyle = '#E9EEF9'; ctx.fill(); k.text('Start a confidential conversation  →', 0, 10, 28, '800', C.ink, { align: 'center' }); ctx.restore(); k.confetti(960, 850, t, bt + .1, 61, 60); ev('hit', bt); }
    var ua = eo(seg(t, bt + .4, bt + 1)); k.mono('arsenalholdingscorp.com · OTCID: ADHI', 960, 950, 20, k.hex('#9CC8EC', ua), { align: 'center' });
    k.text('Product scenes are illustrative; several products are in development. Contains forward-looking statements; actual results may differ. Not an offer to sell or a solicitation to buy securities.', 960, 1040, 15, '400', k.hex('#9AA6C3', ua * .85), { align: 'center' });
    ctx.restore();
    if (iris < 1) { ctx.strokeStyle = 'rgba(156,200,236,' + (1 - iris) + ')'; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(960, 540, r, 0, 6.283); ctx.stroke(); }
  }

  // ───────── headline pill and journey rail ─────────
  var HEADS = [['a1', 'Month-end, *closed*'], ['a3', 'Agents work. People *sign*.'], ['f1', 'One *question*'], ['f2', 'One *answer*'], ['i1', 'Insurance, *serviced*'], ['l1', 'Capital to *grow*'], ['l2', 'Weeks → *days*'], ['e1', 'Energy, *optimized*'], ['m1', 'Digital *twins*'], ['m2', 'AI *implementation*'], ['m3', 'AI-native *publishing*'], ['m4', 'Agents & *robots*'], ['r1', 'One *system*'], ['r2', 'One shared *platform*'], ['r3', 'One relationship, *many lines*'], ['g1', 'Funded by *cash flow*'], ['g2a', 'Four *moves*'], ['g3', 'Growth *compounds*'], ['@proof', 'AI *in* the offering'], ['c1', 'Plug *in*'], ['c2', 'Your business, *amplified*'], ['c3', 'For *investors*']];
  function headline(t) {
    if (t < Q.S('acc') + .2 || t > Q.S('end')) return;
    var FIRST = { a1: 'acc', f1: 'fam', i1: 'ins', l1: 'loan', e1: 'energy', r1: 'reveal', g1: 'engine', c1: 'cta' };   // a new scene's headline arrives with its camera move
    var list = HEADS.map(function (h) { var key = h[0]; return [key[0] === '@' ? Q.S(key.slice(1)) : FIRST[key] ? Math.min(Q.V(key) - .15, Q.S(FIRST[key]) - .45) : Q.V(key) - .15, h[1]]; });
    var cur = -1; for (var i = 0; i < list.length; i++) if (t >= list[i][0]) cur = i; if (cur < 0) return;
    var u = eo(seg(t, list[cur][0], list[cur][0] + .35)), out = 1 - seg(t, Q.S('end') - .3, Q.S('end'));
    var str = list[cur][1], w = k.width(str.replace(/\*/g, ''), 40, '700') + 90;
    ctx.save(); ctx.globalAlpha = out; ctx.translate(960, 86); ctx.scale(lerp(.92, 1, u), lerp(.92, 1, u));
    ctx.shadowColor = 'rgba(11,18,38,.12)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 8; k.rr(-w / 2, -40, w, 80, 40); ctx.fillStyle = 'rgba(255,255,255,.96)'; ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.globalAlpha = out * u; rich(str, 0, 14 + (1 - u) * 10, 40, C.ink, C.navy, 'center', '700');
    ctx.restore();
  }
  var CHAPTERS = [['acc', 'Accounting'], ['fam', 'Wealth'], ['ins', 'Insurance'], ['loan', 'Finance'], ['energy', 'Energy'], ['mont', 'More'], ['reveal', 'One system'], ['engine', 'Engine'], ['cta', 'Partner']];
  function rail(t) {
    if (t < Q.S('acc') + .3 || t > Q.S('end')) return;
    var a = eo(seg(t, Q.S('acc') + .3, Q.S('acc') + .9)) * (1 - seg(t, Q.S('end') - .3, Q.S('end')));
    var cur = 0; CHAPTERS.forEach(function (c, i) { if (t >= Q.S(c[0]) - .3) cur = i; });
    var widths = CHAPTERS.map(function (c) { return k.width(c[1].toUpperCase(), 13, '600', { fam: k.M, track: 1.5 }) + 46; }), total = widths.reduce(function (s, v) { return s + v; }, 0) + 40;
    ctx.save(); ctx.globalAlpha = a; var x = 960 - total / 2, y = 1022;
    k.rr(x, y - 26, total, 52, 26); ctx.fillStyle = 'rgba(255,255,255,.82)'; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 1; ctx.stroke();
    x += 20; CHAPTERS.forEach(function (c, i) { var on = i === cur, past = i < cur; ctx.beginPath(); ctx.arc(x + 14, y, on ? 7 : 5, 0, 6.283); ctx.fillStyle = on || past ? C.navy : '#C5CDE0'; ctx.fill(); k.mono(c[1], x + 28, y + 5, 13, on ? C.ink : past ? C.navy : '#A0A9C0'); x += widths[i]; });
    ctx.restore();
  }

  // ───────── frame ─────────
  function renderAt(t) {
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
    var acc = Q.S('acc');
    // beat pulse on bar downbeats in the energetic parts
    var pulse = 1; if (Q.hi(t) && t > acc) { var lb = Q.lastBar(t); pulse = 1 + .01 * Math.exp(-(t - lb) / .16); }
    ctx.save(); ctx.translate(960, 540); ctx.scale(pulse, pulse); ctx.translate(-960, -540);
    if (t >= acc + .12) {
      var cam = camAt(t), drift = 1 + .025 * ((t - acc) % 1000 ? 0 : 0);
      lightBg(cam);
      var wa = 1 - seg(t, Q.S('wheel') - .3, Q.S('wheel') + .4);
      if (wa > 0) {
        ctx.save(); ctx.globalAlpha = wa; ctx.translate(W / 2, H / 2 + 20); ctx.scale(cam.z * drift, cam.z * drift); ctx.translate(-cam.x, -cam.y);
        slab(t); window.WORLD_SCENES.forEach(function (fn) { fn(t, Q); });
        ctx.restore();
      }
      ring(t); engine(t); proof(t); cta(t);
      headline(t); rail(t);
    }
    // the flash: a white burst blooms out of the A, then clears to reveal the workspace
    if (t < acc + .12) {
      hook(t);
      var fr = eio(seg(t, acc - .32, acc + .12)) * 1400; if (fr > 0) { k.glow(1260, 520, fr + 260, '#FFFFFF', 1); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(1260, 520, fr, 0, 6.283); ctx.fill(); }
    } else if (t < acc + .6) { ctx.fillStyle = 'rgba(255,255,255,' + (1 - eo(seg(t, acc + .12, acc + .6))) + ')'; ctx.fillRect(0, 0, W, H); }
    ctx.restore();
    endCard(t);
    var dur = Q.c.dur; if (t > dur - .8) { ctx.fillStyle = 'rgba(3,5,11,' + seg(t, dur - .8, dur) + ')'; ctx.fillRect(0, 0, W, H); }
  }

  window.storyReady = fetch('cues-' + version + '.json').then(function (r) { return r.json(); }).then(function (c) {
    Q = makeQ(c); buildCamera();
    ev('riser', Q.S('acc') - 2.4); ev('boom', Q.S('acc')); ev('riser', Q.S('end') - 1.6); ev('whoosh', Q.S('wheel') - .3); ev('whoosh', Q.S('engine')); ev('whoosh', Q.S('proof')); ev('whoosh', Q.S('cta')); ev('whoosh', Q.V('c3') - .3);
    window.DURATION = c.dur; window.renderAt = renderAt;
    return document.fonts.ready.then(function () { return Promise.all(['800 40px Archivo', 'italic 700 40px Archivo', '600 16px "JetBrains Mono"'].map(function (f) { return document.fonts.load(f); })); });
  });
  if (!/render/.test(location.search)) window.storyReady.then(function () { var t0 = performance.now(); (function loop(n) { renderAt(((n - t0) / 1000) % window.DURATION); requestAnimationFrame(loop); })(t0); });
})();
