/* ============================================
   Searchify — Shared Utilities
   ============================================ */
(function () {
    'use strict';

    /**
     * Show a center-screen notification toast.
     * @param {string} message
     * @param {'info'|'error'|'success'} type
     * @param {number} duration ms (defaults to 2500ms = 2.5s)
     */
    function showNotification(message, type, duration) {
        type = type || 'info';
        duration = duration || 2500;
        var el = document.getElementById('notification');
        if (!el) return;

        // Cancel previous timer to prevent overlapping/premature dismissal
        clearTimeout(el._timeout);

        // Build notification icon based on type
        var iconSpan = document.createElement('span');
        iconSpan.className = 'notification-icon ' + type + '-icon';
        iconSpan.setAttribute('aria-hidden', 'true');
        if (type === 'success') {
            iconSpan.textContent = '✓';
        } else if (type === 'error') {
            iconSpan.textContent = '✕';
        } else {
            iconSpan.textContent = 'ℹ';
        }

        var textSpan = document.createElement('span');
        textSpan.className = 'notification-text';
        textSpan.textContent = message;

        el.innerHTML = '';
        el.appendChild(iconSpan);
        el.appendChild(textSpan);
        el.className = 'notification ' + type;

        // Force browser reflow so entrance scale/fade animation reliably re-triggers on repeated calls
        void el.offsetWidth;
        el.classList.add('show');

        // Automatically disappear after duration (default: 2.5 seconds)
        el._timeout = setTimeout(function () {
            el.classList.remove('show');
        }, duration);
    }

    /**
     * Parse a comma-separated string into an array of numbers.
     * Returns null if invalid.
     * @param {string} str
     * @returns {number[]|null}
     */
    function parseCustomArray(str) {
        if (!str || !str.trim()) return null;
        var parts = str.split(',');
        var result = [];
        for (var i = 0; i < parts.length; i++) {
            var num = Number(parts[i].trim());
            if (isNaN(num) || !isFinite(num)) return null;
            num = Math.round(num);
            if (num < 1 || num > 999) return null;
            result.push(num);
        }
        if (result.length < 2 || result.length > 80) return null;
        return result;
    }

    /**
     * Generate a random array.
     * @param {number} size
     * @param {number} min
     * @param {number} max
     * @returns {number[]}
     */
    function generateRandomArray(size, min, max) {
        min = min || 5;
        max = max || 100;
        var arr = [];
        for (var i = 0; i < size; i++) {
            arr.push(Math.floor(Math.random() * (max - min + 1)) + min);
        }
        return arr;
    }

    /**
     * Speed presets: slider value (1-6) → milliseconds delay between steps
     * 1x is the lowest speed (longest delay), 6x is the highest speed (shortest delay)
     */
    var SPEED_MAP = {
        1: 850,
        2: 500,
        3: 300,
        4: 160,
        5: 80,
        6: 35
    };

    var SPEED_LABELS = {
        1: '1x',
        2: '2x',
        3: '3x',
        4: '4x',
        5: '5x',
        6: '6x'
    };

    function getSpeedMs(sliderValue) {
        return SPEED_MAP[sliderValue] || 850;
    }

    function getSpeedLabel(sliderValue) {
        return SPEED_LABELS[sliderValue] || '1x';
    }

    window.SearchifyUtils = {
        showNotification: showNotification,
        parseCustomArray: parseCustomArray,
        generateRandomArray: generateRandomArray,
        getSpeedMs: getSpeedMs,
        getSpeedLabel: getSpeedLabel
    };
    window.AlgoVizUtils = window.SearchifyUtils;
})();
