/* The scenes of the Arsenal demo. Each draw function receives the time t and the cue sheet Q.
   World scenes (the five product demos and the montage) are drawn around a centre point and
   filmed by a moving camera; the later scenes are drawn straight to the screen. */
(function () {
  'use strict';
  var k = window.K, ctx = k.ctx, C = k.C, seg = k.seg, eo = k.eo, eio = k.eio, back = k.back, lerp = k.lerp, clamp = k.clamp;
  var EVENTS = window.SFX_EVENTS = {};
  function ev(type, time) { EVENTS[type + '@' + time.toFixed(3)] = { type: type, time: +time.toFixed(3) }; }
  var stamp0 = k.stamp; k.stamp = function (label, x, y, t, t0, color, o) { if (t >= t0 - 1) ev('hit', t0); stamp0(label, x, y, t, t0, color, o); };

  // ───────── world layout ─────────
  var POS = { acc: [0, 0], fam: [2600, 0], ins: [5200, 0], loan: [7800, 0], energy: [10400, 0], m0: [13100, 0], m1: [14700, 0], m2: [16300, 0], m3: [17900, 0] };
  window.POS = POS;

  function label(s, x, y, a) {   // product name chip under each demo
    var w = k.width(s.toUpperCase(), 17, '600', { fam: k.M, track: 2 }) + 44;
    ctx.save(); ctx.globalAlpha *= a; k.rr(x - w / 2, y - 22, w, 44, 22); ctx.fillStyle = C.ink; ctx.fill();
    k.mono(s, x, y + 6, 17, '#fff', { align: 'center', track: 2 }); ctx.restore();
  }
  function enter(t, t0) { return eo(seg(t, t0, t0 + .7)); }

  // ───────── 1 · accounting firm ─────────
  var TASKS = ['Bank reconciliations · 6 accounts', 'Vendor invoices matched', 'AP accruals posted', 'Fixed-asset depreciation', 'Draft financial statements', 'Partner review & sign-off'];
  function accounting(t, Q) {
    var s0 = Q.S('acc'); if (t < s0 - .2) return;
    var p = POS.acc, x = p[0] - 640, y = p[1] - 320, w = 1280, h = 650, e = enter(t, s0 - .1);
    ctx.save(); ctx.globalAlpha = e; ctx.translate(0, (1 - e) * 60);
    k.card(x, y, w, h, 34);
    k.text('Month-end close', x + 48, y + 74, 38, '800', C.ink, { stretch: 'semi-expanded' });
    k.text('March · Hollis & Grant CPAs', x + 48, y + 108, 20, '500', C.muted);
    var a2 = Q.V('a2'), d2 = Q.D('a2'), a3 = Q.V('a3');
    var ticks = [0, 1, 2, 3, 4].map(function (i) { return Q.nb(a2 + .2 + i * (d2 - .2) / 5); });
    var signT = a3 + .95, sealT = Q.nb(a3 + Q.D('a3') + .15);
    var done = ticks.filter(function (tt) { return t >= tt; }).length + (t >= signT ? 1 : 0);
    // progress
    var pct = Math.round(done / 6 * 100);
    k.mono('Close progress', x + w - 430, y + 64, 15);
    k.rr(x + w - 430, y + 80, 380, 14, 7); ctx.fillStyle = C.soft; ctx.fill();
    var pw = 380 * lerp((done - 1 < 0 ? 0 : done - 1) / 6, done / 6, eo(seg(t, done ? (done === 6 ? signT : ticks[done - 1]) : 0, (done === 6 ? signT : ticks[Math.max(0, done - 1)]) + .3)));
    k.rr(x + w - 430, y + 80, Math.max(14, pw), 14, 7); ctx.fillStyle = done === 6 ? C.green : C.navy; ctx.fill();
    k.text(pct + '%', x + w - 48, y + 70, 30, '800', done === 6 ? C.green : C.navy, { align: 'right' });
    // task rows
    var rowY = function (i) { return y + 150 + i * 76; };
    TASKS.forEach(function (name, i) {
      var ry = rowY(i), isDone = i < 5 ? t >= ticks[i] : t >= signT, tk = i < 5 ? seg(t, ticks[i], ticks[i] + .35) : seg(t, signT, signT + .35);
      k.rr(x + 48, ry, 760, 62, 16); ctx.fillStyle = isDone ? '#F3F8F5' : '#F6F8FC'; ctx.fill(); ctx.strokeStyle = isDone ? '#CBE9DA' : C.line; ctx.lineWidth = 1.5; ctx.stroke();
      if (isDone) k.check(x + 82, ry + 31, 15, C.green, 1, tk); else { ctx.beginPath(); ctx.arc(x + 82, ry + 31, 14, 0, 6.283); ctx.strokeStyle = '#C5CDE0'; ctx.lineWidth = 2.5; ctx.stroke(); }
      k.text(name, x + 112, ry + 39, 21, '600', isDone ? C.muted : C.ink);
      var who = i < 5 ? 'AGENT' : 'PARTNER', ww = k.width(who, 13, '600', { fam: k.M, track: 1.5 }) + 22;
      k.rr(x + 790 - ww, ry + 17, ww, 28, 14); ctx.fillStyle = i < 5 ? C.soft : '#EEF0F4'; ctx.fill();
      k.mono(who, x + 790 - ww / 2, ry + 36, 13, i < 5 ? C.navy : C.ink, { align: 'center' });
    });
    // agents panel
    var ax = x + 850, ay = y + 150;
    k.rr(ax, ay, 382, 450, 22); ctx.fillStyle = '#F6F8FC'; ctx.fill();
    k.mono('Agents at work', ax + 24, ay + 40, 15);
    ['Reconciliation agent', 'Payables agent', 'Reporting agent'].forEach(function (n, i) {
      var yy = ay + 70 + i * 74, act = t > a2 - .3 && t < ticks[4] + .6;
      k.spark(ax + 44, yy + 24, 13, C.navy, 1, act ? t * 2 + i : 0);
      k.text(n, ax + 70, yy + 22, 18, '700', C.ink);
      for (var b = 0; b < 14; b++) { var hh = act ? 6 + 16 * Math.abs(Math.sin(t * 7 + b * .9 + i * 2)) : 4; k.rr(ax + 70 + b * 16, yy + 48 - hh / 2, 9, hh, 4); ctx.fillStyle = k.hex(C.facet, act ? .9 : .35); ctx.fill(); }
    });
    // signature box
    var sx = ax + 24, sy = ay + 300;
    k.rr(sx, sy, 334, 124, 16); ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = C.line; ctx.stroke();
    k.mono('Partner sign-off', sx + 18, sy + 30, 13);
    if (t >= signT) {
      ctx.strokeStyle = C.ink; ctx.lineWidth = 3.5; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      var sig = []; for (var q = 0; q <= 40; q++) { var u = q / 40; sig.push([sx + 40 + u * 250, sy + 86 - Math.sin(u * 14) * 16 * (1 - u * .5) - u * 10]); }
      k.partial(sig, seg(t, signT, signT + .6)); ctx.lineCap = 'butt';
    } else { ctx.strokeStyle = '#C5CDE0'; ctx.setLineDash([6, 8]); ctx.beginPath(); ctx.moveTo(sx + 30, sy + 96); ctx.lineTo(sx + 304, sy + 96); ctx.stroke(); ctx.setLineDash([]); }
    // agent cursors hop from task to task
    function hop(list, off) {
      var pts = list.map(function (i) { return [ticks[i], x + 640 + off, rowY(i) + 20]; });
      if (t < a2 - .4 || t > ticks[4] + .8) return null;
      var a = k.clamp((t - (a2 - .4)) / .4, 0, 1), cur = [x + 900, y + 700];
      for (var j = 0; j < pts.length; j++) { var prevT = j ? pts[j - 1][0] : a2 - .4, from = j ? [pts[j - 1][1], pts[j - 1][2]] : [x + 980, y + 640]; if (t <= pts[j][0]) { var u = eio(seg(t, prevT, pts[j][0] - .05)); cur = [lerp(from[0], pts[j][1], u), lerp(from[1], pts[j][2], u)]; break; } cur = [pts[j][1], pts[j][2]]; }
      return [cur[0], cur[1], a * (1 - seg(t, ticks[4] + .4, ticks[4] + .8))];
    }
    var c1 = hop([0, 2, 4], 0), c2 = hop([1, 3], 60);
    if (c1) k.cursor(c1[0], c1[1], 'Agent', C.navy, c1[2]);
    if (c2) k.cursor(c2[0], c2[1], 'Agent', C.facet, c2[2]);
    // the partner signs
    if (t > a3 - .1 && t < sealT + 1.4) {
      var u = eio(seg(t, a3 - .1, signT - .05)), px = lerp(x + w + 120, sx + 60, u), py = lerp(y + h + 80, sy + 70, u);
      if (t > signT) { px = sx + 40 + 250 * eo(seg(t, signT, signT + .6)); py = sy + 70; }
      k.cursor(px, py, 'Partner', C.ink, 1 - seg(t, sealT + .8, sealT + 1.3));
      if (t > signT - .05 && t < signT + .5) { ctx.strokeStyle = k.hex(C.ink, .35 * (1 - seg(t, signT, signT + .5))); ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(sx + 40, sy + 70, 10 + 50 * seg(t, signT, signT + .5), 0, 6.283); ctx.stroke(); }
    }
    ev('click', signT);
    k.stamp('CLOSED', x + w - 240, y + h - 70, t, sealT, C.green, { size: 56, seed: 11, ring: C.green, fill: 'rgba(255,255,255,.92)' });
    label('AI for Accountants · software that runs a firm', p[0], y + h + 64, k.eo(seg(t, Q.V('a1'), Q.V('a1') + .6)));
    ctx.restore();
  }

  // ───────── 2 · family office ─────────
  var SOURCES = [['Accounting', '#34489A'], ['Legal', '#8B5CF6'], ['Insurance', '#14915F'], ['Wealth', '#D98A1A']];
  var ANSWER = [['Tax', 'Spread the gain across two tax years'], ['Legal', 'Update the trust before closing'], ['Insurance', 'Re-title the life policy'], ['Wealth', 'A plan for the proceeds, ready']];
  function family(t, Q) {
    var s0 = Q.S('fam'); if (t < s0 - .4) return;
    var p = POS.fam, x = p[0] - 600, y = p[1] - 330, w = 1200, h = 660, e = enter(t, s0 - .3);
    ctx.save(); ctx.globalAlpha = e; ctx.translate(0, (1 - e) * 60);
    k.card(x, y, w, h, 34);
    k.spark(x + 62, y + 60, 16, C.navy, 1, t);
    k.text('Family office assistant', x + 92, y + 70, 30, '800', C.ink, { stretch: 'semi-expanded' });
    k.text('Dana R. · client of Hollis & Grant', x + w - 48, y + 68, 19, '500', C.muted, { align: 'right' });
    var f1 = Q.V('f1'), d1 = Q.D('f1'), f2 = Q.V('f2'), d2 = Q.D('f2');
    // client's question
    var q = 'If I sell my business this year, what happens to my estate?', qk = seg(t, f1 + .9, f1 + d1 - .2);
    if (t > f1 - .2) {
      var bw = 640, bx = x + w - 48 - bw, by = y + 110, bk = eo(seg(t, f1 - .2, f1 + .3));
      ctx.save(); ctx.globalAlpha *= bk; k.rr(bx, by, bw, 104, 24); ctx.fillStyle = C.navy; ctx.fill();
      var q1 = 'If I sell my business this year,', q2 = 'what happens to my estate?';
      k.text(k.typed(q1, qk * 2), bx + 30, by + 44, 23, '600', '#fff');
      k.text(k.typed(q2, qk * 2 - 1), bx + 30, by + 78, 23, '600', '#fff');
      ctx.beginPath(); ctx.arc(bx + bw + 0, by + 104 + 0, 0, 0, 1); ctx.restore();
      ctx.save(); ctx.globalAlpha *= bk; ctx.beginPath(); ctx.arc(x + w - 48 - bw - 40, by + 52, 26, 0, 6.283); ctx.fillStyle = '#F1E6FF'; ctx.fill(); k.text('DR', x + w - 48 - bw - 40, by + 60, 18, '800', C.tip, { align: 'center' }); ctx.restore();
    }
    // four sources fly in and braid together
    var mx = x + 120, my = y + 420;
    SOURCES.forEach(function (sx, i) {
      var t0 = f2 + d2 * (.3 + i * .12), u = eo(seg(t, t0, t0 + .55));
      if (u <= 0) return;
      if (u > 0 && u < .1) ev('pop', t0);
      var fx = [x - 300, x - 260, x + 200, x + 520][i], fy = [y + 150, y + 700, y + 780, y + 790][i];
      var tx = mx + 10, ty = y + 290 + i * 70, cx = lerp(fx, tx, u), cy = lerp(fy, ty, u);
      var ww = k.width(sx[0], 19, '700') + 50;
      k.rr(cx, cy, ww, 46, 23); ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = k.hex(sx[1], .5); ctx.lineWidth = 2; ctx.stroke();
      ctx.beginPath(); ctx.arc(cx + 22, cy + 23, 7, 0, 6.283); ctx.fillStyle = sx[1]; ctx.fill();
      k.text(sx[0], cx + 36, cy + 30, 19, '700', C.ink);
      // braid line to the answer
      var ak = seg(t, t0 + .4, t0 + .9); if (ak > 0) { ctx.strokeStyle = k.hex(sx[1], .7); ctx.lineWidth = 3; k.partial([[tx + ww, ty + 23], [x + 400, ty + 23], [x + 430, y + 470]], ak); }
    });
    // the answer
    var ansT = f2 + d2 * .82;
    if (t > ansT) {
      var ax = x + 430, ay = y + 290, ak = eo(seg(t, ansT, ansT + .4));
      ctx.save(); ctx.globalAlpha *= ak; k.rr(ax, ay, 722, 330, 24); ctx.fillStyle = '#F6F8FC'; ctx.fill(); ctx.strokeStyle = C.line; ctx.stroke();
      k.spark(ax + 36, ay + 40, 13, C.navy, 1, 0); k.mono('One answer · four disciplines', ax + 60, ay + 46, 15, C.navy);
      ANSWER.forEach(function (a, i) {
        var lk = eo(seg(t, ansT + .25 + i * .22, ansT + .6 + i * .22)); ctx.globalAlpha = ak * lk;
        var yy = ay + 100 + i * 58; ctx.beginPath(); ctx.arc(ax + 40, yy - 7, 8, 0, 6.283); ctx.fillStyle = SOURCES[i][1]; ctx.fill();
        k.text(a[0] + ':', ax + 62, yy, 21, '800', C.ink); k.text(a[1], ax + 62 + k.width(a[0] + ': ', 21, '800'), yy, 21, '500', C.ink);
      });
      ctx.restore();
    }
    k.stamp('ONE ANSWER', x + w - 230, y + h - 40, t, Q.nb(f2 + d2 + .1), C.navy, { size: 44, seed: 21, fill: 'rgba(255,255,255,.92)' });
    label('Multi-Family Office Platform', p[0], y + h + 64, eo(seg(t, f1, f1 + .6)));
    ctx.restore();
  }

  // ───────── 3 · insurance policy ─────────
  function insurance(t, Q) {
    var s0 = Q.S('ins'); if (t < s0 - .4) return;
    var p = POS.ins, w = 980, h = 600, x = p[0] - w / 2, y = p[1] - 310;
    var flip = eo(seg(t, s0 - .3, s0 + .45));
    ctx.save(); ctx.translate(p[0], p[1]); ctx.scale(Math.max(.02, flip), 1); ctx.rotate((1 - flip) * -.08); ctx.translate(-p[0], -p[1]);
    k.card(x, y, w, h, 34);
    ctx.save(); k.rr(x, y, w, 128, 34); ctx.clip(); ctx.fillStyle = C.navy; ctx.fillRect(x, y, w, 128); ctx.restore();
    k.mono('Life policy · UL-20418', x + 48, y + 52, 15, '#C9D4F5');
    k.text('Dana R.', x + 48, y + 98, 36, '800', '#fff', { stretch: 'semi-expanded' });
    var i1 = Q.V('i1'), d1 = Q.D('i1'), i2 = Q.V('i2'), d2 = Q.D('i2');
    var auto = t >= i1 + d1 * .55;
    var pill = auto ? 'Serviced automatically' : 'Needs attention', pw = k.width(pill, 18, '700') + 56;
    k.rr(x + w - 48 - pw, y + 44, pw, 42, 21); ctx.fillStyle = auto ? C.green : '#F2B33D'; ctx.fill();
    k.text(pill, x + w - 48 - pw / 2 + 12, y + 72, 18, '700', '#fff', { align: 'center' });
    if (auto) k.check(x + w - 48 - pw + 24, y + 65, 11, 'rgba(255,255,255,.3)', 1, seg(t, i1 + d1 * .55, i1 + d1 * .55 + .3));
    ev('pop', i1 + d1 * .55);
    var rows = [['Premium autopay', i2 + d2 * .08], ['Life-expectancy analysis', i2 + d2 * .33], ['Settlement record', i2 + d2 * .72]];
    rows.forEach(function (r, i) {
      var ry = y + 170 + i * 128, on = t >= r[1], u = seg(t, r[1], r[1] + .5);
      k.rr(x + 48, ry, w - 96, 108, 20); ctx.fillStyle = '#F6F8FC'; ctx.fill();
      k.text(r[0], x + 84, ry + 64, 26, '700', C.ink);
      if (i === 0) { // toggle
        var tx = x + w - 200, ty = ry + 34; k.rr(tx, ty, 92, 44, 22); ctx.fillStyle = on ? C.green : '#C9D0E0'; ctx.fill();
        ctx.beginPath(); ctx.arc(lerp(tx + 22, tx + 70, back(u)), ty + 22, 17, 0, 6.283); ctx.fillStyle = '#fff'; ctx.fill();
        k.text(on ? 'On' : 'Off', tx - 24, ty + 31, 22, '700', on ? C.green : C.muted, { align: 'right' }); ev('click', r[1]);
      } else if (i === 1) { // curve
        var gx = x + 470, gy = ry + 20, gw = 300, gh = 70; ctx.strokeStyle = C.line; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(gx, gy + gh); ctx.lineTo(gx + gw, gy + gh); ctx.stroke();
        var pts = []; for (var q = 0; q <= 30; q++) { var v = q / 30; pts.push([gx + v * gw, gy + gh - gh * (1 - Math.pow(v, 2.4)) * .95]); }
        ctx.strokeStyle = C.navy; ctx.lineWidth = 3.5; k.partial(pts, u * 1.2);
        if (u >= 1) { k.check(x + w - 120, ry + 54, 18, C.green, 1, seg(t, r[1] + .5, r[1] + .8)); k.text('Done', x + w - 150, ry + 62, 22, '700', C.green, { align: 'right' }); }
      } else { // chain
        for (var b = 0; b < 3; b++) {
          var bk = eo(seg(t, r[1] + b * .18, r[1] + b * .18 + .3)), bx = x + 470 + b * 112, by = ry + 30;
          if (bk <= 0) continue; ctx.save(); ctx.globalAlpha *= bk; k.rr(bx, by + (1 - bk) * -30, 74, 48, 12); ctx.fillStyle = k.hex(C.tip, .14); ctx.fill(); ctx.strokeStyle = C.tip; ctx.lineWidth = 2.5; ctx.stroke();
          k.mono('#' + (4810 + b), bx + 37, by + 30, 12, C.tip, { align: 'center', track: 0 });
          if (b) { ctx.strokeStyle = C.tip; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(bx - 38, by + 24); ctx.lineTo(bx, by + 24); ctx.stroke(); }
          ctx.restore(); ev('click', r[1] + b * .18);
        }
        if (t > r[1] + .8) { k.check(x + w - 120, ry + 54, 18, C.tip, 1, seg(t, r[1] + .8, r[1] + 1.1)); k.text('On-chain', x + w - 150, ry + 62, 22, '700', C.tip, { align: 'right' }); }
      }
    });
    ctx.restore();
    k.stamp('SERVICED', x + w - 170, y + h - 20, t, Q.nb(i2 + d2 + .05), C.green, { size: 46, seed: 31, ring: C.green, fill: 'rgba(255,255,255,.92)' });
    label('AI Insurance Servicing', p[0], y + h + 64, eo(seg(t, i1, i1 + .6)));
  }

  // ───────── 4 · growth capital ─────────
  var METRICS = ['Fleet util.', 'Backlog', 'DSO', 'Margin', 'Leverage', 'Basin mix', 'Rig exposure', 'Capex', 'Cash cycle', 'Customer conc.'];
  function loan(t, Q) {
    var s0 = Q.S('loan'); if (t < s0 - .4) return;
    var p = POS.loan, w = 1340, h = 640, x = p[0] - w / 2, y = p[1] - 320, e = enter(t, s0 - .3);
    ctx.save(); ctx.globalAlpha = e; ctx.translate(0, (1 - e) * 60);
    k.card(x, y, w, h, 34);
    var l1 = Q.V('l1'), l2 = Q.V('l2'), d2 = Q.D('l2');
    k.mono('Credit file · growth capital', x + 48, y + 56, 15);
    k.text('Dana’s company', x + 48, y + 100, 36, '800', C.ink, { stretch: 'semi-expanded' });
    var ask = 'Request: growth line to add two crews';
    k.text(k.typed(ask, seg(t, l1, l1 + Q.D('l1'))), x + 48, y + 138, 21, '500', C.muted);
    // fifty metrics light up
    var gx = x + 48, gy = y + 190, sweep0 = l2 + d2 * .12, sweep1 = l2 + d2 * .55, lit = 0;
    for (var i = 0; i < 50; i++) {
      var c = i % 10, r = Math.floor(i / 10), cx = gx + c * 76, cy = gy + r * 62, on = t >= lerp(sweep0, sweep1, (c + r * .6) / 12.4);
      if (on) lit++;
      k.rr(cx, cy, 68, 50, 12); ctx.fillStyle = on ? C.navy : '#F1F4FA'; ctx.fill();
      k.text(on ? '✓' : '·', cx + 34, cy + 33, 20, '800', on ? '#fff' : '#B7C0D6', { align: 'center' });
    }
    k.mono('Industry metrics scored', gx, gy + 352, 15); k.text(lit + (lit >= 50 ? '+' : ''), gx + 330, gy + 360, 40, '850', C.navy, { stretch: 'semi-expanded' });
    k.mono(METRICS.slice(0, 5).join(' · '), gx, gy + 400, 13, '#9AA3BC', { track: .5 });
    // weeks → days
    var cx0 = x + 860, cy0 = y + 150, collapse = eio(seg(t, l2 + d2 * .74, l2 + d2 * .74 + .7));
    k.rr(cx0, cy0, 430, 420, 24); ctx.fillStyle = '#F6F8FC'; ctx.fill();
    k.mono('Time to decision', cx0 + 28, cy0 + 44, 15);
    var big = collapse < .5 ? 'Weeks' : 'Days', bc = collapse < .5 ? C.red : C.green;
    k.text(big, cx0 + 28, cy0 + 112, 60, '850', bc, { stretch: 'expanded' });
    var cells = Math.round(lerp(28, 3, collapse));
    for (var d = 0; d < 28; d++) {
      var dc = d % 7, dr = Math.floor(d / 7), dx = cx0 + 28 + dc * 54, dy = cy0 + 160 + dr * 54;
      var active = d < cells; k.rr(dx, dy, 44, 44, 10); ctx.fillStyle = active ? (collapse < .5 ? k.hex(C.red, .16 + .1 * (d % 3)) : C.green) : '#E6EAF3'; ctx.fill();
    }
    if (collapse > 0 && collapse < .2) ev('whoosh', l2 + d2 * .74);
    ctx.restore();
    k.stamp('APPROVED', x + w - 230, y + h - 40, t, Q.nb(l2 + d2 + .1), C.green, { size: 50, seed: 41, ring: C.green, fill: 'rgba(255,255,255,.92)' });
    label('Arsenal Finance · growth capital · M&A · wealth & tax', p[0], y + h + 64, eo(seg(t, l1, l1 + .6)));
  }

  // ───────── 5 · energy field ─────────
  function energy(t, Q) {
    var s0 = Q.S('energy'); if (t < s0 - .5) return;
    var p = POS.energy, gx = p[0], gy = p[1] + 170, e = enter(t, s0 - .4);
    ctx.save(); ctx.globalAlpha = e;
    // sky panel
    k.card(gx - 900, p[1] - 360, 1800, 700, 40, { fill: '#F8FAFE' });
    ctx.strokeStyle = C.navy; ctx.lineWidth = 4; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(gx - 860, gy); ctx.lineTo(gx + 860, gy); ctx.stroke();
    // pumpjack
    var px = gx - 640, rock = Math.sin(t * 2.4) * .17;
    ctx.beginPath(); ctx.moveTo(px - 90, gy); ctx.lineTo(px - 90, gy - 26); ctx.lineTo(px + 110, gy - 26); ctx.lineTo(px + 110, gy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(px - 36, gy - 26); ctx.lineTo(px, gy - 190); ctx.lineTo(px + 36, gy - 26); ctx.stroke();
    ctx.save(); ctx.translate(px, gy - 190); ctx.rotate(rock); ctx.beginPath(); ctx.moveTo(-150, 0); ctx.lineTo(140, 0); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-150, -24); ctx.quadraticCurveTo(-190, 0, -150, 44); ctx.stroke(); ctx.restore();
    ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(px - 150 * Math.cos(rock), gy - 190 - 150 * Math.sin(rock) + 44); ctx.lineTo(px - 150, gy); ctx.stroke(); ctx.lineWidth = 4;
    // pipeline with flow
    var pipe = [[px + 120, gy - 50], [gx - 140, gy - 50], [gx - 140, gy - 110], [gx + 10, gy - 110]];
    ctx.strokeStyle = '#D6DDEE'; ctx.lineWidth = 18; k.partial(pipe, 1);
    ctx.strokeStyle = C.facet; ctx.lineWidth = 5; ctx.setLineDash([4, 22]); ctx.lineDashOffset = -t * 90; k.partial(pipe, 1); ctx.setLineDash([]);
    ctx.strokeStyle = C.navy; ctx.lineWidth = 4;
    // processing plant
    var pl = gx + 40;
    ctx.strokeRect(pl, gy - 230, 54, 230); ctx.strokeRect(pl + 74, gy - 160, 120, 160);
    ctx.beginPath(); ctx.arc(pl + 134, gy - 160, 60, Math.PI, 0); ctx.stroke(); ctx.strokeRect(pl + 214, gy - 290, 30, 290);
    // storage tanks
    var st = gx + 380; for (var s = 0; s < 3; s++) { ctx.beginPath(); ctx.ellipse(st + s * 110, gy - 120, 44, 12, 0, 0, 6.283); ctx.stroke(); ctx.beginPath(); ctx.moveTo(st + s * 110 - 44, gy - 120); ctx.lineTo(st + s * 110 - 44, gy); ctx.moveTo(st + s * 110 + 44, gy - 120); ctx.lineTo(st + s * 110 + 44, gy); ctx.stroke(); }
    // biogas dome
    ctx.strokeStyle = C.green; ctx.beginPath(); ctx.arc(gx + 760, gy, 70, Math.PI, 0); ctx.stroke(); ctx.fillStyle = k.hex(C.green, .1); ctx.fill();
    ctx.lineCap = 'butt';
    [['Upstream', px], ['Midstream', gx - 70], ['Downstream', pl + 130], ['Storage', st + 110], ['Biogas', gx + 760]].forEach(function (l) { k.mono(l[0], l[1], gy + 46, 15, l[0] === 'Biogas' ? C.green : C.muted, { align: 'center' }); });
    // agents at work
    var e2 = Q.V('e2'), d2 = Q.D('e2');
    var AG = [[px + 20, gy - 250, 'Pump 3 · bearing wear detected', 'Service scheduled', e2 + d2 * .05], [pl + 130, gy - 340, 'Plant throughput', 'Tuned +', e2 + d2 * .4], [st + 110, gy - 230, 'Valves & seals', 'Parts ordered', e2 + d2 * .75]];
    AG.forEach(function (a, i) {
      if (t < a[4]) return; var u = seg(t, a[4], a[4] + .45), ring = (t - a[4]) % 1.4 / 1.4;
      ev('pop', a[4]);
      ctx.strokeStyle = k.hex(C.navy, (1 - ring) * .6); ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(a[0], a[1] + 90, 20 + ring * 60, 0, 6.283); ctx.stroke();
      k.spark(a[0], a[1] + 90, 16 * back(u), C.navy, 1, t * 1.5);
      var cw = 330, cx = a[0] - cw / 2, cy = a[1] - 70;
      ctx.save(); ctx.globalAlpha *= eo(u); ctx.translate(0, (1 - eo(u)) * 20);
      k.card(cx, cy, cw, 104, 20, { blur: 30, oy: 10 });
      k.mono('Agent', cx + 22, cy + 32, 13, C.navy); k.text(a[2], cx + 22, cy + 62, 18, '700', C.ink);
      var ok = t > a[4] + .7; if (ok) { k.check(cx + 34, cy + 84, 10, C.green, 1, seg(t, a[4] + .7, a[4] + 1)); k.text(a[3], cx + 52, cy + 90, 17, '700', C.green); }
      ctx.restore();
    });
    ctx.restore();
    label('Energy · upstream · midstream · downstream · biogas', p[0], p[1] + 410, eo(seg(t, Q.V('e1'), Q.V('e1') + .6)));
  }

  // ───────── montage: four quick vignettes ─────────
  function montage(t, Q) {
    var keys = ['m1', 'm2', 'm3', 'm4'], names = ['Digital Twins / Legacy AI', 'AI Implementation', 'Publishing & Marketing', 'Agentic Entities & Robotics'];
    keys.forEach(function (key, i) {
      var t0 = Q.V(key) - .35; if (t < t0) return;
      var p = POS['m' + i], w = 1100, h = 600, x = p[0] - w / 2, y = p[1] - 300, e = eo(seg(t, t0, t0 + .45));
      ctx.save(); ctx.globalAlpha = e; ctx.translate(p[0], p[1]); ctx.scale(lerp(.9, 1, e), lerp(.9, 1, e)); ctx.translate(-p[0], -p[1]);
      k.card(x, y, w, h, 34);
      var u = t - Q.V(key);
      if (i === 0) {         // a person becomes a glowing, faceted twin that answers
        person(x + 260, y + 330, 1, '#C9D0E0');
        ctx.strokeStyle = C.navy; ctx.lineWidth = 4; ctx.setLineDash([3, 12]); ctx.beginPath(); ctx.moveTo(x + 400, y + 300); ctx.lineTo(x + 560, y + 300); ctx.stroke(); ctx.setLineDash([]);
        var tw = eo(seg(u, .2, .9)); ctx.save(); ctx.globalAlpha *= tw; k.glow(x + 700, y + 300, 220, C.ice, .5); person(x + 700, y + 330, 1, C.navy, true, t); ctx.restore();
        var bubble = 'Walk away if the books aren’t open in week one.';
        if (u > .9) { ctx.save(); ctx.globalAlpha *= eo(seg(u, .9, 1.2)); k.rr(x + 590, y + 70, 470, 70, 22); ctx.fillStyle = C.navy; ctx.fill(); k.text(k.typed(bubble, seg(u, 1, 2.2)), x + 614, y + 113, 18, '600', '#fff'); ctx.restore(); }
      } else if (i === 1) {  // build → grow → sell
        var steps = ['Build', 'Grow', 'Sell'];
        ctx.strokeStyle = C.line; ctx.lineWidth = 10; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x + 200, y + 300); ctx.lineTo(x + 900, y + 300); ctx.stroke();
        var pk = eio(seg(u, .2, 2)); ctx.strokeStyle = C.navy; ctx.beginPath(); ctx.moveTo(x + 200, y + 300); ctx.lineTo(x + 200 + 700 * pk, y + 300); ctx.stroke(); ctx.lineCap = 'butt';
        steps.forEach(function (s, j) { var sx = x + 200 + j * 350, on = pk >= j / 2 - .01; ctx.beginPath(); ctx.arc(sx, y + 300, 40, 0, 6.283); ctx.fillStyle = on ? C.navy : '#fff'; ctx.fill(); ctx.strokeStyle = on ? C.navy : C.line; ctx.lineWidth = 4; ctx.stroke(); if (on) k.check(sx, y + 300, 20, 'rgba(255,255,255,.2)', 1, 1); k.text(s, sx, y + 390, 34, '800', on ? C.ink : C.muted, { align: 'center', stretch: 'semi-expanded' }); });
        k.text('For owners adopting AI', x + 550, y + 150, 26, '600', C.muted, { align: 'center' });
      } else if (i === 2) {  // a content calendar fills itself
        var days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], items = ['Article', 'Video', 'Podcast', 'Social ×6', 'Newsletter', 'Ad set', 'Case study', 'Webinar', 'Social ×4', 'Report'];
        days.forEach(function (d, j) { k.mono(d, x + 130 + j * 180, y + 120, 15); });
        for (var c = 0; c < 15; c++) { var cx = x + 110 + (c % 5) * 180, cy = y + 150 + Math.floor(c / 5) * 120, on = u > .2 + c * .1 && [0, 2, 3, 6, 7, 9, 11, 12, 13, 14].indexOf(c) >= 0, ck = eo(seg(u, .2 + c * .1, .45 + c * .1));
          k.rr(cx, cy, 160, 100, 16); ctx.fillStyle = '#F6F8FC'; ctx.fill(); if (on) { ctx.save(); ctx.globalAlpha *= ck; k.rr(cx + 8, cy + 8, 144, 84, 12); ctx.fillStyle = [C.navy, C.facet, C.ice, C.tip][c % 4]; ctx.fill(); k.text(items[c % items.length], cx + 22, cy + 60, 19, '700', c % 4 === 2 ? C.ink : '#fff'); ctx.restore(); } }
      } else {               // a builder arm stacks blocks, a service robot waves
        var base = y + 470; ctx.strokeStyle = C.line; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x + 120, base); ctx.lineTo(x + 980, base); ctx.stroke();
        for (var b = 0; b < 3; b++) { var bk = eo(seg(u, .3 + b * .45, .7 + b * .45)); if (bk <= 0) continue; var bx = x + 230, by = base - 90 - b * 90; k.rr(bx, lerp(by - 120, by, bk), 160, 84, 12); ctx.fillStyle = [C.navy, C.facet, C.ice][b]; ctx.fill(); }
        ctx.strokeStyle = C.ink; ctx.lineWidth = 12; ctx.lineCap = 'round'; var ang = Math.sin(u * 3) * .3; ctx.beginPath(); ctx.moveTo(x + 520, base); ctx.lineTo(x + 520, base - 200); ctx.lineTo(x + 520 - 160 * Math.cos(ang), base - 200 - 120 * Math.sin(ang + .6)); ctx.stroke(); ctx.lineCap = 'butt';
        robot(x + 820, base, u);
      }
      label(names[i], p[0], y + h + 64, e);
      ctx.restore();
    });
  }
  function person(x, y, s, color, faceted, t) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    ctx.fillStyle = color; ctx.beginPath(); ctx.arc(0, -120, 70, 0, 6.283); ctx.fill();
    ctx.beginPath(); ctx.moveTo(-140, 130); ctx.quadraticCurveTo(-140, -30, 0, -30); ctx.quadraticCurveTo(140, -30, 140, 130); ctx.closePath(); ctx.fill();
    if (faceted) { ctx.strokeStyle = 'rgba(156,200,236,.9)'; ctx.lineWidth = 2; for (var i = 0; i < 9; i++) { ctx.beginPath(); ctx.moveTo(-140 + i * 35, 130); ctx.lineTo(-100 + i * 25, -20); ctx.lineTo(-60 + i * 20, 130); ctx.stroke(); }
      for (var j = 0; j < 6; j++) k.spark(-120 + j * 48, -150 + Math.sin(t * 2 + j) * 40, 6, '#fff', .8, t); }
    ctx.restore();
  }
  function robot(x, y, u) {
    ctx.save(); ctx.translate(x, y);
    ctx.fillStyle = C.ink; k.rr(-70, -230, 140, 150, 34); ctx.fill(); k.rr(-50, -70, 100, 70, 14); ctx.fill();
    ctx.fillStyle = C.ice; ctx.beginPath(); ctx.arc(-28, -160, 14, 0, 6.283); ctx.arc(28, -160, 14, 0, 6.283); ctx.fill();
    ctx.strokeStyle = C.ink; ctx.lineWidth = 10; ctx.lineCap = 'round'; var wv = Math.sin(u * 9) * .5; ctx.beginPath(); ctx.moveTo(60, -130); ctx.lineTo(60 + 70 * Math.cos(-1.2 + wv), -130 + 70 * Math.sin(-1.2 + wv)); ctx.stroke(); ctx.lineCap = 'butt';
    ctx.restore();
  }

  window.WORLD_SCENES = [accounting, family, insurance, loan, energy, montage];
  window.SCN = { label: label, person: person, ev: ev };
})();
