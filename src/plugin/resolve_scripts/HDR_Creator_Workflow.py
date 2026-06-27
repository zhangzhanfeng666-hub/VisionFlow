import json
import os


WINDOW_ID = "com.hdrcreator.resolve.workflow.safev1"
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
RENDER_NAME_ID = "render_name"
RENDER_PRESET_ID = "render_preset"
QUEUE_RENDER_ID = "queue_render"


def status(message):
    try:
        win.Find(STATUS_ID).Text = message
    except Exception:
        pass


def items():
    return win.GetItems()


def asset_path():
    return items()[ASSET_ID].Text.strip()


def selected_device_family():
    value = items()[DEVICE_ID].CurrentText
    if value == "auto":
        return None
    return value


def selected_platform():
    value = items()[PLATFORM_ID].CurrentText
    if value:
        return value
    return "douyin"


def bin_name():
    value = items()[BIN_ID].Text.strip()
    if value:
        return value
    return "HDR Creator Inbox"


def timeline_name():
    value = items()[TIMELINE_ID].Text.strip()
    if value:
        return value
    asset = os.path.splitext(os.path.basename(asset_path()))[0]
    if asset:
        return asset + "_timeline"
    return "HDR Creator Timeline"


def render_dir():
    value = items()[RENDER_DIR_ID].Text.strip()
    if value:
        return value
    home = os.path.expanduser("~")
    return os.path.join(home, "Videos", "HDR Creator Exports")


def render_name():
    value = items()[RENDER_NAME_ID].Text.strip()
    if value:
        return value
    asset = os.path.splitext(os.path.basename(asset_path()))[0]
    if asset:
        return asset + "_publish_hdr"
    return "hdr_creator_publish_hdr"


def render_preset():
    value = items()[RENDER_PRESET_ID].Text.strip()
    if value:
        return value
    return "H.265 Master"


def set_plan_output(payload):
    items()[PLAN_ID].PlainText = json.dumps(payload, ensure_ascii=False, indent=2)


def browse_asset(ev):
    selected_path = fusion.RequestFile()
    if selected_path:
        items()[ASSET_ID].Text = str(selected_path)
        asset = os.path.splitext(os.path.basename(str(selected_path)))[0]
        if not items()[TIMELINE_ID].Text.strip():
            items()[TIMELINE_ID].Text = asset + "_timeline"
        if not items()[RENDER_NAME_ID].Text.strip():
            items()[RENDER_NAME_ID].Text = asset + "_publish_hdr"
        status("Asset selected.")


def build_basic_plan(source_asset, device_value, platform_value):
    name = os.path.basename(source_asset)
    lower_name = name.lower()
    extension = os.path.splitext(name)[1].lower()

    if device_value:
        family = device_value
        confidence = 0.95
        reasons = ["device family forced by user"]
    elif "iphone" in lower_name or "apple" in lower_name:
        family = "iphone"
        confidence = 0.75
        reasons = ["filename matched iphone/apple"]
    elif "pocket" in lower_name or "dji" in lower_name or "osmo" in lower_name:
        family = "pocket"
        confidence = 0.75
        reasons = ["filename matched pocket/dji/osmo"]
    else:
        family = "generic-hdr"
        confidence = 0.30
        reasons = ["no strong match; generic fallback"]

    if family == "iphone":
        normalize_dctl = "src/dctl/input-normalize/HDRC_normalize_iphone_hlg.dctl"
    elif family == "pocket":
        normalize_dctl = "src/dctl/input-normalize/HDRC_normalize_pocket_hlg.dctl"
    else:
        normalize_dctl = None

    return {
        "asset": {
            "path": source_asset,
            "exists": os.path.exists(source_asset),
            "file_name": name,
            "extension": extension,
            "size_bytes": os.path.getsize(source_asset) if os.path.exists(source_asset) else None,
            "metadata": {}
        },
        "recognition": {
            "device_family": family,
            "confidence": confidence,
            "reasons": reasons
        },
        "color": {
            "normalize_input": normalize_dctl is not None,
            "normalization_dctl": normalize_dctl,
            "publish_dctl": "src/dctl/hdr-publish/HDRC_publish_pocket_hdr.dctl",
            "output_transfer": "rec2100-hlg",
            "output_gamut": "rec2020"
        },
        "output": {
            "publish_target": platform_value,
            "output_container": "mov",
            "output_codec": "hevc-main10",
            "output_file_name": os.path.splitext(name)[0] + "_publish-hdr.mov"
        },
        "warnings": [] if os.path.exists(source_asset) else ["asset path does not exist; plan built from path only"]
    }


def current_project():
    manager = resolve.GetProjectManager()
    if not manager:
        raise RuntimeError("Could not access Resolve project manager")
    project = manager.GetCurrentProject()
    if not project:
        raise RuntimeError("No current Resolve project is open")
    return project


def media_pool():
    pool = current_project().GetMediaPool()
    if not pool:
        raise RuntimeError("Could not access current media pool")
    return pool


def root_folder():
    folder = media_pool().GetRootFolder()
    if not folder:
        raise RuntimeError("Could not access media pool root folder")
    return folder


def find_subfolder_by_name(parent_folder, folder_name_value):
    folders = parent_folder.GetSubFolderList() or []
    for folder in folders:
        if folder.GetName() == folder_name_value:
            return folder
    return None


def ensure_bin(folder_name_value):
    pool = media_pool()
    root = root_folder()
    folder = find_subfolder_by_name(root, folder_name_value)
    if not folder:
        folder = pool.AddSubFolder(root, folder_name_value)
    if not folder:
        raise RuntimeError("Could not create or resolve bin: {0}".format(folder_name_value))
    pool.SetCurrentFolder(folder)
    return folder


def import_media_to_bin(source_asset, folder_name_value):
    resolve.OpenPage("media")
    ensure_bin(folder_name_value)
    result = media_pool().ImportMedia([source_asset])
    if not result:
        raise RuntimeError("Resolve failed to import the selected asset")
    return result


def create_timeline_from_bin(folder_name_value, timeline_name_value):
    resolve.OpenPage("media")
    pool = media_pool()
    target_bin = ensure_bin(folder_name_value)
    clips = target_bin.GetClipList() or []
    if not clips:
        raise RuntimeError("The target bin has no clips to build a timeline from")
    return pool.CreateTimelineFromClips(timeline_name_value, clips)


def queue_render_job(render_preset_value, target_dir_value, custom_name_value):
    resolve.OpenPage("deliver")
    project = current_project()
    if not os.path.exists(target_dir_value):
        os.makedirs(target_dir_value)

    if render_preset_value:
        preset_loaded = project.LoadRenderPreset(render_preset_value)
        if not preset_loaded:
            raise RuntimeError("Resolve could not load render preset: {0}".format(render_preset_value))

    settings = {
        "TargetDir": target_dir_value,
        "CustomName": custom_name_value,
        "SelectAllFrames": 1
    }
    if not project.SetRenderSettings(settings):
        raise RuntimeError("Resolve rejected render settings for target dir: {0}".format(target_dir_value))

    job_id = project.AddRenderJob()
    if not job_id:
        raise RuntimeError("Resolve returned no render job id; preset or deliver state may be invalid")
    return job_id


def generate_plan(ev):
    source_asset = asset_path()
    if not source_asset:
        status("Please choose a source asset first.")
        return

    try:
        payload = build_basic_plan(source_asset, selected_device_family(), selected_platform())
        set_plan_output(payload)
        if items()[IMPORT_ID].Checked:
            import_media_to_bin(source_asset, bin_name())
            status("Plan generated and media imported into the target bin.")
        else:
            status("Workflow plan generated.")
    except Exception as exc:
        status("Plan generation failed: {0}".format(exc))


def import_media(ev):
    source_asset = asset_path()
    if not source_asset:
        status("Please choose a source asset first.")
        return

    try:
        import_media_to_bin(source_asset, bin_name())
        status("Media imported into the target bin.")
    except Exception as exc:
        status("Media import failed: {0}".format(exc))


def create_timeline(ev):
    try:
        timeline = create_timeline_from_bin(bin_name(), timeline_name())
        if not timeline:
            status("Timeline creation returned no timeline object.")
            return
        status("Timeline created: {0}".format(timeline_name()))
    except Exception as exc:
        status("Timeline creation failed: {0}".format(exc))


def queue_render(ev):
    try:
        job_id = queue_render_job(render_preset(), render_dir(), render_name())
        if not job_id:
            status("Failed to add render job.")
            return
        status("Render job queued: {0}".format(job_id))
    except Exception as exc:
        status("Queue render failed: {0}".format(exc))


def on_close(ev):
    dispatcher.ExitLoop()


ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

existing = ui.FindWindow(WINDOW_ID)
if existing:
    existing.Show()
    existing.Raise()
    exit()


win = dispatcher.AddWindow(
    {
        "ID": WINDOW_ID,
        "Geometry": [100, 100, 900, 640],
        "WindowTitle": "HDR Creator Workflow",
    },
    ui.VGroup(
        {"Spacing": 8},
        [
            ui.Label({"Text": "HDR Creator Workflow - Safe Shell", "Weight": 0}),
            ui.Label({"Text": "Stage 1 restore: browse asset, generate plan, import to bin", "Weight": 0}),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.LineEdit({"ID": ASSET_ID, "Text": "", "Weight": 0.82}),
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
                    ui.CheckBox({"ID": IMPORT_ID, "Text": "Import to bin after planning", "Weight": 0.34}),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Label({"Text": "Target Bin", "Weight": 0}),
                    ui.LineEdit({"ID": BIN_ID, "Text": "HDR Creator Inbox", "Weight": 0.28}),
                    ui.Label({"Text": "Timeline", "Weight": 0}),
                    ui.LineEdit({"ID": TIMELINE_ID, "Text": "HDR Creator Timeline", "Weight": 0.28}),
                    ui.HGap(0, 0.18),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Label({"Text": "Render Preset", "Weight": 0}),
                    ui.LineEdit({"ID": RENDER_PRESET_ID, "Text": "H.265 Master", "Weight": 0.2}),
                    ui.Label({"Text": "Output Folder", "Weight": 0}),
                    ui.LineEdit({"ID": RENDER_DIR_ID, "Text": os.path.join(os.path.expanduser("~"), "Videos", "HDR Creator Exports"), "Weight": 0.35}),
                    ui.LineEdit({"ID": RENDER_NAME_ID, "Text": "hdr_creator_publish_hdr", "Weight": 0.2}),
                ],
            ),
            ui.HGroup(
                {"Weight": 0},
                [
                    ui.Button({"ID": GENERATE_ID, "Text": "Generate Plan", "Weight": 0.22}),
                    ui.Button({"ID": IMPORT_BUTTON_ID, "Text": "Import To Bin", "Weight": 0.18}),
                    ui.Button({"ID": CREATE_TIMELINE_ID, "Text": "Create Timeline", "Weight": 0.18}),
                    ui.Button({"ID": QUEUE_RENDER_ID, "Text": "Queue Render Job", "Weight": 0.2}),
                    ui.HGap(0, 0.22),
                ],
            ),
            ui.Label({"Text": "Workflow Plan", "Weight": 0}),
            ui.TextEdit(
                {
                    "ID": PLAN_ID,
                    "ReadOnly": True,
                    "AcceptRichText": False,
                    "LineWrapMode": "NoWrap",
                    "Font": ui.Font({"Family": "Consolas", "PixelSize": 11}),
                    "Weight": 1,
                }
            ),
            ui.LineEdit({"ID": STATUS_ID, "ReadOnly": True, "Text": "Ready.", "Weight": 0}),
        ],
    ),
)

device_combo = win.Find(DEVICE_ID)
device_combo.AddItem("auto")
device_combo.AddItem("pocket")
device_combo.AddItem("iphone")
device_combo.AddItem("generic-hdr")
device_combo.CurrentIndex = 0

platform_combo = win.Find(PLATFORM_ID)
platform_combo.AddItem("douyin")
platform_combo.CurrentIndex = 0

win.On[WINDOW_ID].Close = on_close
win.On[BROWSE_ID].Clicked = browse_asset
win.On[GENERATE_ID].Clicked = generate_plan
win.On[IMPORT_BUTTON_ID].Clicked = import_media
win.On[CREATE_TIMELINE_ID].Clicked = create_timeline
win.On[QUEUE_RENDER_ID].Clicked = queue_render

win.Show()
dispatcher.RunLoop()
