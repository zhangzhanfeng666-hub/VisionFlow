from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AssetHints:
    device_family: str | None = None
    platform: str | None = None
    force_hdr: bool | None = None


@dataclass(slots=True)
class AssetProbe:
    path: str
    exists: bool
    file_name: str
    extension: str
    size_bytes: int | None
    ffprobe_available: bool
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DeviceProfile:
    id: str
    family: str
    match_extensions: list[str]
    filename_keywords: list[str]
    hdr_transfer: str
    hdr_gamut: str
    normalization_dctl: str | None
    notes: str


@dataclass(slots=True)
class PlatformProfile:
    id: str
    publish_target: str
    output_container: str
    output_codec: str
    output_transfer: str
    output_gamut: str
    metadata_strategy: str
    publish_dctl: str | None
    notes: str


@dataclass(slots=True)
class RecognitionResult:
    device_profile: str
    device_family: str
    hdr_transfer: str
    hdr_gamut: str
    normalization_dctl: str | None
    confidence: float
    reasons: list[str]


@dataclass(slots=True)
class ColorTransformPlan:
    normalize_input: bool
    normalization_dctl: str | None
    working_transfer: str
    working_gamut: str
    publish_dctl: str | None
    output_transfer: str
    output_gamut: str
    metadata_strategy: str


@dataclass(slots=True)
class OutputPlan:
    publish_target: str
    output_container: str
    output_codec: str
    output_file_name: str
    output_relative_dir: str


@dataclass(slots=True)
class WorkflowPlan:
    asset: AssetProbe
    recognition: RecognitionResult
    color: ColorTransformPlan
    output: OutputPlan
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_output_name(path: str, suffix: str, new_extension: str) -> str:
    source = Path(path)
    stem = source.stem
    return f"{stem}_{suffix}{new_extension}"
