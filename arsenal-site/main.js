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

  /* ── reveals ── */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: .15 });
  $$('.reveal').forEach(function (n) { io.observe(n); });

  /* ── hero star chart ── */
  if (window.ArsenalSky) {
    ArsenalSky.create($('#sky'), { constellation: true, named: false, box: $('#chartBox') });
    ArsenalSky.create($('#miniSky'), {});
  }

  /* ── what we build: a typical job at each company ── */
  var A = 'agent', P = 'human';
  var COMPANIES = {
    accounting: { name: 'AI for Accountants', line: 'Software that runs an accounting firm. The agent prepares; the partner signs.', task: 'Month-end close',
      wf: [['Bank feeds in', A], ['Reconcile accounts', A], ['Match invoices', A], ['Draft statements', A], ['Partner review', P], ['Sign-off', P]] },
    mfo: { name: 'Multi-Family Office Platform', line: 'One AI tool unifying accounting, legal, insurance and wealth for a family.', task: 'A client asks: “What happens to my estate if I sell this year?”',
      wf: [['Client asks a question', P], ['Pull the books', A], ['Check legal & insurance', A], ['Model the wealth impact', A], ['Draft one answer', A], ['Advisor approves', P]] },
    insurance: { name: 'AI Insurance Servicing', line: 'Policy management, autopay, life settlements on-chain and life-expectancy analysis.', task: 'Servicing a life policy',
      wf: [['Policy onboarded', A], ['Premiums on autopay', A], ['Life-expectancy analysis', A], ['Settlement recorded on-chain', A], ['Servicing team review', P]] },
    implementation: { name: 'AI Implementation', line: 'A build-grow-sell practice for businesses adopting AI.', task: 'Bringing AI into an owner’s business',
      wf: [['Owner sets the goal', P], ['Map the workflows', A], ['Deploy agents', A], ['Move AI into the offering', A], ['Grow, or sell', P]] },
    publishing: { name: 'Publishing & Marketing', line: 'AI-native content and agencies that ship at the speed of software.', task: 'A week of client content',
      wf: [['Editor sets the brief', P], ['Research', A], ['Draft', A], ['Edit & approve', P], ['Publish & distribute', A]] },
    twins: { name: 'Digital Twins / Legacy AI', line: 'Human expertise turned into lasting intelligence.', task: 'Capturing a founder’s judgment',
      wf: [['Expert interviews', P], ['Capture decisions', A], ['Train the twin', A], ['Answer new questions', A], ['Expert reviews', P]] },
    robotics: { name: 'Agentic Entities & Robotics', line: 'Autonomous builders, and service and advertising robots.', task: 'An autonomous build',
      wf: [['Task assigned', P], ['Builder agent plans', A], ['Autonomous build', A], ['Robots deploy', A], ['Approve the next task', P]] }
  };
  var ORDER = Object.keys(COMPANIES);
  var picks = $$('.pick');
  function selectPick(k) {
    var c = COMPANIES[k]; if (!c) return;
    picks.forEach(function (p) { var on = p.dataset.k === k; p.setAttribute('aria-selected', on); p.tabIndex = on ? 0 : -1; if (on) $('#chart').setAttribute('aria-labelledby', p.id); });
    $('#chartName').textContent = c.name; $('#chartLine').textContent = c.line; $('#jobTask').textContent = c.task;
    var agents = c.wf.filter(function (s) { return s[1] === A; }).length;
    $('#jobSplit').innerHTML = '<b>' + agents + ' of ' + c.wf.length + '</b> steps by agents';
    var wf = $('#wf'); wf.innerHTML = '';
    c.wf.forEach(function (s, i) {
      var li = document.createElement('li'); li.className = 'wf__n wf__n--' + s[1]; li.style.setProperty('--i', i);
      li.innerHTML = '<span class="wf__num">' + (i + 1) + '</span><span class="wf__t"></span><span class="wf__who">' + (s[1] === A ? 'Agent' : 'Person') + '</span>';
      li.querySelector('.wf__t').textContent = s[0]; wf.appendChild(li);
    });
    wf.classList.remove('run'); void wf.offsetWidth; wf.classList.add('run');
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
  selectPick('accounting');

  /* ── cross-sell: one relationship, every company ── */
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var a in attrs) e.setAttribute(a, attrs[a]); if (parent) parent.appendChild(e); return e; }
  var svg = $('#flySvg'), C = 280, RAD = 205;
  var COS = ['Accounting AI', 'Family Office', 'Insurance', 'Implementation', 'Publishing', 'Legacy AI', 'Robotics'];
  var CHANNELS = [{ name: 'Accountant', first: 0 }, { name: 'Attorney', first: 5 }, { name: 'RIA', first: 1 }, { name: 'Insurance broker', first: 2 }];
  el('circle', { cx: C, cy: C, r: RAD, class: 'fl-orbit' }, svg);
  var links = [], nodes = [];
  COS.forEach(function (name, i) {
    var a = -Math.PI / 2 + i / COS.length * Math.PI * 2, x = C + Math.cos(a) * RAD, y = C + Math.sin(a) * RAD;
    var path = el('path', { d: 'M' + C + ' ' + C + ' L' + x + ' ' + y, class: 'fl-link' }, svg);
    var len = path.getTotalLength(); path.style.strokeDasharray = len; path.style.strokeDashoffset = len; path.dataset.len = len;
    links.push(path);
    var g = el('g', { class: 'fl-node', transform: 'translate(' + x + ' ' + y + ')' }, svg);
    var w = Math.max(112, name.length * 10.4 + 34);
    el('rect', { x: -w / 2, y: -21, width: w, height: 42, rx: 21 }, g);
    var t = el('text', { y: 6, 'text-anchor': 'middle' }, g); t.textContent = name;
    nodes.push(g);
  });
  var core = el('g', { class: 'fl-core' }, svg);
  el('circle', { cx: C, cy: C, r: 70 }, core);
  var coreT = el('text', { x: C, y: C + 2, 'text-anchor': 'middle', class: 'fl-core__name' }, core);
  var coreS = el('text', { x: C, y: C + 24, 'text-anchor': 'middle', class: 'fl-core__sub' }, core); coreS.textContent = 'one relationship';
  var flyTimers = [];
  function flyTo(ci) {
    var ch = CHANNELS[ci]; coreT.textContent = ch.name;
    flyTimers.forEach(clearTimeout); flyTimers = [];
    var order = [ch.first].concat(COS.map(function (_, i) { return i; }).filter(function (i) { return i !== ch.first; }));
    links.forEach(function (l) { l.classList.remove('on'); l.style.strokeDashoffset = l.dataset.len; });
    nodes.forEach(function (n) { n.classList.remove('on'); });
    var lines = $('#flyLines'); lines.textContent = '0';
    order.forEach(function (idx, k) {
      flyTimers.push(setTimeout(function () {
        links[idx].classList.add('on'); links[idx].style.strokeDashoffset = 0; nodes[idx].classList.add('on'); lines.textContent = k + 1;
      }, REDUCED ? 0 : (k === 0 ? 150 : 650 + k * 180)));
    });
  }
  var chBtns = $$('#channels button');
  chBtns.forEach(function (b) { b.addEventListener('click', function () { chBtns.forEach(function (x) { x.setAttribute('aria-checked', x === b); }); flyTo(+b.dataset.c); }); });
  var flyIO = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { flyTo(0); flyIO.disconnect(); } }, { threshold: .35 });
  flyIO.observe(svg); coreT.textContent = CHANNELS[0].name;

  /* ── foundation tabs ── */
  var tabs = $$('#fTabs [role=tab]');
  function selectTab(t) {
    if (!t) return;
    tabs.forEach(function (x) { var on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; $('#' + x.getAttribute('aria-controls')).hidden = !on; });
  }
  tabs.forEach(function (t, i) {
    t.tabIndex = i ? -1 : 0;
    t.addEventListener('click', function () { selectTab(t); });
    t.addEventListener('keydown', function (e) { var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!d) return; var n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); selectTab(n); });
  });

  /* ── underwriting: weeks → days ── */
  var uw = $('#uwRange'), tl = $('#uwTimeline'), uwl = $('#uwLabel');
  function uwSet() {
    var v = uw.value / 100;
    uw.style.setProperty('--p', uw.value + '%');
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
