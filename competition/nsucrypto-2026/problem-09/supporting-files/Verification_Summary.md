# Verification summary — Problem 9: Vector LRS

19 October 2026

**The unrestricted problem remains unresolved by this submission.** The report is a consolidated partial-results submission, not a complete affirmative solution. No counterexample was found. No claim of mathematical novelty or priority is made.

## Mathematical audit

| Result | Audit determination | Essential restrictions and verification |
|---|---|---|
| Recurrence hypothesis ⇔ (US), Proposition 2.1 | Validated in both directions | Maximum period and coprime decimation are used explicitly. The state argument, decimated period, observation-map invertibility, and realization of an arbitrary (US) space are proved. No computational assumption. |
| Commuting coefficients ⇔ canonical space, Theorem 3.1 | Validated | Uses the maximum-period splitting basis. Transposes, the unital coefficient algebra, its embedding in the field centralizer, and the dimension argument are explicit. It does not assume (US) implies canonicity. |
| (n=m=2), Proposition 4.1 | Validated | Complete elementary order argument over the field of 16 elements; no computation is needed for the proof. |
| Theorem A, Theorem 5.1 | Validated using an external estimate | Requires (m=2), dimension (n), (US), and noncanonicity. Fu–Wan’s corrected v3, Theorems 4.5–4.6, applies with the required nondegeneracy. Orthogonality and the primitive-element indicator are justified. This is a necessary intersection bound. |
| Corollary A1, Corollary 5.2 | Validated | Requires intersection dimension at least (n-1) and n >= 19. The large-(n) bound and the exact arithmetic bridge for 19 <= n <= 38 check out. |
| Corollary A2, Corollary 5.3 | Validated as a computer-assisted theorem | Requires (m=2) and sharing a hyperplane with a scalar middle subfield. The finite normalization and determinant formula are proved. Every finite certificate for 2 <= n <= 18 was rerun. The conclusion holds in every dimension under this additional hypothesis. |
| Prime-(m) extension, Remark 5.4 | Validated | Primality of (m) ensures that an element outside the middle subfield has full relative degree. This extension is not asserted for arbitrary composite (m). |
| Theorem B, Theorem 5.5 | Validated with its additional hypotheses | Requires actual scalar-field linearity and both displayed inequalities. Counting intermediate fields supplies a full-degree element. The asymptotic statement fixes the relative dimension (r). |
| Theorem C, Theorem 5.6 | Validated with its additional hypotheses | Requires (U^{[2]}=cU) and the stated parameter families. The cyclic Frobenius module and divisor classification are justified. (US) has not been shown to force the fixed-space hypothesis. |
| Exhaustive computations | Validated by exact algorithms | Unique reduced bases and every pruning step have completeness arguments. Field cycles, primitive orders, Gaussian counts where applicable, and canonical survivors are checked. |
| Auxiliary index and collision restrictions, Appendix F | Validated | The cyclic-unit lifting argument and ordered-pair counting are proved. Neither gives an unrestricted classification. |

## Computations repeated during final preparation

- All **14 original cases**, comprising **4,729,574 normalized spaces**, were rerun. Counts, survivors, and cached rejecting exponents agree with the original report and its original verification log.
- The ordinary-set quadratic-extension search was rerun for **every n = 2,...,10**. Together with the original table, these establish **19 distinct parameter pairs**.
- The bit-set implementation was also rerun completely for **every n = 2,...,10**, including the largest case. Its survivors, candidate counts, and recursion counts agree with the historical bit-set evidence; its survivor spaces agree with the independent ordinary-set implementation.
- All **17 near-subfield certificates**, covering **1,048,534 normalized candidates**, were verified with exact arithmetic and deterministic coverage checks. Each witness’s primitivity and the complete factorization were checked; prime factors were certified by trial division.
- Complete independent small comparisons covered **7, 155, and 11,811 spaces** for (n=2,3,4). The rank predicate and ratio predicate agree on every space. Rank evaluation stops at its first failure.
- All **69,888 field products** in the field models of sizes 16, 64, and 256 agree with direct polynomial multiplication and reduction.
- The illustrative failed reductions and the Frobenius-kernel witness were checked exactly.
- **672 and 27,776 mixed character sums** were evaluated numerically at (q=4,8), respectively. These floating-point checks are diagnostics only and are not used as mathematical proofs.

The JSON retains historical evidence separately from the new `final_audit` records. Runtime measurements are not mathematical certificates.

## Clarifications and repairs

The final report expands the decimation-period argument and converse realization, makes the coefficient-matrix transpose convention explicit, cites the corrected Fu–Wan version, distinguishes necessary conditions from classifications, and explains why Frobenius symmetry cannot reduce the primitive tests for an arbitrary fixed space. The code is organized and refuses execution with `-O`, which would disable assertion checks. No unsupported general classification is retained.

## Reproduction and files

Use Python 3.10 or later, with the Python file and JSON in the same directory:

```text
python vector_lrs_m2_verify.py --validate --output small.json
python vector_lrs_m2_verify.py --near-subfield --output near.json
python vector_lrs_m2_verify.py --original --output original.json
python vector_lrs_m2_verify.py --output quadratic.json
python vector_lrs_m2_verify.py --engine bitsets --output bitsets.json
```

The arithmetic bridge is checked at startup. Compile the standalone LaTeX source with `pdflatex` twice. The final PDF was compiled locally with MiKTeX/pdfTeX, its references and destinations were checked, and all pages were visually inspected. The 13-page PDF has no unresolved references, duplicate destinations, overfull/underfull boxes, or LaTeX warnings. Author names and PDF metadata match the original report.

The package contains `Vector_LRS_Final.tex`, `Vector_LRS_Final.pdf`, `vector_lrs_m2_verify.py`, `vector_lrs_evidence.json`, this summary, and a SHA-256 manifest.

## Authorship, assistance, and remaining review

The original human author names are preserved exactly: **Hamza El Ghabouchi; Oumaima Aboukhyyou; Abdoulie Y Bojang**. The report discloses Python and generative-AI assistance and does not list AI systems as authors.

The official public [participation outline](https://nsucrypto.nsu.ru/outline/) was checked. It describes submission formats and the requirement for necessary detail, but does not explicitly resolve generative-AI eligibility. This audit does not certify compliance with any additional account-specific competition terms; the human authors should check those before uploading. No file has been submitted to the competition website.

The principal mathematical limitation is unchanged: **(US) ⇒ U = c F_{2^n} has not been proved for arbitrary (n,m)**. Theorems with additional hypotheses and finite computational proofs must not be represented as an unrestricted solution.
