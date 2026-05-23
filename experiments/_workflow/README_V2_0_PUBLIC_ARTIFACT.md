# PrimeClock Dynamics v2.0.0 Public Artifact

This is the public research artifact surface for PrimeClock Dynamics v2.0.0.
It is not a DOI artifact, not a Zenodo record, not a posted preprint, and not
peer reviewed.

## Artifact

```text
pcd_v2_0_public_artifact
```

## Quick Verification

```bash
python3 experiments/_workflow/check_v2_0_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v2_0_public_artifact.json quick
```

## Bundle Verification

```bash
python3 scripts/build_v2_0_public_artifact.py --out /tmp --verify-extraction
```

The bundle excludes internal gate-history packets, future v3.0/v4.0/v5.0
workstreams, `artifacts/`, `app/`, `data/`, and `docs/internal/`.
