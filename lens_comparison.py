"""
Edmund Optics miniature-lens comparison — expanded bubble scatter plot only

Ideal thin-lens Gaussian-beam screening model.
This script generates only the bubble scatter plot and its PNG file.
Verify lens specifications and use real lens prescriptions for final design.
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# 1) USER SETTINGS
# =============================================================================
WAVELENGTH_M = 633e-9
FIBER_MFD_UM = 4.45
MAX_LENS_DIAMETER_MM = 2.0

LENS_POS_MIN_MM = 0.10
LENS_POS_MAX_MM = 4.00
LENS_POS_STEP_MM = 0.005

# Distance downstream of the lens at which beam diameter is evaluated.
TARGET_DISTANCE_FOR_SCATTER_MM = 5.0
TARGET_BEAM_DIAMETER_UM = 180.0  # Set to None to hide target line

# Scatter plot appearance
BUBBLE_SIZE = 250                 # Same size for every lens
COLORMAP = "jet"
LABEL_FONT_SIZE = 9.5

# =============================================================================
# 2) LENS DATABASE
# =============================================================================
lenses = [
    # 1 mm diameter PCX examples
    {"Stock": "45-588", "Name": "PCX 0.60 mm EFL, uncoated", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 0.60, "ClearAperture_mm": 0.50,
     "Coating": "Uncoated",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-06mm-fl-uncoated-plano-convex-lens/6076/"},
    {"Stock": "65-273", "Name": "PCX 0.60 mm EFL, VIS 0 deg", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 0.60, "ClearAperture_mm": 0.50,
     "Coating": "VIS 0 deg",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-06mm-fl-vis-0deg-coated-plano-convex-lens/19915/"},
    {"Stock": "35-694", "Name": "PCX 0.60 mm EFL, VIS-EXT", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 0.60, "ClearAperture_mm": 0.50,
     "Coating": "VIS-EXT",
     "URL": "https://www.edmundoptics.ca/p/10mm-dia-x-06mm-fl-vis-ext-coated-plano-convex-lens/36042/"},

    {"Stock": "45-589", "Name": "PCX 1.00 mm EFL, uncoated", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 1.00, "ClearAperture_mm": 0.50,
     "Coating": "Uncoated",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-10mm-fl-uncoated-plano-convex-lens/6077/"},
    {"Stock": "65-258", "Name": "PCX 1.00 mm EFL, MgF2", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 1.00, "ClearAperture_mm": 0.50,
     "Coating": "MgF2",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-10mm-fl-mgfsub2sub-coated-plano-convex-lens/19900/"},
    {"Stock": "35-695", "Name": "PCX 1.00 mm EFL, VIS-EXT", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 1.00, "ClearAperture_mm": 0.50,
     "Coating": "VIS-EXT",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-10mm-fl-vis-ext-coated-plano-convex-lens/36043/"},

    {"Stock": "65-252", "Name": "PCX 1.50 mm EFL, uncoated", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 1.50, "ClearAperture_mm": 0.50,
     "Coating": "Uncoated",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-15mm-fl-uncoated-plano-convex-lens/19894/"},
    {"Stock": "65-253", "Name": "PCX 2.00 mm EFL, uncoated", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 2.00, "ClearAperture_mm": 0.50,
     "Coating": "Uncoated",
     "URL": "https://www.edmundoptics.ca/p/10mm-dia-x-20mm-fl-uncoated-plano-convex-lens/19895/"},
    {"Stock": "65-260", "Name": "PCX 2.00 mm EFL, MgF2", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 2.00, "ClearAperture_mm": 0.50,
     "Coating": "MgF2",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-20mm-fl-mgfsub2sub-coated-plano-convex-lens/19902/"},
    {"Stock": "65-276", "Name": "PCX 2.00 mm EFL, VIS 0 deg", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 2.00, "ClearAperture_mm": 0.50,
     "Coating": "VIS 0 deg",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-20mm-fl-vis-0deg-coated-plano-convex-lens/19918/"},
    {"Stock": "35-697", "Name": "PCX 2.00 mm EFL, VIS-EXT", "Type": "PCX",
     "Diameter_mm": 1.0, "EFL_mm": 2.00, "ClearAperture_mm": 0.50,
     "Coating": "VIS-EXT",
     "URL": "https://www.edmundoptics.com/p/10mm-dia-x-20mm-fl-vis-ext-coated-plano-convex-lens/36045/"},

    # 1.5 mm diameter PCX examples
    {"Stock": "43-394", "Name": "PCX 1.00 mm EFL, uncoated", "Type": "PCX",
     "Diameter_mm": 1.5, "EFL_mm": 1.00, "ClearAperture_mm": np.nan,
     "Coating": "Uncoated",
     "URL": "https://www.edmundoptics.com/p/15mm-dia-x-10mm-fl-uncoated-plano-convex-lens/4999/"},
    {"Stock": "43-395", "Name": "PCX 1.50 mm EFL, uncoated", "Type": "PCX",
     "Diameter_mm": 1.5, "EFL_mm": 1.50, "ClearAperture_mm": np.nan,
     "Coating": "Uncoated",
     "URL": "https://www.edmundoptics.com/p/15mm-dia-x-15mm-fl-uncoated-plano-convex-lens/5000/"},
    {"Stock": "65-278", "Name": "PCX 1.50 mm EFL, VIS 0 deg", "Type": "PCX",
     "Diameter_mm": 1.5, "EFL_mm": 1.50, "ClearAperture_mm": np.nan,
     "Coating": "VIS 0 deg",
     "URL": "https://www.edmundoptics.com/p/15mm-dia-x-15mm-fl-vis-0deg-coated-plano-convex-lens/19920/"},

    # 2 mm diameter examples from the earlier candidate list.
    # Verify current datasheets and exact specs before relying on them.
    {"Stock": "48-145", "Name": "Molded aspheric candidate", "Type": "Aspheric",
     "Diameter_mm": 2.0, "EFL_mm": 3.33, "ClearAperture_mm": 1.6,
     "Coating": "BBAR 600-1050 nm",
     "URL": "https://www.edmundoptics.com/p/015-na-500mm-fl-nir-ar-coated-molded-aspheric-lens/8345/"},
    {"Stock": "84-127", "Name": "Achromatic doublet candidate", "Type": "Achromatic doublet",
     "Diameter_mm": 2.0, "EFL_mm": 3.0, "ClearAperture_mm": 1.6,
     "Coating": "VIS-NIR",
     "URL": "https://www.edmundoptics.com/p/2mm-dia-x-3mm-fl-vis-nir-coated-achromatic-lens/27235/"},
    {"Stock": "84-128", "Name": "2 mm dia x 4 mm FL VIS-NIR achromat", "Type": "Achromatic doublet",
     "Diameter_mm": 2.0, "EFL_mm": 4.0, "ClearAperture_mm": 1.6,
     "Coating": "VIS-NIR",
     "URL": "https://www.edmundoptics.com/p/2mm-dia-x-4mm-fl-vis-nir-coated-achromatic-lens/27236/"},
    {"Stock": "65-567", "Name": "2 mm dia x 3 mm FL MgF2 achromatic doublet", "Type": "Achromatic doublet",
     "Diameter_mm": 2.0, "EFL_mm": 3.0, "ClearAperture_mm": 1.6,
     "Coating": "MgF2",
     "URL": "https://www.edmundoptics.com/p/2mm-dia-x-30mm-fl-mgfsub2sub-coated-achromatic-doublet-lens/20109/"},
    {"Stock": "65-568", "Name": "2 mm dia x 4 mm FL MgF2 achromatic doublet", "Type": "Achromatic doublet",
     "Diameter_mm": 2.0, "EFL_mm": 4.0, "ClearAperture_mm": 1.6,
     "Coating": "MgF2",
     "URL": "https://www.edmundoptics.com/p/2mm-dia-x-40mm-fl-mgfsub2sub-coated-achromatic-doublet-lens/20110/"},
]


lens_df = pd.DataFrame(lenses)
lens_df = lens_df[lens_df["Diameter_mm"] <= MAX_LENS_DIAMETER_MM].reset_index(drop=True)

# =============================================================================
# 3) IDEAL THIN-LENS GAUSSIAN-BEAM MODEL
# =============================================================================
lam = WAVELENGTH_M
w0_fiber_m = (FIBER_MFD_UM * 1e-6) / 2
zR_fiber_m = np.pi * w0_fiber_m**2 / lam

lens_positions_mm = np.arange(
    LENS_POS_MIN_MM,
    LENS_POS_MAX_MM + LENS_POS_STEP_MM / 2,
    LENS_POS_STEP_MM
)
lens_positions_m = lens_positions_mm * 1e-3

def calculate_beam(lens_position_m, focal_length_m, distance_after_lens_m):
    """Return output waist diameter, half-angle divergence, and target diameter."""
    q_before = lens_position_m + 1j * zR_fiber_m
    q_after = 1.0 / (1.0 / q_before - 1.0 / focal_length_m)

    zR_out = np.imag(q_after)
    if not np.isfinite(zR_out) or zR_out <= 0:
        return np.nan, np.nan, np.nan

    w0_out_m = np.sqrt(lam * zR_out / np.pi)
    waist_diameter_um = 2 * w0_out_m * 1e6
    half_angle_mrad = (lam / (np.pi * w0_out_m)) * 1e3

    q_target = q_after + distance_after_lens_m
    w_target_m = np.sqrt(
        (lam / np.pi) * (np.abs(q_target)**2) / np.imag(q_target)
    )
    target_diameter_um = 2 * w_target_m * 1e6

    return waist_diameter_um, half_angle_mrad, target_diameter_um

# Confirm requested target distance is represented in the configured distance list.
# The model can calculate any positive target distance directly, so no discrete list is needed.
target_distance_m = TARGET_DISTANCE_FOR_SCATTER_MM * 1e-3
if TARGET_DISTANCE_FOR_SCATTER_MM < 0:
    raise ValueError("Target distance must be zero or positive.")

# Sweep lens position and keep the position with the lowest modeled divergence.
results = []
for _, lens in lens_df.iterrows():
    f_m = float(lens["EFL_mm"]) * 1e-3
    waist_values = []
    divergence_values = []
    target_values = []

    for pos_m in lens_positions_m:
        waist_d, divergence, target_d = calculate_beam(
            pos_m, f_m, target_distance_m
        )
        waist_values.append(waist_d)
        divergence_values.append(divergence)
        target_values.append(target_d)

    divergence_values = np.asarray(divergence_values, dtype=float)
    valid = np.isfinite(divergence_values)
    if not np.any(valid):
        continue

    valid_indices = np.where(valid)[0]
    best_idx = valid_indices[np.argmin(divergence_values[valid])]
    results.append({
        "Stock": str(lens["Stock"]),
        "Physical_diameter_mm": float(lens["Diameter_mm"]),
        "EFL_mm": float(lens["EFL_mm"]),
        "Best_lens_position_mm": float(lens_positions_mm[best_idx]),
        "Minimum_half_angle_divergence_mrad": float(divergence_values[best_idx]),
        "Output_waist_diameter_um": float(waist_values[best_idx]),
        "Target_beam_diameter_um": float(target_values[best_idx]),
    })

summary = pd.DataFrame(results).dropna()
summary.to_csv("edmund_lens_bubble_scatter_data.csv", index=False)

# =============================================================================
# 4) BUBBLE SCATTER PLOT ONLY
# =============================================================================
fig, ax = plt.subplots(figsize=(12, 8))

points = ax.scatter(
    summary["Minimum_half_angle_divergence_mrad"],
    summary["Target_beam_diameter_um"],
    s=BUBBLE_SIZE,
    c=summary["Output_waist_diameter_um"],
    cmap=COLORMAP,
    alpha=0.9,
    edgecolors="black",
    linewidths=0.8,
)

# Label each lens with its stock number.
# For identical/near-identical points, stack labels vertically and connect
# each label back to the true point. Circle coordinates are not changed.
from collections import defaultdict

label_groups = defaultdict(list)
for idx, row in summary.iterrows():
    key = (
        round(row["Minimum_half_angle_divergence_mrad"], 3),
        round(row["Target_beam_diameter_um"], 1),
    )
    label_groups[key].append((idx, row))

for group in label_groups.values():
    # Sort consistently by stock number so label order is reproducible.
    group = sorted(group, key=lambda item: item[1]["Stock"])
    n_group = len(group)

    for rank, (_, row) in enumerate(group):
        # Spread labels around the point for multi-lens clusters.
        if n_group == 1:
            offset = (7, 5)
            arrow = None
        else:
            # Vertically separate labels; slight horizontal offset alternates
            # to make the connector lines easier to distinguish.
            vertical_offset = (rank - (n_group - 1) / 2) * 15
            horizontal_offset = 12 if rank % 2 == 0 else 22
            offset = (horizontal_offset, vertical_offset)
            arrow = dict(
                arrowstyle="-",
                color="0.4",
                lw=0.7,
                shrinkA=2,
                shrinkB=4,
                connectionstyle="arc3,rad=0.0",
            )

        ax.annotate(
            row["Stock"],
            xy=(
                row["Minimum_half_angle_divergence_mrad"],
                row["Target_beam_diameter_um"],
            ),
            xytext=offset,
            textcoords="offset points",
            fontsize=LABEL_FONT_SIZE,
            ha="left",
            va="center",
            arrowprops=arrow,
            bbox=dict(
                boxstyle="round,pad=0.12",
                facecolor="white",
                edgecolor="none",
                alpha=0.75,
            ),
            annotation_clip=False,
        )

colorbar = fig.colorbar(points, ax=ax, pad=0.02)
colorbar.set_label("Output waist diameter (µm)")

if TARGET_BEAM_DIAMETER_UM is not None:
    ax.axhline(
        TARGET_BEAM_DIAMETER_UM,
        color="black",
        linestyle="--",
        linewidth=1.4,
        label=f"Target beam diameter = {TARGET_BEAM_DIAMETER_UM:g} µm",
    )
    ax.legend(loc="best", fontsize=9)

ax.set_xlabel("Minimum half-angle divergence (mrad; lower is better)")
ax.set_ylabel(
    f"Beam diameter {TARGET_DISTANCE_FOR_SCATTER_MM:g} mm after lens (µm)"
)
ax.set_title("Edmund Optics Lens Comparison — Bubble Scatter Plot")
ax.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig("edmund_lens_bubble_scatter.png", dpi=300, bbox_inches="tight")
plt.show()

print("\n=== Lens data plotted ===")
print(summary.sort_values("Minimum_half_angle_divergence_mrad").to_string(
    index=False, float_format=lambda x: f"{x:.3f}"
))
print("\nSaved:")
print("  edmund_lens_bubble_scatter.png")
print("  edmund_lens_bubble_scatter_data.csv")
print("\nModel caution: ideal thin-lens Gaussian estimate only; not prescription ray tracing.")
