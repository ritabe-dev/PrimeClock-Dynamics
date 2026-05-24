# PrimeClock Dynamics v3.5.0 Public Artifact

Status: public artifact workflow for slow-cutoff integer-time transfer. This is
not a posted preprint and is not peer reviewed.

## Reading Order

1. `paper/primeclock_dynamics_v3_5_public_manuscript.md`
2. `docs/IT_V3_5_PUBLIC_CLAIM_BOUNDARY.md`
3. `experiments/_workflow/pcd_v3_5_public_artifact.json`
4. `support_evidence/it_v3_5_public_support/summary.json`

## Verification

```bash
python3 experiments/it/_workflow/check_v3_5_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json quick
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json support
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_5_public_artifact.json bundle
```
