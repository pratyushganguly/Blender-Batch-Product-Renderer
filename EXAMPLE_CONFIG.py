"""
EXAMPLE CONFIGURATIONS
======================
Copy one of these into your batch_render.py CONFIG section and customize.
"""

# ============================================================
# EXAMPLE 1: Simple product with multiple shades
# ============================================================

CAMERAS = ["CAM_Main"]

SWITCH_GROUPS = {
    "SHADE": ["SHADE_Black", "SHADE_White", "SHADE_Grey"],
}

FILENAME_PATTERN = "{SHADE}__{camera}"

# Result: 3 renders
# SHADE_Black__CAM_Main.png
# SHADE_White__CAM_Main.png
# SHADE_Grey__CAM_Main.png


# ============================================================
# EXAMPLE 2: Multiple cameras + multiple shades
# ============================================================

CAMERAS = ["CAM_Hero", "CAM_Detail", "CAM_Context"]

SWITCH_GROUPS = {
    "SHADE": ["SHADE_Linen", "SHADE_Silk", "SHADE_Cotton"],
}

FILENAME_PATTERN = "{camera}_{SHADE}"

# Result: 9 renders (3 cameras × 3 shades)
# CAM_Hero_SHADE_Linen.png
# CAM_Hero_SHADE_Silk.png
# ...


# ============================================================
# EXAMPLE 3: Full ecommerce catalogue (backgrounds + shades + lights)
# ============================================================

CAMERAS = ["CAM_Main", "CAM_Closeup"]

ALWAYS_INCLUDE_COLLECTIONS = ["Floor", "Props"]

SWITCH_GROUPS = {
    "BG":    ["BG_LivingRoom", "BG_Bedroom", "BG_StudioWhite"],
    "LGT":   ["LGT_Softbox", "LGT_Dramatic"],
    "SHADE": ["SHADE_A", "SHADE_B", "SHADE_C", "SHADE_D"],
}

FILENAME_PATTERN = "{SHADE}__{BG}__{LGT}__{camera}"

# Result: 48 renders (2 cam × 3 BG × 2 LGT × 4 SHADE)


# ============================================================
# EXAMPLE 4: Excluding specific combinations
# ============================================================

CAMERAS = ["CAM_Main"]

SWITCH_GROUPS = {
    "BG":    ["BG_Modern", "BG_Traditional"],
    "SHADE": ["SHADE_Minimalist", "SHADE_Ornate"],
}

# Don't render ornate shade in modern background
EXCLUDE_RULES = [
    {"BG": "BG_Modern", "SHADE": "SHADE_Ornate"},
]

FILENAME_PATTERN = "{SHADE}__{BG}"

# Result: 3 renders (4 combinations - 1 excluded)
# SHADE_Minimalist__BG_Modern.png
# SHADE_Minimalist__BG_Traditional.png
# SHADE_Ornate__BG_Traditional.png


# ============================================================
# EXAMPLE 5: Manual render plan (not all combinations)
# ============================================================

CAMERAS = ["CAM_Main"]

SWITCH_GROUPS = {
    "BG":    ["BG_A", "BG_B", "BG_C"],
    "SHADE": ["SHADE_X", "SHADE_Y", "SHADE_Z"],
}

RENDER_ALL_COMBINATIONS = False

RENDER_PLAN = [
    {"BG": "BG_A", "SHADE": "SHADE_X"},
    {"BG": "BG_B", "SHADE": "SHADE_Y"},
    {"BG": "BG_C", "SHADE": "SHADE_Z"},
]

FILENAME_PATTERN = "{SHADE}_in_{BG}"

# Result: 3 renders (only the specified combinations)


# ============================================================
# EXAMPLE 6: Furniture with base + cushion variants
# ============================================================

CAMERAS = ["CAM_Front", "CAM_Angle45", "CAM_Top"]

SWITCH_GROUPS = {
    "BASE":    ["BASE_Walnut", "BASE_Oak", "BASE_Black"],
    "CUSHION": ["CUSHION_Leather", "CUSHION_Fabric"],
    "BG":      ["BG_StudioWhite"],
}

FILENAME_PATTERN = "Sofa_{BASE}_{CUSHION}_{camera}"

# Result: 18 renders (3 cam × 3 base × 2 cushion × 1 BG)


# ============================================================
# EXAMPLE 7: Transparent renders for compositing
# ============================================================

FILE_FORMAT = "PNG"
COLOR_MODE = "RGBA"  # Transparent background

CAMERAS = ["CAM_Main"]

SWITCH_GROUPS = {
    "SHADE": ["SHADE_Red", "SHADE_Blue", "SHADE_Green"],
}

FILENAME_PATTERN = "{SHADE}_transparent"

# Result: 3 PNG files with alpha channel for later compositing
