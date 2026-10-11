/* The Arsenal star chart.
   The constellation is the real Arsenal mark: its facets sit on a triangular lattice
   (64.07 x 93.77 units in the logo file), so every vertex becomes a star, every facet edge
   a constellation line, and the eleven named stars are the companies in the portfolio. */
(function () {
  'use strict';

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var COARSE = matchMedia('(pointer: coarse)').matches;

  // Facets of the mark in lattice coordinates [i, j]; i: 0..10 across, j: 0..8 down.
  // 'a' and 'b' are the logo's two facet tones; 't' is the small tip under the A.
  var TRIS = [
    ['a',[5,2],[5,0],[6,1]],['a',[6,3],[6,1],[7,2]],['a',[7,4],[7,2],[8,3]],['a',[8,5],[8,3],[9,4]],
    ['a',[9,6],[9,4],[10,5]],['a',[5,4],[5,2],[6,3]],['a',[6,5],[6,3],[7,4]],['a',[7,6],[7,4],[8,5]],
    ['a',[8,7],[8,5],[9,6]],
    ['b',[5,4],[5,2],[4,3]],['b',[6,1],[6,3],[5,2]],['b',[7,2],[7,4],[6,3]],['b',[8,3],[8,5],[7,4]],
    ['b',[9,4],[9,6],[8,5]],['b',[6,3],[6,5],[5,4]],['b',[7,4],[7,6],[6,5]],['b',[8,5],[8,7],[7,6]],
    ['b',[5,2],[5,0],[4,1]],['b',[4,3],[4,1],[3,2]],['b',[3,4],[3,2],[2,3]],['b',[2,5],[2,3],[1,4]],
    ['b',[1,6],[1,4],[0,5]],['b',[4,5],[4,3],[3,4]],['b',[3,6],[3,4],[2,5]],['b',[2,7],[2,5],[1,6]],
    ['a',[4,1],[4,3],[5,2]],['a',[3,2],[3,4],[4,3]],['a',[2,3],[2,5],[3,4]],['a',[1,4],[1,6],[2,5]],
    ['a',[4,3],[4,5],[5,4]],['a',[3,4],[3,6],[4,5]],['a',[2,5],[2,7],[3,6]],
    ['t',[5,6],[4,7],[5,8]],['t',[5,6],[6,7],[5,8]],['t',[4,7],[3,8],[5,8]],['t',[6,7],[7,8],[5,8]]
  ];

  var STATUS = {
    core:     { label: 'Shared platform',  color: '#E9EEF9' },
    operating:{ label: 'Operating today',  color: '#3DCB8C' },
    build:    { label: 'AI-native build',  color: '#9CC8EC' },
    pipeline: { label: 'Build pipeline',   color: '#B49CFB' }
  };

  var NAMED = {
    '5,0':  { name: 'Shared AI Stack', s: 'core', line: 'Models, data, agents and tooling that every company inherits.', href: '#model' },
    '3,2':  { name: 'AI for Accountants', s: 'build', line: 'Software that runs an accounting firm.', href: '#build', k: 'accounting' },
    '7,2':  { name: 'Multi-Family Office', s: 'build', line: 'One AI tool unifying accounting, legal, insurance & wealth.', href: '#build', k: 'mfo' },
    '1,4':  { name: 'AI Insurance Servicing', s: 'build', line: 'Policy management, autopay, life settlements on-chain.', href: '#build', k: 'insurance' },
    '9,4':  { name: 'AI Implementation', s: 'build', line: 'A build-grow-sell practice for businesses adopting AI.', href: '#build', k: 'implementation' },
    '5,4':  { name: 'Digital Twins / Legacy AI', s: 'build', line: 'Human expertise turned into lasting intelligence.', href: '#build', k: 'twins' },
    '2,7':  { name: 'Publishing & Marketing', s: 'build', line: 'AI-native content and agencies.', href: '#build', k: 'publishing' },
    '8,7':  { name: 'Agentic Entities & Robotics', s: 'build', line: 'Autonomous builders and service/advertising robots.', href: '#build', k: 'robotics' },
    '0,5':  { name: 'Energy', s: 'operating', line: 'Production, infrastructure and waste-to-energy, generating cash today.', href: '#foundation', f: 'energy', label: 'ENERGY' },
    '10,5': { name: 'Finance', s: 'operating', line: 'Specialized financing and M&A for energy companies.', href: '#foundation', f: 'finance', label: 'FINANCE' },
    '5,6':  { name: 'Health & Insurance Services', s: 'pipeline', line: 'The next vertical. Seeking founding partners.', href: '#foundation', f: 'health' }
  };

  function rand(a, b) { return a + Math.random() * (b - a); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function easeOut(t) { t = clamp(t, 0, 1); return 1 - Math.pow(1 - t, 3); }
  function easeInOut(t) { t = clamp(t, 0, 1); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function rgba(c, a) { return 'rgba(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ',' + a + ')'; }

  var ICE = [156, 200, 236], FACET = [110, 143, 214], DEEP = [59, 71, 166], TIP = [139, 92, 246], WHITE = [233, 238, 249];

  /**
   * createSky(canvas, { constellation, box, card, onPick })
   *  constellation: draw the Arsenal A (hero only)
   *  box:  element whose rect positions the constellation
   *  card: element used as the hover card for named stars
   */
  function createSky(canvas, opts) {
    opts = opts || {};
    var ctx = canvas.getContext('2d');
    var host = canvas.parentElement;
    var DPR = Math.min(window.devicePixelRatio || 1, 2);
    var W = 0, H = 0, stars = [], band = null;
    var mouse = { x: -9999, y: -9999, sx: -9999, sy: -9999, in: false };
    var ripples = [], meteors = [], nextMeteor = 2;
    var t0 = performance.now(), last = t0, running = false, visible = true;
    var scrollV = 0, lastScroll = window.scrollY;
    var hover = null;

    // constellation state
    var verts = {}, vlist = [], edges = [], facets = [], box = { x: 0, y: 0, w: 0, h: 0 };

    if (opts.constellation) buildLattice();

    function buildLattice() {
      var seen = {};
      TRIS.forEach(function (t) {
        var pts = t.slice(1).map(function (p) {
          var k = p[0] + ',' + p[1];
          if (!verts[k]) {
            verts[k] = { k: k, i: p[0], j: p[1], x: 0, y: 0, sx: rand(-.3, 1.3), sy: rand(-.3, 1.3),
              d: .05 + p[1] / 8 * .45 + Math.random() * .12, ph: Math.random() * 6.28, info: NAMED[k] || null };
            vlist.push(verts[k]);
          }
          return verts[k];
        });
        for (var e = 0; e < 3; e++) {
          var a = pts[e], b = pts[(e + 1) % 3];
          var key = a.k < b.k ? a.k + '|' + b.k : b.k + '|' + a.k;
          if (!seen[key]) { seen[key] = 1; edges.push({ a: a, b: b, d: .55 + Math.min(a.j, b.j) / 8 * .6 + Math.random() * .15 }); }
        }
        facets.push({ tone: t[0], v: pts, d: 1.2 + Math.random() * .3 });
      });
    }

    function layout() {
      var r = host.getBoundingClientRect();
      W = r.width; H = r.height;
      canvas.width = Math.round(W * DPR); canvas.height = Math.round(H * DPR);
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);

      var n = Math.min(opts.constellation ? 900 : 420, Math.floor(W * H / (opts.constellation ? 1500 : 1900)));
      stars = [];
      for (var i = 0; i < n; i++) {
        var z = Math.pow(Math.random(), 1.8); // most stars far away
        var warm = Math.random() < .08;
        stars.push({ x: Math.random() * W, y: Math.random() * H, z: z,
          r: .35 + z * 1.5 + (Math.random() < .03 ? 1 : 0),
          ph: Math.random() * 6.28, sp: rand(.6, 2.2),
          c: warm ? [255, 214, 170] : mix(WHITE, ICE, Math.random() * .6),
          dx: 0, dy: 0 });
      }
      band = renderBand();

      if (opts.constellation && opts.box) {
        var b = opts.box.getBoundingClientRect();
        // The A's true proportions: 10 columns x 64.07 wide, 8 rows x 93.77 tall.
        var aspect = 640.68 / 750.13, pad = .08;
        var bw = b.width * (1 - pad * 2), bh = bw / aspect;
        if (bh > b.height * (1 - pad * 2)) { bh = b.height * (1 - pad * 2); bw = bh * aspect; }
        box.w = bw; box.h = bh;
        box.x = b.left - r.left + (b.width - bw) / 2;
        box.y = b.top - r.top + (b.height - bh) / 2;
        vlist.forEach(function (v) {
          v.x = box.x + v.i / 10 * box.w;
          v.y = box.y + v.j / 8 * box.h;
          v.fx = v.sx * W; v.fy = v.sy * H; // where it flies in from
        });
        facets.forEach(function (f) {
          f.cx = (f.v[0].x + f.v[1].x + f.v[2].x) / 3;
          f.cy = (f.v[0].y + f.v[1].y + f.v[2].y) / 3;
          var u = (f.cx - box.x) / box.w, w = (f.cy - box.y) / box.h;
          var g = clamp(u * .65 + w * .35, 0, 1);
          f.col = f.tone === 't' ? TIP : (g < .5 ? mix(ICE, FACET, g * 2) : mix(FACET, DEEP, (g - .5) * 2));
          if (f.tone === 'b' && f.tone !== 't') f.col = mix(f.col, WHITE, .18);
        });
      }
    }

    // A faint galactic band with dust, painted once per resize.
    function renderBand() {
      var c = document.createElement('canvas');
      c.width = Math.max(1, Math.round(W)); c.height = Math.max(1, Math.round(H));
      var g = c.getContext('2d');
      g.save();
      g.translate(W * .5, H * .5); g.rotate(-.42); g.translate(-W * .5, -H * .5);
      for (var i = 0; i < 26; i++) {
        var x = rand(-.1, 1.1) * W, y = H * .5 + rand(-.12, .12) * H, rr = rand(.08, .22) * Math.max(W, H);
        var grd = g.createRadialGradient(x, y, 0, x, y, rr);
        var col = Math.random() < .25 ? TIP : (Math.random() < .5 ? DEEP : FACET);
        grd.addColorStop(0, rgba(col, Math.random() * .05 + .025)); grd.addColorStop(1, rgba(col, 0));
        g.fillStyle = grd; g.fillRect(x - rr, y - rr, rr * 2, rr * 2);
      }
      var dust = Math.floor(W * H / 900);
      for (var d = 0; d < dust; d++) {
        var dx = Math.random() * W, dy = H * .5 + (Math.random() + Math.random() + Math.random() - 1.5) * H * .16;
        g.fillStyle = 'rgba(220,230,255,' + (Math.random() * .22) + ')';
        g.fillRect(dx, dy, .7, .7);
      }
      g.restore();
      return c;
    }

    function heroProgress() {
      var r = host.getBoundingClientRect();
      return clamp(-r.top / Math.max(1, r.height), 0, 1);
    }

    function frame(now) {
      if (!running) return;
      var dt = Math.min(.05, (now - last) / 1000); last = now;
      var t = REDUCED ? 99 : (now - t0) / 1000;
      var sy = window.scrollY; scrollV += ((sy - lastScroll) - scrollV) * .2; lastScroll = sy;
      var p = heroProgress();

      mouse.sx += (mouse.x - mouse.sx) * .12; mouse.sy += (mouse.y - mouse.sy) * .12;
      var mx = mouse.in ? (mouse.sx - W / 2) / W : 0, my = mouse.in ? (mouse.sy - H / 2) / H : 0;

      ctx.clearRect(0, 0, W, H);

      // galactic band, slow drift + parallax
      if (band) { ctx.globalAlpha = clamp(t / .8, 0, 1) * (1 - p * .6); ctx.drawImage(band, -mx * 14, -my * 10 - p * 40); ctx.globalAlpha = 1; }

      drawGraticule(t, p);

      // background stars
      var fade = clamp(t / .6, 0, 1), R = COARSE ? 0 : 150, near = [];
      var warp = REDUCED ? 0 : clamp(Math.abs(scrollV), 0, 60);
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        var px = s.x - mx * 40 * s.z, py = s.y - my * 30 * s.z - p * 160 * s.z;
        // ripples push stars outward
        for (var q = 0; q < ripples.length; q++) {
          var rp = ripples[q], age = (now - rp.t) / 1000, rr = age * 520;
          var ddx = px - rp.x, ddy = py - rp.y, dd = Math.sqrt(ddx * ddx + ddy * ddy) || 1;
          var push = 26 * Math.exp(-Math.pow(dd - rr, 2) / 1800) * (1 - age / 1.4);
          if (push > 0) { px += ddx / dd * push; py += ddy / dd * push; }
        }
        // cursor gravity
        if (R && mouse.in) {
          var cx = mouse.sx - px, cy = mouse.sy - py, cd = Math.sqrt(cx * cx + cy * cy);
          if (cd < R) { var f = Math.pow(1 - cd / R, 2) * 10 * (s.z + .3); px += cx / cd * f; py += cy / cd * f; near.push({ x: px, y: py, d: cd, z: s.z }); }
        }
        var tw = REDUCED ? 1 : .65 + .35 * Math.sin(t * s.sp + s.ph);
        var a = fade * tw * (.25 + s.z * .75);
        if (warp > 3 && s.z > .25) {
          ctx.strokeStyle = rgba(s.c, a * .8); ctx.lineWidth = s.r;
          ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px, py - scrollV * s.z * .9); ctx.stroke();
        } else {
          ctx.fillStyle = rgba(s.c, a);
          ctx.beginPath(); ctx.arc(px, py, s.r, 0, 6.283); ctx.fill();
          if (s.r > 1.6) { ctx.fillStyle = rgba(s.c, a * .12); ctx.beginPath(); ctx.arc(px, py, s.r * 4, 0, 6.283); ctx.fill(); }
        }
      }

      // the visitor's own constellation: lines from the cursor to nearby stars, and between them
      if (near.length) {
        near.sort(function (a, b) { return a.d - b.d; });
        near = near.slice(0, 14);
        ctx.lineWidth = .8;
        for (var n1 = 0; n1 < near.length; n1++) {
          var A = near[n1];
          ctx.strokeStyle = 'rgba(156,200,236,' + ((1 - A.d / R) * .45) + ')';
          ctx.beginPath(); ctx.moveTo(mouse.sx, mouse.sy); ctx.lineTo(A.x, A.y); ctx.stroke();
          for (var n2 = n1 + 1; n2 < near.length; n2++) {
            var B = near[n2], ex = A.x - B.x, ey = A.y - B.y, ed = Math.sqrt(ex * ex + ey * ey);
            if (ed < 70) { ctx.strokeStyle = 'rgba(156,200,236,' + ((1 - ed / 70) * .25) + ')'; ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.stroke(); }
          }
        }
        var lg = ctx.createRadialGradient(mouse.sx, mouse.sy, 0, mouse.sx, mouse.sy, R * 1.2);
        lg.addColorStop(0, 'rgba(156,200,236,.07)'); lg.addColorStop(1, 'rgba(156,200,236,0)');
        ctx.fillStyle = lg; ctx.beginPath(); ctx.arc(mouse.sx, mouse.sy, R * 1.2, 0, 6.283); ctx.fill();
      }

      if (opts.constellation) drawConstellation(t, now, p, mx, my);

      drawRipples(now);
      if (!REDUCED) drawMeteors(t, dt);

      requestAnimationFrame(frame);
    }

    function drawGraticule(t, p) {
      if (!opts.constellation) return;
      ctx.save();
      ctx.strokeStyle = 'rgba(156,200,236,.06)'; ctx.lineWidth = 1; ctx.setLineDash([2, 8]);
      var cx = W * .72, cy = H * .48 - p * 60, rot = t * .01;
      for (var i = 1; i <= 3; i++) {
        ctx.beginPath();
        ctx.ellipse(cx, cy, Math.max(W, H) * (.25 + i * .17), Math.max(W, H) * (.1 + i * .07), -.35 + rot, 0, 6.283);
        ctx.stroke();
      }
      ctx.restore();
    }

    function vpos(v, t, p, mx, my) {
      // fly in from the sky, then hold the lattice with a slight breathing motion
      var e = easeInOut((t - v.d) / 1.15);
      var bx = v.x - mx * 18, by = v.y - my * 14;
      var breathe = REDUCED ? 0 : Math.sin(t * .8 + v.ph) * .8;
      var x = v.fx + (bx - v.fx) * e, y = v.fy + (by - v.fy) * e + breathe;
      // scroll: the A lifts and grows slightly as the hero leaves
      var sc = 1 + p * .12, ox = box.x + box.w / 2, oy = box.y + box.h / 2;
      return { x: ox + (x - ox) * sc, y: oy + (y - oy) * sc - p * 90, e: e };
    }

    function drawConstellation(t, now, p, mx, my) {
      var alpha = 1 - p * .85;
      if (alpha <= 0) return;
      var P = {};
      vlist.forEach(function (v) { P[v.k] = vpos(v, t, p, mx, my); });

      // sweeping light across the facets, every ~9s
      var sweepT = ((t - 1.8) % 9) / 1.8, sweepOn = t > 1.8 && sweepT < 1 && !REDUCED;

      // facets
      facets.forEach(function (f) {
        var a = P[f.v[0].k], b = P[f.v[1].k], c = P[f.v[2].k];
        var cx = (a.x + b.x + c.x) / 3, cy = (a.y + b.y + c.y) / 3;
        var base = (f.tone === 't' ? .13 : .085) * easeOut((t - f.d) / .9);
        var glow = 0;
        if (mouse.in) { var dd = Math.hypot(mouse.sx - cx, mouse.sy - cy); glow = Math.pow(clamp(1 - dd / 260, 0, 1), 2) * .32; }
        if (sweepOn) { var u = ((cx - box.x) / box.w + (cy - box.y) / box.h) / 2; glow += Math.exp(-Math.pow(u - (sweepT * 1.6 - .3), 2) / .01) * .22; }
        if (f.tone === 't') glow += (Math.sin(t * 2.2) * .5 + .5) * .08;
        var A = (base + glow) * alpha;
        if (A <= .002) return;
        ctx.fillStyle = rgba(f.col, A);
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.lineTo(c.x, c.y); ctx.closePath(); ctx.fill();
      });

      // edges draw themselves in
      ctx.lineWidth = 1;
      edges.forEach(function (ed) {
        var pr = easeOut((t - ed.d) / .7);
        if (pr <= 0) return;
        var a = P[ed.a.k], b = P[ed.b.k];
        var mxp = (a.x + b.x) / 2, myp = (a.y + b.y) / 2, boost = 0;
        if (mouse.in) boost = Math.pow(clamp(1 - Math.hypot(mouse.sx - mxp, mouse.sy - myp) / 220, 0, 1), 2) * .5;
        var tip = ed.a.j >= 6 && ed.b.j >= 6 && ed.a.i >= 3 && ed.a.i <= 7 && ed.b.i >= 3 && ed.b.i <= 7;
        ctx.strokeStyle = tip ? rgba(TIP.map(function (c) { return c + 60; }), (.4 + boost) * alpha) : 'rgba(186,212,240,' + ((.26 + boost) * alpha) + ')';
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(a.x + (b.x - a.x) * pr, a.y + (b.y - a.y) * pr); ctx.stroke();
      });

      // stars on the lattice
      var hit = null, best = 22;
      vlist.forEach(function (v) {
        var q = P[v.k];
        var named = !!v.info, st = named ? STATUS[v.info.s] : null;
        var col = named ? hexRgb(st.color) : WHITE;
        var tw = REDUCED ? 1 : .8 + .2 * Math.sin(t * 2 + v.ph);
        var r = (named ? 2.6 : 1.5) * tw;
        var isHover = hover === v;
        if (isHover) r *= 1.6;
        var a = clamp(.25 + q.e * .75, 0, 1) * alpha;
        // halo
        var hr = r * (named ? 7 : 4.5);
        var g = ctx.createRadialGradient(q.x, q.y, 0, q.x, q.y, hr);
        g.addColorStop(0, rgba(col, (named ? .45 : .28) * a)); g.addColorStop(1, rgba(col, 0));
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(q.x, q.y, hr, 0, 6.283); ctx.fill();
        // diffraction spikes on named stars
        if (named && q.e > .9) {
          var sp = r * (isHover ? 7 : 4.2);
          ctx.strokeStyle = rgba(col, .5 * a); ctx.lineWidth = .8;
          ctx.beginPath(); ctx.moveTo(q.x - sp, q.y); ctx.lineTo(q.x + sp, q.y); ctx.moveTo(q.x, q.y - sp); ctx.lineTo(q.x, q.y + sp); ctx.stroke();
        }
        ctx.fillStyle = rgba([255, 255, 255], a);
        ctx.beginPath(); ctx.arc(q.x, q.y, r * .55, 0, 6.283); ctx.fill();
        ctx.fillStyle = rgba(col, a * .9);
        ctx.beginPath(); ctx.arc(q.x, q.y, r, 0, 6.283); ctx.fill();

        // pulse ring on the pipeline star and the hovered star
        if (named && (v.info.s === 'pipeline' || isHover) && q.e > .95 && !REDUCED) {
          var ph = (t * .7 + v.ph) % 1;
          ctx.strokeStyle = rgba(col, (1 - ph) * .6 * alpha); ctx.lineWidth = 1;
          ctx.beginPath(); ctx.arc(q.x, q.y, r + ph * 22, 0, 6.283); ctx.stroke();
        }
        // chart labels for the foundation stars
        if (named && v.info.label && q.e > .98 && W > 960) {
          ctx.font = '500 10px "JetBrains Mono", monospace';
          ctx.fillStyle = rgba(col, .75 * alpha);
          ctx.textAlign = v.i < 5 ? 'right' : 'left';
          ctx.fillText(v.info.label, q.x + (v.i < 5 ? -14 : 14), q.y + 3.5);
        }

        if (named && mouse.in) {
          var dd = Math.hypot(mouse.x - q.x, mouse.y - q.y);
          if (dd < best) { best = dd; hit = v; }
        }
        v.px = q.x; v.py = q.y;
      });

      if (hit !== hover && !COARSE) setHover(hit);
    }

    function hexRgb(h) { var n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }

    function setHover(v) {
      hover = v;
      canvas.style.cursor = v ? 'pointer' : (opts.constellation ? 'crosshair' : 'default');
      var card = opts.card;
      if (!card) return;
      if (!v) { card.classList.remove('is-on'); return; }
      var st = STATUS[v.info.s];
      card.style.setProperty('--c', st.color);
      card.innerHTML = '<span class="k"><i></i>' + st.label + '</span><b>' + v.info.name + '</b><p>' + v.info.line + '</p><span class="go">' + (COARSE ? 'Tap again to open →' : 'Click to explore →') + '</span>';
      var cw = card.offsetWidth || 280, ch = card.offsetHeight || 140;
      var x = v.px + 26, y = v.py - ch / 2;
      if (x + cw > W - 16) x = v.px - cw - 26;
      card.style.transform = '';
      card.style.left = clamp(x, 16, W - cw - 16) + 'px';
      card.style.top = clamp(y, 90, H - ch - 16) + 'px';
      card.classList.add('is-on');
    }

    function drawRipples(now) {
      ripples = ripples.filter(function (rp) { return now - rp.t < 1400; });
      ripples.forEach(function (rp) {
        var age = (now - rp.t) / 1000, r = age * 520;
        ctx.strokeStyle = 'rgba(156,200,236,' + (.35 * (1 - age / 1.4)) + ')'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.arc(rp.x, rp.y, r, 0, 6.283); ctx.stroke();
        ctx.strokeStyle = 'rgba(156,200,236,' + (.15 * (1 - age / 1.4)) + ')';
        ctx.beginPath(); ctx.arc(rp.x, rp.y, r * .6, 0, 6.283); ctx.stroke();
      });
    }

    function drawMeteors(t, dt) {
      if (t > nextMeteor) {
        nextMeteor = t + rand(3, 7);
        var ang = rand(.35, .65) + (Math.random() < .5 ? 0 : Math.PI - 1);
        meteors.push({ x: rand(.1, .9) * W, y: rand(0, .35) * H, vx: Math.cos(ang) * 900, vy: Math.sin(ang) * 900, life: 0, max: rand(.6, 1.1) });
      }
      meteors = meteors.filter(function (m) { return m.life < m.max; });
      meteors.forEach(function (m) {
        m.life += dt; m.x += m.vx * dt; m.y += m.vy * dt;
        var a = Math.sin(m.life / m.max * Math.PI);
        var tx = m.x - m.vx * .13, ty = m.y - m.vy * .13;
        var g = ctx.createLinearGradient(m.x, m.y, tx, ty);
        g.addColorStop(0, 'rgba(255,255,255,' + a + ')'); g.addColorStop(1, 'rgba(156,200,236,0)');
        ctx.strokeStyle = g; ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.moveTo(m.x, m.y); ctx.lineTo(tx, ty); ctx.stroke();
      });
    }

    // ── input ──
    function local(e) { var r = canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
    host.addEventListener('pointermove', function (e) {
      var l = local(e); mouse.x = l.x; mouse.y = l.y;
      if (!mouse.in) { mouse.sx = l.x; mouse.sy = l.y; }
      mouse.in = true;
    });
    host.addEventListener('pointerleave', function () { mouse.in = false; mouse.x = mouse.y = -9999; if (!COARSE) setHover(null); });
    canvas.addEventListener('pointerdown', function (e) {
      var l = local(e);
      // find a named star under the pointer
      var tgt = null, best = COARSE ? 34 : 22;
      vlist.forEach(function (v) { if (v.info && v.px != null) { var d = Math.hypot(l.x - v.px, l.y - v.py); if (d < best) { best = d; tgt = v; } } });
      if (tgt) {
        if (COARSE && hover !== tgt) { setHover(tgt); return; }
        if (opts.onPick) opts.onPick(tgt.info);
        return;
      }
      if (COARSE) setHover(null);
      if (!REDUCED) ripples.push({ x: l.x, y: l.y, t: performance.now() });
    });

    // ── lifecycle ──
    function start() { if (running) return; running = true; last = performance.now(); requestAnimationFrame(frame); }
    function stop() { running = false; }
    var io = new IntersectionObserver(function (es) { visible = es[0].isIntersecting; visible && !document.hidden ? start() : stop(); });
    io.observe(host);
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : (visible && start()); });
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(layout, 120); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);

    layout();
    start();
  }

  window.ArsenalSky = { create: createSky };
})();
