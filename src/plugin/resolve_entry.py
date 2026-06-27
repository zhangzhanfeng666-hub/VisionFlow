from __future__ import annotations

import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.workflow.service import HDRWorkflowService


def build_plan_for_asset(
    asset_path: str,
    *,
    device_family: str | None = None,
    platform: str = "douyin-hdr",
) -> dict:
    """Resolve-facing entry point for workflow planning.

    This is a lightweight shell that will later be called by a Resolve
    script or plugin host. For now it only bridges into the workflow engine.
    """

    service = HDRWorkflowService(REPO_ROOT)
    plan = service.build_plan(
        asset_path,
        device_family=device_family,
        platform=platform,
    )
    return plan.to_dict()


if __name__ == "__main__":
    example = build_plan_for_asset("fixtures/pocket_sky_hdr_take01.mov")
    print(json.dumps(example, ensure_ascii=False, indent=2))
