from trankit import Pipeline, trankit2conllu
from tqdm import tqdm

import os


#model_path = os.path.join("..", "Models", "save_dir_ssj+sst")
model_path = r"C:\Users\Tercon\Desktop\save_dir_ssj+sst"
raw_files_path = os.path.join("..", "Datasets", "Solar", "Solar_GaMS-1b", "raw_trailingspace_removed")
output_path = os.path.join("..", "Datasets", "Solar", "Solar_GaMS-1b", "annotated", "Solar_GaMS-1b_annotated.conllu")

relevant_ids_file = os.path.join("..", "Solar_relevant_doc_ids.txt")

# build list of relevant doc ids
relevant_ids = list()
with open(relevant_ids_file, "r", encoding="utf-8") as rf_ids:
    for line in rf_ids:
        relevant_ids.append(line.strip())

# load the Trankit models
p = Pipeline(lang="customized", cache_dir=model_path, embedding='xlm-roberta-large', gpu=True)

print("Done loading Trankit models!")

# open output file
with open(output_path, "w", encoding="utf-8") as wf:
    for doc_id in tqdm(iter(relevant_ids), total=len(relevant_ids), desc="Progress through docs"):
        file = doc_id + ".txt"

        with open(os.path.join(raw_files_path, file), "r", encoding="utf-8") as rf:
            file_text = rf.read()
        
        # annotate
        conllu_output = trankit2conllu(p(file_text))
        conllu_sents = conllu_output.split("\n\n")
        no_of_sents = len(conllu_sents)

        # prepare the final conllu and handle the ids
        final_conllu_text = ""
        for k in range(no_of_sents):  # k represents the sentence index
            if "\t" in conllu_sents[k]:
                final_conllu_text += f"# sent_id = {doc_id}.{str(k + 1)}\n{conllu_sents[k]}\n\n"
        
        # write to output file
        wf.write(final_conllu_text)
