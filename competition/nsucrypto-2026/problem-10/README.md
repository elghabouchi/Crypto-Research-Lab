# Problem 10: Bent decompositions

[NSUCRYPTO 2026](../README.md)

## Problem

**Topic:** Boolean functions; Walsh transforms; isotropic subspaces.

Study decomposition into two bent functions, including the quartic, cubic, essential-support, and bounded-number-of-summands alternatives listed in the statement.

Read the [complete original statement](statement.pdf), including its original notation, assumptions, illustrations, and subquestions. This PDF is copied without conversion from the supplied local statement; the owner confirmed permission to include the statements and illustrations. The [official site](http://nsucrypto.nsu.ru/) is the address printed in the statements; no problem-specific URL was supplied or checked online.

## My Approach

The revised report uses slice lifting, a Hall-theorem condition for functions affine on subspace cosets, highest derivatives, and isotropic subspaces. It supplies sufficient conditions for restricted cubic and quartic families and an explicit eight-variable quartic decomposition.

## My Solution

[Read the complete supplied solution](solution.pdf).

**Status:** Partial results; full conjecture unresolved. This is a description of the supplied work; no official grading or acceptance evidence was supplied.

The full Tokareva conjecture is not settled. The revised report explicitly restricts the quadratic corollary to m >= 2 and explains the two-variable exception. Some base results are imported from the literature; larger computational checks are sampled. Novelty and publication priority are unestablished.

The PDF retains the authorship credited in the original: Hamza El Ghabouchi, Oumaima Aboukhyyou, and Abdoulie Y Bojang. Original source location within the supplied solution collection: `Problem 1/Solution_10_Bent_Decompositions_Revised_261019_063038.pdf`. No mathematical argument has been edited.

No standalone LaTeX source was found for this report. Its PDF is retained in full rather than reconstructed as new LaTeX.

## Supporting Materials

* [bent_decompositions.pdf](supporting-files/bent_decompositions.pdf) â€” AI-assisted research supplement; its text states that the named authors have not reviewed or endorsed it. Its further deductions are not attributed here to the competition authors.
* [bent_decompositions_problem10_certificates.json](supporting-files/bent_decompositions_problem10_certificates.json)
* [bent_decompositions_problem10_verification.txt](supporting-files/bent_decompositions_problem10_verification.txt)
* [bent_decompositions_problem10_verify.py](supporting-files/bent_decompositions_problem10_verify.py)
* [Solution_10_Bent_Decompositions_Partial_Results.pdf](supporting-files/Solution_10_Bent_Decompositions_Partial_Results.pdf) â€” earlier partial-results report, preserved for its distinct work.

The supplement comments on an uncorrected quadratic claim in an earlier report. The supplied revised report already includes the m >= 2 restriction and two-variable exception. The earlier target of that criticism cannot be identified with certainty from the supplied versions. The supplement is retained for provenance and requires author review before any of its further deductions are adopted. Its referenced `verify.py` and `results.json` were not found among the supplied files; the other verifier must not be treated as their replacement.

See the [verification record](../VERIFICATION.md) for checks run during this organization pass.
