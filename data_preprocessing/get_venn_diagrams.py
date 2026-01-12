from matplotlib import pyplot as plt
from matplotlib_venn import venn2
import conllu

import os


def draw_venn(Ab, aB, AB, output_file, mode):
    fig = plt.figure(figsize=(12, 6))
    venn2(subsets=(Ab, aB, AB), set_labels=("first", "second"), set_colors=("green", "pink"))
    plt.title(f"Syntactic Tree Venn Diagram")
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.25)

    # Caption and display the plot
    caption = (r"$\bf{Figure\ 6:}$" + f"Venn diagram comparison of the number of unique {mode} present in "
                f"each treebank.")
    fig.text(0, 0.01, caption, wrap=True, fontsize=10)

    plt.savefig(output_file)


first_file_lemmas = os.path.join("Solar_3.0_human_relevant_shorter.conllu")
first_file_trees = os.path.join("Solar_3.0_human_relevant_shorter_trees.tsv")
second_file_lemmas = os.path.join("Solar_GaMS-27B_annotated_shorter.conllu")
second_file_trees = os.path.join("Solar_GaMS-27B_annotated_shorter_trees.tsv")

output_file_lemmas = os.path.join("Venn_human-gams_lemmas.png")
output_file_trees = os.path.join("Venn_human-gams_trees.png")

# open lemma files
with open(first_file_lemmas, "r", encoding="utf-8") as rf_fl:
    first_sents = conllu.parse(rf_fl.read())
    first_lemmas = set([tok["lemma"] for sent in first_sents for tok in sent])

with open(second_file_lemmas, "r", encoding="utf-8") as rf_sl:
    second_sents = conllu.parse(rf_sl.read())
    second_lemmas = set([tok["lemma"] for sent in second_sents for tok in sent])

# open tree files
with open(first_file_trees, "r", encoding="utf-8") as rf_ft:
    first_lines = rf_ft.readlines()
    first_trees = set([line.strip().split("\t")[0] for line in first_lines[1:]])

with open(second_file_trees, "r", encoding="utf-8") as rf_st:
    second_lines = rf_st.readlines()
    second_trees = set([line.strip().split("\t")[0] for line in second_lines[1:]])


