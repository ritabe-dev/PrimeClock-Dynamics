# PrimeClock Dynamics v3.0.0 Public Artifact Release Notes

PrimeClock Dynamics v3.0.0 records the Mertens Boundary of Angular Kubilius
Chaos as a public research artifact. This artifact is not a posted preprint
and is not peer reviewed.

## Title

PrimeClock Dynamics v3.0.0: The Mertens Boundary of Angular Kubilius Chaos

Subtitle: Mertens-Normalized Uncovered Measures in the Complete-CRT Model

## Included Claim Surface

- complete-CRT Mertens-normalized uncovered random measure;
- martingale random measures;
- q-point hard local factor formula;
- finite L2 total-mass bound;
- weak convergence of complete-CRT Mertens-boundary random finite measures;
- fixed-cutoff `beta -> -infinity` endpoint compatibility with v2.0 finite-beta AKC.

## Explicit Non-Claims

This public artifact does not claim integer-time transfer, diagonal Mertens
uncovered-measure theorem, `U_n(n) log n -> e^{-gamma}`, `beta -> +infinity`
high-point theorem, Fisher-zero theorem, Lee-Yang theorem, prime-time theorem,
standard Gaussian Multiplicative Chaos, a new proof of the classical Mertens
product theorem, posted preprint, or peer review.

## Verification

```bash
python3 experiments/_workflow/check_v3_0_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_0_public_artifact.json quick
python3 scripts/build_v3_0_public_artifact.py --out /tmp --verify-extraction
```
