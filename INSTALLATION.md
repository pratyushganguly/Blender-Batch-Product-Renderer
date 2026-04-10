# Installation & Setup Guide

## Prerequisites

### 1. Install Blender
- Download from [blender.org](https://www.blender.org/download/)
- Minimum version: Blender 3.0 (tested with 3.x and 4.x)
- Install to default location for easier command-line access

**Default installation paths:**
- Windows: `C:\Program Files\Blender Foundation\Blender 4.0\`
- macOS: `/Applications/Blender.app/Contents/MacOS/`
- Linux: `/usr/bin/blender` (if installed via package manager)

### 2. Verify Blender Command Line Access

Open your terminal/command prompt and test:

**Windows (CMD):**
```bat
"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" --version
```

**macOS:**
```bash
/Applications/Blender.app/Contents/MacOS/Blender --version
```

**Linux:**
```bash
blender --version
```

You should see Blender version info printed. If you get "command not found", double-check your installation path.

---

## Setup Steps

### Step 1: Download This Repository

```bash
git clone https://github.com/YOUR_USERNAME/blender-batch-render.git
cd blender-batch-render
```

Or download as ZIP and extract.

### Step 2: Prepare Your Blender Scene

1. Open your product `.blend` file
2. Organize collections in the Outliner:
   - Create collections for each variant type (backgrounds, shades, lights, etc.)
   - Name them clearly with prefixes: `BG_`, `LGT_`, `SHADE_`, etc.
   - Ensure all collections are **included** in your active View Layer

**Example hierarchy:**
```
Scene Collection
├── ALWAYS_ON
├── BG_LivingRoom
├── BG_StudioWhite
├── LGT_Softbox
├── LGT_Studio
├── SHADE_Black
├── SHADE_White
└── SHADE_Bamboo
```

3. Create and name your cameras as objects (not collections):
   - `CAM_Main`
   - `CAM_Closeup`
   - etc.

4. Save the `.blend` file

### Step 3: Configure the Script

1. Copy `batch_render.py` to the same folder as your `.blend` file
2. Open `batch_render.py` in any text editor (VS Code, Notepad++, Sublime, etc.)
3. Edit only the **CONFIG section** at the top:

```python
# Update camera names
CAMERAS = [
    "CAM_Main",        # ← Your actual camera object name
    "CAM_Closeup",     # ← Your actual camera object name
]

# Update collection groups
SWITCH_GROUPS = {
    "BG": [
        "BG_LivingRoom",      # ← Your actual collection names
        "BG_StudioWhite",
    ],
    "SHADE": [
        "SHADE_Black",
        "SHADE_White",
    ],
}

# Update filename pattern
FILENAME_PATTERN = "{SHADE}__{BG}__{camera}"
```

4. Save the file

### Step 4: Run Your First Batch Render

Navigate to your project folder in terminal/CMD:

```bash
cd /path/to/your/project
```

Then run Blender with the script:

**Windows (CMD):**
```bat
"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b "your_scene.blend" --python "batch_render.py"
```

**Windows (PowerShell):**
```powershell
& "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" -b "your_scene.blend" --python "batch_render.py"
```

**macOS:**
```bash
/Applications/Blender.app/Contents/MacOS/Blender -b "your_scene.blend" --python "batch_render.py"
```

**Linux:**
```bash
blender -b "your_scene.blend" --python "batch_render.py"
```

### Step 5: Check Output

Images will be saved in `RENDERS_BATCH/` folder next to your `.blend` file.

Example output:
```
RENDERS_BATCH/
├── SHADE_Black__BG_LivingRoom__CAM_Main.png
├── SHADE_Black__BG_LivingRoom__CAM_Closeup.png
├── SHADE_White__BG_StudioWhite__CAM_Main.png
└── ...
```

---

## Dependencies

**None!** 

This script uses only Python standard library (`os`, `itertools`) and Blender's built-in `bpy` module. No `pip install` needed.

---

## Optional: Add Blender to PATH

To run `blender` from anywhere without typing the full path:

### Windows
1. Search "Environment Variables" in Start menu
2. Edit "Path" variable
3. Add: `C:\Program Files\Blender Foundation\Blender 4.0\`
4. Restart terminal

### macOS
Add to `~/.zshrc` or `~/.bash_profile`:
```bash
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"
```

### Linux
Usually already in PATH if installed via package manager.

---

## Troubleshooting Installation

### "blender: command not found"
- Use full path to Blender executable
- Or add Blender to PATH (see above)

### "ModuleNotFoundError: No module named 'bpy'"
- Don't run with system Python (`python batch_render.py`) ❌
- Must run with Blender: `blender -b file.blend --python batch_render.py` ✅

### "Permission denied"
- On Linux/macOS, ensure script has execute permissions:
  ```bash
  chmod +x batch_render.py
  ```

### PowerShell: "running scripts is disabled"
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Or use CMD instead of PowerShell

---

## Next Steps

- Read [README.md](README.md) for detailed configuration options
- Try rendering with low samples first (32-64) to test faster
- Once confirmed working, increase samples for final quality

---

**Need help?** Open an issue on GitHub or check the [FAQ in README.md](README.md#-faq)
