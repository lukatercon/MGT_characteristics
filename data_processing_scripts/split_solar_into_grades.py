import os
import json

all_raw_texts_filepath = os.path.join("..", "Datasets", "Solar", "Solar_human", "raw", "Solar_3.0_human_raw.txt")
grade_folder = os.path.join("..", "data_analysis", "Obdobja_paper", "Data_by_grade", "human", "raw")
grade_docs_file = os.path.join("..", "Datasets", "Solar", "essay_grades.json")
titles_file = os.path.join("..", "Datasets", "Solar", "Solar_annotated_titles.tsv")
meta_file = os.path.join("..", "Datasets", "Solar", "solar-meta.tsv")
relevant_docs_file = os.path.join("..", "data_analysis", "Obdobja_paper", "Data_by_grade", "Solar_relevant_w_title_info.txt")

with open(grade_docs_file, "r", encoding="utf-8") as rf_json:
    grades_dict = json.loads(rf_json.read())

with open(titles_file, "r", encoding="utf-8") as rf_titles:
    titles_dict = dict()
    for line in rf_titles.readlines()[1:]:
        if "\t" not in line:
            continue

        doc_id, title, ref_lit_work, subtype = line.strip().split("\t")
        titles_dict[doc_id] = (title, ref_lit_work, subtype)

with open(meta_file, "r", encoding="utf-8") as rf_meta:
    gradegenre_dict = dict()
    for line in rf_meta.readlines()[1:]:
        if "\t" not in line:
            continue

        _, orig_id, _, _, _, _, grade, genre, _ = line.strip().split("\t")
        gradegenre_dict[orig_id[:-1]] = (grade, genre)

with open(all_raw_texts_filepath, "r", encoding="utf-8") as rf_raw:
    raw_texts_dict = dict()
    raw_text_split = rf_raw.read().split("\n\n")

    for text in raw_text_split:
        if len(text.strip()) < 1:
            continue

        if text.startswith("solar"):
            text_id = text.split("\n")[0]
            text_main = "\n".join(text.split("\n")[1:])
            raw_texts_dict[text_id] = text_main

relevant_docs = list()
for raw_text_id in raw_texts_dict.keys():
    tgrade, tgenre = gradegenre_dict[raw_text_id]
    if tgenre == "esej ali spis" and any(x != "N/A" for x in titles_dict[raw_text_id]):
        relevant_docs.append(raw_text_id)
        target_file = os.path.join(grade_folder, tgrade.replace(" ", "_"), f"{raw_text_id}.txt")
        with open(target_file, "w", encoding="utf-8") as wf:
            wf.write(raw_texts_dict[raw_text_id])

with open(relevant_docs_file, "w", encoding="utf-8") as wf_relevant:
    wf_relevant.write("\n".join(relevant_docs))
