import os
import conllu
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib_venn import venn3
from upsetplot import UpSet, from_contents


def draw_upset_with_venn(first_set, second_set, third_set, output_file, mode,
                          labels=("Solar_human", "Šolar-GaMS-27b", "Šolar-gemma-2-27B")):
    print(f"Drawing UpSet+Venn diagram for {mode}")

    # --- Build UpSet data ---
    contents = {
        labels[0]: first_set,
        labels[1]: second_set,
        labels[2]: third_set,
    }
    data = from_contents(contents)

    # --- Layout: UpSet on left (~70%), Venn on right (~30%) ---
    fig = plt.figure(figsize=(16, 7))
    fig.suptitle(f"Set Overlap for {mode}", fontsize=15, fontweight="bold", y=1.01)

    gs = gridspec.GridSpec(1, 2, width_ratios=[2.2, 1], wspace=0.05, figure=fig)

    # UpSet axes — UpSet needs to own a gridspec, so we nest it
    gs_upset = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0],
                                                height_ratios=[2.5, 1], hspace=0.08)
    ax_bar   = fig.add_subplot(gs_upset[0])   # intersection bar chart
    ax_matrix = fig.add_subplot(gs_upset[1])  # dot matrix

    # Venn axis
    ax_venn = fig.add_subplot(gs[1])

    # --- Draw UpSet manually for full style control ---
    # Compute all intersection counts
    a, b, c = first_set, second_set, third_set
    intersections = {
        (True,  False, False): len(a - b - c),
        (False, True,  False): len(b - a - c),
        (False, False, True):  len(c - a - b),
        (True,  True,  False): len((a & b) - c),
        (True,  False, True):  len((a & c) - b),
        (False, True,  True):  len((b & c) - a),
        (True,  True,  True):  len(a & b & c),
    }

    # Sort by size descending (common UpSet convention)
    sorted_ints = sorted(intersections.items(), key=lambda x: -x[1])
    keys   = [k for k, _ in sorted_ints]
    counts = [v for _, v in sorted_ints]
    n_bars = len(keys)
    x_pos  = np.arange(n_bars)

    set_names = list(labels)
    n_sets    = len(set_names)

    DARK   = "#2e2e2e"
    LIGHT  = "#cccccc"
    BAR_COLOR = "#3a3a3a"

    # -- Top: bar chart --
    bars = ax_bar.bar(x_pos, counts, color=BAR_COLOR, width=0.5, zorder=3)
    for bar, count in zip(bars, counts):
        ax_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(counts) * 0.01,
                    f"{count:,}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax_bar.set_xlim(-0.5, n_bars - 0.5)
    ax_bar.set_ylabel("Intersection size", fontsize=11)
    ax_bar.set_xticks([])
    ax_bar.spines[["top", "right", "bottom"]].set_visible(False)
    ax_bar.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax_bar.set_axisbelow(True)

    # -- Bottom: dot matrix --
    row_y = {name: n_sets - 1 - i for i, name in enumerate(set_names)}

    # Background row stripes
    for i, name in enumerate(set_names):
        y = row_y[name]
        ax_matrix.axhspan(y - 0.5, y + 0.5,
                          color="#f5f5f5" if i % 2 == 0 else "white", zorder=0)

    # All dots (light), then connected+filled dots for active sets
    dot_r = 0.28
    for xi, key in enumerate(keys):
        active_rows = [set_names[j] for j, active in enumerate(key) if active]

        # Draw faint dots for all rows
        for name in set_names:
            y = row_y[name]
            ax_matrix.scatter(xi, y, s=200, color=LIGHT, zorder=2, linewidths=0)

        # Draw connector line between topmost and bottommost active dot
        if len(active_rows) > 1:
            ys = [row_y[n] for n in active_rows]
            ax_matrix.plot([xi, xi], [min(ys), max(ys)],
                           color=DARK, linewidth=3.5, zorder=3, solid_capstyle="round")

        # Draw filled dots for active rows
        for name in active_rows:
            y = row_y[name]
            ax_matrix.scatter(xi, y, s=200, color=DARK, zorder=4, linewidths=0)

    # Set name labels on y-axis
    ax_matrix.set_yticks(list(row_y.values()))
    ax_matrix.set_yticklabels(list(row_y.keys()), fontsize=10)
    ax_matrix.set_xlim(-0.5, n_bars - 0.5)
    ax_matrix.set_ylim(-0.5, n_sets - 0.5)
    ax_matrix.set_xticks([])
    ax_matrix.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax_matrix.tick_params(left=False)

    # -- Right: Venn diagram --
    v = venn3(
        subsets=(first_set, second_set, third_set),
        set_labels=("", "", ""),
        set_colors=("tomato", "mediumseagreen", "cornflowerblue"),
        alpha=0.5,
        ax=ax_venn
    )
    for patch_id in ["100", "010", "001", "110", "101", "011", "111"]:
        lbl = v.get_label_by_id(patch_id)
        if lbl:
            lbl.set_fontsize(9)
            lbl.set_fontweight("bold")

    venn_label_coords = [
        (labels[0], first_set,  (-0.50,  0.30)),
        (labels[1], second_set, ( 0.42,  0.38)),
        (labels[2], third_set,  ( 0.05, -0.52)),
    ]
    for name, s, (x, y) in venn_label_coords:
        ax_venn.text(x, y, f"{name}\nn={len(s):,}",
                     ha="center", va="center", fontsize=8, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gray", alpha=0.8))
    ax_venn.set_title("Venn", fontsize=11, pad=6)

    # --- Caption ---
    caption = (r"$\bf{Figure\ 6:}$ " +
               f"UpSet plot and Venn diagram comparing unique {mode} across treebanks. "
               f"Bars show intersection sizes; filled dots indicate set membership.")
    fig.text(0.01, -0.03, caption, wrap=True, fontsize=9, color="#444444")

    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    plt.close(fig)


first_file_lemmas = os.path.join("..", "Datasets", "Solar", "Solar_human", "annotated", "Solar_human_annotated_shorter_noeng.conllu")
first_file_trees = os.path.join("Solar_human_annotated_shorter_noeng_trees.tsv")
second_file_lemmas = os.path.join("..", "Datasets", "Solar", "Solar_GaMS-27B", "annotated", "Solar_GaMS-27B_annotated_shorter_noeng.conllu")
second_file_trees = os.path.join("Solar_GaMS-27B_annotated_shorter_noeng_trees.tsv")
third_file_lemmas = os.path.join("..", "Datasets", "Solar", "Solar_gemma-2-27B", "annotated", "Solar_gemma-2-27B_annotated_shorter_noeng.conllu")
third_file_trees = os.path.join("Solar_gemma-2-27B_annotated_shorter_noeng_trees.tsv")

output_file_lemmas = os.path.join("upsetplot_Solar_human-gams-gemma_lemmas.png")
output_file_trees = os.path.join("upsetplot_Solar_human-gams-gemma_trees.png")

# open lemma files
with open(first_file_lemmas, "r", encoding="utf-8") as rf_fl:
    first_sents = conllu.parse(rf_fl.read())
    first_lemmas = set([tok["lemma"] for sent in first_sents for tok in sent])

with open(second_file_lemmas, "r", encoding="utf-8") as rf_sl:
    second_sents = conllu.parse(rf_sl.read())
    second_lemmas = set([tok["lemma"] for sent in second_sents for tok in sent])

with open(third_file_lemmas, "r", encoding="utf-8") as rf_tl:
    third_sents = conllu.parse(rf_tl.read())
    third_lemmas = set([tok["lemma"] for sent in third_sents for tok in sent])

# open tree files
with open(first_file_trees, "r", encoding="utf-8") as rf_ft:
    first_lines = rf_ft.readlines()
    first_trees = set([line.strip().split("\t")[0] for line in first_lines[1:]])

with open(second_file_trees, "r", encoding="utf-8") as rf_st:
    second_lines = rf_st.readlines()
    second_trees = set([line.strip().split("\t")[0] for line in second_lines[1:]])

with open(third_file_trees, "r", encoding="utf-8") as rf_tt:
    third_lines = rf_tt.readlines()
    third_trees = set([line.strip().split("\t")[0] for line in third_lines[1:]])

draw_upset_with_venn(first_lemmas, second_lemmas, third_lemmas, output_file_lemmas, "lemmas")
draw_upset_with_venn(first_trees,  second_trees,  third_trees,  output_file_trees,  "trees")
