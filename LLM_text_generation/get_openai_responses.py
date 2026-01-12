from tqdm import tqdm
from openai import OpenAI

import os

from utils import combine_with_Šolar_default_template, combine_with_Šolar_persona_aware_template, \
                  combine_with_Šolar_linguistically_aware_template, build_lengths_dict, build_titles_dict, \
                  build_metadata_dict, combine_with_locness_default_template, combine_with_locness_linguistically_aware_template

if __name__ == "__main__":
    # define the client and the model to be used
    client = OpenAI()
    model_to_use = "gpt-5-2025-08-07"     # this is the model used by default in the ChatGPT browser interface at time of generation "gpt-5-2025-08-07"
    prompt_type = "default"
    # prompt type can be: ["default", "persona_aware", "longer_responses", "persona_age_awareXX", "linguistically_aware_general", "linguistically_aware_specific"]   # XX refers to the age of the speaker
    dataset = "LOCNESS"
    # dataset can be: ["Šolar", "LOCNESS"]

    # Get the speaker age for persona-aware prompts
    if prompt_type.startswith("persona_age_aware"):
        speaker_age = prompt_type.split("persona_age_aware")[1]
        prompt_type = "persona_age_aware"

    # define the files that contain lengths and titles
    lengths_file = os.path.join("..", "Datasets", "Solar", "Solar_lengths.tsv")
    titles_file = os.path.join("..", "Datasets", "Solar", "Solar_annotated_titles.tsv")

    meta_file = os.path.join("..", "Datasets", "LOCNESS", "locness-meta.tsv")

    # define the output dir
    output_dir = os.path.join("..", "Datasets", "LOCNESS", "LOCNESS-GPT-5", "raw")

    # build metadata dictionaries
    if dataset == "Šolar":
        len_dict = build_lengths_dict(lengths_file)
        titles_dict = build_titles_dict(titles_file)

    meta_dict = build_metadata_dict(meta_file, mode=dataset)

    # build a list of relevant documents
    relevant_docs_dir = os.path.join("..", "LOCNESS_relevant_doc_ids.txt")
    relevant_docs = list()
    with open(relevant_docs_dir, "r", encoding="utf-8") as rf_rel:
        for line in rf_rel:
            if line.strip() != "":
                relevant_docs.append(line.strip())

    # go through every document in human-written and generate a corresponding machine generated essay, 
    # but only if the id is in the list of relevant docs
    for doc_id in tqdm(iter(relevant_docs), total=len(relevant_docs), desc="Progress through docs"):
        # get remaining metadata
        if dataset == "Šolar":
            title_info = titles_dict[doc_id]
            spk_region = meta_dict[doc_id][5]
            schl_subj = meta_dict[doc_id][2]
        if dataset == "LOCNESS":
            topic, length = meta_dict[doc_id]

        # build prompt
        if prompt_type == "default":
            if dataset == "Šolar":
                prompt = combine_with_Šolar_default_template(title_info, len_dict[doc_id])
            elif dataset == "LOCNESS":
                prompt = combine_with_locness_default_template(topic, length)

        elif prompt_type == "persona_aware":
            prompt = combine_with_Šolar_persona_aware_template(title_info, len_dict[doc_id], spk_region, schl_subj)

        elif prompt_type == "persona_age_aware":
            prompt = combine_with_Šolar_persona_aware_template(title_info, len_dict[doc_id], "_", "_", age=speaker_age, mode="age")

        elif prompt_type == "longer_responses":
            prompt = combine_with_Šolar_default_template(title_info, str(len_dict[doc_id]*2))

        elif prompt_type == "linguistically_aware_general":
            if dataset == "Šolar":
                prompt = combine_with_Šolar_linguistically_aware_template(title_info, len_dict[doc_id], spk_region, schl_subj, mode="general")
            elif dataset == "LOCNESS":
                prompt = combine_with_locness_linguistically_aware_template(topic, length)

        elif prompt_type == "linguistically_aware_specific":
            prompt = combine_with_Šolar_linguistically_aware_template(title_info, len_dict[doc_id], spk_region, schl_subj, mode="specific")

        else:
            raise Exception(f"Invalid {prompt_type=}")

        # get response for prompt
        completion = client.chat.completions.create(
            model=model_to_use,
            temperature=1,
            top_p=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # use a default system prompt in English (even for Slovenian user prompts), since this reflects the default usage of most users
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        with open(os.path.join(output_dir, f"{doc_id}.txt"), "w", encoding="utf-8") as wf:
            wf.write(completion.choices[0].message.content)
