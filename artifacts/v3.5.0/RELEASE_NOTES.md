# PrimeClock Dynamics v3.5.0 Release Notes

PrimeClock Dynamics v3.5.0 records a public research artifact for
slow-cutoff integer-time transfer of Mertens-normalized uncovered masses.

This is a GitHub public artifact release. It is not a posted preprint and is
not peer reviewed.

## Included Claim Surface

- `PCD-IT-TV`: total-variation transfer from dyadic integer windows to uniform
  residues modulo `Q`;
- `PCD-IT-DIST`: bounded-test distributional transfer for `F_y=U_y/P_y` under
  `M_y/N -> 0`;
- `PCD-IT-MOM-m`: fixed `m` moment transfer under
  `M_y P_y^{-m}/N -> 0`.

## Non-Claims

This release does not claim full diagonal Mertens transfer, a theorem for
`U_n(n)`, distributional diagonal transfer, a conductor-tail theorem, or any
result beyond the slow-cutoff periodic regime.

The conductor projection table is diagnostic only and does not establish
high-conductor tail decay or diagonal transfer.

## Verification

The release artifact is reproducible through:

```bash
python3 experiments/it/_workflow/check_v3_5_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json quick
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json support
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json bundle
python3 scripts/build_v3_5_public_artifact.py --out /tmp --verify-extraction
```
