# Problem 5: Grandchildren

[NSUCRYPTO 2026](../README.md)

## Problem

**Topic:** Divisibility; integer constraints; ambiguity.

Determine the ages of Asya, Vanya, and Sonya from the house-number and walking clues, and interpret the resulting digital key.

Read the [complete original statement](statement.pdf), including its original notation, assumptions, illustrations, and subquestions. This PDF is copied without conversion from the supplied local statement; the owner confirmed permission to include the statements and illustrations. The [official site](http://nsucrypto.nsu.ru/) is the address printed in the statements; no problem-specific URL was supplied or checked online.

## My Approach

The report gives an admissible assignment (2, 9, 6), then constructs other assignments under explicit house-numbering and endpoint-counting conventions. Its code checks six assignments using exact arithmetic.

## My Solution

[Read the complete supplied solution](solution.pdf).

**Status:** Ambiguity analysis; unique key not established. This is a description of the supplied work; no official grading or acceptance evidence was supplied.

The supplied work argues that the stated clues do not force a unique age triple. The candidate key 296 depends on an age-concatenation convention and is not established as the uniquely required key. The numbering convention and missing speed or distance information require attention.

The PDF retains the authorship credited in the original: Hamza El Ghabouchi, Oumaima Aboukhyyou, and Abdoulie Y Bojang. Original source location within the supplied solution collection: `Problem 5/Solution_05_Grandchildren.pdf`. No mathematical argument has been edited.

No standalone LaTeX source was found for this report. Its PDF is retained in full rather than reconstructed as new LaTeX.

## Supporting Materials

* [grandchildren_problem5_verification.txt](supporting-files/grandchildren_problem5_verification.txt)
* [grandchildren_problem5_verify.py](supporting-files/grandchildren_problem5_verify.py)

See the [verification record](../VERIFICATION.md) for checks run during this organization pass.
