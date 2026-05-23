# PrimeClock Dynamics v1.1.0 Public Artifact

Artifact id:

```text
primeclock_dynamics_v1_1_0_shrinking_angle_gaussian_field
```

This workflow verifies the v1.1.0 public artifact surface for the
Shrinking-Angle Gaussian Field release.

Primary manuscript:

```text
paper/primeclock_dynamics_v1_1_manuscript.md
```

Quick verification:

```bash
python3 experiments/_workflow/check_v1_1_public_artifact.py
python3 scripts/verify_candidate_workflow.py --config experiments/_workflow/pcd_v1_1_public_artifact.json quick
python3 scripts/check_text_hygiene.py
python3 -m pytest tests/test_collision_kernel.py -q
```

Bundle rebuild:

```bash
python3 scripts/build_v1_1_public_artifact.py --out /tmp --verify-extraction
```

Boundary:

- public research artifact;
- not DOI or Zenodo unless a separate deposit is issued;
- not a posted preprint;
- not peer reviewed;
- not integer-time transfer;
- not finite-beta Angular Kubilius Chaos.
