from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3
import conllu

import os


def draw_venn(first_set, second_set, output_file, mode):
    print(f"Drawing Venn diagram for {mode}")

    fig = plt.figure(figsize=(12, 6))
    venn2(subsets=(first_set, second_set), set_labels=("Šolar-GaMS-27b", "Šolar-gemma-2-27B"), set_colors=("green", "blue"))
    plt.title(f"Venn Diagram for {mode}")
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.25)

    # Caption and display the plot
    caption = (r"$\bf{Figure\ 6:}$" + f"Venn diagram comparison of the number of unique {mode} present in "
                f"each treebank.")
    fig.text(0, 0.01, caption, wrap=True, fontsize=10)

    plt.savefig(output_file)


def draw_venn_tree_way_old(first_set, second_set, third_set, output_file, mode):
    print(f"Drawing Venn diagram for {mode}")

    fig = plt.figure(figsize=(12, 6))
    venn3(subsets=(first_set, second_set, third_set), set_labels=("Solar_human", "Šolar-GaMS-27b", "Šolar-gemma-2-27B"), set_colors=("red", "green", "blue"))
    plt.title(f"Venn Diagram for {mode}")
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.25)

    # Caption and display the plot
    caption = (r"$\bf{Figure\ 6:}$" + f"Venn diagram comparison of the number of unique {mode} present in "
                f"each treebank.")
    fig.text(0, 0.01, caption, wrap=True, fontsize=10)

    plt.savefig(output_file)


def draw_venn_tree_way(first_set, second_set, third_set, output_file, mode):
    print(f"Drawing Venn diagram for {mode}s")

    fig, ax = plt.subplots(figsize=(12, 8))

    v = venn3(
        subsets=(first_set, second_set, third_set),
        set_labels=("", "", ""),  # we'll add custom labels manually
        set_colors=("#B32EA1", "#1E3CAA", "#5BC718"),
        alpha=0.55,
        ax=ax
    )

    # Compute totals for annotation
    totals = {
        "Solar_human": len(first_set),
        "Šolar-GaMS-27b": len(second_set),
        "Šolar-gemma-2-27B": len(third_set),
    }

    # Bold, readable patch labels (counts in overlap regions)
    for patch_id in ["100", "010", "001", "110", "101", "011", "111"]:
        label = v.get_label_by_id(patch_id)
        if label:
            label.set_fontsize(13)
            label.set_fontweight("bold")

    # Custom set labels with totals beneath
    label_data = [
        ("A", "Human", first_set,  (-0.60,  0.45)),
        ("B", "GaMS",  second_set, ( 0.35,  0.45)),
        ("C", "Gemma", third_set,  ( 0.35, -0.55)),
    ]
    for _, name, s, (x, y) in label_data:
        ax.text(x, y, f"{name}\n(total = {len(s):,})",
                ha="center", va="center", fontsize=18, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))

    ax.set_title(f"Venn Diagram for {mode} Overlap",
                 fontsize=22, fontweight="bold", pad=16)

    plt.tight_layout()
    fig.subplots_adjust(bottom=0.10)
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    plt.close(fig)


def draw_venn_two_way(first_set, second_set, output_file, mode):
    print(f"Drawing Venn diagram for {mode}s")

    fig, ax = plt.subplots(figsize=(12, 8))

    #green: #3CC014
    #blue: #14A0C0

    v = venn2(
        subsets=(first_set, second_set),
        set_labels=("", ""),  # custom labels added manually
        set_colors=("#CA357F", "#3CC014"),
        alpha=0.55,
        ax=ax
    )

    # Compute intersection count and percentage relative to second set
    intersection = first_set & second_set
    intersection_count = len(intersection)
    pct_of_second = (intersection_count / len(second_set) * 100) if len(second_set) > 0 else 0.0

    # Bold, readable patch labels (counts in overlap regions)
    for patch_id in ["10", "01", "11"]:
        label = v.get_label_by_id(patch_id)
        if label:
            label.set_fontsize(13)
            label.set_fontweight("bold")

    # Append percentage line beneath the raw count in the intersection region
    intersection_label = v.get_label_by_id("11")
    if intersection_label:
        intersection_label.set_text(
            f"{intersection_count}\n({pct_of_second:.1f}%)"
        )

    # Custom set labels with totals beneath
    label_data = [
        ("Human", first_set,  (-0.40, 0.45)),
        ("Gemma",  second_set, ( 0.40, 0.45)),
    ]
    for name, s, (x, y) in label_data:
        ax.text(x, y, f"{name}\n(total = {len(s):,})",
                ha="center", va="center", fontsize=18, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))

    ax.set_title(f"Venn Diagram for {mode} Overlap",
                 fontsize=22, fontweight="bold", pad=16)

    plt.tight_layout()
    fig.subplots_adjust(bottom=0.10)
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    plt.close(fig)


first_file_lemmas = os.path.join("..", "Datasets", "Trendi", "Trendi_human", "annotated", "Trendi_human_annotated.conllu")
first_file_trees = os.path.join("script_output_input", "Trendi_human_vs_GaMS-27b.tsv")
second_file_lemmas = os.path.join("..", "Datasets", "Trendi", "Trendi_GaMS-27B", "annotated", "Trendi_GaMS-27B_annotated.conllu")
second_file_trees = os.path.join("script_output_input", "Trendi_GaMS-27B_vs_human.tsv")
third_file_lemmas = os.path.join("..", "Datasets", "Trendi", "Trendi_gemma-2-27B", "annotated", "Trendi_gemma-2-27B_annotated.conllu")
third_file_trees = os.path.join("script_output_input", "Trendi_gemma-2-27B_vs_human.tsv")

output_file_lemmas = os.path.join("script_output_input", "Venn_Trendi_human-gemma_lemmas.png")
output_file_trees = os.path.join("script_output_input", "Venn_Trendi_human-gemma_trees.png")

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

# draw Venn diagram for lemmas
#draw_venn(first_lemmas, second_lemmas, output_file_lemmas, "lemmas")
#draw_venn_tree_way(first_lemmas, second_lemmas, third_lemmas, output_file_lemmas, "Lemma")
draw_venn_two_way(first_lemmas, third_lemmas, output_file_lemmas, "Lemma")

# draw Venn diagram for trees
#draw_venn(first_trees, second_trees, output_file_trees, "trees")
#draw_venn_tree_way(first_trees, second_trees, third_trees, output_file_trees, "Tree")
draw_venn_two_way(first_trees, third_trees, output_file_trees, "Tree")
