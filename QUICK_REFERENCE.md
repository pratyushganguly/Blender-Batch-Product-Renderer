# Quick Reference Card

## One-Page Cheat Sheet

### Essential Command (copy-paste ready)

**Windows CMD:**
```bat
"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b "scene.blend" --python "batch_render.py"
```

**Windows PowerShell:**
```powershell
& "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b "scene.blend" --python "batch_render.py"
```

**macOS/Linux:**
```bash
blender -b "scene.blend" --python "batch_render.py"
```

---

### Minimal Working Config

```python
OUTPUT_DIR = bpy.path.abspath("//RENDERS_BATCH")
CAMERAS = ["CAM_Main"]
SWITCH_GROUPS = {
    "SHADE": ["SHADE_A", "SHADE_B"],
}
FILENAME_PATTERN = "{SHADE}_{camera}"
```

---

### Common Edits

| Task | What to Change | Example |
|------|----------------|---------|
| Add camera | `CAMERAS` list | `["CAM_Main", "CAM_Detail"]` |
| Add variant group | `SWITCH_GROUPS` dict | `"BG": ["BG_Room", "BG_Studio"]` |
| Change filenames | `FILENAME_PATTERN` | `"{camera}_{SHADE}_{BG}"` |
| Skip a combo | `EXCLUDE_RULES` list | `{"SHADE": "A", "BG": "B"}` |
| Change format | `FILE_FORMAT` | `"JPEG"` or `"OPEN_EXR"` |
| Transparent BG | `COLOR_MODE` | `"RGBA"` |

---

### Collection Naming Tips

✅ **Good:**
- `CAM_Main`, `CAM_Hero`, `CAM_Detail`
- `BG_LivingRoom`, `BG_StudioWhite`
- `SHADE_Black`, `SHADE_White`

❌ **Avoid:**
- Spaces: `Shade Black` (use underscore)
- Special chars: `Shade#1` (use `SHADE_01`)
- Duplicates across groups

---

### Troubleshooting Fast

| Error | Fix |
|-------|-----|
| `Collection not found` | Check spelling in CONFIG vs Outliner (case-sensitive) |
| `No valid cameras` | Camera names = object names, not collection names |
| `KeyError: 'BASE'` | Remove `{BASE}` from `FILENAME_PATTERN` or add back to `SWITCH_GROUPS` |
| No images saved | Check `OUTPUT_DIR` path exists, check Blender console for errors |
| PowerShell won't run | Add `&` before blender path: `& "C:\..."` |

---

### Project Structure

```
MyProject/
├── scene.blend
├── batch_render.py
└── RENDERS_BATCH/          ← Auto-created by script
    ├── SHADE_A__CAM_Main.png
    └── ...
```

---

### Filename Tokens

Available in `FILENAME_PATTERN`:
- `{camera}` — camera object name
- Any key from `SWITCH_GROUPS` — e.g., `{SHADE}`, `{BG}`, `{LGT}`

Example:
```python
FILENAME_PATTERN = "Product_{SHADE}_{BG}_{camera}"
# → Product_SHADE_Black_BG_Room_CAM_Main.png
```

---

### Render All vs. Manual Plan

**All combinations (default):**
```python
RENDER_ALL_COMBINATIONS = True
```

**Specific combinations only:**
```python
RENDER_ALL_COMBINATIONS = False
RENDER_PLAN = [
    {"BG": "BG_A", "SHADE": "SHADE_X"},
    {"BG": "BG_B", "SHADE": "SHADE_Y"},
]
```

---

### Output Math

Total renders = `cameras × combinations`

Example:
- 2 cameras
- 3 backgrounds × 4 shades = 12 combinations
- **Total: 24 renders**

---

### Performance Tips

1. **Test first:** Start with 1 camera, 2 variants, low samples (32)
2. **Final batch:** Increase samples to 128-512 after confirming setup
3. **Overnight:** Run full batch overnight for large catalogues
4. **Resume:** Script doesn't skip existing files (overwrites), so delete output folder to re-render specific items

---

### Links

- Full docs: [README.md](README.md)
- Setup guide: [INSTALLATION.md](INSTALLATION.md)
- Examples: [EXAMPLE_CONFIG.py](EXAMPLE_CONFIG.py)
- Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/blender-batch-render/issues)

---

**Bookmark this page for quick reference!**
