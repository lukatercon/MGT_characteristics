# Script that extracts all essays by 6th grade students that are labeled as "esej ali spis"
import conllu
import os

meta_file_path = os.path.join("..", "Datasets", "Solar", "solar-meta.tsv")

# open the meta file and get our target essay IDs
target_ids = list()
with open(meta_file_path, "r", encoding="utf-8") as rf:
    for line in rf:
        line_split = line.strip().split("\t")
        essay_id = line_split[1][:-1]
        grade = line_split[6]
        text_type = line_split[7]

        if grade == "6. razred" and text_type == "esej ali spis":
            target_ids.append(essay_id)

#TODO: Everything else!!
