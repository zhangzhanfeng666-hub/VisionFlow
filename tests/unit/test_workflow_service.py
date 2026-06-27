import unittest
from pathlib import Path

from src.workflow.service import HDRWorkflowService


class WorkflowServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[2]
        self.service = HDRWorkflowService(self.repo_root)

    def test_build_plan_for_pocket_asset_by_filename(self) -> None:
        plan = self.service.build_plan("fixtures/pocket_sky_hdr_take01.mov")
        self.assertEqual(plan.recognition.device_family, "pocket")
        self.assertEqual(plan.color.output_transfer, "rec2100-hlg")
        self.assertEqual(plan.output.publish_target, "douyin")
        self.assertIn("publish-hdr", plan.output.output_file_name)

    def test_build_plan_with_hint_for_iphone(self) -> None:
        plan = self.service.build_plan(
            "fixtures/random_clip.mov",
            device_family="iphone",
        )
        self.assertEqual(plan.recognition.device_family, "iphone")
        self.assertGreaterEqual(plan.recognition.confidence, 0.9)

    def test_unknown_platform_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.service.build_plan("fixtures/sample.mov", platform="unknown")


if __name__ == "__main__":
    unittest.main()
