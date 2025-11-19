import os
import sys
from transformers import pipeline
from tqdm import tqdm

from utils import combine_with_Šolar_default_template, combine_with_Šolar_persona_aware_template, build_lengths_dict, build_titles_dict, build_metadata_dict

if __name__ == "__main__":
    # get arguments (usage: "python get_hf_model_responses.py model_name output_dir prompt_type")
    # prompt type can be: ["default", "persona_aware"]
    model_name, output_dir, prompt_type = sys.argv[1], sys.argv[2], sys.argv[3]

    # define the files that contain lengths and titles
    lengths_file = os.path.join("..", "Datasets", "Solar", "Solar_lengths.tsv")
    titles_file = os.path.join("..", "Datasets", "Solar", "Solar_annotated_titles.tsv")
    meta_file = os.path.join("..", "Datasets", "Solar", "solar-meta.tsv")

    # build text lengths dictionary, titles dictionary, and metadata dictionary
    len_dict = build_lengths_dict(lengths_file)
    titles_dict = build_titles_dict(titles_file)
    meta_dict = build_metadata_dict(meta_file)

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

    for doc_id in tqdm(iter(relevant_docs), total=len(relevant_docs), desc="Progress through docs"):
        title_info = titles_dict[doc_id]
        spk_region = meta_dict[doc_id][5]
        schl_subj = meta_dict[doc_id][2]

        if prompt_type == "default":
            prompt = combine_with_Šolar_default_template(title_info, len_dict[doc_id])
        elif  prompt_type == "persona_aware":
            prompt = combine_with_Šolar_persona_aware_template(title_info, len_dict[doc_id], spk_region, schl_subj)

        message = [{"role": "user", "content": prompt}]
        response = pline(message, max_new_tokens=2048)

        with open(os.path.join(output_dir, f"{doc_id}.txt"), "w", encoding="utf-8") as wf:
            wf.write(response[0]["generated_text"][-1]["content"])
