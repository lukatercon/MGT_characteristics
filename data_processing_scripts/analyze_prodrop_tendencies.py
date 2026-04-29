import os
import conllu


def parse_conllu(filepath):
    with open(filepath, "r", encoding="utf-8") as rf:
        conllu_sents = conllu.parse(rf.read())
    
    return conllu_sents


def count_fv(sent):
    count = 0

    for tok in sent:
        if tok["upos"] == "VERB" and tok["feats"] and tok["feats"].get("VerbForm") == "Fin":
            count += 1
    
    return count

def count_fv_os(sent):
    count = 0

    for tok in sent:
        head_is_finite = sent[tok["head"] - 1]["upos"] == "VERB" and sent[tok["head"] - 1]["feats"] \
            and sent[tok["head"] - 1]["feats"].get("VerbForm") == "Fin"

        if tok["deprel"] == "nsubj" and head_is_finite:
            count += 1
    
    return count


def count_fv_ops(sent):
    count = 0

    for tok in sent:
        head_is_finite = sent[tok["head"] - 1]["upos"] == "VERB" and sent[tok["head"] - 1]["feats"] \
            and sent[tok["head"] - 1]["feats"].get("VerbForm") == "Fin"

        if tok["deprel"] == "nsubj" and tok["upos"] == "PRON" and head_is_finite:
            count += 1
    
    return count


first_file = os.path.join("..", "Datasets", "Solar", "Solar_GaMS-27B", "annotated", "Solar_GaMS-27B_annotated_shorter_noeng.conllu")
second_file = os.path.join("..", "Datasets", "Solar", "Solar_gemma-2-27B", "annotated", "Solar_gemma-2-27B_annotated_shorter_noeng.conllu")

first_sents = parse_conllu(first_file)
second_sents = parse_conllu(second_file)

print(f"Length of first corpus: {len([tok for sent in first_sents for tok in sent])} tokens.")
print(f"Length of second corpus: {len([tok for sent in second_sents for tok in sent])} tokens.")

finite_verbs_count = [0, 0]
finite_verbs_ovrt_subj_count = [0, 0]
finite_verbs_ovrt_prn_subj_count = [0, 0]

for sent_list in [first_sents, second_sents]:
    if sent_list == first_sents:
        index = 0
    else:
        index = 1

    for sent in sent_list:
        finite_verbs_count[index] += count_fv(sent)
        finite_verbs_ovrt_subj_count[index] += count_fv_os(sent)
        finite_verbs_ovrt_prn_subj_count[index] += count_fv_ops(sent)

print(f"{finite_verbs_count=}\n{finite_verbs_ovrt_subj_count=}\n{finite_verbs_ovrt_prn_subj_count=}")
