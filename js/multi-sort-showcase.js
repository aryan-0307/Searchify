/**
 * js/multi-sort-showcase.js
 * =========================
 * Powers the Multi-Algorithm Sorting Comparison Showcase on the Searchify homepage.
 * Allows users to choose any N sorting techniques to compare on the EXACT SAME dataset.
 * Showcases synchronized execution, step-by-step progress, comparative operations,
 * and a finish leaderboard highlighting algorithmic efficiency differences.
 */

(function () {
    'use strict';

    // ───────────────────────────────────────────────────────────
    // Algorithm Metadata & Definitions
    // ───────────────────────────────────────────────────────────
    var ALGORITHMS = [
        { id: 'bubbleSort', name: 'Bubble Sort', complexity: 'O(n²)', category: 'n2', tag: 'Classic' },
        { id: 'selectionSort', name: 'Selection Sort', complexity: 'O(n²)', category: 'n2', tag: 'Classic' },
        { id: 'insertionSort', name: 'Insertion Sort', complexity: 'O(n²)', category: 'n2', tag: 'Classic' },
        { id: 'mergeSort', name: 'Merge Sort', complexity: 'O(n log n)', category: 'nlogn', tag: 'Divide & Conquer' },
        { id: 'quickSort', name: 'Quick Sort', complexity: 'O(n log n)', category: 'nlogn', tag: 'Partitioning' },
        { id: 'heapSort', name: 'Heap Sort', complexity: 'O(n log n)', category: 'nlogn', tag: 'Heap Tree' },
        { id: 'shellSort', name: 'Shell Sort', complexity: 'O(n log² n)', category: 'nlogn', tag: 'Diminishing Gap' },
        { id: 'countingSort', name: 'Counting Sort', complexity: 'O(n + k)', category: 'linear', tag: 'Non-Comparison' },
        { id: 'radixSort', name: 'Radix Sort', complexity: 'O(d(n+k))', category: 'linear', tag: 'Digit Buckets' },
        { id: 'bucketSort', name: 'Bucket Sort', complexity: 'O(n + k)', category: 'linear', tag: 'Range Buckets' }
    ];

    // Presets mapping
    var PRESETS = {
        popular: ['bubbleSort', 'mergeSort', 'quickSort'],
        nlogn: ['mergeSort', 'quickSort', 'heapSort'],
        n2: ['bubbleSort', 'selectionSort', 'insertionSort'],
        linear: ['countingSort', 'radixSort', 'bucketSort'],
        all: ALGORITHMS.map(function (a) { return a.id; })
    };

    // Default state
    var selectedAlgos = ['bubbleSort', 'mergeSort', 'quickSort'];
    var defaultArray = [68, 24, 91, 45, 12, 78, 36, 83, 52, 19];
    var sharedArray = defaultArray.slice();

    // Trace cache per algorithm: { algoId: [steps] }
    var traces = {};
    var maxStepsAcrossSelected = 0;
    var currentStepIndex = 0;
    var isPlaying = false;
    var playbackTimer = null;
    var speedMultiplier = 2; // 1x = 350ms, 2x = 180ms, 3x = 90ms, 4x = 40ms

    // Rankings recorded during playback: [{ algoId, finishedAtStep, comparisons, swaps }]
    var finishRankings = [];

    // DOM Elements cache
    var dom = {};

    // ───────────────────────────────────────────────────────────
    // Initialization
    // ───────────────────────────────────────────────────────────
    function init() {
        var section = document.getElementById('try-it');
        if (!section) return;

        dom.section = section;
        dom.chipsGrid = document.getElementById('showcase-chips-grid');
        dom.grid = document.getElementById('showcase-grid');
        dom.selectedCount = document.getElementById('showcase-selected-count');
        dom.presetBtns = section.querySelectorAll('.preset-btn');
        dom.playBtn = document.getElementById('showcase-play-btn');
        dom.prevBtn = document.getElementById('showcase-prev-btn');
        dom.nextBtn = document.getElementById('showcase-next-btn');
        dom.resetBtn = document.getElementById('showcase-reset-btn');
        dom.shuffleBtn = document.getElementById('showcase-shuffle-btn');
        dom.customInput = document.getElementById('showcase-custom-input');
        dom.applyBtn = document.getElementById('showcase-apply-btn');
        dom.speedSlider = document.getElementById('showcase-speed');
        dom.speedVal = document.getElementById('showcase-speed-val');
        dom.statusText = document.getElementById('showcase-status-text');
        dom.leaderboard = document.getElementById('showcase-leaderboard');
        dom.leaderboardContent = document.getElementById('leaderboard-content');

        // Set initial custom input placeholder/value
        if (dom.customInput) {
            dom.customInput.value = sharedArray.join(', ');
        }

        renderChips();
        recomputeTraces();
        renderGrid();
        bindEvents();
    }

    // ───────────────────────────────────────────────────────────
    // Event Handlers
    // ───────────────────────────────────────────────────────────
    function bindEvents() {
        // Preset buttons
        if (dom.presetBtns) {
            Array.from(dom.presetBtns).forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var presetKey = btn.getAttribute('data-preset');
                    if (PRESETS[presetKey]) {
                        applyPreset(presetKey);
                    }
                });
            });
        }

        // Shuffle button
        if (dom.shuffleBtn) {
            dom.shuffleBtn.addEventListener('click', function () {
                shuffleArray();
            });
        }

        // Apply custom array button
        if (dom.applyBtn) {
            dom.applyBtn.addEventListener('click', function () {
                applyCustomArray();
            });
        }
        if (dom.customInput) {
            dom.customInput.addEventListener('keyup', function (e) {
                if (e.key === 'Enter') applyCustomArray();
            });
        }

        // Play/Pause button
        if (dom.playBtn) {
            dom.playBtn.addEventListener('click', function () {
                togglePlay();
            });
        }

        // Step buttons
        if (dom.prevBtn) {
            dom.prevBtn.addEventListener('click', function () {
                stepBackward();
            });
        }
        if (dom.nextBtn) {
            dom.nextBtn.addEventListener('click', function () {
                stepForward();
            });
        }

        // Reset button
        if (dom.resetBtn) {
            dom.resetBtn.addEventListener('click', function () {
                reset();
            });
        }

        // Speed slider
        if (dom.speedSlider) {
            dom.speedSlider.addEventListener('input', function () {
                speedMultiplier = parseInt(dom.speedSlider.value, 10) || 2;
                if (dom.speedVal) {
                    dom.speedVal.textContent = speedMultiplier + 'x';
                }
                if (isPlaying) {
                    pause();
                    play();
                }
            });
        }
    }

    // ───────────────────────────────────────────────────────────
    // Algorithm Selection & Preset Management
    // ───────────────────────────────────────────────────────────
    function renderChips() {
        if (!dom.chipsGrid) return;
        dom.chipsGrid.innerHTML = '';

        ALGORITHMS.forEach(function (algo) {
            var isSelected = selectedAlgos.indexOf(algo.id) !== -1;
            var chip = document.createElement('button');
            chip.type = 'button';
            chip.className = 'showcase-chip' + (isSelected ? ' is-selected' : '');
            chip.setAttribute('data-algo', algo.id);
            chip.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
            chip.innerHTML = '<span class="chip-checkbox">' + (isSelected ? '✓' : '') + '</span>' +
                '<span class="chip-name">' + algo.name + '</span>' +
                '<span class="chip-badge">' + algo.complexity + '</span>';

            chip.addEventListener('click', function () {
                toggleAlgoSelection(algo.id);
            });

            dom.chipsGrid.appendChild(chip);
        });

        updateSelectedCount();
    }

    function toggleAlgoSelection(algoId) {
        var idx = selectedAlgos.indexOf(algoId);
        if (idx !== -1) {
            // Cannot deselect all
            if (selectedAlgos.length <= 1) {
                alert('Please keep at least 1 sorting algorithm selected for comparison.');
                return;
            }
            selectedAlgos.splice(idx, 1);
        } else {
            selectedAlgos.push(algoId);
        }

        pause();
        updateChipsActiveState();
        updatePresetButtonsState();
        recomputeTraces();
        renderGrid();
    }

    function applyPreset(presetKey) {
        var list = PRESETS[presetKey];
        if (!list) return;

        pause();
        selectedAlgos = list.slice();
        updateChipsActiveState();
        updatePresetButtonsState(presetKey);
        recomputeTraces();
        renderGrid();
    }

    function updateChipsActiveState() {
        if (!dom.chipsGrid) return;
        var chips = dom.chipsGrid.querySelectorAll('.showcase-chip');
        chips.forEach(function (chip) {
            var id = chip.getAttribute('data-algo');
            var isSel = selectedAlgos.indexOf(id) !== -1;
            if (isSel) {
                chip.classList.add('is-selected');
                chip.setAttribute('aria-pressed', 'true');
                chip.querySelector('.chip-checkbox').textContent = '✓';
            } else {
                chip.classList.remove('is-selected');
                chip.setAttribute('aria-pressed', 'false');
                chip.querySelector('.chip-checkbox').textContent = '';
            }
        });
        updateSelectedCount();
    }

    function updateSelectedCount() {
        if (dom.selectedCount) {
            dom.selectedCount.textContent = selectedAlgos.length + ' Selected';
        }
    }

    function updatePresetButtonsState(activePreset) {
        if (!dom.presetBtns) return;
        Array.from(dom.presetBtns).forEach(function (btn) {
            if (activePreset && btn.getAttribute('data-preset') === activePreset) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // ───────────────────────────────────────────────────────────
    // Shared Array Operations
    // ───────────────────────────────────────────────────────────
    function shuffleArray() {
        pause();
        var arr = [];
        var count = 10;
        for (var i = 0; i < count; i++) {
            arr.push(Math.floor(Math.random() * 85) + 12);
        }
        sharedArray = arr;
        if (dom.customInput) {
            dom.customInput.value = sharedArray.join(', ');
        }
        recomputeTraces();
        renderGrid();
        setStatus('Fresh shared array generated. Ready to race!');
    }

    function applyCustomArray() {
        if (!dom.customInput) return;
        var raw = dom.customInput.value.trim();
        if (!raw) {
            alert('Please enter comma-separated numbers (e.g. 45, 12, 85, 32).');
            return;
        }

        var parsed = raw.split(/[\s,]+/).map(function (v) {
            return parseInt(v, 10);
        }).filter(function (v) {
            return !isNaN(v);
        });

        if (parsed.length < 3) {
            alert('Please enter at least 3 numbers to compare sorting.');
            return;
        }
        if (parsed.length > 25) {
            parsed = parsed.slice(0, 25);
        }

        pause();
        sharedArray = parsed;
        dom.customInput.value = sharedArray.join(', ');
        recomputeTraces();
        renderGrid();
        setStatus('Custom array applied across all ' + selectedAlgos.length + ' algorithms.');
    }

    // ───────────────────────────────────────────────────────────
    // Multi-Trace Computation
    // ───────────────────────────────────────────────────────────
    function recomputeTraces() {
        traces = {};
        maxStepsAcrossSelected = 0;
        currentStepIndex = 0;
        finishRankings = [];

        if (!window.SortingAlgorithms) {
            console.warn('SortingAlgorithms engine not loaded.');
            return;
        }

        selectedAlgos.forEach(function (algoId) {
            var fn = window.SortingAlgorithms[algoId];
            if (typeof fn === 'function') {
                var trace = fn(sharedArray.slice(), true); // ascending
                traces[algoId] = trace;
                if (trace.length > maxStepsAcrossSelected) {
                    maxStepsAcrossSelected = trace.length;
                }
            }
        });

        if (dom.leaderboard) {
            dom.leaderboard.style.display = 'none';
        }
    }

    // ───────────────────────────────────────────────────────────
    // Grid & Card Rendering
    // ───────────────────────────────────────────────────────────
    function renderGrid() {
        if (!dom.grid) return;
        dom.grid.innerHTML = '';

        selectedAlgos.forEach(function (algoId) {
            var meta = ALGORITHMS.find(function (a) { return a.id === algoId; });
            if (!meta) return;

            var card = document.createElement('article');
            card.className = 'showcase-algo-card';
            card.id = 'showcase-card-' + algoId;
            card.setAttribute('data-algo', algoId);

            var trace = traces[algoId] || [];
            var totalSteps = Math.max(0, trace.length - 1);

            card.innerHTML =
                '<header class="algo-card-header">' +
                    '<div class="algo-card-title-group">' +
                        '<h4 class="algo-card-title">' + meta.name + '</h4>' +
                        '<span class="algo-card-complexity">' + meta.complexity + '</span>' +
                    '</div>' +
                    '<div class="algo-card-status">' +
                        '<span class="algo-status-pill pill-ready">Ready</span>' +
                    '</div>' +
                '</header>' +
                '<figure class="algo-card-canvas" aria-label="' + meta.name + ' array bars"></figure>' +
                '<div class="algo-card-stats">' +
                    '<span class="stat-pill"><i aria-hidden="true">⚖️</i> <b class="comp-val">0</b> comps</span>' +
                    '<span class="stat-pill"><i aria-hidden="true">🔄</i> <b class="swap-val">0</b> swaps</span>' +
                    '<span class="stat-pill"><i aria-hidden="true">⏱️</i> Step <b class="step-val">0 / ' + totalSteps + '</b></span>' +
                '</div>' +
                '<div class="algo-card-progress">' +
                    '<div class="progress-bar-fill" style="width: 0%;"></div>' +
                '</div>' +
                '<footer class="algo-card-footer">' +
                    '<span class="op-message">Initial array ready</span>' +
                '</footer>';

            dom.grid.appendChild(card);
        });

        renderAllTracksAtStep(currentStepIndex);
        updatePlaybackButtonsUI();
    }

    function renderAllTracksAtStep(stepIdx) {
        var minVal = Math.min.apply(null, sharedArray);
        var maxVal = Math.max.apply(null, sharedArray);
        var valSpan = (maxVal - minVal) || 1;

        selectedAlgos.forEach(function (algoId) {
            var card = document.getElementById('showcase-card-' + algoId);
            if (!card) return;

            var trace = traces[algoId] || [];
            if (trace.length === 0) return;

            // Clamped step for this algorithm (once finished, stays at final step)
            var clampedStep = Math.min(stepIdx, trace.length - 1);
            var step = trace[clampedStep];
            var isFinished = (clampedStep === trace.length - 1 && trace.length > 1);

            // Record ranking if finished for the first time
            if (isFinished && !finishRankings.some(function (r) { return r.algoId === algoId; })) {
                finishRankings.push({
                    algoId: algoId,
                    name: ALGORITHMS.find(function (a) { return a.id === algoId; }).name,
                    stepCount: trace.length - 1,
                    comparisons: step.counters ? step.counters.comparisons : 0,
                    swaps: step.counters ? step.counters.swaps : 0,
                    finishedOrder: finishRankings.length + 1
                });
            }

            // 1. Render Bars
            var canvas = card.querySelector('.algo-card-canvas');
            canvas.innerHTML = '';

            var arr = step.array || [];
            var comparing = step.comparing || [];
            var swapping = step.swapping || [];
            var sorted = step.sorted || [];
            var pivot = step.pivot || [];

            arr.forEach(function (val, idx) {
                var bar = document.createElement('div');
                bar.className = 'showcase-bar';

                // Height calculation: min 14%, max 96%
                var pct = ((val - minVal) / valSpan) * 82 + 14;
                bar.style.height = pct + '%';

                // State colors
                if (isFinished || sorted.indexOf(idx) !== -1) {
                    bar.classList.add('is-sorted');
                } else if (swapping.indexOf(idx) !== -1) {
                    bar.classList.add('is-swapping');
                } else if (comparing.indexOf(idx) !== -1) {
                    bar.classList.add('is-comparing');
                } else if (pivot.indexOf(idx) !== -1) {
                    bar.classList.add('is-pivot');
                }

                bar.innerHTML = '<span class="bar-val showcase-bar-val">' + val + '</span>';
                canvas.appendChild(bar);
            });

            // 2. Update Stats
            var compVal = card.querySelector('.comp-val');
            var swapVal = card.querySelector('.swap-val');
            var stepVal = card.querySelector('.step-val');
            var progressFill = card.querySelector('.progress-bar-fill');
            var opMsg = card.querySelector('.op-message');
            var statusPill = card.querySelector('.algo-status-pill');

            var comparisons = step.counters ? step.counters.comparisons : 0;
            var swaps = step.counters ? step.counters.swaps : 0;
            var total = Math.max(1, trace.length - 1);
            var progressPct = Math.round((clampedStep / total) * 100);

            if (compVal) compVal.textContent = comparisons;
            if (swapVal) swapVal.textContent = swaps;
            if (stepVal) stepVal.textContent = clampedStep + ' / ' + total;
            if (progressFill) progressFill.style.width = progressPct + '%';
            if (opMsg) opMsg.textContent = step.explanation || 'Sorting...';

            // 3. Status Pill & Finish Badge
            if (isFinished) {
                card.classList.add('is-completed', 'is-finished');
                var rankItem = finishRankings.find(function (r) { return r.algoId === algoId; });
                var rankText = rankItem ? getOrdinal(rankItem.finishedOrder) + ' Place' : 'Sorted ✓';
                statusPill.className = 'algo-status-pill pill-sorted';
                statusPill.textContent = '🏆 ' + rankText;
            } else if (isPlaying) {
                card.classList.remove('is-completed', 'is-finished');
                statusPill.className = 'algo-status-pill pill-sorting';
                statusPill.textContent = '⚡ Sorting';
            } else {
                card.classList.remove('is-completed', 'is-finished');
                statusPill.className = 'algo-status-pill pill-ready';
                statusPill.textContent = clampedStep > 0 ? 'Paused' : 'Ready';
            }
        });

        // Check if all algorithms have completed
        var allDone = selectedAlgos.every(function (id) {
            var tr = traces[id] || [];
            return tr.length <= 1 || stepIdx >= tr.length - 1;
        });

        if (allDone && stepIdx > 0) {
            pause();
            setStatus('All ' + selectedAlgos.length + ' algorithms finished sorting!');
            renderLeaderboard();
        }
    }

    function getOrdinal(n) {
        var s = ['th', 'st', 'nd', 'rd'];
        var v = n % 100;
        return n + (s[(v - 20) % 10] || s[v] || s[0]);
    }

    // ───────────────────────────────────────────────────────────
    // Playback Engine
    // ───────────────────────────────────────────────────────────
    function togglePlay() {
        if (isPlaying) {
            pause();
        } else {
            play();
        }
    }

    function play() {
        if (selectedAlgos.length === 0) return;

        // If at end, restart
        if (currentStepIndex >= maxStepsAcrossSelected - 1) {
            currentStepIndex = 0;
            finishRankings = [];
            if (dom.leaderboard) dom.leaderboard.style.display = 'none';
        }

        isPlaying = true;
        updatePlaybackButtonsUI();
        setStatus('Race in progress! Comparing ' + selectedAlgos.length + ' algorithms...');

        function loop() {
            if (!isPlaying) return;

            if (currentStepIndex < maxStepsAcrossSelected - 1) {
                currentStepIndex++;
                renderAllTracksAtStep(currentStepIndex);
                var delay = getStepDelay();
                playbackTimer = setTimeout(loop, delay);
            } else {
                pause();
            }
        }

        var delay = getStepDelay();
        playbackTimer = setTimeout(loop, delay);
    }

    function pause() {
        isPlaying = false;
        if (playbackTimer) {
            clearTimeout(playbackTimer);
            playbackTimer = null;
        }
        updatePlaybackButtonsUI();
        if (currentStepIndex > 0 && currentStepIndex < maxStepsAcrossSelected - 1) {
            setStatus('Race paused at step ' + currentStepIndex);
        }
    }

    function stepForward() {
        pause();
        if (currentStepIndex < maxStepsAcrossSelected - 1) {
            currentStepIndex++;
            renderAllTracksAtStep(currentStepIndex);
            setStatus('Stepped forward to step ' + currentStepIndex);
        }
    }

    function stepBackward() {
        pause();
        if (currentStepIndex > 0) {
            currentStepIndex--;
            renderAllTracksAtStep(currentStepIndex);
            setStatus('Stepped backward to step ' + currentStepIndex);
        }
    }

    function reset() {
        pause();
        currentStepIndex = 0;
        finishRankings = [];
        if (dom.leaderboard) dom.leaderboard.style.display = 'none';
        renderAllTracksAtStep(0);
        setStatus('Reset to initial step. Ready to race!');
    }

    function getStepDelay() {
        // Speed multiplier 1: 350ms, 2: 170ms, 3: 80ms, 4: 35ms
        switch (speedMultiplier) {
            case 1: return 340;
            case 2: return 160;
            case 3: return 75;
            case 4: return 30;
            default: return 160;
        }
    }

    function updatePlaybackButtonsUI() {
        if (!dom.playBtn) return;
        var icon = dom.playBtn.querySelector('.play-icon');
        var text = dom.playBtn.querySelector('.play-text');

        if (isPlaying) {
            if (icon) icon.textContent = '⏸';
            if (text) text.textContent = 'Pause Race';
            dom.playBtn.classList.add('is-playing');
        } else {
            if (icon) icon.textContent = '▶';
            if (text) text.textContent = (currentStepIndex > 0 && currentStepIndex < maxStepsAcrossSelected - 1) ? 'Resume Race' : 'Start Race';
            dom.playBtn.classList.remove('is-playing');
        }
    }

    function setStatus(msg) {
        if (dom.statusText) {
            dom.statusText.textContent = msg;
        }
    }

    // ───────────────────────────────────────────────────────────
    // Leaderboard & Comparison Summary
    // ───────────────────────────────────────────────────────────
    function renderLeaderboard() {
        if (!dom.leaderboard || !dom.leaderboardContent) return;

        // Sort finish rankings by finishedOrder
        finishRankings.sort(function (a, b) {
            return a.finishedOrder - b.finishedOrder;
        });

        var html = '<div class="leaderboard-grid">';
        finishRankings.forEach(function (item, idx) {
            var medal = idx === 0 ? '🥇 1st' : (idx === 1 ? '🥈 2nd' : (idx === 2 ? '🥉 3rd' : (idx + 1) + 'th'));
            html +=
                '<div class="leaderboard-card' + (idx === 0 ? ' winner-card' : '') + '">' +
                    '<div class="leaderboard-rank">' + medal + '</div>' +
                    '<h4 class="leaderboard-algo-name">' + item.name + '</h4>' +
                    '<div class="leaderboard-metrics">' +
                        '<span><strong>' + item.stepCount + '</strong> steps</span> • ' +
                        '<span><strong>' + item.comparisons + '</strong> comps</span> • ' +
                        '<span><strong>' + item.swaps + '</strong> swaps</span>' +
                    '</div>' +
                '</div>';
        });
        html += '</div>';

        // Add summary note comparing 1st and last
        if (finishRankings.length >= 2) {
            var winner = finishRankings[0];
            var last = finishRankings[finishRankings.length - 1];
            var stepDiff = last.stepCount - winner.stepCount;
            var compDiff = last.comparisons - winner.comparisons;
            html += '<p class="leaderboard-summary-note">' +
                '⚡ <strong>' + winner.name + '</strong> sorted the dataset first in only <strong>' + winner.stepCount + ' steps</strong> (' + winner.comparisons + ' comparisons). ' +
                'In comparison, <strong>' + last.name + '</strong> took <strong>' + last.stepCount + ' steps</strong> (+' + stepDiff + ' steps, +' + compDiff + ' comparisons) on the exact same array.' +
                '</p>';
        }

        dom.leaderboardContent.innerHTML = html;
        dom.leaderboard.style.display = 'block';

        // Smooth scroll into view gently if needed
        try {
            dom.leaderboard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } catch (e) { }
    }

    // ───────────────────────────────────────────────────────────
    // Boot
    // ───────────────────────────────────────────────────────────
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
