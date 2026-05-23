# PrimeClock Dynamics v1.1.0

**A Shrinking-Angle Gaussian Field**

This is the PrimeClock Dynamics v1.1.0 public research artifact for the
complete-CRT Shrinking-Angle Gaussian Field theorem surface. It is not a DOI
artifact, not a Zenodo record, not a posted preprint, and not peer reviewed.

The artifact version is `v1.1.0`. The Python package metadata is aligned to
`1.1.0`; this does not extend the v1.1 claim surface.

The main manuscript is:

```text
paper/primeclock_dynamics_v1_1_manuscript.md
```

## Claim Surface

- complete-CRT collision kernel for moving angles;
- complete-CRT kernel-conditioned finite-dimensional Gaussian convergence;
- explicit zero-ray shrinking-angle Gaussian corollary;
- deterministic collision-kernel support checks.

## Non-Claims

This public artifact does not claim:

- integer-time shrinking-angle transfer;
- diagonal shrinking-angle Angular Erdos-Kac;
- finite-beta Angular Kubilius Chaos;
- standard Gaussian Multiplicative Chaos;
- uniform-in-alpha convergence;
- a full Gaussian field theorem over all angles;
- a distance-only collision-kernel theorem for arbitrary moving angles;
- a diagonal Mertens uncovered-measure law;
- high-point or extremal asymptotics;
- prime-time trace theorems;
- DOI, Zenodo publication, posted preprint, or peer review.

Angular Kubilius Chaos is mentioned only as later outlook.

Some helper modules from earlier Dynamics work are included as package context.
Their presence does not extend the v1.1 claim surface beyond the
Shrinking-Angle Gaussian Field result described here.

## Verification

```bash
python3 -m pip install -e ".[dev]"
python3 experiments/_workflow/check_v1_1_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v1_1_public_artifact.json quick
python3 scripts/check_text_hygiene.py
python3 -m pytest tests/test_collision_kernel.py -q
```

To rebuild the public artifact ZIP:

```bash
python3 scripts/build_v1_1_public_artifact.py --out /tmp --verify-extraction
```

## Repository Map

```text
docs/        v1.1 definitions, related work, and claim boundaries
paper/       v1.1 manuscript
src/         prime_clock_dynamics Python package
tests/       focused kernel and workflow tests
experiments/ reproducibility workflows and support builders
```

MIT License. See `LICENSE`.
