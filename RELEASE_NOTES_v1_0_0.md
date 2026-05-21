# PrimeClock Dynamics v1.0.0 Release Notes

PrimeClock Dynamics v1.0.0 is a public research artifact and preprint-style
manuscript. It is not peer reviewed. It is not a DOI artifact or Zenodo record
unless a DOI/Zenodo deposit is issued separately.

## Title

PrimeClock Dynamics: An Angular Erdos-Kac Theorem and a Fixed-Cutoff
Geometric Mertens Identity

## Included Claim Surface

- finite-dimensional fixed-angle Angular Erdos-Kac theorem on dyadic windows;
- fixed-angle diagonal Angular Erdos-Kac theorem as the one-dimensional case;
- fixed-cutoff complete-CRT Angular CLT input;
- slow finite-window moment transfer;
- all-angle L1 diagonal tail removal;
- fixed-cutoff CRT uncovered-average identity;
- fixed-cutoff uncovered-average asymptotic obtained from the classical Mertens
  product theorem.

## Explicit Non-Claims

This artifact does not claim uniform-in-alpha convergence, a shrinking-angle
theorem, a log-correlated Gaussian field theorem, a full Gaussian field theorem,
a diagonal Mertens uncovered-measure law, pointwise or typical laws for `U(n)`,
a random/non-random theorem, a result about prime gaps, a result about the
Riemann hypothesis, a result about classical covering systems, a new proof of
Mertens' theorem, or peer review.

The `alpha=0` fiber recovers `omega(n)`. The Angular Erdos-Kac theorem therefore
contains the corresponding dyadic `omega(n)` statement as a special case. This
is consistent with the classical Erdos-Kac theorem and is not presented as a new
strengthening of the classical theorem.

Boundary scan summary: not uniform-in-alpha convergence; not a new proof of Mertens' theorem.

## Main Manuscript

```text
paper/primeclock_dynamics_v1_0_preprint.md
```

## Verification

```bash
python3 -m pip install -e ".[dev]"
python3 experiments/_workflow/check_v1_0_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v1_0_public_artifact.json quick
python3 scripts/check_text_hygiene.py
python3 -m pytest -q
python3 -m ruff check src tests experiments scripts
```

To rebuild:

```bash
python3 scripts/build_v1_0_public_artifact.py --out /tmp --verify-extraction
```
