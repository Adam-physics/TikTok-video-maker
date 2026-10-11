(function () {
  'use strict';
  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  document.documentElement.classList.add('js');
  $('#yr').textContent = new Date().getFullYear();
  requestAnimationFrame(function () { document.body.classList.add('is-ready'); });

  /* ── nav: glass over the sky, solid over the page ── */
  var nav = $('#nav'), hero = $('.hero');
  function navState() { nav.classList.toggle('is-solid', hero.getBoundingClientRect().bottom < 90); }
  addEventListener('scroll', navState, { passive: true }); navState();
  var burger = $('#burger'), mnav = $('#mnav');
  burger.addEventListener('click', function () {
    var open = burger.getAttribute('aria-expanded') !== 'true';
    burger.setAttribute('aria-expanded', open); mnav.classList.toggle('is-open', open);
  });
  $$('a', mnav).forEach(function (a) { a.addEventListener('click', function () { burger.setAttribute('aria-expanded', 'false'); mnav.classList.remove('is-open'); }); });

  /* ── reveals + counters ── */
  function count(el) {
    var to = parseFloat(el.dataset.count), dec = +(el.dataset.dec || 0), pre = el.dataset.prefix || '', suf = el.dataset.suffix || '';
    if (REDUCED) { el.textContent = pre + to.toFixed(dec) + suf; return; }
    var t0 = performance.now(), dur = 1500;
    (function step(now) {
      var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 4);
      el.textContent = pre + (to * e).toFixed(dec) + suf;
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in'); io.unobserve(e.target);
      $$('[data-count]', e.target).forEach(count);
      if (e.target.matches('[data-count]')) count(e.target);
      var g = $('.growth', e.target); if (g) setTimeout(function () { g.classList.remove('pre'); }, 150);
    });
  }, { threshold: .2 });
  $('#growth').classList.add('pre');
  $$('.reveal').forEach(function (el) { io.observe(el); });

  /* ── hero star chart ── */
  function goTo(id) { var el = $(id); if (el) el.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth' }); }
  if (window.ArsenalSky) {
    ArsenalSky.create($('#sky'), {
      constellation: true, box: $('#chartBox'), card: $('#skyCard'),
      onPick: function (info) {
        if (info.k) selectPick(info.k);
        if (info.f) selectTab($('#ft-' + info.f));
        goTo(info.href);
      }
    });
    ArsenalSky.create($('#miniSky'), {});
  }
  var hint = $('.hero__hint');
  if (hint) $('.hero').addEventListener('pointermove', function once() { hint.style.opacity = '0'; $('.hero').removeEventListener('pointermove', once); });

  /* ── portfolio explorer (tabs) ── */
  var picks = $$('.pick'), title = $('#deviceTitle');
  function selectPick(k) {
    picks.forEach(function (p) {
      var on = p.dataset.k === k;
      p.setAttribute('aria-selected', on); p.tabIndex = on ? 0 : -1;
      var m = $('#mock-' + p.dataset.k); m.hidden = !on;
      if (on) { title.textContent = 'arsenal · ' + $('b', p).textContent.toLowerCase(); m.style.animation = 'none'; m.offsetHeight; m.style.animation = ''; }
    });
  }
  picks.forEach(function (p, i) {
    p.tabIndex = i ? -1 : 0;
    p.addEventListener('click', function () { selectPick(p.dataset.k); });
    p.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return; e.preventDefault();
      var n = picks[(i + d + picks.length) % picks.length]; n.focus(); selectPick(n.dataset.k);
    });
  });

  /* ── cross-sell flywheel ── */
  var NS = 'http://www.w3.org/2000/svg';
  var svg = $('#flySvg');
  var COS = ['Accounting AI', 'Family Office', 'Insurance', 'Implementation', 'Publishing', 'Legacy AI', 'Robotics'];
  var CHANNELS = [
    { name: 'Accountant', first: 0 }, { name: 'Attorney', first: 5 },
    { name: 'RIA', first: 1 }, { name: 'Insurance broker', first: 2 }
  ];
  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  var C = 260, RAD = 180, nodes = [], links = [];
  el('circle', { cx: C, cy: C, r: RAD, class: 'fl-orbit' }, svg);
  el('circle', { cx: C, cy: C, r: RAD * .55, class: 'fl-orbit' }, svg);
  COS.forEach(function (name, i) {
    var a = -Math.PI / 2 + i / COS.length * Math.PI * 2;
    var x = C + Math.cos(a) * RAD, y = C + Math.sin(a) * RAD;
    var path = el('path', { d: 'M' + C + ' ' + C + ' Q ' + (C + Math.cos(a + .5) * RAD * .5) + ' ' + (C + Math.sin(a + .5) * RAD * .5) + ' ' + x + ' ' + y, class: 'fl-link' }, svg);
    var len = path.getTotalLength(); path.style.strokeDasharray = len; path.style.strokeDashoffset = len; path.dataset.len = len;
    links.push(path);
    var g = el('g', { class: 'fl-node' }, svg);
    el('circle', { cx: x, cy: y, r: 26 }, g);
    el('path', { d: 'M' + x + ' ' + (y - 8) + ' L' + (x + 8) + ' ' + (y + 6) + ' L' + (x - 8) + ' ' + (y + 6) + ' Z', class: 'glyph' }, g);
    var lx = C + Math.cos(a) * (RAD + 46), ly = C + Math.sin(a) * (RAD + 46) + 4;
    var tx = el('text', { x: lx, y: ly, 'text-anchor': Math.abs(Math.cos(a)) < .3 ? 'middle' : (Math.cos(a) > 0 ? 'start' : 'end') }, g);
    if (Math.abs(Math.cos(a)) >= .3) tx.setAttribute('x', C + Math.cos(a) * (RAD + 34));
    tx.textContent = name;
    nodes.push(g);
  });
  var core = el('g', { class: 'fl-chan' }, svg);
  el('circle', { cx: C, cy: C, r: 62 }, core);
  var coreT = el('text', { x: C, y: C - 2, 'text-anchor': 'middle' }, core);
  var coreS = el('text', { x: C, y: C + 16, 'text-anchor': 'middle', style: 'font-weight:500;opacity:.7;font-size:11px' }, core);
  coreS.textContent = 'one relationship';
  var flyTimers = [];
  function flyTo(ci) {
    var ch = CHANNELS[ci];
    coreT.textContent = ch.name;
    flyTimers.forEach(clearTimeout); flyTimers = [];
    var order = [ch.first].concat(COS.map(function (_, i) { return i; }).filter(function (i) { return i !== ch.first; }));
    links.forEach(function (l) { l.classList.remove('on'); l.style.strokeDashoffset = l.dataset.len; });
    nodes.forEach(function (n) { n.classList.remove('on'); });
    var lines = $('#flyLines'); lines.textContent = '0';
    order.forEach(function (idx, k) {
      flyTimers.push(setTimeout(function () {
        links[idx].classList.add('on'); links[idx].style.strokeDashoffset = 0; nodes[idx].classList.add('on');
        lines.textContent = k + 1;
      }, REDUCED ? 0 : (k === 0 ? 150 : 650 + k * 170)));
    });
  }
  var chBtns = $$('#channels button');
  chBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      chBtns.forEach(function (x) { x.setAttribute('aria-checked', x === b); });
      flyTo(+b.dataset.c);
    });
  });
  var flyIO = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { flyTo(0); flyIO.disconnect(); } }, { threshold: .4 });
  flyIO.observe(svg);
  coreT.textContent = CHANNELS[0].name;

  /* ── studio model: sticky steps ── */
  var steps = $$('.step'), vis = $$('#panel .vis'), bars = $$('#panelBars i'), plabel = $('#panelLabel');
  // small screens get each visual inline under its step
  steps.forEach(function (s, i) {
    var holder = $('.step__vis-m', s), clone = vis[i].cloneNode(true);
    clone.classList.add('is-on'); holder.appendChild(clone);
  });
  function setStep(i) {
    steps.forEach(function (s, k) { s.classList.toggle('is-cur', k === i); });
    vis.forEach(function (v, k) { v.classList.toggle('is-on', k === i); });
    bars.forEach(function (b, k) { b.classList.toggle('on', k === i); });
    plabel.textContent = 'Step ' + (i + 1) + ' of 4';
  }
  var stepIO = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) setStep(+e.target.dataset.i); });
  }, { rootMargin: '-45% 0px -45% 0px' });
  steps.forEach(function (s) { stepIO.observe(s); });

  /* ── foundation tabs ── */
  var tabs = $$('#fTabs [role=tab]');
  function selectTab(t) {
    if (!t) return;
    tabs.forEach(function (x) {
      var on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
      $('#' + x.getAttribute('aria-controls')).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.tabIndex = i ? -1 : 0;
    t.addEventListener('click', function () { selectTab(t); });
    t.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return; var n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); selectTab(n);
    });
  });

  /* ── underwriting: weeks → days ── */
  var uw = $('#uwRange'), tl = $('#uwTimeline'), uwl = $('#uwLabel');
  function uwSet() {
    var v = uw.value / 100;
    uw.style.setProperty('--p', uw.value + '%');
    // sequential hand-offs (manual) collapse into overlapping automated work (platform)
    tl.style.setProperty('--step', (25 - v * 21) + '%');
    tl.style.setProperty('--w', (25 - v * 3) + '%');
    uwl.textContent = v < .34 ? 'Weeks' : v < .67 ? 'Weeks → Days' : 'Days';
  }
  uw.addEventListener('input', uwSet); uwSet();

  /* ── partner: deal structure ── */
  var DEALS = [
    { name: 'Full Acquisition', badge: 'Clean exit', keep: 4, keepL: 'A complete, well-run sale',
      desc: 'A complete, well-run sale for owners ready to move on. Fair process, diligence support, and a buyer who understands operations because we run our own.',
      terms: ['Cash and/or equity consideration', 'Diligence bandwidth support', 'Team and brand continuity commitments'] },
    { name: 'Majority + Earnout', badge: 'Most popular', keep: 42, keepL: 'Meaningful retained equity',
      desc: 'Sell the majority, keep a stake, and earn out on the growth we build together. The structure that aligns everyone on making AI transformation actually work.',
      terms: ['Meaningful retained equity', 'Earnout tied to real growth', 'You stay as much, or as little, as you want'] },
    { name: 'Partnership / JV', badge: 'No sale required', keep: 100, keepL: 'Full ownership stays with you',
      desc: 'Keep full ownership. We bring the AI capability, implementation muscle and capital; the venture shares in the upside it creates. Proof before commitment.',
      terms: ['Revenue-share or JV structures', 'AI roadmap built for your operation', 'A path to deeper partnership, if you want it'] }
  ];
  var dealBtns = $$('#deals button');
  function setDeal(i) {
    var d = DEALS[i];
    dealBtns.forEach(function (b, k) { b.setAttribute('aria-checked', k === i); });
    $('#dealName').textContent = d.name; $('#dealBadge').textContent = d.badge; $('#dealDesc').textContent = d.desc;
    $('#keepBar').style.width = d.keep + '%'; $('#keepLabel').textContent = d.keepL;
    $('#dealTerms').innerHTML = d.terms.map(function (t) { return '<li>' + t + '</li>'; }).join('');
  }
  dealBtns.forEach(function (b) { b.addEventListener('click', function () { setDeal(+b.dataset.d); }); });
  setDeal(1);
})();
