# Problem 7: Sherlock Holmes

[NSUCRYPTO 2026](../README.md)

## Problem

**Topic:** Bitcoin transaction serialization; Morse decoding.

Recover the safe-deposit access code from the hexadecimal string and its hint about the Return.

Read the [complete original statement](statement.pdf), including its original notation, assumptions, illustrations, and subquestions. This PDF is copied without conversion from the supplied local statement; the owner confirmed permission to include the statements and illustrations. The [official site](http://nsucrypto.nsu.ru/) is the address printed in the statements; no problem-specific URL was supplied or checked online.

## My Approach

The report parses the supplied 1816 bytes as a transaction with 64 outputs. Two output types encode dots and dashes; OP_RETURN outputs delimit letters. The decoded message gives the access code CRYPTOWORLD.

## My Solution

[Read the complete supplied solution](solution.pdf).

**Status:** Completed decoding; exact checks. This is a description of the supplied work; no official grading or acceptance evidence was supplied.

The transaction is problem data, not a claim of a live payment. The code verifies field boundaries, the byte-for-byte round trip, the payload hash, and all Morse groups.

The PDF retains the authorship credited in the original: Hamza El Ghabouchi, Oumaima Aboukhyyou, and Abdoulie Y Bojang. Original source location within the supplied solution collection: `Problem 7/Solution_07_Sherlock_Holmes.pdf`. No mathematical argument has been edited.

No standalone LaTeX source was found for this report. Its PDF is retained in full rather than reconstructed as new LaTeX.

## Supporting Materials

* [sherlock_problem7_transaction.hex](supporting-files/sherlock_problem7_transaction.hex)
* [sherlock_problem7_verification.txt](supporting-files/sherlock_problem7_verification.txt)
* [sherlock_problem7_verify.py](supporting-files/sherlock_problem7_verify.py)

See the [verification record](../VERIFICATION.md) for checks run during this organization pass.
