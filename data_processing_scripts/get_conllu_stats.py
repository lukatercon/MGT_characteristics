import conllu

import os

conllu_file = os.path.join("..", "Datasets", "Solar", "Solar_gemma-2-27B", "annotated", "Solar_gemma-2-27B_annotated_shorter_noeng.conllu")

with open(conllu_file, "r", encoding="utf-8") as rf:
    parsed_sents = conllu.parse(rf.read())

doc_set = set()
sent_count = 0
token_count = 0

for sent in parsed_sents:
    # sents
    sent_count += 1

    # docs
    sent_id = sent.metadata["sent_id"]
    doc = sent_id.split(".")[0]
    doc_set.add(doc)

    # tokens
    for tok in sent:
        token_count += 1

doc_count = len(doc_set)

print(f"Stats for {os.path.split(conllu_file)[1]}:\n{doc_count=}, {sent_count=}, {token_count=}")
