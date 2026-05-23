# Public Artifact Policy

This policy fixes how PrimeClock Dynamics public artifacts are organized as the
repository grows beyond v0.2.0.

## Purpose

A public artifact is a narrow, reproducible release surface for one versioned
claim set. It is not a transcript of the research process. It should let a
reader answer four questions:

- what is included;
- what is not claimed;
- how to verify it;
- how to cite it.

## Versioned Artifact Directory

Every public version gets a directory under `artifacts/`. This rule is
version-generic: it applies to v0, v1, v2, and every later public version. A
new public release is incomplete until this directory exists.

```text
artifacts/vX.Y.Z/
  ARTIFACT_MANIFEST.json
  RELEASE_NOTES.md
  CITATION.cff
```

The root-level files may remain the public landing surface for the current
release, but the versioned directory is the stable audit surface once a version
is published.

Published artifacts must keep a frozen source surface under the versioned
directory:

```text
artifacts/vX.Y.Z/source/
```

Builders for an already-published version must read from that frozen source
surface, not from branch-local research files such as the current
`docs/CLAIM_BOUNDARY.md`. DOI-backed versions use the DOI-archived release ZIP
as the canonical frozen source when it differs from a later refreshed GitHub
asset.

## Required Invariant

For every public version `vX.Y.Z`, the repository must satisfy:

- `artifacts/vX.Y.Z/ARTIFACT_MANIFEST.json` exists;
- `artifacts/vX.Y.Z/RELEASE_NOTES.md` exists;
- `artifacts/vX.Y.Z/CITATION.cff` exists;
- `artifacts/vX.Y.Z/source/` exists and is a frozen copy of the public ZIP
  source surface;
- `scripts/build_artifact.py --version X.Y.Z` can rebuild from that frozen
  source surface;
- generated caches such as `.pytest_cache`, `__pycache__`, and `.DS_Store` do
  not appear under `artifacts/vX.Y.Z/`;
- DOI-backed versions also keep `DOI_RECORD.md` and `SHA256SUMS.txt`.

Run `python3 scripts/check_public_artifact_protocol.py` after adding or changing
any public artifact version.

## Public ZIP Surface

Public artifacts are created only for closed claim surfaces that pass Gate P.
Do not create a public artifact merely because the internal research version
increased by `0.1`.

Public ZIP builders should include only:

- public landing files, release notes, citation metadata, license, and manifest;
- the main note for the released claim set;
- stable mathematical docs needed to understand the release;
- source, focused tests, verification scripts, and deterministic support
  evidence.

Public ZIP builders should exclude:

- internal gate records, review packets, draft requests, status registries, and
  work logs;
- roadmaps, future planning notes, and internal verification records;
- progress percentages, slice estimates, impact scoring, or other process
  commentary;
- detailed future-version notes unless the release explicitly includes them;
- visual app code unless visual evidence is part of the claim surface;
- generated data outside the deterministic support evidence selected by the
  artifact builder.

Public ZIP tests must be self-contained within the ZIP. A test included in a
public artifact must not import internal Gate R/Gate C support builders,
future-version workflows, review packets, or branch-local research files.

## Post-Publication Maintenance

After a versioned public artifact is released, treat the published ZIP and
checksum as immutable. Do not replace release assets for ordinary maintenance.
If a public-facing correction changes artifact contents, make a patch release
such as `v0.2.1` with its own manifest, release notes, citation metadata, ZIP,
and checksum.

Internal records may store release URLs, tag names, workflow evidence, and
checksums for auditability. Those records are process history and must stay out
of public artifact ZIPs unless a future artifact explicitly defines them as part
of its release surface.

When checking public-artifact invariance from a research branch, use either the
released branch/tag/worktree or the frozen source surface. Do not compare a
published SHA against a build that inferred files from the current research
branch.

## Future DOI And Preprint Layout

If a later version becomes DOI-backed, place DOI metadata in that versioned
directory:

```text
artifacts/vX.Y.Z/
  ARTIFACT_MANIFEST.json
  RELEASE_NOTES.md
  CITATION.cff
  DOI_RECORD.md
  SHA256SUMS.txt
```

If a later version becomes a preprint, keep the paper source separate from the
artifact metadata:

```text
paper/vX_Y_preprint/
  main.tex
  references.bib
  figures/

artifacts/vX.Y.Z/
  ARTIFACT_MANIFEST.json
  RELEASE_NOTES.md
  CITATION.cff
```

The preprint explains the mathematics. The artifact remains the reproducible
source/support bundle.

## Builder Rule

Version-specific builders may remain as wrappers, but the long-term entrypoint
is `scripts/build_artifact.py --version X.Y.Z`. That wrapper must delegate to
the version-specific builder and must not infer a release surface from the
whole repository.
