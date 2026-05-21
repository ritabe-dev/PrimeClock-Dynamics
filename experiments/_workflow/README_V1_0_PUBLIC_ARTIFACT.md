# PrimeClock Dynamics v1.0.0 Public Artifact

This is the public research artifact verification surface for PrimeClock Dynamics
v1.0.0. It is not peer reviewed. It is not a DOI artifact or Zenodo record
unless a DOI/Zenodo deposit is issued separately.

Artifact id:

```text
primeclock_dynamics_v1_0_0_angular_ek_fixed_cutoff_mertens
```

Read first:

```text
paper/primeclock_dynamics_v1_0_preprint.md
docs/CLAIM_BOUNDARY.md
RELEASE_NOTES_v1_0_0.md
ARTIFACT_MANIFEST_v1_0_0.json
```

Verification:

```bash
python3 experiments/_workflow/check_v1_0_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v1_0_public_artifact.json quick
python3 scripts/build_v1_0_public_artifact.py --out /tmp --verify-extraction
```
