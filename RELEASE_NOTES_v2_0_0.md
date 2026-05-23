# PrimeClock Dynamics v2.0.0 Release Notes

PrimeClock Dynamics v2.0.0 records Angular Kubilius Chaos via Holomorphic
Generating Functionals as a public research artifact. This artifact is not a
posted preprint and not peer reviewed. A versioned Zenodo record archives the
verified public artifact:

- Zenodo record: <https://zenodo.org/records/20357499>
- Version DOI: <https://doi.org/10.5281/zenodo.20357499>
- Concept DOI: <https://doi.org/10.5281/zenodo.20336785>

## Title

PrimeClock Dynamics v2.0.0: Angular Kubilius Chaos via Holomorphic Generating
Functionals

## Included Claim Surface

- complete-CRT finite-beta AKC random measure;
- martingale random measures;
- q-point local factor / moment formula;
- finite-beta L2 total-mass bound;
- weak convergence of random finite measures;
- Gaussian tangent recovery.

## Explicit Non-Claims

This public artifact does not claim integer-time finite-beta transfer, diagonal
Mertens uncovered-measure theorem, beta-to-negative-infinity uncovered theorem,
high-point or extremal theorem, Fisher-zero theorem, Lee-Yang theorem,
prime-time theorem, standard Gaussian Multiplicative Chaos, posted preprint, or
peer review.

## Verification

```bash
python3 experiments/_workflow/check_v2_0_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v2_0_public_artifact.json quick
python3 scripts/build_v2_0_public_artifact.py --out /tmp --verify-extraction
```
