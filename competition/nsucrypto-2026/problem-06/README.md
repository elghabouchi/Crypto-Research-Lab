# Problem 6: Alice in the Tweedleworld

[NSUCRYPTO 2026](../README.md)

## Problem

**Topic:** Rotating grilles; transposition cryptanalysis.

Read the reply ciphertext and explain the encryption method using the supplied known plaintext and ciphertext.

Read the [complete original statement](statement.pdf), including its original notation, assumptions, illustrations, and subquestions. This PDF is copied without conversion from the supplied local statement; the owner confirmed permission to include the statements and illustrations. The [official site](http://nsucrypto.nsu.ru/) is the address printed in the statements; no problem-specific URL was supplied or checked online.

## My Approach

The report models each 36-character block with a 6 by 6 rotating grille containing nine holes. It recovers the first grille from the known pair, uses its transposed mask for the reply, and preserves every encoded space and punctuation mark.

## My Solution

[Read the complete supplied solution](solution.pdf).

**Status:** Completed decryption; exact checks. This is a description of the supplied work; no official grading or acceptance evidence was supplied.

The recovered reply retains the unusual spacing in the ciphertext. The supplied code includes exhaustive grille recovery and encryption/decryption round trips; the explanation should be read with those exact strings.

The PDF retains the authorship credited in the original: Hamza El Ghabouchi, Oumaima Aboukhyyou, and Abdoulie Y Bojang. Original source location within the supplied solution collection: `Problem 6/Solution_06_Alice_in_the_Tweedleworld.pdf`. No mathematical argument has been edited.

No standalone LaTeX source was found for this report. Its PDF is retained in full rather than reconstructed as new LaTeX.

## Supporting Materials

* [tweedleworld_problem6_verification.txt](supporting-files/tweedleworld_problem6_verification.txt)
* [tweedleworld_problem6_verify.py](supporting-files/tweedleworld_problem6_verify.py)

See the [verification record](../VERIFICATION.md) for checks run during this organization pass.
