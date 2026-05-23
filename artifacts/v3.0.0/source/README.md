# PrimeClock Dynamics v3.0.0

**The Mertens Boundary of Angular Kubilius Chaos**

This public research artifact records PrimeClock Dynamics v3.0.0: The Mertens Boundary of Angular Kubilius Chaos. It is not a posted preprint and is not peer reviewed.

The main manuscript draft is:

```text
paper/primeclock_dynamics_v3_0_public_manuscript.md
```

## Included Claim Surface

- complete-CRT Mertens-normalized uncovered random measure;
- martingale random measures for bounded Borel test functions;
- q-point hard local factor formula;
- finite L2 total-mass bound for the normalized uncovered measure;
- weak convergence of complete-CRT Mertens-boundary random finite measures;
- fixed-cutoff compatibility with the `beta -> -infinity` finite-beta AKC endpoint.

## Non-Claims

This public artifact does not claim:

- integer-time transfer;
- diagonal Mertens uncovered-measure theorem;
- `U_n(n) log n -> e^{-gamma}`;
- `beta -> +infinity` high-point theorem;
- Fisher-zero theorem;
- Lee-Yang theorem;
- standard Gaussian Multiplicative Chaos;
- prime-time theorem;
- a new proof of the classical Mertens product theorem;
- posted preprint or peer review.

v3.5 soft integer-time transfer, v4.0 integer-time diagonal Mertens, and v5.0
high-point/extremal directions remain future targets and are not part of this
v3.0 claim surface.

## Reading Order

1. `paper/primeclock_dynamics_v3_0_public_manuscript.md`
2. `docs/MB_V3_0_PUBLIC_CLAIM_BOUNDARY.md`
3. `experiments/_workflow/README_V3_0_PUBLIC_ARTIFACT.md`
4. `support_evidence/mb_v3_0_public_support/summary.json`

## Verification

```bash
python3 experiments/_workflow/check_v3_0_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_0_public_artifact.json quick
python3 scripts/check_text_hygiene.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/test_mertens_boundary.py tests/test_mb_v3_0_public_surface.py tests/test_text_hygiene.py -q
```

To rebuild the public artifact ZIP:

```bash
python3 scripts/build_v3_0_public_artifact.py --out /tmp --verify-extraction
```

MIT License. See `LICENSE`.
