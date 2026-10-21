(function () {
  'use strict';
  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var el = Mark.el;

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
  function goTo(id) { var n = $(id); if (n) n.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth' }); }
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

  /* ── what we build: each company is a star, each star runs a workflow ── */
  var A = 'agent', P = 'human';
  var COMPANIES = {
    accounting: { name: 'AI for Accountants', line: 'Software that runs an accounting firm. The agent prepares; the partner signs.',
      wf: [['Bank feeds in', A], ['Reconcile accounts', A], ['Match invoices', A], ['Draft statements', A], ['Partner review', P], ['Sign-off', P]] },
    mfo: { name: 'Multi-Family Office Platform', line: 'One AI tool unifying accounting, legal, insurance and wealth for a family.',
      wf: [['Client asks a question', P], ['Pull the books', A], ['Check legal & insurance', A], ['Model the wealth impact', A], ['Draft one answer', A], ['Advisor approves', P]] },
    insurance: { name: 'AI Insurance Servicing', line: 'Policy management, autopay, life settlements on-chain and life-expectancy analysis.',
      wf: [['Policy onboarded', A], ['Premiums on autopay', A], ['Life-expectancy analysis', A], ['Settlement recorded on-chain', A], ['Servicing team review', P]] },
    implementation: { name: 'AI Implementation', line: 'A build-grow-sell practice for businesses adopting AI.',
      wf: [['Owner sets the goal', P], ['Map the workflows', A], ['Deploy agents', A], ['Move AI into the offering', A], ['Grow, or sell', P]] },
    publishing: { name: 'Publishing & Marketing', line: 'AI-native content and agencies that ship at the speed of software.',
      wf: [['Editor sets the brief', P], ['Research', A], ['Draft', A], ['Edit & approve', P], ['Publish & distribute', A]] },
    twins: { name: 'Digital Twins / Legacy AI', line: 'Human expertise turned into lasting intelligence.',
      wf: [['Expert interviews', P], ['Capture decisions', A], ['Train the twin', A], ['Answer new questions', A], ['Expert reviews', P]] },
    robotics: { name: 'Agentic Entities & Robotics', line: 'Autonomous builders, and service and advertising robots.',
      wf: [['Task assigned', P], ['Builder agent plans', A], ['Autonomous build', A], ['Robots deploy', A], ['Approve the next task', P]] }
  };
  var ORDER = Object.keys(COMPANIES);
  var buildMark = Mark.create($('#buildMark'), { cls: 'mk--chart', pad: 50 });
  var picks = $$('.pick');
  function selectPick(k) {
    var c = COMPANIES[k]; if (!c) return;
    picks.forEach(function (p) { var on = p.dataset.k === k; p.setAttribute('aria-selected', on); p.tabIndex = on ? 0 : -1; if (on) $('#chart').setAttribute('aria-labelledby', p.id); });
    buildMark.svg.setAttribute('data-sel', k);
    $$('.mk__s--named', buildMark.svg).forEach(function (s) { s.classList.toggle('is-sel', s.dataset.id === k); });
    $('#chartCoord').textContent = 'Company ' + (ORDER.indexOf(k) + 1) + ' of 7 · AI-native build';
    $('#chartName').textContent = c.name; $('#chartLine').textContent = c.line;
    var wf = $('#wf'); wf.innerHTML = '';
    c.wf.forEach(function (s, i) {
      var li = document.createElement('li'); li.className = 'wf__n wf__n--' + s[1]; li.style.setProperty('--i', i);
      li.innerHTML = '<span class="wf__dot"></span><span class="wf__t"></span><span class="wf__who">' + (s[1] === A ? 'Agent' : 'Person') + '</span>';
      li.querySelector('.wf__t').textContent = s[0]; wf.appendChild(li);
    });
    wf.style.setProperty('--n', c.wf.length);
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
  // clicking a company star in the chart selects it too
  $$('.mk__s--named', buildMark.svg).forEach(function (s) { if (COMPANIES[s.dataset.id]) s.addEventListener('click', function () { selectPick(s.dataset.id); }); });
  selectPick('accounting');

  /* ── cross-sell: one relationship lights up the whole mark ── */
  var flyMark = Mark.create($('#flyFig'), { cls: 'mk--fly', pad: 50 });
  var fsvg = flyMark.svg; fsvg.setAttribute('viewBox', '-380 -70 1080 900');
  var CH = [-250, 620], gLinks = el('g', { class: 'fly__links' }), stars = $('.mk__stars', fsvg);
  fsvg.insertBefore(gLinks, stars);
  var LABEL = { accounting: 'Accounting AI', mfo: 'Family Office', insurance: 'Insurance', implementation: 'Implementation', twins: 'Legacy AI', publishing: 'Publishing', robotics: 'Robotics' };
  var links = {}, labels = {};
  ORDER.forEach(function (id) {
    var p = flyMark.P(id), dx = p[0] - CH[0], dy = p[1] - CH[1], mx = (CH[0] + p[0]) / 2 + dy * .18, my = (CH[1] + p[1]) / 2 - dx * .18;
    var path = el('path', { d: 'M' + CH[0] + ' ' + CH[1] + ' Q' + mx + ' ' + my + ' ' + p[0] + ' ' + p[1], class: 'fly__link' }, gLinks);
    var len = path.getTotalLength(); path.style.strokeDasharray = len; path.style.strokeDashoffset = len; path.dataset.len = len;
    links[id] = path;
    var right = p[0] > 320, t = el('text', { x: p[0] + (right ? 30 : -30), y: p[1] + 8, 'text-anchor': right ? 'start' : 'end', class: 'fly__label' }, fsvg);
    t.textContent = LABEL[id]; labels[id] = t;
  });
  var chG = el('g', { class: 'fly__chan', transform: 'translate(' + CH.join(' ') + ')' }, fsvg);
  el('circle', { r: 46, class: 'fly__chan-halo' }, chG); el('circle', { r: 16, class: 'fly__chan-dot' }, chG);
  var chName = el('text', { y: 86, 'text-anchor': 'middle', class: 'fly__chan-name' }, chG);
  var chSub = el('text', { y: 118, 'text-anchor': 'middle', class: 'fly__chan-sub' }, chG); chSub.textContent = 'one relationship';
  var CHANNELS = [{ name: 'Accountant', first: 'accounting' }, { name: 'Attorney', first: 'twins' }, { name: 'RIA', first: 'mfo' }, { name: 'Insurance broker', first: 'insurance' }];
  var flyTimers = [];
  function flyTo(ci) {
    var ch = CHANNELS[ci]; chName.textContent = ch.name;
    flyTimers.forEach(clearTimeout); flyTimers = [];
    var order = [ch.first].concat(ORDER.filter(function (i) { return i !== ch.first; }));
    ORDER.forEach(function (id) { links[id].classList.remove('on'); links[id].style.strokeDashoffset = links[id].dataset.len; labels[id].classList.remove('on'); flyMark.star(id).classList.remove('is-lit'); });
    fsvg.classList.remove('is-full');
    var lines = $('#flyLines'); lines.textContent = '0';
    order.forEach(function (id, k) {
      flyTimers.push(setTimeout(function () {
        links[id].classList.add('on'); links[id].style.strokeDashoffset = 0; labels[id].classList.add('on'); flyMark.star(id).classList.add('is-lit');
        lines.textContent = k + 1; if (k === order.length - 1) fsvg.classList.add('is-full');
      }, REDUCED ? 0 : (k === 0 ? 150 : 700 + k * 200)));
    });
  }
  var chBtns = $$('#channels button');
  chBtns.forEach(function (b) { b.addEventListener('click', function () { chBtns.forEach(function (x) { x.setAttribute('aria-checked', x === b); }); flyTo(+b.dataset.c); }); });
  var flyIO = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { flyTo(0); flyIO.disconnect(); } }, { threshold: .35 });
  flyIO.observe(fsvg); chName.textContent = CHANNELS[0].name;

  /* ── studio model: the mark builds itself, one move per step ── */
  var CAPS = ['A new company joins the mark', 'Agents go to work inside it', 'It connects to every neighbor', 'The whole mark compounds · ADHI, audited and public'];
  var MOVES = ['Build', 'Embed', 'Scale', 'Compound'];
  function studioMark(host, step) {
    var m = Mark.create(host, { cls: 'mk--studio', pad: 60 });
    var p = m.P('twins'), orbit = el('g', { class: 'mk__orbit', transform: 'translate(' + p.join(' ') + ')' });
    for (var i = 0; i < 3; i++) el('circle', { r: 6, cx: 46, cy: 0, style: '--o:' + i, class: 'mk__agent' }, orbit);
    m.svg.appendChild(orbit);
    m.svg.setAttribute('data-step', step); return m;
  }
  var studio = studioMark($('#studioMark'), 0);
  var steps = $$('.step'), bars = $$('#panelBars i');
  steps.forEach(function (s, i) { studioMark($('.step__vis-m', s), i); });
  function setStep(i) {
    steps.forEach(function (s, k) { s.classList.toggle('is-cur', k === i); });
    bars.forEach(function (b, k) { b.classList.toggle('on', k === i); });
    studio.svg.setAttribute('data-step', i);
    $('#panelLabel').textContent = 'Step ' + (i + 1) + ' of 4 · ' + MOVES[i];
    $('#panelCap').textContent = CAPS[i];
  }
  // the visual always matches the step whose heading sits closest to the panel's middle
  var panel = $('#panel'), curStep = 0, stepTick = false;
  function syncStep() {
    stepTick = false;
    if (!panel.offsetParent) return;
    var pr = panel.getBoundingClientRect(), mid = Math.min(pr.top + pr.height / 2, innerHeight / 2), best = 0, bestD = Infinity;  // before the panel sticks, use the screen's middle
    steps.forEach(function (s, k) { var h = $('h3', s).getBoundingClientRect(), d = Math.abs(h.top + h.height / 2 - mid); if (d < bestD) { bestD = d; best = k; } });
    if (best !== curStep) { curStep = best; setStep(best); }
  }
  addEventListener('scroll', function () { if (!stepTick) { stepTick = true; requestAnimationFrame(syncStep); } }, { passive: true });
  addEventListener('resize', syncStep);
  syncStep();

  /* ── foundation: the two feet of the A ── */
  var footMark = Mark.create($('#footMark'), { cls: 'mk--feet', pad: 60 });
  var tabs = $$('#fTabs [role=tab]');
  function selectTab(t) {
    if (!t) return;
    tabs.forEach(function (x) { var on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; $('#' + x.getAttribute('aria-controls')).hidden = !on; });
    footMark.svg.setAttribute('data-sel', t.dataset.id);
  }
  tabs.forEach(function (t, i) {
    t.tabIndex = i ? -1 : 0;
    t.addEventListener('click', function () { selectTab(t); });
    t.addEventListener('keydown', function (e) { var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!d) return; var n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); selectTab(n); });
  });
  selectTab(tabs[0]);

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
