/* ============================================
   Searchify — Sorting Visualizer Controller (Full-Width Edition)
   ============================================ */
(function () {
    'use strict';

    /* ---------- state ---------- */
    var currentAlgorithm = 'bubbleSort';
    var currentArray = [];
    var originalArray = [];
    var steps = [];
    var currentStep = 0;
    var isPlaying = false;
    var playTimer = null;
    var speed = 800;          // ms between steps (1x default)
    var sortOrder = 'asc';
    var arraySize = 15;

    /* ---------- DOM cache ---------- */
    var el = {};

    function getUsableAreaHeight(areaEl) {
        var rawHeight = (areaEl && areaEl.clientHeight > 120) ? areaEl.clientHeight : 440;
        if (window.innerWidth <= 768) {
            // Mobile viewport clearance:
            // Status pill is at top: 14px; height: ~28px (bottom ~42px).
            // Legend is placed UNDER the visualizer area, so it no longer takes canvas top space.
            // Reserved space for status pill (~42px) + buffer (~30px) + label (~22px) + bottom padding (~36px) = 130px.
            // Guarantees highest bar + label stays strictly lower than status pill, with legend under canvas.
            var reservedSpace = 144;
            var minH = 110;
            return Math.max(minH, rawHeight - reservedSpace);
        }
        return Math.max(200, rawHeight - 116);
    }

    function cacheElements() {
        el.vizArea = document.getElementById('visualization-area');
        el.algoSelect = document.getElementById('algorithm-select');
        el.generateBtn = document.getElementById('generate-btn');
        el.customInput = document.getElementById('custom-array');
        el.applyCustomBtn = document.getElementById('apply-custom-btn');
        el.sizeSlider = document.getElementById('array-size');
        el.sizeValue = document.getElementById('size-value');
        el.speedSlider = document.getElementById('speed-slider');
        el.speedValue = document.getElementById('speed-value');
        el.ascBtn = document.getElementById('asc-btn');
        el.descBtn = document.getElementById('desc-btn');
        el.prevBtn = document.getElementById('prev-btn');
        el.playBtn = document.getElementById('play-btn');
        el.nextBtn = document.getElementById('next-btn');
        el.resetBtn = document.getElementById('reset-btn');
        el.restartBtn = document.getElementById('restart-btn');
        el.stepDisplay = document.getElementById('step-display');
        el.stepPct = document.getElementById('step-pct');
        el.progressFill = document.getElementById('progress-fill');
        el.explanation = document.getElementById('explanation-text');
        el.explanationBadge = document.getElementById('op-tag-element');
        el.explanationResult = document.getElementById('explanation-result');
        el.comparisons = document.getElementById('comparisons-count');
        el.swaps = document.getElementById('swaps-count');
        el.complexity = document.getElementById('complexity-display');
        el.canvasStatusPill = document.getElementById('canvas-status-pill');
        el.canvasStatusText = document.getElementById('canvas-status-text');
        el.completionBanner = document.getElementById('completion-banner');
        el.completionStats = document.getElementById('completion-banner-stats');
        el.completionReplay = document.getElementById('completion-replay-btn');
    }

    /* ---------- event binding ---------- */
    function bindEvents() {
        el.algoSelect.addEventListener('change', onAlgorithmChange);
        el.generateBtn.addEventListener('click', onGenerate);
        el.applyCustomBtn.addEventListener('click', onApplyCustom);
        el.customInput.addEventListener('keyup', function (e) {
            if (e.key === 'Enter') onApplyCustom();
        });
        el.sizeSlider.addEventListener('input', onSizeChange);
        el.speedSlider.addEventListener('input', onSpeedChange);
        el.ascBtn.addEventListener('click', function () { setOrder('asc'); });
        el.descBtn.addEventListener('click', function () { setOrder('desc'); });
        el.prevBtn.addEventListener('click', onPrev);
        el.playBtn.addEventListener('click', onPlayPause);
        el.nextBtn.addEventListener('click', onNext);
        el.resetBtn.addEventListener('click', onReset);
        el.restartBtn.addEventListener('click', onRestart);

        if (el.completionReplay) {
            el.completionReplay.addEventListener('click', function () {
                onRestart();
                play();
            });
        }

        document.addEventListener('keydown', function (e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
            switch (e.key) {
                case ' ': e.preventDefault(); onPlayPause(); break;
                case 'ArrowLeft': onPrev(); break;
                case 'ArrowRight': onNext(); break;
                case 'r':
                case 'R': onReset(); break;
            }
        });

        var resizeTimer;
        window.addEventListener('resize', function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () {
                if (currentArray && currentArray.length && !isPlaying) {
                    renderBars(currentArray);
                }
            }, 60);
        });
    }

    /* ---------- handlers ---------- */
    function onAlgorithmChange() {
        currentAlgorithm = el.algoSelect.value;
        resetExecution();
        renderComplexity();
        if (currentArray.length) renderBars(currentArray);
    }

    function onGenerate() {
        resetExecution();
        currentArray = SearchifyUtils.generateRandomArray(arraySize);
        originalArray = currentArray.slice();
        renderBars(currentArray, true);
        SearchifyUtils.showNotification('New array generated', 'success');
    }

    function onApplyCustom() {
        var rawInput = (el.customInput.value || '').trim();
        if (!rawInput) {
            SearchifyUtils.showNotification('No data is given. Tap on Generate for sample input.', 'info');
            return;
        }
        var parsed = SearchifyUtils.parseCustomArray(rawInput);
        if (!parsed) {
            SearchifyUtils.showNotification('Invalid input. Enter 2–80 comma-separated numbers (1–999).', 'error');
            return;
        }
        resetExecution();
        currentArray = parsed;
        originalArray = parsed.slice();
        renderBars(currentArray, true);
        SearchifyUtils.showNotification('Custom array applied', 'success');
    }

    function onSizeChange() {
        var newSize = parseInt(el.sizeSlider.value, 10);
        if (isNaN(newSize) || newSize < 2) return;
        var prevSize = currentArray ? currentArray.length : 0;
        arraySize = newSize;
        el.sizeValue.textContent = arraySize;

        resetExecution();

        if (!currentArray || currentArray.length === 0) {
            currentArray = SearchifyUtils.generateRandomArray(arraySize);
            originalArray = currentArray.slice();
            renderBars(currentArray, true);
            return;
        }

        var area = el.vizArea;
        var oldLaunching = area.querySelectorAll('.bar-launching');
        for (var ol = 0; ol < oldLaunching.length; ol++) oldLaunching[ol].remove();

        var existingBars = area.querySelectorAll('.bar');

        if (existingBars.length === 0) {
            currentArray = SearchifyUtils.generateRandomArray(arraySize);
            originalArray = currentArray.slice();
            renderBars(currentArray, true);
            return;
        }

        if (newSize > prevSize) {
            // Increasing: append new random elements
            var needed = newSize - prevSize;
            for (var i = 0; i < needed; i++) {
                currentArray.push(Math.floor(Math.random() * 95) + 5);
            }
        } else if (newSize < prevSize) {
            // Decreasing: slice down to new size
            currentArray = currentArray.slice(0, newSize);
        }

        originalArray = currentArray.slice();

        // Calculate layout geometry for updated array
        var maxVal = Math.max.apply(null, currentArray);
        if (maxVal <= 0) maxVal = 1;
        var areaHeight = getUsableAreaHeight(area);
        var availableWidth = Math.max(300, (area.clientWidth > 100 ? area.clientWidth : 960) - 64);
        var calculatedWidth = Math.floor(availableWidth / currentArray.length) - 8;
        var barWidth = Math.min(52, Math.max(6, calculatedWidth));
        var showLabels = currentArray.length <= 36;

        if (newSize > prevSize) {
            // 1. Existing bars: smoothly adjust width via CSS transition and update heights/labels
            for (var i = 0; i < existingBars.length; i++) {
                var bar = existingBars[i];
                bar.classList.remove('drop-in');
                bar.style.width = barWidth + 'px';
                bar.style.height = Math.max(14, Math.round((currentArray[i] / maxVal) * areaHeight)) + 'px';

                var valLabel = bar.querySelector('.bar-label');
                var idxLabel = bar.querySelector('.bar-index');
                if (showLabels) {
                    if (!valLabel) {
                        valLabel = document.createElement('span');
                        valLabel.className = 'bar-label';
                        bar.appendChild(valLabel);
                    }
                    valLabel.textContent = currentArray[i];

                    if (!idxLabel) {
                        idxLabel = document.createElement('span');
                        idxLabel.className = 'bar-index';
                        bar.appendChild(idxLabel);
                    }
                    idxLabel.textContent = i;
                } else {
                    if (valLabel) valLabel.remove();
                    if (idxLabel) idxLabel.remove();
                }
            }

            // 2. Newly added bars: fall from height and bounce following natural laws of gravity
            for (var j = existingBars.length; j < newSize; j++) {
                var newBar = document.createElement('div');
                newBar.className = 'bar drop-in';
                newBar.style.height = Math.max(14, Math.round((currentArray[j] / maxVal) * areaHeight)) + 'px';
                newBar.style.width = barWidth + 'px';
                newBar.style.animationDelay = Math.min(0.25, (j - existingBars.length) * 0.035) + 's';
                newBar.addEventListener('animationend', function () {
                    this.classList.remove('drop-in');
                });

                if (showLabels) {
                    var nLabel = document.createElement('span');
                    nLabel.className = 'bar-label';
                    nLabel.textContent = currentArray[j];
                    newBar.appendChild(nLabel);

                    var nIdx = document.createElement('span');
                    nIdx.className = 'bar-index';
                    nIdx.textContent = j;
                    newBar.appendChild(nIdx);
                }

                area.appendChild(newBar);
            }
        } else if (newSize < prevSize) {
            // Capture positions of bars to launch upwards in reverse physics
            var barsToLaunch = [];
            var areaRect = area.getBoundingClientRect();
            for (var k = newSize; k < existingBars.length; k++) {
                var oldBar = existingBars[k];
                var barRect = oldBar.getBoundingClientRect();
                var leftOffset = barRect.left - areaRect.left;
                var bottomOffset = areaRect.bottom - barRect.bottom;
                var barW = oldBar.offsetWidth;
                var barH = oldBar.offsetHeight;
                var valLabel = oldBar.querySelector('.bar-label');
                var idxLabel = oldBar.querySelector('.bar-index');
                barsToLaunch.push({
                    left: leftOffset,
                    bottom: bottomOffset,
                    width: barW,
                    height: barH,
                    val: valLabel ? valLabel.textContent : '',
                    idx: idxLabel ? idxLabel.textContent : '',
                    stagger: k - newSize
                });
                oldBar.remove();
            }

            // Launch removed bars into sky with reverse gravity bounce physics
            for (var l = 0; l < barsToLaunch.length; l++) {
                var info = barsToLaunch[l];
                var launchBar = document.createElement('div');
                launchBar.className = 'bar-launching';
                launchBar.style.left = info.left + 'px';
                launchBar.style.bottom = info.bottom + 'px';
                launchBar.style.width = info.width + 'px';
                launchBar.style.height = info.height + 'px';
                launchBar.style.animationDelay = Math.min(0.2, info.stagger * 0.035) + 's';

                if (info.val) {
                    var vl = document.createElement('span');
                    vl.className = 'bar-label';
                    vl.textContent = info.val;
                    launchBar.appendChild(vl);

                    var il = document.createElement('span');
                    il.className = 'bar-index-launching';
                    il.textContent = info.idx;
                    launchBar.appendChild(il);
                }

                launchBar.addEventListener('animationend', function () {
                    this.remove();
                });
                area.appendChild(launchBar);
            }

            // Update remaining bars: smoothly expand width via CSS transition
            for (var m = 0; m < newSize; m++) {
                var bar = existingBars[m];
                bar.classList.remove('drop-in');
                bar.style.width = barWidth + 'px';
                bar.style.height = Math.max(14, Math.round((currentArray[m] / maxVal) * areaHeight)) + 'px';

                var valLabel = bar.querySelector('.bar-label');
                var idxLabel = bar.querySelector('.bar-index');
                if (showLabels) {
                    if (!valLabel) {
                        valLabel = document.createElement('span');
                        valLabel.className = 'bar-label';
                        bar.appendChild(valLabel);
                    }
                    valLabel.textContent = currentArray[m];

                    if (!idxLabel) {
                        idxLabel = document.createElement('span');
                        idxLabel.className = 'bar-index';
                        bar.appendChild(idxLabel);
                    }
                    idxLabel.textContent = m;
                } else {
                    if (valLabel) valLabel.remove();
                    if (idxLabel) idxLabel.remove();
                }
            }
        }
    }

    function onSpeedChange() {
        var val = parseInt(el.speedSlider.value, 10);
        speed = SearchifyUtils.getSpeedMs(val);
        el.speedValue.textContent = SearchifyUtils.getSpeedLabel(val);
        if (isPlaying) {
            clearInterval(playTimer);
            playTimer = setInterval(advanceStep, speed);
        }
    }

    function setOrder(order) {
        sortOrder = order;
        el.ascBtn.classList.toggle('active', order === 'asc');
        el.descBtn.classList.toggle('active', order === 'desc');
        el.ascBtn.setAttribute('aria-pressed', order === 'asc');
        el.descBtn.setAttribute('aria-pressed', order === 'desc');
        if (steps.length) {
            resetExecution();
            renderBars(originalArray);
        }
    }

    function onPlayPause() {
        if (currentArray.length === 0) {
            SearchifyUtils.showNotification('Generate an array first.', 'error');
            return;
        }
        if (isPlaying) {
            pause();
        } else {
            play();
        }
    }

    function onNext() {
        if (currentArray.length === 0) return;
        if (steps.length === 0) runAlgorithm();
        if (currentStep < steps.length - 1) {
            currentStep++;
            renderStep();
        }
    }

    function onPrev() {
        if (steps.length === 0) return;
        if (currentStep > 0) {
            currentStep--;
            renderStep();
        }
    }

    function onReset() {
        pause();
        resetExecution();
        currentArray = originalArray.slice();
        renderBars(currentArray);
        SearchifyUtils.showNotification('Visualizer reset to initial array', 'info');
    }

    function onRestart() {
        pause();
        if (steps.length > 0) {
            currentStep = 0;
            renderStep();
        }
    }

    /* ---------- playback ---------- */
    function play() {
        if (steps.length === 0) runAlgorithm();
        if (steps.length === 0) return;
        if (currentStep >= steps.length - 1) {
            currentStep = 0;
        }
        isPlaying = true;
        updatePlayButton();
        playTimer = setInterval(advanceStep, speed);
    }

    function pause() {
        isPlaying = false;
        clearInterval(playTimer);
        playTimer = null;
        updatePlayButton();
    }

    function advanceStep() {
        if (currentStep < steps.length - 1) {
            currentStep++;
            renderStep();
            if (currentStep === steps.length - 1) {
                SearchifyUtils.showNotification('Sorting complete!', 'success');
            }
        } else {
            pause();
        }
    }

    function updatePlayButton() {
        if (isPlaying) {
            el.playBtn.innerHTML = '&#10074;&#10074;';
            el.playBtn.title = 'Pause (Space)';
            el.playBtn.setAttribute('aria-label', 'Pause');
        } else {
            el.playBtn.innerHTML = '&#9654;';
            el.playBtn.title = 'Play (Space)';
            el.playBtn.setAttribute('aria-label', 'Play');
        }
    }

    /* ---------- algorithm execution ---------- */
    function runAlgorithm() {
        if (!window.SortingAlgorithms || !window.SortingAlgorithms[currentAlgorithm]) {
            SearchifyUtils.showNotification('Algorithm not loaded.', 'error');
            return;
        }
        steps = window.SortingAlgorithms[currentAlgorithm](originalArray.slice(), sortOrder);
        currentStep = 0;
        renderStep();
    }

    function resetExecution() {
        pause();
        steps = [];
        currentStep = 0;
        updateCounters(0, 0);
        updateStepDisplay(0, 0);
        if (el.explanation) el.explanation.textContent = 'Select an algorithm and click Generate to start.';
        if (el.explanationBadge) {
            el.explanationBadge.className = 'op-badge compare';
            el.explanationBadge.textContent = 'READY';
        }
        if (el.explanationResult) el.explanationResult.style.display = 'none';
        if (el.canvasStatusText) el.canvasStatusText.textContent = 'Ready';
        if (el.canvasStatusPill) el.canvasStatusPill.className = 'canvas-status-pill';
        if (el.completionBanner) el.completionBanner.classList.remove('show');
        if (el.vizArea) {
            var launching = el.vizArea.querySelectorAll('.bar-launching');
            for (var li = 0; li < launching.length; li++) launching[li].remove();
        }
        window.dispatchEvent(new CustomEvent('searchify:run-reset'));
    }

    /* ---------- rendering ---------- */
    function renderBars(arr, animateDrop) {
        var area = el.vizArea;
        var children = area.querySelectorAll('.bar, .viz-placeholder');
        for (var i = 0; i < children.length; i++) {
            children[i].remove();
        }

        if (!arr || arr.length === 0) return;

        var maxVal = Math.max.apply(null, arr);
        if (maxVal <= 0) maxVal = 1;
        var areaHeight = getUsableAreaHeight(area);
        var availableWidth = Math.max(300, (area.clientWidth > 100 ? area.clientWidth : 960) - 64);
        var calculatedWidth = Math.floor(availableWidth / arr.length) - 8;
        var barWidth = Math.min(52, Math.max(6, calculatedWidth));
        var showLabels = arr.length <= 36;

        for (var i = 0; i < arr.length; i++) {
            var bar = document.createElement('div');
            bar.className = animateDrop ? 'bar drop-in' : 'bar';
            bar.style.height = Math.max(14, Math.round((arr[i] / maxVal) * areaHeight)) + 'px';
            bar.style.width = barWidth + 'px';
            if (animateDrop) {
                bar.style.animationDelay = Math.min(0.35, i * 0.02) + 's';
                bar.addEventListener('animationend', function () {
                    this.classList.remove('drop-in');
                });
            }

            if (showLabels) {
                var label = document.createElement('span');
                label.className = 'bar-label';
                label.textContent = arr[i];
                bar.appendChild(label);

                var idxLabel = document.createElement('span');
                idxLabel.className = 'bar-index';
                idxLabel.textContent = i;
                bar.appendChild(idxLabel);
            }

            area.appendChild(bar);
        }
    }

    function renderStep() {
        if (steps.length === 0) return;
        var step = steps[currentStep];
        var area = el.vizArea;

        var old = area.querySelectorAll('.bar, .viz-placeholder');
        for (var i = 0; i < old.length; i++) old[i].remove();

        var arr = step.array;
        var maxVal = Math.max.apply(null, arr);
        if (maxVal <= 0) maxVal = 1;
        var areaHeight = getUsableAreaHeight(area);
        var availableWidth = Math.max(300, (area.clientWidth > 100 ? area.clientWidth : 960) - 64);
        var calculatedWidth = Math.floor(availableWidth / arr.length) - 8;
        var barWidth = Math.min(52, Math.max(6, calculatedWidth));
        var showLabels = arr.length <= 36;

        for (var i = 0; i < arr.length; i++) {
            var bar = document.createElement('div');
            bar.className = 'bar';
            bar.style.height = Math.max(14, Math.round((arr[i] / maxVal) * areaHeight)) + 'px';
            bar.style.width = barWidth + 'px';

            if (step.sorted && step.sorted.indexOf(i) !== -1) {
                bar.classList.add('sorted');
            }
            if (step.comparing && step.comparing.indexOf(i) !== -1) {
                bar.classList.add('comparing');
            }
            if (step.swapping && step.swapping.indexOf(i) !== -1) {
                bar.classList.add('swapping');
            }
            if (step.pivot && step.pivot.indexOf(i) !== -1) {
                bar.classList.add('pivot');
            }

            if (showLabels) {
                var label = document.createElement('span');
                label.className = 'bar-label';
                label.textContent = arr[i];
                bar.appendChild(label);

                var idxLabel = document.createElement('span');
                idxLabel.className = 'bar-index';
                idxLabel.textContent = i;
                bar.appendChild(idxLabel);
            }

            area.appendChild(bar);
        }

        updateExplanationCard(step);
        updateStatusPill(step);
        updateCompletionBanner(step);
        updateCounters(step.counters.comparisons, step.counters.swaps);
        updateStepDisplay(currentStep + 1, steps.length);
        window.dispatchEvent(new CustomEvent('searchify:step', { detail: { algorithm: currentAlgorithm, step: step, currentStep: currentStep, totalSteps: steps.length } }));
    }

    /* ---------- explanation card ---------- */
    function updateExplanationCard(step) {
        if (!el.explanation) return;
        var rawText = step.explanation || '';

        var badgeText = 'OPERATION';
        var badgeCls = 'compare';
        if (step.swapping && step.swapping.length > 0) {
            badgeText = 'SWAP OPERATION';
            badgeCls = 'swap';
        } else if (step.comparing && step.comparing.length > 0) {
            badgeText = 'COMPARING ELEMENTS';
            badgeCls = 'compare';
        } else if (step.pivot && step.pivot.length > 0) {
            badgeText = 'PIVOT / PARTITION';
            badgeCls = 'pivot';
        } else if (step.sorted && step.sorted.length === step.array.length) {
            badgeText = 'ARRAY SORTED';
            badgeCls = 'sorted';
        } else if (rawText.toLowerCase().indexOf('pass') !== -1) {
            badgeText = 'PASS PROGRESS';
            badgeCls = 'compare';
        }

        if (el.explanationBadge) {
            el.explanationBadge.className = 'op-badge ' + badgeCls;
            el.explanationBadge.textContent = badgeText;
        }

        var formatted = escapeHtml(rawText);
        formatted = formatted.replace(/\b(\d+)\b/g, '<span class="val-chip">$1</span>');
        el.explanation.innerHTML = formatted;

        if (el.explanationResult) {
            if (step.swapping && step.swapping.length > 0) {
                el.explanationResult.style.display = 'block';
                el.explanationResult.innerHTML = '<strong>Action:</strong> Swapping elements into relative order.';
            } else if (step.comparing && step.comparing.length > 0) {
                el.explanationResult.style.display = 'block';
                el.explanationResult.innerHTML = '<strong>Action:</strong> Comparing adjacent values to check ordering condition.';
            } else if (step.sorted && step.sorted.length === step.array.length) {
                el.explanationResult.style.display = 'block';
                el.explanationResult.innerHTML = '<strong>Status:</strong> All elements confirmed in final sorted positions.';
            } else {
                el.explanationResult.style.display = 'none';
            }
        }
    }

    /* ---------- floating status pill ---------- */
    function updateStatusPill(step) {
        if (!el.canvasStatusText || !el.canvasStatusPill) return;

        if (step.sorted && step.sorted.length === step.array.length) {
            el.canvasStatusText.textContent = 'Sorted!';
            el.canvasStatusPill.className = 'canvas-status-pill sorted';
        } else if (step.swapping && step.swapping.length >= 2) {
            var i1 = step.swapping[0], i2 = step.swapping[1];
            el.canvasStatusText.textContent = 'Swapping ' + step.array[i1] + ' ↔ ' + step.array[i2];
            el.canvasStatusPill.className = 'canvas-status-pill swapping';
        } else if (step.comparing && step.comparing.length >= 2) {
            var c1 = step.comparing[0], c2 = step.comparing[1];
            el.canvasStatusText.textContent = 'Comparing ' + step.array[c1] + ' & ' + step.array[c2];
            el.canvasStatusPill.className = 'canvas-status-pill';
        } else if (step.pivot && step.pivot.length > 0) {
            el.canvasStatusText.textContent = 'Pivot: ' + step.array[step.pivot[0]];
            el.canvasStatusPill.className = 'canvas-status-pill';
        } else {
            el.canvasStatusText.textContent = 'Running';
            el.canvasStatusPill.className = 'canvas-status-pill';
        }
    }

    /* ---------- completion banner ---------- */
    function updateCompletionBanner(step) {
        if (!el.completionBanner) return;
        var isDone = (currentStep === steps.length - 1) && steps.length > 1;
        if (isDone) {
            if (el.completionStats) {
                el.completionStats.textContent = 'Completed in ' + step.counters.comparisons + ' comparisons and ' + step.counters.swaps + ' swaps.';
            }
            el.completionBanner.classList.add('show');
        } else {
            el.completionBanner.classList.remove('show');
        }
    }

    /* ---------- panel helpers ---------- */
    function updateCounters(comps, swps) {
        el.comparisons.textContent = comps;
        el.swaps.textContent = swps;
    }

    function updateStepDisplay(current, total) {
        el.stepDisplay.textContent = current + ' / ' + total;
        var pct = total > 0 ? Math.round((current / total) * 100) : 0;
        el.progressFill.style.width = pct + '%';
        if (el.stepPct) el.stepPct.textContent = pct + '%';
    }

    /* ---------- dedicated complexity below canvas ---------- */
    function renderComplexity() {
        var SA = window.SortingAlgorithms;
        if (!SA || !SA.complexityInfo || !SA.complexityInfo[currentAlgorithm]) {
            el.complexity.innerHTML = '';
            return;
        }
        var info = SA.complexityInfo[currentAlgorithm];

        var html = '';
        html += '<div class="complexity-section-label">Algorithm Complexity &amp; Analysis</div>';
        html += '<h2 class="complexity-algo-name">' + escapeHtml(info.name) + '</h2>';
        html += '<p class="complexity-algo-desc">' + escapeHtml(info.description) + '</p>';

        // 4 Complexity Cards Grid
        html += '<div class="complexity-cards-grid">';
        html += '<div class="complexity-stat-card"><span class="stat-card-label">Best Case</span><span class="stat-card-value">' + escapeHtml(info.best) + '</span></div>';
        html += '<div class="complexity-stat-card"><span class="stat-card-label">Average Case</span><span class="stat-card-value">' + escapeHtml(info.average) + '</span></div>';
        html += '<div class="complexity-stat-card"><span class="stat-card-label">Worst Case</span><span class="stat-card-value">' + escapeHtml(info.worst) + '</span></div>';
        html += '<div class="complexity-stat-card"><span class="stat-card-label">Space Complexity</span><span class="stat-card-value">' + escapeHtml(info.space) + '</span></div>';
        html += '</div>';

        // Additional Learning Information (Properties & When to Use)
        html += '<div class="complexity-details-row">';

        // Properties Card
        html += '<div class="properties-card">';
        html += '<div class="card-section-title">Algorithm Properties</div>';
        html += '<div class="properties-list">';
        html += '<div class="property-item"><span class="property-name">Stability</span><span class="complexity-tag ' + (info.stable ? 'yes' : 'no') + '">' + (info.stable ? '✔ Stable' : '✘ Not Stable') + '</span></div>';
        html += '<div class="property-item"><span class="property-name">In-Place</span><span class="complexity-tag ' + (info.inPlace ? 'yes' : 'no') + '">' + (info.inPlace ? '✔ In-Place' : '✘ Not In-Place') + '</span></div>';
        html += '</div>';
        html += '</div>';

        // When to Use Card
        html += '<div class="when-to-use-card">';
        html += '<div class="card-section-title">💡 When to Use</div>';
        html += '<p>' + escapeHtml(info.whenToUse || 'Used for educational analysis and comparison-based sorting.') + '</p>';
        html += '</div>';

        html += '</div>'; // End complexity-details-row

        el.complexity.innerHTML = html;
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    /* ---------- init ---------- */
    function init() {
        cacheElements();
        bindEvents();
        onSpeedChange();
        renderComplexity();
        onGenerate();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
