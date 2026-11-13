# NSUCRYPTO 2026

This collection documents work on the second round of the International Olympiad in Cryptography NSUCRYPTO 2026. The supplied statements identify the round as General, Teams, 12–19 October 2026.

The archive contains personal solutions and attempts, mathematical proofs, partial research results, and supporting computations for all twelve supplied problems. The original reports credit Hamza El Ghabouchi, Oumaima Aboukhyyou, and Abdoulie Y Bojang; that team attribution is preserved. These are personal competition documents, not official competition solutions. No official grading or acceptance evidence was supplied.

## Problems

| Problem | Topic | Status of supplied work | Materials |
|---|---|---|---|
| 1. An ancient civilization | Vigenere cryptanalysis; blockchain clues | Completed decryption; construction limits | [Problem and solution](problem-01/README.md) |
| 2. Cryptanalysis of RSA | RSA; scaled Fermat factorization | Completed solution; exact checks | [Problem and solution](problem-02/README.md) |
| 3. The BSW Conjecture | Finite fields; quadratic characters; clique enumeration | Finite-case alternative; general conjecture unresolved | [Problem and solution](problem-03/README.md) |
| 4. Secret coding | Exact linear algebra; bounded-error recovery | Completed solution and uniqueness certificate | [Problem and solution](problem-04/README.md) |
| 5. Grandchildren | Divisibility; integer constraints; ambiguity | Ambiguity analysis; unique key not established | [Problem and solution](problem-05/README.md) |
| 6. Alice in the Tweedleworld | Rotating grilles; transposition cryptanalysis | Completed decryption; exact checks | [Problem and solution](problem-06/README.md) |
| 7. Sherlock Holmes | Bitcoin transaction serialization; Morse decoding | Completed decoding; exact checks | [Problem and solution](problem-07/README.md) |
| 8. Crypto room | Visual clues; RSA decryption | Completed decryption; visual interpretation | [Problem and solution](problem-08/README.md) |
| 9. Vector LRS | Finite fields; splitting subspaces; recurrence matrices | Partial results; unrestricted implication unresolved | [Problem and solution](problem-09/README.md) |
| 10. Bent decompositions | Boolean functions; Walsh transforms; isotropic subspaces | Partial results; full conjecture unresolved | [Problem and solution](problem-10/README.md) |
| 11. Who is here? | Visual reconstruction; message interpretation | Completed interpretation; traversal not prescribed | [Problem and solution](problem-11/README.md) |
| 12. A quantum cipher | Pauli encryption; Bell measurements; key reuse | Completed vulnerability analysis; model restrictions | [Problem and solution](problem-12/README.md) |

“Completed” describes the scope addressed by the submitted document, not official correctness. Problem 3 addresses the permitted finite-case alternative; it does not prove the general BSW conjecture. Problem 5 records non-uniqueness under explicit conventions. Problems 9 and 10 contain partial results with unresolved general assertions.

## Mathematical techniques

The supplied work uses periodic substitution analysis and rotating grilles; exact modular arithmetic and scaled Fermat factorization; quadratic characters and compatibility-graph enumeration; rational Gaussian elimination and bounded-error certificates; finite-field linear algebra and splitting subspaces; Walsh–Hadamard transforms, slice lifting, and isotropic subspaces; and Pauli-channel and Bell-basis calculations. Each problem page summarizes only arguments present in its associated documents.

## Reading and preservation

Each problem page follows **Problem → My Approach → My Solution → Supporting Materials**. `statement.pdf` is the complete original local statement and `solution.pdf` is an unchanged supplied report. Only Problem 9 has a supplied standalone LaTeX source, retained as `solution.tex`. Earlier reports and separate computations are linked under supporting materials. No proof has been transcribed or rewritten, and no new mathematical solution has been generated.

The owner confirmed permission to include the original statements and illustrations. The official address printed in the statements is [nsucrypto.nsu.ru](http://nsucrypto.nsu.ru/); external pages and citations were not fetched or checked. Original mathematical notation, diagrams, and subquestions are preserved in the PDF copies.

## Attribution and limitations

The Problem 9 consolidated report discloses generative-AI assistance. The separate Problem 10 research supplement states that its further deductions were developed with AI research assistance and were not reviewed or endorsed by the named authors. It is labelled separately and is not treated as an endorsed competition solution. This organization pass preserves those disclosures and adds documentation only.

Read the [review notes](REVIEW-NOTES.md) for unresolved issues and version distinctions, the [verification record](VERIFICATION.md) for the scope of fresh checks, and the [source manifest](source-manifest.json) for the original-to-repository mapping and SHA-256 hashes. Historical verification claims remain attributed to the supplied files.

[All competitions](../README.md) · [Repository home](../../README.md)
