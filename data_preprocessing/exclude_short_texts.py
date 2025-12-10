# Primarily for GaMS-27B, it was found that the model sometimes generates exceptionally short texts, which was usually
# caused by the model refusing to provide a response in line with the prompt we used. In these cases, we extracted 
# a subset of MGT that consisted only of essays that are longer than 100 words. Additionally, we also excluded 
# the essay with the"solar28" document ID, as it was found that the model produced only a repetition of the title 
# in a long loop and no additional content. The excluding of these essays was done both for MGT as well as HWT
# in order to ensure a fair comparison. By doing this, we ensured that we didn't include any model refusals 
# and repetition-type model errors.

import conllu
import os


def split_into_docs(sents):
    docs = list()
    curr_doc = list()
    curr_doc_id = ""
    for sent in sents:
        sent_doc_id = sent.metadata["sent_id"].strip().split(".")[0]

        if curr_doc_id == "":
            curr_doc_id = sent_doc_id
        
        if sent_doc_id != curr_doc_id:
            curr_doc_id = sent_doc_id
            docs.append(curr_doc)
            curr_doc = list()
        
        curr_doc.append(sent)
    
    docs.append(curr_doc)
    return docs


def get_short_doc_ids(docs):
    doc_ids = list()

    for doc in docs:
        words = 0
        doc_id = doc[0].metadata["sent_id"].strip().split(".")[0]

        for sent in doc:
            words += len(sent)
        
        if words < 100:
            doc_ids.append(doc_id)
    
    return doc_ids


def get_longer_docs(docs, short_docs_list):
    final_docs = list()

    # additionally add the docs where repetition occurs here
    repetition_doc_ids = ["solar91"] 

    exclude_docs = short_docs_list + repetition_doc_ids

    for doc in docs:
        if doc[0].metadata["sent_id"].strip().split(".")[0] not in exclude_docs:
            final_docs.append(doc)
    
    return final_docs


threshold = 100
mgt_input_path = os.path.join("..", "Datasets", "Solar", "Solar_GaMS-27B_age_18", "annotated", "Solar_GaMS-27B_age_18_annotated.conllu")
hwt_input_path = os.path.join("..", "Datasets", "Solar", "Solar_3.0_human", "Solar_3.0_human_relevant.conllu")

mgt_output_path = os.path.join("..", "Datasets", "Solar", "Solar_GaMS-27B_age_18", "annotated", "Solar_GaMS-27B_age_18_annotated_shorter.conllu")
hwt_output_path = os.path.join("..", "Datasets", "Solar", "Solar_3.0_human", "Solar_3.0_human_relevant_age_18_shorter.conllu")

with open(mgt_input_path, "r", encoding="utf-8") as rf_mgt:
    mgt_sents = conllu.parse(rf_mgt.read())

with open(hwt_input_path, "r", encoding="utf-8") as rf_hwt:
    hwt_sents = conllu.parse(rf_hwt.read())

mgt_docs = split_into_docs(mgt_sents)
hwt_docs = split_into_docs(hwt_sents)

short_doc_ids = get_short_doc_ids(mgt_docs)

print(f"{len(short_doc_ids)=}")

final_mgt_docs = get_longer_docs(mgt_docs, short_doc_ids)
final_hwt_docs = get_longer_docs(hwt_docs, short_doc_ids)

if not os.path.exists(mgt_output_path):
    with open(mgt_output_path, "w", encoding="utf-8") as wf_mgt:
        for doc in final_mgt_docs:
            for sent in doc:
                wf_mgt.write(sent.serialize())
else:
    raise Exception(f"Can't write to file {mgt_output_path}, since it already exists!")

if not os.path.exists(hwt_output_path):
    with open(hwt_output_path, "w", encoding="utf-8") as wf_hwt:
        for doc in final_hwt_docs:
            for sent in doc:
                wf_hwt.write(sent.serialize())
else:
    raise Exception(f"Can't write to file {hwt_output_path}, since it already exists!")
