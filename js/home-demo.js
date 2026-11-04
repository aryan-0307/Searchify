/* Searchify homepage quick-sort demo */
(function () {
  'use strict';
  var values = [72, 28, 91, 43, 16, 64, 35, 80];
  var timer = null;
  var busy = false;
  var root;
  function render(activeA, activeB, sorted) {
    var bars = root.querySelector('#home-demo-bars');
    bars.innerHTML = '';
    var max = Math.max.apply(null, values);
    values.forEach(function(value, index) {
      var bar = document.createElement('div');
      bar.className = 'home-demo-bar';
      if (sorted && sorted.indexOf(index) !== -1) bar.classList.add('is-sorted');
      if (index === activeA || index === activeB) bar.classList.add('is-active');
      bar.style.height = (value / max * 100) + '%';
      bar.innerHTML = '<span>' + value + '</span>';
      bars.appendChild(bar);
    });
  }
  function status(message) { root.querySelector('#home-demo-status').textContent = message; }
  function stop() { if (timer) clearTimeout(timer); timer = null; busy = false; root.querySelector('#home-demo-run').disabled = false; }
  function shuffle() {
    stop();
    for (var i=values.length-1;i>0;i--) {
      var j=Math.floor(Math.random()*(i+1)), t=values[i]; values[i]=values[j]; values[j]=t;
    }
    render(-1,-1,[]);
    status('Fresh array ready. Press Run Bubble Sort!');
  }
  function run() {
    if (busy) return;
    busy = true;
    root.querySelector('#home-demo-run').disabled = true;
    var arr = values.slice(), i=0, j=0, pass=0;
    function tick() {
      if (i >= arr.length-1) {
        values = arr.slice(); render(-1,-1,arr.map(function(_,k){return k;}));
        status('Sorted! Bubble Sort finished this 8-element array.');
        stop(); return;
      }
      if (j >= arr.length-1-pass) { i++; pass++; j=0; tick(); return; }
      render(j,j+1,[]);
      status('Comparing ' + arr[j] + ' and ' + arr[j+1]);
      if (arr[j] > arr[j+1]) {
        var t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;
        values=arr.slice();
        timer=setTimeout(function(){render(j,j+1,[]);status('Swapped! ' + arr[j] + ' and ' + arr[j+1]);j++;timer=setTimeout(tick,360);},360);
      } else { j++; timer=setTimeout(tick,360); }
    }
    tick();
  }
  function init() {
    root=document.querySelector('.home-quick-demo');
    if (!root) return;
    render(-1,-1,[]);
    root.querySelector('#home-demo-run').addEventListener('click',run);
    root.querySelector('#home-demo-shuffle').addEventListener('click',shuffle);
    window.addEventListener('beforeunload',stop);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();