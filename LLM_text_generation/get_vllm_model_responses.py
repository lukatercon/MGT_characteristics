import os
import sys
from vllm import LLM, SamplingParams
from tqdm import tqdm

from utils import combine_with_Šolar_default_template, combine_with_Šolar_persona_aware_template, combine_with_Šolar_linguistically_aware_template, \
                  build_lengths_dict, build_titles_dict, build_metadata_dict, combine_with_Trendi_default_template

if __name__ == "__main__":
    # get arguments (usage: "python get_hf_model_responses.py model_name output_dir prompt_type dataset")
    # prompt type can be: ["default", "persona_aware", "longer_responses", "persona_age_awareXX", "persona_grade_awareXX", "linguistically_aware_general", "linguistically_aware_specific"]   # XX refers to the age/grade of the speaker
    # dataset can be: ["Šolar", "Trendi"]
    model_name, output_dir, prompt_type, dataset = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    # define the files that contain lengths and titles
    if dataset == "Šolar":
        lengths_file = os.path.join("..", "Datasets", "Solar", "Solar_lengths.tsv")
        titles_file = os.path.join("..", "Datasets", "Solar", "Solar_annotated_titles.tsv")
    meta_file = os.path.join("..", "Datasets", "Trendi", "Trendi_2026-05_relevant_metadata.tsv")

    # build text lengths dictionary, titles dictionary, and metadata dictionary
    if dataset == "Šolar":
        len_dict = build_lengths_dict(lengths_file)
        titles_dict = build_titles_dict(titles_file)
    meta_dict = build_metadata_dict(meta_file, mode=dataset)

    # build a list of relevant documents
    if dataset == "Šolar":
        relevant_docs_dir = os.path.join("..", "Solar_relevant_doc_ids.txt")
        relevant_docs = list()
        with open(relevant_docs_dir, "r", encoding="utf-8") as rf_rel:
            for line in rf_rel:
                if line.strip() != "":
                    relevant_docs.append(line.strip())
    elif dataset == "Trendi":
        relevant_docs = list(meta_dict.keys())

    # Get the speaker age or grade for persona-aware prompts
    if prompt_type.startswith("persona_age_aware"):
        speaker_age = prompt_type.split("persona_age_aware")[1]
        prompt_type = "persona_age_aware"
    
    if prompt_type.startswith("persona_grade_aware"):
        grade = prompt_type.split("persona_grade_aware")[1].replace("_", " ")
        prompt_type = "persona_grade_aware"

    # initialize the pipeline
    model_id = model_name

    model = LLM(model_id)

    sampling_params = SamplingParams(
        n=1,
        temperature=0.6,
        top_p=0.9,
        max_tokens=2048
    )

    for doc_id in tqdm(iter(relevant_docs), total=len(relevant_docs), desc="Progress through docs"):
        if dataset == "Šolar":
            title_info = titles_dict[doc_id]
            spk_region = meta_dict[doc_id][5]
            schl_subj = meta_dict[doc_id][2]

            if prompt_type == "default":
                prompt = combine_with_Šolar_default_template(title_info, len_dict[doc_id])
            elif prompt_type == "persona_aware":
                prompt = combine_with_Šolar_persona_aware_template(title_info, len_dict[doc_id], spk_region, schl_subj)
            elif prompt_type == "persona_age_aware":
                prompt = combine_with_Šolar_persona_aware_template(title_info, len_dict[doc_id], "_", "_", age=speaker_age, mode="age")
            elif prompt_type == "persona_grade_aware":
                prompt = combine_with_Šolar_persona_aware_template(title_info, len_dict[doc_id], "_", "_", grade=grade, mode="grade")
            elif prompt_type == "longer_responses":
                prompt = combine_with_Šolar_default_template(title_info, str(len_dict[doc_id]*2))
            elif prompt_type == "linguistically_aware_general":
                prompt = combine_with_Šolar_linguistically_aware_template(title_info, len_dict[doc_id], spk_region, schl_subj, mode="general")
            elif prompt_type == "linguistically_aware_specific":
                prompt = combine_with_Šolar_linguistically_aware_template(title_info, len_dict[doc_id], spk_region, schl_subj, mode="specific")
            else:
                raise Exception(f"Invalid {prompt_type=}")
        
        elif dataset == "Trendi":
            article_length, article_topic, article_title = meta_dict[doc_id]

            prompt = combine_with_Trendi_default_template(article_title, article_topic, article_length)


        message = [[{"role": "user", "content": prompt}]]
        response = model.chat(message, sampling_params)

        with open(os.path.join(output_dir, f"{doc_id}.txt"), "w", encoding="utf-8") as wf:
            wf.write(response[0].outputs[0].text)
