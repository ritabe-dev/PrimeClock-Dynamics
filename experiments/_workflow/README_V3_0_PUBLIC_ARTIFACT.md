# PrimeClock Dynamics v3.0 Public Artifact

Status: public artifact verification surface for the Mertens boundary of
Angular Kubilius Chaos. Gate C and Gate P reviews passed. This is not a posted preprint and is not peer reviewed.

Read first:

```text
paper/primeclock_dynamics_v3_0_public_manuscript.md
docs/MB_V3_0_PUBLIC_CLAIM_BOUNDARY.md
experiments/_workflow/pcd_v3_0_public_artifact.json
```

Verification:

```bash
python3 experiments/_workflow/check_v3_0_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_0_public_artifact.json quick
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_0_public_artifact.json support
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v3_0_public_artifact.json bundle
```
