# Fibonacci Algorithm Performance Results

| Method                |   Time (seconds) |   Current Memory (KB) |   Peak Memory (KB) | Accuracy   |
|:----------------------|-----------------:|----------------------:|-------------------:|:-----------|
| Naive Recursion       |      4.89241     |              14.1836  |           14.5371  | True       |
| Memoized Recursion    |      0.000153065 |               5.86328 |            6.07227 | True       |
| Iterative             |      0.00106692  |               2.67578 |            2.99805 | True       |
| Matrix Exponentiation |      0.00918078  |              47.8477  |           48.8848  | True       |
| Binet's Formula       |      0.000419855 |               2.78516 |            3.02539 | True       |

## Summary

* Fastest method: Memoized Recursion (0.000153 seconds)
* Most memory-efficient method: Iterative (3.00 KB)

## About the Methods

* **Naive Recursion**: Slowest method as it recalculates the same values repeatedly. Has O(2^n) time complexity.
* **Memoized Recursion**: Top-down dynamic programming approach. Values are stored and reused. Has O(n) time and O(n) space complexity.
* **Iterative**: Bottom-up dynamic programming approach. Uses less memory. Has O(n) time and O(1) space complexity.
* **Matrix Exponentiation**: Calculates in logarithmic time using matrix exponentiation. Has O(log n) time complexity.
* **Binet's Formula**: Closed-form solution. Theoretically has O(1) time complexity, but may have precision issues for large numbers in practice.
