# Blender Batch Product Renderer

**Automate rendering multiple product variants with different cameras, backgrounds, lighting, and materials — without clicking "Render" hundreds of times.**

Perfect for ecommerce product photography, catalogue generation, and design iteration workflows where you need the same scene with swappable elements.

***

## 🎯 What This Does

Renders **all combinations** (or specific combinations) of:
- 📷 Multiple cameras (hero shot, close-up, 45° angle, etc.)
- 🏠 Multiple backgrounds (living room, studio white, bedroom, etc.)
- 💡 Multiple lighting setups (soft, dramatic, studio, etc.)
- 🎨 Multiple product variants (shades, colors, materials, finishes, etc.)

**Example:** 2 cameras × 3 backgrounds × 4 product shades = **24 images** rendered automatically with one command.

All images saved with clean, consistent filenames for easy upload to Shopify, WooCommerce, or any ecommerce platform.

***

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Blender 3.0+ installed ([download here](https://www.blender.org/download/))
- One `.blend` file with your scene set up
- Basic familiarity with Blender's Outliner and Collections

### Step 1: Organize Your Scene

In Blender's **Outliner**, organize elements into **Collections**:

```
Scene Collection
├── ALWAYS_ON          (props that are always visible)
├── CAM_Main           (camera object)
├── CAM_Closeup        (camera object)
├── BG_LivingRoom      (background collection)
├── BG_StudioWhite     (background collection)
├── LGT_Softbox        (light rig collection)
├── LGT_Studio         (light rig collection)
├── SHADE_Black        (product variant collection)
├── SHADE_White        (product variant collection)
└── SHADE_Bamboo       (product variant collection)
```

**Naming tip:** Use prefixes like `CAM_`, `BG_`, `LGT_`, `SHADE_` so collections are easy to identify.

### Step 2: Download the Script

1. Download `batch_render.py` from this repository
2. Save it in the same folder as your `.blend` file

### Step 3: Edit the CONFIG Section

Open `batch_render.py` in any text editor and **only edit the CONFIG section** at the top:

```python
# 1) Where to save renders
OUTPUT_DIR = bpy.path.abspath("//RENDERS_BATCH")

# 4) Cameras to render with (object names)
CAMERAS = ["CAM_Main", "CAM_Closeup"]

# 6) SWITCH GROUPS: choose one from each group per render
SWITCH_GROUPS = {
    "BG":    ["BG_LivingRoom", "BG_StudioWhite"],
    "LGT":   ["LGT_Softbox", "LGT_Studio"],
    "SHADE": ["SHADE_Black", "SHADE_White", "SHADE_Bamboo"],
}

# 9) Filename pattern
FILENAME_PATTERN = "{SHADE}__{BG}__{LGT}__{camera}"
```

**What to change:**
- Replace `"CAM_Main"`, `"CAM_Closeup"` with **your actual camera object names**
- Replace `"BG_LivingRoom"`, etc. with **your actual collection names** (exact spelling, case-sensitive)
- Replace `"SHADE_Black"`, etc. with **your product variant collection names**

### Step 4: Run the Script

#### Windows (Command Prompt):
```bat
"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b "your_scene.blend" --python "batch_render.py"
```

#### Windows (PowerShell):
```powershell
& "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b "your_scene.blend" --python "batch_render.py"
```

#### macOS / Linux:
```bash
blender -b "your_scene.blend" --python "batch_render.py"
```

**That's it!** Images will appear in the `RENDERS_BATCH` folder next to your `.blend` file.

***

## 📖 Detailed Configuration Guide

### Collections That Are Always Visible

If you have props, floor planes, or helper objects that should **always** be in every render:

```python
ALWAYS_INCLUDE_COLLECTIONS = ["ALWAYS_ON", "Floor", "Props"]
```

### Adding More "Switch Groups"

Each group represents "choose exactly one collection from this list per render."

**Example:** You manufacture lamps with different bases AND different shades:

```python
SWITCH_GROUPS = {
    "BASE":  ["BASE_Wood", "BASE_Metal", "BASE_Marble"],
    "SHADE": ["SHADE_Linen", "SHADE_Silk", "SHADE_Paper"],
    "BG":    ["BG_LivingRoom", "BG_Bedroom"],
}
```

This renders **all combinations**: 3 bases × 3 shades × 2 backgrounds = **18 images**.

### Removing a Group You Don't Need

If you don't have multiple backgrounds or lighting setups, **delete the entire line** from `SWITCH_GROUPS`.

Before:
```python
SWITCH_GROUPS = {
    "BG":    ["BG_LivingRoom", "BG_StudioWhite"],
    "SHADE": ["SHADE_Black", "SHADE_White"],
}
```

After (if you only have one background):
```python
SWITCH_GROUPS = {
    "SHADE": ["SHADE_Black", "SHADE_White"],
}
```

**Also update the filename pattern** to remove unused tokens:

```python
FILENAME_PATTERN = "{SHADE}__{camera}"
```

### Excluding Specific Combinations

Sometimes certain combinations don't make sense (e.g., "don't render bamboo shade on studio white background").

```python
EXCLUDE_RULES = [
    {"SHADE": "SHADE_Bamboo", "BG": "BG_StudioWhite"},
]
```

Any combination matching this rule will be skipped.

### Rendering Only Specific Combinations (Not All)

If you want **manual control** instead of all combinations:

```python
RENDER_ALL_COMBINATIONS = False

RENDER_PLAN = [
    {"BG": "BG_LivingRoom", "LGT": "LGT_Softbox", "SHADE": "SHADE_Black"},
    {"BG": "BG_StudioWhite", "LGT": "LGT_Studio", "SHADE": "SHADE_White"},
]
```

Only these 2 combinations will render (× number of cameras).

### Customizing Output Filenames

Use tokens from your `SWITCH_GROUPS` keys + `{camera}`:

```python
FILENAME_PATTERN = "{SHADE}__{BG}__{camera}"
# Result: SHADE_Black__BG_LivingRoom__CAM_Main.png

FILENAME_PATTERN = "{camera}_{SHADE}"
# Result: CAM_Main_SHADE_Black.png

FILENAME_PATTERN = "Product_{SHADE}_{BG}"
# Result: Product_SHADE_Black_BG_LivingRoom.png
```

### Changing Output Format

Default is PNG. To change to JPEG or OpenEXR:

```python
FILE_FORMAT = "JPEG"  # or "OPEN_EXR"
COLOR_MODE  = "RGB"   # or "RGBA" for transparency
```

***

## 🛠️ Troubleshooting

### "Collection not found in view layer"

**Problem:** Warning like `WARNING: Collection not found in view layer: SHADE_Black`

**Solution:**
1. Check spelling and capitalization (it's case-sensitive)
2. Make sure the collection is **included** in your active View Layer (not excluded in Outliner)

### "No valid cameras found"

**Problem:** Script exits with "No valid cameras found."

**Solution:**
1. Check that camera names in `CAMERAS = [...]` match **object names** (not collection names)
2. In Outliner, cameras are objects (camera icon), not collections

### "KeyError: 'BASE'" when rendering

**Problem:** Script crashes with `KeyError: 'BASE'`

**Solution:**
- Your `FILENAME_PATTERN` contains `{BASE}` but you deleted `"BASE"` from `SWITCH_GROUPS`
- Either add `"BASE"` back to `SWITCH_GROUPS` or remove `{BASE}` from the filename pattern

### Script runs but no images appear

**Problem:** Script finishes but `RENDERS_BATCH` folder is empty

**Solution:**
1. Check that `OUTPUT_DIR` path is valid (default `//RENDERS_BATCH` works if script is next to `.blend`)
2. Verify render settings in Blender (resolution, samples, etc.) — low samples = fast test
3. Check Blender console output for errors

### PowerShell: "The term 'blender' is not recognized"

**Solution:** Use the full path to `blender.exe` with the `&` call operator:
```powershell
& "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b ...
```

***

## 💡 Tips & Best Practices

### Start Small, Then Scale
1. Test with 1 camera and 2 variants first
2. Confirm output files look correct
3. Then add more cameras, backgrounds, lights

### Use Low Samples for Testing
Set Cycles samples to 32 or 64 during setup, then increase to 128–512 for final renders.

### Consistent Naming = Easy Sorting
Use prefixes (`CAM_`, `BG_`, `LGT_`, `SHADE_`) so you can quickly find collections in large scenes.

### Check Your View Layer
Make sure all collections are **included** in the View Layer you're using (default is `View Layer`). The script only works with collections that are part of the active View Layer.

### Transparent Backgrounds for Compositing
If you want to composite products over different backgrounds later:
```python
COLOR_MODE = "RGBA"
```
And enable Film → Transparent in Blender render settings.

***

## 📂 Example Project Structure

```
MyProductCatalog/
├── scene.blend               (your Blender file)
├── batch_render.py           (this script)
└── RENDERS_BATCH/            (auto-created by script)
    ├── SHADE_Black__BG_LivingRoom__LGT_Softbox__CAM_Main.png
    ├── SHADE_Black__BG_LivingRoom__LGT_Softbox__CAM_Closeup.png
    ├── SHADE_White__BG_StudioWhite__LGT_Studio__CAM_Main.png
    └── ...
```

***

## 🤝 Contributing

Issues and pull requests welcome! If you find a bug or have a feature request, please open an issue.

***

## 📄 License

MIT License — free to use for personal and commercial projects.

***

## 🙏 Credits

Created for product designers, ecommerce teams, and anyone tired of manual batch rendering.

If this saved you time, consider sharing it with other Blender users!

***

## ❓ FAQ

**Q: Can I use this for animations?**  
A: This script is optimized for still images. For animations, you'd need to modify the render call to use frame ranges.

**Q: Does this work with Eevee?**  
A: Yes! The script uses whatever render engine is active in your `.blend` file.

**Q: Can I render to a network drive?**  
A: Yes, just set `OUTPUT_DIR` to an absolute path like `"Z:\\Renders\\Batch"`

**Q: How do I add more than 4 switch groups?**  
A: Just add more entries to `SWITCH_GROUPS = {...}`. There's no limit.

**Q: My filename pattern doesn't include all groups — is that OK?**  
A: Yes! Only include the tokens you need. Unused groups are fine, but make sure your filenames are unique.

***

**Happy Rendering! 🎨**
