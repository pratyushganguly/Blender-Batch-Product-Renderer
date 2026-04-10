"""
Blender Batch Product Renderer
===============================
Automate rendering multiple product variants with different cameras, 
backgrounds, lighting setups, and materials.

GitHub: [Add your repo URL here]
License: MIT

INSTRUCTIONS:
1. Organize your scene into Collections (one for each variant)
2. Edit only the CONFIG section below
3. Run from command line: blender -b scene.blend --python batch_render.py
4. Find renders in RENDERS_BATCH folder (or your custom OUTPUT_DIR)

For detailed documentation, see README.md
"""

import bpy
import os
import itertools


# ============================================================
# CONFIG SECTION
# Edit this section to match your scene setup
# ============================================================

# -----------------------------
# 1. OUTPUT SETTINGS
# -----------------------------

# Where to save rendered images
# "//" means "next to the .blend file" (recommended)
OUTPUT_DIR = bpy.path.abspath("//RENDERS_BATCH")

# Force specific output format (recommended for consistency)
FORCE_FORMAT = True
FILE_FORMAT = "PNG"      # Options: "PNG", "JPEG", "OPEN_EXR"
COLOR_MODE  = "RGB"      # Options: "RGB" (opaque), "RGBA" (transparent)
USE_FILE_EXTENSION = True  # Auto-add .png, .jpg, etc. to filenames


# -----------------------------
# 2. VIEW LAYER
# -----------------------------

# Which View Layer to use for rendering
# Set to None to use the currently active View Layer
# Or specify exact name: "ViewLayer" or "RenderLayer_Products"
VIEW_LAYER_NAME = None


# -----------------------------
# 3. CAMERAS
# -----------------------------

# List of camera OBJECT names to render with
# Must match object names in Outliner (not collection names)
# The script will render once with each camera for each combination
CAMERAS = [
    "CAM_Main",
    # "CAM_Closeup",
    # "CAM_45deg",
]


# -----------------------------
# 4. ALWAYS-ON COLLECTIONS
# -----------------------------

# Collections that should ALWAYS be visible in every render
# Examples: floor, props, helper objects
# Use exact collection names from Outliner
ALWAYS_INCLUDE_COLLECTIONS = [
    "ALWAYS_ON",
]


# -----------------------------
# 5. SWITCH GROUPS
# -----------------------------

# Each group represents "choose exactly one collection per render"
# Format: "GroupName": ["Collection1", "Collection2", ...]
#
# How to use:
# - Add a group for each "variant dimension" (backgrounds, lights, shades, etc.)
# - List all collection names for that dimension
# - Script will render all combinations (or use RENDER_PLAN below)
#
# Example: 2 backgrounds × 3 shades = 6 combinations (× cameras)

SWITCH_GROUPS = {
    # Backgrounds: choose one per render
    "BG": [
        "BG_LivingRoom",
        "BG_StudioWhite",
    ],
    
    # Lighting setups: choose one per render
    "LGT": [
        "LGT_Softbox",
        "LGT_Studio",
    ],
    
    # Product shades/variants: choose one per render
    "SHADE": [
        "SHADE_Black",
        "SHADE_White",
        "SHADE_Bamboo",
    ],
    
    # Add more groups as needed:
    # "BASE": ["BASE_Wood", "BASE_Metal"],
    # "FINISH": ["FINISH_Matte", "FINISH_Glossy"],
}

# HOW TO REMOVE A GROUP:
# Just delete or comment out the entire group.
# Example: if you don't have multiple lighting setups, delete the "LGT" group.
# Also remove the token from FILENAME_PATTERN (see below).


# -----------------------------
# 6. COMBINATION CONTROL
# -----------------------------

# Option A: Render ALL combinations (cartesian product)
# Example: 2 BG × 2 LGT × 3 SHADE = 12 combinations
RENDER_ALL_COMBINATIONS = True

# Option B: Render ONLY specific combinations
# Set RENDER_ALL_COMBINATIONS = False and define combinations below
# Each dict must include one choice from each group in SWITCH_GROUPS
RENDER_PLAN = [
    # Example:
    # {"BG": "BG_LivingRoom", "LGT": "LGT_Softbox", "SHADE": "SHADE_Black"},
    # {"BG": "BG_StudioWhite", "LGT": "LGT_Studio", "SHADE": "SHADE_White"},
]


# -----------------------------
# 7. EXCLUSION RULES
# -----------------------------

# Skip specific combinations that don't make sense
# Example: don't render bamboo shade on studio white background
EXCLUDE_RULES = [
    # {"SHADE": "SHADE_Bamboo", "BG": "BG_StudioWhite"},
]


# -----------------------------
# 8. FILENAME PATTERN
# -----------------------------

# How to name output files
# Available tokens: {camera} and any key from SWITCH_GROUPS
# Examples:
#   "{SHADE}__{BG}__{camera}"  →  SHADE_Black__BG_LivingRoom__CAM_Main.png
#   "{camera}_{SHADE}"          →  CAM_Main_SHADE_Black.png
#   "Product_{SHADE}_{BG}"      →  Product_SHADE_Black_BG_LivingRoom.png
#
# IMPORTANT: If you remove a group from SWITCH_GROUPS, also remove its token here
# or the script will fail (e.g., if you delete "BASE" group, remove {BASE} from pattern)

FILENAME_PATTERN = "{SHADE}__{BG}__{LGT}__{camera}"


# ============================================================
# SCRIPT INTERNALS
# Do not edit below unless you know what you're doing
# ============================================================

def ensure_output_settings(scene):
    """Apply output format settings if FORCE_FORMAT is enabled."""
    if not FORCE_FORMAT:
        return
    img = scene.render.image_settings
    img.file_format = FILE_FORMAT
    img.color_mode = COLOR_MODE
    scene.render.use_file_extension = USE_FILE_EXTENSION


def find_layer_collection(layer_coll, collection_name: str):
    """
    Find LayerCollection by its underlying Collection name (depth-first search).
    
    LayerCollection is the View Layer-specific wrapper around Collection.
    This is what controls "Exclude from View Layer" visibility.
    """
    if layer_coll.collection.name == collection_name:
        return layer_coll
    for child in layer_coll.children:
        found = find_layer_collection(child, collection_name)
        if found:
            return found
    return None


def map_layer_collections(view_layer, collection_names):
    """Map collection names to their LayerCollections in this view layer."""
    root = view_layer.layer_collection
    mapping = {}
    for name in collection_names:
        mapping[name] = find_layer_collection(root, name)
    return mapping


def set_exclude(lc, state: bool):
    """Safely set exclude flag on a LayerCollection (handles None)."""
    if lc is None:
        return
    lc.exclude = state


def combination_is_excluded(choice_dict):
    """Check if a combination matches any EXCLUDE_RULE."""
    for rule in EXCLUDE_RULES:
        match = True
        for key, value in rule.items():
            if choice_dict.get(key) != value:
                match = False
                break
        if match:
            return True
    return False


def build_combinations():
    """
    Generate list of combinations to render.
    
    If RENDER_ALL_COMBINATIONS is True, generates cartesian product.
    Otherwise, returns RENDER_PLAN as-is.
    """
    if not RENDER_ALL_COMBINATIONS:
        return RENDER_PLAN

    keys = list(SWITCH_GROUPS.keys())
    value_lists = [SWITCH_GROUPS[k] for k in keys]

    combos = []
    for values in itertools.product(*value_lists):
        combo_dict = dict(zip(keys, values))
        combos.append(combo_dict)
    return combos


def validate_config():
    """Check for common configuration errors and warn user."""
    errors = []
    
    # Check for empty groups
    for key, collections in SWITCH_GROUPS.items():
        if not collections:
            errors.append(f"SWITCH_GROUPS['{key}'] is empty. Remove the group or add collections.")
    
    # Check cameras exist
    if not CAMERAS:
        errors.append("CAMERAS list is empty. Add at least one camera object name.")
    
    if errors:
        print("\n" + "="*60)
        print("CONFIGURATION ERRORS:")
        for err in errors:
            print(f"  ❌ {err}")
        print("="*60 + "\n")
        raise RuntimeError("Fix configuration errors before running. See above.")


def main():
    """Main batch rendering loop."""
    
    # Validate configuration first
    validate_config()
    
    scene = bpy.context.scene

    # Select view layer
    if VIEW_LAYER_NAME:
        view_layer = scene.view_layers.get(VIEW_LAYER_NAME)
        if view_layer is None:
            raise RuntimeError(
                f"View Layer '{VIEW_LAYER_NAME}' not found. "
                f"Available: {[vl.name for vl in scene.view_layers]}"
            )
    else:
        view_layer = bpy.context.view_layer

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

    # Apply render settings
    ensure_output_settings(scene)

    # Collect all collection names mentioned in config
    all_switch_collections = sorted({
        coll for group in SWITCH_GROUPS.values() for coll in group
    })
    all_needed_collections = sorted(
        set(all_switch_collections + ALWAYS_INCLUDE_COLLECTIONS)
    )

    # Map collection names to LayerCollections
    lc_map = map_layer_collections(view_layer, all_needed_collections)

    # Warn about missing collections
    missing = [name for name in all_needed_collections if lc_map.get(name) is None]
    if missing:
        print("\n⚠️  WARNING: Collections not found in view layer:")
        for name in missing:
            print(f"     - {name}")
        print("   Check spelling and View Layer includes.\n")

    # Prepare cameras
    camera_objs = []
    for cam_name in CAMERAS:
        cam_obj = bpy.data.objects.get(cam_name)
        if cam_obj is None:
            print(f"⚠️  WARNING: Camera not found: {cam_name}")
        else:
            camera_objs.append(cam_obj)

    if not camera_objs:
        raise RuntimeError(
            "No valid cameras found. Check CAMERAS list matches object names in Outliner."
        )

    # Fix frame (safety for scenes with animations)
    scene.frame_set(scene.frame_start)

    # Build render combinations
    combinations = build_combinations()
    total_renders = len(combinations) * len(camera_objs)
    
    print(f"\n{'='*60}")
    print(f"Batch render starting...")
    print(f"  Cameras: {len(camera_objs)}")
    print(f"  Combinations: {len(combinations)}")
    print(f"  Total renders: {total_renders}")
    print(f"{'='*60}\n")

    render_count = 0

    # Main render loop: camera → combination → render
    for cam in camera_objs:
        scene.camera = cam

        for choice in combinations:
            # Skip if excluded
            if combination_is_excluded(choice):
                print(f"⏭️  Skipping excluded: {choice}")
                continue

            # 1) Exclude ALL switch collections (start clean)
            for coll_name in all_switch_collections:
                set_exclude(lc_map.get(coll_name), True)

            # 2) Include ALWAYS collections
            for coll_name in ALWAYS_INCLUDE_COLLECTIONS:
                set_exclude(lc_map.get(coll_name), False)

            # 3) Include chosen collections for this combination
            for group_key, coll_name in choice.items():
                set_exclude(lc_map.get(coll_name), False)

            # 4) Build filename
            safe_choice = dict(choice)
            safe_choice["camera"] = cam.name
            
            try:
                basename = FILENAME_PATTERN.format(**safe_choice)
            except KeyError as e:
                print(f"\n❌ ERROR: Filename pattern token {e} not found in SWITCH_GROUPS or 'camera'")
                print(f"   FILENAME_PATTERN: {FILENAME_PATTERN}")
                print(f"   Available tokens: {list(safe_choice.keys())}")
                raise

            filepath = os.path.join(OUTPUT_DIR, basename)
            scene.render.filepath = filepath

            # 5) Render and save
            render_count += 1
            print(f"[{render_count}/{total_renders}] Rendering: {basename}")
            bpy.ops.render.render(write_still=True)

    print(f"\n{'='*60}")
    print(f"✅ Batch render complete!")
    print(f"   {render_count} images saved to: {OUTPUT_DIR}")
    print(f"{'='*60}\n")


# Run main when script is executed
if __name__ == "__main__":
    main()
