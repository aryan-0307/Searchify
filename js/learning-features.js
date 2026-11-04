/* Searchify learning upgrades: optional code trace, Big-O explorer, XP and mini challenge. */
(function () {
  'use strict';
  var STORAGE_KEY = 'searchify-learning-progress-v1';
  var progress = { xp: 0, completedRuns: 0, badges: [] };
  try { progress = Object.assign(progress, JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')); } catch (e) {}
  var root;
  function save() { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(progress)); } catch (e) {} }
  function escapeHTML(value) {
    return String(value == null ? '' : value).replace(/[&<>"]/g, function (c) {
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]);
    });
  }
  function complexitySVG(n) {
    var w = 620, h = 230, left = 42, bottom = 194, plotW = 550, plotH = 170;
    var series = [
      { name: 'O(1)', color: '#D93D81', fn: function(){return 1;}},
      { name: 'O(log n)', color: '#224D95', fn: function(x){return Math.log2(x);}},
      { name: 'O(n)', color: '#27845B', fn: function(x){return x;}},
      { name: 'O(n log n)', color: '#B47727', fn: function(x){return x*Math.log2(x);}},
      { name: 'O(n²)', color: '#8055A5', fn: function(x){return x*x;}}
    ];
    var max = series[4].fn(20);
    var html = '<svg viewBox="0 0 '+w+' '+h+'" role="img" aria-label="Big O growth curves for constant, logarithmic, linear, linearithmic and quadratic time">';
    [0,0.25,0.5,0.75,1].forEach(function(t){
      var y = bottom - t*plotH;
      html += '<line x1="'+left+'" y1="'+y+'" x2="'+(left+plotW)+'" y2="'+y+'" stroke="#D8D5C9" stroke-dasharray="3 5"/>';
    });
    html += '<path d="M'+left+' '+(bottom-plotH)+' V'+bottom+' H'+(left+plotW)+'" fill="none" stroke="#686868"/>';
    series.forEach(function(s){
      var d = '';
      for (var x=1;x<=20;x++) {
        var px = left + (x-1)/19*plotW;
        var py = bottom - s.fn(x)/max*plotH;
        d += (x===1?'M':' L')+px.toFixed(1)+' '+py.toFixed(1);
      }
      html += '<path d="'+d+'" fill="none" stroke="'+s.color+'" stroke-width="3" stroke-linecap="round"/>';
    });
    html += '<text x="'+left+'" y="218" font-size="11" fill="#686868">1</text><text x="'+(left+plotW-10)+'" y="218" font-size="11" fill="#686868">20</text><text x="300" y="228" font-size="11" fill="#686868">Input size (n)</text></svg>';
    html += '<div class="sf-curve-legend">'+series.map(function(s){return '<span><i style="background:'+s.color+'"></i>'+s.name+'</span>';}).join('')+'</div>';
    return html;
  }
  function updateProgress() {
    var level = Math.floor(progress.xp / 100) + 1;
    var xpInLevel = progress.xp % 100;
    var xp = root.querySelector('#sf-xp');
    var levelEl = root.querySelector('#sf-level');
    var fill = root.querySelector('#sf-xp-fill');
    var badges = root.querySelector('#sf-badges');
    if (xp) xp.textContent = progress.xp + ' XP';
    if (levelEl) levelEl.textContent = 'Level ' + level;
    if (fill) fill.style.width = xpInLevel + '%';
    if (badges) badges.innerHTML = (progress.badges.length ? progress.badges : ['First Run']).map(function(b){return '<span class="sf-badge">'+escapeHTML(b)+'</span>';}).join('');
  }
  function awardRun() {
    if (root.dataset.awarded === 'yes') return;
    root.dataset.awarded = 'yes';
    progress.xp += 25;
    progress.completedRuns += 1;
    var newBadge = progress.completedRuns === 1 ? 'First Finish' : (progress.completedRuns === 5 ? '5 Runs' : (progress.completedRuns === 10 ? '10 Runs' : null));
    if (newBadge && progress.badges.indexOf(newBadge) === -1) progress.badges.push(newBadge);
    save(); updateProgress();
    var note = root.querySelector('#sf-xp-note');
    if (note) note.textContent = '+25 XP earned — run completed!';
  }
  function renderCodeTrace(detail) {
    var panel = root.querySelector('#sf-code-lines');
    if (!panel) return;
    var algorithm = detail.algorithm;
    var lines = [];
    var library = algorithm.indexOf('Sort') !== -1 ? window.SortingAlgorithms : window.SearchingAlgorithms;
    if (library && library.pseudocode) lines = library.pseudocode[algorithm] || [];
    if (!lines.length) {
      panel.innerHTML = '<p class="sf-muted">Code trace is not available for this algorithm yet.</p>';
      return;
    }
    var active = Number(detail.step && detail.step.pseudocodeLine);
    panel.innerHTML = lines.map(function(line, index) {
      return '<div class="sf-code-line '+(index===active?'active':'')+'"><span>'+(index+1)+'</span><code>'+escapeHTML(line)+'</code></div>';
    }).join('');
    var current = panel.querySelector('.active');
    if (current && current.scrollIntoView) current.scrollIntoView({block:'nearest'});
  }
  function renderStep(event) {
    var detail = event.detail || {};
    root.dataset.awarded = 'no';
    renderCodeTrace(detail);
    var count = root.querySelector('#sf-step-label');
    if (count) count.textContent = 'Step ' + (detail.currentStep + 1) + ' of ' + detail.totalSteps;
    if (detail.currentStep === detail.totalSteps - 1) awardRun();
  }
  function init() {
    var main = document.querySelector('.viz-content-container');
    if (!main) return;
    root = document.createElement('section');
    root.className = 'sf-learning-lab';
    root.innerHTML =
      '<div class="sf-lab-heading"><span class="sf-eyebrow">LEARN BY DOING</span><h2>Your algorithm learning lab</h2><p>Track progress, inspect the active code line, and compare how algorithms grow as input gets larger.</p></div>'+
      '<div class="sf-lab-grid">'+
        '<article class="sf-lab-card sf-progress-card"><div class="sf-card-top"><h3>Your progress</h3><span id="sf-level">Level 1</span></div><strong id="sf-xp">0 XP</strong><div class="sf-xp-track"><span id="sf-xp-fill"></span></div><div id="sf-badges" class="sf-badges"></div><p id="sf-xp-note" class="sf-muted">Complete a visualization to earn 25 XP.</p></article>'+
        '<article class="sf-lab-card sf-challenge-card"><div class="sf-card-top"><h3>Mini challenge</h3><span class="sf-challenge-tag">QUICK PRACTICE</span></div><p>Sort this array in ascending order using the custom array input above:</p><div class="sf-challenge-array">8 · 3 · 6 · 1 · 5</div><button type="button" id="sf-load-challenge">Load challenge array</button><p class="sf-muted">Choose an algorithm, then step through the solution.</p></article>'+
      '</div>'+
      '<article class="sf-lab-card sf-trace-card"><div class="sf-card-top"><h3>Live code trace</h3><span id="sf-step-label">Waiting for a step</span></div><details><summary>Show code trace (optional)</summary><div id="sf-code-lines" class="sf-code-lines"><p class="sf-muted">Start a visualization to highlight the active pseudocode line.</p></div></details></article>'+
      '<article class="sf-lab-card sf-complexity-card"><div class="sf-card-top"><h3>Big-O growth explorer</h3><span>Illustrative growth · not benchmark timings</span></div><p class="sf-muted">Compare common time-complexity families as input size increases.</p><div id="sf-complexity-plot">'+complexitySVG(20)+'</div><label class="sf-n-control" for="sf-n-slider">Input size: <strong id="sf-n-value">20</strong><input id="sf-n-slider" type="range" min="1" max="20" value="20"></label><p id="sf-complexity-caption" class="sf-muted">At n = 20, quadratic growth rises much faster than linear growth.</p></article>';
    main.appendChild(root);
    updateProgress();
    root.querySelector('#sf-load-challenge').addEventListener('click', function(){
      var input = document.getElementById('custom-array');
      if (input) { input.value = '8, 3, 6, 1, 5'; input.focus(); }
      var note = root.querySelector('#sf-xp-note');
      if (note) note.textContent = 'Challenge loaded. Press Apply above to begin.';
    });
    root.querySelector('#sf-n-slider').addEventListener('input', function(){
      var n = Number(this.value);
      root.querySelector('#sf-n-value').textContent = n;
      root.querySelector('#sf-complexity-caption').textContent = 'At n = '+n+', compare the relative growth of the five complexity families. The curves are normalized for learning.';
    });
    window.addEventListener('searchify:step', renderStep);
    window.addEventListener('searchify:run-reset', function(){ root.dataset.awarded = 'no'; });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();