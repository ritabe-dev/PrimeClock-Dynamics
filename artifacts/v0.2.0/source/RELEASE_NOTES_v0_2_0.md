# PrimeClock Dynamics v0.2.0 Fixed-Cutoff Foundation Artifact

## Summary

`v0.2.0` is a small public research artifact for the fixed-cutoff foundation of
PrimeClock Dynamics. It records finite CRT identities for an angular
prime-counting model and its fixed-cutoff uncovered-measure baseline.

This artifact is intentionally narrow. It is not a preprint, not a
peer-reviewed mathematical result, and not a diagonal PrimeClock theorem.

## Included Claim Surface

- `PCD-FC-0`: twelve-o'clock fiber `D(n,0)=omega(n)`;
- `PCD-FC-1`: fixed-angle residue selector;
- `PCD-FC-2`: fixed-cutoff CRT mean/variance;
- `PCD-FC-3`: fixed-cutoff two-angle covariance;
- `PCD-MG-1`: Fixed-Cutoff CRT Average Identity;
- `PCD-MG-2`: Finite-Window Periodic Discrepancy Bound.

## Main Note

```text
paper/fixed_cutoff_foundation_v0_2_0.md
```

## Verification

Recommended verification commands:

```bash
python3 -m pip install -e ".[dev]"
python3 experiments/_workflow/check_v0_2_public_artifact.py
python3 experiments/_workflow/check_fixed_cutoff_theorem_packet.py
python3 scripts/check_text_hygiene.py
python3 -m pytest -q
python3 -m ruff check src tests experiments scripts
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/v0_2_verification_workflow.json quick
```

## Non-Claims

This artifact does not claim:

- an Erdos-Kac CLT;
- a Gaussian field theorem;
- a Mertens asymptotic law;
- a diagonal theorem for `D(n,alpha)=D_n(n,alpha)`;
- a diagonal theorem for `U(n)=U_n(n)`;
- a random-model theorem;
- visual app evidence as mathematical evidence;
- a DOI artifact or Zenodo record;
- a result about prime gaps, the Riemann hypothesis, or classical covering
  systems;
- peer review.

## Future Context

The v0.3 diagonal bridge and v0.4 random-control diagnostics remain future
work. They are not part of the v0.2.0 public claim surface.
