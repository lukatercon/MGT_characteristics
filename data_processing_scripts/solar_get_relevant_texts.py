import os

metadata_file = os.path.join("..", "Datasets", "Solar", "solar-meta.tsv")
titles_file = os.path.join("..", "Datasets", "Solar", "Solar_annotated_titles.tsv")
output_file = os.path.join("..", "Solar_relevant_doc_ids.txt")


# functions to check for the three conditions
def is_essay(id):
    if meta_dict[id][4] == "esej ali spis":
        return True
    else:
        return False
    

def is_by_relevant_student(id):
    if meta_dict[id][1] == "gimnazija" and meta_dict[id][3] == "4. letnik":
        return True
    else:
        return False
    

def has_title_or_ref_work(id):
    if titles_dict[id][0] != "N/A" or titles_dict[id][1] != "N/A":
        return True
    else:
        return False


# build metadata dictionary
meta_dict = dict()
with open(metadata_file, "r", encoding="utf-8") as rf_meta:
    for line in rf_meta.readlines()[1:]: # ignore header line
        _, doc_id, _, date, school, subject, grade, text_type, region = line.strip().split("\t")
        doc_id = doc_id[:-1]
        meta_dict[doc_id] = (date, school, subject, grade, text_type, region)

# build titles dictionary
titles_dict = dict()
with open(titles_file, "r", encoding="utf-8") as rf_titles:
    for line in rf_titles.readlines()[1:]:
        doc_id, title, ref_work, subtitle = line.strip().split("\t")
        titles_dict[doc_id] = (title, ref_work, subtitle)

# open the output file and write down all relevant document IDs
with open(output_file, "w", encoding="utf-8") as wf:
    for doc_id in meta_dict.keys():
        # the conditions
        if is_essay(doc_id) and is_by_relevant_student(doc_id) and has_title_or_ref_work(doc_id):
            wf.write(doc_id + "\n")
