from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .models import AssetProbe


class AssetProbeService:
    def probe(self, asset_path: str) -> AssetProbe:
        path = Path(asset_path)
        exists = path.exists()
        metadata: dict[str, object] = {}
        ffprobe_available = shutil.which("ffprobe") is not None

        if exists and ffprobe_available:
            metadata = self._probe_with_ffprobe(path)

        return AssetProbe(
            path=str(path),
            exists=exists,
            file_name=path.name,
            extension=path.suffix.lower(),
            size_bytes=path.stat().st_size if exists else None,
            ffprobe_available=ffprobe_available,
            metadata=metadata,
        )

    def _probe_with_ffprobe(self, path: Path) -> dict[str, object]:
        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(path),
        ]
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        except (subprocess.CalledProcessError, OSError):
            return {}
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {}
