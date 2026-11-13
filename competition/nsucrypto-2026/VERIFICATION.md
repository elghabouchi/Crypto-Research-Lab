# Verification record

Organization pass: 13 November 2026. All checks used supplied local files; no external pages or services were accessed.

## Preservation and matching

The twelve original statements were inspected, including rendered pages for scanned mathematics and illustrations. Official numbers, titles, and mathematical contents agree with the associated reports. Each statement and supplied solution/supporting artifact is copied without content changes. The [source manifest](source-manifest.json) records 58 copies with their source-relative locations and SHA-256 hashes. Original source files remain in place. No automated PDF-to-LaTeX conversion was used.

The Problem 10 revision originally stored under Problem 1 is filed by its explicit heading and content. Earlier Problem 9 and Problem 10 reports are retained separately. All five entries in the supplied Problem 9 historical hash manifest match, allowing for its PDF filename discrepancy described in [review notes](REVIEW-NOTES.md).

## Fresh computational checks

The following thirteen invocations of supplied programs all returned exit code 0. They reproduce computations; they do not independently certify every proof or an unrestricted conjecture. Python 3.14 was used without optimization. Run from each problem's `supporting-files` directory unless noted; these programs use the standard library.

| Problem | Invocation | Fresh scope |
|---|---|---|
| 2 | `python rsa_solution.py` | Scaled factorization, exact plaintext recovery, and modular round trips. |
| 3 | `python bsw_problem3_verify.py` | All ten listed primes from 43 to 127; exact counts and direct involution checks. |
| 3 | `python bsw_problem3_verify.py controls` | Five smaller-prime negative controls. |
| 3 | `python bsw_problem3_independent.py` | Separate fixed-order search at 43 and 47. |
| 4 | `python secret_coding_problem4_verify.py` | Exact equations, bounded errors, and uniqueness certificate. |
| 5 | `python grandchildren_problem5_verify.py` | Six assignments under the stated conventions; non-uniqueness evidence. |
| 6 | `python tweedleworld_problem6_verify.py` | Exact space-sensitive encryption and decryption. |
| 6 | `python tweedleworld_problem6_verify.py --recover` | All 262144 grille masks; unique match in this model. |
| 7 | `python sherlock_problem7_verify.py` | Full transaction parsing, hash, byte round trip, and Morse groups. |
| 8 | `python crypto_room_problem8_verify.py` | Seventeen RSA blocks, exact round trips, and trial-division primality checks. |
| 9 | `python vector_lrs_m2_verify.py --validate --output small.json` | Complete small comparisons at n = 2, 3, 4; 69888 field-product checks; arithmetic bridge and failed-reduction examples. |
| 10 | `python bent_decompositions_problem10_verify.py` | All 2048 four-variable degree-at-most-two targets; explicit eight-variable example; 256 sampled cubic lifts and 8 sampled quartic forms. |
| 12 | `python quantum_cipher_problem12_verify.py` | Exact matrix/channel identities, all sixteen allowed input pairs, key probe and malleability checks. Entropy alone uses floating-point logarithms. |

The Problem 9 validation also evaluates 672 and 27776 character sums numerically. These are consistency diagnostics, not proofs of character-sum theorems. Its larger original searches, n = 2,...,10 full searches, and near-subfield certificate sweep were not rerun in this pass. Historical evidence and its original audit summary remain supplied-source claims.

No standalone program was supplied for Problems 1 or 11, and their embedded reasoning was not converted into new code. The Problem 10 supplement's separately named verification package was not supplied.

## LaTeX and document integrity

The only supplied standalone LaTeX source, Problem 9, was processed twice with locally installed MiKTeX/pdfLaTeX and automatic package installation disabled. The second-pass document log has no undefined references, LaTeX warnings, or overfull/underfull boxes. A 13-page PDF was produced and its extracted text agrees page by page with the supplied PDF. The supplied PDF remains the repository copy.

MiKTeX returned a nonzero process status because access to its separate application-log directory was denied. Thus the document was successfully typeset, but the tool invocation did not finish with a clean process exit. Build products and machine-specific logs were kept outside the repository. No other LaTeX source was supplied for compilation.

All relative Markdown file and directory targets were checked locally. External URLs were not fetched. Hash comparison verifies that original proofs, equations, spacing, tables, and illustrations were not lost through copying. PDF metadata and attachments and readable source text were inspected for accidental private information; the retained author metadata and attribution qualifications are recorded in the review notes. Existing repository files are preserved except for the requested root README integration.
