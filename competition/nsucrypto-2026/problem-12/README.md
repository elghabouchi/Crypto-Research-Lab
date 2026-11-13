# Problem 12: A quantum cipher

[NSUCRYPTO 2026](../README.md)

## Problem

**Topic:** Pauli encryption; Bell measurements; key reuse.

Describe vulnerabilities of the cipher that applies the same keyed Pauli to both qubits of each allowed pair, including reuse of the key across encryptions.

Read the [complete original statement](statement.pdf), including its original notation, assumptions, illustrations, and subquestions. This PDF is copied without conversion from the supplied local statement; the owner confirmed permission to include the statements and illustrations. The [official site](http://nsucrypto.nsu.ru/) is the address printed in the statements; no problem-specific URL was supplied or checked online.

## My Approach

The report presents a legal chosen-plaintext probe for key recovery, identifies key-independent correlation leakage using Bell measurements, describes the averaged encryption channel, and analyzes malleability. It includes exact matrix checks and an ensemble-specific information calculation.

## My Solution

[Read the complete supplied solution](solution.pdf).

**Status:** Completed vulnerability analysis; model restrictions. This is a description of the supplied work; no official grading or acceptance evidence was supplied.

Chosen-plaintext key recovery assumes access to a chosen encryption; it is not a general ciphertext-only key-recovery claim. The half-bit information figure uses the specified uniform sixteen-label ensemble. Only entropy evaluation uses floating-point logarithms in the accompanying verifier.

The PDF retains the authorship credited in the original: Hamza El Ghabouchi, Oumaima Aboukhyyou, and Abdoulie Y Bojang. Original source location within the supplied solution collection: `Problem 12/Solution_12_A_Quantum_Cipher.pdf`. No mathematical argument has been edited.

No standalone LaTeX source was found for this report. Its PDF is retained in full rather than reconstructed as new LaTeX.

## Supporting Materials

* [quantum_cipher_problem12_verification.txt](supporting-files/quantum_cipher_problem12_verification.txt)
* [quantum_cipher_problem12_verify.py](supporting-files/quantum_cipher_problem12_verify.py)

See the [verification record](../VERIFICATION.md) for checks run during this organization pass.
