# PrimeClock Dynamics v0.2.0

**Fixed-Cutoff Foundation Artifact**

PrimeClock Dynamics studies a prime-indexed circle model in which each prime
`p` contributes an arc on the circle `T = R/Z` centered at `(n mod p) / p` at
integer time `n`.

The central object is the **Prime Clock Multiplicity Field**:

```text
D(n, alpha) = sum_{p <= n} 1_{alpha in I_p(n)}.
```

At the twelve-o'clock direction `alpha = 0`, with the documented half-open
point-membership convention, this recovers the classical distinct prime-divisor
count:

```text
D(n, 0) = omega(n).
```

This artifact records the v0.2 fixed-cutoff foundation: finite CRT identities
for the fixed-cutoff field `D_x(n, alpha)` and the fixed-cutoff uncovered
measure `U_x(n)`. It is a reproducible mathematical research artifact, not a
peer-reviewed paper.

## Scope Of v0.2.0

This artifact covers only fixed-cutoff finite CRT statements:

- `PCD-FC-0`: twelve-o'clock fiber `D(n,0)=omega(n)`;
- `PCD-FC-1`: fixed-angle residue selector;
- `PCD-FC-2`: fixed-cutoff CRT mean/variance;
- `PCD-FC-3`: fixed-cutoff two-angle covariance;
- `PCD-MG-1`: Fixed-Cutoff CRT Average Identity;
- `PCD-MG-2`: Finite-Window Periodic Discrepancy Bound.

The main note is:

```text
paper/fixed_cutoff_foundation_v0_2_0.md
```

## Non-Claims

This artifact does **not** claim:

- an Erdos-Kac CLT;
- a Gaussian field theorem;
- a Mertens asymptotic law;
- a diagonal theorem for `D(n,alpha)=D_n(n,alpha)`;
- a diagonal theorem for `U(n)=U_n(n)`;
- a random-model or non-randomness theorem;
- a result about prime gaps, the Riemann hypothesis, or classical covering
  systems;
- visual app evidence as mathematical evidence;
- a preprint;
- a DOI artifact or Zenodo record;
- peer review.

The v0.3 diagonal bridge and v0.4 random-control diagnostics remain future
research directions and are not part of the v0.2.0 public claim surface.

## Verification

From a clean extraction:

```bash
python3 -m pip install -e ".[dev]"
python3 experiments/_workflow/check_v0_2_public_artifact.py
python3 experiments/_workflow/check_fixed_cutoff_theorem_packet.py
python3 scripts/check_text_hygiene.py
python3 -m pytest tests/test_twelve_oclock_equals_omega.py tests/test_cutoff_multiplicity_moments.py tests/test_uncovered_measure.py -q
python3 -m pytest -q
python3 -m ruff check src tests experiments scripts
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/v0_2_verification_workflow.json quick
```

If editable install fails on an older local Python packaging path, use:

```bash
python3 -m pip install --no-build-isolation -e ".[dev]"
```

## Repository Map

```text
docs/        mathematical specification and claim boundaries
paper/       public fixed-cutoff foundation note
src/         prime_clock_dynamics Python package
tests/       unit, theorem-support, and workflow tests
experiments/ reproducibility workflows and support builders
support_evidence/ deterministic support evidence in generated artifacts
```

## Relation To The Visual App And PRC

The original visual app is a display surface and is not the source of
mathematical claims in this artifact. See:

```text
docs/APP_MODEL_DIFFERENCE.md
```

PrimeClock Dynamics is also separate from the finite Prime Reciprocal Covering
artifact program. See:

```text
docs/RELATION_TO_PRC.md
```

## License

MIT License. See `LICENSE`.
