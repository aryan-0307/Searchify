/**
 * sorting-algorithms.js
 * =====================
 * Provides all sorting algorithm logic for the AlgoViz educational visualizer.
 * Generates step-by-step trace data that the UI renders for interactive learning.
 *
 * Algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort
 *
 * Attached to: window.SortingAlgorithms
 */
(function () {
    'use strict';

    // ───────────────────────────────────────────────────────────
    // Helpers
    // ───────────────────────────────────────────────────────────

    /**
     * Build a step object with consistent shape.
     */
    function makeStep(arr, comparing, swapping, sorted, pivot, explanation, pseudocodeLine, counters, auxiliary) {
        return {
            array: [...arr],
            comparing: [...comparing],
            swapping: [...swapping],
            sorted: [...sorted],
            pivot: [...pivot],
            explanation: explanation,
            pseudocodeLine: pseudocodeLine,
            counters: {
                comparisons: counters.comparisons,
                swaps: counters.swaps,
                step: counters.step
            },
            auxiliary: auxiliary ? JSON.parse(JSON.stringify(auxiliary)) : null
        };
    }

    /**
     * Returns true when a should come before b given the order.
     * For ascending: a < b  → already in order, no swap needed.
     * We check the "wrong order" condition: should we swap?
     */
    function outOfOrder(a, b, order) {
        return order === 'asc' ? a > b : a < b;
    }

    /**
     * Human-friendly comparison operator string.
     */
    function cmpSymbol(order) {
        return order === 'asc' ? '>' : '<';
    }

    /**
     * Inverse comparison word for explanations when elements are already in order.
     */
    function inOrderSymbol(order) {
        return order === 'asc' ? '≤' : '≥';
    }

    // ───────────────────────────────────────────────────────────
    // 1. BUBBLE SORT
    // ───────────────────────────────────────────────────────────

    function bubbleSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const sorted = [];

        // Edge cases
        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Bubble Sort. Array is already sorted.', 0, counters));
            return steps;
        }

        // Initial state
        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], 'Starting Bubble Sort. Compare adjacent elements and swap if they are in the wrong order.', 0, counters));

        for (let i = 0; i < n - 1; i++) {
            let swapped = false;

            // Start of pass
            counters.step++;
            steps.push(makeStep(arr, [], [], [...sorted], [], `Pass ${i + 1}: Iterate through the unsorted portion (indices 0 to ${n - i - 2}).`, 1, counters));

            for (let j = 0; j < n - i - 1; j++) {
                // Comparing
                counters.comparisons++;
                counters.step++;
                steps.push(makeStep(arr, [j, j + 1], [], [...sorted], [], `Compare ${arr[j]} and ${arr[j + 1]} at indices ${j} and ${j + 1}.`, 4, counters));

                if (outOfOrder(arr[j], arr[j + 1], order)) {
                    // Swap
                    counters.swaps++;
                    const tmp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = tmp;
                    swapped = true;

                    counters.step++;
                    steps.push(makeStep(arr, [], [j, j + 1], [...sorted], [], `Since ${arr[j + 1]} ${cmpSymbol(order)} ${arr[j]}, swap their positions.`, 5, counters));
                } else {
                    counters.step++;
                    steps.push(makeStep(arr, [j, j + 1], [], [...sorted], [], `${arr[j]} ${inOrderSymbol(order)} ${arr[j + 1]}, no swap needed.`, 7, counters));
                }
            }

            // Mark last unsorted position as sorted
            sorted.push(n - 1 - i);
            counters.step++;
            steps.push(makeStep(arr, [], [], [...sorted], [], `End of pass ${i + 1}. Element ${arr[n - 1 - i]} at index ${n - 1 - i} is now in its final position.`, 8, counters));

            if (!swapped) {
                // Early termination — mark all remaining as sorted
                for (let k = 0; k < n; k++) {
                    if (!sorted.includes(k)) sorted.push(k);
                }
                sorted.sort((a, b) => a - b);
                counters.step++;
                steps.push(makeStep(arr, [], [], [...sorted], [], 'No swaps occurred in this pass. Array is sorted — early termination!', 9, counters));
                return steps;
            }
        }

        // Mark index 0 as sorted (last remaining)
        if (!sorted.includes(0)) sorted.push(0);
        sorted.sort((a, b) => a - b);

        counters.step++;
        steps.push(makeStep(arr, [], [], [...sorted], [], 'Bubble Sort complete. All elements are in their final positions.', 11, counters));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 2. SELECTION SORT
    // ───────────────────────────────────────────────────────────

    function selectionSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const sorted = [];

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Selection Sort. Array is already sorted.', 0, counters));
            return steps;
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], `Starting Selection Sort. Repeatedly find the ${order === 'asc' ? 'minimum' : 'maximum'} element and place it at the beginning of the unsorted portion.`, 0, counters));

        for (let i = 0; i < n - 1; i++) {
            let extremeIdx = i;

            // Show starting search
            counters.step++;
            steps.push(makeStep(arr, [], [], [...sorted], [i], `Pass ${i + 1}: Find the ${order === 'asc' ? 'minimum' : 'maximum'} in the unsorted portion (indices ${i} to ${n - 1}). Current ${order === 'asc' ? 'minimum' : 'maximum'}: ${arr[i]} at index ${i}.`, 2, counters));

            for (let j = i + 1; j < n; j++) {
                counters.comparisons++;
                counters.step++;
                steps.push(makeStep(arr, [extremeIdx, j], [], [...sorted], [i], `Compare current ${order === 'asc' ? 'minimum' : 'maximum'} ${arr[extremeIdx]} (index ${extremeIdx}) with ${arr[j]} (index ${j}).`, 4, counters));

                if (outOfOrder(arr[extremeIdx], arr[j], order)) {
                    extremeIdx = j;
                    counters.step++;
                    steps.push(makeStep(arr, [extremeIdx], [], [...sorted], [i], `New ${order === 'asc' ? 'minimum' : 'maximum'} found: ${arr[extremeIdx]} at index ${extremeIdx}.`, 5, counters));
                }
            }

            if (extremeIdx !== i) {
                counters.swaps++;
                const tmp = arr[i];
                arr[i] = arr[extremeIdx];
                arr[extremeIdx] = tmp;

                counters.step++;
                steps.push(makeStep(arr, [], [i, extremeIdx], [...sorted], [], `The ${order === 'asc' ? 'minimum' : 'maximum'} value in the unsorted portion is ${arr[i]} (was at index ${extremeIdx}). Swap it with position ${i}.`, 8, counters));
            } else {
                counters.step++;
                steps.push(makeStep(arr, [], [], [...sorted], [], `The ${order === 'asc' ? 'minimum' : 'maximum'} ${arr[i]} is already at position ${i}. No swap needed.`, 8, counters));
            }

            sorted.push(i);
            counters.step++;
            steps.push(makeStep(arr, [], [], [...sorted], [], `Element ${arr[i]} is now in its final position at index ${i}.`, 9, counters));
        }

        // Last element is automatically sorted
        sorted.push(n - 1);
        counters.step++;
        steps.push(makeStep(arr, [], [], [...sorted], [], 'Selection Sort complete. All elements are in their final positions.', 10, counters));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 3. INSERTION SORT
    // ───────────────────────────────────────────────────────────

    function insertionSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const sorted = [];

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Insertion Sort. Array is already sorted.', 0, counters));
            return steps;
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], 'Starting Insertion Sort. Build the sorted portion one element at a time by inserting each element into its correct position.', 0, counters));

        // First element is trivially sorted
        sorted.push(0);
        counters.step++;
        steps.push(makeStep(arr, [], [], [...sorted], [], `Element ${arr[0]} at index 0 is the first element, so it is trivially sorted.`, 1, counters));

        for (let i = 1; i < n; i++) {
            const key = arr[i];
            let j = i - 1;

            // Pick element
            counters.step++;
            steps.push(makeStep(arr, [i], [], [...sorted], [], `Pick element ${key} at index ${i} to insert into the sorted portion.`, 2, counters));

            let shifted = false;
            const shiftedIndices = [];

            while (j >= 0) {
                counters.comparisons++;
                counters.step++;
                steps.push(makeStep(arr, [j, j + 1], [], [...sorted], [], `Compare ${key} with ${arr[j]} at index ${j}.`, 4, counters));

                if (outOfOrder(arr[j], key, order)) {
                    // Shift
                    counters.swaps++;
                    arr[j + 1] = arr[j];
                    shiftedIndices.push(j + 1);
                    shifted = true;

                    counters.step++;
                    steps.push(makeStep(arr, [], [j, j + 1], [...sorted], [], `${arr[j + 1]} ${cmpSymbol(order)} ${key}, shift ${arr[j + 1]} to index ${j + 1}.`, 5, counters));

                    j--;
                } else {
                    counters.step++;
                    steps.push(makeStep(arr, [], [], [...sorted], [], `${arr[j]} ${inOrderSymbol(order)} ${key}, found the correct insertion position.`, 7, counters));
                    break;
                }
            }

            // Insert
            arr[j + 1] = key;
            sorted.push(i);
            sorted.sort((a, b) => a - b);

            counters.step++;
            if (shifted) {
                steps.push(makeStep(arr, [], [j + 1], [...sorted], [], `Insert ${key} at index ${j + 1}. The sorted portion now has ${sorted.length} elements.`, 8, counters));
            } else {
                steps.push(makeStep(arr, [], [], [...sorted], [], `${key} is already in its correct position at index ${j + 1}. The sorted portion now has ${sorted.length} elements.`, 8, counters));
            }
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [...sorted], [], 'Insertion Sort complete. All elements are in their final positions.', 10, counters));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 4. MERGE SORT
    // ───────────────────────────────────────────────────────────

    function mergeSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Merge Sort. Array is already sorted.', 0, counters));
            return steps;
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], 'Starting Merge Sort. Recursively divide the array into halves, then merge them back in sorted order.', 0, counters));

        // We use a recursive approach but track everything on the full array.
        const finalSorted = [];

        function mergeSortRecursive(left, right) {
            if (left >= right) return;

            const mid = Math.floor((left + right) / 2);

            // Show dividing
            const divideIndices = [];
            for (let i = left; i <= right; i++) divideIndices.push(i);

            counters.step++;
            steps.push(makeStep(arr, divideIndices, [], [...finalSorted], [], `Divide sub-array [${left}..${right}] into [${left}..${mid}] and [${mid + 1}..${right}].`, 2, counters));

            mergeSortRecursive(left, mid);
            mergeSortRecursive(mid + 1, right);
            merge(left, mid, right);
        }

        function merge(left, mid, right) {
            // Show merge start
            const mergeIndices = [];
            for (let i = left; i <= right; i++) mergeIndices.push(i);

            counters.step++;
            steps.push(makeStep(arr, [], [], [...finalSorted], mergeIndices, `Merge sub-arrays [${left}..${mid}] and [${mid + 1}..${right}].`, 7, counters));

            const leftArr = arr.slice(left, mid + 1);
            const rightArr = arr.slice(mid + 1, right + 1);

            let i = 0;
            let j = 0;
            let k = left;

            while (i < leftArr.length && j < rightArr.length) {
                counters.comparisons++;

                const leftIdx = left + i;
                const rightIdx = mid + 1 + j;

                counters.step++;
                steps.push(makeStep(arr, [leftIdx, rightIdx], [], [...finalSorted], mergeIndices, `Compare ${leftArr[i]} (left sub-array) with ${rightArr[j]} (right sub-array).`, 9, counters));

                if (!outOfOrder(leftArr[i], rightArr[j], order)) {
                    // leftArr[i] goes first
                    arr[k] = leftArr[i];
                    counters.swaps++;

                    counters.step++;
                    steps.push(makeStep(arr, [], [k], [...finalSorted], mergeIndices, `${leftArr[i]} ${inOrderSymbol(order)} ${rightArr[j]}, place ${leftArr[i]} at index ${k}.`, 10, counters));
                    i++;
                } else {
                    // rightArr[j] goes first
                    arr[k] = rightArr[j];
                    counters.swaps++;

                    counters.step++;
                    steps.push(makeStep(arr, [], [k], [...finalSorted], mergeIndices, `${rightArr[j]} comes before ${leftArr[i]}, place ${rightArr[j]} at index ${k}.`, 12, counters));
                    j++;
                }
                k++;
            }

            // Remaining elements from left sub-array
            while (i < leftArr.length) {
                arr[k] = leftArr[i];
                counters.swaps++;

                counters.step++;
                steps.push(makeStep(arr, [], [k], [...finalSorted], mergeIndices, `Copy remaining element ${leftArr[i]} from left sub-array to index ${k}.`, 14, counters));
                i++;
                k++;
            }

            // Remaining elements from right sub-array
            while (j < rightArr.length) {
                arr[k] = rightArr[j];
                counters.swaps++;

                counters.step++;
                steps.push(makeStep(arr, [], [k], [...finalSorted], mergeIndices, `Copy remaining element ${rightArr[j]} from right sub-array to index ${k}.`, 14, counters));
                j++;
                k++;
            }

            // If this merge covers the full range down to a single-element level,
            // mark elements as in final position when the full array merge completes.
            if (left === 0 && right === n - 1) {
                for (let idx = left; idx <= right; idx++) {
                    if (!finalSorted.includes(idx)) finalSorted.push(idx);
                }
            }

            counters.step++;
            steps.push(makeStep(arr, [], [], [...finalSorted], mergeIndices, `Merge of [${left}..${right}] complete. Sub-array is now sorted.`, 15, counters));
        }

        mergeSortRecursive(0, n - 1);

        // Final step — all sorted
        const allIndices = [];
        for (let i = 0; i < n; i++) allIndices.push(i);

        counters.step++;
        steps.push(makeStep(arr, [], [], allIndices, [], 'Merge Sort complete. All elements are in their final positions.', 15, counters));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 5. QUICK SORT
    // ───────────────────────────────────────────────────────────

    function quickSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const finalSorted = [];

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Quick Sort. Array is already sorted.', 0, counters));
            return steps;
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], 'Starting Quick Sort. Choose a pivot, partition the array, then recursively sort each partition.', 0, counters));

        function quickSortRecursive(low, high) {
            if (low > high) return;

            if (low === high) {
                // Single element — sorted
                if (!finalSorted.includes(low)) finalSorted.push(low);
                counters.step++;
                steps.push(makeStep(arr, [], [], [...finalSorted], [], `Sub-array [${low}..${high}] has one element (${arr[low]}). It is already sorted.`, 1, counters));
                return;
            }

            // Partition
            const pivotVal = arr[high];
            counters.step++;
            steps.push(makeStep(arr, [], [], [...finalSorted], [high], `Partition [${low}..${high}]. Pivot is ${pivotVal} (last element, index ${high}).`, 6, counters));

            let i = low - 1;

            for (let j = low; j < high; j++) {
                counters.comparisons++;
                counters.step++;
                steps.push(makeStep(arr, [j], [], [...finalSorted], [high], `Compare ${arr[j]} at index ${j} with pivot ${pivotVal}.`, 9, counters));

                if (!outOfOrder(arr[j], pivotVal, order)) {
                    // arr[j] should go to the left side of pivot
                    i++;
                    if (i !== j) {
                        counters.swaps++;
                        const tmp = arr[i];
                        arr[i] = arr[j];
                        arr[j] = tmp;

                        counters.step++;
                        steps.push(makeStep(arr, [], [i, j], [...finalSorted], [high], `${arr[i]} ${inOrderSymbol(order)} ${pivotVal}, swap elements at indices ${i} and ${j}.`, 10, counters));
                    } else {
                        counters.step++;
                        steps.push(makeStep(arr, [], [], [...finalSorted], [high], `${arr[i]} ${inOrderSymbol(order)} ${pivotVal}, element is already in the correct partition.`, 10, counters));
                    }
                } else {
                    counters.step++;
                    steps.push(makeStep(arr, [j], [], [...finalSorted], [high], `${arr[j]} ${cmpSymbol(order)} ${pivotVal}, it stays on the ${order === 'asc' ? 'right' : 'left'} side.`, 11, counters));
                }
            }

            // Place pivot in correct position
            const pivotIdx = i + 1;
            if (pivotIdx !== high) {
                counters.swaps++;
                const tmp = arr[pivotIdx];
                arr[pivotIdx] = arr[high];
                arr[high] = tmp;

                counters.step++;
                steps.push(makeStep(arr, [], [pivotIdx, high], [...finalSorted], [pivotIdx], `Place pivot ${pivotVal} in its correct position at index ${pivotIdx}.`, 12, counters));
            } else {
                counters.step++;
                steps.push(makeStep(arr, [], [], [...finalSorted], [pivotIdx], `Pivot ${pivotVal} is already in its correct position at index ${pivotIdx}.`, 12, counters));
            }

            // Mark pivot as sorted
            if (!finalSorted.includes(pivotIdx)) finalSorted.push(pivotIdx);
            counters.step++;
            steps.push(makeStep(arr, [], [], [...finalSorted], [pivotIdx], `Pivot ${pivotVal} is now at its final position (index ${pivotIdx}). Elements to the left are ${order === 'asc' ? 'smaller' : 'larger'}, elements to the right are ${order === 'asc' ? 'larger' : 'smaller'}.`, 13, counters));

            // Recurse
            quickSortRecursive(low, pivotIdx - 1);
            quickSortRecursive(pivotIdx + 1, high);
        }

        quickSortRecursive(0, n - 1);

        // Final step
        const allIndices = [];
        for (let i = 0; i < n; i++) allIndices.push(i);

        counters.step++;
        steps.push(makeStep(arr, [], [], allIndices, [], 'Quick Sort complete. All elements are in their final positions.', 14, counters));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 6. HEAP SORT
    // ───────────────────────────────────────────────────────────

    function heapSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const sorted = [];

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Heap Sort. Array is already sorted.', 0, counters, {
                type: 'heapTree',
                heapSize: n,
                activeParent: null,
                activeChildren: [],
                phase: 'done'
            }));
            return steps;
        }

        const isMaxHeap = order === 'asc';
        const heapTypeName = isMaxHeap ? 'Max-Heap' : 'Min-Heap';

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], `Starting Heap Sort. First, build a ${heapTypeName} from the array so the root element is always the ${isMaxHeap ? 'maximum' : 'minimum'}.`, 0, counters, {
            type: 'heapTree',
            heapSize: n,
            activeParent: null,
            activeChildren: [],
            phase: 'build'
        }));

        function heapViolates(childVal, parentVal) {
            return isMaxHeap ? childVal > parentVal : childVal < parentVal;
        }

        function heapify(size, i) {
            let extreme = i;
            const left = 2 * i + 1;
            const right = 2 * i + 2;
            const comparedChildren = [];

            if (left < size) comparedChildren.push(left);
            if (right < size) comparedChildren.push(right);

            if (comparedChildren.length > 0) {
                counters.comparisons++;
                counters.step++;
                steps.push(makeStep(arr, [i, ...comparedChildren], [], [...sorted], [], `Heapify at node ${i} (${arr[i]}): checking children [${comparedChildren.map(c => `node ${c}: ${arr[c]}`).join(', ')}].`, 8, counters, {
                    type: 'heapTree',
                    heapSize: size,
                    activeParent: i,
                    activeChildren: comparedChildren,
                    phase: 'heapify'
                }));
            }

            if (left < size) {
                counters.comparisons++;
                if (heapViolates(arr[left], arr[extreme])) {
                    extreme = left;
                }
            }

            if (right < size) {
                counters.comparisons++;
                if (heapViolates(arr[right], arr[extreme])) {
                    extreme = right;
                }
            }

            if (extreme !== i) {
                counters.swaps++;
                const tmp = arr[i];
                arr[i] = arr[extreme];
                arr[extreme] = tmp;

                counters.step++;
                steps.push(makeStep(arr, [], [i, extreme], [...sorted], [], `Swap parent node ${i} (${arr[extreme]}) with child node ${extreme} (${arr[i]}) to maintain ${heapTypeName} invariant.`, 11, counters, {
                    type: 'heapTree',
                    heapSize: size,
                    activeParent: extreme,
                    activeChildren: [],
                    phase: 'heapify'
                }));

                heapify(size, extreme);
            }
        }

        // Build Heap (bottom-up from last non-leaf node down to root)
        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], `Phase 1: Sift down from index ${Math.floor(n / 2) - 1} down to 0 to construct initial ${heapTypeName}.`, 1, counters, {
            type: 'heapTree',
            heapSize: n,
            activeParent: Math.floor(n / 2) - 1,
            activeChildren: [],
            phase: 'build'
        }));

        for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
            heapify(n, i);
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [0], `${heapTypeName} successfully built! Root element ${arr[0]} is the ${isMaxHeap ? 'largest' : 'smallest'} in the active heap.`, 1, counters, {
            type: 'heapTree',
            heapSize: n,
            activeParent: 0,
            activeChildren: [],
            phase: 'built'
        }));

        // Extract elements one by one from heap
        for (let i = n - 1; i > 0; i--) {
            counters.swaps++;
            const tmp = arr[0];
            arr[0] = arr[i];
            arr[i] = tmp;
            sorted.push(i);

            counters.step++;
            steps.push(makeStep(arr, [], [0, i], [...sorted], [], `Extract root ${tmp}: swap with element at position ${i}. Element ${tmp} is now locked in its final sorted position.`, 3, counters, {
                type: 'heapTree',
                heapSize: i,
                activeParent: 0,
                activeChildren: [],
                extracted: tmp,
                phase: 'extract'
            }));

            // Restore heap on reduced size i
            heapify(i, 0);
        }

        if (!sorted.includes(0)) sorted.push(0);
        sorted.sort((a, b) => a - b);

        counters.step++;
        steps.push(makeStep(arr, [], [], [...sorted], [], 'Heap Sort complete. All elements are in their final positions.', 5, counters, {
            type: 'heapTree',
            heapSize: 0,
            activeParent: null,
            activeChildren: [],
            phase: 'done'
        }));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 7. SHELL SORT
    // ───────────────────────────────────────────────────────────

    function shellSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const sorted = [];

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Shell Sort. Array is already sorted.', 0, counters, {
                type: 'shellSort',
                gap: 1,
                gapSequence: [1],
                isFinalPass: true
            }));
            return steps;
        }

        // Build gap sequence: Shell's classic sequence (floor(n/2) down to 1)
        const gapSeq = [];
        let g = Math.floor(n / 2);
        while (g > 0) {
            gapSeq.push(g);
            g = Math.floor(g / 2);
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], `Starting Shell Sort. Selected gap sequence: [${gapSeq.join(', ')}]. Gap sorting enables elements to leap over multiple positions at once.`, 0, counters, {
            type: 'shellSort',
            gap: gapSeq[0],
            gapSequence: gapSeq,
            gapIndex: 0,
            isFinalPass: gapSeq[0] === 1
        }));

        for (let gIdx = 0; gIdx < gapSeq.length; gIdx++) {
            const gap = gapSeq[gIdx];
            const isFinalPass = (gap === 1);

            counters.step++;
            steps.push(makeStep(arr, [], [], [...sorted], [], isFinalPass ?
                'Final pass: gap = 1. Performing insertion sort on the nearly sorted array for fast linear-time completion.' :
                `Beginning pass with gap = ${gap}. Comparing and sorting sub-arrays of elements spaced ${gap} apart.`,
                1, counters, {
                type: 'shellSort',
                gap: gap,
                gapSequence: gapSeq,
                gapIndex: gIdx,
                isFinalPass: isFinalPass
            }));

            // Perform gap-based insertion sort
            for (let i = gap; i < n; i++) {
                counters.step++;
                steps.push(makeStep(arr, [i], [], [...sorted], [], `Inspect element ${arr[i]} at index ${i} with gap = ${gap}.`, 2, counters, {
                    type: 'shellSort',
                    gap: gap,
                    gapSequence: gapSeq,
                    gapIndex: gIdx,
                    isFinalPass: isFinalPass
                }));

                for (let j = i; j >= gap; j -= gap) {
                    counters.comparisons++;
                    counters.step++;
                    steps.push(makeStep(arr, [j - gap, j], [], [...sorted], [], `Compare elements separated by gap ${gap}: arr[${j - gap}] (${arr[j - gap]}) and arr[${j}] (${arr[j]}).`, 4, counters, {
                        type: 'shellSort',
                        gap: gap,
                        gapSequence: gapSeq,
                        gapIndex: gIdx,
                        isFinalPass: isFinalPass,
                        comparedPair: [j - gap, j]
                    }));

                    if (outOfOrder(arr[j - gap], arr[j], order)) {
                        counters.swaps++;
                        const tmp = arr[j];
                        arr[j] = arr[j - gap];
                        arr[j - gap] = tmp;

                        counters.step++;
                        steps.push(makeStep(arr, [], [j - gap, j], [...sorted], [], `Since ${arr[j]} ${cmpSymbol(order)} ${arr[j - gap]}, swap elements over gap ${gap}.`, 5, counters, {
                            type: 'shellSort',
                            gap: gap,
                            gapSequence: gapSeq,
                            gapIndex: gIdx,
                            isFinalPass: isFinalPass,
                            comparedPair: [j - gap, j]
                        }));
                    } else {
                        counters.step++;
                        steps.push(makeStep(arr, [j - gap, j], [], [...sorted], [], `Elements ${arr[j - gap]} ${inOrderSymbol(order)} ${arr[j]} are in correct relative order for gap ${gap}.`, 7, counters, {
                            type: 'shellSort',
                            gap: gap,
                            gapSequence: gapSeq,
                            gapIndex: gIdx,
                            isFinalPass: isFinalPass
                        }));
                        break;
                    }
                }
            }
        }

        const allIndices = [];
        for (let i = 0; i < n; i++) allIndices.push(i);

        counters.step++;
        steps.push(makeStep(arr, [], [], allIndices, [], 'Shell Sort complete. Array is completely sorted.', 10, counters, {
            type: 'shellSort',
            gap: 1,
            gapSequence: gapSeq,
            gapIndex: gapSeq.length - 1,
            isFinalPass: true
        }));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 8. COUNTING SORT
    // ───────────────────────────────────────────────────────────

    function countingSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const sorted = [];

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Counting Sort. Array is already sorted.', 0, counters, {
                type: 'countingSort',
                phase: 'done',
                counts: [],
                outputArray: [...arr]
            }));
            return steps;
        }

        let minVal = arr[0];
        let maxVal = arr[0];
        for (let i = 1; i < n; i++) {
            if (arr[i] < minVal) minVal = arr[i];
            if (arr[i] > maxVal) maxVal = arr[i];
        }

        if (minVal === maxVal) {
            const allIdx = [];
            for (let i = 0; i < n; i++) allIdx.push(i);
            counters.step++;
            steps.push(makeStep(arr, [], [], allIdx, [], `All elements are identical (${minVal}). Array is already sorted.`, 0, counters, {
                type: 'countingSort',
                phase: 'done',
                counts: [n],
                minVal,
                maxVal,
                outputArray: [...arr]
            }));
            return steps;
        }

        const offset = -minVal;
        const k = maxVal - minVal + 1;
        const count = new Array(k).fill(0);
        const output = new Array(n).fill(null);

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], `Starting Counting Sort. Min: ${minVal}, Max: ${maxVal}, Range k: ${k}${minVal < 0 ? ` (Negative offset: ${offset})` : ''}. Initializing count array of size ${k}.`, 1, counters, {
            type: 'countingSort',
            phase: 'init',
            minVal,
            maxVal,
            offset,
            counts: [...count],
            outputArray: [...output]
        }));

        // 1. Frequency counting
        for (let i = 0; i < n; i++) {
            const val = arr[i];
            const cIdx = val + offset;
            count[cIdx]++;
            counters.step++;
            steps.push(makeStep(arr, [i], [], [], [], `Count frequency of ${val} at index ${i}: increment count[${val}] to ${count[cIdx]}.`, 4, counters, {
                type: 'countingSort',
                phase: 'count',
                minVal,
                maxVal,
                offset,
                activeCountIndex: cIdx,
                activeValue: val,
                counts: [...count],
                outputArray: [...output]
            }));
        }

        // 2. Cumulative counts (prefix sums)
        if (order === 'asc') {
            for (let c = 1; c < k; c++) {
                count[c] += count[c - 1];
                counters.step++;
                steps.push(makeStep(arr, [], [], [], [], `Cumulative prefix sum: count for value ${c + minVal} becomes ${count[c]} (ending position: ${count[c] - 1}).`, 6, counters, {
                    type: 'countingSort',
                    phase: 'cumulative',
                    minVal,
                    maxVal,
                    offset,
                    activeCountIndex: c,
                    counts: [...count],
                    outputArray: [...output]
                }));
            }
        } else {
            for (let c = k - 2; c >= 0; c--) {
                count[c] += count[c + 1];
                counters.step++;
                steps.push(makeStep(arr, [], [], [], [], `Cumulative descending sum: count for value ${c + minVal} becomes ${count[c]} (ending position: ${count[c] - 1}).`, 6, counters, {
                    type: 'countingSort',
                    phase: 'cumulative',
                    minVal,
                    maxVal,
                    offset,
                    activeCountIndex: c,
                    counts: [...count],
                    outputArray: [...output]
                }));
            }
        }

        // 3. Build output array stably from right to left
        const workingCounts = [...count];

        for (let i = n - 1; i >= 0; i--) {
            const val = arr[i];
            const cIdx = val + offset;
            const pos = workingCounts[cIdx] - 1;
            output[pos] = val;
            workingCounts[cIdx]--;

            counters.swaps++;
            counters.step++;
            steps.push(makeStep(arr, [], [i], [], [], `Place element ${val} (from index ${i}) into ${order === 'asc' ? 'sorted' : 'descending'} output array at position ${pos}.`, 8, counters, {
                type: 'countingSort',
                phase: 'output',
                minVal,
                maxVal,
                offset,
                activeCountIndex: cIdx,
                activeOutputIndex: pos,
                counts: [...workingCounts],
                outputArray: [...output]
            }));
        }

        // 4. Copy sorted output back into original array
        for (let i = 0; i < n; i++) {
            arr[i] = output[i];
            sorted.push(i);
            counters.step++;
            steps.push(makeStep(arr, [], [], [...sorted], [], `Copy element ${arr[i]} from output into final array at index ${i}.`, 10, counters, {
                type: 'countingSort',
                phase: 'copy',
                minVal,
                maxVal,
                offset,
                counts: [...workingCounts],
                outputArray: [...output]
            }));
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [...sorted], [], 'Counting Sort complete. All elements are sorted in linear O(n + k) time.', 11, counters, {
            type: 'countingSort',
            phase: 'done',
            minVal,
            maxVal,
            offset,
            counts: [...workingCounts],
            outputArray: [...arr]
        }));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 9. RADIX SORT (LSD)
    // ───────────────────────────────────────────────────────────

    function radixSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const sorted = [];

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Radix Sort. Array is already sorted.', 0, counters, {
                type: 'radixSort',
                phase: 'done',
                buckets: [[], [], [], [], [], [], [], [], [], []]
            }));
            return steps;
        }

        const hasNegatives = arr.some(x => x < 0);

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], `Starting LSD (Least Significant Digit) Radix Sort. Digit-by-digit stable bucket distribution from ones place upward.${hasNegatives ? ' Negative integers are partitioned by sign and stably sorted.' : ''}`, 0, counters, {
            type: 'radixSort',
            phase: 'init',
            buckets: [[], [], [], [], [], [], [], [], [], []]
        }));

        function getDigitPlaceName(exp) {
            if (exp === 1) return 'Ones (10⁰)';
            if (exp === 10) return 'Tens (10¹)';
            if (exp === 100) return 'Hundreds (10²)';
            if (exp === 1000) return 'Thousands (10³)';
            return `10^${Math.round(Math.log10(exp))} Place`;
        }

        function sortSubarrayByDigits(subArr) {
            if (subArr.length <= 1) return subArr;
            const maxVal = Math.max(...subArr.map(x => Math.abs(x)));
            const totalPasses = Math.max(1, Math.floor(Math.log10(maxVal || 1)) + 1);

            let current = [...subArr];
            let pass = 1;

            for (let exp = 1; Math.floor(maxVal / exp) > 0; exp *= 10, pass++) {
                const placeName = getDigitPlaceName(exp);
                const buckets = Array.from({ length: 10 }, () => []);

                counters.step++;
                steps.push(makeStep(arr, [], [], [...sorted], [], `Pass ${pass}/${totalPasses}: Grouping elements by ${placeName} into 10 digit buckets (0–9).`, 2, counters, {
                    type: 'radixSort',
                    phase: 'passStart',
                    exp: exp,
                    digitPlace: placeName,
                    pass: pass,
                    totalPasses: totalPasses,
                    buckets: buckets.map(b => [...b])
                }));

                for (let i = 0; i < current.length; i++) {
                    const val = current[i];
                    const digit = Math.floor(Math.abs(val) / exp) % 10;
                    buckets[digit].push(val);

                    counters.swaps++;
                    counters.step++;
                    steps.push(makeStep(arr, [i], [], [...sorted], [], `Element ${val}: ${placeName} digit is ${digit} → distribute into Bucket ${digit}.`, 8, counters, {
                        type: 'radixSort',
                        phase: 'distribute',
                        exp: exp,
                        digitPlace: placeName,
                        pass: pass,
                        totalPasses: totalPasses,
                        activeBucket: digit,
                        activeItem: val,
                        activeDigit: digit,
                        buckets: buckets.map(b => [...b])
                    }));
                }

                current = [];
                for (let b = 0; b < 10; b++) {
                    for (let item of buckets[b]) {
                        current.push(item);
                    }
                }

                counters.step++;
                steps.push(makeStep(arr, [], [0], [...sorted], [], `Pass ${pass} complete: Collected elements stably from buckets 0 through 9.`, 9, counters, {
                    type: 'radixSort',
                    phase: 'collect',
                    exp: exp,
                    digitPlace: placeName,
                    pass: pass,
                    totalPasses: totalPasses,
                    buckets: buckets.map(b => [...b])
                }));
            }
            return current;
        }

        if (!hasNegatives) {
            const sortedValues = sortSubarrayByDigits(arr);
            if (order === 'desc') sortedValues.reverse();

            for (let i = 0; i < n; i++) {
                arr[i] = sortedValues[i];
                sorted.push(i);
            }
        } else {
            const negatives = arr.filter(x => x < 0);
            const positives = arr.filter(x => x >= 0);

            counters.step++;
            steps.push(makeStep(arr, [], [], [], [], `Partitioning into ${negatives.length} negative and ${positives.length} non-negative numbers for sign-separated digit sorting.`, 1, counters, {
                type: 'radixSort',
                phase: 'partition',
                buckets: [[], [], [], [], [], [], [], [], [], []]
            }));

            const sortedNegAbs = sortSubarrayByDigits(negatives.map(x => Math.abs(x)));
            const sortedNegatives = sortedNegAbs.reverse().map(x => -x);
            const sortedPositives = sortSubarrayByDigits(positives);

            let combined = [...sortedNegatives, ...sortedPositives];
            if (order === 'desc') combined.reverse();

            for (let i = 0; i < n; i++) {
                arr[i] = combined[i];
                sorted.push(i);
            }
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [...sorted], [], 'Radix Sort complete. All elements stably sorted across all digit places.', 10, counters, {
            type: 'radixSort',
            phase: 'done',
            buckets: [[], [], [], [], [], [], [], [], [], []]
        }));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // 10. BUCKET SORT
    // ───────────────────────────────────────────────────────────

    function bucketSort(inputArray, order) {
        const arr = [...inputArray];
        const n = arr.length;
        const steps = [];
        const counters = { comparisons: 0, swaps: 0, step: 0 };
        const sorted = [];

        if (n <= 1) {
            counters.step++;
            steps.push(makeStep(arr, [], [], n === 1 ? [0] : [], [], 'Starting Bucket Sort. Array is already sorted.', 0, counters, {
                type: 'bucketSort',
                phase: 'done',
                buckets: []
            }));
            return steps;
        }

        let minVal = arr[0];
        let maxVal = arr[0];
        for (let i = 1; i < n; i++) {
            if (arr[i] < minVal) minVal = arr[i];
            if (arr[i] > maxVal) maxVal = arr[i];
        }

        if (minVal === maxVal) {
            const allIdx = [];
            for (let i = 0; i < n; i++) allIdx.push(i);
            counters.step++;
            steps.push(makeStep(arr, [], [], allIdx, [], `All elements are identical (${minVal}). Array is already sorted.`, 0, counters, {
                type: 'bucketSort',
                phase: 'done',
                buckets: [[...arr]]
            }));
            return steps;
        }

        const k = Math.max(2, Math.min(n, 6));
        const range = (maxVal - minVal) / k;
        const buckets = Array.from({ length: k }, () => []);

        const bucketRanges = [];
        for (let b = 0; b < k; b++) {
            const low = minVal + b * range;
            const high = minVal + (b + 1) * range;
            bucketRanges.push(`${Math.round(low * 10) / 10}–${Math.round(high * 10) / 10}`);
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [], [], `Starting Bucket Sort. Created ${k} buckets covering range [${minVal} to ${maxVal}]. Step 1: Scatter elements into their respective buckets.`, 2, counters, {
            type: 'bucketSort',
            phase: 'init',
            numBuckets: k,
            bucketRanges: bucketRanges,
            buckets: buckets.map(b => [...b])
        }));

        // 1. Distribute elements into buckets
        for (let i = 0; i < n; i++) {
            const val = arr[i];
            let bIdx = Math.floor((val - minVal) / range);
            if (bIdx >= k) bIdx = k - 1;
            if (bIdx < 0) bIdx = 0;

            buckets[bIdx].push(val);
            counters.swaps++;
            counters.step++;
            steps.push(makeStep(arr, [i], [], [], [], `Scatter ${val} at index ${i} into Bucket ${bIdx} (range ${bucketRanges[bIdx]}).`, 5, counters, {
                type: 'bucketSort',
                phase: 'distribute',
                numBuckets: k,
                bucketRanges: bucketRanges,
                activeBucket: bIdx,
                activeItem: val,
                buckets: buckets.map(b => [...b])
            }));
        }

        // 2. Sort individual buckets using stable Insertion Sort
        for (let b = 0; b < k; b++) {
            const bLen = buckets[b].length;
            if (bLen > 1) {
                counters.step++;
                steps.push(makeStep(arr, [], [], [], [], `Sort Bucket ${b} (${bLen} elements: [${buckets[b].join(', ')}]) using Insertion Sort.`, 7, counters, {
                    type: 'bucketSort',
                    phase: 'sortBucket',
                    numBuckets: k,
                    bucketRanges: bucketRanges,
                    activeBucket: b,
                    buckets: buckets.map(bk => [...bk])
                }));

                for (let i = 1; i < bLen; i++) {
                    const key = buckets[b][i];
                    let j = i - 1;
                    while (j >= 0 && outOfOrder(buckets[b][j], key, order)) {
                        counters.comparisons++;
                        buckets[b][j + 1] = buckets[b][j];
                        j--;
                    }
                    buckets[b][j + 1] = key;
                }

                counters.step++;
                steps.push(makeStep(arr, [], [], [], [], `Bucket ${b} sorted: [${buckets[b].join(', ')}].`, 7, counters, {
                    type: 'bucketSort',
                    phase: 'sortedBucket',
                    numBuckets: k,
                    bucketRanges: bucketRanges,
                    activeBucket: b,
                    buckets: buckets.map(bk => [...bk])
                }));
            }
        }

        // 3. Concatenate buckets
        let writeIdx = 0;
        const bucketOrder = order === 'asc' ?
            Array.from({ length: k }, (_, i) => i) :
            Array.from({ length: k }, (_, i) => k - 1 - i);

        for (let b of bucketOrder) {
            for (let val of buckets[b]) {
                arr[writeIdx] = val;
                sorted.push(writeIdx);

                counters.swaps++;
                counters.step++;
                steps.push(makeStep(arr, [], [writeIdx], [...sorted], [], `Gather element ${val} from Bucket ${b} into final array at index ${writeIdx}.`, 8, counters, {
                    type: 'bucketSort',
                    phase: 'concatenate',
                    numBuckets: k,
                    bucketRanges: bucketRanges,
                    activeBucket: b,
                    activeOutputIndex: writeIdx,
                    buckets: buckets.map(bk => [...bk])
                }));
                writeIdx++;
            }
        }

        counters.step++;
        steps.push(makeStep(arr, [], [], [...sorted], [], 'Bucket Sort complete. All buckets concatenated into final sorted array.', 9, counters, {
            type: 'bucketSort',
            phase: 'done',
            numBuckets: k,
            bucketRanges: bucketRanges,
            buckets: buckets.map(bk => [...bk])
        }));

        return steps;
    }

    // ───────────────────────────────────────────────────────────
    // PSEUDOCODE
    // ───────────────────────────────────────────────────────────

    const pseudocode = {
        bubbleSort: [
            'procedure bubbleSort(A, n)',           // 0
            '  for i = 0 to n-2',                   // 1
            '    swapped = false',                   // 2
            '    for j = 0 to n-i-2',               // 3
            '      if A[j] > A[j+1] then',          // 4
            '        swap A[j] and A[j+1]',         // 5
            '        swapped = true',               // 6
            '      end if',                         // 7 (end of pass)
            '    end for',                          // 8
            '  if swapped = false then return',     // 9
            '  end for',                            // 10
            'end procedure'                         // 11
        ],
        selectionSort: [
            'procedure selectionSort(A, n)',         // 0
            '  for i = 0 to n-2',                   // 1
            '    minIdx = i',                        // 2
            '    for j = i+1 to n-1',               // 3
            '      if A[j] < A[minIdx] then',       // 4
            '        minIdx = j',                    // 5
            '      end if',                         // 6
            '    end for',                          // 7
            '    swap A[i] and A[minIdx]',          // 8
            '  end for',                            // 9
            'end procedure'                         // 10
        ],
        insertionSort: [
            'procedure insertionSort(A, n)',         // 0
            '  for i = 1 to n-1',                   // 1
            '    key = A[i]',                        // 2
            '    j = i - 1',                         // 3
            '    while j >= 0 and A[j] > key',      // 4
            '      A[j+1] = A[j]',                  // 5
            '      j = j - 1',                      // 6
            '    end while',                        // 7
            '    A[j+1] = key',                     // 8
            '  end for',                            // 9
            'end procedure'                         // 10
        ],
        mergeSort: [
            'procedure mergeSort(A, left, right)',   // 0
            '  if left < right then',               // 1
            '    mid = (left + right) / 2',         // 2
            '    mergeSort(A, left, mid)',           // 3
            '    mergeSort(A, mid+1, right)',        // 4
            '    merge(A, left, mid, right)',        // 5
            '  end if',                             // 6
            'procedure merge(A, left, mid, right)',  // 7
            '  while i < leftLen and j < rightLen', // 8
            '    if leftArr[i] ≤ rightArr[j]',      // 9
            '      A[k] = leftArr[i]; i++',         // 10
            '    else',                             // 11
            '      A[k] = rightArr[j]; j++',        // 12
            '    end if; k++',                      // 13
            '  copy remaining elements',            // 14
            'end procedure'                         // 15
        ],
        quickSort: [
            'procedure quickSort(A, low, high)',     // 0
            '  if low < high then',                 // 1
            '    pivotIdx = partition(A, low, high)',// 2
            '    quickSort(A, low, pivotIdx-1)',     // 3
            '    quickSort(A, pivotIdx+1, high)',    // 4
            'procedure partition(A, low, high)',     // 5
            '  pivot = A[high]',                    // 6
            '  i = low - 1',                        // 7
            '  for j = low to high-1',              // 8
            '    if A[j] ≤ pivot then',             // 9
            '      i++; swap A[i] and A[j]',        // 10
            '    end if',                           // 11
            '  swap A[i+1] and A[high]',            // 12
            '  return i + 1',                       // 13
            'end procedure'                         // 14
        ],
        heapSort: [
            'procedure heapSort(A, n)',             // 0
            '  buildHeap(A, n)',                    // 1
            '  for i = n-1 down to 1',              // 2
            '    swap A[0] and A[i]',               // 3
            '    heapify(A, i, 0)',                 // 4
            '  end for',                            // 5
            'procedure heapify(A, size, i)',        // 6
            '  extreme = i, left = 2*i+1, right = 2*i+2', // 7
            '  if left < size and A[left] violates A[extreme] then extreme = left', // 8
            '  if right < size and A[right] violates A[extreme] then extreme = right', // 9
            '  if extreme ≠ i then',                // 10
            '    swap A[i] and A[extreme]',         // 11
            '    heapify(A, size, extreme)',        // 12
            '  end if',                             // 13
            'end procedure'                         // 14
        ],
        shellSort: [
            'procedure shellSort(A, n)',             // 0
            '  for gap = floor(n/2) down to 1 by gap/2', // 1
            '    for i = gap to n-1',               // 2
            '      temp = A[i], j = i',             // 3
            '      while j >= gap and A[j-gap] > A[j]', // 4
            '        swap A[j] and A[j-gap]',       // 5
            '        j = j - gap',                  // 6
            '      end while',                      // 7
            '    end for',                          // 8
            '  end for',                            // 9
            'end procedure'                         // 10
        ],
        countingSort: [
            'procedure countingSort(A, n)',          // 0
            '  find min and max in A; offset = -min',// 1
            '  count = array of zeros of size (max - min + 1)', // 2
            '  for i = 0 to n-1',                    // 3
            '    count[A[i] + offset]++',            // 4
            '  for c = 1 to count.length-1',         // 5
            '    count[c] += count[c-1]',            // 6
            '  for i = n-1 down to 0',               // 7
            '    output[count[A[i] + offset] - 1] = A[i]', // 8
            '    count[A[i] + offset]--',            // 9
            '  copy output into A',                  // 10
            'end procedure'                          // 11
        ],
        radixSort: [
            'procedure radixSort(A, n)',             // 0
            '  maxVal = getMaximum(A)',              // 1
            '  for exp = 1; maxVal / exp > 0; exp *= 10', // 2
            '    countSortByDigit(A, n, exp)',       // 3
            'procedure countSortByDigit(A, n, exp)', // 4
            '  initialize 10 digit buckets (0 to 9)',// 5
            '  for i = 0 to n-1',                    // 6
            '    digit = floor(abs(A[i]) / exp) % 10', // 7
            '    buckets[digit].push(A[i])',         // 8
            '  A = flatten buckets sequentially',    // 9
            'end procedure'                          // 10
        ],
        bucketSort: [
            'procedure bucketSort(A, n, k)',         // 0
            '  find min and max in A',               // 1
            '  create k empty buckets',              // 2
            '  for i = 0 to n-1',                    // 3
            '    bIdx = floor(k * (A[i] - min) / (max - min))', // 4
            '    buckets[bIdx].push(A[i])',          // 5
            '  for b = 0 to k-1',                    // 6
            '    insertionSort(buckets[b])',         // 7
            '  concatenate sorted buckets into A',   // 8
            'end procedure'                          // 9
        ]
    };

    // ───────────────────────────────────────────────────────────
    // COMPLEXITY INFO
    // ───────────────────────────────────────────────────────────

    const complexityInfo = {
        bubbleSort: {
            name: 'Bubble Sort',
            description: 'A simple comparison-based algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. Named because smaller elements gradually "bubble" to the top.',
            howItWorks: 'Iterates repeatedly through the array. In each pass, adjacent pairs (A[j] and A[j+1]) are compared and swapped if unordered. After pass k, the k-th largest element is locked into its final position at the end. An early termination check terminates execution if a pass completes with zero swaps.',
            best: 'O(n) optimized',
            average: 'O(n²)',
            worst: 'O(n²)',
            space: 'O(1)',
            stable: true,
            inPlace: true,
            whenToUse: 'Educational demonstrations and checking if an array is already sorted. Not suitable for large production datasets due to quadratic comparison count.',
            observations: 'Very high number of writes/swaps. Performs O(n²) operations even when partially sorted unless early exit triggers.',
            keyDifferences: 'Compares only adjacent neighbors (distance = 1). Unlike Shell Sort which compares across large gaps, or Quick/Merge Sort which divide recursively.'
        },
        selectionSort: {
            name: 'Selection Sort',
            description: 'An in-place comparison sort that divides the array into a sorted prefix and an unsorted suffix. It repeatedly identifies the minimum (or maximum) element from the unsorted suffix and swaps it to the front.',
            howItWorks: 'Maintains a boundary index i from 0 to n-2. Scans the remaining unsorted subarray from i+1 to n-1 to locate the extreme value. Once found, performs exactly one swap to place it at index i.',
            best: 'O(n²)',
            average: 'O(n²)',
            worst: 'O(n²)',
            space: 'O(1)',
            stable: false,
            inPlace: true,
            whenToUse: 'When memory write operations are significantly more costly than read operations, as it makes at most O(n) swaps total.',
            observations: 'Always executes n(n-1)/2 comparisons regardless of initial array ordering. Unstable because distant swaps can leap over identical keys.',
            keyDifferences: 'Minimizes the total number of swaps to at most n-1, whereas Bubble and Insertion Sort may execute up to O(n²) swaps.'
        },
        insertionSort: {
            name: 'Insertion Sort',
            description: 'Builds the sorted array one item at a time by consuming elements from the unsorted region and inserting them into their correct position within the sorted prefix.',
            howItWorks: 'Starts with index 0 trivially sorted. For each subsequent element from 1 to n-1, stores the element in a temporary key and shifts greater elements in the sorted prefix one position to the right until the correct insertion slot is cleared.',
            best: 'O(n)',
            average: 'O(n²)',
            worst: 'O(n²)',
            space: 'O(1)',
            stable: true,
            inPlace: true,
            whenToUse: 'Small arrays (n ≤ 30) or arrays that are already nearly sorted. Frequently embedded as the base case in hybrid algorithms like Timsort and introsort.',
            observations: 'Adaptive: runs in O(n) time when input is already sorted. Highly cache-friendly with low constant overhead.',
            keyDifferences: 'Inserts into an already sorted contiguous prefix. Shell Sort extends this concept by allowing insertions over variable gaps.'
        },
        mergeSort: {
            name: 'Merge Sort',
            description: 'A classic divide-and-conquer algorithm that recursively splits the input array into halves, sorts each half independently, and cleanly merges the two sorted halves into a unified sorted array.',
            howItWorks: 'Divides the array at midpoint mid = floor((left+right)/2) until subarrays of size 1 are reached. Then uses two pointers to compare the leading elements of both sorted halves, copying the smaller element into an auxiliary buffer before writing back.',
            best: 'O(n log n)',
            average: 'O(n log n)',
            worst: 'O(n log n)',
            space: 'O(n)',
            stable: true,
            inPlace: false,
            whenToUse: 'When stable sorting with guaranteed O(n log n) worst-case performance is required, or when sorting linked lists or external disk files where sequential access is paramount.',
            observations: 'Guarantees O(n log n) even on worst-case inputs, but requires O(n) auxiliary memory allocation for array merging.',
            keyDifferences: 'Requires extra auxiliary memory for buffer merging, unlike Quick Sort, Heap Sort, or Shell Sort which operate in-place.'
        },
        quickSort: {
            name: 'Quick Sort',
            description: 'A highly optimized divide-and-conquer algorithm that partitions an array around a selected pivot element so that all elements smaller than the pivot precede it and all larger elements follow it.',
            howItWorks: 'Selects a pivot element (Lomuto partition uses the last element). Scans with index j and maintains pointer i for smaller elements, swapping elements into place. Places pivot at its permanent index i+1, then recursively partitions the left and right subarrays.',
            best: 'O(n log n)',
            average: 'O(n log n)',
            worst: 'O(n²)',
            space: 'O(log n) average',
            stable: false,
            inPlace: true,
            whenToUse: 'General-purpose in-memory sorting. Usually the fastest comparison-based sort in practical benchmarks due to cache locality and low constant factors.',
            observations: 'Degrades to O(n²) if an extreme pivot is repeatedly chosen on already sorted inputs, which is mitigated via median-of-three or randomized pivoting.',
            keyDifferences: 'Divides work based on element values relative to a pivot, whereas Merge Sort divides work strictly by array index.'
        },
        heapSort: {
            name: 'Heap Sort',
            description: 'An efficient comparison-based sorting algorithm that converts the array into a Binary Heap data structure, repeatedly extracts the maximum (or minimum) root element, and restores the heap property in logarithmic time.',
            howItWorks: 'Phase 1: Builds a Max-Heap in O(n) time by calling heapify from index floor(n/2)-1 down to 0. Phase 2: Iteratively swaps the root element (maximum value in heap) with the last element of the unsorted heap portion, shrinks the heap boundary by 1, and calls heapify on root (index 0) to restore the heap property in O(log n) time.',
            best: 'O(n log n)',
            average: 'O(n log n)',
            worst: 'O(n log n)',
            space: 'O(1)',
            stable: false,
            inPlace: true,
            whenToUse: 'Embedded systems and mission-critical applications where strict O(n log n) upper bound is required without allocating O(n) auxiliary memory (which Merge Sort requires) or risking O(n²) worst cases (which Quick Sort risks).',
            observations: 'Excellent theoretical guarantees (in-place O(1) auxiliary space and O(n log n) worst-case). Slower in practice than Quick Sort due to poor cache locality from non-contiguous child node lookups (2i+1, 2i+2).',
            keyDifferences: 'Utilizes an explicit complete binary tree structure mapped onto array indices. Guarantees O(n log n) in-place without recursion stack overhead.'
        },
        shellSort: {
            name: 'Shell Sort',
            description: 'An ingenious generalization of Insertion Sort that allows the comparison and exchange of elements that are far apart, progressively reducing the gap distance until it reaches 1 for a final insertion pass.',
            howItWorks: 'Initializes a gap sequence (Shell classic: floor(n/2) down to 1). For each gap, performs gap-interleaved insertion sort where elements at indices j and j-gap are compared and swapped if out of order. Elements take large leaps early on, eliminating major inversions quickly so the final gap = 1 pass runs in near-linear time.',
            best: 'O(n log n)',
            average: 'Gap-dependent (~O(n^(4/3)))',
            worst: 'Gap-dependent (O(n²) for Shell, O(n^(3/2)) for Knuth)',
            space: 'O(1)',
            stable: false,
            inPlace: true,
            whenToUse: 'Medium-sized arrays where simple code with zero recursion overhead is desired, such as embedded firmware or microcontrollers with limited call-stack depth.',
            observations: 'Complexity strongly depends on the chosen gap sequence. Shell original sequence (n/2^k) yields O(n²), while Knuth (3k+1)/2 yields O(n^(3/2)) and Tokuda or Sedgewick yield O(n^(4/3)).',
            keyDifferences: 'Compares distant elements across variable strides (gaps), unlike Insertion Sort which only shifts adjacent elements.'
        },
        countingSort: {
            name: 'Counting Sort',
            description: 'A non-comparison integer sorting algorithm that operates by counting the distinct frequencies of each value in the input array, computing prefix sums, and directly calculating each element\'s final output index in linear time.',
            howItWorks: 'Scans array to determine min and max values. Computes negative offset = -min. Allocates a count array of size k = max - min + 1. Counts occurrences of each value. Calculates cumulative prefix sums so each count[v] represents the last output index for value v. Scans input array from right to left, placing elements into output array to preserve stability.',
            best: 'O(n + k)',
            average: 'O(n + k)',
            worst: 'O(n + k)',
            space: 'O(n + k)',
            stable: true,
            inPlace: false,
            whenToUse: 'When sorting integers within a known, small range k where k = O(n), such as exam grades (0-100), age metrics, or as the stable subroutine inside Radix Sort.',
            observations: 'Breaks the O(n log n) comparison lower bound by leveraging direct array indexing. Inefficient and impractical if the range k is significantly larger than n (e.g. k = 1,000,000 for n = 10).',
            keyDifferences: 'Does not compare elements against each other. Determines position via direct numerical indexing into a frequency table.'
        },
        radixSort: {
            name: 'Radix Sort',
            description: 'A non-comparison sorting algorithm that avoids comparisons by creating and categorizing elements into buckets based on their individual radix (digits). LSD (Least Significant Digit) processes digits from ones to highest place.',
            howItWorks: 'Determines the maximum absolute value to know total digit passes d. Iterates through digit positions (exp = 1, 10, 100...). In each pass, distributes elements into 10 buckets (0 to 9) according to the digit at the active place value, then collects elements in order. Handles negative integers by separating signs, sorting each partition stably, and recombining.',
            best: 'O(d(n + k))',
            average: 'O(d(n + k))',
            worst: 'O(d(n + k))',
            space: 'O(n + k)',
            stable: true,
            inPlace: false,
            whenToUse: 'When sorting large collections of integers or fixed-length strings (such as phone numbers, dates, student IDs, or zip codes) where digit length d is small and bounded.',
            observations: 'Runs in linear time O(n) when d is constant. Highly stable. Requires auxiliary memory for the digit buckets.',
            keyDifferences: 'Sorts numbers digit-by-digit from right to left using multiple stable bucket passes, rather than comparing whole numbers at once.'
        },
        bucketSort: {
            name: 'Bucket Sort',
            description: 'A distribution-based algorithm that partitions elements into a finite number of uniformly spaced buckets, sorts each individual bucket using an auxiliary sorting algorithm, and concatenates all buckets in order.',
            howItWorks: 'Determines the minimum and maximum values across the array. Divides the range into k uniformly spaced buckets. Distributes each element into its corresponding bucket using an arithmetic normalization formula. Sorts each bucket independently using Insertion Sort. Gathers and concatenates elements from all buckets in order.',
            best: 'O(n + k) average under suitable distribution',
            average: 'Distribution-dependent (~O(n + k))',
            worst: 'O(n²)',
            space: 'O(n + k)',
            stable: true,
            inPlace: false,
            whenToUse: 'When input values are uniformly distributed over a known continuous interval, such as floating-point numbers in [0, 1) or normalized real-world sensor measurements.',
            observations: 'Performance relies heavily on the distribution of input data. If all elements cluster into a single bucket, complexity degrades to the underlying bucket sort (O(n²)).',
            keyDifferences: 'Scatters elements across value ranges into separate containers (buckets), then gathers them back, combining distribution and local sorting.'
        }
    };

    // ───────────────────────────────────────────────────────────
    // EXPORT
    // ───────────────────────────────────────────────────────────

    window.SortingAlgorithms = {
        bubbleSort: bubbleSort,
        selectionSort: selectionSort,
        insertionSort: insertionSort,
        mergeSort: mergeSort,
        quickSort: quickSort,
        heapSort: heapSort,
        shellSort: shellSort,
        countingSort: countingSort,
        radixSort: radixSort,
        bucketSort: bucketSort,
        pseudocode: pseudocode,
        complexityInfo: complexityInfo
    };

})();
