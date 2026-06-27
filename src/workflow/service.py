from __future__ import annotations

from pathlib import Path

from .asset_probe import AssetProbeService
from .color_pipeline import ColorPipelineBuilder
from .material_recognizer import MaterialRecognizer
from .models import AssetHints, WorkflowPlan
from .output_planner import OutputPlanner
from .profile_loader import ProfileLoader


class HDRWorkflowService:
    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        loader = ProfileLoader(self.repo_root)
        self.device_profiles = loader.load_device_profiles()
        self.platform_profiles = {profile.id: profile for profile in loader.load_platform_profiles()}
        self.prober = AssetProbeService()
        self.recognizer = MaterialRecognizer(self.device_profiles)
        self.color_builder = ColorPipelineBuilder()
        self.output_planner = OutputPlanner()

    def build_plan(
        self,
        asset_path: str,
        *,
        device_family: str | None = None,
        platform: str = "douyin-hdr",
        force_hdr: bool | None = None,
    ) -> WorkflowPlan:
        if platform not in self.platform_profiles:
            available = ", ".join(sorted(self.platform_profiles))
            raise ValueError(f"unknown platform profile '{platform}', expected one of: {available}")

        probe = self.prober.probe(asset_path)
        hints = AssetHints(device_family=device_family, platform=platform, force_hdr=force_hdr)
        recognition = self.recognizer.recognize(probe, hints)
        platform_profile = self.platform_profiles[platform]
        color = self.color_builder.build(recognition, platform_profile)
        output = self.output_planner.build(asset_path, platform_profile)

        warnings: list[str] = []
        if not probe.exists:
            warnings.append("asset path does not exist; plan was built from path and hints only")
        if not probe.ffprobe_available:
            warnings.append("ffprobe not found; metadata probing fell back to file name and extension heuristics")
        if recognition.confidence < 0.5:
            warnings.append("low-confidence recognition; provide device_family hint or improve fixture naming")

        return WorkflowPlan(
            asset=probe,
            recognition=recognition,
            color=color,
            output=output,
            warnings=warnings,
        )
