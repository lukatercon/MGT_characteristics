import os
import sys
from transformers import pipeline
from tqdm import tqdm

from utils import combine_with_Šolar_template, build_lengths_dict, build_titles_dict

if __name__ == "__main__":
    # get arguments (usage: "python get_hf_model_responses.py model_name output_dir")
    model_name, output_dir = sys.argv[1], sys.argv[2]

    # define the files that contain lengths and titles
    lengths_file = os.path.join("..", "Datasets", "Solar", "Solar_lengths.tsv")
    titles_file = os.path.join("..", "Datasets", "Solar", "Solar_annotated_titles.tsv")

    # build text lengths dictionary and titles dictionary
    len_dict = build_lengths_dict(lengths_file)
    titles_dict = build_titles_dict(titles_file)

    # for Šolar: build a list of relevant documents
    relevant_docs_dir = os.path.join("..", "Solar_relevant_doc_ids.txt")
    relevant_docs = list()
    with open(relevant_docs_dir, "r", encoding="utf-8") as rf_rel:
        for line in rf_rel:
            if line.strip() != "":
                relevant_docs.append(line.strip())

    # initialize the pipeline
    model_id = model_name
    pline = pipeline(
        "text-generation",
        model=model_id,
        device_map="cuda"
    )

    i = 1
    for doc_id in tqdm(iter(relevant_docs), total=len(relevant_docs), desc="Progress through docs"):
        title_info = titles_dict[doc_id]

        prompt = combine_with_Šolar_template(title_info, len_dict[doc_id])

        message = [{"role": "user", "content": prompt}]
        response = pline(message, max_new_tokens=1024)

        with open(os.path.join(output_dir, f"{doc_id}.txt"), "w", encoding="utf-8") as wf:
            wf.write(response[0]["generated_text"][-1]["content"])

        if i % 100 == 0:
            print(f"Document {i}/{len(relevant_docs)}") 

        i += 1 
