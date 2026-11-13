# Problem 2: Cryptanalysis of RSA

[NSUCRYPTO 2026](../README.md)

## Problem

**Topic:** RSA; scaled Fermat factorization.

Recover two messages from the supplied RSA public key and ciphertexts, and decode the second message using the supplied Python conversion.

Read the [complete original statement](statement.pdf), including its original notation, assumptions, illustrations, and subquestions. This PDF is copied without conversion from the supplied local statement; the owner confirmed permission to include the statements and illustrations. The [official site](http://nsucrypto.nsu.ru/) is the address printed in the statements; no problem-specific URL was supplied or checked online.

## My Approach

The report scans small multipliers in a scaled Fermat factorization and succeeds at k = 76. It derives the private exponent, identifies the first ciphertext as a fixed point, and decodes the second message, with modular re-encryption checks.

## My Solution

[Read the complete supplied solution](solution.pdf).

**Status:** Completed solution; exact checks. This is a description of the supplied work; no official grading or acceptance evidence was supplied.

The factorization exploits this particular modulus. The supplied program checks the recovered messages exactly; it is not a general RSA attack or a standalone primality certificate for the large factors.

The PDF retains the authorship credited in the original: Hamza El Ghabouchi, Oumaima Aboukhyyou, and Abdoulie Y Bojang. Original source location within the supplied solution collection: `Problem 2 - RSA/Solution_02_Cryptanalysis_of_RSA.pdf`. No mathematical argument has been edited.

No standalone LaTeX source was found for this report. Its PDF is retained in full rather than reconstructed as new LaTeX.

## Supporting Materials

* [rsa_solution.py](supporting-files/rsa_solution.py)
* [verification.txt](supporting-files/verification.txt)

See the [verification record](../VERIFICATION.md) for checks run during this organization pass.
