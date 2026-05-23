# v1.1.0 Release Notes

PrimeClock Dynamics v1.1.0 is a public research artifact titled:

```text
PrimeClock Dynamics v1.1.0: A Shrinking-Angle Gaussian Field
```

This release is not a DOI artifact, not a Zenodo record, not a posted preprint,
and not peer reviewed.

The artifact version is `v1.1.0`. Python package metadata is aligned to
`1.1.0` and is not used to expand the mathematical claim surface.

## Main Additions

- Complete-CRT collision kernel for moving angles.
- Kernel-conditioned finite-dimensional Gaussian theorem in the complete-CRT
  model.
- Explicit zero-ray shrinking-angle corollary with covariance parameter
  `theta` for `delta_x = exp(-(log x)^theta)`, `0 < theta < 1`.
- Deterministic collision-kernel support and focused tests.

## Boundary

The v1.1.0 public artifact does not claim integer-time transfer, finite-beta
Angular Kubilius Chaos, standard Gaussian Multiplicative Chaos,
uniform-in-alpha convergence, a full Gaussian field theorem, a general
distance-only kernel asymptotic, diagonal Mertens laws, high-point asymptotics,
or prime-time theorems.

## Verification

```bash
python3 experiments/_workflow/check_v1_1_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v1_1_public_artifact.json quick
python3 scripts/build_v1_1_public_artifact.py --out /tmp --verify-extraction
```
