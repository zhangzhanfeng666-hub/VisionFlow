from __future__ import annotations

import argparse
import json
from pathlib import Path

from .service import HDRWorkflowService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HDR Creator workflow planner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Build a workflow plan for one asset")
    plan.add_argument("asset_path", help="Path to the source media asset")
    plan.add_argument("--device-family", help="Override inferred device family, e.g. pocket or iphone")
    plan.add_argument("--platform", default="douyin-hdr", help="Output platform profile id")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    service = HDRWorkflowService(repo_root)

    if args.command == "plan":
        plan = service.build_plan(
            args.asset_path,
            device_family=args.device_family,
            platform=args.platform,
        )
        print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2))
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
