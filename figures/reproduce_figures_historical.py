"""
Alibaba ASI GPU Execution-Duration Prediction
Manuscript Figure Generator

M0 baseline:  blue  #0072B2
M1 augmented: red   #D62728
Neutral:       gray  #73777D

All signed gains = M0 LogMAE - M1 LogMAE.
Positive gains favor M1.

Experiment 1: held-out test.
Experiments 2–3: exploratory selected-validation analyses.

No fitting, prediction, or bootstrap recomputation.
Embedded numerical records are transcribed from the audited
experiment summaries and appendix tables.

Outputs:
    ./figures/F01_control_ablations.{pdf,svg,png}
    ...
    ./figures/F09_model_selection.{pdf,svg,png}  [if report available]
"""

from pathlib import Path
import json
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

BLUE = "#0072B2"
RED = "#D62728"
GRAY = "#73777D"
LIGHT = "#D9DDE2"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "savefig.facecolor": "white",
})

def save(fig, name):
    for ext in ("pdf", "svg", "png"):
        fig.savefig(
            FIG / f"{name}.{ext}",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.12,
        )
    plt.close(fig)
    print("Saved:", name)

def gain_pct(m0, m1):
    return 100 * (m0 - m1) / m0

def zero(ax, vertical=True):
    if vertical:
        ax.axvline(0, color=GRAY, linewidth=0.9)
    else:
        ax.axhline(0, color=GRAY, linewidth=0.9)

# ============================================================
# AUDITED EXPERIMENT 1 DATA
# Source: results-summary.json / Appendix C.
# Values below are rounded for display; separately reported
# percentages are retained where precision matters.
# ============================================================

SEEDS = [20260927, 20260928, 20260929]

EXP1 = {
    "Four-type": {
        "R": [
            (0.829185, 0.738576, 10.927),
            (0.829160, 0.736323, 11.197),
            (0.828601, 0.739617, 10.739),
        ],
        "R+P": [
            (0.767696, 0.722023, 5.949),
            (0.767084, 0.722254, 5.844),
            (0.766950, 0.722099, 5.848),
        ],
        "R+P+A": [
            (0.726195, 0.719324, 0.946168),
            (0.724717, 0.718813, 0.814672),
            (0.727546, 0.717515, 1.378673),
        ],
    },
    "Finite fitted": {
        "R": [
            (0.651313, 0.643147, 1.254),
            (0.651304, 0.643159, 1.251),
            (0.651307, 0.643339, 1.223),
        ],
        "R+P": [
            (0.634900, 0.629229, 0.893),
            (0.634885, 0.629227, 0.891),
            (0.634870, 0.629238, 0.887),
        ],
        "R+P+A": [
            (0.626713, 0.624741, 0.314775),
            (0.628609, 0.624667, 0.626969),
            (0.628681, 0.626730, 0.310363),
        ],
    },
}

EXP1_CI = np.array([
    [-1.155669, 2.558092],
    [-1.323891, 2.402525],
    [-0.755445, 3.014961],
])

# ============================================================
# F1 — COMPLETE CONTROL ABLATIONS
# Grouped dot plot: discrete configurations, not a time series.
# ============================================================

fig, axs = plt.subplots(
    1, 2, figsize=(7.2, 3.0), layout="constrained",
    sharey=True
)

controls = ["R", "R+P", "R+P+A"]
offsets = [-0.13, 0, 0.13]

for ax, (population, comparisons) in zip(axs, EXP1.items()):
    for j, control in enumerate(controls):
        for k, (_, _, pct) in enumerate(comparisons[control]):
            ax.scatter(
                pct, j + offsets[k],
                color=RED,
                marker="o",
                s=31,
                alpha=0.85,
            )

    ax.set_yticks(range(3), controls)
    ax.invert_yaxis()
    zero(ax)
    ax.grid(axis="x", alpha=0.13)
    ax.set_title(population)
    ax.set_xlabel("Relative LogMAE gain (%)")

axs[0].set_ylabel("M0 control features")
fig.suptitle(
    "Experiment 1: incremental value of workload type\n"
    "Held-out test; three fitting seeds per configuration",
    fontsize=10,
)
save(fig, "F01_control_ablations")

# ============================================================
# F2 — RICH-CONTROL HELD-OUT CONFIDENCE INTERVALS
# ============================================================

gains = np.array([
    x[2] for x in EXP1["Four-type"]["R+P+A"]
])

fig, ax = plt.subplots(figsize=(6.6, 2.7), layout="constrained")
y = np.arange(3)

ax.errorbar(
    gains, y,
    xerr=[
        gains - EXP1_CI[:, 0],
        EXP1_CI[:, 1] - gains,
    ],
    fmt="o",
    color=RED,
    capsize=4,
    linewidth=1.3,
    markersize=5,
)

zero(ax)
ax.set_yticks(y, [str(s) for s in SEEDS])
ax.invert_yaxis()
ax.set_xlabel("Relative LogMAE gain (%)")
ax.set_ylabel("Fitting seed")
ax.set_title(
    "Experiment 1: rich-control held-out gains\n"
    "95% paired workload-bootstrap intervals"
)
ax.grid(axis="x", alpha=0.13)

save(fig, "F02_heldout_uncertainty")

# ============================================================
# F3 — DURATION-STRATIFIED HELD-OUT EFFECTS
# Source: exp1_checkpoint_original.md / Appendix C.
# Values are relative LogMAE gains in percent.
# ============================================================

BINS = [
    "<1 h", "1–6 h", "6–24 h", "1–3 d",
    "3–7 d", "7–14 d", "14–28 d", "≥28 d"
]

TAIL = {
    "Four-type": np.array([
        [-7.638, -7.427, -6.885],
        [-1.577, -0.618, -2.427],
        [1.026, 0.915, 1.515],
        [7.803, 7.585, 8.417],
        [16.505, 14.898, 17.614],
        [10.622, 8.709, 11.791],
        [14.134, 12.069, 15.015],
        [8.961, 7.538, 9.929],
    ]),
    "Finite fitted": np.array([
        [-0.140, -2.880, 0.196],
        [0.172, 0.191, 0.465],
        [0.735, 3.311, 0.292],
        [0.527, 2.215, 0.280],
        [0.567, 1.372, 0.345],
        [0.535, 0.764, 0.545],
        [0.683, 0.422, 0.349],
        [0.423, 0.503, 0.505],
    ]),
}

fig, axs = plt.subplots(
    1, 2, figsize=(8, 3.6), layout="constrained",
    sharey=True
)

for ax, (population, values) in zip(axs, TAIL.items()):
    y = np.arange(len(BINS))

    for k in range(3):
        ax.scatter(
            values[:, k],
            y + offsets[k],
            color=RED,
            s=21,
            alpha=0.8,
        )

    zero(ax)
    ax.set_yticks(y, BINS)
    ax.invert_yaxis()
    ax.set_xlabel("Relative LogMAE gain (%)")
    ax.set_title(population)
    ax.grid(axis="x", alpha=0.12)

axs[0].set_ylabel("Observed duration bin")
fig.suptitle(
    "Experiment 1: duration-stratified held-out gains\n"
    "Three fitting seeds; descriptive strata",
    fontsize=10,
)

save(fig, "F03_duration_strata")

# ============================================================
# AUDITED EXPERIMENT 2 DATA
# Source: exp2_phase1_findings_original.md / Appendix D.
# Exploratory selected-validation comparisons.
# ============================================================

EXP2_SEEDS = [20260927, 20261020]

EXP2_EXEC = [2.083576, -4.906626]
EXP2_WORK = [3.664494, -2.754915]

EXP2_SHARED = {
    "Original saved pair": (0.854011, 0.850717),
    "Second saved pair": (0.839569, 0.860921),
}

# ============================================================
# F4 — TWO-PARTITION SENSITIVITY
# Shapes distinguish weighting, not model identity.
# ============================================================

fig, ax = plt.subplots(figsize=(6.8, 2.8), layout="constrained")

y = np.arange(2)

ax.scatter(
    EXP2_EXEC, y - 0.10,
    color=GRAY, marker="o", s=48,
    label="Execution-weighted",
)

ax.scatter(
    EXP2_WORK, y + 0.10,
    color=RED, marker="s", s=42,
    label="Equal-workload",
)

zero(ax)
ax.set_yticks(y, [str(s) for s in EXP2_SEEDS])
ax.invert_yaxis()
ax.set_xlabel("Relative LogMAE gain (%)")
ax.set_ylabel("Split seed")
ax.set_title(
    "Experiment 2: selected-validation sensitivity"
)
ax.legend(frameon=False)
ax.grid(axis="x", alpha=0.13)

save(fig, "F04_two_partition_sensitivity")

# ============================================================
# F5 — SHARED VALIDATION RECORDS
# Same 100,221 records; two independently saved predictor pairs.
# ============================================================

labels = list(EXP2_SHARED)
m0 = [EXP2_SHARED[k][0] for k in labels]
m1 = [EXP2_SHARED[k][1] for k in labels]

fig, ax = plt.subplots(figsize=(7.0, 2.8), layout="constrained")

x = np.arange(2)
width = 0.33

ax.bar(
    x - width / 2, m0,
    width, color=BLUE, label="M0 baseline"
)
ax.bar(
    x + width / 2, m1,
    width, color=RED, label="M1 augmented"
)

ax.set_xticks(x, labels)
ax.set_ylabel("LogMAE (lower is better)")
ax.set_title(
    "Experiment 2: same 100,221 validation executions"
)
ax.legend(frameon=False)
ax.set_ylim(0, 1.0)

for i in range(2):
    delta = m0[i] - m1[i]
    ax.annotate(
        f"Δ={delta:+.6f}",
        (i, max(m0[i], m1[i])),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        fontsize=8,
    )

save(fig, "F05_shared_records")

# ============================================================
# AUDITED EXPERIMENT 3 DATA
# Source: exp3_report_original.json / Appendix E.
# Exploratory selected-validation results.
# ============================================================

EXP3_SEEDS = list(range(20261028, 20261107))

EXP3_EXEC_M0 = np.array([
    0.726590, 0.760963, 0.765733, 0.729070, 0.723052,
    0.801967, 0.815797, 0.697835, 0.699318, 0.680174,
])

EXP3_EXEC_M1 = np.array([
    0.707546, 0.753716, 0.751961, 0.719003, 0.767299,
    0.818130, 0.798671, 0.688280, 0.691157, 0.659762,
])

EXP3_WORK_M0 = np.array([
    0.771419, 0.774018, 0.771629, 0.767121, 0.796039,
    0.802192, 0.772255, 0.764632, 0.766861, 0.770773,
])

EXP3_WORK_M1 = np.array([
    0.753788, 0.744829, 0.745451, 0.734240, 0.815601,
    0.794344, 0.745112, 0.742269, 0.738312, 0.748350,
])

# Preserve reported relative percentages rather than deriving
# them from six-decimal rounded losses.

EXP3_EXEC_GAIN_PCT = np.array([
    2.621041, 0.952380, 1.798561, 1.380831,
    -6.119481, -2.015370, 2.099191, 1.369197,
    1.167035, 3.001094,
])

EXP3_WORK_GAIN_PCT = np.array([
    2.285490, 3.771069, 3.392490, 4.286259,
    -2.457371, 0.978313, 3.514843, 2.924704,
    3.722862, 2.909197,
])

# ============================================================
# F6 — TEN-PARTITION SENSITIVITY
# ============================================================

fig, ax = plt.subplots(figsize=(7.3, 4.2), layout="constrained")

y = np.arange(10)

ax.scatter(
    EXP3_EXEC_GAIN_PCT, y - 0.13,
    color=GRAY, marker="o", s=36,
    label="Execution-weighted",
)

ax.scatter(
    EXP3_WORK_GAIN_PCT, y + 0.13,
    color=RED, marker="s", s=34,
    label="Equal-workload",
)

zero(ax)
ax.set_yticks(y, [str(s) for s in EXP3_SEEDS])
ax.invert_yaxis()
ax.set_xlabel("Relative LogMAE gain (%)")
ax.set_ylabel("Split seed")
ax.set_title(
    "Experiment 3: partition and weighting sensitivity\n"
    "Restricted population; exploratory selected validation"
)
ax.grid(axis="x", alpha=0.13)
ax.legend(frameon=False, loc="lower left")

# Highlight the ranking reversal without implying significance.
ax.axhspan(4.55, 5.45, color=LIGHT, alpha=0.35, zorder=0)
ax.annotate(
    "Weighting reversal",
    xy=(-2.015370, 5 - 0.13),
    xytext=(-6.7, 3.8),
    fontsize=8,
    arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8),
)

save(fig, "F06_ten_partition_sensitivity")

# ============================================================
# F7 — 20261102 WEIGHTING REVERSAL
# Source: Appendices E/F.
# Top-1% and remaining contributions use the execution
# denominator. Equal-workload gain is a different aggregation.
# ============================================================

TOP_GAIN = -0.011784732
REST_GAIN = -0.004377877
EXEC_GAIN = -0.016162609
WORK_GAIN = 0.007847947

assert abs(TOP_GAIN + REST_GAIN - EXEC_GAIN) < 1e-8

fig, axs = plt.subplots(
    1, 2, figsize=(7.6, 3.0), layout="constrained"
)

names = ["Frequency-top 1%", "Remaining workloads"]
values = [TOP_GAIN, REST_GAIN]

axs[0].barh(names, values, color=[RED, RED], alpha=[0.95, 0.55])
zero(axs[0])
axs[0].invert_yaxis()
axs[0].set_xlabel("Contribution to execution-weighted gain")
axs[0].set_title("(a) Signed execution contributions")

for i, value in enumerate(values):
    axs[0].text(
        value - 0.0003, i,
        f"{value:+.6f}",
        ha="right", va="center", fontsize=8,
    )

axs[1].barh(
    ["Execution-weighted", "Equal-workload"],
    [EXEC_GAIN, WORK_GAIN],
    color=[RED, BLUE],
)
zero(axs[1])
axs[1].invert_yaxis()
axs[1].set_xlabel("Absolute LogMAE gain")
axs[1].set_title("(b) Same models, different weighting")

for i, value in enumerate([EXEC_GAIN, WORK_GAIN]):
    axs[1].text(
        value + (0.0004 if value >= 0 else -0.0004),
        i,
        f"{value:+.6f}",
        ha="left" if value >= 0 else "right",
        va="center", fontsize=8,
    )

fig.suptitle(
    "Experiment 3, split 20261102: weighting reversal",
    fontsize=10,
)

save(fig, "F07_weighting_reversal")

# ============================================================
# F8 — CONCENTRATION AND ATTRIBUTION
# Source: exp3_concentration_attribution.csv / Appendix E.
# Contributions use the full validation execution denominator.
# ============================================================

SHARE = np.array([
    64.010, 65.099, 63.060, 62.634, 67.608,
    67.704, 58.519, 65.653, 64.009, 68.334,
])

TOP_CONTRIB = np.array([
    0.011222946, -0.000205236, 0.002221511,
    -0.000438347, -0.021777991, -0.011784732,
    0.005153339, 0.001680760, -0.000678906,
    0.013552698,
])

REST_CONTRIB = np.array([
    0.007821281, 0.007452501, 0.011550669,
    0.010505573, -0.022469050, -0.004377877,
    0.011971790, 0.007873974, 0.008840193,
    0.006859977,
])

fig, axs = plt.subplots(
    1, 2, figsize=(8.0, 3.5), layout="constrained"
)

axs[0].scatter(
    SHARE, EXP3_EXEC_GAIN_PCT,
    color=RED, s=38,
)
axs[0].axhline(0, color=GRAY, lw=0.9)
axs[0].set_xlabel("Executions in frequency-top 1% (%)")
axs[0].set_ylabel("Relative LogMAE gain (%)")
axs[0].set_title("(a) Concentration versus gain")
axs[0].grid(alpha=0.12)

for i in (4, 5):
    axs[0].annotate(
        str(EXP3_SEEDS[i]),
        (SHARE[i], EXP3_EXEC_GAIN_PCT[i]),
        xytext=(5, 4),
        textcoords="offset points",
        fontsize=7,
    )

y = np.arange(10)

axs[1].barh(
    y - 0.17, TOP_CONTRIB,
    height=0.32, color=RED,
    label="Frequency-top 1%",
)
axs[1].barh(
    y + 0.17, REST_CONTRIB,
    height=0.32, color=GRAY,
    label="Remaining workloads",
)

zero(axs[1])
axs[1].set_yticks(y, [str(s) for s in EXP3_SEEDS])
axs[1].invert_yaxis()
axs[1].set_xlabel("Absolute LogMAE gain contribution")
axs[1].set_title("(b) Signed contributions")
axs[1].legend(frameon=False, fontsize=7)

fig.suptitle(
    "Experiment 3: execution concentration and attribution",
    fontsize=10,
)

save(fig, "F08_concentration_attribution")

# ============================================================
# F9 — MODEL SELECTION DIAGNOSTICS
# Requires original candidate records. Do not invent them.
# ============================================================

REPORT_PATH = ROOT / "data" / "exp3_report_original.json"

if REPORT_PATH.exists():
    report = json.loads(REPORT_PATH.read_text())
    outcomes = sorted(
        report["seed_outcomes"],
        key=lambda r: r["split_seed"],
    )
    candidates = report["candidate_outcomes"]

    assert len(outcomes) == 10
    assert len(candidates) == 240

    fig, axs = plt.subplots(
        1, 2, figsize=(8.0, 3.8), layout="constrained"
    )

    y = np.arange(10)

    for role, color, marker, offset in [
        ("m0", BLUE, "o", -0.12),
        ("m1", RED, "s", 0.12),
    ]:
        rounds = [
            r[f"{role}_best_iteration"]
            for r in outcomes
        ]

        axs[0].scatter(
            rounds, y + offset,
            color=color,
            marker=marker,
            label=role.upper(),
            s=35,
        )

    axs[0].set_yticks(
        y, [str(r["split_seed"]) for r in outcomes]
    )
    axs[0].invert_yaxis()
    axs[0].set_xlabel("Selected boosting rounds")
    axs[0].set_title("(a) Selected model complexity")
    axs[0].legend(frameon=False)

    focus = 20261101

    for role, color, marker in [
        ("m0", BLUE, "o"),
        ("m1", RED, "s"),
    ]:
        subset = sorted(
            [
                c for c in candidates
                if c["split_seed"] == focus
                and c["role"] == role
            ],
            key=lambda c: c["candidate_id"],
        )

        assert len(subset) == 12

        axs[1].scatter(
            [c["candidate_id"] for c in subset],
            [c["validation_log_mae"] for c in subset],
            color=color,
            marker=marker,
            s=35,
            label=role.upper(),
        )

    axs[1].set_xlabel("Candidate ID (categorical)")
    axs[1].set_ylabel("Execution-weighted validation LogMAE")
    axs[1].set_title(
        "(b) Candidate scores, split 20261101"
    )
    axs[1].legend(frameon=False)

    fig.suptitle(
        "Experiment 3: exploratory model-selection diagnostics",
        fontsize=10,
    )

    save(fig, "F09_model_selection")

else:
    print(
        "Skipping F09: original Experiment 3 report not found at",
        REPORT_PATH,
    )

print("\nFinished. Figures saved in:", FIG)