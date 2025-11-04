from trankit import Pipeline, trankit2conllu
import os

model_path = os.path.join("..", "Models", "save_dir_ssj+sst")
raw_files_path = os.path.join("..", "Datasets", "Solar", "Solar_GPT-5", "raw")
output_path = os.path.join("..", "Datasets", "Solar", "Solar_GPT-5", "annotated")

p = Pipeline(lang="customize", cache_dir=model_path, embedding='xlm-roberta-large', gpu=True)

print("Done loading Trankit models!")

for file in os.listdir(raw_files_path):
    doc_id = file.split(".txt")[0]

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
    with open(os.path.join(output_path, file), "w", encoding="utf-8") as wf:
        wf.write(final_conllu_text)
