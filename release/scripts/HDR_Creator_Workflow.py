from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
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
BIN_ID = "bin_name"
TIMELINE_ID = "timeline_name"
CREATE_TIMELINE_ID = "create_timeline"
RENDER_DIR_ID = "render_dir"
BROWSE_RENDER_DIR_ID = "browse_render_dir"
RENDER_PRESET_ID = "render_preset"
RENDER_NAME_ID = "render_name"
QUEUE_RENDER_ID = "queue_render"
REFRESH_PRESETS_ID = "refresh_presets"


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


def _bin_name() -> str:
    value = _get_items()[BIN_ID].Text.strip()
    return value or "HDR Creator Inbox"


def _timeline_name() -> str:
    value = _get_items()[TIMELINE_ID].Text.strip()
    if value:
        return value
    asset = Path(_asset_path())
    return f"{asset.stem}_timeline" if asset.stem else "HDR Creator Timeline"


def _render_dir() -> str:
    value = _get_items()[RENDER_DIR_ID].Text.strip()
    if value:
        return value
    return str(REPO_ROOT / "tests" / "exports")


def _render_name() -> str:
    value = _get_items()[RENDER_NAME_ID].Text.strip()
    if value:
        return value
    asset = Path(_asset_path())
    return f"{asset.stem}_publish_hdr" if asset.stem else "hdr_creator_publish_hdr"


def _render_preset() -> str:
    return _get_items()[RENDER_PRESET_ID].CurrentText.strip()


def _set_plan_output(payload: dict) -> None:
    _get_items()[PLAN_ID].PlainText = json.dumps(payload, ensure_ascii=False, indent=2)


def _project():
    manager = resolve.GetProjectManager()
    if not manager:
        raise RuntimeError("Could not access Resolve project manager")
    project = manager.GetCurrentProject()
    if not project:
        raise RuntimeError("No current Resolve project is open")
    return project


def _media_pool():
    pool = _project().GetMediaPool()
    if not pool:
        raise RuntimeError("Could not access current media pool")
    return pool


def _root_folder():
    folder = _media_pool().GetRootFolder()
    if not folder:
        raise RuntimeError("Could not access media pool root folder")
    return folder


def _find_subfolder_by_name(parent_folder, folder_name: str):
    for folder in parent_folder.GetSubFolderList() or []:
        if folder.GetName() == folder_name:
            return folder
    return None


def _ensure_bin(folder_name: str):
    media_pool = _media_pool()
    root = _root_folder()
    folder = _find_subfolder_by_name(root, folder_name)
    if not folder:
        folder = media_pool.AddSubFolder(root, folder_name)
    if not folder:
        raise RuntimeError(f"Could not create or resolve bin: {folder_name}")
    media_pool.SetCurrentFolder(folder)
    return folder


def browse_asset(ev):
    selected_path = fusion.RequestFile()
    if selected_path:
        _get_items()[ASSET_ID].Text = str(selected_path)
        asset = Path(str(selected_path))
        if not _get_items()[TIMELINE_ID].Text.strip():
            _get_items()[TIMELINE_ID].Text = f"{asset.stem}_timeline"
        if not _get_items()[RENDER_NAME_ID].Text.strip():
            _get_items()[RENDER_NAME_ID].Text = f"{asset.stem}_publish_hdr"
        _status("Asset selected. You can now build a workflow plan.")


def browse_render_dir(ev):
    selected_path = fusion.RequestDir()
    if selected_path:
        _get_items()[RENDER_DIR_ID].Text = str(selected_path)
        _status("Render output directory selected.")


def generate_plan(ev):
    asset_path = _asset_path()
    if not asset_path:
        _status("Please choose a source asset first.")
        return

    service = _get_service()
    try:
        plan = service.build_plan(
            asset_path,
            device_family=_selected_device_family(),
            platform=_selected_platform(),
        )
    except Exception as exc:
        _status(f"Plan generation failed: {exc}")
        return

    payload = plan.to_dict()
    _set_plan_output(payload)
    _get_items()[RENDER_NAME_ID].Text = payload["output"]["output_file_name"].rsplit(".", 1)[0]

    if _get_items()[IMPORT_ID].Checked:
        try:
            import_media_to_bin(asset_path, _bin_name())
            _status("Plan generated and media imported into the target bin.")
        except Exception as exc:
            _status(f"Plan generated, but media import failed: {exc}")
    else:
        _status("Workflow plan generated.")


def import_media(ev):
    asset_path = _asset_path()
    if not asset_path:
        _status("Please choose a source asset first.")
        return

    try:
        import_media_to_bin(asset_path, _bin_name())
        _status("Media imported into the target bin.")
    except Exception as exc:
        _status(f"Media import failed: {exc}")


def create_timeline(ev):
    try:
        timeline = create_timeline_from_bin(_bin_name(), _timeline_name())
        if not timeline:
            _status("Timeline creation returned no timeline object.")
            return
        _status(f"Timeline created: {_timeline_name()}")
    except Exception as exc:
        _status(f"Timeline creation failed: {exc}")


def queue_render(ev):
    try:
        job_id = queue_render_job(_render_preset(), _render_dir(), _render_name())
        if not job_id:
            _status("Failed to add render job.")
            return
        _status(f"Render job queued: {job_id}")
    except Exception as exc:
        _status(f"Queue render failed: {exc}")


def refresh_render_presets(ev=None):
    combo = win.Find(RENDER_PRESET_ID)
    combo.Clear()
    presets = []
    try:
        presets = _project().GetRenderPresets() or []
    except Exception:
        presets = []

    if presets:
        for preset in presets:
            combo.AddItem(preset)
        combo.CurrentIndex = 0
        _status("Render preset list refreshed.")
    else:
        combo.AddItem("H.265 Master")
        combo.CurrentIndex = 0
        _status("Could not query render presets; using fallback preset label.")


def import_media_to_bin(asset_path: str, bin_name: str):
    resolve.OpenPage("media")
    _ensure_bin(bin_name)
    result = _media_pool().ImportMedia([asset_path])
    if not result:
        raise RuntimeError("Resolve failed to import the selected asset")
    return result


def create_timeline_from_bin(bin_name: str, timeline_name: str):
    resolve.OpenPage("media")
    media_pool = _media_pool()
    target_bin = _ensure_bin(bin_name)
    clips = target_bin.GetClipList() or []
    if not clips:
        raise RuntimeError("The target bin has no clips to build a timeline from")
    return media_pool.CreateTimelineFromClips(timeline_name, clips)


def queue_render_job(render_preset: str, target_dir: str, custom_name: str):
    resolve.OpenPage("deliver")
    project = _project()
    if render_preset:
        project.LoadRenderPreset(render_preset)
    settings = {
        "TargetDir": target_dir,
        "CustomName": custom_name,
        "SelectAllFrames": 1,
    }
    if not project.SetRenderSettings(settings):
        raise RuntimeError("Resolve rejected render settings")
    return project.AddRenderJob()


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
        "Geometry": [100, 100, 980, 760],
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
                    "Text": "V2: asset selection, device recognition, bin import, timeline creation, render job setup",
                    "Weight": 0,
                }
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.LineEdit(
                        {
                            "ID": ASSET_ID,
                            "PlaceholderText": "Choose a Pocket or iPhone HDR source file",
                            "Weight": 0.82,
                        }
                    ),
                    ui.Button({"ID": BROWSE_ID, "Text": "Choose Asset", "Weight": 0.18}),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Label({"Text": "Device", "Weight": 0}),
                    ui.ComboBox({"ID": DEVICE_ID, "Weight": 0.18}),
                    ui.Label({"Text": "Platform", "Weight": 0}),
                    ui.ComboBox({"ID": PLATFORM_ID, "Weight": 0.18}),
                    ui.CheckBox({"ID": IMPORT_ID, "Text": "Import to bin after planning", "Weight": 0.4}),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Label({"Text": "Target Bin", "Weight": 0}),
                    ui.LineEdit({"ID": BIN_ID, "Text": "HDR Creator Inbox", "Weight": 0.3}),
                    ui.Label({"Text": "Timeline", "Weight": 0}),
                    ui.LineEdit({"ID": TIMELINE_ID, "Text": "HDR Creator Timeline", "Weight": 0.35}),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Label({"Text": "Render Preset", "Weight": 0}),
                    ui.ComboBox({"ID": RENDER_PRESET_ID, "Weight": 0.35}),
                    ui.Button({"ID": REFRESH_PRESETS_ID, "Text": "Refresh Presets", "Weight": 0.18}),
                    ui.HGap(0, 0.47),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.LineEdit(
                        {
                            "ID": RENDER_DIR_ID,
                            "Text": str(REPO_ROOT / "tests" / "exports"),
                            "Weight": 0.62,
                        }
                    ),
                    ui.Button({"ID": BROWSE_RENDER_DIR_ID, "Text": "Output Folder", "Weight": 0.18}),
                    ui.LineEdit({"ID": RENDER_NAME_ID, "Text": "hdr_creator_publish_hdr", "Weight": 0.2}),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Button({"ID": GENERATE_ID, "Text": "Generate Plan", "Weight": 0.2}),
                    ui.Button({"ID": IMPORT_BUTTON_ID, "Text": "Import To Bin", "Weight": 0.18}),
                    ui.Button({"ID": CREATE_TIMELINE_ID, "Text": "Create Timeline", "Weight": 0.18}),
                    ui.Button({"ID": QUEUE_RENDER_ID, "Text": "Queue Render Job", "Weight": 0.2}),
                    ui.HGap(0, 0.24),
                ],
            ),
            ui.Label({"Text": "Workflow Plan", "Weight": 0}),
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
                    "Text": "Ready.",
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

refresh_render_presets()

win.On[WINDOW_ID].Close = on_close
win.On[BROWSE_ID].Clicked = browse_asset
win.On[BROWSE_RENDER_DIR_ID].Clicked = browse_render_dir
win.On[GENERATE_ID].Clicked = generate_plan
win.On[IMPORT_BUTTON_ID].Clicked = import_media
win.On[CREATE_TIMELINE_ID].Clicked = create_timeline
win.On[QUEUE_RENDER_ID].Clicked = queue_render
win.On[REFRESH_PRESETS_ID].Clicked = refresh_render_presets

win.Show()
dispatcher.RunLoop()
