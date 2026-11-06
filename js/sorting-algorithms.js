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
    function makeStep(arr, comparing, swapping, sorted, pivot, explanation, pseudocodeLine, counters) {
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
            }
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
        ]
    };

    // ───────────────────────────────────────────────────────────
    // COMPLEXITY INFO
    // ───────────────────────────────────────────────────────────

    const complexityInfo = {
        bubbleSort: {
            name: 'Bubble Sort',
            description: 'A simple comparison-based algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. Named because smaller (or larger) elements "bubble" to the top of the list.',
            best: 'O(n)',
            average: 'O(n²)',
            worst: 'O(n²)',
            space: 'O(1)',
            stable: true,
            inPlace: true,
            whenToUse: 'Best for small datasets or nearly sorted arrays. Useful for educational purposes to understand basic sorting concepts. Not recommended for large datasets due to quadratic time complexity.'
        },
        selectionSort: {
            name: 'Selection Sort',
            description: 'An in-place comparison sorting algorithm that divides the input into a sorted region (built from left to right) and an unsorted region. It repeatedly selects the smallest (or largest) element from the unsorted region and moves it to the end of the sorted region.',
            best: 'O(n²)',
            average: 'O(n²)',
            worst: 'O(n²)',
            space: 'O(1)',
            stable: false,
            inPlace: true,
            whenToUse: 'Useful when memory writes are expensive, since it performs at most O(n) swaps. Good for small arrays. Not recommended for large datasets due to quadratic time complexity in all cases.'
        },
        insertionSort: {
            name: 'Insertion Sort',
            description: 'Builds the final sorted array one element at a time by picking each element and inserting it into its correct position among the previously sorted elements. Similar to how most people sort a hand of playing cards.',
            best: 'O(n)',
            average: 'O(n²)',
            worst: 'O(n²)',
            space: 'O(1)',
            stable: true,
            inPlace: true,
            whenToUse: 'Excellent for small arrays or nearly sorted data. Often used as the base case in hybrid sorting algorithms (e.g., Timsort). Performs well when the array is almost sorted.'
        },
        mergeSort: {
            name: 'Merge Sort',
            description: 'A divide-and-conquer algorithm that divides the array into halves, recursively sorts each half, and then merges the sorted halves back together. It guarantees O(n log n) performance in all cases but requires additional memory.',
            best: 'O(n log n)',
            average: 'O(n log n)',
            worst: 'O(n log n)',
            space: 'O(n)',
            stable: true,
            inPlace: false,
            whenToUse: 'Ideal when stable sorting is required and consistent O(n log n) performance is needed. Great for linked lists. Used when worst-case performance matters more than memory usage.'
        },
        quickSort: {
            name: 'Quick Sort',
            description: 'A highly efficient divide-and-conquer algorithm that selects a "pivot" element, partitions the array around it (elements smaller than pivot on the left, larger on the right), and recursively sorts the partitions. Average case is very fast in practice.',
            best: 'O(n log n)',
            average: 'O(n log n)',
            worst: 'O(n²)',
            space: 'O(log n)',
            stable: false,
            inPlace: true,
            whenToUse: 'The go-to general-purpose sorting algorithm for most applications. Excellent cache performance and low overhead. Worst case can be avoided with randomized pivot selection. Used in most standard library implementations.'
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
        pseudocode: pseudocode,
        complexityInfo: complexityInfo
    };

})();
