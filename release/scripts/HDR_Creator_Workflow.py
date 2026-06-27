from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(r"C:\Users\wuche\Desktop\HDR_Master")
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.workflow.service import HDRWorkflowService


WINDOW_ID = "com.hdrcreator.resolve.workflow"
ASSET_ID = "asset_path"
DEVICE_ID = "device_family"
PLATFORM_ID = "platform"
PLAN_ID = "plan_output"
STATUS_ID = "status_line"
IMPORT_ID = "import_after_plan"
GENERATE_ID = "generate_plan"
BROWSE_ID = "browse_asset"
IMPORT_BUTTON_ID = "import_media"


def _status(message: str) -> None:
    win.Find(STATUS_ID).Text = message


def _get_service() -> HDRWorkflowService:
    return HDRWorkflowService(REPO_ROOT)


def _get_items():
    return win.GetItems()


def _selected_device_family() -> str | None:
    current_text = _get_items()[DEVICE_ID].CurrentText
    if current_text == "auto":
        return None
    return current_text


def _selected_platform() -> str:
    return _get_items()[PLATFORM_ID].CurrentText or "douyin-hdr"


def _asset_path() -> str:
    return _get_items()[ASSET_ID].Text.strip()


def _set_plan_output(payload: dict) -> None:
    _get_items()[PLAN_ID].PlainText = json.dumps(payload, ensure_ascii=False, indent=2)


def browse_asset(ev):
    selected_path = fusion.RequestFile()
    if selected_path:
        _get_items()[ASSET_ID].Text = str(selected_path)
        _status("素材路径已选择，可以生成工作流计划。")


def generate_plan(ev):
    asset_path = _asset_path()
    if not asset_path:
        _status("请先选择素材路径。")
        return

    service = _get_service()
    try:
        plan = service.build_plan(
            asset_path,
            device_family=_selected_device_family(),
            platform=_selected_platform(),
        )
    except Exception as exc:
        _status(f"生成计划失败: {exc}")
        return

    payload = plan.to_dict()
    _set_plan_output(payload)

    if _get_items()[IMPORT_ID].Checked:
        try:
            import_media_to_current_bin(asset_path)
            _status("计划已生成，并已尝试导入当前媒体池。")
        except Exception as exc:
            _status(f"计划已生成，但导入媒体失败: {exc}")
    else:
        _status("工作流计划已生成。")


def import_media(ev):
    asset_path = _asset_path()
    if not asset_path:
        _status("请先选择素材路径。")
        return

    try:
        import_media_to_current_bin(asset_path)
        _status("素材已导入当前媒体池。")
    except Exception as exc:
        _status(f"导入素材失败: {exc}")


def import_media_to_current_bin(asset_path: str) -> None:
    current_project = resolve.GetProjectManager().GetCurrentProject()
    if not current_project:
        raise RuntimeError("当前没有打开的 Resolve 项目")
    media_pool = current_project.GetMediaPool()
    if not media_pool:
        raise RuntimeError("无法获取当前项目的媒体池")
    result = media_pool.ImportMedia([asset_path])
    if not result:
        raise RuntimeError("Resolve 未成功导入该素材")


def on_close(ev):
    dispatcher.ExitLoop()


ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

existing = ui.FindWindow(WINDOW_ID)
if existing:
    existing.Show()
    existing.Raise()
    sys.exit(0)


win = dispatcher.AddWindow(
    {
        "ID": WINDOW_ID,
        "WindowTitle": "HDR Creator Workflow",
        "Geometry": [100, 100, 860, 680],
    },
    ui.VGroup(
        {"Spacing": 8},
        [
            ui.Label(
                {
                    "Text": "HDR Creator Resolve Workflow",
                    "Weight": 0,
                    "Font": ui.Font({"Family": "Segoe UI", "PixelSize": 18, "Bold": True}),
                }
            ),
            ui.Label(
                {
                    "Text": "第一版目标：选素材 -> 识别设备 -> 生成 HDR 发布工作流计划",
                    "Weight": 0,
                }
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.LineEdit(
                        {
                            "ID": ASSET_ID,
                            "PlaceholderText": "选择素材路径，例如 Pocket 或 iPhone HDR 素材",
                            "Weight": 0.85,
                        }
                    ),
                    ui.Button({"ID": BROWSE_ID, "Text": "选择素材", "Weight": 0.15}),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Label({"Text": "设备识别", "Weight": 0}),
                    ui.ComboBox({"ID": DEVICE_ID, "Weight": 0.2}),
                    ui.Label({"Text": "输出平台", "Weight": 0}),
                    ui.ComboBox({"ID": PLATFORM_ID, "Weight": 0.2}),
                    ui.CheckBox({"ID": IMPORT_ID, "Text": "生成计划后导入当前媒体池", "Weight": 0.4}),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Button({"ID": GENERATE_ID, "Text": "生成工作流计划", "Weight": 0.25}),
                    ui.Button({"ID": IMPORT_BUTTON_ID, "Text": "仅导入素材", "Weight": 0.2}),
                    ui.HGap(0, 0.55),
                ],
            ),
            ui.Label({"Text": "计划输出", "Weight": 0}),
            ui.TextEdit(
                {
                    "ID": PLAN_ID,
                    "ReadOnly": True,
                    "AcceptRichText": False,
                    "LineWrapMode": "NoWrap",
                    "Lexer": "json",
                    "Font": ui.Font({"Family": "Consolas", "PixelSize": 11, "MonoSpaced": True}),
                    "Weight": 1,
                }
            ),
            ui.LineEdit(
                {
                    "ID": STATUS_ID,
                    "ReadOnly": True,
                    "Text": "准备就绪。",
                    "Weight": 0,
                }
            ),
        ],
    ),
)

device_combo = win.Find(DEVICE_ID)
for item in ["auto", "pocket", "iphone", "generic-hdr"]:
    device_combo.AddItem(item)
device_combo.CurrentIndex = 0

platform_combo = win.Find(PLATFORM_ID)
for item in ["douyin-hdr"]:
    platform_combo.AddItem(item)
platform_combo.CurrentIndex = 0

win.On[WINDOW_ID].Close = on_close
win.On[BROWSE_ID].Clicked = browse_asset
win.On[GENERATE_ID].Clicked = generate_plan
win.On[IMPORT_BUTTON_ID].Clicked = import_media

win.Show()
dispatcher.RunLoop()
