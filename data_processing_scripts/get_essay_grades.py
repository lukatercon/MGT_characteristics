import os
import json
from collections import defaultdict


def build_metadata_dict(meta_file):
    meta_dict = dict()
    with open(meta_file, "r", encoding="utf-8") as rf_meta:
        for line in rf_meta.readlines()[1:]:
            _, solar_id, _, date, school_type, subject, grade, text_type, region = line.strip().split("\t")

            solar_id = solar_id[:-1]
            meta_dict[solar_id] = (date, school_type, subject, grade, text_type, region)

    return meta_dict


meta_file = os.path.join("..", "Datasets", "Solar", "solar-meta.tsv")
meta_dict = build_metadata_dict(meta_file)

output_file = os.path.join("..", "Datasets", "Solar", "essay_grades.json")

# build a dictionary of essay ids per grade (only include essays)
grade_dict = defaultdict(list)
for doc in meta_dict.keys():
    if meta_dict[doc][4] == "esej ali spis":
        grade_dict[meta_dict[doc][3]].append(doc)

#assert not os.path.isfile(output_file)

with open(output_file, "w", encoding="utf-8") as wf:
    json.dump(grade_dict, wf, indent=4)
