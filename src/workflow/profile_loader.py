from __future__ import annotations

import json
from pathlib import Path

from .models import DeviceProfile, PlatformProfile


class ProfileLoader:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def load_device_profiles(self) -> list[DeviceProfile]:
        path = self.repo_root / "profiles" / "devices" / "profiles.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        return [DeviceProfile(**item) for item in payload["profiles"]]

    def load_platform_profiles(self) -> list[PlatformProfile]:
        path = self.repo_root / "profiles" / "platforms" / "profiles.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        return [PlatformProfile(**item) for item in payload["profiles"]]
