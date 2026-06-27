from __future__ import annotations

from .models import AssetHints, AssetProbe, DeviceProfile, RecognitionResult


class MaterialRecognizer:
    def __init__(self, profiles: list[DeviceProfile]) -> None:
        self.profiles = profiles

    def recognize(self, probe: AssetProbe, hints: AssetHints) -> RecognitionResult:
        if hints.device_family:
            hinted = self._by_family(hints.device_family)
            if hinted is not None:
                return RecognitionResult(
                    device_profile=hinted.id,
                    device_family=hinted.family,
                    hdr_transfer=hinted.hdr_transfer,
                    hdr_gamut=hinted.hdr_gamut,
                    normalization_dctl=hinted.normalization_dctl,
                    confidence=0.95,
                    reasons=[f"device family forced by hint: {hints.device_family}"],
                )

        candidates: list[tuple[float, DeviceProfile, list[str]]] = []
        file_name = probe.file_name.lower()
        extension = probe.extension.lower()

        for profile in self.profiles:
            score = 0.0
            reasons: list[str] = []

            if extension in profile.match_extensions:
                score += 0.35
                reasons.append(f"extension matched {extension}")

            keyword_hits = [kw for kw in profile.filename_keywords if kw in file_name]
            if keyword_hits:
                score += min(0.55, 0.2 * len(keyword_hits))
                reasons.append(f"filename keywords matched: {', '.join(keyword_hits)}")

            if score > 0:
                candidates.append((score, profile, reasons))

        if not candidates:
            fallback = self._by_family("generic-hdr") or self.profiles[0]
            return RecognitionResult(
                device_profile=fallback.id,
                device_family=fallback.family,
                hdr_transfer=fallback.hdr_transfer,
                hdr_gamut=fallback.hdr_gamut,
                normalization_dctl=fallback.normalization_dctl,
                confidence=0.25,
                reasons=["no profile strongly matched; fell back to generic HDR profile"],
            )

        score, profile, reasons = sorted(candidates, key=lambda item: item[0], reverse=True)[0]
        return RecognitionResult(
            device_profile=profile.id,
            device_family=profile.family,
            hdr_transfer=profile.hdr_transfer,
            hdr_gamut=profile.hdr_gamut,
            normalization_dctl=profile.normalization_dctl,
            confidence=round(score, 2),
            reasons=reasons,
        )

    def _by_family(self, family: str) -> DeviceProfile | None:
        for profile in self.profiles:
            if profile.family == family:
                return profile
        return None
