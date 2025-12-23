import os
import json
import copy

import conllu

output_dir = os.path.join("..", "Datasets", "Solar", "Solar_3.0_human", "essays_by_grades")
grades_file = os.path.join("..", "Datasets", "Solar", "essay_grades.json")
human_essays_file = os.path.join("..", "Datasets", "Solar", "Solar_3.0_human", "Solar_3.0_human_annotated_spaces_fixed.conllu")

with open(grades_file, "r", encoding="utf-8") as rf_grades:
    grades_dict = json.load(rf_grades)

with open(human_essays_file, "r", encoding="utf-8") as rf_essays:
    all_sents = conllu.parse(rf_essays.read())

for grade, ids_list in grades_dict.items():
    grades_sents = list()

    for sent in all_sents:
        if sent.metadata["sent_id"].split(".")[0] in ids_list:
            grades_sents.append(sent)

    with open(os.path.join(output_dir, f"{grade.replace(" ", "_")}_sents.conllu"), "w", encoding="utf-8") as wf:
        for grade_sent in grades_sents:
            wf.write(grade_sent.serialize())
