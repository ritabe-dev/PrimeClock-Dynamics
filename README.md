# PrimeClock Dynamics v3.5.0

**Slow-Cutoff Integer-Time Transfer**

This public research artifact records a slow-cutoff integer-time transfer
theorem for Mertens-normalized PrimeClock uncovered masses. It is not a posted
preprint and is not peer reviewed.

Rio Itabe is the sole human author and accepts responsibility for the public
claims. AI assistance and its limits are described in
[AI_DISCLOSURE.md](AI_DISCLOSURE.md). This maintenance update does not alter
any existing tag or release asset.

The main manuscript is:

```text
paper/primeclock_dynamics_v3_5_public_manuscript.md
```

## Included Claim Surface

- `PCD-IT-TV`: total-variation transfer from dyadic integer windows to uniform
  residues modulo `Q`;
- `PCD-IT-DIST`: bounded-test distributional transfer for `F_y=U_y/P_y` under
  `M_y/N -> 0`;
- `PCD-IT-MOM-m`: fixed `m` moment transfer under
  `M_y P_y^{-m}/N -> 0`, with sufficient Mertens-scale condition
  `M_y (log y)^m/N -> 0`.

## Non-Claims

This public artifact does not claim:

- full diagonal Mertens transfer;
- a theorem for `U_n(n)`;
- distributional diagonal transfer;
- a conductor-tail theorem;
- a theorem beyond the slow-cutoff periodic regime;
- a result about prime gaps or the Riemann hypothesis;
- posted preprint or peer review.

The conductor projection table is diagnostic only and does not establish
high-conductor tail decay or diagonal transfer.

## Reading Order

1. `paper/primeclock_dynamics_v3_5_public_manuscript.md`
2. `docs/IT_V3_5_PUBLIC_CLAIM_BOUNDARY.md`
3. `experiments/_workflow/README_V3_5_PUBLIC_ARTIFACT.md`
4. `support_evidence/it_v3_5_public_support/summary.json`

## Verification

```bash
python3 -m pip install -e ".[dev]"
python3 experiments/it/_workflow/check_v3_5_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json quick
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json support
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json bundle
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/test_integer_time_transfer.py tests/test_it_v3_5_public_surface.py tests/test_text_hygiene.py -q
python3 scripts/check_text_hygiene.py
python3 -m ruff check src tests experiments scripts
python3 scripts/build_v3_5_public_artifact.py --out /tmp --verify-extraction
```

## License

MIT License. See `LICENSE`.
