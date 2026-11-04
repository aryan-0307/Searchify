/* ============================================
   AlgoViz — Searching Visualizer Controller (Full-Width Edition)
   ============================================ */
(function () {
    'use strict';

    /* ---------- state ---------- */
    var currentAlgorithm = 'linearSearch';
    var currentArray = [];
    var originalArray = [];
    var searchTarget = null;
    var steps = [];
    var currentStep = 0;
    var isPlaying = false;
    var playTimer = null;
    var speed = 400;          // ms between steps
    var arraySize = 15;

    /* ---------- DOM cache ---------- */
    var el = {};

    function cacheElements() {
        el.vizArea          = document.getElementById('visualization-area');
        el.algoSelect       = document.getElementById('algorithm-select');
        el.generateBtn      = document.getElementById('generate-btn');
        el.customInput      = document.getElementById('custom-array');
        el.applyCustomBtn   = document.getElementById('apply-custom-btn');
        el.targetInput      = document.getElementById('target-input');
        el.sizeSlider       = document.getElementById('array-size');
        el.sizeValue        = document.getElementById('size-value');
        el.speedSlider      = document.getElementById('speed-slider');
        el.speedValue       = document.getElementById('speed-value');
        el.prevBtn          = document.getElementById('prev-btn');
        el.playBtn          = document.getElementById('play-btn');
        el.nextBtn          = document.getElementById('next-btn');
        el.resetBtn         = document.getElementById('reset-btn');
        el.restartBtn       = document.getElementById('restart-btn');
        el.stepDisplay      = document.getElementById('step-display');
        el.stepPct          = document.getElementById('step-pct');
        el.progressFill     = document.getElementById('progress-fill');
        el.explanation      = document.getElementById('explanation-text');
        el.explanationBadge = document.getElementById('op-tag-element');
        el.explanationResult= document.getElementById('explanation-result');
        el.comparisons      = document.getElementById('comparisons-count');
        el.examined         = document.getElementById('examined-count');
        el.complexity       = document.getElementById('complexity-display');
        el.canvasStatusPill = document.getElementById('canvas-status-pill');
        el.canvasStatusText = document.getElementById('canvas-status-text');
        el.completionBanner = document.getElementById('completion-banner');
        el.completionTitle  = document.getElementById('completion-banner-title');
        el.completionStats  = document.getElementById('completion-banner-stats');
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
        el.targetInput.addEventListener('change', onTargetChange);
        el.targetInput.addEventListener('keyup', function (e) {
            if (e.key === 'Enter') onTargetChange();
        });
        el.sizeSlider.addEventListener('input', onSizeChange);
        el.speedSlider.addEventListener('input', onSpeedChange);
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
                case ' ':          e.preventDefault(); onPlayPause(); break;
                case 'ArrowLeft':  onPrev(); break;
                case 'ArrowRight': onNext(); break;
                case 'r':
                case 'R':          onReset(); break;
            }
        });
    }

    /* ---------- handlers ---------- */
    function onAlgorithmChange() {
        currentAlgorithm = el.algoSelect.value;
        resetExecution();
        renderComplexity();

        if (currentAlgorithm === 'binarySearch' && currentArray.length > 0) {
            currentArray.sort(function (a, b) { return a - b; });
            originalArray = currentArray.slice();
            AlgoVizUtils.showNotification('Array sorted for Binary Search.', 'info');
        }
        if (currentArray.length) renderInitialCells(currentArray);
    }

    function onGenerate() {
        resetExecution();
        currentArray = AlgoVizUtils.generateRandomArray(arraySize, 5, 99);
        if (currentAlgorithm === 'binarySearch') {
            currentArray.sort(function (a, b) { return a - b; });
        }
        originalArray = currentArray.slice();

        if (Math.random() > 0.3) {
            searchTarget = currentArray[Math.floor(Math.random() * currentArray.length)];
        } else {
            searchTarget = Math.floor(Math.random() * 95) + 5;
        }
        el.targetInput.value = searchTarget;

        renderInitialCells(currentArray);
        AlgoVizUtils.showNotification('New array generated (target: ' + searchTarget + ')', 'success');
    }

    function onApplyCustom() {
        var rawInput = (el.customInput.value || '').trim();
        if (!rawInput) {
            AlgoVizUtils.showNotification('No data is given. Tap on Generate for sample input.', 'info');
            return;
        }
        var parsed = AlgoVizUtils.parseCustomArray(rawInput);
        if (!parsed || parsed.length > 40) {
            AlgoVizUtils.showNotification('Invalid input. Enter 2–40 comma-separated numbers (1–999).', 'error');
            return;
        }
        resetExecution();
        currentArray = parsed;
        if (currentAlgorithm === 'binarySearch') {
            currentArray.sort(function (a, b) { return a - b; });
            AlgoVizUtils.showNotification('Custom array sorted for Binary Search.', 'info');
        } else {
            AlgoVizUtils.showNotification('Custom array applied.', 'success');
        }
        originalArray = currentArray.slice();

        if (el.targetInput.value !== '') {
            searchTarget = Number(el.targetInput.value);
        } else {
            searchTarget = currentArray[0];
            el.targetInput.value = searchTarget;
        }

        renderInitialCells(currentArray);
    }

    function onTargetChange() {
        var val = el.targetInput.value.trim();
        if (val === '') {
            searchTarget = null;
            resetExecution();
            if (currentArray.length) renderInitialCells(currentArray);
            return;
        }
        var num = Number(val);
        if (isNaN(num)) {
            AlgoVizUtils.showNotification('Please enter a valid numeric target.', 'error');
            return;
        }
        searchTarget = Math.round(num);
        el.targetInput.value = searchTarget;
        resetExecution();
        if (currentArray.length) renderInitialCells(currentArray);
    }

    function onSizeChange() {
        arraySize = parseInt(el.sizeSlider.value, 10);
        el.sizeValue.textContent = arraySize;
    }

    function onSpeedChange() {
        var val = parseInt(el.speedSlider.value, 10);
        speed = AlgoVizUtils.getSpeedMs(val);
        el.speedValue.textContent = AlgoVizUtils.getSpeedLabel(val);
        if (isPlaying) {
            clearInterval(playTimer);
            playTimer = setInterval(advanceStep, speed);
        }
    }

    function onPlayPause() {
        if (currentArray.length === 0) {
            AlgoVizUtils.showNotification('Generate an array first.', 'error');
            return;
        }
        if (searchTarget === null || isNaN(searchTarget)) {
            AlgoVizUtils.showNotification('Enter a target value to search for.', 'error');
            el.targetInput.focus();
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
        if (searchTarget === null || isNaN(searchTarget)) {
            AlgoVizUtils.showNotification('Enter a target value to search for.', 'error');
            el.targetInput.focus();
            return;
        }
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
        renderInitialCells(currentArray);
        AlgoVizUtils.showNotification('Visualizer reset to initial array', 'info');
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
                var finalStep = steps[currentStep];
                if (finalStep && finalStep.found !== undefined) {
                    AlgoVizUtils.showNotification('Target ' + searchTarget + ' found at index ' + finalStep.found + '!', 'success');
                } else if (finalStep && finalStep.notFound) {
                    AlgoVizUtils.showNotification('Target ' + searchTarget + ' not found in array.', 'info');
                }
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
        if (!window.SearchingAlgorithms || !window.SearchingAlgorithms[currentAlgorithm]) {
            AlgoVizUtils.showNotification('Algorithm not loaded.', 'error');
            return;
        }
        steps = window.SearchingAlgorithms[currentAlgorithm](originalArray.slice(), searchTarget);
        currentStep = 0;
        renderStep();
    }

    function resetExecution() {
        pause();
        steps = [];
        currentStep = 0;
        updateCounters(0, 0);
        updateStepDisplay(0, 0);
        if (el.explanation) el.explanation.textContent = 'Select an algorithm, generate an array, and enter a target value to begin.';
        if (el.explanationBadge) {
            el.explanationBadge.className = 'op-badge search';
            el.explanationBadge.textContent = 'READY';
        }
        if (el.explanationResult) el.explanationResult.style.display = 'none';
        if (el.canvasStatusText) el.canvasStatusText.textContent = 'Ready';
        if (el.canvasStatusPill) el.canvasStatusPill.className = 'canvas-status-pill';
        if (el.completionBanner) el.completionBanner.classList.remove('show');
    }

    /* ---------- rendering ---------- */
    function renderInitialCells(arr) {
        var area = el.vizArea;
        var old = area.querySelectorAll('.search-cells-wrapper, .viz-placeholder');
        for (var i = 0; i < old.length; i++) old[i].remove();

        if (!arr || arr.length === 0) return;

        var wrapper = document.createElement('div');
        wrapper.className = 'search-cells-wrapper';

        var targetDisplay = document.createElement('div');
        targetDisplay.className = 'search-target-display';
        targetDisplay.innerHTML = 'Target Value: <strong>' + (searchTarget !== null ? searchTarget : 'None') + '</strong>';
        wrapper.appendChild(targetDisplay);

        var cellsContainer = document.createElement('div');
        cellsContainer.className = 'search-cells';

        for (var i = 0; i < arr.length; i++) {
            var cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = arr[i];

            var idxLabel = document.createElement('span');
            idxLabel.className = 'cell-index';
            idxLabel.textContent = i;
            cell.appendChild(idxLabel);

            cellsContainer.appendChild(cell);
        }

        wrapper.appendChild(cellsContainer);
        area.appendChild(wrapper);
    }

    function renderStep() {
        if (steps.length === 0) return;
        var step = steps[currentStep];
        var area = el.vizArea;

        var old = area.querySelectorAll('.search-cells-wrapper, .viz-placeholder');
        for (var i = 0; i < old.length; i++) old[i].remove();

        var arr = step.array;
        var wrapper = document.createElement('div');
        wrapper.className = 'search-cells-wrapper';

        var targetDisplay = document.createElement('div');
        targetDisplay.className = 'search-target-display';
        targetDisplay.innerHTML = 'Target Value: <strong>' + (searchTarget !== null ? searchTarget : 'None') + '</strong>';
        wrapper.appendChild(targetDisplay);

        var cellsContainer = document.createElement('div');
        cellsContainer.className = 'search-cells';

        var isBinary = currentAlgorithm === 'binarySearch';

        for (var i = 0; i < arr.length; i++) {
            var cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = arr[i];

            var idxLabel = document.createElement('span');
            idxLabel.className = 'cell-index';
            idxLabel.textContent = i;
            cell.appendChild(idxLabel);

            if (isBinary) {
                var pointerBadges = [];
                if (step.low === i) pointerBadges.push({ label: 'L', cls: 'low' });
                if (step.mid === i) pointerBadges.push({ label: 'M', cls: 'mid' });
                if (step.high === i) pointerBadges.push({ label: 'H', cls: 'high' });

                if (pointerBadges.length > 0) {
                    var ptrSpan = document.createElement('span');
                    ptrSpan.className = 'cell-pointer';
                    ptrSpan.innerHTML = pointerBadges.map(function (b) {
                        return '<span class="pointer-label ' + b.cls + '">' + b.label + '</span>';
                    }).join(' ');
                    cell.appendChild(ptrSpan);
                }

                if (step.low === i) cell.classList.add('low-ptr');
                if (step.mid === i) cell.classList.add('mid-ptr');
                if (step.high === i) cell.classList.add('high-ptr');
            }

            if (step.eliminated && step.eliminated.indexOf(i) !== -1) {
                cell.classList.add('eliminated');
            } else if (step.active && step.active.indexOf(i) !== -1) {
                cell.classList.add('active');
            }

            if (step.checked && step.checked.indexOf(i) !== -1) {
                cell.classList.add('checked');
            }

            if (step.current === i) {
                cell.classList.add('current');
            }

            if (step.found === i) {
                cell.classList.remove('current', 'checked', 'eliminated', 'active');
                cell.classList.add('found');
            }

            if (step.notFound) {
                cell.classList.add('not-found');
            }

            cellsContainer.appendChild(cell);
        }

        wrapper.appendChild(cellsContainer);
        area.appendChild(wrapper);

        updateExplanationCard(step);
        updateStatusPill(step);
        updateCompletionBanner(step);
        updateCounters(step.counters.comparisons, step.counters.elementsExamined);
        updateStepDisplay(currentStep + 1, steps.length);
    }

    /* ---------- explanation card ---------- */
    function updateExplanationCard(step) {
        if (!el.explanation) return;
        var rawText = step.explanation || '';

        var badgeText = 'SEARCHING';
        var badgeCls = 'search';

        if (step.found !== null) {
            badgeText = 'TARGET FOUND';
            badgeCls = 'sorted';
        } else if (step.notFound) {
            badgeText = 'NOT FOUND';
            badgeCls = 'swap';
        } else if (step.mid !== null) {
            badgeText = 'CHECKING MIDPOINT';
            badgeCls = 'compare';
        } else if (step.current !== null) {
            badgeText = 'CHECKING ELEMENT';
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
            if (step.found !== null) {
                el.explanationResult.style.display = 'block';
                el.explanationResult.innerHTML = '<strong>Result:</strong> Match confirmed at index ' + step.found + '!';
            } else if (step.notFound) {
                el.explanationResult.style.display = 'block';
                el.explanationResult.innerHTML = '<strong>Result:</strong> Search concluded. Target does not exist in array.';
            } else if (step.mid !== null && searchTarget !== null) {
                el.explanationResult.style.display = 'block';
                var midVal = step.array[step.mid];
                if (searchTarget > midVal) {
                    el.explanationResult.innerHTML = '<strong>Decision:</strong> Target (' + searchTarget + ') > Mid (' + midVal + ') → search right half.';
                } else if (searchTarget < midVal) {
                    el.explanationResult.innerHTML = '<strong>Decision:</strong> Target (' + searchTarget + ') < Mid (' + midVal + ') → search left half.';
                } else {
                    el.explanationResult.innerHTML = '<strong>Decision:</strong> Target (' + searchTarget + ') == Mid (' + midVal + ') → match!';
                }
            } else {
                el.explanationResult.style.display = 'none';
            }
        }
    }

    /* ---------- floating status pill ---------- */
    function updateStatusPill(step) {
        if (!el.canvasStatusText || !el.canvasStatusPill) return;

        if (step.found !== null) {
            el.canvasStatusText.textContent = 'Found at index ' + step.found + '!';
            el.canvasStatusPill.className = 'canvas-status-pill sorted';
        } else if (step.notFound) {
            el.canvasStatusText.textContent = 'Not Found';
            el.canvasStatusPill.className = 'canvas-status-pill swapping';
        } else if (step.mid !== null) {
            el.canvasStatusText.textContent = 'Mid: ' + step.array[step.mid] + ' (idx ' + step.mid + ')';
            el.canvasStatusPill.className = 'canvas-status-pill';
        } else if (step.current !== null) {
            el.canvasStatusText.textContent = 'Checking idx ' + step.current + ' (' + step.array[step.current] + ')';
            el.canvasStatusPill.className = 'canvas-status-pill swapping';
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
            if (step.found !== null) {
                if (el.completionTitle) el.completionTitle.textContent = '🎯 Target ' + searchTarget + ' found at index ' + step.found + '!';
                if (el.completionStats) el.completionStats.textContent = 'Found in ' + step.counters.comparisons + ' comparisons & ' + step.counters.elementsExamined + ' examined elements.';
                el.completionBanner.style.borderColor = 'var(--color-sorted)';
            } else {
                if (el.completionTitle) el.completionTitle.textContent = '🔍 Target ' + searchTarget + ' not found';
                if (el.completionStats) el.completionStats.textContent = 'Examined ' + step.counters.elementsExamined + ' elements with ' + step.counters.comparisons + ' comparisons.';
                el.completionBanner.style.borderColor = 'var(--vibrant-pink)';
            }
            el.completionBanner.classList.add('show');
        } else {
            el.completionBanner.classList.remove('show');
        }
    }

    /* ---------- panel helpers ---------- */
    function updateCounters(comps, examined) {
        el.comparisons.textContent = comps;
        el.examined.textContent = examined;
    }

    function updateStepDisplay(current, total) {
        el.stepDisplay.textContent = current + ' / ' + total;
        var pct = total > 0 ? Math.round((current / total) * 100) : 0;
        el.progressFill.style.width = pct + '%';
        if (el.stepPct) el.stepPct.textContent = pct + '%';
    }

    /* ---------- dedicated complexity below canvas ---------- */
    function renderComplexity() {
        var SA = window.SearchingAlgorithms;
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
        html += '<div class="card-section-title">Search Properties</div>';
        html += '<div class="properties-list">';
        html += '<div class="property-item"><span class="property-name">Array Ordering</span><span class="complexity-tag ' + (info.requiresSorted ? 'no' : 'yes') + '">' + (info.requiresSorted ? 'Requires Sorted Array' : 'Works on Any Array') + '</span></div>';
        html += '<div class="property-item"><span class="property-name">Data Structure</span><span class="complexity-tag yes">Contiguous Arrays</span></div>';
        html += '</div>';
        html += '</div>';

        // When to Use Card
        html += '<div class="when-to-use-card">';
        html += '<div class="card-section-title">💡 When to Use</div>';
        html += '<p>' + escapeHtml(info.whenToUse || 'Used for lookup and search operations in arrays.') + '</p>';
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
        renderComplexity();
        onGenerate();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
