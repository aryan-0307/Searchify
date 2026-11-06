/**
 * searching-algorithms.js
 * ========================
 * Searching algorithm implementations for the AlgoViz educational visualizer.
 * Provides Linear Search and Binary Search with step-by-step trace data.
 *
 * Every function returns an array of step objects that the UI renders
 * to animate the algorithm's execution.
 *
 * Attached to window.SearchingAlgorithms.
 */
(function () {
    'use strict';

    // ─────────────────────────────────────────────
    // Helpers
    // ─────────────────────────────────────────────

    /**
     * Build a step object with sensible defaults.
     * Callers override only the fields they need.
     */
    function makeStep(overrides) {
        return Object.assign(
            {
                array: [],
                current: null,
                checked: [],
                found: null,
                notFound: false,
                low: null,
                mid: null,
                high: null,
                active: [],
                eliminated: [],
                explanation: '',
                pseudocodeLine: 0,
                counters: {
                    comparisons: 0,
                    elementsExamined: 0,
                    step: 1,
                    result: null,
                },
            },
            overrides
        );
    }

    /**
     * Return true when `arr` is sorted in ascending (non-decreasing) order.
     */
    function isSortedAscending(arr) {
        for (var i = 1; i < arr.length; i++) {
            if (arr[i] < arr[i - 1]) return false;
        }
        return true;
    }

    /**
     * Return an array of integers from `lo` to `hi` inclusive.
     */
    function rangeInclusive(lo, hi) {
        var result = [];
        for (var i = lo; i <= hi; i++) {
            result.push(i);
        }
        return result;
    }

    // ─────────────────────────────────────────────
    // Linear Search
    // ─────────────────────────────────────────────

    /**
     * Perform a linear search for `target` in `inputArray`.
     *
     * @param {number[]} inputArray – the array to search (not mutated)
     * @param {number}   target     – the value to find
     * @returns {Object[]} steps    – array of step trace objects
     */
    function linearSearch(inputArray, target) {
        var arr = inputArray.slice(); // deep-enough copy of primitives
        var steps = [];
        var comparisons = 0;
        var elementsExamined = 0;
        var stepNum = 0;
        var checked = [];

        // Handle empty array
        if (arr.length === 0) {
            stepNum++;
            steps.push(
                makeStep({
                    array: arr.slice(),
                    current: null,
                    checked: [],
                    found: null,
                    notFound: true,
                    explanation:
                        'The array is empty. Target ' +
                        target +
                        ' cannot be found.',
                    pseudocodeLine: 6,
                    counters: {
                        comparisons: 0,
                        elementsExamined: 0,
                        step: stepNum,
                        result: { found: false, index: -1 },
                    },
                })
            );
            return steps;
        }

        // Initial state step
        stepNum++;
        steps.push(
            makeStep({
                array: arr.slice(),
                current: null,
                checked: [],
                found: null,
                notFound: false,
                explanation:
                    'Starting Linear Search for target ' +
                    target +
                    ' in an array of ' +
                    arr.length +
                    ' element' +
                    (arr.length === 1 ? '' : 's') +
                    '. Will check each element from left to right.',
                pseudocodeLine: 0,
                counters: {
                    comparisons: comparisons,
                    elementsExamined: elementsExamined,
                    step: stepNum,
                    result: null,
                },
            })
        );

        // Iterate through each element
        for (var i = 0; i < arr.length; i++) {
            comparisons++;
            elementsExamined++;
            stepNum++;

            if (arr[i] === target) {
                // Found
                steps.push(
                    makeStep({
                        array: arr.slice(),
                        current: i,
                        checked: checked.slice(),
                        found: i,
                        notFound: false,
                        explanation:
                            'Check index ' +
                            i +
                            '. The value is ' +
                            arr[i] +
                            '. Found target ' +
                            target +
                            ' at index ' +
                            i +
                            '!',
                        pseudocodeLine: 3,
                        counters: {
                            comparisons: comparisons,
                            elementsExamined: elementsExamined,
                            step: stepNum,
                            result: { found: true, index: i },
                        },
                    })
                );
                return steps;
            }

            // Not a match
            steps.push(
                makeStep({
                    array: arr.slice(),
                    current: i,
                    checked: checked.slice(),
                    found: null,
                    notFound: false,
                    explanation:
                        'Check index ' +
                        i +
                        '. The value is ' +
                        arr[i] +
                        ', which does not match the target ' +
                        target +
                        '. Continue.',
                    pseudocodeLine: 2,
                    counters: {
                        comparisons: comparisons,
                        elementsExamined: elementsExamined,
                        step: stepNum,
                        result: null,
                    },
                })
            );

            checked.push(i);
        }

        // Not found after full scan
        stepNum++;
        steps.push(
            makeStep({
                array: arr.slice(),
                current: null,
                checked: checked.slice(),
                found: null,
                notFound: true,
                explanation:
                    'Target ' +
                    target +
                    ' was not found in the array. All ' +
                    arr.length +
                    ' element' +
                    (arr.length === 1 ? ' has' : 's have') +
                    ' been checked.',
                pseudocodeLine: 6,
                counters: {
                    comparisons: comparisons,
                    elementsExamined: elementsExamined,
                    step: stepNum,
                    result: { found: false, index: -1 },
                },
            })
        );

        return steps;
    }

    // ─────────────────────────────────────────────
    // Binary Search
    // ─────────────────────────────────────────────

    /**
     * Perform a binary search for `target` in `inputArray`.
     * If the array is not sorted, it is sorted ascending first.
     *
     * @param {number[]} inputArray – the array to search (not mutated)
     * @param {number}   target     – the value to find
     * @returns {Object[]} steps    – array of step trace objects
     */
    function binarySearch(inputArray, target) {
        var arr = inputArray.slice();
        var steps = [];
        var comparisons = 0;
        var elementsExamined = 0;
        var stepNum = 0;
        var eliminated = [];

        // Handle empty array
        if (arr.length === 0) {
            stepNum++;
            steps.push(
                makeStep({
                    array: arr.slice(),
                    current: null,
                    checked: [],
                    found: null,
                    notFound: true,
                    low: null,
                    mid: null,
                    high: null,
                    active: [],
                    eliminated: [],
                    explanation:
                        'The array is empty. Target ' +
                        target +
                        ' cannot be found.',
                    pseudocodeLine: 13,
                    counters: {
                        comparisons: 0,
                        elementsExamined: 0,
                        step: stepNum,
                        result: { found: false, index: -1 },
                    },
                })
            );
            return steps;
        }

        // Check if sorted; sort if needed
        var wasSorted = isSortedAscending(arr);
        if (!wasSorted) {
            arr.sort(function (a, b) {
                return a - b;
            });
            stepNum++;
            steps.push(
                makeStep({
                    array: arr.slice(),
                    current: null,
                    checked: [],
                    found: null,
                    notFound: false,
                    low: 0,
                    mid: null,
                    high: arr.length - 1,
                    active: rangeInclusive(0, arr.length - 1),
                    eliminated: [],
                    explanation:
                        'The array has been automatically sorted for Binary Search. Sorted array: [' +
                        arr.join(', ') +
                        ']. Now searching for target ' +
                        target +
                        '.',
                    pseudocodeLine: 0,
                    counters: {
                        comparisons: comparisons,
                        elementsExamined: elementsExamined,
                        step: stepNum,
                        result: null,
                    },
                })
            );
        }

        // Initial state step (always shown)
        stepNum++;
        steps.push(
            makeStep({
                array: arr.slice(),
                current: null,
                checked: [],
                found: null,
                notFound: false,
                low: 0,
                mid: null,
                high: arr.length - 1,
                active: rangeInclusive(0, arr.length - 1),
                eliminated: [],
                explanation:
                    'Starting Binary Search for target ' +
                    target +
                    ' in a sorted array of ' +
                    arr.length +
                    ' element' +
                    (arr.length === 1 ? '' : 's') +
                    '. Set low = 0, high = ' +
                    (arr.length - 1) +
                    '.',
                pseudocodeLine: 1,
                counters: {
                    comparisons: comparisons,
                    elementsExamined: elementsExamined,
                    step: stepNum,
                    result: null,
                },
            })
        );

        var low = 0;
        var high = arr.length - 1;
        var checked = [];

        while (low <= high) {
            var mid = Math.floor((low + high) / 2);
            comparisons++;
            elementsExamined++;
            stepNum++;

            var activeRange = rangeInclusive(low, high);

            if (arr[mid] === target) {
                // Found the target
                steps.push(
                    makeStep({
                        array: arr.slice(),
                        current: mid,
                        checked: checked.slice(),
                        found: mid,
                        notFound: false,
                        low: low,
                        mid: mid,
                        high: high,
                        active: activeRange,
                        eliminated: eliminated.slice(),
                        explanation:
                            'Compute mid = floor((' +
                            low +
                            ' + ' +
                            high +
                            ') / 2) = ' +
                            mid +
                            '. The middle element is ' +
                            arr[mid] +
                            '. Found target ' +
                            target +
                            ' at index ' +
                            mid +
                            '!',
                        pseudocodeLine: 6,
                        counters: {
                            comparisons: comparisons,
                            elementsExamined: elementsExamined,
                            step: stepNum,
                            result: { found: true, index: mid },
                        },
                    })
                );
                return steps;
            }

            if (arr[mid] < target) {
                // Target is in the right half
                var newEliminated = rangeInclusive(low, mid);
                for (var e = 0; e < newEliminated.length; e++) {
                    if (eliminated.indexOf(newEliminated[e]) === -1) {
                        eliminated.push(newEliminated[e]);
                    }
                }
                checked.push(mid);

                steps.push(
                    makeStep({
                        array: arr.slice(),
                        current: mid,
                        checked: checked.slice(),
                        found: null,
                        notFound: false,
                        low: low,
                        mid: mid,
                        high: high,
                        active: activeRange,
                        eliminated: eliminated.slice(),
                        explanation:
                            'Compute mid = floor((' +
                            low +
                            ' + ' +
                            high +
                            ') / 2) = ' +
                            mid +
                            '. The middle element is ' +
                            arr[mid] +
                            '. Since target ' +
                            target +
                            ' is greater than ' +
                            arr[mid] +
                            ', eliminate the left half and search right. Set low = ' +
                            (mid + 1) +
                            '.',
                        pseudocodeLine: 8,
                        counters: {
                            comparisons: comparisons,
                            elementsExamined: elementsExamined,
                            step: stepNum,
                            result: null,
                        },
                    })
                );

                low = mid + 1;
            } else {
                // Target is in the left half
                var newElimRight = rangeInclusive(mid, high);
                for (var r = 0; r < newElimRight.length; r++) {
                    if (eliminated.indexOf(newElimRight[r]) === -1) {
                        eliminated.push(newElimRight[r]);
                    }
                }
                checked.push(mid);

                steps.push(
                    makeStep({
                        array: arr.slice(),
                        current: mid,
                        checked: checked.slice(),
                        found: null,
                        notFound: false,
                        low: low,
                        mid: mid,
                        high: high,
                        active: activeRange,
                        eliminated: eliminated.slice(),
                        explanation:
                            'Compute mid = floor((' +
                            low +
                            ' + ' +
                            high +
                            ') / 2) = ' +
                            mid +
                            '. The middle element is ' +
                            arr[mid] +
                            '. Since target ' +
                            target +
                            ' is less than ' +
                            arr[mid] +
                            ', eliminate the right half and search left. Set high = ' +
                            (mid - 1) +
                            '.',
                        pseudocodeLine: 10,
                        counters: {
                            comparisons: comparisons,
                            elementsExamined: elementsExamined,
                            step: stepNum,
                            result: null,
                        },
                    })
                );

                high = mid - 1;
            }
        }

        // Not found
        stepNum++;
        steps.push(
            makeStep({
                array: arr.slice(),
                current: null,
                checked: checked.slice(),
                found: null,
                notFound: true,
                low: low,
                mid: null,
                high: high,
                active: [],
                eliminated: eliminated.slice(),
                explanation:
                    'low (' +
                    low +
                    ') > high (' +
                    high +
                    '). The search range is empty. Target ' +
                    target +
                    ' was not found in the array.',
                pseudocodeLine: 13,
                counters: {
                    comparisons: comparisons,
                    elementsExamined: elementsExamined,
                    step: stepNum,
                    result: { found: false, index: -1 },
                },
            })
        );

        return steps;
    }

    // ─────────────────────────────────────────────
    // Pseudocode definitions
    // ─────────────────────────────────────────────

    var pseudocode = {
        linearSearch: [
            'procedure linearSearch(A, target)',
            '  for i = 0 to length(A) - 1',
            '    if A[i] == target then',
            '      return i',
            '    end if',
            '  end for',
            '  return -1',
            'end procedure',
        ],
        binarySearch: [
            'procedure binarySearch(A, target)',
            '  low = 0',
            '  high = length(A) - 1',
            '  while low <= high',
            '    mid = floor((low + high) / 2)',
            '    if A[mid] == target then',
            '      return mid',
            '    else if A[mid] < target then',
            '      low = mid + 1',
            '    else',
            '      high = mid - 1',
            '    end if',
            '  end while',
            '  return -1',
            'end procedure',
        ],
    };

    // ─────────────────────────────────────────────
    // Complexity information
    // ─────────────────────────────────────────────

    var complexityInfo = {
        linearSearch: {
            name: 'Linear Search',
            description:
                'Linear Search sequentially checks each element of the list until a match is found or the whole list has been searched.',
            best: 'O(1)',
            average: 'O(n)',
            worst: 'O(n)',
            space: 'O(1)',
            requiresSorted: false,
            whenToUse:
                'Small or unsorted datasets, linked lists, or when the data is searched only once.',
        },
        binarySearch: {
            name: 'Binary Search',
            description:
                'Binary Search works on sorted arrays by repeatedly dividing the search interval in half. It compares the target with the middle element and eliminates half the remaining elements each step.',
            best: 'O(1)',
            average: 'O(log n)',
            worst: 'O(log n)',
            space: 'O(1)',
            requiresSorted: true,
            whenToUse:
                'Large sorted datasets where fast lookup is needed. Much more efficient than linear search for sorted data.',
        },
    };

    // ─────────────────────────────────────────────
    // Public API
    // ─────────────────────────────────────────────

    window.SearchingAlgorithms = {
        linearSearch: linearSearch,
        binarySearch: binarySearch,
        pseudocode: pseudocode,
        complexityInfo: complexityInfo,
    };
})();
