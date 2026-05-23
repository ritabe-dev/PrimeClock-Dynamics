# PrimeClock Dynamics v2.0.0

**Angular Kubilius Chaos via Holomorphic Generating Functionals**

This public research artifact records the PrimeClock Dynamics v2.0.0 complete-CRT
finite-beta Angular Kubilius Chaos theorem surface. It is not a posted preprint
and not peer reviewed. The versioned archive is recorded on Zenodo:

- Zenodo record: <https://zenodo.org/records/20357499>
- Version DOI: <https://doi.org/10.5281/zenodo.20357499>
- Concept DOI: <https://doi.org/10.5281/zenodo.20336785>

The main manuscript draft is:

```text
paper/primeclock_dynamics_v2_0_public_manuscript.md
```

The research artifact version is `v2.0.0`. Python package metadata is aligned
to `2.0.0`; this does not extend the v2.0 claim surface.

## Included Claim Surface

- complete-CRT finite-beta AKC random measure;
- martingale random measures for bounded Borel test functions;
- q-point local factor / moment formula;
- finite-beta L2 total-mass bound;
- weak convergence of complete-CRT random finite measures;
- Gaussian tangent recovery linking v1.1 and v1.2 to v2.0.

## Non-Claims

This public artifact does not claim:

- integer-time finite-beta transfer;
- diagonal Mertens uncovered-measure theorem;
- beta-to-negative-infinity uncovered theorem;
- high-point or extremal theorem;
- Fisher-zero theorem;
- Lee-Yang theorem;
- prime-time theorem;
- standard Gaussian Multiplicative Chaos;
- a result about prime gaps or the Riemann hypothesis;
- posted preprint or peer review.

v3.0 is reserved for the complete-CRT Mertens boundary of AKC:
Mertens-normalized uncovered measures at the `beta -> -infinity` hard endpoint.
v3.5 soft integer-time transfer, v4.0 integer-time diagonal Mertens, and v5.0
high-point/extremal directions remain future targets and are not part of this
v2.0 claim surface.

## Reading Order

1. `paper/primeclock_dynamics_v2_0_public_manuscript.md`
2. `docs/AKC_V2_0_PUBLIC_CLAIM_BOUNDARY.md`
3. `experiments/_workflow/README_V2_0_PUBLIC_ARTIFACT.md`
4. `support_evidence/akc_v2_0_public_support/summary.json`

## Verification

```bash
python3 -m pip install -e ".[dev]"
python3 experiments/_workflow/check_v2_0_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v2_0_public_artifact.json quick
python3 scripts/check_text_hygiene.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/test_akc.py tests/test_akc_v2_0_public_surface.py tests/test_text_hygiene.py -q
```

To rebuild the public artifact ZIP:

```bash
python3 scripts/build_v2_0_public_artifact.py --out /tmp --verify-extraction
```

MIT License. See `LICENSE`.
