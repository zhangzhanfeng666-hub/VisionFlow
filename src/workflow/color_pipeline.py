from __future__ import annotations

from .models import ColorTransformPlan, PlatformProfile, RecognitionResult


class ColorPipelineBuilder:
    def build(
        self,
        recognition: RecognitionResult,
        platform: PlatformProfile,
    ) -> ColorTransformPlan:
        return ColorTransformPlan(
            normalize_input=recognition.normalization_dctl is not None,
            normalization_dctl=recognition.normalization_dctl,
            working_transfer=recognition.hdr_transfer,
            working_gamut=recognition.hdr_gamut,
            publish_dctl=platform.publish_dctl,
            output_transfer=platform.output_transfer,
            output_gamut=platform.output_gamut,
            metadata_strategy=platform.metadata_strategy,
        )
