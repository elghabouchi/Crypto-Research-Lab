# Problem 4: Secret coding

[NSUCRYPTO 2026](../README.md)

## Problem

**Topic:** Exact linear algebra; bounded-error recovery.

Recover the six-coordinate secret and twelve errors from the given linear equations, with errors in {-1, 0, 1} and secret coordinates of absolute value at most 10.

Read the [complete original statement](statement.pdf), including its original notation, assumptions, illustrations, and subquestions. This PDF is copied without conversion from the supplied local statement; the owner confirmed permission to include the statements and illustrations. The [official site](http://nsucrypto.nsu.ru/) is the address printed in the statements; no problem-specific URL was supplied or checked online.

## My Approach

The report eliminates the secret from seven equations using an exact integer row relation. It enumerates 729 error prefixes, recovers the unique secret (7, -4, 3, -6, 2, 5), and gives a compact certificate using two sets of 27 integers.

## My Solution

[Read the complete supplied solution](solution.pdf).

**Status:** Completed solution and uniqueness certificate. This is a description of the supplied work; no official grading or acceptance evidence was supplied.

The exact computation verifies all twelve equations and the uniqueness certificate. No separate LaTeX source was supplied.

The PDF retains the authorship credited in the original: Hamza El Ghabouchi, Oumaima Aboukhyyou, and Abdoulie Y Bojang. Original source location within the supplied solution collection: `Problem 4/Solution_04_Secret_Coding.pdf`. No mathematical argument has been edited.

No standalone LaTeX source was found for this report. Its PDF is retained in full rather than reconstructed as new LaTeX.

## Supporting Materials

* [secret_coding_problem4_verification.txt](supporting-files/secret_coding_problem4_verification.txt)
* [secret_coding_problem4_verify.py](supporting-files/secret_coding_problem4_verify.py)

See the [verification record](../VERIFICATION.md) for checks run during this organization pass.
