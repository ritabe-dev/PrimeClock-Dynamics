#!/usr/bin/env python3
"""Build a versioned PrimeClock Dynamics public artifact.

This is the stable wrapper for future artifact versions. Version-specific
builders own the exact release surface; this wrapper only routes to them and
must not infer a release surface from the whole repository.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build_v0_2_public_artifact import build_zip as build_v0_2_zip
from build_v1_0_public_artifact import build_zip as build_v1_0_zip
from build_v1_1_public_artifact import build_zip as build_v1_1_zip
from build_v2_0_public_artifact import build_zip as build_v2_0_zip


SUPPORTED_VERSIONS = {"0.2.0", "1.0.0", "1.1.0", "2.0.0"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True, choices=sorted(SUPPORTED_VERSIONS))
    parser.add_argument("--out", type=Path, default=Path("/tmp"))
    parser.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()

    if args.version == "0.2.0":
        zip_path, sha_path, file_count = build_v0_2_zip(
            args.out,
            verify=args.verify_extraction,
        )
    elif args.version == "1.0.0":
        zip_path, sha_path, file_count = build_v1_0_zip(
            args.out,
            verify=args.verify_extraction,
        )
    elif args.version == "1.1.0":
        zip_path, sha_path, file_count = build_v1_1_zip(
            args.out,
            verify=args.verify_extraction,
        )
    elif args.version == "2.0.0":
        zip_path, sha_path, file_count = build_v2_0_zip(
            args.out,
            verify=args.verify_extraction,
        )
    else:  # pragma: no cover - argparse choices keep this unreachable.
        raise SystemExit(f"unsupported artifact version: {args.version}")

    print(f"build_artifact: version={args.version}")
    print(f"build_artifact: zip={zip_path}")
    print(f"build_artifact: sha256={sha_path}")
    print(f"build_artifact: files={file_count}")


if __name__ == "__main__":
    main()
