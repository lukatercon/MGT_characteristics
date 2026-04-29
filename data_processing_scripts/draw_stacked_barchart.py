import os
import conllu
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib_venn import venn3


def draw_stacked_bar(first_set, second_set, third_set, output_file, mode):
    # first_set = human, second_set = gams, third_set = gemma
    
    # Calculate overlaps
    human_gams_overlap = len(first_set & second_set)
    human_gemma_overlap = len(first_set & third_set)
    gams_only = len(second_set - first_set)
    gemma_only = len(third_set - first_set)
    
    # Bar data
    gams_bar = [human_gams_overlap, gams_only]
    gemma_bar = [human_gemma_overlap, gemma_only]
    
    # Calculate totals for percentage calculation
    gams_total = sum(gams_bar)
    gemma_total = sum(gemma_bar)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(2)
    width = 0.6
    
    # Colors for segments
    color_human_overlap = "#5CCC65"
    color_only = "#4FBBBE"
    
    # Stack the bars
    ax.bar(x[0], human_gams_overlap, width, label='Overlap with Human', color=color_human_overlap)
    ax.bar(x[0], gams_only, width, bottom=human_gams_overlap, label='Rest', color=color_only)
    
    ax.bar(x[1], human_gemma_overlap, width, color=color_human_overlap)
    ax.bar(x[1], gemma_only, width, bottom=human_gemma_overlap, color=color_only)
    
    # Add text labels with arrows
    def add_label_with_arrow(ax, x_pos, height, y_bottom, label_text, color, total):
        if height > 0:
            percentage = (height / total) * 100
            y_center = y_bottom + height/2
            text_x = x_pos + width/2 + 0.05
            ax.annotate(label_text + f'({percentage:.1f}%)', xy=(x_pos + width/2, y_center), xytext=(text_x, y_center),
                       fontsize=14, fontweight='bold', color='#000000',
                       arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                       ha='left', va='center')
    
    # GaMS bar labels
    add_label_with_arrow(ax, x[0], human_gams_overlap, 0, 'Overlap ', color_human_overlap, gams_total)
    add_label_with_arrow(ax, x[0], gams_only, human_gams_overlap, 'Rest ', color_only, gams_total)
    
    # Gemma bar labels
    add_label_with_arrow(ax, x[1], human_gemma_overlap, 0, 'Overlap ', color_human_overlap, gemma_total)
    add_label_with_arrow(ax, x[1], gemma_only, human_gemma_overlap, 'Rest ', color_only, gemma_total)
    
    # Labels and formatting
    ax.set_ylabel('Count', fontsize=18, fontweight='bold')
    ax.set_title(f'Internal Composition for Sets of {mode.capitalize()}', fontsize=22, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['GaMS', 'Gemma'], fontsize=18, fontweight='bold')
    ax.tick_params(axis='y', labelsize=13)
    ax.legend(loc='upper left', fontsize=18, framealpha=0.95)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Stacked bar chart saved to {output_file}")


first_file_lemmas = os.path.join("..", "Datasets", "Solar", "Solar_human", "annotated", "Solar_human_annotated_shorter_noeng.conllu")
first_file_trees = os.path.join("Solar_human_annotated_shorter_noeng_trees.tsv")
second_file_lemmas = os.path.join("..", "Datasets", "Solar", "Solar_GaMS-27B", "annotated", "Solar_GaMS-27B_annotated_shorter_noeng.conllu")
second_file_trees = os.path.join("Solar_GaMS-27B_annotated_shorter_noeng_trees.tsv")
third_file_lemmas = os.path.join("..", "Datasets", "Solar", "Solar_gemma-2-27B", "annotated", "Solar_gemma-2-27B_annotated_shorter_noeng.conllu")
third_file_trees = os.path.join("Solar_gemma-2-27B_annotated_shorter_noeng_trees.tsv")

output_file_lemmas = os.path.join("stackedbar_Solar_human-gams-gemma_lemmas.png")
output_file_trees = os.path.join("stackedbar_Solar_human-gams-gemma_trees.png")

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

draw_stacked_bar(first_lemmas, second_lemmas, third_lemmas, output_file_lemmas, "lemmas")
draw_stacked_bar(first_trees,  second_trees,  third_trees,  output_file_trees,  "trees")
