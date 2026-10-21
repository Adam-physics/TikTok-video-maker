/* The Arsenal mark as an SVG constellation, shared by every section below the hero.
   Same lattice as the logo file (and the hero canvas): each vertex is a star, each facet
   edge a line, and the eleven named stars are the businesses in the portfolio. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var DX = 64.068, DY = 93.766, W = 640.68, H = 750.13;
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
  // the eleven named stars: the shared stack at the apex, seven companies on the facets,
  // the two operating businesses as the feet, and the next vertical as the violet tip
  var IDS = { platform: '5,0', accounting: '3,2', mfo: '7,2', insurance: '1,4', implementation: '9,4', twins: '5,4',
    publishing: '2,7', robotics: '8,7', energy: '0,5', finance: '10,5', health: '5,6' };
  var NAME = {};
  Object.keys(IDS).forEach(function (id) { NAME[IDS[id]] = id; });

  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var a in attrs) e.setAttribute(a, attrs[a]); if (parent) parent.appendChild(e); return e; }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function rgb(c) { return 'rgb(' + c.map(Math.round).join(',') + ')'; }
  var ICE = [156, 200, 236], FACET = [110, 143, 214], DEEP = [59, 71, 166], TIP = [139, 92, 246], WHITE = [233, 238, 249];
  function pt(k) { var p = k.split(','); return [p[0] * DX, p[1] * DY]; }

  /** create(host, { pad, cls }) → { svg, P(id), star(id) } */
  function create(host, o) {
    o = o || {};
    var pad = o.pad == null ? 40 : o.pad;
    var svg = el('svg', { viewBox: [-pad, -pad, W + pad * 2, H + pad * 2].join(' '), class: 'mk ' + (o.cls || ''), 'aria-hidden': 'true', focusable: 'false' });
    var gF = el('g', { class: 'mk__facets' }, svg), gE = el('g', { class: 'mk__edges' }, svg), gS = el('g', { class: 'mk__stars' }, svg);
    var verts = {}, edges = {};
    TRIS.forEach(function (tr) {
      var ks = tr.slice(1).map(function (p) { return p[0] + ',' + p[1]; });
      var pts = ks.map(pt), cx = (pts[0][0] + pts[1][0] + pts[2][0]) / 3 / W, cy = (pts[0][1] + pts[1][1] + pts[2][1]) / 3 / H;
      var g = Math.min(1, cx * .65 + cy * .35), col = tr[0] === 't' ? TIP : g < .5 ? mix(ICE, FACET, g * 2) : mix(FACET, DEEP, (g - .5) * 2);
      if (tr[0] === 'b') col = mix(col, WHITE, .18);
      var cls = 'mk__f mk__f--' + tr[0];
      ks.forEach(function (k) { verts[k] = 1; if (NAME[k]) cls += ' has-' + NAME[k]; });
      el('polygon', { points: pts.map(function (p) { return p.join(','); }).join(' '), fill: rgb(col), class: cls }, gF);
      for (var i = 0; i < 3; i++) { var a = ks[i], b = ks[(i + 1) % 3], key = a < b ? a + '|' + b : b + '|' + a; edges[key] = [a, b]; }
    });
    Object.keys(edges).forEach(function (key) {
      var a = edges[key][0], b = edges[key][1], pa = pt(a), pb = pt(b), cls = 'mk__e';
      [a, b].forEach(function (k) { if (NAME[k]) cls += ' to-' + NAME[k]; });
      if (pt(a)[1] >= 6 * DY && pt(b)[1] >= 6 * DY && Math.abs(pa[0] - W / 2) <= 2.1 * DX && Math.abs(pb[0] - W / 2) <= 2.1 * DX) cls += ' mk__e--tip';
      el('line', { x1: pa[0], y1: pa[1], x2: pb[0], y2: pb[1], class: cls }, gE);
    });
    Object.keys(verts).forEach(function (k) {
      var p = pt(k), id = NAME[k], g = el('g', { class: 'mk__s' + (id ? ' mk__s--named mk__s--' + id : ''), transform: 'translate(' + p[0] + ' ' + p[1] + ')' }, gS);
      if (id) { g.setAttribute('data-id', id); el('circle', { r: 30, class: 'mk__halo' }, g); el('circle', { r: 17, class: 'mk__ring' }, g); }
      el('circle', { r: id ? 9 : 4.5, class: 'mk__dot' }, g);
    });
    host.appendChild(svg);
    return {
      svg: svg,
      P: function (id) { return pt(IDS[id] || id); },
      star: function (id) { return gS.querySelector('[data-id="' + id + '"]'); },
      size: [W, H]
    };
  }

  window.Mark = { create: create, IDS: IDS, el: el };
})();
