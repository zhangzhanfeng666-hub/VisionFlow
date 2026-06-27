from __future__ import annotations

from .models import OutputPlan, PlatformProfile, build_output_name


class OutputPlanner:
    def build(self, asset_path: str, platform: PlatformProfile) -> OutputPlan:
        extension = ".mov" if platform.output_container == "mov" else f".{platform.output_container}"
        return OutputPlan(
            publish_target=platform.publish_target,
            output_container=platform.output_container,
            output_codec=platform.output_codec,
            output_file_name=build_output_name(asset_path, "publish-hdr", extension),
            output_relative_dir="tests/exports",
        )
